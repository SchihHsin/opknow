# 方法论定位与修订方案 / Methodological Positioning and Revision Plan

2026-09-08 · 讨论稿 / Discussion draft

本稿按作者澄清调整投稿方案：方法论是主要贡献，CANN/CUDA 审计是应用和初步检验案例。下列贡献表述与章节结构是修订目标；尚未完成的独立复核或验证不能写成已完成结果。

This plan follows the author's clarification: the methodology is the primary contribution, and the CANN/CUDA audit serves as an application and a case for preliminary evaluation. The contributions and structure below are revision targets. Proposed validation must not be reported as completed research.

## 1. 保留原标题 / Retain the Original Title

**中文：AI 能找到开发者所需的知识吗？开发者生态中面向 AI 的知识可得性的定义与度量**

**English: Can AI Find What Developers Need? Defining and Measuring Knowledge Availability for AI in Developer Ecosystems**

该题目包含问题动机、核心概念和方法贡献，与作者意图一致。此前的替代题目强调 Auditing，是因担心现有证据不足而提出的保守定位，但会改变论文的贡献中心，现不推荐替换。Find 可以在引言中明确为发现、取得和判断任务适用性，避免只被理解为搜索命中；无需因此改题。

The title identifies the motivating question, the central construct, and the methodological contribution. The earlier alternative emphasized auditing to reduce the evidential burden, but that would shift the contribution away from the author's intended focus. The introduction should clarify that finding knowledge includes discovering it, obtaining it, and assessing its applicability to a task, rather than only retrieving a search result.

## 2. 核心论证 / Central Argument

**中文：** 本文提出并操作化“面向 AI 的知识可得性”，以任务级取证协议和分层指标识别技术知识从来源到行动建议之间的取得条件与证据缺口。CANN/CUDA 案例用于展示该方法怎样实施、能产生什么诊断，以及哪些结论依赖编码与聚合假设。

**English:** We define and operationalize knowledge availability for AI through a task-level evidence collection protocol and a layered indicator framework. The method examines the conditions and evidence gaps involved in obtaining technical knowledge for action-oriented recommendations. A CANN/CUDA case study illustrates its application, the diagnoses it supports, and the dependence of its conclusions on coding and aggregation assumptions.

## 3. 三项贡献 / Three Contributions

### C1 概念贡献 / Conceptual Contribution

**中文：** 定义面向 AI 的知识可得性，明确它是在给定任务、Agent 与工具配置、检索环境及时间条件下，技术知识能够被发现、取得并判断适用性的程度，区分其与检索命中、文档可用性及答案正确性的关系。

**English:** We define knowledge availability for AI as the extent to which technical knowledge can be discovered, obtained, and assessed for applicability under a specified task, agent and tool configuration, retrieval environment, and time. We distinguish this construct from retrieval hits, documentation usability, and answer correctness.

### C2 方法贡献 / Methodological Contribution

**中文：** 提出可追溯的任务级测量方法，分开来源条件、获取成本、产出检查和综合解释，提供任务选择、来源归类、证据记录、编码锚点、缺失处理与分析规则。

**English:** We introduce a traceable, task-level measurement method that separates source conditions, acquisition costs, output checks, and aggregate interpretation. The method specifies task selection, source classification, evidence recording, coding anchors, missing-data treatment, and analysis procedures.

### C3 案例与初步评价 / Case Application and Preliminary Evaluation

**中文：** 通过加速计算开发任务案例，展示该方法对知识取得障碍、版本不确定和跨来源补偿路径的诊断能力，并检查编码和聚合假设对诊断的影响，明确适用边界。

**English:** Through cases of software development tasks for AI-accelerated computing, we demonstrate how the method diagnoses barriers to knowledge access, version uncertainty, and cross-source compensating pathways. We examine how coding and aggregation assumptions affect these diagnoses and identify the method's scope.

案例中的 G 是 CUDA→ROCm/HIP 与 CUDA→CANN 的迁移类比，应明确分类；可保留用于方法覆盖范围的展示，但不能混入 CUDA/CANN 生态均值。其他任务对仍需逐项核对起点和目标范围。

Task G compares migration from CUDA to ROCm/HIP with migration from CUDA to CANN. It may illustrate the method's coverage of migration tasks, but must not be counted as an ordinary CUDA/CANN ecosystem pair. The starting conditions and outcome scope of other task pairs also require review.

## 4. 研究问题 / Research Questions

**RQ1 中文：** 如何定义并操作化开发者生态中面向 AI 的知识可得性，使任务所需知识的取得条件与证据缺口能够被系统记录和复核？

**RQ1 English:** How can knowledge availability for AI in developer ecosystems be defined and operationalized so that the conditions for obtaining task-relevant knowledge and the resulting evidence gaps can be systematically recorded and reviewed?

**RQ2 中文：** 将该方法应用于开发任务时，它能揭示哪些知识取得障碍与跨来源补偿路径，其诊断对编码和聚合假设的依赖及适用边界是什么？

**RQ2 English:** When applied to development tasks, what barriers to knowledge access and cross-source compensating pathways does the method reveal, and how do coding assumptions, aggregation choices, and scope conditions affect its diagnoses?

## 5. 从案例结果转向方法评价 / From Case Findings to Method Evaluation

