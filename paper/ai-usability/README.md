# AI 可用性论文工作区

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

当前稿件是内容定稿前的可编辑中文源文件。PDF 为阅读与版式校对预览，不等同于已选定投稿会刊的匿名模板。待选定投稿场所后，再从该源稿裁剪篇幅、补齐并核验参考文献、制作正式矢量图，并转换为该刊/会的匿名模板。

两张正文图均为可编辑 SVG。`figure-1-agent-evidence-cycle.svg` 将 Agent 的检索、读取、先验、证据判断与收敛过程映射到测量框架；`figure-2-task-matrix.svg` 来自交互版任务矩阵的 52 个已渲染审计单元，文字和单元格均可编辑。若原始矩阵更新，在仓库根目录运行 `python3 paper/ai-usability/scripts/export_task_matrix_svg.py` 后再检查图和论文引用。
