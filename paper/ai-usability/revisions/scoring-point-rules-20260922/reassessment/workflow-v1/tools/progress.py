#!/usr/bin/env python3
"""Report selected-input progress; denominator is manifest records, never files."""
from consolidate import ARTIFACTS, discover, manifest_ids, read, sha, validate_run
import argparse, json
from pathlib import Path

def status(rid, d):
    def exists(n): return d and ((d/n).exists() or (n in ("facts.json", "packet-index.json") and (d/"prepared"/n).exists()))
    have = {n for n in ARTIFACTS if exists(n)} | ({"packet-index.json"} if exists("packet-index.json") else set())
    if not d or not {"facts.json", "packet-index.json"} <= have: return "missing"
    if "assessment.json" not in have: return "prepared"
    if "check.json" not in have: return "draft"
    try: mechanical = read(d/"check.json").get("mechanical_pass") is True and read(d/"check.json").get("issues") == []
    except Exception: mechanical = False
    if mechanical:
        c = read(d/"check.json"); fpath = d/"facts.json" if (d/"facts.json").exists() else d/"prepared"/"facts.json"; ipath = d/"packet-index.json" if (d/"packet-index.json").exists() else d/"prepared"/"packet-index.json"
        mechanical = c.get("facts_sha256") == sha(fpath) and c.get("assessment_sha256") == sha(d/"assessment.json") and c.get("packet_sha256") == read(ipath).get("packet_sha256")
    if not mechanical: return "draft"
    if not {"review.json", "receipt.json"} <= have: return "mechanical_pass"
    try:
        validate_run(rid, d, {})
        return "parent_reviewed"
    except Exception: return "mechanical_pass"

def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True); ap.add_argument("--manifest", type=Path, required=True); ap.add_argument("--out", type=Path)
    a=ap.parse_args(argv); ids,_=manifest_ids(a.manifest); found=discover(a.root); rows=[{"run_id":r,"status":status(r,found.get(r))} for r in ids]
    counts={k:sum(x["status"]==k for x in rows) for k in ("prepared","draft","mechanical_pass","parent_reviewed","missing")}
    result={"selected_inputs":len(ids),"counts":counts,"records":rows}
    text=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if a.out: a.out.write_text(text)
    else: print(text,end="")
    return 0
if __name__ == "__main__": raise SystemExit(main())
