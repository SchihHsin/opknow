#!/usr/bin/env python3
"""Build offline English/Chinese reading HTML using the real citation database."""
from pathlib import Path
import re
import subprocess
import shutil
import html

ROOT=Path(__file__).resolve().parents[1]
PANDOC=shutil.which('pandoc') or str(ROOT/'submission/.tools/pandoc')
CSS='''
:root{color-scheme:light;--ink:#24313d;--muted:#536574;--line:#dce3e7;--accent:#176253}
*{box-sizing:border-box}html{background:#f0f3f5}body{max-width:1060px;margin:36px auto 80px;padding:48px 76px 64px;background:white;color:var(--ink);font:17px/1.8 Georgia,"Noto Serif CJK SC","Songti SC",serif;box-shadow:0 10px 40px #152b3b0d}
.edition{font:13px/1.5 system-ui,sans-serif;letter-spacing:.04em;color:var(--muted);border-bottom:1px solid var(--line);padding-bottom:16px;margin-bottom:30px}h1{font-size:30px;line-height:1.35;letter-spacing:-.015em;margin:0 0 12px}.authors{font:15px/1.6 system-ui,sans-serif;color:var(--muted);margin:0;letter-spacing:.02em}.authors sup{font:700 11px/1 system-ui;vertical-align:super}.affiliation{font:13px/1.6 system-ui,sans-serif;color:var(--muted);margin:3px 0 30px}h2{font-size:24px;line-height:1.5;margin:46px 0 18px;padding-top:12px;border-top:1px solid var(--line)}h3{font-size:19px;line-height:1.6;margin:28px 0 12px;color:var(--accent)}p{margin:0 0 17px}a{color:#176d70;text-decoration-thickness:1px;text-underline-offset:3px}strong{color:#173c36}figure{margin:28px 0}figure img{display:block;width:100%;height:auto}figcaption{font:13px/1.6 system-ui,sans-serif;color:var(--muted);margin-top:12px}table{width:100%;border-collapse:collapse;margin:24px 0;font:14px/1.65 system-ui,sans-serif;table-layout:fixed}th,td{padding:10px 12px;border:1px solid var(--line);vertical-align:top;overflow-wrap:anywhere}th{background:#eef4f2;text-align:left}tbody tr:nth-child(even){background:#fafcfc}code{font:85%/1.6 ui-monospace,monospace;background:#f2f4f6;padding:1px 3px}pre{white-space:pre-wrap;background:#f3f5f7;padding:18px}math[display="block"]{font-size:100%;margin:22px 0;overflow-x:auto}.references{font:14px/1.65 system-ui,sans-serif}.csl-entry{margin-bottom:14px}.csl-left-margin{float:left;min-width:28px}.csl-right-inline{margin-left:32px}
body{counter-reset:fig}figure{counter-increment:fig}figcaption::before{content:"Figure " counter(fig) ". ";font-weight:bold}:lang(zh-CN) figcaption::before{content:"图 " counter(fig) "　"}caption{caption-side:top;text-align:left;color:var(--muted);font-size:13px;margin-bottom:8px}
@page{size:A4;margin:18mm 17mm 18mm;@bottom-center{content:counter(page);font:8pt Arial;color:#536574}} @media print{html{background:white}body{margin:0;padding:0;box-shadow:none;max-width:none;font-size:10.5pt;line-height:1.7}h1{font-size:21pt}h2{font-size:15pt;margin-top:25pt;break-after:avoid}h3{font-size:12pt;break-after:avoid}p{orphans:3;widows:3}table{font-size:8.3pt;line-height:1.55}th,td{padding:6pt}tr{break-inside:avoid}thead{display:table-header-group}figure{break-inside:avoid}figure img{max-height:220mm;object-fit:contain}figcaption{font-size:8.5pt}.edition{font-size:8pt}.authors,.affiliation{display:none}nav{display:none}a{text-decoration:none;color:inherit}.references{font-size:8.5pt}.csl-entry{break-inside:avoid}math[display="block"]{font-size:9pt}}
@media(max-width:700px){body{margin:0;padding:26px 20px;box-shadow:none}h1{font-size:25px}table{font-size:12px}th,td{padding:7px}}
'''

def main():
    for lang in ['en','cn']:
        source=ROOT/f'manuscript-{lang}-v0.2.md'
        text=source.read_text()
        cmd=[PANDOC,str(source),'--from=markdown+tex_math_dollars+implicit_figures','--to=html5','--citeproc','--bibliography',str(ROOT/'references.bib'),'--mathml','--standalone','--metadata',f'lang={"en-US" if lang=="en" else "zh-CN"}','--metadata','pagetitle=Knowledge Availability for AI']
        csl=ROOT/'submission/acm-sig-proceedings.csl'
        if csl.exists():cmd+=['--csl',str(csl)]
        result=subprocess.run(cmd,capture_output=True,text=True,check=True)
        page=result.stdout
        # Remove the stock style element and the indentation that precedes it,
        # then inject the shared reading-page stylesheet below.
        page=re.sub(r'\s*<style>.*?</style>','',page,flags=re.S)
        page=page.replace('</head>',f'<style>{CSS}</style></head>')
        label='ENGLISH MANUSCRIPT · V0.2 · 11 SEPTEMBER 2026' if lang=='en' else '中文对照阅读版 · V0.2 · 2026-09-11'
        page=page.replace('<body>',f'<body><div class="edition">{label}</div>')
        authors='<div class="authors">时昕昱　·　闫浩<sup>*</sup>　·　张敬文　·　郦旻硕</div><div class="affiliation">Huawei Technologies (China)　·　* Corresponding author</div>'
        page=re.sub(r'(<h1\b[^>]*>.*?</h1>)',r'\1'+authors,page,count=1,flags=re.S)
        page=page.replace('<div id="refs"',f'<h2>{"References" if lang=="en" else "参考文献"}</h2>\n<div id="refs"')
        # Long citation URLs are wrapped by CSS; sources remain local and offline.
        output=source.with_suffix('.html');output.write_text(page)
        print(output)

if __name__=='__main__':main()
