#!/usr/bin/env python3
"""Export the rendered 26-task audit matrix as an editable SVG figure.

The interactive matrix remains the authoritative exploration view in
``17_official_site_focus.html``. This exporter renders its populated table in
headless Chrome, then writes a print-oriented SVG with native text and vector
rectangles. No raster screenshot is used, so the figure can be edited in
Illustrator, Figma, Inkscape, or a vector-aware presentation tool.
"""

from __future__ import annotations

from html import escape
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "17_official_site_focus.html"
OUTPUT = ROOT / "paper" / "ai-usability" / "figures" / "figure-2-task-matrix.svg"


class MatrixParser(HTMLParser):
    """Collect the generated ``#hmbody`` cells from Chrome's DOM dump."""

    def __init__(self) -> None:
        super().__init__()
        self.in_body = False
        self.current: dict[str, str] | None = None
        self.rows: list[list[dict[str, str]]] = []
        self.row: list[dict[str, str]] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag == "tbody" and attr.get("id") == "hmbody":
            self.in_body = True
        elif self.in_body and tag == "tr":
            self.row = []
        elif self.in_body and tag == "td" and self.row is not None:
            self.current = {
                "class": attr.get("class", ""),
                "rowspan": attr.get("rowspan", "1"),
                "text": "",
            }

    def handle_data(self, data: str) -> None:
        if self.current is not None:
            self.current["text"] += data

    def handle_endtag(self, tag: str) -> None:
        if tag == "tbody":
            self.in_body = False
        elif self.in_body and tag == "td" and self.current is not None and self.row is not None:
            self.current["text"] = " ".join(self.current["text"].split())
            self.row.append(self.current)
            self.current = None
        elif self.in_body and tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None


def rendered_dom() -> str:
    chrome = next(
        (
            candidate
            for candidate in (
                Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
                Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
            )
            if candidate.exists()
        ),
        None,
    )
    if chrome is None:
        raise SystemExit("Chrome/Chromium is required to render the source matrix.")
    with tempfile.TemporaryDirectory() as profile:
        command = [
            str(chrome),
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            f"--user-data-dir={profile}",
            "--virtual-time-budget=3500",
            "--dump-dom",
            SOURCE.as_uri(),
        ]
        # macOS Chrome can leave an updater child alive after writing stdout.
        # Its partial stdout is already a complete DOM, so retain it on timeout.
        try:
            run = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=18, check=False)
            dom = run.stdout
        except subprocess.TimeoutExpired as error:
            dom = error.stdout or ""
            if isinstance(dom, bytes):
                dom = dom.decode("utf-8", errors="replace")
    if "id=\"hmbody\"" not in dom:
        raise SystemExit("The source matrix did not render; no SVG was written.")
    return dom


PALETTE = {
    "v5": ("#EFF5FF", "#667EAF"),
    "v4": ("#EEF7EE", "#5B8960"),
    "v3": ("#FCEFC7", "#92620A"),
    "v2": ("#FAD7BC", "#9A4A12"),
    "v1": ("#F7C0C0", "#A11414"),
    "blk": ("#E7EAF1", "#5B6070"),
}
METRICS = [
    ("可发现", "官方命中"), ("可抓取", "页面正文"), ("正文详尽", "命令/参数"),
    ("版本清晰", "版本关系"), ("二手数量", "独立来源"), ("二手可信", "质量/互证"),
    ("模型先验", "知识覆盖"), ("检索成本", "少为好"), ("版本可锁", "适用组合"),
    ("可复现", "步骤可执行"), ("综合", "置信度"),
]
GROUPS = [("官方知识", 0, 4, "#EAF0FF"), ("补充知识", 4, 3, "#F1F3F7"), ("行动条件", 7, 3, "#F1F3F7"), ("汇总", 10, 1, "#EAF0FF")]


def svg_text(x: float, y: float, text: str, size: float, *, fill: str = "#1F2937", anchor: str = "start", weight: int = 400) -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(text)}</text>'


