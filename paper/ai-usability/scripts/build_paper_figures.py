#!/usr/bin/env python3
"""Build editable SVG figures and adjacent English vector PDFs from frozen data.

Uses ReportLab for the PDF drawing surface. No website acquisition is performed.
Run with a Python environment containing reportlab.
"""
from pathlib import Path
import json
import math
from html import escape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"


class Drawing:
    def __init__(self, name, width, height, language, description):
        self.width, self.height = width, height
        self.path = OUT / (name + '-' + language)
        self.svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>{escape(description)}</title><desc>{escape(description)}</desc>', '<rect width="100%" height="100%" fill="white"/>']
        self.pdf = None
        if language == 'en':
            self.pdf = canvas.Canvas(str(self.path.with_suffix('.pdf')), pagesize=(width*.5, height*.5), invariant=1)
            self.pdf.setTitle(description)
            self.pdf.setAuthor('')
            self.pdf.scale(.5, .5)

    def rect(self, x, y, w, h, fill='#ffffff', stroke=None, r=6):
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke or "none"}"/>')
        if self.pdf:
            self.pdf.setFillColor(HexColor(fill))
            if stroke:self.pdf.setStrokeColor(HexColor(stroke))
            self.pdf.roundRect(x, self.height-y-h, w, h, r, fill=1, stroke=int(bool(stroke)))

    def text(self, x, y, value, size=18, fill='#243447', bold=False, anchor='start'):
        self.svg.append(f'<text x="{x}" y="{y}" font-family="Arial, PingFang SC, Noto Sans CJK SC, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{anchor}" fill="{fill}">{escape(str(value))}</text>')
        if self.pdf:
            self.pdf.setFillColor(HexColor(fill))
            self.pdf.setFont('Helvetica-Bold' if bold else 'Helvetica',size)
            method={'start':self.pdf.drawString,'middle':self.pdf.drawCentredString,'end':self.pdf.drawRightString}[anchor]
            method(x,self.height-y,str(value))

    def line(self, points, color='#6c7b89', dash=False, arrow=False, width=1.6):
        attrs=' stroke-dasharray="6 4"' if dash else ''
        self.svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in points)+f'" fill="none" stroke="{color}" stroke-width="{width}"{attrs}/>')
        if self.pdf:
            self.pdf.setStrokeColor(HexColor(color));self.pdf.setLineWidth(width)
            self.pdf.setDash([6,4] if dash else [])
            p=self.pdf.beginPath();p.moveTo(points[0][0],self.height-points[0][1])
            for x,y in points[1:]:p.lineTo(x,self.height-y)
            self.pdf.drawPath(p)
            self.pdf.setDash([])
        if arrow:
            (x0,y0),(x,y)=points[-2:];a=math.atan2(y-y0,x-x0)
            p=[(x-9*math.cos(a-.45),y-9*math.sin(a-.45)),(x,y),(x-9*math.cos(a+.45),y-9*math.sin(a+.45))]
            self.line(p,color,width=width)

    def save(self):
        self.path.with_suffix('.svg').write_text('\n'.join(self.svg)+ '\n</svg>\n',encoding='utf-8')
        if self.pdf:self.pdf.showPage();self.pdf.save()


