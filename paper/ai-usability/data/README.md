# Frozen audit appendix

This directory packages existing project records for an archival illustration of the paper's method. It contains no new web retrieval, agent experiment, independent human review, or hardware execution. The original project files are unchanged.

Run with Python 3.9 or later, without third-party dependencies:

```sh
python3 scripts/build_paper_analysis.py
```

Run the command from the paper directory, or invoke the script by its location from any working directory. To move this appendix, keep `data/` beside `scripts/build_paper_analysis.py`. The script verifies frozen-file hashes, checks that the frozen RAW and scores exactly match the packaged historical script, and writes deterministic outputs under `data/generated/`. It does not require the original project, network access, or local absolute paths.

## Frozen inputs

| File | Contents |
| --- | --- |
| `manifest.json` | Source identities, SHA-256 hashes, freeze date, and included-file hashes. |
| `legacy_score_metrics.py` | Byte-for-byte copy of the historical scoring script; retained for reproduction, not recommended as a validated instrument. |
| `legacy_task_run_log.md` | Byte-for-byte copy of the compiled historical run summary. This is not an original tool transcript. |
| `raw_original.json` | All 26 × 2 historical RAW records, including judgment-based fields and unknown dates. |
| `legacy_scores_original.json` | All 52 historical score rows and formula outputs. |
| `tasks.json` | Complete task list, retained Chinese questions, editorial English target summaries, original workflow groups, and paper-scope flags. |
| `source_evidence.json` | Frozen excerpts and original line references supporting the audit decisions and task taxonomy. |
| `corrections.json` | Explicit scope, source-ownership, unresolved-count, and interpretation decisions. |

## Generated outputs

`generated/paper_analysis.json` contains 25-pair descriptive statistics, separately labelled 26-pair historical statistics, workflow summaries, and an arithmetic removal of the model-prior channel. It records both means of exact formula results and means of the historical three-decimal archived results, avoiding silent rounding differences.

`generated/units.json` retains all 52 units with their original RAW and original scores, descriptive access status, known source-ownership exclusion, unresolved issues, and arithmetic sensitivity result. `generated/task_table.md`, `generated/corrections.md`, and `generated/english_findings.md` are readable paper appendices.

## What changes and what stays archived

- G is a migration analogy whose CUDA-labelled side examines AMD ROCm/HIP. It remains in the archive but is excluded from the 25-pair primary description.
- H.cuda's `nvidia-blog` entry is treated as vendor-owned official material in the audit view. It is removed from the count of candidate secondary sources in that view. Original RAW and historical scores are not overwritten or presented as corrected scores.
- A.cann's zero failed-fetch count conflicts with a missing-body report in the retained log. It remains unresolved; no replacement value is invented.
- `static` and `ssr` map to the same descriptive access status. `partial` and `spa`/`robots` remain distinct. This mapping does not infer sufficiency or execution success. The old unequal numeric scores are retained only to reproduce the historical formula.
- Removing the prior channel sets `OWN=0` inside the historical formula while leaving all other inputs unchanged. It is an assumption-sensitivity calculation, not a run of a different model or a no-retrieval condition.

## Data interpretation

`raw_original` fields and their historical anchors are documented in the packaged scoring script. `own`, `consist`, `churn`, `ref_level`, `pin`, and `repro` include judgment or coding decisions. In particular, `repro=copyrun` is an archived assessment, not evidence that code was run successfully. The legacy index is not a calibrated probability.

The field `candidate_secondary_count_after_known_ownership_exclusion` applies only the explicitly documented H.cuda ownership correction. It must not be read as a verified count of independent, accessible, or answer-supporting sources. `independent_source_count_verified` remains `null` for every unit. Original questions for later batches are labelled according to what the compiled log reports about their recovery; original transcripts have not been reconstructed or added.

No retained aggregate should be interpreted as a current website measurement, ecosystem ranking, causal effect, developer success rate, or validated model capability estimate.
