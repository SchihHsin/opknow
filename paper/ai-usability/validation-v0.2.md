# v0.2 交付验证 / Delivery validation

完成日期 / Completed: 2026-09-09

本记录汇总本次修订中已经完成的内容、计算和文件检查。验证范围是交付物一致性与已有材料的可追溯性，不是对测量方法有效性的独立验证，也不是新的网页实验。

This record summarizes completed content, calculation, and artifact checks. It verifies delivery consistency and traceability to retained materials, not independent validity of the measurement method or a new web experiment.

## 内容与双语一致性 / Content and bilingual consistency

| 检查 / Check | 结果 / Result |
| --- | --- |
| 题目与定位 / Title and positioning | 保留原标题及原稿的方法论主线，审计作为应用案例。 / Original title and methodological focus retained; the audit remains the application case. |
| 英文摘要 / English abstract | 141词，低于150词上限。 / 141 words, within the 150-word limit. |
| 双语对应 / Bilingual alignment | 段落块数量、标题层级序列和引文序列一致。 / Matching paragraph-block counts, heading-level sequences, and citation sequences. |
| 文献 / References | 16个引用键均有书目记录；两份HTML均渲染16项参考文献。元数据核验范围见书目审计。 / All 16 citation keys resolve and appear in both HTML bibliographies; verification scope is documented in the bibliography audit. |
| 图稿 / Figures | 正文五张图（流程图、三张完整矩阵分面与读取状态辅助图）均提供中英文SVG；英文另提供LaTeX所用矢量PDF，图稿路径有效。 / All five main-text figures (workflow, three full-matrix facets, and access-profile detail) have Chinese/English SVGs and English vector PDFs for LaTeX; figure paths resolve. |
| 原件保留 / Original records | v0.1和原研究页面保留；冻结数据保留历史评分与来源哈希。 / Version 0.1 and source research pages remain available; frozen data preserve historical scores and source hashes. |

## 已有数据的本地核验 / Local checks of retained data

- 全部归档为26任务、52单元；G的ROCm/HIP迁移类比单列，主比较为25对、50单元。 / The archive contains 26 tasks and 52 units; the ROCm/HIP migration analogy G is separate from the 25-pair, 50-unit comparison.
- 25对原公式的精确均值为CANN .731902、CUDA .922067；移除模型先验项后为 .602049、.846369。这是对固定记录的计算，不是无检索条件下的新模型实验。 / Exact legacy-formula means for 25 pairs are .731902/.922067; removing the prior term gives .602049/.846369. These are calculations over fixed records, not new no-retrieval model trials.
- 正文另标明26行历史复算的范围，避免与25对主比较混用。 / The manuscript explicitly labels the separate 26-row historical reproduction.
- 可移植分析脚本从其他工作目录运行并产生确定性输出；补充包在独立临时目录解压后离线运行成功。 / The portable analysis runs deterministically from another working directory; the extracted supplement ran successfully offline in a separate temporary directory.
- 原始评分与描述性内容取得状态分开；访问路径不由历史 `core_fetch` 字段追溯推断。A.cann计数边界仍标为未决，没有猜测补齐。 / Historical scores and descriptive content-acquisition states remain distinct; access route is not inferred retrospectively from the historical `core_fetch` field. The unresolved A.cann counting boundary is not filled by guesswork.
- 已新增 A.cann 填写示例，逐项连接任务需求、事件、来源、留存证据、内容状态／访问路径及指标编码；它只重述既有档案，不创建新观测。 / A new A.cann worked record connects requirements, events, sources, saved evidence, content status/access route, and indicator codes; it only restates retained archival material and creates no new observation.

## 排版与打包 / Rendering and packaging

| 检查 / Check | 结果 / Result |
| --- | --- |
| 英文PDF / English PDF | ACM单栏匿名审稿格式，16页。 / ACM single-column anonymous review format, 16 pages. |
| 中文PDF / Chinese PDF | 中文阅读与校对版，17页。 / Chinese reading and proofreading edition, 17 pages. |
| 逐页视觉检查 / Page-by-page visual inspection | 最终两份PDF全部33页均已渲染检查；未发现裁切、文字重叠或不可读图表。 / All 33 final pages were rendered and inspected; no clipping, text overlap, or unreadable figures were identified. |
| 引用与溢出 / References and overflow | 最终TeX日志无未解析引用或Overfull hbox。 / No unresolved references or Overfull hbox in the final TeX log. |
| 文本与身份路径 / Text and identity paths | 两份PDF可提取文字，无替换字符，正文无本机用户路径或用户名。 / Text extraction succeeds without replacement characters or local user paths/names in the PDF text. |
| ZIP完整性 / ZIP integrity | 源码包7项、补充包19项；完整性检查通过，无绝对或越界成员路径。 / Seven source-package entries and 19 supplement entries; integrity checks pass without absolute or traversal member paths. |

最终PDF的SHA-256 / Final PDF SHA-256:

```text
English: c93596f39fd74c3ec16461a6f27da971ebdb9b05d290bdb62d42d6efa5fb279b
Chinese: 1cf4edb0ccc160a514a6ab1ffe2b26c49959b906abfe58a5bdd4813c450405fa
```

英文构建使用缓存中的真实ACM `acmart` v1.83（2022-02-19）及Tectonic 0.17.0。此记录没有把缓存类的版本表述为最新版本。源码包可交给作者在自己的ACM/Overleaf环境继续维护。

The English build uses the authentic cached ACM `acmart` v1.83 (2022-02-19) and Tectonic 0.17.0; the cached class is not represented as the latest release. Authors can maintain the source package in their own ACM/Overleaf environment.

## 仍然存在的研究边界 / Remaining research limits

精确模型版本、完整工具配置、逐次完整返回和最终答案未在全部归档单元中统一保留。现有材料不能据此宣称独立人工核验、评分者一致性、真实硬件运行、用户研究或部署干预效果。M7是先验估计，M9/M10是记录中指令的检查，M11是启发式指数；三者均按此边界陈述。

Exact model versions, full tool configurations, complete returns, and final answers are not uniformly retained across the archive. The materials do not establish independent human verification, inter-rater reliability, hardware execution, a user study, or intervention effects. M7 is a prior estimate, M9/M10 inspect recorded instructions, and M11 is a heuristic index.

文件已经生成并检查，尚未向CHI提交。正式提交仍需作者完成最终全文审阅、作者与PCS条目以及适用声明。本记录不表示已经获得外部方法验证或录用保证。

The files have been generated and checked but have not been submitted to CHI. Final author review, authorship and PCS entries, and applicable declarations remain part of submission. This record does not establish external methodological validation or guarantee acceptance.
