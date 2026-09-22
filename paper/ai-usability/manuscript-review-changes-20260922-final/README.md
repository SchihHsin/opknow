# 2026-09-22 批注修订审阅稿

本目录从 `manuscript-cn-review-changes/` 独立复制而来，保留归档稿的历史试跑范围与版本状态，并依据 `revisions/full-rerun-20260921/comment-revision-notes-20260922.md` 完成四类批注修改及“根因诊断与不确定性”补充。本目录不修改原始归档文件夹。

网页入口：

- [中文审阅页](index.html)
- [English review page](manuscript-en-review-changes.html)

主要改动包括研究缺口与本文增量、指标选择逻辑及边界、量规与权重形成过程、案例与发现章节的诊断定位、指标文献依据表，以及跨生态差异的根因分类和不确定性说明。`programs/` 保留归档提供的生成程序和 BUILD 说明；PDF、Word 和 Markdown 历史交付物仅作为本副本的上下文，不宣称已与 HTML 全量同步。

原归档说明如下。

这个文件夹保存当前中文、英文审阅页，以及目前已有的 Markdown、Word 和 PDF 版本。

## 中文版

| 文件 | 状态 |
| --- | --- |
| `index.html` | 当前中文审阅页的副本，对应仓库上层的 `manuscript-cn-review-changes.html`。打开文件夹时可直接访问。 |
| `manuscript-cn-v0.2.md` | 当前已有的中文 Markdown v0.2；它不是由当前审阅页反向导出的精确快照。 |
| `knowledge-availability-ai-cn-v0.2.pdf` | 当前已有的中文 PDF v0.2；生成时间为 2026-09-11，早于当前审阅页，因此不宣称与审阅页完全同步。 |

## 英文版

| 文件 | 状态 |
| --- | --- |
| `manuscript-en-review-changes.html` | 当前英文审阅页的副本，对应仓库上层的 `manuscript-en-review-changes.html`。 |
| `manuscript-en-v0.2.md` | 当前已有的英文 Markdown v0.2。 |
| `manuscript-en-v0.2.docx` | 当前已有的英文 Word 稿。 |
| `knowledge-availability-ai-chi2027-en-v0.2.pdf` | 英文 v0.2 PDF。 |
| `knowledge-availability-ai-chi2027-en-analysis-revision.pdf` | 英文分析修订版 PDF。 |
| `knowledge-availability-ai-chi2027-en-approval.pdf` | 英文审批版 PDF。 |
| `knowledge-availability-ai-chi2027-en-m2-revision.pdf` | 英文 M2 修订版 PDF。 |
| `knowledge-availability-ai-chi2027-en-method-wording.pdf` | 英文方法措辞版 PDF。 |
| `knowledge-availability-ai-chi2027-en-before-20260912.pdf` | 2026-09-12 前版本 PDF。 |

英文 Markdown、Word 和 PDF 是 v0.2 或更早的已生成稿；目前没有与 `manuscript-en-review-changes.html` 完全同步生成的英文 Markdown/PDF。论文工作区的 `README.md` 也记录了这一版本关系。

## 生成程序

对应的 Python、Pandoc 配置和 PDF 构建脚本已放在 [`programs/`](programs/)；生成链路和依赖见 [`programs/BUILD.md`](programs/BUILD.md)。
