# CHI 2027 投稿可行性审阅与英文定位草案

审阅日期：2026-09-08。此文件为内部讨论稿，不修改原论文或原始评分，不是投稿就绪声明。范围为 AI 知识可得性审计；不混入 DACT 参与者研究。

> 定位更新（同日，按作者澄清）：论文以方法论为主要贡献，CANN/CUDA 审计作为应用与初步检验案例。保留原标题 *Can AI Find What Developers Need? Defining and Measuring Knowledge Availability for AI in Developer Ecosystems*。下文将论文收窄为审计论文的建议及替代标题已不作为推荐方向；具体证据问题与算术核验仍有效。后续方案提供中英文对照，见 [方法论定位与修订方案](methodology-positioning-cn-en-v0.1.md)。

## 判断

研究问题与 CHI 相关，但现稿直接翻译投稿风险较高。可发展的贡献是：开发者把信息寻径委托给 Agent 后，技术知识能否成为可引用、可判定版本、可组织下一步行动的证据，以及哪些知识供给断点需要被文档与 Agent 界面显式表达。

CHI 不要求每篇论文都有用户实验；证据和验证方式应与贡献匹配。本稿更适合定位为回溯性任务审计与案例分析。现有材料尚不能支撑经过校准的答案正确概率、实际执行成功率、人类体验改善或完整协同过程的经验结论。

## 官方要求（2026-09-08 核实）

- 会次为 CHI 2027，Papers 截止：2026-09-10 日终 AoE，即北京时间 2026-09-11 19:59:59。
- 今年没有独立摘要截止；正文、视频与补充材料同日截止。
- 摘要不超过 150 英文词。鼓励正文 5,000–8,000 词；约 5,000 词及以下的短论文也在同一 Papers 审稿流程中，不降低质量要求。
- 评审稿使用单栏 ACM 模板，匿名要求覆盖正文、补充材料和外链。现有中文 HTML 转 PDF 是阅读预览，不能直接充当正式评审稿。
- 作者需准备 ORCID，PCS 的 DBLP 字段填写个人页面或 n/a；提交前确认全体作者、机构及审稿责任信息。
- 官网另有 24 小时应急宽限说明，但明确要求不将其当作延期。计划以正式截止为准。

来源：

- https://chi2027.acm.org/authors/papers/
- https://chi2027.acm.org/guide-to-a-successful-submission/
- https://chi2027.acm.org/chi-publication-formats/

## 具体证据问题与修订优先级

| 问题 | 可核查位置 | 修订建议 |
| --- | --- | --- |
| 综合分称为“置信度”，但没有用独立判断的答案正确性或执行结果进行校准；模型先验来自自评 | manuscript-cn-v0.1.md §3.3–3.4；score_metrics.py 706–711、740–750 行 | 改称启发式证据可得性指数，主结果呈现分项观测与案例。将模型先验列为推断，独立展示并做移除分析；三渠道不应被当作独立成功概率。 |
| 可抓取性按网页实现类型扣分：static=5、SSR=4，即使正文均已取得 | score_metrics.py 658–660 行 | 按实际取得的任务所需正文完整性重新编码；保留网页类型作描述变量。不能直接把所有 SSR 改满分，须核对正文取得情况。 |
| 迁移任务 G 的“CUDA 侧”查的是 AMD ROCm/HIP 文档 | task_run_log.md 253–280 行；score_metrics.py 249–268 行 | 从 CUDA/CANN 主比较中移出，保留为单列迁移案例。主分析可采用其余 25 对，但仍需审查其他问题对的起点、范围与资料归属。 |
| 官方/第三方归类没有完全统一 | score_metrics.py 273–275 行将 NVIDIA 开发者博客作为二手来源 | 审计全部来源，区分同生态官方、其他机构官方、独立第三方与转述；平台不同不能自动证明内容独立。 |
| 方法陈述未准确反映运行与资料恢复过程 | task_run_log.md 334–338 行说明后批由 sub-agent 并行，问句从 transcript 恢复；稿件 239 行仍写部分问题事后补编 | 对照可取得记录修正方法。区分同一模型系统与多个 Agent 会话，交代评分者/编码者、工具、日期、检索与停止条件及缺失字段。问句恢复声明需保留出处，不能未经核实继续写成事后编造。 |
| 时序图包含建模内容，示范代码不等于当时实验配置 | 20_human_ai_journey.html 346、683、814、828–829 行 | 图可用作概念解释；仅检索部分作为观测。不要由示范代码填写模型版本，也不要把开发阶段、三档自主度或内部停止动机当作已测事实。 |
| “步骤可复现性”没有硬件运行验证；“ROI”来自公式反事实 | manuscript-cn-v0.1.md §3.3、4.6、6 | 将步骤指标明确为所记录步骤的完整性/可执行性判断。ROI 改为评分模型的情境或敏感性分析，不声称真实收益或因果效果。 |

