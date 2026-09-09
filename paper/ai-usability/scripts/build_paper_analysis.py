#!/usr/bin/env python3
"""Reproduce a paper appendix from frozen historical artifacts, using stdlib only.

Run from any directory: python3 path/to/scripts/build_paper_analysis.py
No web access, new agent runs, response validation, or hardware execution occurs.
The historical source files remain unchanged. Outputs go to data/generated/.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
DATA = Path(__file__).resolve().parent.parent / "data"
OUT = DATA / "generated"
SIDES = ("cann", "cuda")
BANDS = {"高": "high", "中高": "medium_high", "中": "medium", "低": "low", "很低": "very_low"}
ACCESS = {
    "static": "core_text_retrieved",
    "ssr": "core_text_retrieved",
    "partial": "partial_text_retrieved",
    "spa": "core_text_not_retrieved",
    "robots": "core_text_not_retrieved",
}
GROUPS = {
    "environment_installation": "Environment and installation",
    "operator_development": "Operator development",
    "training": "Training",
    "inference_deployment": "Inference and deployment",
    "performance_optimization": "Performance optimization",
    "debugging": "Debugging",
    "migration": "Migration and conceptual comparison",
}


def read_json(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def write_json(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def mean(values):
    return round(statistics.mean(values), 6)


def counts(values):
    return dict(sorted(Counter(values).items()))


def markdown_cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def verify_frozen_inputs():
    manifest = read_json("manifest.json")
    for name, expected in manifest["frozen_files"].items():
        actual = hashlib.sha256((DATA / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Frozen input changed: {name}; expected {expected}, got {actual}")
    spec = importlib.util.spec_from_file_location("paper_legacy_metrics", DATA / "legacy_score_metrics.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load the packaged legacy scoring script")
    legacy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(legacy)
    raw = read_json("raw_original.json")
    archived_scores = read_json("legacy_scores_original.json")
    if raw != legacy.RAW or archived_scores != legacy.compute():
        raise ValueError("Frozen RAW or scores differ from the packaged historical script")
    tasks = read_json("tasks.json")
    if [t["task_id"] for t in tasks] != legacy.TASKS or len(tasks) != 26:
        raise ValueError("Expected all 26 historical task pairs in order")
    if [t["task_id"] for t in tasks if not t["include_in_25_pair_summary"]] != ["G"]:
        raise ValueError("G must be the sole migration analogy excluded from the 25-pair summary")
    for task in legacy.TASKS:
        for side in SIDES:
            r = raw[task][side]
            if len(r["sources"]) != len(r["platforms"]) or len(r["sources"]) != len(r["dates"]):
                raise ValueError(f"Mismatched source arrays: {task}.{side}")
    return legacy, raw, archived_scores, tasks


def build_units(legacy, raw, archived_scores, tasks):
    units = []
    for task in tasks:
        tid = task["task_id"]
        for side in SIDES:
            r = raw[tid][side]
            original_scores = archived_scores[tid][side]["scores"]
            exact, band, intermediates = legacy.score11_overall(original_scores)
            no_prior_scores = list(original_scores)
            no_prior_scores[6] = legacy.BLK  # Mathematical removal of OWN; not an observed score.
            no_prior, no_prior_band, _ = legacy.score11_overall(no_prior_scores)
            ownership_exclusions = [0] if (tid, side) == ("H", "cuda") else []
            units.append({
                "unit_id": f"{tid}.{side}",
                "task_id": tid,
                "legacy_side_label": side,
                "case_label": "AMD ROCm / HIP migration analogy" if (tid, side) == ("G", "cuda") else side.upper(),
                "include_in_25_pair_summary": task["include_in_25_pair_summary"],
                "workflow_group": task["workflow_group"],
                "raw_original": r,
                "legacy_scores_original": archived_scores[tid][side],
                "legacy_index_recomputed_exact": exact,
                "legacy_band": BANDS[band[0]],
                "legacy_intermediates_recomputed_exact": intermediates,
                "recorded_access_status": ACCESS[r["core_fetch"]],
                "access_status_provenance": "Descriptive mapping of retained core_fetch code; no new page retrieval or content verification.",
                "recorded_access_route": "unknown_not_consistently_retained",
                "access_route_provenance": "The legacy core_fetch field does not distinguish an original entry from an alternative route; route is therefore not inferred retrospectively.",
                "retrieval_does_not_establish": ["content sufficiency", "answer correctness", "actual execution success"],
                "candidate_secondary_count_original": len(r["sources"]),
                "known_official_source_indices_in_legacy_secondary_list": ownership_exclusions,
                "candidate_secondary_count_after_known_ownership_exclusion": len(r["sources"]) - len(ownership_exclusions),
                "independent_source_count_verified": None,
                "source_count_note": "Remaining candidates have not been independently verified for ownership, originality, accessibility, or support for the answer.",
                "audit_flags": (["C01"] if tid == "G" else []) + (["C02"] if ownership_exclusions else []) + (["C03"] if (tid, side) == ("A", "cann") else []) + ["C04"],
                "sensitivity_remove_prior": {
                    "setting": "Set OWN=0 while retaining every other historical formula input, including original source coding.",
                    "index": no_prior,
                    "band": BANDS[no_prior_band[0]],
                    "interpretation": "Arithmetic sensitivity of an unvalidated legacy index; not a no-retrieval experiment or a new model observation.",
                },
            })
    return units


def summarize_side(units):
    original = [u["legacy_index_recomputed_exact"] for u in units]
    archived = [u["legacy_scores_original"]["overall"] for u in units]
    without = [u["sensitivity_remove_prior"]["index"] for u in units]
    return {
        "n": len(units),
        "recorded_access_status_counts": counts(u["recorded_access_status"] for u in units),
        "original_core_fetch_code_counts": counts(u["raw_original"]["core_fetch"] for u in units),
        "recorded_reference_completeness_counts": counts(u["raw_original"]["ref_level"] for u in units),
        "recorded_search_rounds_counts": counts(u["raw_original"]["rounds"] for u in units),
        "recorded_fetches_total": sum(u["raw_original"]["fetch"] for u in units),
        "recorded_fetch_failures_total_unresolved_counts_preserved": sum(u["raw_original"]["fetch_fail"] for u in units),
        "legacy_version_clarity_score_counts": counts(u["legacy_scores_original"]["scores"][3] for u in units),
        "candidate_secondary_count_original_mean": mean(u["candidate_secondary_count_original"] for u in units),
        "candidate_secondary_count_after_known_ownership_exclusion_mean": mean(u["candidate_secondary_count_after_known_ownership_exclusion"] for u in units),
        "legacy_prior_self_rating_mean": mean(u["legacy_scores_original"]["scores"][6] for u in units),
        "legacy_prior_self_rating_equal_to_5_count": sum(u["legacy_scores_original"]["scores"][6] == 5 for u in units),
        "legacy_index": {
            "status": "Historical heuristic, unvalidated and uncalibrated; not answer correctness or task success probability.",
            "mean_from_exact_recomputation": mean(original),
            "mean_of_archived_3_decimal_values": mean(archived),
            "min_exact": round(min(original), 6),
            "max_exact": round(max(original), 6),
            "band_counts_using_exact_formula": counts(u["legacy_band"] for u in units),
        },
        "sensitivity_remove_prior": {
            "mean": mean(without),
            "mean_change_from_exact_legacy": mean(b - a for a, b in zip(original, without)),
            "band_counts": counts(u["sensitivity_remove_prior"]["band"] for u in units),
            "tasks_at_low_or_very_low": [{"task_id": u["task_id"], "index": round(u["sensitivity_remove_prior"]["index"], 6), "band": u["sensitivity_remove_prior"]["band"]} for u in units if u["sensitivity_remove_prior"]["band"] in {"low", "very_low"}],
        },
    }


def summarize_scope(units):
    return {side: summarize_side([u for u in units if u["legacy_side_label"] == side]) for side in SIDES}


def write_tables(tasks, units, corrections):
    task_lines = ["# Retained task formulations", "", "English targets below are editorial summaries of the archived Chinese formulations, not prompts used in new runs. Full archived question text is preserved in `../tasks.json`. G is retained as a migration analogy and excluded from the 25-pair summary. Workflow groups reproduce the original report's taxonomy; they are not asserted to be a sequential journey.", "", "| ID | Task | Workflow group | CUDA-labelled target | CANN target | Paper scope |", "| --- | --- | --- | --- | --- | --- |"]
    for t in tasks:
        row = [t["task_id"], t["name_en"], GROUPS[t["workflow_group"]], t["english_target_summaries"]["cuda"], t["english_target_summaries"]["cann"], "25-pair summary" if t["include_in_25_pair_summary"] else "Analogy only (AMD ROCm / HIP on CUDA-labelled side)"]
        task_lines.append("| " + " | ".join(map(markdown_cell, row)) + " |")
    (OUT / "task_table.md").write_text("\n".join(task_lines) + "\n", encoding="utf-8")
    correction_lines = ["# Transparent audit decisions", "", "These decisions do not overwrite frozen RAW or legacy scores. No independent human coding or original tool-payload validation is claimed.", "", "| ID | Unit | Status | Original issue | Paper treatment | Evidence | Unresolved limit |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for c in corrections:
        refs = "; ".join(f"{e['file']}:{e['lines'][0]}–{e['lines'][1]}" for e in c["evidence"])
        row = [c["id"], c["unit"], c["status"], c["original"], c["paper_treatment"], refs, c["limit"]]
        correction_lines.append("| " + " | ".join(map(markdown_cell, row)) + " |")
    (OUT / "corrections.md").write_text("\n".join(correction_lines) + "\n", encoding="utf-8")


def write_english_findings(analysis):
    p = analysis["primary_25_pairs"]
    ca, cu = p["cann"], p["cuda"]
    c_access, n_access = ca["recorded_access_status_counts"], cu["recorded_access_status_counts"]
    text = f"""# Wording supported by the retained artifacts