| 方法应回答的问题 / Evaluation question | 现有基础与下一步 / Existing basis and next step |
| --- | --- |
| 为什么需要这些维度？ / Why are these dimensions needed? | 从知识取得过程与相关研究推导每个维度，明确指标之间的关系；不能只用案例出现了某问题来证明11项已经完备。 / Derive dimensions from the knowledge acquisition process and relevant literature. Case coverage alone does not establish that all 11 indicators are necessary or exhaustive. |
| 他人能否照此实施？ / Can others apply the method? | 将18、日志与脚本整合为操作协议，提供空白记录表和完整算例；准确描述原审计中发生的迭代修订。 / Integrate the metric definitions, logs, and scripts into a protocol with a blank recording form and a worked example. Document the actual iterative development of the audit. |
| 能否区分有意义的断点？ / Does it distinguish meaningful breakdowns? | 用A、D、E展示“检索命中”“取得正文”“正文够用”的不同；在相同日志上与只看命中或只看读取的简化诊断作对照，作为待补的分析。 / Use A, D, and E to distinguish retrieval, access, and adequacy. A proposed analysis should compare the framework's diagnoses with retrieval-only or access-only assessments using the same records. |
| 编码能否复核？ / Can the coding be reviewed consistently? | 日志已有问题、查询、命中和读取描述，可建立观察→编码→分项→结论映射；如能增加独立复核，报告真实分歧，不将AI子代理审阅算成人类专家验证。 / Map observations to codes, indicators, and conclusions. If independent review is added, report actual disagreements; AI subagent review is not human expert validation. |
| 结论有多依赖公式？ / How much do conclusions depend on aggregation? | 已有移除模型先验的敏感性复算，可进一步检查规则变化；改变假设后分数变化本身不否定方法，关键是解释变化与哪些结论仍成立。 / Existing sensitivity calculations remove the model-prior channel. Further checks can examine coding and aggregation choices. Score changes do not by themselves invalidate the method; their interpretation and consequences must be explicit. |
| 能推广到哪里？ / Where might the method transfer? | 说明适用对象和如何替换领域任务、术语及版本锚点。跨模型、跨时间和其他领域的稳定性仍待独立评价。 / Specify scope and how domain tasks, terminology, and version anchors can be adapted. Stability across models, time, and other domains remains to be evaluated. |

方法框架、具体指标和综合公式应分层。现有11项可作为一套操作化实现接受审查；其中模型先验属于需特别说明的估计，综合公式属于需验证的汇总选择。方法的价值不应完全依赖一个分数，也不能用方法定位免除对该分数的有效性要求。

The framework, its indicators, and its aggregation formula should be treated as distinct layers. The current 11 indicators form an operationalization to be examined. Model-prior assessments require particular care, and the composite formula is an aggregation choice requiring justification. The method's value need not depend entirely on one score, but a methodological framing does not remove the need to validate that score's interpretation.

## 6. task_run_log.md 的作用 / Role of the Process Log

该文件应是方法实施与演化的核心过程材料。它包含问题、实际查询、来源命中、读取结果和评分说明；第三批还记录了主代理对子代理观测的清洗，以及从 transcript 恢复问题原文的过程。应据此准确修订论文中“事后补编”等不一致说法，并区分早期判断、后续订正与最终编码。

The log is a core process record for the method's application and development. It includes task questions, queries, retrieved sources, access outcomes, and scoring explanations. It also records the consolidation of subagent observations and recovery of original questions from a transcript. The paper should reconcile inconsistent statements about reconstructed questions and distinguish early judgments, subsequent corrections, and final codes.

现有日志可以支持可追溯的回溯分析。精确模型配置、逐次完整返回和最终答案若未留存，应明确其可用性；不因缺少部分原始记录就否定整份日志，也不将过程摘要描述成逐字完整记录。

The existing log supports traceable retrospective analysis. The availability of exact model configurations, complete tool returns, and final answers should be stated explicitly. Missing records do not make the log valueless, but process summaries should not be described as complete verbatim traces.

## 7. 建议正文结构 / Proposed Paper Structure

| 中文 | English |
| --- | --- |
| 1 引言：为什么需要测量面向AI的知识可得性 | 1 Introduction: Why Measure Knowledge Availability for AI? |
| 2 相关研究与概念边界 | 2 Related Work and Construct Boundaries |
| 3 方法框架：任务、知识来源与证据取得条件 | 3 Framework: Tasks, Knowledge Sources, and Conditions of Access |
| 4 操作化：指标、取证协议、编码与分析 | 4 Operationalization: Indicators, Evidence Collection, Coding, and Analysis |
| 5 CANN 与 CUDA 开发生态的案例分析 | 5 Case Study of the CANN and CUDA Developer Ecosystems |
| 6 方法评价：诊断价值、可复核性与敏感性 | 6 Method Evaluation: Diagnostic Value, Reviewability, and Sensitivity |
| 7 讨论：对开发者生态和Agent产品设计的意义 | 7 Discussion: Implications for Developer Ecosystems and Agent Design |
| 8 局限与结论 | 8 Limitations and Conclusion |

篇幅应由贡献完整性决定，暂不以短论文篇幅限制方法论展开。第6节只报告实际完成的评价，未完成项进入局限或未来工作。

Length should follow the contribution rather than a predetermined short-paper target. Section 6 must report only evaluations actually completed; outstanding evaluations belong in limitations or future work.
