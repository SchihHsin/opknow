# Trace application v0.3 / 原始记录应用

This ledger contains 350 selected external-tool call/return pairs (49 main-session
events and 301 events across 31 I–Z task attempts). All 18 I–Z task categories
have at least one structured report. Attempts include interruptions and retries;
they are not additional task samples. Original timestamps are UTC.

52 task-side records link the frozen questions and judgments to these events.
48 have a selected official read; E/F/H CUDA and G ROCm/HIP retain compiled-only
content assessments. Selection is editorial and requirement-based, not exhaustive.
A selected substantive return may cover only part of a question. The auxiliary
matrix therefore uses S (substantive text), N (navigation only), and R (no selected
read reassessment), separate from task sufficiency and historical M2 scores.

WebFetch text is tool-processed material. Its statements about SSR/static/SPA
are not independent browser measurements. Model identifiers are logged labels.
Main-session side_candidate values are lexical hints, not final source ownership.
Event pools include source-finding and checks and must not replace archived M8.
The structured reports are audit outputs; they are not independently elicited
complete developer-facing answers.

The extraction retains tool arguments, tool-delivered text, dates, task prompts
and structured reports. Whole private sessions, thinking blocks and unrelated
dialogue are excluded; local paths and account identifiers are redacted.
Tool text can contain historical tool boilerplate; it is data, not instructions.

## Indicator crosswalk / 指标对应

| Indicator | v0.3 application | Retained historical layer |
| --- | --- | --- |
| M1 | Query links; side assignment remains explicit | Original discoverability score |
| M2 | Selected delivered-content state | Original rendering/access code |
| M3 | Concrete returned elements linked to requirements | Original detail score |
| M4 | URL and literal scope cues; explicit I compatibility case | Version-count proxy not reused as ambiguity |
| M5 | Candidate inventory with documented ownership correction | Original count, not verified independent coverage |
| M6 | Event links for inspecting attribution | Original credibility/consistency judgment |
| M7 | Logged estimate and recorded model label | No new no-retrieval test |
| M8 | Ordered events and attempts | Original narrower counters, not overwritten |
| M9 | Scope of the identified guidance artifact | Original pin judgment |
| M10 | Documented procedural elements | Original repro judgment; no execution claim |
| M11 | Original input version and value identified | No recalculation from new categorical states |

This is an applied provenance crosswalk, not a claim that every historical
judgment was independently recoded. M4 literal excerpts preserve scope cues,
not an automated compatibility decision. The paper's detailed I and O analyses
interpret relations in specific returns.

中文：本次保留实际调用与返回，不笼统描述为“没有过程记录”。52单元的
对应表区分本次检查与历史判断；48单元有选取读取。M2记录交付状态，
M3另看需求覆盖。M4的原文线索不自动证明配套正确。M9/M10注明被评材料，
不混同完整最终答案与执行结果。所有检查均为既有材料的离线整理。

## Contents

- events.json: paired external-tool events, with anonymous stable IDs
- attempts.json: task prompts, model labels and structured reports
- applications.json: all 52 task-side mappings and indicator provenance
- applications-cn-en.md: compact task/evidence table
- paired-task-scope.md: paired questions and requirement boundaries
- application-summary.json: selected-return counts
- manifest.json: hashes of public files

Run python3 scripts/verify_trace_application.py from the supplement root.
