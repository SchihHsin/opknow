#!/usr/bin/env python3
"""Build editable SVG figures and adjacent English vector PDFs from frozen data.

Uses ReportLab for the PDF drawing surface. No website acquisition is performed.
Run with a Python environment containing reportlab.
"""
from pathlib import Path
import json
import math
import subprocess
import tempfile
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
    d=Drawing('figure-1-framework',1040,790,lang,'Observable Agent acquisition loop and measurement locations' if en else '可观察的 Agent 知识获取循环与测量位置')
    text=lambda zh,en_text: en_text if en else zh
    d.rect(330,12,340,48,'#edf2f8','#b6c5d5')
    d.text(500,34,text('任务与记录上下文','Task and recorded context'),22,bold=True,anchor='middle')
    d.text(500,51,text('目标、初始材料、Agent／工具、时间','Goal, artifacts, agent/tools, time'),14,anchor='middle')
    d.rect(350,88,300,54,'#f1ebf8','#cbbce5')
    d.text(500,111,text('① 解析需求','1. Interpret needs'),18,bold=True,anchor='middle')
    d.text(500,130,text('并拆解子目标','and decompose subgoals'),16,anchor='middle')
    d.rect(350,165,300,54,'#fff6df','#e0bd67')
    d.text(500,188,text('② 是否需要','2. Need external'),18,bold=True,anchor='middle')
    d.text(500,207,text('外部证据？','evidence?'),16,anchor='middle')
    d.rect(70,255,270,64,'#eaf1f8','#b4cadd')
    d.text(205,268,'web_search',20,bold=True,anchor='middle')
    d.text(205,290,text('发现官方／社区候选来源','Discover official / community candidates'),14,anchor='middle')
    d.text(205,307,text('M1 发现性 · M5 替代覆盖','M1 discovery · M5 alternative coverage'),12,fill='#426d8e',anchor='middle')
    d.rect(70,343,270,66,'#eaf1f8','#b4cadd')
    d.text(205,366,text('③ 选择 URL','3. Select URLs'),17,bold=True,anchor='middle')
    d.text(205,384,text('记录发布者、来源角色与查询','Record publisher, source role, and query'),12,anchor='middle')
    d.text(205,401,text('M6 来源可信度','M6 source credibility'),12,fill='#426d8e',anchor='middle')
    d.rect(70,433,270,64,'#eaf1f8','#b4cadd')
    d.text(205,461,'web_fetch',20,bold=True,anchor='middle')
    d.text(205,482,text('取得正文、片段或失败状态','Obtain body, fragment, or failure state'),14,anchor='middle')
    d.text(205,499,text('M2 内容状态 · M3 充分性','M2 content status · M3 adequacy'),12,fill='#426d8e',anchor='middle')
    # All M-labels deliberately use the same small blue annotation treatment.
    # They describe a measurement location rather than serving as node titles.
    d.rect(690,280,270,82,'#f3edf9','#cbbce5')
    d.text(825,307,text('模型先验','Model prior'),18,bold=True,anchor='middle')
    d.text(825,329,text('单独登记为估计或测试；','Register separately as estimate or test;'),13,anchor='middle')
    d.text(825,344,text('不等同于已取得来源','not retrieved evidence'),13,anchor='middle')
    d.text(825,356,'M7',12,fill='#426d8e',anchor='middle')
    d.rect(365,512,270,62,'#f5f6f7','#ccd3da')
    d.text(500,538,text('④ 汇总证据台账','4. Integrate the evidence ledger'),17,bold=True,anchor='middle')
    d.text(500,555,text('查询、URL、返回内容、成本与缺口','Queries, URLs, returns, effort, gaps'),12,anchor='middle')
    d.text(500,568,'M8',12,fill='#426d8e',anchor='middle')
    d.rect(365,587,270,58,'#fff6df','#e0bd67')
    d.text(500,611,text('⑤ 评估充分性与','5. Assess adequacy and'),17,bold=True,anchor='middle')
    d.text(500,630,text('版本适用性','version applicability'),16,anchor='middle')
    d.text(500,641,text('M4、M9、M10','M4, M9, M10'),12,fill='#426d8e',anchor='middle')
    d.rect(700,589,250,58,'#fff4e8','#dfaa6e')
    d.text(825,613,text('调整查询并重试','Refine query and retry'),17,bold=True,anchor='middle')
    d.text(825,632,text('仍有可检索的证据空间','When evidence remains searchable'),12,anchor='middle')
    d.rect(300,700,400,60,'#e9f3ee','#8fb9a3')
    d.text(500,724,text('⑥ 作答：下一步行动','6. Answer: next action'),18,bold=True,anchor='middle')
    d.text(500,743,text('或明确证据缺口','or explicit evidence gap'),16,anchor='middle')
    d.text(500,758,'M11',12,fill='#426d8e',anchor='middle')
    d.line([(500,60),(500,88)],arrow=True)
    d.line([(500,142),(500,165)],arrow=True)
    d.line([(430,219),(205,219),(205,255)],arrow=True)
    d.text(296,241,text('是','yes'),13,fill='#26735f',anchor='middle')
    d.line([(205,319),(205,343)],arrow=True)
    d.line([(205,409),(205,433)],arrow=True)
    # Connect to the centre of each node edge, rather than a corner, so that
    # the directional arrows remain visually unambiguous after PDF scaling.
    d.line([(340,465),(365,543)],arrow=True)
    d.line([(650,192),(825,192),(825,288)],arrow=True,dash=True)
    d.text(829,215,text('否：先验分支','no: prior branch'),12,fill='#7252a1')
    d.line([(825,362),(825,543),(635,543)],arrow=True,dash=True)
    d.line([(500,574),(500,587)],arrow=True)
    d.line([(500,645),(500,700)],arrow=True)
    d.text(520,675,text('证据充分或边界已说明','sufficient evidence or explicit boundary'),12,fill='#26735f')
    d.line([(635,616),(700,616)],arrow=True)
    d.text(668,604,text('不足','insufficient'),12,fill='#aa6d18',anchor='middle')
    # The retry loop visibly returns to web_search while routing around the
    # separate model-prior branch rather than through it.
    d.line([(950,618),(985,618),(985,235),(205,235),(205,255)],arrow=True,dash=True)
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
        1:('M1 Official find','M1 官方发现'), 2:('M2 Official access','M2 官方可获取'),
        3:('M3 Official detail','M3 官方详尽'), 4:('M4 Source version','M4 资料版本'),
        5:('M5 3P count','M5 第三方数量'), 6:('M6 3P credibility','M6 第三方可信'),
        7:('M7 Prior estimate*','M7 自带知识估计*'), 8:('M8 Search / access effort','M8 检索与获取成本'),
        9:('M9 Response version','M9 回答版本'), 10:('M10 Actionability','M10 步骤可操作'),
        11:('M11 Confidence†','M11 综合置信度†'),
    }
    return labels[metric][0 if lang=='en' else 1]


