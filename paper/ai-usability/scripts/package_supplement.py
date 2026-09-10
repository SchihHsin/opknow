#!/usr/bin/env python3
"""Package only the anonymous data, protocol, and their portable computation."""
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
README='''# Anonymous supplement / 匿名补充材料
The v0.3 application links 52 task-side records to 350 selected external-tool
call/return pairs. Read data/trace-v0.3/README.md for selection, scope and provenance.
The original numerical files and their manifest remain frozen.
The old worked A form and original protocol are v0.2 artifacts; the applied
v0.3 ledger provides the current evidence links.
- protocol-cn-en-v0.3.md: bilingual protocol
- data/trace-v0.3/: selected returns, task attempts, application ledger and hashes
- scripts/verify_trace_application.py: offline integrity and coverage checks
- scripts/build_paper_analysis.py: historical arithmetic
- figures/v0.3/: six bilingual design illustrations

Run both scripts with Python 3. These checks verify integrity and internal
consistency; they do not establish independent coding agreement or task success.
No new website experiments were run. Whole private conversations and reasoning
are excluded. Returned text is tool-delivered material, not raw HTTP.

中文：本包包含52任务侧记录、350条选取的工具调用—返回对及其关联。
历史数值保持冻结；新增材料的范围、来源和解释见 trace-v0.3/README.md。
检查脚本验证文件完整性和内部一致性，不代表独立编码或运行成功验证。
'''

def main():
    files=[ROOT/'protocol-cn-en-v0.3.md',ROOT/'record-template-v0.3.json',ROOT/'scripts/build_paper_analysis.py',ROOT/'scripts/verify_trace_application.py']
    files += [p for p in (ROOT/'data').rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc']
    design_stems = ['figure-6-compatibility-design', 'figure-7-diagnostic-content-design',
                    'figure-8-readable-export-design', 'figure-9-acquisition-design',
                    'figure-10-environment-design', 'figure-11-verification-design']
    files += [ROOT/'figures/v0.3'/f'{stem}-{lang}.svg' for stem in design_stems for lang in ['cn','en']]
    for p in files:
        if p.suffix in ['.md','.json','.py','.csv'] and '/Users/' in p.read_text():
            raise ValueError(f'Local account path in supplement: {p.name}')
    out=ROOT/'submission/knowledge-availability-ai-supplement-v0.3.zip'
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('README.md',README)
        for p in sorted(files):z.write(p,p.relative_to(ROOT).as_posix())
    print(out)
    print(len(files)+1,'files')

if __name__=='__main__':main()