17–20 HTML 含有可用的来源、过程描述和分析细节；其中 17 是矩阵与逐格解释，18 是指标方法，19 是综合解释和方案，20 是检索事实与流程建模的组合。它们不能自动替代逐次工具返回、原始最终答案或实测模型配置；目前并未据此确认这套完整记录是否仍在其他位置保存。

## 已完成的算术核验

以下是对现有 score_metrics.py 的只读复算，未改数据或重跑网页实验。均值取逐任务综合分再平均。移除先验是将 OWN 贡献置零，其他分项不动，不是新增的无检索实验。

| 情境 | CANN 均值 | CUDA/现有 cuda 列均值 | 含义 |
| --- | ---: | ---: | --- |
| 原 26 行 | .736269 | .920423 | 稿件的 .736/.920 可复算，但含 G 的比较范围问题。 |
| 原 26 行，移除模型先验渠道 | .605873 | .847663 | 比较方向保持，数值与档位明显依赖模型先验设定。 |
| 排除 G，保留其他原设定 | .731920 | .922040 | G 的移出没有改变总体方向。不能据此跳过其他编码审计。 |

移除先验后，CANN 的档位为 3 高、7 中高、13 中、2 低、1 很低，D=.181、E=.388、M=.446；CUDA 为 20 高、4 中高、2 中。此处“高低”均仅是原启发式阈值。

公式另有明显饱和性质：当模型先验为 5 时，OWN=1，K 恒等于 1，官方与第三方渠道对 K 不再有影响。当前 cuda 列 14/26 行符合这一条件。故不能把高综合分解释为已验证的外部证据充分。

原稿版本指标提升至 5 时平均增分约 .104、16 项跨档也可复算；这验证了运算，不验证现实改版会产生相同收益。

## 截止前值得做的强化

1. 先整理证据账本：每项任务的问题、查询、来源、读取状态、可定位的最终答案、日期、编码依据与缺失项。优先核对影响正文主张的单元。
2. 修正比较范围和编码规则；分开直接观测、研究者编码、模型自评/推断及公式输出。
3. 以 D（正文未取得）、E（正文可读但不足）、I 或 X（版本/替代证据）构成三组完整案例。每例展示“任务需要→实际取得→缺失→能支持到哪一步”，只引用已保存的实际内容。
4. 保留分项矩阵，缩减总分排名；做先验移除、聚合方法及版本折扣敏感性检查。新增复核或重跑应明确标为新的日期和条件。
5. 如果有能参与的合作者，让其按明确规则独立复核代表案例，记录分歧。AI 子代理审阅不能写成独立人类专家验证。
6. 对照开发者信息寻径、文档/API 研究、检索与答案归因评价、人机核验等文献，明确本文增加了什么。现稿参考文献仍是起步版本，需核对并补充相关近年工作。
7. 英文按收敛后的论证重写，目标约 4,500–5,000 词，以贡献完整为准；再完成英文图、ACM 单栏匿名稿、引用、图像描述及匿名补充包。

不建议在这次截止前扩展为完整的 20 人 DACT 研究，也不应将其未来实验写入本稿结果。若现有过程证据无法支撑最核心的案例和方法描述，英文排版完成也不足以解决投稿质量问题。

建议安排：9 月 8 日晚冻结定位和证据问题；9 月 9 日完成关键复核、方法与结果修订，并同步英文正文；9 月 10 日完成图表、引用、匿名模板和首次提交；9 月 11 日作为正式截止前的纠错余量。该安排是工作建议，不是已安排的自动化或已完成的提交。

## 英文定位草案（用于讨论）

**From Retrieved Pages to Actionable Evidence: Auditing Knowledge Availability for AI-Assisted Development**

以下为讨论版摘要，尚未替代原稿。任务数量和定量结果待比较范围与编码修订后再加入。

AI agents increasingly mediate developers’ access to documentation and community knowledge. Yet retrieving a page does not ensure access to evidence for a version-specific next step. We examine knowledge availability for AI through a retrospective audit of retrieval records for software development tasks for AI-accelerated computing. The audit distinguishes inaccessible content from readable but insufficient guidance, fragmented version information, and limited alternative evidence. We separate recorded retrieval observations from interpretive assessments and heuristic aggregation. Contrasting cases motivate design considerations for documentation infrastructure and agent interfaces that expose source access, version uncertainty, and verification needs. The study offers a task-level approach to inspecting the evidence available during delegated information foraging. Its scores describe conditions observed in the audited records; they do not measure answer correctness, execution success, or developers’ experience.

建议英文结构：Introduction → Related Work → Retrospective Audit Method → Evidence Breakdowns and Contrasting Cases → Sensitivity of the Heuristic Index → Design Implications → Limitations → Conclusion。
