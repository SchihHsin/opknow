#!/usr/bin/env python3
"""Build the Word (.docx) editions of the English manuscript.

    python3 paper/ai-usability/scripts/build_manuscript_docx.py            # current revision
    python3 paper/ai-usability/scripts/build_manuscript_docx.py before     # pre-scoring-revision snapshot
    python3 paper/ai-usability/scripts/build_manuscript_docx.py ba96b79    # text before the indicator rework

The `current` profile writes paper/ai-usability/manuscript-en-v0.2.docx next
to the Markdown and reading-page editions of the same revision. The `before`
profile writes manuscript-en-v0.2-before-scoring-revision.docx from the frozen
snapshot in reviews/scoring-revision-20260921/before/, which holds its own copy
of the Markdown, the figure artwork and the bibliography as they stood before
the 21 September 2026 scoring revision.

The `ba96b79` profile writes manuscript-en-v0.2-before-indicator-rework.docx
and takes text, artwork and bibliography out of that commit: it is the last one
that touched the manuscript before the indicator rework, so it is the newest
state in which the composite confidence score M11 is still the single-step
formula. Nothing between it and the 21 September revision was ever committed.

The Markdown stays the single editable source. This script only re-lays it out:

  1. manuscript-en-v0.2.md  -> working Markdown: the H1 becomes document
     metadata, `##`/`###` are promoted one level so section numbering starts
     at 1 for Introduction, and Abstract/Keywords are unnumbered.
  2. figures/*-en.svg       -> PNG raster copies (Word cannot embed the SVG
     artwork; headless Chrome does the rasterisation, no extra tooling).
  3. pandoc 3.11 (bundled in submission/.tools) with the ACM citation style,
     the shared table-width filter and a styled reference.docx.
  4. OOXML post-processing: table-cell text style, A4 page setup, page-number
     footer, field refresh, document properties.

Every value below is the Word rendering of the reading page's own stylesheet
(paper/ai-usability/scripts/render_paper_reading.py), so the two editions show
the same palette, type scale and wording.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # paper/ai-usability
REPO = ROOT.parents[1]                              # repository root
BUILD = REPO / "tmp" / "paper-word-build"

PANDOC = ROOT / "submission" / ".tools" / "pandoc"
LUA = ROOT / "scripts" / "docx-layout.lua"
CSL = ROOT / "submission" / "acm-sig-proceedings.csl"
BEFORE_DIR = ROOT / "reviews" / "scoring-revision-20260921" / "before"

CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

# Front matter. The reading page renders the same strings; keep them in step.
AUTHORS = "时昕昱　·　闫浩　·　张敬文"
AFFILIATION = "Huawei Technologies (China)　·　Corresponding author: 闫浩"

REFERENCE = BUILD / "reference.docx"

# Editions of the same manuscript are buildable from this one script.
# `before` is the snapshot taken ahead of the 21 September 2026 scoring
# revision, which rewrote the indicator rules, the rubric figures and the
# bibliography; the results and discussion sections are word-for-word the same
# in both, so the two files differ only in methods and artwork.
# `ba96b79` reads text, artwork and bibliography straight out of git at that
# commit: the indicator rework that followed it was never committed, so this is
# the closest recoverable state to "before the indicators changed".
PROFILES = {
    "current": {
        "source": ROOT / "manuscript-en-v0.2.md",
        "figures": [ROOT / "figures"],
        "bib": ROOT / "references.bib",
        "output": ROOT / "manuscript-en-v0.2.docx",
        "subtitle": "English manuscript · v0.2 · 21 September 2026 · Methods revised, conclusion pending",
        "tag": "",
    },
    "before": {
        "source": BEFORE_DIR / "manuscript-en-v0.2.md",
        # The snapshot keeps only the artwork the revision replaced (Figure 1
        # and the four rubric figures). Everything else is unchanged, so it is
        # read from the live figures directory.
        "figures": [BEFORE_DIR / "figures", ROOT / "figures"],
        "bib": BEFORE_DIR / "references.bib",
        "output": ROOT / "manuscript-en-v0.2-before-scoring-revision.docx",
        "subtitle": "English manuscript · v0.2 · text before the 21 September 2026 scoring revision",
        "tag": "before",
    },
    "ba96b79": {
        # The last commit that touched the manuscript before the indicator
        # rework. Text, artwork and bibliography all come out of that commit.
        "git_rev": "ba96b79",
        "source": ROOT / "manuscript-en-v0.2.md",
        "figures_git": True,
        "bib": ROOT / "references.bib",
        "output": ROOT / "manuscript-en-v0.2-before-indicator-rework.docx",
        "subtitle": "English manuscript · v0.2 · commit ba96b79 · 12 September 2026 · text before the indicator rework",
        "tag": "before-indicator-rework",
    },
}


def git_export(rev: str, repo_path: Path, dest: Path) -> Path:
    """Write one repository file exactly as it stood at <rev>."""
    data = subprocess.run(
        ["git", "show", f"{rev}:{repo_path.relative_to(REPO).as_posix()}"],
        cwd=REPO, capture_output=True, check=True,
    ).stdout
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return dest


def use_profile(name: str) -> None:
    """Point every path in this module at one of the manuscript editions."""
    global SOURCE_MD, FIGURES, BIB, OUTPUT, SUBTITLE, WORK_MD, FIGURE_DIR
    p = PROFILES[name]
    FIGURES = p.get("figures", [])
    OUTPUT = p["output"]
    SUBTITLE = p["subtitle"]
    suffix = f"-{p['tag']}" if p["tag"] else ""
    WORK_MD = BUILD / f"manuscript-en{suffix}-docx.md"
    FIGURE_DIR = BUILD / f"figures{suffix}"
    if p.get("git_rev"):
        stamp = BUILD / f"git-{p['git_rev']}"
        SOURCE_MD = git_export(p["git_rev"], p["source"], stamp / "manuscript-en-v0.2.md")
        BIB = git_export(p["git_rev"], p["bib"], stamp / "references.bib")
        if p.get("figures_git"):
            # Take the artwork from the same commit as the text. Figure files
            # keep their names across revisions, so a file on disk is no
            # evidence of what this revision actually showed.
            figure_dir = stamp / "figures"
            stems = sorted(set(re.findall(
                r"\(figures/([^)\s]+)\.svg\)", SOURCE_MD.read_text(encoding="utf-8"))))
            for stem in stems:
                git_export(p["git_rev"], ROOT / "figures" / f"{stem}.svg",
                           figure_dir / f"{stem}.svg")
            FIGURES = [figure_dir]
            print(f"  figures from git {p['git_rev']}: {len(stems)}")
    else:
        SOURCE_MD = p["source"]
        BIB = p["bib"]


use_profile("current")

# --- Rasterisation ---------------------------------------------------------

# ~375 dpi at the printed 160 mm width: text inside the diagrams stays legible
# on screen and in print without inflating the .docx.
TARGET_PX = 2200
MAX_SCALE = 4.0
RENDER_TIMEOUT = 90


def svg_size(svg: Path) -> tuple[float, float]:
    head = svg.read_text(encoding="utf-8")[:4000]
    box = re.search(r'viewBox="([-\d.eE\s,]+)"', head)
    if box:
        parts = [float(v) for v in re.split(r"[\s,]+", box.group(1).strip()) if v]
        if len(parts) == 4 and parts[2] > 0 and parts[3] > 0:
            return parts[2], parts[3]
    w = re.search(r'\bwidth="([\d.]+)', head)
    h = re.search(r'\bheight="([\d.]+)', head)
    if w and h:
        return float(w.group(1)), float(h.group(1))
    raise ValueError(f"cannot read the canvas size of {svg.name}")


def render_png(svg: Path, png: Path) -> None:
    if png.exists() and png.stat().st_mtime >= svg.stat().st_mtime:
        return
    width, height = svg_size(svg)
    scale = min(MAX_SCALE, max(1.0, TARGET_PX / width))
    box_w, box_h = int(round(width)), int(round(height))
    wrapper = BUILD / f"_{svg.stem}.html"
    wrapper.write_text(
        "<!doctype html><html><head><meta charset=\"utf-8\"><style>"
        "html,body{margin:0;padding:0;background:#fff}"
        f"img{{display:block;width:{box_w}px;height:{box_h}px}}"
        "</style></head><body>"
        f'<img src="{svg.as_uri()}"></body></html>',
        encoding="utf-8",
    )
    png.parent.mkdir(parents=True, exist_ok=True)
    if png.exists():
        png.unlink()

    proc = subprocess.Popen(
        [
            str(CHROME), "--headless", "--no-sandbox", "--disable-gpu",
            "--hide-scrollbars", "--no-first-run", "--no-default-browser-check",
            "--disable-extensions", f"--user-data-dir={BUILD/'chrome-profile'}",
            f"--force-device-scale-factor={scale:g}",
            f"--window-size={box_w},{box_h}", f"--screenshot={png}",
            wrapper.as_uri(),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Chrome does not always exit after writing the shot, so wait on the file
    # and stop the process ourselves.
    deadline = time.time() + RENDER_TIMEOUT
    settled = -1
    while time.time() < deadline:
        if png.exists():
            size = png.stat().st_size
            if size and size == settled:
                break
            settled = size
        time.sleep(0.4)
    proc.kill()
    proc.wait()
    wrapper.unlink(missing_ok=True)
    if not png.exists() or png.stat().st_size == 0:
        raise RuntimeError(f"headless Chrome did not render {svg.name}")
    print(f"  {svg.name} -> {png.name}  {png.stat().st_size // 1024} KB  x{scale:g}")


def find_figure(stem: str) -> Path:
    """First matching <stem>.svg across the profile's figure directories."""
    for directory in FIGURES:
        candidate = directory / f"{stem}.svg"
        if candidate.exists():
            return candidate
    raise SystemExit(f"no SVG for {stem!r} in " + ", ".join(str(d) for d in FIGURES))


