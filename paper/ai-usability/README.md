# AI 可用性论文工作区

## 当前版本：CHI 修订稿 v0.2 / Current CHI revision

保留原标题 **Can AI Find What Developers Need? Defining and Measuring Knowledge Availability for AI in Developer Ecosystems**。沿用原稿的方法论主线与三来源、11项指标，以既有审计作为应用案例；本次没有重新采集网页实验。

The original title and methodological focus are retained. The three-source, eleven-indicator framework is developed through its existing case application. This revision does not add a new website-acquisition experiment.

| 交付物 / Deliverable | 文件 / File |
| --- | --- |
| 中文可编辑稿 / Chinese manuscript | [manuscript-cn-v0.2.md](manuscript-cn-v0.2.md) |
| 中文阅读版 / Chinese reading page | [manuscript-cn-v0.2.html](manuscript-cn-v0.2.html) |
| 英文可编辑稿 / English manuscript | [manuscript-en-v0.2.md](manuscript-en-v0.2.md) |
| 英文阅读版 / English reading page | [manuscript-en-v0.2.html](manuscript-en-v0.2.html) |
| ACM 单栏匿名英文 PDF / ACM anonymous English PDF | [English review PDF](../../output/pdf/knowledge-availability-ai-chi2027-en-v0.2.pdf) |
| 中文阅读 PDF / Chinese reading PDF | [Chinese PDF](../../output/pdf/knowledge-availability-ai-cn-v0.2.pdf) |
| LaTeX 源码包 / Portable LaTeX source | [ACM source ZIP](submission/knowledge-availability-ai-acm-source-v0.2.zip) |
| 匿名数据与方法补充材料 / Anonymous data and protocol supplement | [Supplement ZIP](submission/knowledge-availability-ai-supplement-v0.2.zip) |
| 可复用协议、空白表与填写示例 / Protocol, blank form, and worked example | [Protocol, CN/EN](protocol-cn-en.md) · [JSON form](record-template.json) · [A.cann worked example](data/worked-recording-example-a-cann.json) |
| 核验后的文献 / Verified bibliography | [BibTeX](references.bib) · [Verification notes](bibliography-audit.md) |
| 数据与未决项 / Data and unresolved entries | [Data README](data/README.md) · [Corrections](data/generated/corrections.md) |
| 完成检查 / Completed checks | [Validation report](validation-v0.2.md) |

### 本次修订 / Revision focus

- 恢复原材料的分析主线：矩阵模式 → 获取与版本问题 → 任务知识支撑差异 → 供给侧与Agent侧设计 → 广覆盖改进与局部断点修复。正文保留综合置信度的定义和必要汇总，敏感性及计算口径集中于[双语补充分析说明](data/supplementary-analysis-notes-cn-en.md)。 / Restored the source analysis from matrix patterns through task-specific knowledge support to supply-side and agent-side design, distinguishing widespread improvements from localized repairs. Sensitivity and calculation details are consolidated in the bilingual supplementary analysis notes.

- 加强定义、指标角色、取证协议和观察到诊断的连接；案例仍用于论证方法的可操作性和诊断范围。 / Strengthened construct boundaries, indicator roles, recording procedures, and observation-to-diagnosis links.
- G 的 ROCm/HIP 迁移类比单列；主比较为25对，全部26任务52单元保留。 / G is a separate migration analogy; 25 pairs form the comparison and all 52 archival records remain available.
- 静态与SSR页面按取得内容同等描述；原评分单独冻结供追溯。M7标明先验估计，M9/M10不再暗示实际执行成功，M11明确为由M1–M8汇总的综合置信度。 / Access profiles describe acquired content regardless of rendering technology. Historical scores are preserved; prior estimates, response checks, and the Composite Confidence Score computed from M1–M8 are explicitly distinguished.
- 对照已保留日志修正批次、子Agent及问句恢复的描述，保留未能确定的配置与计数边界。 / Method reporting follows the retained log and explicitly identifies unavailable configuration and unresolved counting boundaries.
- 中英文段落、引文和公式对应；16项参考文献经过元数据核验；英文摘要165词。 / Aligned bilingual manuscripts, 16 bibliographically checked references, and a 165-word English abstract.