def full_matrix_panel(lang,panel,metrics):
    en=lang=='en'
    tasks=json.loads((ROOT/'data/tasks.json').read_text())
    scores=json.loads((ROOT/'data/legacy_scores_original.json').read_text())
    d=Drawing(f'figure-2-full-matrix-{panel}',1100,920,lang,'Full eleven-indicator archival matrix' if en else '完整十一项指标档案矩阵')
    title={'a':('A. Official-source conditions','A．官方来源条件'),'b':('B. Third-party, prior, and acquisition conditions','B．第三方、先验与获取条件'),'c':('C. Response checks and composite confidence','C．回答检查与综合置信度')}[panel]
    d.text(18,28,title[0] if en else title[1],22,bold=True)
    d.text(18,49,'Archived codes by workflow. Each task row has CANN and CUDA columns; G uses ROCm/HIP in the second column.' if en else '按工作流组织的历史编码。每项任务均列 CANN 与 CUDA；G 的第二列为 ROCm/HIP。',13,fill='#566474')
    # Reserve a readable task-label column: the prior 250-unit column let the
    # migration label run beneath the first score cell in the rendered PDF.
    left=310;cell=96;header_y=66
    d.text(18,92,'Task' if en else '任务',18,bold=True)
    for i,metric in enumerate(metrics):
        x=left+i*cell*2
        d.rect(x,header_y,cell*2-6,25,'#edf1f5',r=3)
        d.text(x+cell-3,84,metric_label(metric,lang),15,bold=True,anchor='middle')
        d.text(x+cell/2,108,'CANN',14,bold=True,anchor='middle')
        d.text(x+cell*1.5,108,'CUDA‡',14,bold=True,anchor='middle')
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
        # The footer establishes G's ROCm/HIP comparison. Keeping the row
        # label short makes the full matrix readable at normal PDF size.
        d.text(20,y+16,t,15,bold=True)
        d.text(50,y+16,name,16)
        for i,metric in enumerate(metrics):
            x=left+i*cell*2
            for side,stack in enumerate(['cann','cuda']):
                value=score_value(scores[t][stack],metric)
                d.rect(x+side*cell+2,y+2,cell-7,h-4,metric_color(value,metric),r=3)
                shown='—' if value in (None,'受阻') else (f'{value:.2f}' if metric==11 else str(value))
                d.text(x+side*cell+(cell-5)/2,y+16,shown,15,bold=True,anchor='middle')
        y+=h
    d.text(18,872,'M1–M10 are archived ordinal codes (1–5; higher is more favorable; M8 is an inverse effort score). “—” = unobserved official content detail.' if en else 'M1–M10 为历史有序编码（1–5；高值更有利；M8 为逆向成本评分）。“—”表示官方正文详尽度未观测。',13,fill='#566474')
    d.text(18,892,'* M7 is an archived estimate. † M11 is the historical composite confidence score from M1–M8. ‡ For G, CUDA‡ = ROCm/HIP; it is excluded from CANN/CUDA summaries.' if en else '* M7 为历史估计。† M11 为由 M1–M8 汇总的历史综合置信度。‡ G 的 CUDA‡ 实为 ROCm/HIP，且不计入 CANN/CUDA 汇总。',13,fill='#566474')
    d.save()