def render_figures(markdown: str) -> None:
    sources = sorted(set(re.findall(r"\(figures/([^)\s]+)\.svg\)", markdown)))
    print(f"figures: {len(sources)} referenced")
    for stem in sources:
        svg = find_figure(stem)
        try:
            origin = svg.parent.relative_to(ROOT)
        except ValueError:                       # exported from git into tmp/
            origin = svg.parent.relative_to(REPO)
        note = "" if origin == Path("figures") else f"  [{origin}]"
        render_png(svg, FIGURE_DIR / f"{stem}.png")
        if note:
            print(f"  {stem}: from {origin}")


# --- Working Markdown ------------------------------------------------------

def working_markdown() -> tuple[str, str]:
    lines = SOURCE_MD.read_text(encoding="utf-8").split("\n")
    if not lines[0].startswith("# "):
        raise SystemExit("manuscript-en-v0.2.md no longer starts with the title H1")
    title = lines[0][2:].strip()
    body = "\n".join(lines[1:])
    # Promote one level so the first numbered heading is Introduction = 1.
    body = re.sub(r"^## ", "# ", body, flags=re.M)
    body = re.sub(r"^### ", "## ", body, flags=re.M)
    # Front matter must not consume section numbers.
    body = re.sub(r"^# (Abstract|Keywords)$", r"# \1 {.unnumbered}", body, flags=re.M)
    return title, body


