"""Gate matrix rendering on a complete, receipt-validated consolidation."""
from __future__ import annotations
import json
from pathlib import Path
from collections import Counter
from consolidate import parse_identity, GateError

METRICS = [f"M{i}" for i in range(1, 12)]
STATUSES = {"scored", "not_applicable", "blocked", "needs_review", "unscorable", "not_assessed"}

class MatrixInputError(RuntimeError):
    pass

def load_complete(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MatrixInputError(f"cannot read consolidated results: {exc}") from exc
    gate = data.get("consolidation_gate")
    rows = data.get("rows")
    if not isinstance(gate, dict) or gate.get("formal") is not True:
        raise MatrixInputError("formal matrix replacement requires a formal consolidation gate")
    if gate.get("universe_size") != 156 or gate.get("validated_receipts") != 156:
        raise MatrixInputError("formal matrix replacement requires 156 receipt-validated runs")
    if not isinstance(rows, list) or len(rows) != 156:
        raise MatrixInputError("formal matrix replacement requires exactly 156 rows")
    run_ids = [r.get("run_id") for r in rows if isinstance(r, dict)]
    if len(run_ids) != 156 or any(not isinstance(x, str) or not x for x in run_ids) or len(set(run_ids)) != 156:
        raise MatrixInputError("formal matrix replacement requires 156 unique run IDs")
    if gate.get("pair_key") != ["model", "task", "ecosystem"]:
        raise MatrixInputError("matrix rows must use model/task/ecosystem pairing")
    for row in rows:
        try:
            identity = parse_identity(row["run_id"])
        except GateError as exc:
            raise MatrixInputError(str(exc)) from exc
        identity["model"] = identity["model"].replace("glm-5_3", "glm-5.3").replace("deepseek-v4_1-flash", "deepseek-v4.1-flash")
        if any(row.get(key) != value for key, value in identity.items()):
            raise MatrixInputError("row identity does not match its run_id")
    expected_pairs = gate.get("expected_pairs")
    actual_pairs = sorted({(r.get("model"), r.get("task"), r.get("ecosystem")) for r in rows})
    if not isinstance(expected_pairs, list) or sorted(map(tuple, expected_pairs)) != actual_pairs:
        raise MatrixInputError("matrix rows do not match manifest-derived model/task/ecosystem pairs")
    if len(actual_pairs) != 156 or len({p[0] for p in actual_pairs}) != 3 or len({p[1] for p in actual_pairs}) != 26:
        raise MatrixInputError("matrix requires 3 models × 26 tasks × 2 ecosystems")
    task_counts = Counter(r.get("task") for r in rows)
    if any(task_counts[t] != 6 for t in task_counts) or task_counts.get("G") != 6:
        raise MatrixInputError("each task must have six rows and G must have six migration rows")
    if gate.get("main_task_count") != len({r.get("task") for r in rows if r.get("task") != "G"}):
        raise MatrixInputError("main task count does not match rows")
    if gate.get("migration_analogy_tasks") != ["G"]:
        raise MatrixInputError("migration analogy task set must be exactly ['G']")
    if any(sum(r.get("task") == task and r.get("model") == model for r in rows) != 2 for task in {r.get("task") for r in rows} for model in {r.get("model") for r in rows}):
        raise MatrixInputError("each model/task pair must have exactly two ecosystems")
    coverage = data.get("metric_coverage")
    if not isinstance(coverage, dict) or set(METRICS) - set(coverage):
        raise MatrixInputError("consolidation is missing per-metric denominator/null coverage")
    for metric in METRICS:
        item = coverage[metric]
        if not isinstance(item.get("denominator_scored"), int) or not isinstance(item.get("null_reasons"), list):
            raise MatrixInputError(f"{metric} is missing denominator or null reasons")
        observed = Counter()
        nulls = []
        for row in rows:
            metrics = row.get("metrics")
            metric_value = metrics.get(metric) if isinstance(metrics, dict) else None
            if not isinstance(metric_value, dict) or metric_value.get("status") not in STATUSES:
                raise MatrixInputError(f"{metric} has an invalid status object")
            status = metric_value["status"]; score = metric_value.get("score")
            if status == "scored":
                if not isinstance(score, (int, float)) or isinstance(score, bool) or not (0 <= score <= 100 if metric == "M11" else 1 <= score <= 5):
                    raise MatrixInputError(f"{metric} has an invalid scored value")
                if metric != "M2" and metric != "M11" and not isinstance(score, int):
                    raise MatrixInputError(f"{metric} scored values must be integers")
            elif score is not None:
                raise MatrixInputError(f"{metric} has a non-null score for status {status}")
            observed[status] += 1
            if status != "scored": nulls.append({"run_id": row["run_id"], "status": status, "reason": metric_value.get("reason", "")})
        if item["denominator_scored"] != observed["scored"] or item["status_counts"] != dict(observed) or item["null_reasons"] != nulls:
            raise MatrixInputError(f"{metric} coverage metadata does not match rows")
    return data