def framework(lang):
    en=lang=='en'
    d=Drawing('figure-1-framework',1000,760,lang,'Observable Agent acquisition loop and measurement locations' if en else '可观察的 Agent 知识获取循环与测量位置')
    text=lambda zh,en_text: en_text if en else zh
    d.rect(330,12,340,48,'#edf2f8','#b6c5d5')
    d.text(500,34,text('任务与记录上下文','Task and recorded context'),22,bold=True,anchor='middle')
    d.text(500,51,text('目标、初始材料、Agent／工具、时间','Goal, artifacts, agent/tools, time'),14,anchor='middle')
    d.rect(350,88,300,42,'#f1ebf8','#cbbce5')
    d.text(500,114,text('① 解析需求并拆解子目标','1. Interpret needs and decompose subgoals'),18,bold=True,anchor='middle')
    d.rect(350,155,300,42,'#fff6df','#e0bd67')
    d.text(500,181,text('② 是否需要外部证据？','2. Need external evidence?'),18,bold=True,anchor='middle')
    d.rect(70,240,270,64,'#eaf1f8','#b4cadd')
    d.text(205,268,'web_search',20,bold=True,anchor='middle')
    d.text(205,290,text('发现官方／社区候选来源','Discover official / community candidates'),14,anchor='middle')
    d.text(205,307,text('M1 发现性 · M5 替代覆盖','M1 discovery · M5 alternative coverage'),12,fill='#426d8e',anchor='middle')
    d.rect(70,328,270,50,'#eaf1f8','#b4cadd')
    d.text(205,351,text('③ 选择 URL','3. Select URLs'),17,bold=True,anchor='middle')
    d.text(205,369,text('记录发布者、来源角色与查询','Record publisher, source role, and query'),12,anchor='middle')
    d.rect(70,402,270,64,'#eaf1f8','#b4cadd')
    d.text(205,430,'web_fetch',20,bold=True,anchor='middle')
    d.text(205,451,text('取得正文、片段或失败状态','Obtain body, fragment, or failure state'),14,anchor='middle')
    d.text(205,468,text('M2 访问 · M3 充分性','M2 access · M3 adequacy'),12,fill='#426d8e',anchor='middle')
    d.rect(665,278,270,72,'#f3edf9','#cbbce5')
    d.text(800,306,text('模型先验（M7）','Model prior (M7)'),18,bold=True,anchor='middle')
    d.text(800,327,text('单独登记为估计或测试；','Register separately as estimate or test;'),13,anchor='middle')
    d.text(800,344,text('不等同于已取得来源','not retrieved evidence'),13,anchor='middle')
    d.rect(365,493,270,50,'#f5f6f7','#ccd3da')
    d.text(500,519,text('④ 汇总证据台账','4. Integrate the evidence ledger'),17,bold=True,anchor='middle')
    d.text(500,536,text('查询、URL、返回内容、成本与缺口（M8）','Queries, URLs, returns, effort, gaps (M8)'),12,anchor='middle')
    d.rect(365,568,270,52,'#fff6df','#e0bd67')
    d.text(500,594,text('⑤ 评估充分性与版本适用性','5. Assess adequacy and version applicability'),17,bold=True,anchor='middle')
    d.text(500,612,text('M4、M9、M10','M4, M9, M10'),12,anchor='middle')
    d.rect(675,565,245,56,'#fff4e8','#dfaa6e')
    d.text(797,589,text('调整查询并重试','Refine query and retry'),17,bold=True,anchor='middle')
    d.text(797,608,text('仍有可检索的证据空间','When evidence remains searchable'),12,anchor='middle')
    d.rect(300,680,400,58,'#e9f3ee','#8fb9a3')
    d.text(500,706,text('⑥ 作答：下一步行动或明确证据缺口','6. Answer: next action or explicit evidence gap'),18,bold=True,anchor='middle')
    d.text(500,725,text('M11 为可选启发式汇总，不替代剖面','M11 is optional heuristic summary, not a substitute for the profile'),12,anchor='middle')
    d.line([(500,60),(500,88)],arrow=True)
    d.line([(500,130),(500,155)],arrow=True)
    d.line([(430,197),(205,197),(205,240)],arrow=True)
    d.text(296,218,text('是','yes'),13,fill='#26735f',anchor='middle')
    d.line([(205,304),(205,328)],arrow=True)
    d.line([(205,378),(205,402)],arrow=True)
    d.line([(340,434),(365,493)],arrow=True)
    d.line([(650,176),(800,176),(800,278)],arrow=True,dash=True)
    d.text(804,200,text('否：先验分支','no: prior branch'),12,fill='#7252a1')
    d.line([(800,350),(800,470),(635,470),(635,518)],arrow=True,dash=True)
    d.line([(500,543),(500,568)],arrow=True)
    d.line([(500,620),(500,680)],arrow=True)
    d.text(520,653,text('证据充分或边界已说明','sufficient evidence or explicit boundary'),12,fill='#26735f')
    d.line([(635,594),(675,594)],arrow=True)
    d.text(654,582,text('不足','insufficient'),12,fill='#aa6d18',anchor='middle')
    d.line([(797,565),(797,218),(340,218)],arrow=True,dash=True)
    d.save()


SHORT=['Model conversion','Profiling','Library selection','Custom operator','Error-code diagnosis','Distributed training','Migration analogy','Quantization','Version compatibility','Installation','Container setup','Operator accuracy','Dynamic shapes / tiling','Operator fusion','Framework integration','Mixed precision','Memory / OOM','Training convergence','Inference serving','Dynamic inference','Memory / occupancy','Compute-transfer overlap','Multi-device communication','Memory-error diagnosis','Chip migration','Programming concepts']
SHORT_CN=['模型转换／导出','性能定位','算子库选型','自定义算子','错误码排查','分布式训练','迁移类比','量化','版本配套','安装与环境','容器环境','算子精度','动态形状／Tiling','算子融合','注册与框架集成','混合精度','显存／OOM','训练精度与收敛','推理部署','动态推理','访存与利用率','计算与传输重叠','多卡通信','内存越界','跨芯片迁移','编程概念对照']


GROUPS=[
    ('environment_installation','Environment and installation','环境与安装'),
    ('operator_development','Operator development','算子开发'),
    ('training','Training','训练'),
    ('inference_deployment','Inference and deployment','推理与部署'),
    ('performance_optimization','Performance and optimization','性能与优化'),
    ('debugging','Debugging','调试'),
    ('migration','Migration','迁移'),
]


