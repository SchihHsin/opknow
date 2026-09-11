#!/usr/bin/env python3
"""Package only the anonymous data, protocol, and their portable computation."""
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
README='''# Supplement: Knowledge Availability for AI

This anonymous supplement accompanies the methodological paper. It contains the
case application, including task data, source evidence, and calculation materials.

- `data/`: 26 tasks / 52 frozen task-side records, source-provenance notes,
  historical scoring code, known corrections, and descriptive outputs.
- `data/supplementary-analysis-notes-cn-en.md`: bilingual composite calculation,
  sensitivity, discrepancy, and improvement-scenario notes.
- `protocol-cn-en.md`: the reusable protocol, in English and Chinese.
- `record-template.json`: a blank future recording form with item schemas.
- `data/worked-recording-example-a-cann.json`: a filled task example that
  links requirements, events, sources, saved evidence, and indicator codes.
- `scripts/build_paper_analysis.py`: portable offline arithmetic reproduction.
- `data/m2_scoring.json`: published M2 anchors and affected-record checks.
- `data/generated/current_scores.json`: scores used in the current paper.
- `data/design-illustrations-cn-en.md` and the Figure 10-15 SVGs in `figures/`:
  design provenance notes and editable bilingual illustrations from the paper.

Run with Python 3, without external dependencies:

    python3 scripts/build_paper_analysis.py

The primary comparison excludes task G's ROCm/HIP migration analogy and contains
25 pairs. The original records are retained. H.cuda's vendor-blog ownership is
flagged in the audit view; A.cann's failure-count boundary remains unresolved.
Descriptive access profiles treat static and server-rendered returns alike.
The matrix and composite use robots=1, spa=2, partial=3, ssr=4, static=5.
Original scores are retained for provenance. Scores are not calibrated probabilities.

The English task summaries translate the retained Chinese questions. The process
log is preserved in its original language. Complete conversations and hardware-execution evidence are not included in this package. No independent
human coding or hardware-execution validation is claimed.

## 中文说明

本补充材料保留26任务52单元，主比较排除G的ROCm/HIP迁移类比后为25对。
包含冻结数据、历史评分、来源说明、归类修订和未决计数、可复用协议、带单条字段结构的空白记录表及一份填写示例。
脚本只做已有记录的离线计算，不重新联网检索。综合置信度不是答案正确概率；双语补充分析说明汇集计算口径、敏感性和情境分析的解释。
问题的英文摘要是编辑性翻译；过程日志保留原中文。填写示例提供来源URL与获取结果；补充包不包含完整会话，也不声称进行了独立人工编码或硬件执行验证。
'''

def main():
    files=[ROOT/'protocol-cn-en.md',ROOT/'record-template.json',ROOT/'scripts/build_paper_analysis.py']
    files += [p for p in (ROOT/'data').rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc']
    design_stems = ['figure-6-compatibility-design', 'figure-7-diagnostic-content-design',
                    'figure-8-readable-export-design', 'figure-9-acquisition-design',
                    'figure-10-environment-design', 'figure-11-verification-design']
    files += [ROOT/'figures'/f'{stem}-{lang}.svg' for stem in design_stems for lang in ['cn','en']]
    for p in files:
        if p.suffix in ['.md','.json','.py','.csv'] and '/Users/' in p.read_text():
            raise ValueError(f'Local account path in supplement: {p.name}')
    out=ROOT/'submission/knowledge-availability-ai-supplement-v0.2.zip'
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('README.md',README)
        for p in sorted(files):z.write(p,p.relative_to(ROOT).as_posix())
    print(out)
    print(len(files)+1,'files')

if __name__=='__main__':main()
