# 任务级知识可得性测量协议 / Task-Level Knowledge Availability Protocol

本协议是论文v0.2的可复用操作说明。原案例是迭代形成的回溯性应用，不声称原52单元从一开始就满足本协议的全部字段。

This protocol is the reusable specification accompanying manuscript v0.2. The case application developed iteratively; the original 52 records are not claimed to have satisfied every field prospectively.

## 1. 定义任务与条件 / Define the task and conditions

记录结果目标、初始材料、适用版本、约束，以及支撑下一步行动所需的证据。记录Agent/模型、工具、语言、搜索环境、时间和上下文策略；不明信息填null并说明。比较任务必须说明起点和范围差异，不能只因名称相似就宣称严格等价。

Record the desired outcome, starting artifacts, versions, constraints, and evidence requirements. Record the agent/model, tools, language, search environment, time, and context policy. Use null with an explanation for unknown fields. Describe differences between comparison tasks rather than assuming controlled equivalence.

## 2. 预先说明记录边界 / State the recording boundary

注明哪些观察新采集、哪些复用。设置并记录检索预算或可观察的停止规则。分别计数检索、读取、失败、改词；同时说明计数是否包含辅助参考页。无法从原记录确定的规则不能事后冒充既定实验设置。

Identify newly acquired and reused observations. Specify a retrieval budget or observable stopping rule. Count searches, reads, failures, and refinements separately, stating whether ancillary references are included. Do not retrospectively invent missing experimental settings.

## 3. 保留来源与返回 / Retain sources and returns

逐次保留查询词、URL、返回内容或可定位摘录、来源发布者、角色与已知日期。官方材料按发布主体归属判断，不能按GitHub/CSDN等托管平台简单判断；跨域转载不是自动独立。替代入口应关联原失败入口。

Retain queries, URLs, returns or locatable excerpts, publisher identity, source role, and known dates. Classify official ownership by the publisher, not the hosting platform. Cross-domain reproduction does not establish independence. Link an alternative access route to the original attempt.

## 4. 编码与缺失 / Code observations and missingness

M1记录官方发现路径。M2记录**官方正文可获取性**。M2在本研究的工具配置下，首先判断robots访问限制，再依据页面交付方式与实际返回结果评分：robots限制为1分，SPA导致正文未取得为2分，任务相关正文部分可获取为3分，服务端渲染正文可获取为4分，静态正文可获取为5分。3分表示部分目标正文已取得、另有目标正文因技术障碍未取得；它不表示已取得资料不够详尽，也不因使用替代入口而自动赋予。未知状态单独标记，不据此推定分值。**访问路径**另列为原入口、替代入口或未知。完整正文即使经镜像取得，仍记为“核心正文已取得＋替代入口”，而不能因为入口替代就降为部分内容。M3记录官方正文的详尽层级，未读取时记unobserved，不推断成低质量或任务已经解决。M4记录资料的适用版本与未解决的配套关系，多版本存在不自动等于模糊。M5/M6保留第三方来源的条数、归属、可信度及独立性的不确定。M7标明自评/推断或另行实测，不能将自评当训练覆盖事实。M8保留原始检索与获取次数及成本公式，不将其表述为实际耗时、Token或费用。M9/M10分别检查回答的版本明确性与步骤可操作性，并与真正执行结果区分。M11为基于M1–M8的综合置信度，必须附公式和解释边界，不称为已校准正确概率。

M1 records discovery. M2 records **official content accessibility**. Under the study’s tool configuration, M2 first considers robots restrictions, then page delivery and observed returns: robots restriction, 1; SPA preventing body retrieval, 2; partial retrieval of task-relevant bodies, 3; retrievable server-rendered body, 4; retrievable static body, 5. Grade 3 means that some targeted body content was obtained while other targeted body content remained technically inaccessible; it does not denote insufficient detail in obtained material or follow automatically from using an alternative entry. Unknown acquisition status is recorded separately without inferring a score. **Access route** is a separate field: original entry, alternative entry, or unknown. A complete body obtained through a mirror is therefore coded as “core content obtained + alternative entry,” not downgraded to partial content merely because the route differed. M3 records the level of detail in official content; inaccessible content is unobserved, not presumed poor or task-resolving. M4 records source applicability and unresolved compatibility relations. M5/M6 retain third-party source counts, attribution, credibility, and uncertainty about independence. M7 distinguishes estimates from separate empirical tests. M8 retains raw search and acquisition counts and cost assumptions, rather than actual time, tokens, or fees. M9/M10 respectively check response version specificity and procedural actionability, separately from actual execution. M11 is a composite confidence score based on M1–M8; it requires a disclosed formula and must not be interpreted as calibrated correctness probability.

## 5. 输出可复核证据链 / Report an inspectable evidence chain

每项诊断至少连接“任务需求→取得的内容→未支持的需求→编码依据→可采取的修复方向”。先呈现分项，综合分可选。复核者的身份类型、复核范围和真实分歧应明确记录；未进行的独立复核不写成已验证。

Connect each diagnosis to task requirements, obtained content, unsupported requirements, coding rationale, and a possible remediation. Report profiles before optional aggregates. State who reviewed the coding, their scope, and actual disagreements. Do not claim independent validation that was not performed.

## 算例：A的读取边界 / Worked example: access boundaries in A

转换任务需要ATC命令、输入/设备参数及设备信息步骤。日志记录quickstart提供这些内容，同时另一次参考页读取未取得正文。因此核心转换路径有支持，而完整参考并未取得。此判断不需要运行硬件。RAW中的fetch=3、fetch_fail=0与参考页缺失描述之间仍存在计数边界问题；保留差异，不能猜改成已确定的失败次数。

The conversion task requires an ATC command, input/device parameters, and a device-information step. The log records these in the quickstart while an additional reference read did not return its body. The main path thus has documentary support, but the full reference was not obtained. This observation requires no hardware-execution claim. The RAW values fetch=3 and fetch_fail=0 remain inconsistent or underspecified relative to the missing reference body; preserve the discrepancy instead of guessing a replacement count.

## 记录模板 / Recording template

见 `record-template.json` 中每类数组的单条字段形状，以及 `data/worked-recording-example-a-cann.json` 中A.cann任务的填写示例。空值表示待记录，不是已完成的观测；示例提供实际访问的URL与获取结果，不声称已完成硬件执行。原数据、归类修订和未决项见 `data/`；回溯重算脚本见 `scripts/build_paper_analysis.py`。

See the item schemas in `record-template.json` and the worked example for task A.cann in `data/worked-recording-example-a-cann.json`. Empty fields are recording slots, not completed observations; the example provides the accessed URLs and acquisition outcomes without claiming hardware execution. Frozen data, classification revisions, and unresolved issues are in `data/`; retrospective computation uses `scripts/build_paper_analysis.py`.