# --- reference.docx --------------------------------------------------------

INK, MUTED, LINE = "24313D", "536574", "DCE3E7"
ACCENT, STRONG, LINK = "176253", "173C36", "176D70"
HEAD_BG, BLOCK_BG, BLOCK_RULE, CODE_BG, ZEBRA = "EEF4F2", "FAF5E9", "BC8C38", "F2F4F6", "FAFCFC"
SERIF, SANS, MONO = "Georgia", "Arial", "Consolas"


def rpr(font=SERIF, size=None, color=INK, bold=False, italic=False, spacing=None) -> str:
    bits = [f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:eastAsia="{font}" w:cs="{font}"/>']
    if bold:
        bits.append("<w:b/><w:bCs/>")
    if italic:
        bits.append("<w:i/><w:iCs/>")
    if spacing:
        bits.append(f'<w:spacing w:val="{spacing}"/>')
    if color:
        bits.append(f'<w:color w:val="{color}"/>')
    if size:
        bits.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    return "<w:rPr>" + "".join(bits) + "</w:rPr>"


def para_style(sid, name, *, based="Normal", nxt=None, ppr="", rpr_xml="", custom=False,
               is_default=False):
    flag = ' w:customStyle="1"' if custom else ""
    if is_default:
        flag = ' w:default="1"'
    xml = [f'<w:style w:type="paragraph"{flag} w:styleId="{sid}">']
    xml.append(f'<w:name w:val="{name}"/>')
    if based:
        xml.append(f'<w:basedOn w:val="{based}"/>')
    if nxt:
        xml.append(f'<w:next w:val="{nxt}"/>')
    xml.append("<w:qFormat/>")
    if ppr:
        xml.append(f"<w:pPr>{ppr}</w:pPr>")
    if rpr_xml:
        xml.append(rpr_xml)
    xml.append("</w:style>")
    return "".join(xml)


BODY_PPR = '<w:spacing w:before="0" w:after="120" w:line="300" w:lineRule="auto"/><w:jc w:val="both"/>'
HEAD_PPR = '<w:keepNext/><w:keepLines/>'


def styles_xml(original: str) -> str:
    defs = []

    defaults = (
        "<w:docDefaults><w:rPrDefault>"
        + rpr(font=SERIF, size=21)
        + '<w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="ar-SA"/></w:rPrDefault>'
        '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="300" w:lineRule="auto"/>'
        '<w:jc w:val="both"/></w:pPr></w:pPrDefault></w:docDefaults>'
    )

    def paragraph(sid, name, ppr, r, **kw):
        defs.append(para_style(sid, name, ppr=ppr, rpr_xml=r, **kw))

    paragraph("Normal", "Normal", '<w:spacing w:before="0" w:after="120" w:line="300" w:lineRule="auto"/><w:jc w:val="both"/>',
              rpr(size=21), based=None, is_default=True)
    paragraph("BodyText", "Body Text", BODY_PPR, rpr(size=21), based="Normal", nxt="BodyText")
    paragraph("FirstParagraph", "First Paragraph", BODY_PPR, rpr(size=21), based="BodyText",
              nxt="BodyText", custom=True)
    # Appendix A's rubric levels: numbered list items, body-adjacent size.
    paragraph("Compact", "Compact", '<w:spacing w:before="0" w:after="60" w:line="280" w:lineRule="auto"/>'
              '<w:contextualSpacing/><w:jc w:val="both"/>', rpr(size=20), based="Normal", custom=True)
    # Footnotes/captions inside cells would otherwise inherit Compact.
    paragraph("FootnoteText", "Footnote Text", '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>',
              rpr(size=18, color=MUTED), based="Normal")

    # Headings: the reading page's h2 (top rule + strong green) and h3 (accent).
    paragraph("Heading1", "heading 1",
              HEAD_PPR + '<w:spacing w:before="360" w:after="120"/>'
              f'<w:pBdr><w:top w:val="single" w:sz="6" w:space="10" w:color="{LINE}"/></w:pBdr>'
              '<w:outlineLvl w:val="0"/>',
              rpr(font=SERIF, size=30, color=STRONG, bold=True), based="Normal", nxt="BodyText")
    paragraph("Heading2", "heading 2",
              HEAD_PPR + '<w:spacing w:before="240" w:after="80"/><w:outlineLvl w:val="1"/>',
              rpr(font=SERIF, size=24, color=ACCENT, bold=True), based="Normal", nxt="BodyText")
    paragraph("Heading3", "heading 3",
              HEAD_PPR + '<w:spacing w:before="200" w:after="60"/><w:outlineLvl w:val="2"/>',
              rpr(font=SERIF, size=22, color=STRONG, bold=True), based="Normal", nxt="BodyText")
    paragraph("Heading4", "heading 4",
              HEAD_PPR + '<w:spacing w:before="160" w:after="40"/><w:outlineLvl w:val="3"/>',
              rpr(font=SERIF, size=21, color=MUTED, bold=True, italic=True), based="Normal", nxt="BodyText")
    for level in range(5, 10):
        paragraph(f"Heading{level}", f"heading {level}",
                  HEAD_PPR + f'<w:spacing w:before="140" w:after="40"/><w:outlineLvl w:val="{level - 1}"/>',
                  rpr(font=SERIF, size=20, color=MUTED, bold=True), based="Normal", nxt="BodyText")

    # Front matter.
    paragraph("Title", "Title", '<w:spacing w:before="0" w:after="80" w:line="280" w:lineRule="auto"/>'
              '<w:jc w:val="left"/>', rpr(font=SERIF, size=42, color=INK, bold=True), based="Normal")
    paragraph("Subtitle", "Subtitle", '<w:spacing w:before="0" w:after="40"/><w:jc w:val="left"/>',
              rpr(font=SANS, size=16, color=MUTED, spacing=12), based="Normal", nxt="Author")
    paragraph("Author", "Author", '<w:spacing w:before="160" w:after="0"/><w:jc w:val="left"/>',
              rpr(font=SANS, size=22, color=MUTED), based="Normal", nxt="Date", custom=True)
    paragraph("Date", "Date", '<w:spacing w:before="40" w:after="200"/><w:jc w:val="left"/>',
              rpr(font=SANS, size=17, color=MUTED), based="Normal", nxt="BodyText")

    # Revision-status callouts.
    paragraph("BlockText", "Block Text",
              '<w:spacing w:before="200" w:after="200" w:line="300" w:lineRule="auto"/>'
              '<w:ind w:left="240" w:right="240" w:firstLine="0"/>'
              f'<w:pBdr><w:left w:val="single" w:sz="18" w:space="10" w:color="{BLOCK_RULE}"/></w:pBdr>'
              f'<w:shd w:val="clear" w:color="auto" w:fill="{BLOCK_BG}"/>',
              rpr(font=SANS, size=19, color=INK), based="BodyText", nxt="BodyText")

    # Figures and tables.
    caption = '<w:spacing w:before="0" w:after="240" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/>'
    figure_ppr = '<w:spacing w:before="200" w:after="0" w:line="240" w:lineRule="auto"/>' \
                 '<w:keepNext/><w:jc w:val="center"/>'
    paragraph("Caption", "Caption", caption, rpr(font=SANS, size=17, color=MUTED), based="Normal")
    paragraph("ImageCaption", "Image Caption", caption, rpr(font=SANS, size=17, color=MUTED),
              based="Caption", custom=True)
    paragraph("TableCaption", "Table Caption",
              '<w:spacing w:before="200" w:after="60"/><w:keepNext/><w:jc w:val="left"/>',
              rpr(font=SANS, size=17, color=MUTED), based="Caption", custom=True)
    paragraph("CaptionedFigure", "Captioned Figure", figure_ppr, rpr(size=17), based="Normal", custom=True)
    paragraph("Figure", "Figure", figure_ppr, rpr(size=17), based="Normal", custom=True)
    paragraph("TableCell", "Table Cell Text",
              '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
              '<w:contextualSpacing/><w:jc w:val="left"/>',
              rpr(font=SANS, size=17, color=INK), based="Normal", custom=True)

    paragraph("Bibliography", "Bibliography",
              '<w:spacing w:before="0" w:after="120" w:line="260" w:lineRule="auto"/>'
              '<w:ind w:left="360" w:hanging="360"/><w:jc w:val="left"/>',
              rpr(font=SERIF, size=17), based="Normal", nxt="Bibliography")

    # Code.
    defs.append(
        '<w:style w:type="paragraph" w:customStyle="1" w:styleId="SourceCode">'
        '<w:name w:val="Source Code"/><w:basedOn w:val="Normal"/><w:qFormat/>'
        '<w:pPr><w:spacing w:before="120" w:after="120" w:line="240" w:lineRule="auto"/>'
        f'<w:shd w:val="clear" w:color="auto" w:fill="{CODE_BG}"/>'
        '<w:ind w:left="240" w:firstLine="0"/><w:jc w:val="left"/></w:pPr>'
        + rpr(font=MONO, size=18, color=INK) + "</w:style>"
    )

    # Contents.
    paragraph("TOCHeading", "TOC Heading",
              HEAD_PPR + '<w:spacing w:before="240" w:after="120"/>'
              f'<w:pBdr><w:top w:val="single" w:sz="6" w:space="10" w:color="{LINE}"/></w:pBdr>'
              '<w:outlineLvl w:val="9"/>',
              rpr(font=SERIF, size=30, color=STRONG, bold=True), based="Normal", nxt="BodyText")
    for level in range(1, 4):
        indent = "" if level == 1 else f'<w:ind w:left="{(level - 1) * 240}"/>'
        defs.append(
            f'<w:style w:type="paragraph" w:styleId="TOC{level}">'
            f'<w:name w:val="toc {level}"/><w:basedOn w:val="Normal"/><w:next w:val="BodyText"/>'
            '<w:qFormat/>'
            '<w:pPr>'
            f'<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9078"/></w:tabs>'
            f'<w:spacing w:before="60" w:after="60" w:line="260" w:lineRule="auto"/>'
            f'{indent}<w:jc w:val="left"/></w:pPr>'
            + rpr(font=SERIF, size=20 if level == 1 else 19, color=INK) + "</w:style>"
        )

    # Footer.
    paragraph("Footer", "Footer",
              '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/>',
              rpr(font=SANS, size=16, color=MUTED), based="Normal", custom=True)

    # Character styles.
    defs.append(
        '<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont">'
        '<w:name w:val="Default Paragraph Font"/><w:uiPriority w:val="1"/>'
        '<w:semiHidden/><w:unhideWhenUsed/></w:style>'
    )
    defs.append(
        '<w:style w:type="character" w:customStyle="1" w:styleId="SectionNumber">'
        '<w:name w:val="Section Number"/><w:basedOn w:val="DefaultParagraphFont"/>'
        f'<w:rPr><w:rFonts w:ascii="{SERIF}" w:hAnsi="{SERIF}" w:eastAsia="{SERIF}" w:cs="{SERIF}"/>'
        '<w:noProof/></w:rPr></w:style>'
    )
    defs.append(
        '<w:style w:type="character" w:customStyle="1" w:styleId="VerbatimChar">'
        '<w:name w:val="Verbatim Char"/><w:basedOn w:val="DefaultParagraphFont"/>'
        + rpr(font=MONO, size=18, color=INK).replace(
            "<w:rPr>", f'<w:rPr><w:shd w:val="clear" w:color="auto" w:fill="{CODE_BG}"/>')
        + "</w:style>"
    )
    defs.append(
        '<w:style w:type="character" w:styleId="Hyperlink">'
        '<w:name w:val="Hyperlink"/><w:basedOn w:val="DefaultParagraphFont"/>'
        f'<w:rPr><w:color w:val="{LINK}"/><w:u w:val="single"/></w:rPr></w:style>'
    )
    defs.append(
        '<w:style w:type="character" w:styleId="FootnoteReference">'
        '<w:name w:val="footnote reference"/><w:basedOn w:val="DefaultParagraphFont"/>'
        '<w:rPr><w:vertAlign w:val="superscript"/></w:rPr></w:style>'
    )

    # Table: the reading page's rules, header band and zebra striping.
    defs.append(
        '<w:style w:type="table" w:default="1" w:styleId="Table">'
        '<w:name w:val="Table"/><w:qFormat/>'
        '<w:tblPr>'
        f'<w:tblBorders>'
        + "".join(f'<w:{edge} w:val="single" w:sz="6" w:space="0" w:color="{LINE}"/>'
                  for edge in ("top", "left", "bottom", "right", "insideH", "insideV"))
        + "</w:tblBorders>"
        '<w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="120" w:type="dxa"/>'
        '<w:bottom w:w="60" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tblCellMar>'
        "</w:tblPr>"
        '<w:tblStylePr w:type="firstRow">'
        f'<w:rPr><w:b/><w:bCs/></w:rPr>'
        f'<w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{HEAD_BG}"/></w:tcPr>'
        "</w:tblStylePr>"
        '<w:tblStylePr w:type="band2Horz">'
        f'<w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{ZEBRA}"/></w:tcPr>'
        "</w:tblStylePr>"
        "</w:style>"
    )

    # Definition lists are not used by this manuscript but pandoc emits the
    # styles when they appear; keep Word from reporting them as missing.
    defs.append('<w:style w:type="paragraph" w:styleId="DefinitionTerm"><w:name w:val="Definition Term"/>'
                '<w:basedOn w:val="Normal"/><w:qFormat/></w:style>')
    defs.append('<w:style w:type="paragraph" w:styleId="Definition"><w:name w:val="Definition"/>'
                '<w:basedOn w:val="Normal"/><w:qFormat/></w:style>')

    replaced = {
        "Normal", "BodyText", "FirstParagraph", "Compact", "FootnoteText",
        "Heading1", "Heading2", "Heading3", "Heading4", "Heading5", "Heading6",
        "Heading7", "Heading8", "Heading9",
        "Title", "Subtitle", "Author", "Date", "BlockText",
        "Caption", "ImageCaption", "TableCaption", "CaptionedFigure", "Figure",
        "Bibliography", "TOCHeading", "TOC1", "TOC2", "TOC3", "Footer",
        "DefaultParagraphFont", "SectionNumber", "VerbatimChar", "Hyperlink",
        "FootnoteReference", "Table", "DefinitionTerm", "Definition",
        "SourceCode",
    }
    xml = re.sub(r"<w:docDefaults>.*?</w:docDefaults>", defaults, original, flags=re.S)
    for sid in sorted(replaced):
        xml = re.sub(r'<w:style [^>]*w:styleId="%s">.*?</w:style>' % re.escape(sid), "", xml, flags=re.S)
    xml = xml.replace("</w:styles>", "".join(defs) + "</w:styles>")
    return xml


FOOTER_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    '<w:p><w:pPr><w:pStyle w:val="Footer"/></w:pPr>'
    '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
    '<w:r><w:instrText xml:space="preserve">PAGE</w:instrText></w:r>'
    '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
    '<w:r><w:t>1</w:t></w:r>'
    '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
    "</w:p></w:ftr>"
)


