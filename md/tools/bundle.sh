#!/bin/sh
# 把资料包的 4 份正文按序拼成一个文件，便于一次性投喂给 AI。
# 用法：sh md/tools/bundle.sh
set -e
cd "$(dirname "$0")/.."          # -> md/
OUT=00_全集.md

FILES="17_任务评分对照矩阵.md 18_指标定义与计算方法.md 19_发现与体验综合分析.md 20_开发者与Agent协作分析.md"

{
  echo '# opknow 研究资料包 · 全集'
  echo
  echo '> 本文件由 `md/tools/bundle.sh` 拼接生成，请勿手工编辑。'
  echo '> 顺序：17 任务评分对照矩阵 → 18 指标定义与计算方法 → 19 发现与体验综合分析 → 20 开发者与 Agent 协作分析。'
  echo '> 四份单独的文件都在 `md/` 下；20 引用的 5 张 SVG 在 `md/figs/`。'
  echo '> 注意：SVG 对 AI 只是坐标碎片，读不出内容——20 里图的意思请读同节的 Mermaid 代码块与明细表。'
  for f in $FILES; do
    echo
    echo '---'
    echo
    printf '<!-- ==================== %s ==================== -->\n' "$f"
    echo
    cat "$f"
  done
} > "$OUT"

printf '写出 %s  %s 字节  %s 行\n' "$OUT" "$(wc -c < "$OUT" | tr -d ' ')" "$(wc -l < "$OUT" | tr -d ' ')"