def access_profile(lang):
    en=lang=='en'
    tasks=json.loads((ROOT/'data/tasks.json').read_text())
    raw=json.loads((ROOT/'data/raw_original.json').read_text())
    scores=json.loads((ROOT/'data/legacy_scores_original.json').read_text())
    d=Drawing('figure-3-access-profile',1100,920,lang,'Access-profile detail for archived task pairs' if en else '任务对的读取状态辅助剖面')
    d.text(18,28,'Access-profile detail' if en else '读取状态辅助剖面',22,bold=True)
    d.text(18,49,'Actual acquisition states are distinct from the historical M2 accessibility scores in Figures 2–4.' if en else '该辅助图将实际获取状态与图2–4中的历史 M2 官方正文可获取性评分区分。',13,fill='#566474')
    labels=['Content access','Official content detail','Source version clarity'] if en else ['正文读取状态','官方正文详尽度','资料版本清晰度']
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
    d.text(18,872,'Content status: C = core obtained; P = partial content obtained; N = not obtained. Access route is recorded separately in the protocol.' if en else '内容状态：C＝核心正文已取得；P＝部分内容已取得；N＝未取得。访问路径在协议中单独记录。',12,fill='#566474')
    d.text(18,892,'‡ For G, CUDA‡ = ROCm/HIP; it is a migration analogy and is excluded from CANN/CUDA summaries.' if en else '‡ G 的 CUDA‡ 实为 ROCm/HIP；它是迁移类比，不计入 CANN/CUDA 汇总。',12,fill='#566474')
    d.save()


