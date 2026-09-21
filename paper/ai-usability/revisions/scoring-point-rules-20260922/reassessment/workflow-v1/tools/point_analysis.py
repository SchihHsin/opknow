"""Bounded descriptive analysis for receipt-gated point results.

This module never imputes nulls, pools models, or converts M11 to a 1--5 scale.
"""
from __future__ import annotations
import argparse, json, statistics
from collections import Counter
from pathlib import Path
from matrix_input import METRICS, load_complete

MAIN_TASKS = tuple(chr(i) for i in range(ord("A"), ord("Z") + 1) if chr(i) != "G")
ECOSYSTEMS = ("cann", "cuda")

def _scores(rows, metric):
    return [r["metrics"][metric]["score"] for r in rows if r["metrics"][metric].get("status") == "scored"]

def _summary(rows, metric):
    vals = _scores(rows, metric)
    counts = Counter((r["metrics"][metric].get("status") for r in rows))
    null_reasons = Counter(r["metrics"][metric].get("reason", "") for r in rows if r["metrics"][metric].get("status") != "scored")
    return {"count": len(rows), "status_counts": dict(sorted(counts.items())), "null_reasons": dict(sorted(null_reasons.items())), "scored_n": len(vals), "mean": statistics.fmean(vals) if vals else None, "median": statistics.median(vals) if vals else None}

def _pair_stats(rows, metric, tasks=MAIN_TASKS, model=None):
    """Summarize one model and task scope; never pool the complete matrix."""
    scoped = [r for r in rows if model is None or r.get("model") == model]
    ix={(r["model"], r["task"], r["ecosystem"]): r for r in scoped}
    pairs=[]; excluded=[]
    models = [model] if model is not None else sorted({r["model"] for r in scoped})
    for model_name in models:
        for task in tasks:
            ca=ix.get((model_name, task, "cann")); cu=ix.get((model_name, task, "cuda"))
            if not ca or not cu:
                excluded.append({"model":model_name,"task":task,"reason":"missing ecosystem row"}); continue
            cm=ca["metrics"][metric]; um=cu["metrics"][metric]
            if cm.get("status") != "scored" or um.get("status") != "scored":
                excluded.append({"model":model_name,"task":task,"reason":"pair not both scored","cann_status":cm.get("status"),"cuda_status":um.get("status")}); continue
            delta=um["score"]-cm["score"]
            pairs.append({"model":model_name,"task":task,"cann":cm["score"],"cuda":um["score"],"delta":delta})
    ds=[x["delta"] for x in pairs]
    return {"n":len(pairs),"mean":statistics.fmean(ds) if ds else None,"median":statistics.median(ds) if ds else None,"cuda_wins":sum(d>0 for d in ds),"ties":sum(d==0 for d in ds),"cuda_losses":sum(d<0 for d in ds),"pairs":pairs,"excluded":excluded}

def analyze_data(data: dict) -> dict:
    rows=data["rows"]
    models=sorted({r["model"] for r in rows})

    def ecosystem_metrics(tasks):
        scoped=[r for r in rows if r.get("task") in tasks]
        return {model:{eco:{m:_summary([r for r in scoped if r.get("model")==model and r.get("ecosystem")==eco],m) for m in METRICS} for eco in ECOSYSTEMS} for model in models}

    main_metrics=ecosystem_metrics(MAIN_TASKS)
    migration_metrics=ecosystem_metrics(("G",))
    return {
        "scope":{"main_tasks":list(MAIN_TASKS),"migration_task":"G","ecosystems":list(ECOSYSTEMS),"models":models},
        # Historical key remains the primary 25-task scope. G is separate.
        "model_ecosystem_metrics":main_metrics,
        "main_model_ecosystem_metrics":main_metrics,
        "migration_G_model_ecosystem_metrics":migration_metrics,
        "paired_main":{model:{m:_pair_stats(rows,m,tasks=MAIN_TASKS,model=model) for m in METRICS} for model in models},
        "migration_G":{model:{m:_pair_stats(rows,m,tasks=("G",),model=model) for m in METRICS} for model in models},
    }

def analyze_path(path: Path) -> dict:
    return analyze_data(load_complete(path))

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args(argv)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(analyze_path(args.input), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
