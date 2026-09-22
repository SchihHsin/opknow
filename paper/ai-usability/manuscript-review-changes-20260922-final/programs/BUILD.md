# 文件生成程序

这里保存的是本归档所对应的生成程序副本。它们来自论文工作区的 `paper/ai-usability/scripts/` 和 `paper/ai-usability/submission/`，用于追溯当前 HTML、Word、图稿和投稿 PDF 的生成链路。

## HTML

先由 Markdown 生成普通阅读版 HTML：

```bash
python3 paper/ai-usability/scripts/render_paper_reading.py
```

该脚本使用 Pandoc 3.11、`references.bib` 和 `acm-sig-proceedings.csl`，生成 `manuscript-cn-v0.2.html` 与 `manuscript-en-v0.2.html`。

再由 Python 添加左侧目录、语言切换和审阅导航：

```bash
python3 paper/ai-usability/scripts/build_hci_revision_review.py
```

它读取两个普通阅读版 HTML，嵌入图稿并生成 `manuscript-cn-review-changes.html` 与 `manuscript-en-review-changes.html`。归档目录中的 `index.html` 和英文审阅 HTML 是这两个输出的副本。

`render_manuscript_html.mjs` 是早期 v0.1 阅读版脚本，不是当前 v0.2 审阅稿的生成脚本。

## Word

英文 Word 稿由以下命令生成：

```bash
python3 paper/ai-usability/scripts/build_manuscript_docx.py
```

它读取 `manuscript-en-v0.2.md`，将 SVG 图稿栅格化为 PNG，调用 Pandoc 生成 DOCX，再用 `docx-layout.lua` 和 Python 做 OOXML 后处理。`before` 和 `ba96b79` 参数用于生成历史版本。

## 英文投稿 PDF

英文 ACM PDF 使用：

```bash
python3 paper/ai-usability/submission/build_acm.py --package
```

流程是 Pandoc 转 LaTeX，再由 Tectonic 编译 PDF。中文 PDF 和这些当前审阅 HTML 并非同一时间生成，归档中保留的是已有的历史 PDF。

## 运行环境说明

这些文件是程序和配置的溯源副本，不是已经改写成可脱离论文工作区运行的独立项目。重新生成时仍需要原工作区中的 `figures/`、`submission/.tools/pandoc`、Tectonic 以及相应的 Markdown 文件；本目录中的 HTML、Word 和 PDF 是已生成结果。
