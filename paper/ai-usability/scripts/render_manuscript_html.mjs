#!/usr/bin/env node
/** Render the editable Markdown manuscript into its standalone reading page. */
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { marked } = require('marked');

const here = path.dirname(new URL(import.meta.url).pathname);
const paperDir = path.resolve(here, '..');
const source = path.join(paperDir, 'manuscript-cn-v0.1.md');
const output = path.join(paperDir, 'manuscript-cn-v0.1.html');
let markdown = fs.readFileSync(source, 'utf8');
markdown = markdown.replace(/^# .*\n+> 英文投稿题目：.*\n*/u, '');

const content = marked.parse(markdown, { gfm: true, breaks: false });
const css = `
:root{--ink:#1e2630;--muted:#67737f;--line:#dfe5e9;--paper:#fff;--bg:#f2f5f6;--accent:#0e6b61}
*{box-sizing:border-box}html{background:var(--bg)}body{margin:0;color:var(--ink);font-family:"Noto Serif CJK SC","Songti SC",STSong,serif;font-size:17px;line-height:1.88}.mast{background:#173e3a;color:#fff;padding:38px 24px 32px;border-bottom:5px solid #c3a250}.mast-inner,article{max-width:920px;margin:0 auto}.mast .kicker{font:600 12px/1.3 -apple-system,BlinkMacSystemFont,"Noto Sans SC",sans-serif;letter-spacing:.15em;color:#cce9e4}.mast h1{margin:12px 0 0;font-size:30px;line-height:1.35;font-weight:700}.mast p{margin:8px 0 0;color:#d8e9e6;font:14px/1.7 -apple-system,BlinkMacSystemFont,"Noto Sans SC",sans-serif}article{background:var(--paper);padding:50px 72px 80px;box-shadow:0 8px 34px rgba(26,54,51,.1);min-height:100vh}h1{font-size:30px;line-height:1.35;margin:0 0 14px}h2{font-size:24px;line-height:1.45;margin:58px 0 20px;padding-top:8px;border-top:1px solid var(--line)}h3{font-size:19px;line-height:1.55;margin:34px 0 12px;color:#1d5952}p{margin:0 0 16px}strong{font-weight:700;color:#102e2b}blockquote{margin:18px 0 24px;padding:13px 18px;border-left:4px solid #c3a250;background:#fbf9f3;color:#46534f;font-family:"Noto Sans SC",sans-serif;font-size:15px}ul,ol{padding-left:1.45em;margin:5px 0 18px}li{margin:4px 0}code{font-family:"SFMono-Regular",Consolas,monospace;font-size:.82em;color:#9b3e27;background:#f6f2ef;padding:1px 4px;border-radius:3px;word-break:break-word}pre{padding:18px;background:#152725;color:#e3f2ee;border-radius:8px;overflow:auto;font:13px/1.65 "SFMono-Regular",Consolas,monospace}pre code{background:transparent;color:inherit;padding:0}.tablewrap{overflow-x:auto;margin:20px 0 25px;border:1px solid var(--line);border-radius:7px}table{width:100%;border-collapse:collapse;font-family:"Noto Sans SC",-apple-system,sans-serif;font-size:13px;line-height:1.65}th{background:#eaf2f0;color:#1e4b45;text-align:left;font-weight:700}th,td{padding:9px 11px;border-bottom:1px solid var(--line);vertical-align:top}tr:last-child td{border-bottom:0}tbody tr:nth-child(even){background:#fbfcfc}hr{border:0;border-top:1px solid var(--line);margin:38px 0}a{color:#08776b;text-decoration-color:#9bc9c1;text-underline-offset:3px}p:has(>img[src$=".svg"]){margin:26px -38px 8px}p:has(>img[src$=".svg"]) img{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:7px}p:has(>img[src$=".svg"])+p{margin:9px -34px 26px;color:#526174;font:13px/1.65 -apple-system,BlinkMacSystemFont,"Noto Sans SC",sans-serif}@media print{html,body{background:#fff}body{font-size:11pt}.mast{background:#fff;color:#111;border-bottom:1px solid #111;padding:0 0 12px}.mast .kicker,.mast p{color:#555}.mast h1{color:#111}article{box-shadow:none;padding:24px 0}h2{page-break-after:avoid}table{font-size:8.5pt}.tablewrap{break-inside:avoid}p:has(>img[src$=".svg"]){break-before:page;margin:0}p:has(>img[src$=".svg"])+p{margin:9px 0 26px}}@media(max-width:700px){body{font-size:16px}.mast{padding:26px 20px}.mast h1{font-size:24px}article{padding:34px 22px 60px}h1{font-size:26px}h2{font-size:22px}p:has(>img[src$=".svg"]),p:has(>img[src$=".svg"])+p{margin-left:0;margin-right:0}}`;

const page = `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Can AI Find What Developers Need?</title><style>${css}</style></head><body><header class="mast"><div class="mast-inner"><div class="kicker">CHINESE MANUSCRIPT · V0.1 · 2026-09-08</div><h1>AI 能找到开发者所需的吗？</h1><p><em>Can AI Find What Developers Need? Defining and Measuring Knowledge Availability for AI in Developer Ecosystems</em></p></div></header><article>${content}</article></body></html>`;
fs.writeFileSync(output, page, 'utf8');
console.log(output);