def ordered_tasks(tasks):
    by_group={group:[] for group,_,_ in GROUPS}
    analogy=None
    for task in tasks:
        if task['task_id']=='G':
            analogy=task
        else:
            by_group[task['workflow_group']].append(task)
    rows=[]
    for group,en_name,cn_name in GROUPS:
        entries=sorted(by_group[group],key=lambda x:x['task_id'])
        if entries:
            rows.append(('group',en_name,cn_name))
            rows.extend(('task',task) for task in entries)
    rows.append(('group','Migration analogy (not in CANN/CUDA summaries)','迁移类比（不计入 CANN/CUDA 汇总）'))
    rows.append(('task',analogy))
    return rows


PALETTE={1:'#f4c7c3',2:'#f9dec3',3:'#fbebc9',4:'#e4efe9',5:'#d0e4df'}


def score_value(scores, metric):
    if metric==11:
        return scores['overall']
    return scores['scores'][metric-1]


def metric_color(value, metric):
    if value in (None,'受阻'):
        return '#f3c9c6'
    if metric==11:
        if value>=.80:return '#d0e4df'
        if value>=.65:return '#e4efe9'
        if value>=.50:return '#fbebc9'
        return '#f4c7c3'
    return PALETTE.get(value,'#e4e7ec')


def metric_label(metric,lang):
    labels={
        1:('M1 Find','M1 发现'), 2:('M2 Fetch','M2 获取'),
        3:('M3 Adequacy','M3 充分性'), 4:('M4 Version','M4 版本'),
        5:('M5 Alternatives','M5 替代来源'), 6:('M6 Credibility','M6 可信度'),
        7:('M7 Prior*','M7 先验*'), 8:('M8 Effort','M8 成本'),
        9:('M9 Pinning','M9 版本锁定'), 10:('M10 Steps','M10 步骤完整'),
        11:('M11 Index†','M11 指数†'),
    }
    return labels[metric][0 if lang=='en' else 1]


def full_matrix_panel(lang,panel,metrics):
    en=lang=='en'
    tasks=json.loads((ROOT/'data/tasks.json').read_text())
    scores=json.loads((ROOT/'data/legacy_scores_original.json').read_text())
    d=Drawing(f'figure-2-full-matrix-{panel}',1100,920,lang,'Full eleven-indicator archival matrix' if en else '完整十一项指标档案矩阵')
    title={'a':('A. Official-source conditions','A．官方来源条件'),'b':('B. Alternative, prior, and acquisition conditions','B．替代来源、先验与获取条件'),'c':('C. Instruction checks and heuristic index','C．指导材料检查与启发式指数')}[panel]
    d.text(18,28,title[0] if en else title[1],22,bold=True)
    d.text(18,49,'Archived codes by workflow. Each task row has CANN and CUDA columns; G uses ROCm/HIP in the second column.' if en else '按工作流组织的历史编码。每项任务均列 CANN 与 CUDA；G 的第二列为 ROCm/HIP。',13,fill='#566474')
    left=250;cell=105;header_y=66
    d.text(17,92,'Task' if en else '任务',17,bold=True)
    for i,metric in enumerate(metrics):
        x=left+i*cell*2
        d.rect(x,header_y,cell*2-6,25,'#edf1f5',r=3)
        d.text(x+cell-3,84,metric_label(metric,lang),14,bold=True,anchor='middle')
        d.text(x+cell/2,108,'CANN',13,bold=True,anchor='middle')
        d.text(x+cell*1.5,108,'CUDA‡',13,bold=True,anchor='middle')
    y=120
    stripe=False
    for row in ordered_tasks(tasks):
        if row[0]=='group':
            d.rect(12,y,1074,17,'#edf4f2',r=0)
            d.text(18,y+13,row[1] if en else row[2],13,bold=True,fill='#285f55')
            y+=19
            continue
        task=row[1];t=task['task_id'];h=22
        if stripe:d.rect(12,y,1074,h,'#f8fafb',r=0)
        stripe=not stripe
        name=(SHORT if en else SHORT_CN)[ord(t)-65]
        suffix=('  [CANN / ROCm-HIP]' if en else '［CANN／ROCm-HIP］') if t=='G' else ''
        d.text(18,y+16,t,14,bold=True)
        d.text(42,y+16,name+suffix,13.5)
        for i,metric in enumerate(metrics):
            x=left+i*cell*2
            for side,stack in enumerate(['cann','cuda']):
                value=score_value(scores[t][stack],metric)
                d.rect(x+side*cell+2,y+2,cell-7,h-4,metric_color(value,metric),r=3)
                shown='—' if value in (None,'受阻') else (f'{value:.2f}' if metric==11 else str(value))
                d.text(x+side*cell+(cell-5)/2,y+16,shown,14,bold=True,anchor='middle')
        y+=h
    d.text(18,872,'M1–M10 are archived ordinal codes (1–5; higher is more favorable; M8 denotes lower effort). “—” = unobserved core adequacy.' if en else 'M1–M10 为历史有序编码（1–5；高值更有利；M8 高值表示更低成本）。“—”表示核心充分性未观测。',12,fill='#566474')
    d.text(18,892,'* M7 is an archived estimate. † M11 is the historical heuristic availability index. ‡ For G, CUDA‡ = ROCm/HIP; it is excluded from CANN/CUDA summaries.' if en else '* M7 为历史估计。† M11 为历史启发式可得性指数。‡ G 的 CUDA‡ 实为 ROCm/HIP，且不计入 CANN/CUDA 汇总。',12,fill='#566474')
    d.save()


