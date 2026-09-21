#!/usr/bin/env python3
"""Consolidate only fully gated workflow-v1 records.

This module deliberately knows nothing about the previous scoring tree.  The
manifest supplies the selected run universe and the workflow directory is
searched recursively for the new per-run artifacts.
"""
from __future__ import annotations
import argparse, hashlib, json, re, statistics, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "skill" / "ai-usability-rescore" / "scripts"))
from validate_point_assessment import validate_assessment

METRICS = [f"M{i}" for i in range(1, 12)]
ARTIFACTS = ("facts.json", "assessment.json", "check.json", "review.json", "receipt.json")
ALIASES = {"check.json": ("check.json", "check-report.json"),
           "receipt.json": ("receipt.json", "review-receipt.json")}

def artifact_path(directory, name):
    """Resolve canonical names while accepting archived artifact aliases."""
    for candidate in ALIASES.get(name, (name,)):
        path = directory / candidate
        if path.exists():
            return path
    return directory / name

def read(p):
    try: return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e: raise GateError(f"cannot read {p}: {e}")

def sha(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""): h.update(b)
    return h.hexdigest()

class GateError(RuntimeError): pass

def manifest_ids(path):
    d = read(path)
    rows = d.get("records") if isinstance(d, dict) else d
    if not isinstance(rows, list): raise GateError("manifest.records must be a list")
    ids = [r.get("run_id") if isinstance(r, dict) else None for r in rows]
    if any(not isinstance(x, str) or not x for x in ids): raise GateError("manifest contains a run without run_id")
    dup = sorted(x for x, n in Counter(ids).items() if n > 1)
    if dup: raise GateError("duplicate run_id in selected manifest: " + ", ".join(dup))
    return ids, {r["run_id"]: r for r in rows}

def discover(root):
    # Production roots contain formal batch/pilot trees. Exclude fresh and
    # rejected/history copies, which may duplicate a formal run. A root with
    # neither child is retained for synthetic validator fixtures.
    formal = [root / name for name in ("batch", "pilot") if (root / name).is_dir()]
    search_roots = formal or [root]
    found = {}
    candidates = (p for sr in search_roots for p in sr.rglob("*"))
    for p in candidates:
        if not p.is_dir(): continue
        # prepared/ and similar nested directories belong to their enclosing
        # run; never treat their packet index as a second run record.
        if any(parent != p and parent.is_relative_to(sr) and
               ((parent / "facts.json").exists() or (parent / "packet-index.json").exists())
               for sr in search_roots for parent in p.parents):
            continue
        names = {x.name for x in p.iterdir() if x.is_file()}
        if not ({"facts.json", "packet-index.json"} & names): continue
        vals = []
        for n in ("facts.json", "packet-index.json", "assessment.json", "check.json", "review.json", "receipt.json"):
            q = artifact_path(p, n)
            if q.exists():
                try: vals.append((n, read(q).get("run_id")))
                except GateError: pass
        rid = next((v for n, v in vals if isinstance(v, str) and v), None)
        if not rid: continue
        if rid in found: raise GateError(f"duplicate discovered run_id: {rid} ({found[rid]} and {p})")
        found[rid] = p
    return found

def packet_hash(run_dir, facts, index):
    # A real packet.json is preferred. packet-index is an index whose value is
    # the hash of the immutable packet kept in the input store.
    packet = run_dir / "packet.json"
    if packet.exists(): return sha(packet)
    value = index.get("packet_sha256")
    if isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value): return value
    value = facts.get("packet_sha256")
    if isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value): return value
    raise GateError(f"{run_dir}: no packet hash")

def parse_identity(rid):
    m = re.match(r"^(?P<task>[A-Z]+)-(?P<ecosystem>cann|cuda)-(?P<model>.+?)-standard-", rid)
    if not m:
        # Synthetic CLI smoke records are accepted by the validator tests only;
        # production consolidation still obtains its 156 IDs from the manifest.
        if rid.startswith("synthetic-"): return {"task": "synthetic", "ecosystem": "synthetic", "model": "synthetic"}
        raise GateError(f"unrecognised run_id: {rid}")
    return m.groupdict()