The appendix preserves 26 historical task formulations and 52 ecosystem-labelled records. Task G is a migration analogy: its CUDA-labelled side examines migration to AMD ROCm/HIP. It is retained for transparency and excluded from the descriptive comparison of 25 goal-related task pairs (50 records). Task formulations differ in language, starting conditions, and implementation requirements; they are not controlled-equivalent experimental treatments.

In the retained records for the 25-pair subset, the CANN side contains {c_access.get('core_text_retrieved', 0)} cases coded as retrieved core text, {c_access.get('partial_text_retrieved', 0)} as partial retrieval, and {c_access.get('core_text_not_retrieved', 0)} as core text not retrieved. All {n_access.get('core_text_retrieved', 0)} CUDA-labelled cases were coded as retrieved core text. This descriptive mapping treats static and server-rendered pages alike. It reports the archived access observation, without treating page architecture as a quality hierarchy or inferring content sufficiency, answer correctness, or successful execution.

The ownership audit identifies an NVIDIA developer blog counted in the historical secondary-source list for H.cuda. The audit view classifies that entry as vendor-owned official material and reduces the candidate secondary-source count for that record from four to three. The original data and historical index are preserved unchanged. The remaining candidates are not asserted to be verified independent sources. A separate discrepancy remains unresolved: A.cann records three fetches and zero failures, whereas its compiled log reports a missing SPA body on the third fetch. No inferred replacement count is inserted.