def framework(lang):
    """Export the paper figure from the full, editable Agent-cycle source.

    The canonical Chinese SVG is deliberately retained as a close adaptation
    of ``reports/synthesis/arch-d3.html``: its decision diamonds, direct-fetch
    route, retry loop, and evidence-exhaustion branch are method content, not
    decorative detail.  The manuscript variants only translate its labels.
    """
    source = OUT / 'figure-1-agent-evidence-cycle.svg'
    svg = source.read_text(encoding='utf-8')
    if lang == 'en':
        replacements = {
            'Agent 面向技术知识生态形成答案的证据循环': 'Agent evidence cycle for technical knowledge ecosystems',
            '开发任务 / 用户问句': 'Development task / user question',
            '组装任务上下文': 'Assemble task context',
            '约束、历史与当前问句': 'Constraints, history, and current question',
            '① 意图解析': '1. Interpret intent',
            '② 子目标拆解': '2. Decompose subgoals',
            '③ 路由：检索 / 抓取 / 直接作答': '3. Route: search / fetch / answer',
            '是否需要检索？': 'Need retrieval?',
            '工具调用决策': 'Tool-use decision',
            '发现官方与第三方候选页面': 'Discover official / third-party candidates',
            'M1 官方可发现性 · M5 第三方来源数量': 'M1 Official source discoverability · M5 Third-party source count',
            '读取选中页面的正文': 'Retrieve selected page content',
            'M2 官方正文可获取性 · M3 官方正文详尽度': 'M2 Official content accessibility · M3 Official content detail',
            '模型自带知识': 'Model prior knowledge',
            '无需检索的补充证据；': 'Supplementary evidence without retrieval;',
            '薄弱时也可能填补空缺。': 'when weak, it may fill gaps.',
            'M7 模型自带知识估计': 'M7 Estimated model prior knowledge',
            '汇总当前证据（回灌）': 'Integrate current evidence (feedback)',
            'M6 第三方来源可信度': 'M6 Third-party source credibility',
            'M8 检索与获取成本': 'M8 Search and acquisition effort',
            '④ 证据是否充分？': '4. Is evidence adequate?',
            'M4 资料版本清晰度': 'M4 Source version clarity',
            'M9 回答版本明确性': 'M9 Response version specificity',
            'M10 回答步骤可操作性': 'M10 Procedural actionability of responses',
            '⑥ 收敛（证据充分）': '6. Converge (evidence adequate)',
            '能否继续检索？': 'Can retrieval continue?',
            '未达上限且预期有效': 'Below limit and expected to help',
            '是否仍有可靠证据？': 'Any reliable evidence left?',
            '官方 / 第三方 / 先验任一充分': 'Official / third-party / prior: any adequate',
            '终答': 'Final answer',
            'M11 综合置信度（M1–M8）': 'M11 Composite confidence score (M1–M8)',
            '证据不足时，回答应显式暴露边界，而非把缺口伪装成确定性。': 'When evidence is insufficient, state the boundary rather than disguise gaps as certainty.',
            '否：依据模型先验': 'No: use model prior',
            '是：调用工具检索': 'Yes: call retrieval tools',
            '选中 URL': 'Select URL',
            '充分': 'Adequate',
            '不足': 'Insufficient',
            '是：换检索词再搜索': 'Yes: refine and search again',
            '否：检索已穷尽': 'No: retrieval exhausted',
            '有：依据证据作答': 'Yes: answer from evidence',
            '无：最高风险': 'No: highest risk',
            '模型无法可靠识别知识缺口，': 'The model may not reliably detect a knowledge gap,',
            '可能凭记忆填补空缺。': 'and may fill it from memory.',
            '已知 URL 可直接抓取': 'Known URL: fetch directly',
        }
        for original, translated in replacements.items():
            svg = svg.replace(original, translated)
        svg = svg.replace(
            'Agent 解析开发任务后，可通过搜索与抓取获取官方和第三方资料，或使用模型自带知识；随后判断证据是否充分，继续检索或基于证据收敛为终答。证据耗尽而仍不充分时存在凭记忆填补空缺的风险。',
            'After interpreting a development task, an agent can search and fetch official and third-party material or draw on model prior knowledge. It then assesses evidence, retries retrieval, or converges to a final answer. Evidence exhaustion can leave a risk of filling gaps from memory.'
        )
        # The English labels are materially wider than their Chinese
        # counterparts. Widen only these nodes while retaining their centres
        # and connection anchors, so the shared process geometry stays intact.
        svg = svg.replace('<rect x="190" y="14" width="180"', '<rect x="140" y="14" width="280"')
        svg = svg.replace('width="178" height="64"', 'width="178" height="76"')
        svg = svg.replace('y="351" font-size="6.2" fill="#426d8e">M7 Estimated model prior knowledge', 'y="361" font-size="6.2" fill="#426d8e">M7 Estimated model prior knowledge')
        svg = svg.replace('M501,358 V427 H300 V438', 'M501,370 V427 H300 V438')
        svg = svg.replace('points="250,490 335,532 250,574 165,532"', 'points="250,490 360,532 250,574 140,532"')
        svg = svg.replace('<path d="M335,532 H370"', '<path d="M360,532 H420"')
        svg = svg.replace('<text x="351" y="526"', '<text x="370" y="520"')
        svg = svg.replace('<rect x="172" y="592" width="156"', '<rect x="140" y="592" width="220"')
        # Shift the last decision rightward to create a clear routing gutter:
        # the positive branch leaves left, then turns downward without crossing
        # the widened convergence node.
        svg = svg.replace('points="470,590 575,625 470,660 365,625"', 'points="520,590 625,625 520,660 415,625"')
        svg = svg.replace('points="470,490 570,532 470,574 370,532"', 'points="520,490 620,532 520,574 420,532"')
        svg = svg.replace('<text x="470" y="527"', '<text x="520" y="527"')
        svg = svg.replace('<text x="470" y="541"', '<text x="520" y="541"')
        svg = svg.replace('<text x="470" y="622"', '<text x="520" y="622"')
        svg = svg.replace('<text x="470" y="636"', '<text x="520" y="636"')
        svg = svg.replace('M570,532 H652 V190 H364', 'M620,532 H652 V190 H364')
        svg = svg.replace('<path d="M470,574 V590"', '<path d="M520,574 V590"')
        svg = svg.replace('<text x="478" y="585"', '<text x="526" y="585"')
        svg = svg.replace('<path d="M365,625 H360 V700"', '<path d="M415,625 H385 V700"')
        svg = svg.replace('<text x="346" y="670"', '<text x="280" y="680"')
        svg = svg.replace('<path d="M470,660 V700"', '<path d="M520,660 V700"')
        svg = svg.replace('<text x="486" y="674"', '<text x="536" y="674"')
        svg = svg.replace('<text x="486" y="686"', '<text x="536" y="686"')
        svg = svg.replace('<text x="486" y="697"', '<text x="536" y="697"')
    destination = OUT / f'figure-1-framework-{lang}.svg'
    destination.write_text(svg, encoding='utf-8')

    # The anonymous ACM build accepts PDF figures.  Chrome retains the SVG as
    # vector artwork in the adjacent English PDF; the editable SVG remains the
    # canonical source and is used by the Chinese reading manuscript.
    if lang == 'en':
        chrome = Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
        if not chrome.exists():
            raise FileNotFoundError('Google Chrome is required to export the SVG figure PDF.')
        with tempfile.TemporaryDirectory() as tmp:
            html = Path(tmp) / 'figure.html'
            html.write_text(
                '<!doctype html><style>@page{size:520pt 556pt;margin:0}html,body{margin:0;width:520pt;height:556pt;overflow:hidden}img{width:520pt;height:556pt;object-fit:contain;display:block}</style>'
                f'<img src="{destination.as_uri()}">', encoding='utf-8'
            )
            subprocess.run([
                str(chrome), '--headless=new', '--disable-gpu', '--no-sandbox',
                '--allow-file-access-from-files', '--no-pdf-header-footer',
                f'--print-to-pdf={destination.with_suffix(".pdf")}', html.as_uri(),
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    for lang in ['en','cn']:
        framework(lang)
        full_matrix_panel(lang,'a',[1,2,3,4])
        full_matrix_panel(lang,'b',[5,6,7,8])
        full_matrix_panel(lang,'c',[9,10,11])
        access_profile(lang)
    print('Built the workflow figure, three full-matrix facets, and an access-profile detail in editable SVG.')