def main() -> None:
    parser = MatrixParser()
    parser.feed(rendered_dom())
    if len(parser.rows) != 52:
        raise SystemExit(f"Expected 52 ecosystem-task rows; got {len(parser.rows)}.")

    category = ""
    category_left = 0
    parsed: list[dict[str, object]] = []
    for row_index, row in enumerate(parser.rows):
        if row and "catcol" in row[0]["class"]:
            category = row[0]["text"]
            category_left = int(row[0]["rowspan"])
            row = row[1:]
        task, stack, *cells = row
        parsed.append({"category": category, "task": task["text"], "stack": stack["text"], "cells": cells})
        category_left -= 1
        if category_left == 0:
            category = ""

    width, left, top, row_h, cell_w = 1160, 30, 124, 18, 74
    category_w, task_w, stack_w = 72, 176, 48
    matrix_x = left + category_w + task_w + stack_w
    height = top + row_h * len(parsed) + 76
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>text{font-family:"Noto Sans CJK SC","PingFang SC","Microsoft YaHei",Arial,sans-serif}.thin{stroke:#D8DEE9;stroke-width:.6}.sep{stroke:#C6CEDD;stroke-width:1.1}</style>',
        '<rect width="100%" height="100%" fill="#FFFFFF"/>',
        svg_text(left, 26, "图 2　26 个结果目标匹配任务的面向 AI 的知识可得性矩阵", 16, weight=700),
        svg_text(left, 47, "每项任务各有 CUDA 与 CANN 两个审计单元；①–⑦、⑨–⑩为 1–5 分，⑧为实际检索成本，⑪为三源噪声-OR 综合置信度。", 9.5, fill="#526174"),
    ]

    # Group header and column headers.
    for label, start, span, color in GROUPS:
        x = matrix_x + start * cell_w
        w = span * cell_w
        parts += [f'<rect x="{x}" y="{62}" width="{w}" height="20" rx="3" fill="{color}"/>', svg_text(x + w / 2, 76, label, 8.5, anchor="middle", weight=700, fill="#34435B")]
    parts += [
        f'<rect x="{left}" y="{62}" width="{category_w}" height="{top-62}" rx="3" fill="#F1F3F7"/>',
        f'<rect x="{left+category_w}" y="{62}" width="{task_w}" height="{top-62}" rx="3" fill="#F1F3F7"/>',
        f'<rect x="{left+category_w+task_w}" y="{62}" width="{stack_w}" height="{top-62}" rx="3" fill="#F1F3F7"/>',
        svg_text(left + category_w / 2, 104, "工作流", 8.5, anchor="middle", weight=700),
        svg_text(left + category_w + task_w / 2, 104, "结果目标", 8.5, anchor="middle", weight=700),
        svg_text(left + category_w + task_w + stack_w / 2, 104, "生态", 8.5, anchor="middle", weight=700),
    ]
    for index, (title, subtitle) in enumerate(METRICS):
        x = matrix_x + index * cell_w
        parts += [
            f'<rect x="{x+1}" y="{84}" width="{cell_w-2}" height="{top-84}" rx="3" fill="#FAFBFD"/>',
            svg_text(x + cell_w / 2, 102, title, 8, anchor="middle", weight=700, fill="#34435B"),
            svg_text(x + cell_w / 2, 115, subtitle, 6.5, anchor="middle", fill="#748197"),
        ]

    # Matrix body. Category labels span pairs of ecosystem rows.
    category_start = 0
    while category_start < len(parsed):
        name = str(parsed[category_start]["category"])
        end = category_start + 1
        while end < len(parsed) and parsed[end]["category"] == name:
            end += 1
        y = top + category_start * row_h
        h = (end - category_start) * row_h - 2
        parts += [
            f'<rect x="{left}" y="{y+1}" width="{category_w-3}" height="{h}" rx="3" fill="#E7EAF1"/>',
            svg_text(left + category_w / 2 - 2, y + h / 2 + 3, name, 7.4, anchor="middle", weight=700, fill="#34435B"),
        ]
        category_start = end

    for i, item in enumerate(parsed):
        y = top + i * row_h
        task = str(item["task"])
        stack = str(item["stack"])
        task_fill = "#F7F8FB" if i % 2 == 0 else "#FBFCFE"
        stack_fill = "#EEF5E2" if stack == "CUDA" else "#FBE8EC"
        stack_color = "#5C850B" if stack == "CUDA" else "#B32338"
        parts += [
            f'<rect x="{left+category_w}" y="{y+1}" width="{task_w-3}" height="{row_h-2}" rx="2" fill="{task_fill}"/>',
            svg_text(left+category_w+6, y+12.3, task if i % 2 == 0 else "", 7.4, weight=650, fill="#334155"),
            f'<rect x="{left+category_w+task_w}" y="{y+1}" width="{stack_w-3}" height="{row_h-2}" rx="2" fill="{stack_fill}"/>',
            svg_text(left+category_w+task_w+(stack_w-3)/2, y+12.3, stack, 7.3, anchor="middle", weight=700, fill=stack_color),
        ]
        for c, cell in enumerate(item["cells"]):
            classes = str(cell["class"]).split()
            key = next((name for name in PALETTE if name in classes), "v3")
            bg, fg = PALETTE[key]
            x = matrix_x + c * cell_w
            label = str(cell["text"])
            font = 7.2 if c != 7 else 6.0
            parts += [
                f'<rect x="{x+1.5}" y="{y+1}" width="{cell_w-3}" height="{row_h-2}" rx="2" fill="{bg}"/>',
                svg_text(x + cell_w/2, y + 12.3, label, font, anchor="middle", weight=700 if key in {"v1", "v2", "blk"} else 500, fill=fg),
            ]
        if i == len(parsed) - 1 or parsed[i + 1]["category"] != item["category"]:
            parts.append(f'<line x1="{left}" y1="{y+row_h+1}" x2="{matrix_x+len(METRICS)*cell_w}" y2="{y+row_h+1}" class="sep"/>')

    legend_y = top + row_h * len(parsed) + 26
    parts.append(svg_text(left, legend_y, "分值", 8.5, weight=700, fill="#526174"))
    for index, key in enumerate(("v5", "v4", "v3", "v2", "v1", "blk")):
        bg, fg = PALETTE[key]
        label = {"v5": "5", "v4": "4", "v3": "3", "v2": "2", "v1": "1", "blk": "受阻"}[key]
        x = left + 34 + index * 54
        parts += [f'<rect x="{x}" y="{legend_y-10}" width="34" height="14" rx="3" fill="{bg}"/>', svg_text(x+17, legend_y, label, 7.5, anchor="middle", weight=700, fill=fg)]
    parts += [
        svg_text(left + 375, legend_y, "颜色表示指标档位；“受阻”表示核心正文无法读取，不能等同于低分。", 8, fill="#526174"),
        svg_text(left, legend_y + 26, "资料来源：本研究 52 个审计单元的原始检索记录与可复算评分；交互版矩阵保留逐单元证据与来源细节。", 7.5, fill="#748197"),
        "</svg>",
    ]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(parts), encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