def access_profile(lang):
    en=lang=='en'
    tasks=json.loads((ROOT/'data/tasks.json').read_text())
    raw=json.loads((ROOT/'data/raw_original.json').read_text())
    scores=json.loads((ROOT/'data/legacy_scores_original.json').read_text())
    d=Drawing('figure-3-access-profile',1100,920,lang,'Access-profile detail for archived task pairs' if en else '任务对的读取状态辅助剖面')
    d.text(18,28,'Access-profile detail' if en else '读取状态辅助剖面',22,bold=True)
    d.text(18,49,'This detail keeps actual acquisition states distinct from the legacy M2 extraction score in Figure 2.' if en else '该辅助图将实际获取状态与图2中的历史 M2 抽取评分明确区分。',13,fill='#566474')
    labels=['Content access','Content adequacy','Version clarity'] if en else ['正文读取状态','正文充分性','版本清晰度']
    left=400;cell=114
    d.text(17,92,'Task' if en else '任务',17,bold=True)
    for g,title in enumerate(labels):
        x=left+g*cell*2
        d.rect(x,66,cell*2-6,25,'#edf1f5',r=3)
        d.text(x+cell-3,84,title,14,bold=True,anchor='middle')
        d.text(x+cell/2,108,'CANN',13,bold=True,anchor='middle')
        d.text(x+cell*1.5,108,'CUDA‡',13,bold=True,anchor='middle')
    status={'static':('C','#e0eee8'),'ssr':('C','#e0eee8'),'partial':('P','#faeac2'),'spa':('N','#f3c9c6'),'robots':('N','#f3c9c6')}
    y=120;stripe=False
    for row in ordered_tasks(tasks):
        if row[0]=='group':
            d.rect(12,y,1074,17,'#edf4f2',r=0)
            d.text(18,y+13,row[1] if en else row[2],13,bold=True,fill='#285f55')
            y+=19
            continue
        task=row[1];t=task['task_id'];h=22
        if stripe:d.rect(12,y,1074,h,'#f8fafb',r=0)
        stripe=not stripe
        name=(SHORT if en else SHORT_CN)[ord(t)-65]
        suffix=('  [CANN / ROCm-HIP]' if en else '［CANN／ROCm-HIP］') if t=='G' else ''
        d.text(18,y+16,t,14,bold=True);d.text(42,y+16,name+suffix,13.5)
        for side,stack in enumerate(['cann','cuda']):
            s=scores[t][stack]['scores'];access,col=status[raw[t][stack]['core_fetch']]
            values=[(access,col),(s[2],PALETTE.get(s[2],'#e4e7ec')),(s[3],PALETTE.get(s[3],'#e4e7ec'))]
            for g,(value,color) in enumerate(values):
                x=left+g*cell*2+side*cell
                d.rect(x+2,y+2,cell-7,h-4,color,r=3)
                shown='—' if value=='受阻' else value
                d.text(x+(cell-5)/2,y+16,shown,14,bold=True,anchor='middle')
        y+=h
    d.text(18,872,'Access: C = core obtained; P = partial / alternative route; N = not obtained. Adequacy and version retain archival 1–5 codes.' if en else '读取：C＝核心正文已取得；P＝部分／替代路径取得；N＝未取得。充分性和版本保留历史 1–5 编码。',12,fill='#566474')
    d.text(18,892,'‡ For G, CUDA‡ = ROCm/HIP; it is a migration analogy and is excluded from CANN/CUDA summaries.' if en else '‡ G 的 CUDA‡ 实为 ROCm/HIP；它是迁移类比，不计入 CANN/CUDA 汇总。',12,fill='#566474')
    d.save()


if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    for lang in ['en','cn']:
        framework(lang)
        full_matrix_panel(lang,'a',[1,2,3,4])
        full_matrix_panel(lang,'b',[5,6,7,8])
        full_matrix_panel(lang,'c',[9,10,11])
        access_profile(lang)
    print('Built the workflow figure, three full-matrix facets, and an access-profile detail in editable SVG.')
