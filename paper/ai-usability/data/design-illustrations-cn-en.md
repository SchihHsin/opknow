# Design illustrations / 设计示意图

The discussion retains findings and implications beyond the six illustrated examples. Figures 10-14 connect official knowledge provision with agent feedback; Figure 15 illustrates source inspection and corrective feedback. Figures 10-15 adapt selected concepts from the findings and design-synthesis page into paper illustrations. They are proposed interfaces linked to the audit's task conditions. They are not screenshots of an evaluated implementation or transcripts of observed user interactions.

讨论保留六个示例之外的发现与启示。图10-14结合官方知识供给与Agent反馈，图15展示来源核验与纠错反馈。图10-15将原发现与设计综合材料中的部分概念整理为论文插图，依据审计任务的知识条件提出界面设计。它们不是经过评估的产品截图，也不是实际用户对话记录。

| Figure / 图 | Task evidence / 任务依据 | Proposed interaction / 拟议交互 |
| --- | --- | --- |
| 10 | A/I: multiple version trees and distributed compatibility information; M4. / A/I：多个版本树及分散配套信息；M4。 | Query constraints, supported combinations, provenance, and unresolved conditions. Version fields are placeholders. / 按条件查询受支持组合，保留依据与未决条件，版本字段为占位。 |
| 11 | A/I: source applicability depends on task environment; M4/M9. / A/I：来源适用性依赖任务环境；M4/M9。 | Record local facts separately and distinguish matched, mismatched, and unknown states. / 独立记录本机事实，区分匹配、不匹配与未知状态。 |
| 12 | E: accessible error page with generic advice; M3/M4. / E：错误页可读但建议泛化；M3/M4。 | Organize local facts, diagnostic checks, attributed cases, and unresolved branches. Case fields are placeholders. / 组织现场信息、诊断检查、案例依据与未决分支；案例为待填字段。 |
| 13 | A: retained conversion guidance; D: missing core body; M2-M4. / A：留存转换指导；D：核心正文缺失；M2-M4。 | Preserve task, version, parameters, and related steps in a proposed export. / 在拟议导出中保留任务、版本、参数及步骤关系。 |
| 14 | D: core how-to body not obtained; E: readable official error page with generic advice; M1-M3. / D：核心操作指南正文未取得；E：错误页可读但建议泛化；M1-M3。 | Different feedback and next actions: the agent first seeks body links or readable sources, retaining optional access to the original guide; diagnostic context and relevant log excerpts support further case retrieval. / 区分反馈与后续行动：Agent先寻找正文链接或可读来源，保留原始指南供按需查看；诊断情境与相关日志片段用于继续检索案例。 |
| 15 | A: acquired ATC command and parameter guidance from the commercial 80RC2 quickstart; source-version and response checks. / A：商用80RC2快速入门的留存ATC命令与参数指导；来源版本及回答层检查。 | Expand the cited passage, open the original page, and attach an error or correction to the original suggestion while retaining its source and task context. / 展开引用段落、访问原始页面，将报错或修正关联到原建议，并保留来源与任务上下文。 |

The command excerpts shown in Figures 13 and 15 are retained in `legacy_task_run_log.md`, lines 53-58, and the corresponding excerpt in `source_evidence.json`. Figure 13 shows abbreviated command and parameter fields; Figure 15 displays the retained source command across two lines for legibility and explicitly abbreviates the response line. The figure does not supply a verified target-device setting or assert that the command was executed.

图13和图15中的命令节选见 `legacy_task_run_log.md` 第53-58行及 `source_evidence.json` 对应片段。图13展示命令节选与参数字段；图15为易读性将来源命令分两行展示，回答中的命令另明确标为节选。图示不提供经核验的目标设备参数，也不声称执行过该命令。

The source material's design examples included illustrative dialogue, compatibility values, timing, and source-composition percentages. The paper illustrations retain the interaction concepts without asserting those illustrative values as measurements. The original title, task observations, scoring rules, and previously retained figures remain unchanged by this addition.

原材料的设计示例包含示意对话、配套值、耗时与来源组成比例。本次保留其交互概念，不把示意值呈现为测量结果。本次增图不改变原标题、任务观测、评分规则与此前保留的图稿。

Editable bilingual SVGs are included under `figures/` in this supplement. The English LaTeX source package includes the corresponding vector PDFs. No external service is required to view the SVGs.

本补充包的 `figures/` 下提供可编辑的双语SVG；英文LaTeX源码包包含对应矢量PDF。查看SVG无需外部服务。
