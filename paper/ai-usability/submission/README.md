# ACM CHI 英文匿名稿构建

本目录只提供排版和构建基础设施；论文内容来自上级目录的 `manuscript-en-v0.2.md`，文献来自 `references.bib`。没有复制 DACT 论文内容，也没有加入默认作者、机构、实验结果或 AI 使用声明。

使用真正的 ACM 类和参考文献样式：

```tex
\documentclass[manuscript,review,anonymous]{acmart}
\bibliographystyle{ACM-Reference-Format}
```

## 构建

在 `paper/ai-usability/` 目录运行：

```bash
python3 submission/build_acm.py --no-pdf
python3 submission/build_acm.py --package
```

第一条只检查并生成 LaTeX。第二条用 Tectonic 自动运行 LaTeX/BibTeX 和交叉引用，成功后输出到项目的 `output/pdf/knowledge-availability-ai-chi2027-en-v0.2.pdf`。构建日志和中间文件位于 `submission/_build/`；可移植 LaTeX 源码 ZIP 位于 `submission/knowledge-availability-ai-acm-source-v0.2.zip`。

`--only-cached` 可限制 Tectonic 只使用本机已缓存的 TeX 依赖。`--source`、`--bibliography` 和 `--output` 可覆盖默认路径。工具只在编译成功且引用没有缺项时更新交付 PDF；成功编译仍需要逐页视觉检查。

## Markdown 约定

- 第一个 `#` 标题保留已经确定的英文题目；也支持 YAML `title`。
- 使用 `## Abstract`、`## Keywords`；构建时提取为 ACM 的摘要、关键词，正文从 `## Introduction` 开始。正文标题不手写编号。
- 文献写为 `[@citationKey]` 或 `[@firstKey; @secondKey]`，键必须存在于 `references.bib`。
- 行内/独立公式使用 `$...$` / `$$...$$`。普通 Markdown 表格、列表和代码块由 Pandoc 转换。
- 图片示例：

```markdown
![A caption describing the framework.](figures/figure-1-framework-en.svg){#fig:framework description="Accessible description of the complete diagram."}
```

SVG 路径会自动改用相邻同名 PDF；SVG→PDF 的图稿导出由图表脚本完成。构建不会把 SVG 栅格化。图片必须具有 `description`，将转换为 ACM `\Description{}`。构建包内图片使用相对路径，元数据不写入用户路径。

CCS 分类未由模板猜测，当前不显示 CCS。需要加入时应在确认具体 ACM 分类后扩展模板。匿名稿不添加会议、DOI、版权和作者机构占位信息；这些属于接受后的正式制作流程。

## 工具来源

- Pandoc 3.11：来自官方 `jgm/pandoc` GitHub release，macOS arm64 ZIP 的 SHA-256 固定为 `15806bedf9517bfead72e88fe6a6696635c3691efbb6e152173440e9c5bb50b4`。副本位于被 Git 忽略的 `.tools/pandoc`。重装只需 `python3 submission/bootstrap_tools.py`，不修改系统设置。
- Tectonic：优先环境变量 `TECTONIC`，其次 PATH、本目录 `.tools/tectonic`，再检测本机 Codex LaTeX 插件的 `bin/tectonic`。已发现可运行的 0.17.0。所需 `acmart.cls` 等依赖由 Tectonic 官方 bundle 提供并缓存，不修改或手工重造 ACM 类。
- 如使用其他平台，可设置环境变量 `PANDOC` 和 `TECTONIC` 指向本机工具。

源码 ZIP 可直接在 Overleaf 中以 `main.tex` 为主文档编译，保留相同 ACM 单栏匿名审稿格式。