正文十五张图均提供中英文可编辑SVG；英文另有嵌入LaTeX的矢量PDF。图1为流程图，图2-5按解释段落穿插呈现评分规则，图6-9为完整指标矩阵分面及读取状态辅助图；图10-12为供给侧设计，图13-15为Agent侧设计。附录A补齐十一项指标的计算细则。六个示例随相关讨论出现，完整保留其他发现、第三方知识供给、优先级及方法复用论述。设计依据见[双语说明](data/design-illustrations-cn-en.md)。`scripts/build_paper_figures.py`生成原有图稿，`scripts/build_design_figures.py`生成设计插图，`scripts/render_paper_reading.py`生成阅读HTML，`submission/build_acm.py --package`生成ACM稿与源码包。

All fifteen main-text figures have editable English/Chinese SVGs and English vector PDFs for LaTeX. Figure 1 shows the workflow; Figures 2-5 interleave scoring rules with explanatory paragraphs; Figures 6-9 retain the full matrix and access profile. Figures 10-12 illustrate knowledge provision and Figures 13-15 illustrate agent interaction. Appendix A specifies all eleven scoring calculations. These selected examples accompany the broader discussion of findings, third-party knowledge, prioritization, and method reuse. The supplement includes provenance notes and twelve editable design SVGs.

v0.2是按CHI Papers要求准备的匿名稿件文件，不代表已经提交或已经获得方法有效性的外部验证。作者信息、PCS条目及最终作者审阅需在正式提交时完成。原稿v0.1与原研究页面继续保留如下，作为版本来源。

Version 0.2 provides anonymous manuscript files prepared for CHI Papers. It has not been submitted and does not claim external validation that was not performed. Author details, PCS entries, and final author review remain part of submission. Version 0.1 and the original research artifacts are retained below.

## 原稿 v0.1 与研究来源 / Original manuscript and research sources

本目录是独立于 DACT 用户研究的论文工作区。论文只基于 `opknow` 中已经完成的 26 项任务级 AI 可用性审计，不等待、不混入开发者访谈或协同任务研究。

- [中文论文初稿（可编辑源）](manuscript-cn-v0.1.md)
- [中文论文阅读版](manuscript-cn-v0.1.html)
- [中文论文 PDF 预览](../../output/pdf/ai-usability-technical-knowledge-ecosystem-cn-v0.1.pdf)
- [正文图 1：可编辑 Agent 证据循环（SVG）](figures/figure-1-agent-evidence-cycle.svg)
- [正文图 2：可编辑任务矩阵（SVG）](figures/figure-2-task-matrix.svg)
- [任务矩阵导出脚本](scripts/export_task_matrix_svg.py)
- [论文阅读版渲染脚本](scripts/render_manuscript_html.mjs)
- [任务矩阵](../../17_official_site_focus.html)
- [指标方法](../../18_metric_definition.html)
- [发现与反事实 ROI](../../19_findings_ux_synthesis.html)
- [检索记录](../../task_run_log.md)
- [评分脚本](../../score_metrics.py)

以上 v0.1 为早期中文源稿，配套 PDF 仅供阅读与版式校对。当前 CHI 匿名英文稿、双语修订稿、核验文献和新版图稿见本页顶部 v0.2 交付物索引。

两张正文图均为可编辑 SVG。`figure-1-agent-evidence-cycle.svg` 将 Agent 的检索、读取、先验、证据判断与收敛过程映射到测量框架；`figure-2-task-matrix.svg` 来自交互版任务矩阵的 52 个已渲染审计单元，文字和单元格均可编辑。若原始矩阵更新，在仓库根目录运行 `python3 paper/ai-usability/scripts/export_task_matrix_svg.py` 后再检查图和论文引用。

分段评分图由 `scripts/build_scoring_figure.py` 生成（Matplotlib，中英文 SVG/PDF）。各图紧随对应解释段落，分档共用刻度；M6等计算细则在附录A。 / The rubric figures accompany their explanatory paragraphs and use shared grade labels; detailed calculations appear in Appendix A.
