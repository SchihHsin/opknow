#!/bin/sh
# 20 号资料「抽取 → 出图 → 生成 Markdown」一键复现。
# 依赖：npm i d3 jsdom（本机在 /Users/hsin/.workbuddy/binaries/node/workspace，
#      脚本自己会去那里 require，可用 NODE_WS 环境变量改）。
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
PY=${PY:-/Users/hsin/.workbuddy/binaries/python/versions/3.13.12/bin/python3}

echo "① 抽取数据层 → $HERE/j20.json"
node "$HERE/extract20.mjs"

echo "② 用原页 d3 代码出图 → $(cd "$HERE/.." && pwd)/figs/"
node "$HERE/render20.mjs"

echo "③ 生成 Markdown → $(cd "$HERE/.." && pwd)/20_开发者与Agent协作分析.md"
"$PY" "$HERE/gen20.py"

echo "完成。"