For historical reproducibility only, the 25-pair subset has mean legacy heuristic indices of {ca['legacy_index']['mean_from_exact_recomputation']:.6f} for CANN and {cu['legacy_index']['mean_from_exact_recomputation']:.6f} for the CUDA-labelled side, using the original formula inputs. Means computed from the archived three-decimal values are {ca['legacy_index']['mean_of_archived_3_decimal_values']:.6f} and {cu['legacy_index']['mean_of_archived_3_decimal_values']:.6f}, respectively. These indices are neither calibrated confidence estimates nor observed performance measures.

An arithmetic sensitivity analysis sets the model-prior channel to zero while retaining all other historical inputs. The 25-pair means become {ca['sensitivity_remove_prior']['mean']:.6f} and {cu['sensitivity_remove_prior']['mean']:.6f}. The direction of the between-case difference persists, but absolute values and bands depend on the treatment of the prior channel. This is a re-analysis of a formula, not an additional agent experiment. In {cu['legacy_prior_self_rating_equal_to_5_count']} of the {cu['n']} CUDA-labelled records, the historical prior self-rating equals five. Because normalization makes OWN equal to one, K is then algebraically fixed at one regardless of the external-source factors; version and cost factors still affect the final legacy index.

The artifact supports inspection and arithmetic reproduction of the retained audit. It does not supply original tool transcripts, a verified model configuration, fresh website measurements, independently validated generated answers, human coding reliability, or hardware execution results. The associated workflow is therefore presented as a method with a worked archival illustration, not as a validated benchmark of ecosystem or agent performance.
"""
    (OUT / "english_findings.md").write_text(text, encoding="utf-8")


def main():
    legacy, raw, archived_scores, tasks = verify_frozen_inputs()
    units = build_units(legacy, raw, archived_scores, tasks)
    primary = [u for u in units if u["include_in_25_pair_summary"]]
    corrections = read_json("corrections.json")
    if len(units) != 52 or len(primary) != 50:
        raise ValueError("Unexpected unit counts")
    analysis = {
        "schema_version": 1,
        "analysis_type": "Descriptive archival re-analysis and arithmetic sensitivity; no new empirical run.",
        "frozen_manifest": "../manifest.json",
        "scope": {"retained_pairs": 26, "retained_units": 52, "primary_pairs": 25, "primary_units": 50, "excluded_from_primary": ["G"], "exclusion_reason": "G's CUDA-labelled side uses AMD ROCm / HIP migration material."},
        "primary_25_pairs": summarize_scope(primary),
        "historical_26_pairs_including_migration_analogy": summarize_scope(units),
        "workflow_groups_25_pairs": {g: summarize_scope([u for u in primary if u["workflow_group"] == g]) for g in GROUPS},
        "audit_decisions": corrections,
        "limitations": [
            "Frozen records include judgments and compiled retrieval summaries, not original tool transcripts.",
            "No new retrieval, independent human review, response validation, or hardware execution was performed.",
            "Exact agent and retrieval-tool configuration cannot be established from this appendix.",
            "Legacy indices are unvalidated heuristics, not calibrated confidence or task-success probabilities.",
            "Legacy static-versus-SSR scoring is retained only for historical reproduction and is not recommended as an access criterion.",
            "Known source-ownership exclusions are applied to an audit count only; original RAW and scores remain untouched.",
            "Source counts are candidate counts; platform diversity does not establish informational independence.",
            "A.cann failure-count discrepancy is unresolved; original cost coding remains in legacy arithmetic.",
            "The OWN=0 calculation changes a formula assumption, not observed model behavior.",
        ],
    }
    OUT.mkdir(exist_ok=True)
    write_json("units.json", units)
    write_json("paper_analysis.json", analysis)
    write_tables(tasks, units, corrections)
    write_english_findings(analysis)
    print(json.dumps({"verified_frozen_units": len(units), "primary_units": len(primary), "output_directory": "data/generated", "primary_25_pairs": analysis["primary_25_pairs"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