def validate_run(rid, d, manifest_row=None):
    def path_for(name):
        q = artifact_path(d, name)
        if q.exists(): return q
        if name in ("facts.json", "packet-index.json") and (d / "prepared" / name).exists(): return d / "prepared" / name
        return q
    missing = [n for n in ARTIFACTS if not path_for(n).exists()]
    if missing: raise GateError(f"{rid}: missing {', '.join(missing)}")
    facts, assessment, check, review, receipt = [read(path_for(n)) for n in ARTIFACTS]
    index = read(path_for("packet-index.json"))
    actual_packet = packet_hash(d, facts, index)
    if manifest_row:
        if manifest_row.get("packet_sha256") and manifest_row["packet_sha256"] != actual_packet:
            raise GateError(f"{rid}: packet hash does not match selected manifest")
        if manifest_row.get("process_sha256") and assessment.get("process_sha256") != manifest_row["process_sha256"]:
            raise GateError(f"{rid}: process hash does not match selected manifest")
    if facts.get("run_id") != rid or index.get("run_id") != rid: raise GateError(f"{rid}: facts/index run_id mismatch")
    for obj, name in ((facts, "facts"), (assessment, "assessment"), (check, "check"), (review, "review"), (receipt, "receipt")):
        if obj.get("run_id") not in (None, rid): raise GateError(f"{rid}: {name}.run_id mismatch")
    if facts.get("packet_sha256") != actual_packet or index.get("packet_sha256") != actual_packet: raise GateError(f"{rid}: packet hash mismatch")
    if assessment.get("run_id") != rid: raise GateError(f"{rid}: assessment run_id missing/mismatch")
    schema_issues = validate_assessment(assessment)
    if schema_issues: raise GateError(f"{rid}: assessment schema invalid: {schema_issues}")
    metrics = assessment.get("metrics")
    if not isinstance(metrics, dict) or set(METRICS) - set(metrics): raise GateError(f"{rid}: assessment does not contain all M1-M11")
    for metric in METRICS:
        item = metrics[metric]
        if not isinstance(item, dict) or not isinstance(item.get("status"), str): raise GateError(f"{rid}: {metric} is not a metric object")
        if not isinstance(item.get("reason"), str) or not item["reason"].strip(): raise GateError(f"{rid}: {metric} has no content reason")
        if item.get("status") == "scored" and not isinstance(item.get("score"), (int, float)): raise GateError(f"{rid}: {metric} scored without a numeric point")
    hashes = {"packet_sha256": actual_packet, "facts_sha256": sha(path_for("facts.json")), "assessment_sha256": sha(path_for("assessment.json")), "check_report_sha256": sha(path_for("check.json"))}
    for k in ("packet_sha256", "facts_sha256", "assessment_sha256"):
        if check.get(k) != hashes[k]: raise GateError(f"{rid}: check.{k} mismatch")
    if check.get("report_sha256") != __import__("hashlib").sha256(json.dumps({k:v for k,v in check.items() if k != "report_sha256"}, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest():
        raise GateError(f"{rid}: check report self-hash mismatch")
    for obj, label in ((review, "review"), (receipt, "receipt")):
        for k, v in hashes.items():
            if obj.get(k) != v: raise GateError(f"{rid}: {label}.{k} mismatch")
    if check.get("mechanical_pass") is not True or check.get("issues") != []: raise GateError(f"{rid}: check is not a mechanical pass")
    if review.get("reviewer") != "root" or review.get("findings_resolved") is not True: raise GateError(f"{rid}: missing root parent review")
    scope = review.get("review_scope", "")
    if not isinstance(scope, str) or not all(m in scope for m in METRICS): raise GateError(f"{rid}: review scope is not explicitly per-metric")
    if not isinstance(review.get("limitations"), str) or not review["limitations"].strip(): raise GateError(f"{rid}: review limitations missing")
    if receipt.get("mechanical_pass") is not True or receipt.get("findings_resolved") is not True: raise GateError(f"{rid}: receipt does not record a completed gate")
    if receipt.get("semantic_pass") is True: raise GateError(f"{rid}: receipt falsely claims automatic semantic certification")
    if "Reviewer assertion only" not in receipt.get("content_review_assertion", ""): raise GateError(f"{rid}: receipt content assertion missing")
    identity = parse_identity(rid)
    identity["model"] = identity["model"].replace("glm-5_3", "glm-5.3").replace("deepseek-v4_1-flash", "deepseek-v4.1-flash")
    row = {**identity, "run_id": rid, "assessment_path": str((d/"assessment.json")), "metrics": metrics, "packet_sha256": actual_packet}
    return row

def paired(rows, metric):
    ix = {(r["task"], r["ecosystem"]): r for r in rows}
    out, excluded = [], []
    for task in sorted({r["task"] for r in rows} - {"G"}):
        if (task, "cann") not in ix or (task, "cuda") not in ix: excluded.append({"task": task, "reason": "missing side"}); continue
        a, b = ix[task, "cann"]["metrics"][metric], ix[task, "cuda"]["metrics"][metric]
        if a.get("status") != "scored" or b.get("status") != "scored": excluded.append({"task": task, "cann_status": a.get("status"), "cuda_status": b.get("status")}); continue
        out.append({"task": task, "cann": a.get("score"), "cuda": b.get("score"), "delta": b.get("score") - a.get("score")})
    return {"n": len(out), "pairs": out, "excluded": excluded, "cann": statistics.mean(x["cann"] for x in out) if out else None, "cuda": statistics.mean(x["cuda"] for x in out) if out else None, "delta": statistics.mean(x["delta"] for x in out) if out else None, "cuda_higher": sum(x["delta"] > 1e-9 for x in out), "cann_higher": sum(x["delta"] < -1e-9 for x in out), "ties": sum(abs(x["delta"]) <= 1e-9 for x in out)}

def consolidate(root, manifest, out, historical_results=None):
    ids, meta = manifest_ids(manifest); found = discover(root)
    if historical_results:
        old = read(historical_results).get("rows", [])
        for r in old:
            if r.get("run_id") in meta:
                meta[r["run_id"]].update({k: r.get(k) for k in ("gate_passed", "gate")})
    if len(ids) != 156: raise GateError(f"selected input universe must contain 156 runs, found {len(ids)}")
    extra = sorted(set(found) - set(ids))
    if extra: raise GateError("unexpected workflow runs: " + ", ".join(extra))
    missing = sorted(set(ids) - set(found))
    if missing: raise GateError("missing workflow runs: " + ", ".join(missing))
    rows = [validate_run(rid, found[rid], meta.get(rid)) for rid in ids]
    if len(rows) != 156: raise GateError("coverage is not 156")
    summary = {g: {"runs": len(rs), "metrics": {m: dict(Counter(x["metrics"][m].get("status") for x in rs)) for m in METRICS}} for g, rs in (("all", rows), ("main", [x for x in rows if x["task"] != "G"]), ("migration_analogy", [x for x in rows if x["task"] == "G"]))}
    results = {"rule_version": "point-rubric-20260922-v1", "assessor": "workflow-v1", "new_collection": False, "summary": summary, "rows": rows}
    analysis = {"rule_version": results["rule_version"], "assessor": results["assessor"], "comparison": "CUDA minus CANN; paired observed point scores, no imputation or statistical uncertainty estimate.", "primary_inclusion": "Per-metric scored status on both sides; historical run gates are separate.", "models": {}, "historical_gate_sensitivity": {}, "common_tasks": {}}
    for model in sorted({x["model"] for x in rows}):
        rs = [x for x in rows if x["model"] == model]
        analysis["models"][model] = {m: paired(rs, m) for m in METRICS}
        gated = [x for x in rs if meta.get(x["run_id"], {}).get("gate_passed") is True]
        has_gate = all(isinstance(meta.get(x["run_id"], {}).get("gate_passed"), bool) for x in rs)
        analysis["historical_gate_sensitivity"][model] = ({m: paired(gated, m) for m in METRICS} if has_gate else {"available": False, "reason": "historical gate metadata is incomplete"})
    for m in METRICS:
        sets = []
        for model in analysis["models"]:
            rs = [x for x in rows if x["model"] == model and x["task"] != "G"]
            sets.append({t for t in {x["task"] for x in rs} if all(any(x["task"] == t and x["ecosystem"] == e and x["metrics"][m].get("status") == "scored" for x in rs) for e in ("cann", "cuda"))})
        common = set.intersection(*sets) if sets else set()
        analysis["common_tasks"][m] = {"tasks": sorted(common), "models": {model: paired([x for x in rows if x["model"] == model and x["task"] in common], m) for model in analysis["models"]}}
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    (out / "paired-summary.json").write_text(json.dumps(analysis, ensure_ascii=False, indent=2) + "\n")

def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True); ap.add_argument("--manifest", type=Path, required=True); ap.add_argument("--out", type=Path, required=True); ap.add_argument("--historical-results", type=Path)
    args = ap.parse_args(argv)
    try: consolidate(args.root, args.manifest, args.out, args.historical_results)
    except GateError as e: print(f"consolidate: {e}", file=sys.stderr); return 2
    return 0
if __name__ == "__main__": raise SystemExit(main())
