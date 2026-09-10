# 任务级知识可得性测量协议 / Task-Level Knowledge Availability Protocol

本协议是论文v0.3的可复用操作说明。本次将52条任务侧记录连接到留存工具事件；历史数值与本次证据解释分别呈现。

This protocol is the reusable specification accompanying manuscript v0.3. The application connects 52 task-side records to retained events, separating historical numerical codes from the current evidence interpretation.

## 1. 定义任务与条件 / Define the task and conditions

记录结果目标、初始材料、适用版本、约束，以及支撑下一步行动所需的证据。记录Agent/模型、工具、语言、搜索环境、时间和上下文策略；不明信息填null并说明。比较任务必须说明起点和范围差异，不能只因名称相似就宣称严格等价。

Record the desired outcome, starting artifacts, versions, constraints, and evidence requirements. Record the agent/model, tools, language, search environment, time, and context policy. Use null with an explanation for unknown fields. Describe differences between comparison tasks rather than assuming controlled equivalence.

## 2. 预先说明记录边界 / State the recording boundary

注明哪些观察新采集、哪些复用。设置并记录检索预算或可观察的停止规则。分别计数检索、读取、失败、改词；同时说明计数是否包含辅助参考页。无法从原记录确定的规则不能事后冒充既定实验设置。

Identify newly acquired and reused observations. Specify a retrieval budget or observable stopping rule. Count searches, reads, failures, and refinements separately, stating whether ancillary references are included. Do not retrospectively invent missing experimental settings.

## 3. 保留来源与返回 / Retain sources and returns

逐次保留查询词、URL、返回内容或可定位摘录、来源发布者、角色与已知日期。官方材料按发布主体归属判断，不能按GitHub/CSDN等托管平台简单判断；跨域转载不是自动独立。相关入口应保留事件关系与顺序，不默认一个入口的失败发生在另一个入口的获取之前。

Retain queries, URLs, returns or locatable excerpts, publisher identity, source role, and known dates. Classify official ownership by the publisher, not the hosting platform. Cross-domain reproduction does not establish independence. Retain the order and relationship of relevant entry checks; do not presume that an unsuccessful check preceded a useful return.

## 4. 编码与缺失 / Code observations and missingness

M1记录官方发现路径。M2记录**官方正文可获取性**：实质文本、仅有导航、错误或未观测；任务需求覆盖另记；static与SSR按实际返回同等处理。**访问路径**另列为原入口、替代入口或未知。相同正文不会因镜像入口而降低需求覆盖，交付状态与访问路径分别记录。M3记录官方正文的详尽层级，未读取时记unobserved，不推断成低质量或任务已经解决。M4记录资料的适用版本与未解决的配套关系，多版本存在不自动等于模糊。M5/M6保留第三方来源的条数、归属、可信度及独立性的不确定。M7标明自评/推断或另行实测，不能将自评当训练覆盖事实。M8保留原始检索与获取次数及成本公式，不将其表述为实际耗时、Token或费用。M9/M10先注明被评对象（来源指导、审计报告中的指导或最终答复），再检查版本明确性与步骤可操作性，并与真正执行结果区分。M11为基于M1–M8的综合置信度，必须附公式和解释边界，不称为已校准正确概率。

M1 records discovery. M2 records **official content accessibility**: substantive text, navigation only, error, or unobserved; task-requirement coverage is recorded separately; static and server-rendered pages are treated according to returned content. **Access route** is a separate field: original entry, alternative entry, or unknown. An identical body obtained through a mirror retains its requirement coverage; delivered-content state and route are separate fields. M3 records the level of detail in official content; inaccessible content is unobserved, not presumed poor or task-resolving. M4 records source applicability and unresolved compatibility relations. M5/M6 retain third-party source counts, attribution, credibility, and uncertainty about independence. M7 distinguishes estimates from separate empirical tests. M8 retains raw search and acquisition counts and cost assumptions, rather than actual time, tokens, or fees. M9/M10 first identify the assessed artifact (source guidance, guidance in an audit report, or a final answer), then check its version specificity and procedural actionability, separately from actual execution. M11 is a composite confidence score based on M1–M8; it requires a disclosed formula and must not be interpreted as calibrated correctness probability.

## 5. 输出可复核证据链 / Report an inspectable evidence chain

每项诊断至少连接“任务需求→取得的内容→未支持的需求→编码依据→可采取的修复方向”。先呈现分项，综合分可选。复核者的身份类型、复核范围和真实分歧应明确记录；未进行的独立复核不写成已验证。

Connect each diagnosis to task requirements, obtained content, unsupported requirements, coding rationale, and a possible remediation. Report profiles before optional aggregates. State who reviewed the coding, their scope, and actual disagreements. Do not claim independent validation that was not performed.

## 算例：A的读取边界 / Worked example: access boundaries in A

档案中的转换任务需要ATC命令、输入/设备参数及设备信息步骤。日志记录quickstart提供这些内容，同时另一次参考页读取未取得正文。因此核心转换路径有支持，而完整参考并未取得。此判断不需要运行硬件。RAW中的fetch=3、fetch_fail=0与参考页缺失描述之间仍存在计数边界问题；保留差异，不能猜改成已确定的失败次数。

The archived conversion task requires an ATC command, input/device parameters, and a device-information step. The log records these in the quickstart while an additional reference read did not return its body. The main path thus has documentary support, but the full reference was not obtained. This observation requires no hardware-execution claim. The RAW values fetch=3 and fetch_fail=0 remain inconsistent or underspecified relative to the missing reference body; preserve the discrepancy instead of guessing a replacement count.

## 记录模板 / Recording template

见 `record-template-v0.3.json` 中每类数组的单条字段形状，以及 `data/worked-recording-example-a-cann.json` 中基于既有 A.cann 档案填写的示例。空值表示待记录，不是已完成的观测；旧版A表作为编制示例保留；v0.3实际URL与返回见原始记录对应表。原数据、归类修订和未决项见 `data/`；回溯重算脚本见 `scripts/build_paper_analysis.py`。

See the item schemas in `record-template-v0.3.json` and the worked example derived from the retained A.cann archive in `data/worked-recording-example-a-cann.json`. Empty fields are recording slots, not completed observations; the older A form remains an archival example; v0.3 URLs and actual returns are linked in the trace ledger. Frozen data, classification revisions, and unresolved issues are in `data/`; retrospective computation uses `scripts/build_paper_analysis.py`.

## v0.3 实际应用 / Applied records

见 data/trace-v0.3/applications.json（52单元）及 events.json（350条调用—返回对）。其中48单元选取官方读取，另4单元沿用整理记录。新M2类别不代入旧M11；M1/M5/M6/M7的历史判断注明保留来源，M8区分事件池与原计数。O-A01-E005先于E009，不能把其路径关系写成先失败再恢复。

See data/trace-v0.3/applications.json (52 units) and events.json (350 paired events). Official reads are selected for 48 units; four retain compiled assessments. New M2 categories are not substituted into historical M11. Retained judgments and new observations have separate provenance. Event pools are not the original M8 counters. O-A01-E005 precedes E009; no failure-to-recovery chronology is inferred.
