#!/usr/bin/env python3
"""Convert the English Markdown manuscript to an anonymous, genuine acmart PDF.

No paper text is stored in this script. Pandoc supplies the Markdown parser and
LaTeX writer; Tectonic runs the ACM class and ACM BibTeX style. Source files and
the bibliography are staged with relative paths so the compiled paper and the
optional source archive contain no local account paths.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
PAPER = ROOT.parent
PROJECT = PAPER.parent.parent
EXPECTED_TITLE = "Can AI Find What Developers Need? Defining and Measuring Knowledge Availability for AI in Developer Ecosystems"


def find_binary(name: str) -> str:
    candidates = [os.environ.get(name.upper()), shutil.which(name), str(ROOT / ".tools" / name)]
    if name == "tectonic":
        candidates += [str(path) for path in sorted(
            (Path.home() / ".codex/plugins/cache/openai-bundled/latex").glob("*/bin/tectonic"), reverse=True
        )]
        candidates += ["/opt/homebrew/bin/tectonic", "/usr/local/bin/tectonic"]
    for candidate in candidates:
        if candidate and Path(candidate).is_file() and os.access(candidate, os.X_OK):
            return candidate
    instruction = "Run python3 submission/bootstrap_tools.py, or set PANDOC." if name == "pandoc" else "Set TECTONIC to a local Tectonic executable."
    raise ValueError(f"Cannot find {name}. {instruction}")


def run(command: list[str], *, data: str | None = None, cwd: Path | None = None) -> str:
    result = subprocess.run(command, input=data, text=True, capture_output=True, cwd=cwd, check=False)
    if result.returncode:
        raise ValueError(f"Command failed ({Path(command[0]).name}):\n{result.stdout}\n{result.stderr}")
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)
    return result.stdout


def flatten(value) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(flatten(item) for item in value)
    if isinstance(value, dict):
        if value.get("t") in {"Space", "SoftBreak", "LineBreak"}:
            return " "
        if value.get("t") == "Code":
            return value["c"][1]
        if value.get("t") == "Link":
            return flatten(value["c"][1])
        return flatten(value.get("c", ""))
    return ""


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def prepare(document: dict, source: Path, stage: Path, bibliography: Path) -> dict:
    meta = document["meta"]
    blocks = document["blocks"]
    # A visible H1 title is accepted in addition to ordinary YAML title metadata.
    if blocks and blocks[0].get("t") == "Header" and blocks[0]["c"][0] == 1:
        meta.setdefault("title", {"t": "MetaInlines", "c": blocks.pop(0)["c"][2]})
    title = flatten(meta.get("title", {})).strip()
    if title != EXPECTED_TITLE:
        raise ValueError(f"The manuscript must retain the agreed title. Found: {title!r}")

    remaining = []
    i = 0
    while i < len(blocks):
        block = blocks[i]
        if block.get("t") == "Header":
            level, _, text = block["c"]
            heading = flatten(text).strip().lower()
            if heading in {"abstract", "keywords"}:
                collected = []
                i += 1
                while i < len(blocks) and not (blocks[i].get("t") == "Header" and blocks[i]["c"][0] <= level):
                    collected.append(blocks[i])
                    i += 1
                if heading == "abstract":
                    meta[heading] = {"t": "MetaBlocks", "c": collected}
                else:
                    meta[heading] = {"t": "MetaString", "c": " ".join(flatten(item) for item in collected).strip()}
                continue
        remaining.append(block)
        i += 1
    if not flatten(meta.get("abstract", {})).strip():
        raise ValueError("Missing Abstract section or abstract metadata.")

    headers = [block["c"][0] for block in remaining if block.get("t") == "Header"]
    shift = (min(headers) - 1) if headers else 0
    for block in remaining:
        if block.get("t") == "Header":
            block["c"][0] = max(1, block["c"][0] - shift)
            # Strip an explicitly typed numeric section prefix, if one exists.
            inlines = block["c"][2]
            if inlines and inlines[0].get("t") == "Str":
                inlines[0]["c"] = re.sub(r"^\d+(?:\.\d+)*\.?\s*", "", inlines[0]["c"])
                if not inlines[0]["c"]:
                    inlines.pop(0)
                    if inlines and inlines[0].get("t") == "Space":
                        inlines.pop(0)
    document["blocks"] = remaining
    # Do not carry identifying author metadata from a draft into the LaTeX writer.
    for key in ("author", "authors", "affiliation", "email", "date", "thanks"):
        meta.pop(key, None)

    files = []
    citations = set()
    for node in walk(document):
        if node.get("t") == "Cite":
            citations.update(item["citationId"] for item in node["c"][0])
        if node.get("t") != "Image":
            continue
        target = node["c"][2][0]
        if re.match(r"^[a-z]+:", target, flags=re.I):
            raise ValueError(f"Use a local figure file, not a remote/absolute URI: {target}")
        image = (source.parent / target).resolve()
        if image.suffix.lower() == ".svg":
            image = image.with_suffix(".pdf")
        if not image.is_file():
            raise ValueError(f"Missing PDF/raster figure: {image}. Export SVG figures to adjacent PDFs first.")
        if image.suffix.lower() not in {".pdf", ".png", ".jpg", ".jpeg"}:
            raise ValueError(f"Unsupported LaTeX figure type: {image.suffix}")
        target_relative = Path("figures") / image.name
        target_file = stage / target_relative
        target_file.parent.mkdir(exist_ok=True)
        shutil.copyfile(image, target_file)
        node["c"][2][0] = target_relative.as_posix()
        files.append(target_relative.as_posix())

    bib_text = bibliography.read_text(encoding="utf-8")
    keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib_text))
    missing = sorted(citations - keys)
    if missing:
        raise ValueError(f"Citations missing from references.bib: {', '.join(missing)}")
    shutil.copyfile(bibliography, stage / "references.bib")
    return {
        "source": source.name,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "bibliography_sha256": hashlib.sha256(bibliography.read_bytes()).hexdigest(),
        "figure_files": sorted(set(files)),
        "cited_keys": sorted(citations),
        "title": title,
        "format": "acmart: manuscript,review,anonymous",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=PAPER / "manuscript-en-v0.2.md")
    parser.add_argument("--bibliography", type=Path, default=PAPER / "references.bib")
    parser.add_argument("--output", type=Path, default=PROJECT / "output/pdf/knowledge-availability-ai-chi2027-en-v0.2.pdf")
    parser.add_argument("--template", type=Path, default=ROOT / "acm-review-template.tex", help="ACM Pandoc template; the default remains the anonymous submission template.")
    parser.add_argument("--no-pdf", action="store_true", help="Generate and validate LaTeX inputs without compiling a PDF.")
    parser.add_argument("--only-cached", action="store_true", help="Tell Tectonic to use cached TeX packages only.")
    parser.add_argument("--package", action="store_true", help="Also create a portable LaTeX source ZIP inside submission/.")
    args = parser.parse_args()
    source = args.source.resolve()
    bibliography = args.bibliography.resolve()
    template = args.template.resolve()
    if not source.is_file() or not bibliography.is_file() or not template.is_file():
        raise ValueError("The English manuscript, bibliography, and ACM template must all exist before building.")
    pandoc = find_binary("pandoc")
    stage = ROOT / "_build"
    stage.mkdir(exist_ok=True)
    document = json.loads(run([
        pandoc, str(source), "--from=markdown+tex_math_dollars+raw_tex+implicit_figures", "--to=json"
    ]))
    manifest = prepare(document, source, stage, bibliography)
    latex = run([
        pandoc, "--from=json", "--to=latex", "--standalone", "--natbib", "--number-sections",
        "--syntax-highlighting=none", "--wrap=none", "--template", str(template),
        "--lua-filter", str(ROOT / "acm-figures.lua"),
    ], data=json.dumps(document, ensure_ascii=False))
    if "/Users/" in latex or "file://" in latex:
        raise ValueError("Identifying local paths found in generated LaTeX; remove them from the manuscript.")
    (stage / "main.tex").write_text(latex, encoding="utf-8")
    manifest["pandoc_version"] = run([pandoc, "--version"]).splitlines()[0]

    if not args.no_pdf:
        tectonic = find_binary("tectonic")
        manifest["tectonic_version"] = run([tectonic, "--version"]).strip()
        command = [tectonic, "--keep-logs", "--keep-intermediates", "--print"]
        if args.only_cached:
            command.append("--only-cached")
        command.append("main.tex")
        compiled = subprocess.run(command, cwd=stage, text=True, capture_output=True, check=False)
        transcript = compiled.stdout + "\n" + compiled.stderr
        (stage / "build.log").write_text(transcript, encoding="utf-8")
        if compiled.returncode or not (stage / "main.pdf").is_file():
            raise ValueError(f"ACM compilation failed. Full log: {stage / 'build.log'}\n{transcript[-7000:]}")
        latex_log = (stage / "main.log").read_text(errors="replace") if (stage / "main.log").is_file() else ""
        # Tectonic's combined transcript contains expected first-pass citation
        # warnings. Only its final TeX pass and final BibTeX log are decisive.
        bib_log = (stage / "main.blg").read_text(errors="replace") if (stage / "main.blg").is_file() else ""
        if re.search(r"Citation .+ undefined|There were undefined citations|I couldn't open database file|Warning--I didn't find a database entry", latex_log + bib_log):
            raise ValueError(f"Unresolved bibliography entries. See {stage / 'build.log'}")
        output = args.output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(stage / "main.pdf", output)
        manifest["pdf_filename"] = output.name
        manifest["pdf_sha256"] = hashlib.sha256(output.read_bytes()).hexdigest()
        print(f"ACM review PDF: {output}")
        warnings = [line for line in transcript.splitlines() if "warning:" in line.lower()]
        if warnings:
            print("Compilation warnings (inspect layout before delivery):\n" + "\n".join(warnings[-20:]))
    (stage / "build-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    if args.package:
        archive_path = ROOT / "knowledge-availability-ai-acm-source-v0.2.zip"
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name in ["main.tex", "references.bib"] + manifest["figure_files"]:
                archive.write(stage / name, arcname=name)
        print(f"Portable ACM LaTeX source: {archive_path}")
    print(f"Generated LaTeX: {stage / 'main.tex'}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        raise SystemExit(str(error)) from error
