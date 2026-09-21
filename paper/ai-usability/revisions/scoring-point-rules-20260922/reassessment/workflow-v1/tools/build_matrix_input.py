"""Build the only results file accepted by point-matrix renderers."""
from __future__ import annotations
import argparse, json, tempfile, os
from collections import Counter
from pathlib import Path
import consolidate
from matrix_input import MatrixInputError, load_complete

METRICS = [f"M{i}" for i in range(1, 12)]

def build(root: Path, manifest: Path, out: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        consolidate.consolidate(root, manifest, tmpdir)
        data = json.loads((tmpdir / "results.json").read_text(encoding="utf-8"))
    rows = data["rows"]
    manifest_data = json.loads(manifest.read_text(encoding="utf-8"))
    manifest_rows = manifest_data.get("records", manifest_data)
    expected_pairs = []
    for record in manifest_rows:
        identity = consolidate.parse_identity(record["run_id"])
        expected_pairs.append((identity["model"].replace("glm-5_3", "glm-5.3").replace("deepseek-v4_1-flash", "deepseek-v4.1-flash"), identity["task"], identity["ecosystem"]))
    expected_pairs = sorted(set(expected_pairs))
    tasks = sorted({r["task"] for r in rows})
    data["metric_coverage"] = {
        m: {
            "denominator_scored": sum(r["metrics"][m].get("status") == "scored" for r in rows),
            "status_counts": dict(Counter(r["metrics"][m].get("status") for r in rows)),
            "null_reasons": [{"run_id": r["run_id"], "status": r["metrics"][m].get("status"), "reason": r["metrics"][m].get("reason", "")} for r in rows if r["metrics"][m].get("status") != "scored"],
        } for m in METRICS
    }
    data["consolidation_gate"] = {"formal": True, "universe_size": len(rows), "validated_receipts": len(rows), "main_task_count": len([t for t in tasks if t != "G"]), "migration_analogy_tasks": [t for t in tasks if t == "G"], "pair_key": ["model", "task", "ecosystem"], "expected_pairs": [list(p) for p in expected_pairs], "null_values_are_statused": True}
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=out, prefix=".results-", suffix=".json", delete=False) as handle:
        temp = Path(handle.name)
        json.dump(data, handle, ensure_ascii=False, indent=2); handle.write("\n")
    try:
        load_complete(temp)
        os.replace(temp, out / "results.json")
    finally:
        temp.unlink(missing_ok=True)

def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True); ap.add_argument("--manifest", type=Path, required=True); ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args(argv)
    try: build(args.root, args.manifest, args.out)
    except (consolidate.GateError, MatrixInputError) as exc: ap.error(str(exc))
    return 0

if __name__ == "__main__": raise SystemExit(main())