def build_reference() -> None:
    raw = subprocess.run(
        [str(PANDOC), "--print-default-data-file", "reference.docx"],
        capture_output=True, check=True,
    ).stdout
    tmp = BUILD / "_reference-default.docx"
    tmp.write_bytes(raw)
    with zipfile.ZipFile(tmp) as zin:
        parts = {name: zin.read(name) for name in zin.namelist()}

    styles = parts["word/styles.xml"].decode("utf-8")
    parts["word/styles.xml"] = styles_xml(styles).encode("utf-8")

    # Pandoc keeps only this section's properties, so page setup lives here.
    doc = parts["word/document.xml"].decode("utf-8")
    sect = (
        "<w:sectPr>"
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1247" w:right="1247" w:bottom="1247" w:left="1247"'
        ' w:header="720" w:footer="720" w:gutter="0"/>'
        '<w:cols w:space="720"/><w:docGrid w:linePitch="360"/>'
        "</w:sectPr>"
    )
    doc = re.sub(r"<w:sectPr>.*?</w:sectPr>", sect, doc, count=1, flags=re.S)
    parts["word/document.xml"] = doc.encode("utf-8")

    with zipfile.ZipFile(REFERENCE, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in parts.items():
            zout.writestr(name, data)
    tmp.unlink()
    print(f"reference.docx: {REFERENCE.stat().st_size // 1024} KB")


# --- pandoc ----------------------------------------------------------------

def run_pandoc(title: str) -> None:
    cmd = [
        str(PANDOC), str(WORK_MD),
        "--from=markdown+tex_math_dollars+implicit_figures",
        "--to=docx",
        "--citeproc",
        f"--bibliography={BIB}",
        f"--csl={CSL}",
        f"--lua-filter={LUA}",
        f"--reference-doc={REFERENCE}",
        "--number-sections",
        "--toc",
        "--toc-depth=3",
        "-M", f"title={title}",
        "-M", f"subtitle={SUBTITLE}",
        "-M", f"author={AUTHORS}",
        "-M", f"date={AFFILIATION}",
        "-M", "reference-section-title=References",
        "-M", "lang=en-US",
        "-o", str(OUTPUT),
    ]
    result = subprocess.run(cmd, cwd=BUILD, capture_output=True, text=True)
    for line in result.stderr.splitlines():
        if line.strip():
            print("  pandoc:", line.strip())
    if result.returncode != 0:
        raise SystemExit("pandoc failed")
    print(f"pandoc: {OUTPUT.stat().st_size // 1024} KB")


# --- OOXML post-processing -------------------------------------------------

def postprocess(title: str) -> int:
    with zipfile.ZipFile(OUTPUT) as zin:
        parts = {name: zin.read(name) for name in zin.namelist()}

    doc = parts["word/document.xml"].decode("utf-8")

    # Pandoc shares one "Compact" style between list items and table cells.
    # Table cells need the smaller sans setting; lists keep body size.
    def retag(match: re.Match) -> str:
        return match.group(0).replace('w:pStyle w:val="Compact"', 'w:pStyle w:val="TableCell"')

    doc, table_hits = re.subn(r"<w:tbl>.*?</w:tbl>", retag, doc, flags=re.S)
    table_cells = doc.count('w:pStyle w:val="TableCell"')

    # Page-number footer, and refresh the TOC field when Word opens the file.
    doc = re.sub(
        r"(<w:sectPr[^>]*>)",
        r'\1<w:footerReference w:type="default" r:id="rIdFtr"/>',
        doc, count=1,
    )
    doc = re.sub(r"<w:pgSz\b[^>]*/>", '<w:pgSz w:w="11906" w:h="16838"/>', doc, count=1)
    doc = re.sub(
        r"<w:pgMar\b[^>]*/>",
        '<w:pgMar w:top="1247" w:right="1247" w:bottom="1247" w:left="1247"'
        ' w:header="720" w:footer="720" w:gutter="0"/>',
        doc, count=1,
    )
    parts["word/document.xml"] = doc.encode("utf-8")
    parts["word/footer1.xml"] = FOOTER_XML.encode("utf-8")

    rels = parts["word/_rels/document.xml.rels"].decode("utf-8")
    if "footer1.xml" not in rels:
        rels = rels.replace(
            "</Relationships>",
            '<Relationship Type="http://schemas.openxmlformats.org/officeDocument/2006/'
            'relationships/footer" Id="rIdFtr" Target="footer1.xml"/></Relationships>',
        )
    parts["word/_rels/document.xml.rels"] = rels.encode("utf-8")

    types = parts["[Content_Types].xml"].decode("utf-8")
    if "footer1.xml" not in types:
        types = types.replace(
            "</Types>",
            '<Override PartName="/word/footer1.xml" ContentType="application/vnd.'
            'openxmlformats-officedocument.wordprocessingml.footer+xml"/></Types>',
        )
    parts["[Content_Types].xml"] = types.encode("utf-8")

    settings = parts["word/settings.xml"].decode("utf-8")
    if "updateFields" not in settings:
        # CT_Settings is an ordered sequence. Pandoc's settings.xml ends its
        # ordered run at savePreviewPicture, so updateFields goes next, before
        # rsids, which is where the schema expects it.
        settings = settings.replace(
            "<w:rsids>", '<w:updateFields w:val="true" /><w:rsids>', 1
        )
    parts["word/settings.xml"] = settings.encode("utf-8")

    core = parts["docProps/core.xml"].decode("utf-8")
    core = re.sub(r"<dc:title>.*?</dc:title>",
                  f"<dc:title>{escape(title)}</dc:title>", core, flags=re.S)
    core = re.sub(r"<dc:creator>.*?</dc:creator>",
                  "<dc:creator>Schih Hsin (paper manuscript build)</dc:creator>", core, flags=re.S)
    parts["docProps/core.xml"] = core.encode("utf-8")

    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in parts.items():
            zout.writestr(name, data)

    print(f"post-processed: {table_cells} table cell paragraphs, footer + page setup applied")
    return table_hits


def escape(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# --- report ----------------------------------------------------------------

def report() -> None:
    with zipfile.ZipFile(OUTPUT) as z:
        names = z.namelist()
        doc = z.read("word/document.xml").decode("utf-8")
        styles = z.read("word/styles.xml").decode("utf-8")

    text = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", doc))
    print("\nbuild report")
    print(f"  file          {OUTPUT}  ({OUTPUT.stat().st_size / 1048576:.1f} MB)")
    print(f"  media         {len([n for n in names if n.startswith('word/media/')])} images")
    print(f"  tables        {doc.count('<w:tbl>')}")
    print(f"  equations     {doc.count('<m:oMath')}")
    print(f"  headings      {len(re.findall(r'w:pStyle w:val=\"Heading[0-9]\"', doc))}")
    print(f"  characters    {len(text):,}")
    print(f"  TOC field     {'TOC ' in doc}")
    print(f"  footer        {'footer1.xml' in ' '.join(names)}")
    print(f"  numbered      {'SectionNumber' in doc}")
    missing = [s for s in ("TableCell", "CaptionedFigure", "BlockText", "Bibliography", "TOC1")
               if f'w:styleId="{s}"' not in styles]
    print(f"  styles        {'all present' if not missing else 'MISSING ' + ', '.join(missing)}")


if __name__ == "__main__":
    profile = next((a for a in sys.argv[1:] if not a.startswith("-")), "current")
    if profile not in PROFILES:
        raise SystemExit(f"unknown profile {profile!r}; pick one of: {', '.join(PROFILES)}")
    use_profile(profile)

    BUILD.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"profile {profile}  ->  {OUTPUT.relative_to(ROOT)}")
    print(f"  source      {SOURCE_MD.relative_to(REPO)}")
    print(f"  bib         {BIB.relative_to(REPO)}")
    print(f"  figures     {', '.join(str(d.relative_to(REPO)) for d in FIGURES)}")

    print("1/5 working Markdown")
    title, body = working_markdown()
    WORK_MD.write_text(body, encoding="utf-8")
    print(f"  title: {title[:70]}…")

    print("2/5 figures")
    render_figures(body)

    print("3/5 reference.docx")
    build_reference()

    print("4/5 pandoc")
    run_pandoc(title)

    print("5/5 OOXML post-processing")
    postprocess(title)

    report()
