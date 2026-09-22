"""Generate bilingual current-rule figures; historical matrices are never rescored.

Requires Matplotlib. SVG text stays editable; PDF and PNG are matching exports.
Full anchors and decision rules are in Appendix A, copied from frozen rules.md.
"""
from pathlib import Path
from textwrap import wrap
import argparse
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager, colors
import numpy as np
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'figures'
FONT = Path('/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
if FONT.exists():
    font_manager.fontManager.addfont(str(FONT))
INK = '#24313d'
BLUE = '#397ac0'
MUTED = '#536574'
M5_COLOR='#9869b9'; M6_COLOR='#6887c3'; M7_COLOR='#7e78c5'; M8_COLOR='#a17cba'; INDIGO='#239b8e'; SLATE='#61788d'
PALETTE={**{f'M{i}':BLUE for i in range(1,5)},'M5':M5_COLOR,'M6':M6_COLOR,'M7':M7_COLOR,'M8':M8_COLOR,'M9':INDIGO,'M10':INDIGO}

# Abbreviated visual anchors. Appendix A contains the full decision boundaries.
ROWS = {
'M1': ([ '预算内未发现', '第3次及之后\n查询首次发现', '第2次查询\n首次发现', '首查第2–5条', '首查第1条'],
       ['No relevant official hit within budget','First hit on query 3 or later','First hit on query 2','First query, position 2–5','First query, position 1']),
'M2': (['未取得可识别\n目标内容','仅标题、导航\n或元数据','明确摘要／摘录\n未取得直接正文','直接正文\n有截断／缺失证据','直接正文\n完整起止有据'],
       ['No identifiable target content','Title, navigation or metadata only','Explicit summary / excerpt; no direct body','Direct body with evidence of truncation / gaps','Direct body with verified complete boundaries']),
'M3': (['只有概述\n无相关细节','零散相关细节\n未成完整段落','已有完整段落\n关键内容仍缺','主流程与前提齐\n所需分支仍缺','原题所需解释、\n步骤、参数、约束齐'],
       ['Overview only; no relevant details','Isolated details; no complete passage','Complete passages; key task content missing','Main procedure and prerequisites; required branches incomplete','All required explanations, steps, parameters and constraints']),
'M4': (['无版本信息','有版本，但无选择依据，\n或官方说明冲突且\n无法消解','已明确部分适用关系，\n但仍缺少完成版本选择\n所需的对应关系','需自行合并官方约束，\n才能确定适用版本','官方已明确适用关系，\n直接查表或套用规则\n即可确定'],
       ['No version information','Versions without selection criteria, or unresolved official conflicts','Partial applicability; a necessary correspondence is missing','Combine official constraints to determine applicable versions','Explicit official applicability: direct lookup or rule application']),
'M5': (['相关独立来源\n0条','相关独立来源\n1–2条','相关独立来源\n3–4条','相关独立来源\n5条','相关独立来源\n至少6条'],
       ['0 relevant independent sources','1–2 relevant independent sources','3–4 relevant independent sources','5 relevant independent sources','At least 6 relevant independent sources']),
'M6': (['关键说法与可靠依据\n直接矛盾且未解决','未发现确证矛盾\n关键说法无核对依据','部分关键说法有据\n其余未核验','全部关键说法有据\n无未决矛盾\n缺少独立互证','全部关键说法有据\n独立来源互证\n无未决矛盾'],
       ['Unresolved key contradiction with reliable evidence','No confirmed conflict; key claims lack traceable basis','Some key claims supported; others unverified','All key claims supported; no conflict; no independent corroboration','All key claims supported and independently corroborated; no conflict']),
'M7': (['检索前无可核验\n正确知识或主张被否定','检索前只有正确概念\n无具体方法／解释','检索前有正确片段\n关键细节仍需查','检索前流程／解释完整\n参数或约束仍需补','检索前已准确覆盖\n原题全部所需知识'],
       ['No verifiable correct task knowledge, or refuted key claims','Correct concepts only; no concrete method / explanation','Correct fragments; key details need external material','Correct full procedure; task parameters / constraints incomplete','Accurately covers all required task knowledge before retrieval']),
'M8': (['C ≥ 9','C = 7–8','C = 5–6','C = 3–4','C = 1–2'],
       ['C ≥ 9','C = 7–8','C = 5–6','C = 3–4','C = 1–2']),
'M9': (['无原题所需版本','有版本但适用性无据\n或关键定版矛盾','部分所需组件有据\n其余未确定','所有所需组件\n均有据范围\n至少一项未定具体版','所有所需组件\n均有据具体版本\n无未决配套冲突'],
       ['Required versions absent','Versions lack supported applicability, or conflict with evidence','Some required components supported; others unresolved','Supported ranges for all components; at least one not specific','Supported specific versions for all components; no unresolved conflict']),
'M10': (['只有目标／示意\n无可执行方案','仅操作骨架\n关键操作无法确定','具体方案需补充\n或修正才能执行','完整指导，仅替换\n已标明且有说明的\n用户环境参数','指导与适用前提明确\n无需补写或修正\n可直接执行'],
        ['Goal / illustration only; no executable plan','Skeleton only; key operation indeterminate','Concrete plan requires additions or corrections','Complete guidance; only explained user-environment substitutions','Explicit guidance and prerequisites; no additions or corrections'])}


def names(lang):
    return {x[1].strip(): x[2].strip() for line in (ROOT/f'manuscript-{lang}-v0.2.md').read_text().splitlines() if line.startswith('| M') for x in [line.split('|')]}


def canvas(lang, height):
    plt.rcParams.update({'font.family': 'Arial Unicode MS' if lang == 'cn' else 'DejaVu Sans', 'svg.fonttype': 'none', 'pdf.fonttype': 42, 'font.size': 9, 'text.color': INK})
    fig = plt.figure(figsize=(10, height/100), facecolor='white')
    ax = fig.add_axes([0,0,1,1]); ax.set(xlim=(0,1000), ylim=(height,0)); ax.axis('off')
    return fig, ax


def label(ax, x, y, value, size=9, color=INK, ha='left', width=None):
    if width:
        value = '\n'.join('\n'.join(wrap(p,width,break_long_words=False,break_on_hyphens=False)) for p in value.split('\n'))
    return ax.text(x,y,value,fontsize=size,color=color,ha=ha,va='top',linespacing=1.45)


def save(fig, stem, lang):
    for ext in ('svg','pdf','png'):
        fig.savefig(OUT/f'{stem}-{lang}.{ext}', dpi=170)
    plt.close(fig)


def rubric(lang, group, ids):
    cn = lang == 'cn'; ns = names(lang)
    rh = 136 if not cn else 114
    height = 54 + rh*len(ids) + 76
    fig,ax=canvas(lang,height)
    label(ax,18,13,'指标 / 得分' if cn else 'Indicator / grade',9,color=MUTED)
    left=210; cw=154
    for j in range(5):label(ax,left+j*cw+cw/2,8,str(j+1),15,PALETTE[ids[0]],'center')
    for n,key in enumerate(ids):
        y=52+n*rh
        color=PALETTE[key]
        label(ax,18,y+5,key,13,color)
        label(ax,18,y+32,ns[key],9,color,width=25 if not cn else None)
        for j,s in enumerate(ROWS[key][0 if cn else 1]):
            x=left+j*cw
            ax.plot([x,x+cw-10],[y,y],color=np.array(colors.to_rgb(color))*(.2+.8*j/4)+(1-(.2+.8*j/4)),lw=2)
            label(ax,x,y+12,s,8.8 if cn else 8.1,width=None if cn else 22)
    y=height-67
    foot = {
      'official': ('M2：按独立文档最终状态等权平均；重试不重复计数；完整性未知保留4–5，不删除未知项。\nM3/M4：只看原题与实际取得的官方内容；无正文记受阻；版本多不扣分。', 'M2: equal weight per final document state; merge retries; unknown completeness stays 4–5, without dropping documents.\nM3/M4: assess acquired official material against the task; missing body is blocked; version count incurs no penalty.'),
      'support': ('M5：转载／镜像不作独立来源；M6：无第三方材料记N/A；M7：核查检索前答案，不用自评。\nM8：C=S+F；失败调用只计一次；C=0或异常中断不自动给高分。', 'M5: reposts/mirrors are not independent. M6: no third-party material is N/A. M7: inspect the prior answer, not confidence.\nM8: C=S+F; a failed call counts once. Zero calls or abnormal interruption do not automatically earn a high grade.'),
      'answers': ('M9：先固定原题需要定版的组件；无版本要求记N/A。\nM10：4分不能包含内容纠错；运行状态另记，未实际运行不是4/5分界。', 'M9: fix required components before assessment; no version requirement is N/A.\nM10: grade 4 excludes correcting content errors. Execution status is separate and does not distinguish grades 4 and 5.')}
    label(ax,18,y,foot[group][0 if cn else 1],8,color=MUTED)
    label(ax,18,height-24,'冻结规则：2026-09-21 · 完整判定见附录A · 五档为研究约定' if cn else 'Frozen rules: 21 September 2026 · Full decisions in Appendix A · Study-defined ordinal grades',7.5,color=MUTED)
    save(fig,'figure-scoring-'+group,lang)


def box(ax,x,y,w,h,title,body,cn):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0,rounding_size=8',linewidth=.8,edgecolor='#b2c4d2',facecolor='#f0f3f6'))
    label(ax,x+14,y+12,title,10,SLATE)
    label(ax,x+14,y+37,body,9 if cn else 8.5)


def arrow(ax,a,b):
    ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','lw':1.15,'color':MUTED})


def confidence(lang):
    # Restore the original compact label + horizontal strip composition.
    # The original slate palette is continuous: no grade bins or cutoffs.
    cn=lang=='cn';fig,ax=canvas(lang,42)
    fig.set_size_inches(6.5,.42)
    ax.set(xlim=(0,650),ylim=(42,0))
    label(ax,8,7,'M11',8.5,SLATE)
    label(ax,39,7,'综合置信度' if cn else 'Composite\nconfidence',7.5 if cn else 7,SLATE)
    cmap=colors.LinearSegmentedColormap.from_list('confidence_continuous',['#f0f3f6','#d6e0e8','#b2c4d2','#8ba3b7','#61788d'])
    ax.imshow(np.linspace(0,1,1024)[None,:],extent=(150,638,22,3),aspect='auto',cmap=cmap,vmin=0,vmax=1,interpolation='bilinear')
    for value in [0,20,40,60,80,100]:
        label(ax,150+value/100*488,26,str(value),7,SLATE,'center')
    save(fig,'figure-scoring-confidence',lang)


def support(lang):
    cn=lang=='cn'; ns=names(lang)
    fig,ax=canvas(lang,590)
    # M6 and M7 share the five-grade strip layout with distinct colors.
    for key,color,top in [('M6',M6_COLOR,12),('M7',M7_COLOR,172)]:
        label(ax,18,top,key,13,color)
        label(ax,18,top+30,ns[key],9,color,width=24 if not cn else None)
        for j,t in enumerate(ROWS[key][0 if cn else 1]):
            x=210+j*154;strength=.2+.8*j/4
            label(ax,x+72,top-3,str(j+1),12,color,'center')
            ax.plot([x,x+144],[top+26,top+26],lw=2,color=np.array(colors.to_rgb(color))*strength+(1-strength))
            label(ax,x,top+39,t,8.5 if cn else 8,width=None if cn else 22)
    # Restore the two step plots with the current count thresholds.
    for pos,key,x,y,color in [([.07,.16,.385,.25],'M5',list(range(8)),[1,2,2,3,3,4,5,5],M5_COLOR),([.59,.16,.385,.25],'M8',list(range(1,12)),[5,5,4,4,3,3,2,2,1,1,1],M8_COLOR)]:
        a=fig.add_axes(pos);a.step(x,y,where='post',color=color,lw=1.3)
        dense=np.linspace(x[0],x[-1],1601);heights=np.array(y)[np.clip(np.searchsorted(x,dense,side='right')-1,0,len(y)-1)]
        for lo,hi in zip(np.linspace(1,5,45)[:-1],np.linspace(1,5,45)[1:]):
            a.fill_between(dense,lo,np.minimum(heights,hi),where=heights>lo,step='post',color=(*colors.to_rgb(color),.025+.34*(hi-1)/4),linewidth=0)
        a.plot(x,y,'o',ms=3,color=color)
        a.set(ylim=(.8,5.2),xlim=(x[0],x[-1]),yticks=[1,2,3,4,5],xticks=[0,1,3,5,6,7] if key=='M5' else [1,3,5,7,9,11])
        a.tick_params(labelsize=8,length=2,pad=2,colors=color);a.grid(axis='y',color='#e5eaf0',lw=.5)
        a.spines[['top','right']].set_visible(False)
        for sp in ['left','bottom']:a.spines[sp].set_color('#d3dce5')
        a.set_xlabel(('去重独立来源数 n' if cn else 'Distinct independent sources n') if key=='M5' else ('实际调用数 C = S + F' if cn else 'Actual calls C = S + F'),fontsize=9,labelpad=4)
        label(ax,pos[0]*1000,320,key+'  '+ns[key],10,color)
    label(ax,18,537,'M5：来源去重计数。M6：依据关键说法核验。M7：核查检索前答案。M8：按实际调用计数。' if cn else 'M5: deduplicated sources. M6: claim verification. M7: pre-retrieval answer. M8: actual calls.',8,MUTED)
    label(ax,18,566,'冻结规则：2026-09-21 · 完整判定见附录A · 五档为研究约定' if cn else 'Frozen rules: 21 September 2026 · Full decisions in Appendix A · Study-defined ordinal grades',7.5,MUTED)
    save(fig,'figure-scoring-support',lang)


def main():
    args=argparse.ArgumentParser();args.add_argument('--official-only',action='store_true');opt=args.parse_args()
    for lang in ('cn','en'):
        rubric(lang,'official',['M1','M2','M3','M4'])
        if not opt.official_only:
            support(lang)
            rubric(lang,'answers',['M9','M10'])
            confidence(lang)


if __name__=='__main__':
    main()
