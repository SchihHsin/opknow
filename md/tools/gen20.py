# -*- coding: utf-8 -*-
"""把 20_human_ai_journey.html 重写成保留图形信息的 Markdown（v2）。
数据源：extract20.mjs 导出的 JSON（由内嵌 <script> 经 Node 求值）。
"""
import json, re, pathlib, sys

# 目录自洽：<repo>/md/tools/gen20.py
HERE = pathlib.Path(__file__).resolve().parent
MD   = HERE.parent                     # <repo>/md
REPO = MD.parent                       # <repo>

# 用法：python3 gen20.py [数据JSON] [输出MD]
DATA = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else (HERE / 'j20.json')
OUT  = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else (MD / '20_开发者与Agent协作分析.md')

D = json.load(open(DATA, encoding='utf-8'))

# ---------------- 工具 ----------------
LANE = {'off': '昇腾官方', 'sec': '二手社区', 'ai': 'AI（Agent）',
        'hu': '人类用户', 'tool': '本机工具', 'comm': '社区（官方 / 二手）',
        'exec': '执行方（① 档＝人类用户，②③ 档＝AI）', 'self': '自身（自持动作）'}
# 渲染顺序取自 renderV 的 LX（sec < off < ai < hu < tool）
ORDER = ['sec', 'off', 'ai', 'hu', 'tool']
# 注意：`OFF` 是 Mermaid sequenceDiagram 词法里的保留字，别名必须避开
PID = {'sec': 'SEC', 'off': 'OFFI', 'ai': 'AI', 'hu': 'HU', 'tool': 'TOOL', 'comm': 'COMM'}


def pid(k):
    return PID.get(k, str(k).upper())
KIND_ZH = {'start': '起点', 'search': '检索（多来源）', 'fetch': '检索（抓官方）',
           'draft': '起草', 'run': '执行', 'decision': '决策', 'deliver': '交付'}
PHASE_RGB = [('EEF1F7', 238, 241, 247), ('EFEAF7', 239, 234, 247), ('E9F4F0', 233, 244, 240),
             ('E9F4F0', 233, 244, 240), ('FBF0E0', 251, 240, 224), ('E9F4F0', 233, 244, 240),
             ('E6EDF8', 230, 237, 248)]


def clean(h):
    """把源页 HTML 富文本转成 markdown 行内文本。"""
    if not h:
        return ''
    s = h
    s = re.sub(r'<span class="lbl">(.*?)</span>', r'**【\1】** ', s)
    s = re.sub(r'<br\s*/?>', '<br>', s)
    s = re.sub(r'</div>\s*<div[^>]*>', '<br>', s)
    s = re.sub(r'<div[^>]*>', '', s)
    s = s.replace('</div>', '')
    s = re.sub(r'<b>(.*?)</b>', r'**\1**', s, flags=re.S)
    s = re.sub(r'<code>(.*?)</code>', r'`\1`', s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', s)
    s = (s.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
         .replace('&nbsp;', ' ').replace('&quot;', '"'))
    s = re.sub(r'\s*<br>\s*', '<br>', s)
    s = re.sub(r'(<br>)+', '<br>', s)
    s = s.strip().strip('<br>').strip()
    return s.replace('|', '\\|')


def cell(h):
    return clean(h).replace('\n', ' ')


def nodes_of(scen):
    return D[f'{scen}_NODES']


def phases_of(scen):
    return D[f'{scen}_PHASE']


def branches_of(scen):
    return D.get(f'{scen}_BRANCH', [])


def flow_of(scen):
    return D[f'{scen}_FLOW']


def detail_of(scen):
    return D[f'{scen}_NDETAIL']


def aliist(scen):
    if scen == 'D':
        return D['SCEN_D']['A']
    if scen == 'TR':
        return D['SCEN_TR']['A']
    return D['ARCHIVED_G'].get('A', [])


def ns_of(scen):
    if scen == 'D':
        return D['SCEN_D'].get('nodeScore', {})
    if scen == 'TR':
        return D['SCEN_TR'].get('nodeScore', {})
    return {}


def exec_role(scen, frm_to, lvl=0):
    return 'ai' if (frm_to == 'exec' and lvl >= 1) else ('hu' if frm_to == 'exec' else frm_to)


# ---------------- 时序图（Mermaid） ----------------
def seq_diagram(scen, lvl=0):
    NODES = nodes_of(scen)
    FLOW = flow_of(scen)
    PHASE = phases_of(scen)
    BRANCH = branches_of(scen)
    NS = ns_of(scen)
    A = aliist(scen)
    lines = ['```mermaid', 'sequenceDiagram']
    for k in ORDER:
        lines.append(f'    participant {pid(k)} as {LANE[k]}')
    if any((FLOW.get(n['id'], {}) or {}).get('to') == 'comm' for n in NODES):
        lines.append(f'    participant COMM as {LANE["comm"]}')
    title = {'D': '算子开发', 'TR': '训练', 'G': '迁移（已归档）'}[scen]
    lines.append(f'    %% 场景：{title} · 档位：{["① 人主笔·AI 辅助", "② AI 主写·人审", "③ 人委派·AI 自管"][lvl]}')

    by_id = {n['id']: n for n in NODES}
    for pi, ph in enumerate(PHASE):
        r, g, b = PHASE_RGB[pi % 7][1:]
        lines.append(f'    rect rgb({r},{g},{b})')
        lines.append(f'    Note over SEC,TOOL: 【{ph["n"]}】')
        for i, n in enumerate(NODES):
            if not (ph['a'] <= i <= ph['b']):
                continue
            nid, kind, lane = n['id'], n['kind'], n['lane']
            t = n['t']
            if kind == 'decision':
                tier = 'A 类 · 非人不可' if nid in A else 'B 类 · 技术路线'
                extra = f' ｜ {NS[nid]}' if nid in NS else ''
                lines.append(f'    Note over {pid(lane)}: ◆ {nid} 决策：{t.replace("决策：", "")}（{tier}{extra}）')
                continue
            f = FLOW.get(nid)
            if not f:
                continue
            frm = exec_role(scen, f['frm'], lvl)
            to = exec_role(scen, f['to'], lvl)
            if to == 'self' or frm == to:
                lines.append(f'    Note over {pid(frm)}: {nid} {t}（自持）')
                continue
            label = f'{nid} {t}'
            if nid in NS and not f.get('blocked'):
                label += f' ｜ {NS[nid]}'
            lines.append(f'    {pid(frm)}->>{pid(to)}: {label}')
            if f.get('blocked'):
                back = f'✕ 抓取为空（SPA）'
                if nid in NS:
                    back += f' ｜ {NS[nid]}'
                lines.append(f'    {pid(to)}--x{pid(frm)}: {back}')
            # 挂在该节点上的用户独立分支（仅档①②）
            if lvl <= 1:
                for br in BRANCH:
                    if br['from'] != nid:
                        continue
                    tgt = br.get('to') or 'off'
                    step = f' ｜ ascend {br["step"]}' if br.get('step') else ''
                    lines.append(f'    HU-->>{pid(tgt)}: {br["id"]} 用户独立分支（人→{LANE[tgt]}）· {br["t"]}{step}')
        lines.append('    end')
    lines.append('```')
    return '\n'.join(lines)


# ---------------- 阶段表 ----------------
def phase_table(scen, lvl=0):
    NODES = nodes_of(scen)
    PHASE = phases_of(scen)
    PD = D[f'{scen}_PHASE_DETAIL']
    A = aliist(scen)
    rows = ['| 阶段 | 时间步 | 主导方（该段动作多寡） | 人 / AI 动作数 | 该阶段边界说明（① 档口径） |',
            '| --- | --- | --- | --- | --- |']
    for pi, ph in enumerate(PHASE):
        ids = [i for i in range(len(NODES)) if ph['a'] <= i <= ph['b']]
        ai = sum(1 for i in ids if NODES[i]['lane'] == 'ai')
        hu = sum(1 for i in ids if NODES[i]['lane'] != 'ai')
        owner = 'Agent 自动化主导' if ai > hu else ('用户主导' if hu > ai else '人机协同')
        rng = f'{ph["a"]}–{ph["b"]}' if ph['a'] != ph['b'] else f'{ph["a"]}'
        det = PD[pi] if pi < len(PD) else {}
        nodes = det.get('nodes', '')
        bound = clean(det.get('bound', ''))
        rows.append(f'| **{ph["n"]}** | {rng} | {owner} | AI {ai} / 人 {hu} | `{nodes}`<br>{bound} |')
    return '\n'.join(rows)


# ---------------- 时间步明细表 ----------------
def step_table(scen):
    NODES = nodes_of(scen)
    FLOW = flow_of(scen)
    PHASE = phases_of(scen)
    ND = detail_of(scen)
    NS = ns_of(scen)
    A = aliist(scen)
    rows = ['| # | 阶段 | 生命线 | 类型 | 标题 | 消息方向（frm → to） | 对应架构环节（`arch`） | 矩阵分 | 发生了什么 |',
            '| --- | --- | --- | --- | --- | --- | --- | --- | --- |']
    for i, n in enumerate(NODES):
        ph = next((p['n'] for p in PHASE if p['a'] <= i <= p['b']), '')
        kind = n['kind']
        if kind == 'decision':
            typ = '决策（' + ('A 类·非人不可' if n['id'] in A else 'B 类·技术路线') + '）'
            direc = f'落在 {LANE[n["lane"]]} 线上'
        else:
            typ = KIND_ZH[kind] + ('·受阻' if n.get('blocked') else '')
            f = FLOW.get(n['id'])
            direc = f'{LANE[f["frm"]]} → {LANE[f["to"]]}' if f else '—'
        arch = clean(ND.get(n['id'], {}).get('arch', '')) or '—'
        if n['id'] in ND and (ND[n['id']].get('tier') or ND[n['id']].get('arch')):
            pass
        rows.append(f'| {i} | {ph} | {LANE[n["lane"]]} | {typ} | **{n["t"]}** | {direc} | {arch} | '
                    f'{NS.get(n["id"], "—")} | {cell(n["b"])} |')
    return '\n'.join(rows)


def branch_table(scen):
    BR = branches_of(scen)
    if not BR:
        return '_该场景无用户独立分支（`BRANCH` 为空数组）。_'
    rows = ['| 触发于（节点 → 目标线） | 动作 | 说明 |', '| --- | --- | --- |']
    for br in BR:
        tgt = br.get('to') or 'off'
        step = f' · `ascend {br["step"]}`' if br.get('step') else ''
        rows.append(f'| `{br["from"]}` → {LANE[tgt]}{step} | **{br["t"]}** | {cell(br["b"])} |')
    return '\n'.join(rows)


def decision_section(scen):
    """决策点明细。键能对上就展开；对不上则退到附录。"""
    NODES = nodes_of(scen)
    ND = detail_of(scen)
    A = aliist(scen)
    ids = [n['id'] for n in NODES if n['kind'] == 'decision']
    hit = [i for i in ids if i in ND and ND[i].get('tier')]
    miss = [i for i in ids if i not in hit]
    out = []
    for nid in ids:
        tier = 'A 类 · 非人不可' if nid in A else 'B 类 · 技术路线'
        node = next(n for n in NODES if n['id'] == nid)
        out.append(f'#### `{nid}` {node["t"]}（{tier}）')
        d = ND.get(nid)
        if not d or not d.get('tier'):
            out.append(f'> ⚠ 原页 `NDETAIL` 中**没有以 `{nid}` 为键的条目**，该决策的「决策依据 / 前置条件 / 决策链」在当前页面里不会弹出。'
                       f'内容仍存在数据层，见文末**附录 B**（按旧 ID 存放）。')
            out.append('')
            out.append(f'**原页节点正文**：{cell(node["b"])}')
            out.append('')
            continue
        if d.get('intro'):
            out.append(f'- **决策依据**：{clean(d["intro"])}')
        if d.get('pre'):
            out.append(f'- **前置条件**：{clean(d["pre"])}')
        out.append('')
        for tag, key, note in [('人做版（档①②·实测口径）', 'chain', ''),
                               ('AI 接管版（档③·原页标注为「推演」）', 'chainAI', '（推演）')]:
            ch = d.get(key) or []
            if not ch:
                continue
            out.append(f'**{tag}**')
            out.append('')
            out.append('| 阶段 | 平台 / 工具 | 具体动作 |')
            out.append('| --- | --- | --- |')
            for c in ch:
                plat = re.sub(r'<[^>]+>', '', c['plat'])
                out.append(f'| {c["st"]} | {plat} | {cell(c["d"])} |')
            out.append('')
    return '\n'.join(out), hit, miss


# ---------------- 节点职责（§4.3） ----------------
ANODE = {
    'ask': ('用户原始问句', '开发者的原始自然语言需求，原样进入 `messages`、不做关键词抽取或模板化预处理。对 D：开发一个 Ascend C 自定义算子并接入 PyTorch。'),
    'msg': ('组装 messages', '将 **system 约束**（要求给可照抄命令、锁定版本、抓取不到则如实标注）+ 历史 + 当前问句拼成模型输入；理解全部交给模型。'),
    'intent': ('① 意图解析', '读出「需完成什么 + 目标产物 + 硬约束」。对 D＝识别「开发 Ascend C 算子并接入 PyTorch」，并捕捉隐含约束：可照抄、可运行、锁版本、与本机芯片型号强相关。'),
    'subgoal': ('② 子目标拆解', '切分为可分别检索的子问题：① 官方 how-to（msopgen→编包→部署）② 工程脚手架 ③ 接入 PyTorch 的绑定方式。'),
    'route': ('③ 路由：检索 / 抓取 / 直接作答', '决定本轮如何获取信息：`web_search` 了解全貌 / `web_fetch` 抓取某官方页 / 信息已充分则直接作答。'),
    'gate': ('是否需要检索?', '模型本轮是**调用工具检索**（`tool_use`），还是**不检索、直接依据自带知识作答**（`end_turn`）。注意：选择直接作答时，若自带知识不可靠，同样可能杜撰。'),
    'search': ('web_search · 服务端工具', '在**同一次调用内自循环**（生成 query→检索→研判→续检索/停止）。关键：它**一次检索即把官方文档与 CSDN / 知乎 / GitHub 等二手内容一并返回**——并非先检索官方、失败后才转二手。`max_uses` 封顶。'),
    'fetch': ('web_fetch · 客户端工具', '需查看某官方页正文时，返回 `tool_use` 交由客户端抓取；抓取为空则如实返回「正文无法取回」。'),
    'own': ('模型自带知识（⑦）', '模型训练内置的知识，**无需检索亦可用**，是矩阵三来源（官方 / 二手 / 自带）中的第三条。**充分时为可靠答案的底；薄弱、且检索未能补足时，即为「杜撰」之源**。'),
    'relay': ('汇总当前证据（回灌）', '将本轮取回的官方正文、二手内容连同自带知识一并提交模型，进入研判。'),
    'judge': ('④ 证据是否充分?', '判断手中证据**是否足以答好本题**。充分→收敛输出终答；不足→评估能否继续检索。对 D：第 2 轮即发现官方核心页 SPA 抓取为空、二手稀薄，判定「不足」。'),
    'converge': ('⑥ 收敛（证据充分）', '证据充分即停止检索，将片段组织为有序步骤（环境→msopgen→核函数→编包→部署→绑定），并标注需用户核验项。'),
    'redo': ('能否继续检索?', '**继续检索的条件**：尚未达到检索次数上限（`max_uses` / 轮数），且模型判断「更换检索词或来源后再检索预期有效」。满足则**再检索一轮**（官方与二手仍一并返回）。'),
    'hasEv': ('是否仍有可靠证据?（检索穷尽后）', '**停止检索的条件**：要么证据已充分，要么已无法继续（达到上限 / 判断再检索亦无效）。停止后被迫作答，此时答案可靠与否取决于——官方 / 二手 / 自带 中**是否至少有一条充分**。'),
    'final': ('终答 · end_turn', '**证据充分时**：可照抄命令 + 锁定版本 + 标注核验，结果可靠。**证据缺失时风险最高**：模型**无法可靠识别「自身不知道」**，会凭记忆填补空缺，产出「看似正确、实则有误」的命令 / 版本 / 来源——即上一页 Stack Overflow『66% 被此类答案误导』。'),
}
ARCH_ORDER = ['ask', 'msg', 'intent', 'subgoal', 'route', 'gate', 'search', 'fetch', 'own',
              'relay', 'judge', 'converge', 'redo', 'hasEv', 'final']


def arch_flowchart():
    return '''```mermaid
flowchart TD
    ASK(["用户原始问句"]) --> MSG["组装 messages<br>system 约束 + 历史 + 当前问句"]
    MSG --> INTENT["① 意图解析"] --> SUB["② 子目标拆解"] --> ROUTE["③ 路由：检索 / 抓取 / 直接作答"]
    ROUTE --> GATE{"是否需要检索?<br>stop_reason"}

    GATE -- "是 · 调用工具检索" --> SEARCH["web_search · 服务端自循环<br>一次检索即把官方与二手一并返回"]
    GATE -- "是 · 调用工具检索" --> FETCH["web_fetch · 抓取官方正文"]
    GATE -- "否 · 不检索，直接依据自带知识作答" --> FINAL

    OWN["模型自带知识（⑦）<br>无需检索亦可用；薄弱时即「杜撰」之源"]

    SEARCH --> RELAY["汇总当前证据（回灌）"]
    FETCH --> RELAY
    OWN --> RELAY

    RELAY --> JUDGE{"④ 证据是否充分?<br>能否答好此题"}
    JUDGE -- "充分" --> CONV["⑥ 收敛（证据充分）"] --> FINAL
    JUDGE -- "不足" --> REDO{"能否继续检索?<br>未达上限 且 预期有效"}
    REDO -- "是 · 换检索词再检索" --> ROUTE
    REDO -- "否 · 检索已穷尽" --> HASEV{"是否仍有可靠证据?<br>官方 / 二手 / 自带 任一充分"}
    HASEV -- "有 · 依据证据作答（可靠）" --> FINAL
    HASEV -- "无 · 最高风险：凭记忆填补空缺 = 杜撰" --> FINAL

    FINAL(["终答 · end_turn<br>证据充分 → 可照抄命令 + 锁版本 + 标注核验<br>证据缺失 → 看似正确、实则有误"])

    classDef gate fill:#FCEFC7,stroke:#8a6d1a,color:#5a4708,stroke-width:1.5px
    classDef core fill:#ECE7F6,stroke:#b9abe0,color:#4a3f9e
    classDef tool fill:#eaf1f7,stroke:#bcd0e0,color:#1f5a8a
    classDef ownk fill:#F1EBF8,stroke:#a98fd0,color:#5a3fa0
    classDef grey fill:#eef0f3,stroke:#9aa0aa,color:#3a3f48
    class GATE,JUDGE,REDO,HASEV gate
    class INTENT,SUB,ROUTE core
    class SEARCH,FETCH tool
    class OWN ownk
    class ASK,MSG,RELAY,CONV,FINAL grey
```
'''


def archflow_mini():
    return '''```mermaid
flowchart TD
    A["③ 工具路由<br>决定抓官方 how-to 页（devguide / opdevg）"]
    B["⚠ web_fetch 官方页<br>SPA 子树只回导航 + meta，正文抓取为空<br>—— 出问题就在这一步（5 搜索里唯一）"]
    C["④ 研判<br>判定证据不足 / 官方受阻，不凭记忆杜撰"]
    D["⑤ 遇阻处理<br>转二手社区（sD2）+ 自带知识<br>+ 让用户开浏览器人眼自查（分支 b1）"]
    A --> B --> C --> D
    classDef err fill:#FBE3E5,stroke:#C8102E,color:#8a1220,stroke-width:1.8px
    classDef fix fill:#FBEAD9,stroke:#c0703a,color:#7a3a12
    classDef ok fill:#eef0f3,stroke:#9aa0aa,color:#3a3f48
    class A ok
    class B err
    class C,D fix
```
'''


def xychart(title, cats, vals, ylab='综合置信度（0–100）'):
    c = ', '.join('"%s"' % x for x in cats)
    return ('```mermaid\nxychart-beta\n'
            f'    title "{title}"\n'
            f'    x-axis [{c}]\n'
            f'    y-axis "{ylab}" 0 --> 100\n'
            f'    bar [{", ".join(str(v) for v in vals)}]\n'
            '```')


# ================= 组装 =================
H = []
w = H.append

w('# 开发者与 Agent 协作分析 · 人机协同旅程')
w('')
w('> **出处**：`opknow/20_human_ai_journey.html`（原页标题：*人机协同旅程：开发者完成一段任务的全链路*）')
w('> **事实基础**：取自 `task_run_log.md` 实测（**仅检索段实测、开发段重建**）。')
w('>')
w('> **一句话主题**：把「开发者从立项到交付的整段旅程」画成 **5 参与者时序图**——用时序图独有的「时间 + 协同」视角，收敛出可用性**逐段在变、被人机交接质量卡住、体感前松后紧**三个判断。')
w('>')
w('> **整理原则（v2 · 图形还原）**：')
w('>')
w('> 下面 1–3 条**不是三份数据、三种结论**，而是**同一份数据的三种承载方式**——数据层只有一份（原页内嵌 `<script>` 里的'
  '`D_NODES` / `D_BRANCH` / `D_PHASE` / `D_FLOW` 等）。1 是把图**原样搬**过来，2 是按同一份数据**重画**一遍，'
  '3 是把**画图的那段代码**也留下。真正的差别在「装法」和「有没有被重画」，不在数据本身。')
w('>')
w('> 1. **原图直接嵌进来**，不是重画：§① 的竖向时序图由原页自己的 d3 代码（`renderV()`）跑出真实 SVG，落在 `figs/`；')
w('>    §4.3 的 Agent 循环架构图本就是**手写的静态内联 `<svg>`**（不是 d3），原样抽出。README 级的图都在正文里直接可看。')
w('> 2. **同时给 Mermaid 版**：原图很宽（920px）且依赖 d3/CDN，Mermaid 版是「结构化等价」，便于在任意 Markdown 渲染器里看、也便于检索与复制。')
w('> 3. **原绘制代码入附录 A**：`renderV()` 及其依赖、§4.3 的 SVG 源码、受阻链路图生成器、以及本次出图的复现脚本——都能直接复用。')
w('> 4. 原页**折进悬浮 tooltip 的内容**（节点正文、阶段边界说明、决策依据 / 前置条件 / 决策链、§4.3 每个环节的职责）在此全部展开成表。')
w('> 5. 所有数字与文本取自内嵌 `<script>` 数据层，经 Node 求值导出，**不手工转录**。')
w('> 6. 原页 3 档「AI 自主度」滑块会 morph 图上的执行方与分支，三档各出一张原图（§1.1），Mermaid 版以 **① 档** 为基准。')
w('> 7. **图的保真度逐条验过**（拿页面实际渲染出的那份比，不是肉眼看着像）：'
  '正文 4 张时序图的**文本节点与几何坐标全部逐条一致**，架构图同样一致，明细见附录 A.4。'
  '唯一差别是字体——原页从 Google Fonts 加载 `Noto Sans SC`，独立 `.svg` 取不到该字体时回退到系统字体，'
  '字形略异但**布局不受影响**（坐标全是硬编码的）。')
w('')
w('---')
w('')

# -------- 校订提示 --------
w('## ⚠️ 校订提示：与源页的三处出入')
w('')
w('整理过程中发现三处源页自身的不一致，此处如实记录（**不改动原页数据**）：')
w('')
w('**（1）生命线的渲染顺序与页面文字说明相反**')
w('')
w('原页 §① 的提示文字写「左→右：昇腾官方 ｜ 二手社区 ｜ AI ｜ 人类用户 ｜ 本机工具」，但绘制代码 `renderV()` 里的坐标是 '
  '`LX={sec:185, off:350, ai:515, hu:680, tool:845}`，实际渲染出的**最左列是「二手社区」、其次才是「昇腾官方」**。'
  '本文的时序图按**实际渲染顺序**排列（二手社区在最左）。')
w('')
w('**（2）「算子开发」场景的节点详情键名已脱钩**')
w('')
w('原页弹层用 `NDETAIL[d.id]` 取详情。`D_NDETAIL` 的键是 `s2 / s3 / s4 / s5 / s7 / s9 / s11` 与 `d1 / d2 / d3 / dR / dP / dT / dF / dB / dQ`（**旧的一套节点 id**），'
  '而当前 `D_NODES` 的 id 是 `sD / sD2 / gD / dSoc / dTil / dVer / dAcc …`——两组**交集为空**。'
  '后果：在「算子开发」场景里，**任何节点的「对应架构环节 / 决策依据 / 决策链」都不会弹出**（`det` 恒为 `{}`）。'
  '训练（`TR_NDETAIL`）与迁移（`G_NDETAIL`）两个场景的键名是对的，功能正常。')
w('')
w('同时，旧 ID 方案里有 **9 个决策点**（A 类 3 + B 类 6），当前 `D_NODES` 只保留了 **4 个**（`dSoc / dTil / dVer / dAcc`），'
  '其中 `S.A` 只认 3 个为 A 类（`dTil` 落为 B 类）。旧数据里的 `dR`（选开发路线）、`dP`（算子原型 dtype/format）、`dF`（报错后改哪里）、`dB`（PyTorch 绑定方式）、`dQ`（精度不达标修复方向）**在新节点集里没有对应节点**——这批内容仍在数据层，见**附录 A**。')
w('')
w('**（3）§③ 交付物汇总的计数是旧口径**')
w('')
w('§③ 原文写「4 参与者 …… 、14 主节点 + 9 决策点（A 类 3 非人不可 + B 类 6 技术路线）」。'
  '按当前数据层实际值：**5 条生命线、22 个节点、4 个决策点（A 类 3 + B 类 1）、6 条用户独立分支**。'
  '本节保留原文并加此注。')
w('')
w('---')
w('')

# -------- 导语 --------
w(clean(D['SCEN_D']['label']) and '')
w('> **原页标题**：人机协同旅程：开发者完成一段任务的全链路')
w('')
w('把**开发者从立项到交付的整段旅程**画成 5 参与者时序图。当前场景：**算子开发**——开发一个算子**沿时间串过 5 次搜索'
  '（D 写 kernel → M Tiling → X 内存 → O 集成 → L 精度）**，每次对应 26 任务里不同的一个、各打穿矩阵不同行；'
  '唯一官方真受阻的是写 kernel 的 D（.41）。（上方 Tab 可切**训练场景**看另一条路对照——5 搜全在中高/高带、无受阻深谷；'
  '**推理**场景制作中、迁移场景已归档备扩。）事实取自 `task_run_log.md` 实测（仅检索段实测、开发段重建）。')
w('')
w('---')
w('')

# -------- ① --------
w('## ① 全链路时序图')
w('')
w(f'竖向时序图、**5 条生命线**。这是**「算子开发场景」全流程**：开发一个算子沿时间撞上 **5 次搜索（D→M→X→O→L）**，'
  f'每次对应 26 任务里不同的一个、各打穿矩阵不同行。原页可拖滑块看 3 档自主度、悬浮节点看细节。')
w('')
w('**核心发现**：5 次搜索里**只有写 kernel 的 D（`sD`）官方真受阻**——AI 向昇腾官方 `web_fetch`，返回红色空箭头'
  '「✕ 抓取为空（SPA）」、再转二手社区兜底；后面 M/X/O/L 官方都抓得到、但各有版本 / 二手 / 自带的坑。'
  '拖动滑块时执行 / 决策发起方 morph——越自动「人类用户」线越靠边。')
w('')

w('### 1.0 怎么读：生命线、消息与决策')
w('')
w('| 元素 | 值 | 含义 |')
w('| --- | --- | --- |')
w('| 生命线 ×5 | 二手社区 ｜ 昇腾官方 ｜ AI（Agent） ｜ 人类用户 ｜ 本机工具 | 按 `renderV()` 的实际渲染顺序（左→右） |')
w('| 消息 · 涉及 AI | 紫色实线箭头 | AI 与官方 / 二手 / 执行方之间的消息 |')
w('| 消息 · 人↔工具 | 灰蓝实线箭头 | 人在本机执行（msopgen / build.sh / 部署 / 测试） |')
w('| 受阻 · 空返回 | 红色虚线 + ✕ | `web_fetch` 官方返回空（SPA 拦），整条旅程只有 `sD` 一处 |')
w('| 用户独立分支 | 深蓝虚线箭头（人→社区） | 人**脱离 AI** 直接去昇腾社区的独立动作 |')
w('| 决策 · A 类 | 深金实心菱形 | **非人不可**——AI 拿不到本机 / 业务事实 |')
w('| 决策 · B 类 | 浅金斜纹菱形 | **技术路线**——AI 可建议、用户定夺 |')
w('| 矩阵分红字 | 节点旁红色小字 | 该步打穿到热力矩阵（17）的指标分 |')
w('| 阶段色带 | 最左列 | P1–P7 七个阶段 + 该段「人 / AI 动作数」比例条 + 四轴点（检 / 产 / 执 / 决） |')
w('| 主导方色带 | 第 2 列 | 用户主导（蓝） / 人机协同（绿） / Agent 自动化主导（紫） |')
w('')
w('> **阶段主导方**在原页里是**现算**的：`phaseOwner()` 按该阶段内 AI 节点数与用户节点数谁多来定；'
  '`phaseStats()` 另给该段的「人 / AI 动作数」与四轴归属。下表 1.1 已把这两项复算出来。')
w('')

# 1.1 三档自主度
w('### 1.1 三档「AI 自主度」（原页滑块）')
w('')
LVL = D['LVL']
w('| 档 | 模式 | 执行归谁 | 决策归谁 | 涵盖 | 说明 |')
w('| --- | --- | --- | --- | --- | --- |')
for i, L in enumerate(LVL):
    w(f'| {"①②③"[i]} | **{L["name"]}** | {L["exec"]} | {L["decide"]} | {clean(L["covers"])} | {clean(L["desc"])} |')
w('')
w('滑块对图的影响（**是建模、非实测**；仅「① 人主笔」对应实测的这一次检索）：')
w('')
w('| 档 | 图上变化 | 主导权易手次数 | 用户独立分支 |')
w('| --- | --- | --- | --- |')
for i, (h, b) in enumerate([(10, 6), (8, 6), (2, 0)]):
    w(f'| {"①②③"[i]} | '
      + ('`gD/gM/gX/gO/gL` 由 `AI → 人类用户`；`eD/eC/eX/eO/eT` 由 `人类用户 → 本机工具`；6 条用户独立分支都在'
         if i == 0 else
         ('执行转交 AI：`g*/e*` 的发起方都变 AI；**决策仍归人**，6 条独立分支保留' if i == 1 else
          '执行与决策全交 AI：`g*` 与 `e*` 塌缩在 AI 线上；**独立分支归零、安全网消失**'))
      + f' | {h} | {b} |')
w('')
w('> 原页在这三档下**受阻事实不变**（同一 CANN 生态），变的只是「谁执行、人是否核查」。')
w('')
w('**三档的原图**（由原页 `renderV()` 现场渲染，同一份算子开发旅程）：')
w('')
w('**① 人主笔 · AI 辅助**（实测对应档；6 条用户独立分支都在）')
w('')
w('![算子开发时序图 · 档① 人主笔·AI 辅助](figs/20-seq-D-l0.svg)')
w('')
w('**② AI 主写 · 人审**（执行转交 AI；交接由 10 次降到 8 次，分支仍在）')
w('')
w('![算子开发时序图 · 档② AI 主写·人审](figs/20-seq-D-l1.svg)')
w('')
w('**③ 人委派 · AI 自管**（执行与决策全交 AI；**独立分支归零、安全网消失**，图上少了 6 条虚线）')
w('')
w('![算子开发时序图 · 档③ 人委派·AI 自管](figs/20-seq-D-l2.svg)')
w('')
w('')
w('**任务分工 · 四轴**（原页折进生命线名里，现展开）：')
w('')
w('| 轴 | 归属 | 是否随档位变 | 依据 |')
w('| --- | --- | --- | --- |')
w('| 检索 · 获取知识 | AI 100% | 恒 AI | 不论哪档，「搜什么 / 抓哪页 / 几轮够 / 怎么拼步骤骨架」始终由 AI 主导 |')
w('| 产出 · 编写代码 | AI 为主（≈82%） | 恒 AI | 起草 msopgen 命令 / 核函数 / Tiling / aclnn 绑定 |')
w('| 执行 · 本地运行 | ① 档：人 100%<br>②③ 档：AI 100% | **随档位转手** | 本地 msopgen / build.sh / 部署 OPP / 集成 / 跑测试 |')
w('| 决策 · 裁定验收 | ① 档：人 100%<br>② 档：人（审批）<br>③ 档：AI（人终验） | **随档位转手** | soc_version / 版本 / 精度阈值等 A 类决策 |')
w('')
w('> 原页特意说明**为何不写单一「AI 41%」**：那只是数了几个动作节点、是较弱的代理指标；换一轴比例就反转'
  '（按产出看 AI 为主、按执行 / 决策看归属）——拆四轴各看更诚实。')
w('')
w('---')
w('')

# 1.2 算子开发
w('### 1.2 场景一 · 算子开发（原页默认场景）')
w('')
w('开发一个 Ascend C 自定义算子并接入 PyTorch——沿时间串过 **5 次搜索（D 写 kernel → M Tiling → X 内存越界 → O 注册集成 → L 精度排查）**，'
  '每次对应 26 任务里不同的一个。**唯一官方真受阻的是写 kernel 的 D（.41）**。')
w('')
w('#### 1.2.1 时序图（原图 · 档① 人主笔·AI 辅助）')
w('')
w('![算子开发全链路时序图（原页 d3 渲染）](figs/20-seq-D-l0.svg)')
w('')
w('#### 1.2.2 时序图（Mermaid 结构化等价）')
w('')
w(seq_diagram('D', 0))
w('')
w('> 图为**档①**。切到档②③时 `gD/gM/gX/gO/gL` 的接收方由「人类用户」变为「AI 自身」，`eD/eC/eX/eO/eT` 的发起方也归 AI；'
  '6 条虚线（用户独立分支）在档③消失。')
w('')
w('#### 1.2.2 阶段划分（含主导方与动作数）')
w('')
w(phase_table('D'))
w('')
w('#### 1.2.3 时间步明细（22 步）')
w('')
w(step_table('D'))
w('')
w('#### 1.2.4 用户独立分支（人 → 社区，脱离 AI 的独立动作，6 条）')
w('')
w(branch_table('D'))
w('')
w('#### 1.2.5 决策点明细（4 个）')
w('')
ds, hit, miss = decision_section('D')
w(f'> 当前 `D_NODES` 里的决策点共 **{len(hit) + len(miss)} 个**：A 类 {sum(1 for i in hit + miss if i in aliist("D"))} 个、'
  f'B 类 {sum(1 for i in hit + miss if i not in aliist("D"))} 个。其中 `NDETAIL` 能命中的 **{len(hit)} 个** —— '
  f'详见文首「校订提示（2）」。')
w('')
w(ds)
w('')
w('---')
w('')

# 1.3 训练
w('### 1.3 场景二 · 训练')
w('')
w('训练同样是 **5 次搜索的串联**，但与算子开发是**两种地形**：5 搜里**官方全部抓得到（② 全 4）**，最弱的 F 分布式也有 .72（中高）——'
  '没有 D 那种「.41 受阻、又最靠前」的深谷。真实摩擦不是文档受阻，而是**两类 AI 够不着的事实**：版本对齐、卡数 / 拓扑 / 显存 / 精度阈值。')
w('')
w('#### 1.3.1 时序图（原图 · 档①）')
w('')
w('![训练场景全链路时序图（原页 d3 渲染）](figs/20-seq-TR-l0.svg)')
w('')
w('#### 1.3.2 时序图（Mermaid 结构化等价）')
w('')
w(seq_diagram('TR', 0))
w('')
w('#### 1.3.2 阶段划分')
w('')
w(phase_table('TR'))
w('')
w('#### 1.3.3 时间步明细（23 步）')
w('')
w(step_table('TR'))
w('')
w('#### 1.3.4 用户独立分支（3 条）')
w('')
w(branch_table('TR'))
w('')
w('#### 1.3.5 决策点明细（4 个）')
w('')
ds, hit, miss = decision_section('TR')
w(ds)
w('')
w('---')
w('')

# 1.4 迁移
w('### 1.4 场景三 · 迁移（已归档 · 备扩）')
w('')
w('原页把该场景归档备扩（`ARCHIVED_G`），数据仍在页内，**不参与 Tab 切换**。')
w('')
w('#### 1.4.1 时序图（Mermaid —— 该场景**没有原图**）')
w('')
w('> 原页把迁移场景放进 `ARCHIVED_G`，**没有注册进 `SCENARIOS`**，Tab 切换里也不出现，所以页面从未渲染过它。')
w('> 另外 `G_FLOW` 里的目标写的是 **`comm`**，而 `renderV()` 的坐标表 `LX` 只有 `sec/off/ai/hu/tool` 五条线——'
  '一旦把这个场景接进 `SCENARIOS` 就会算出 `NaN` 坐标、箭头全乱。**故此处只给 Mermaid 版**（按「社区（官方 / 二手）」合并表示）。')
w('')
w(seq_diagram('G', 0))
w('')
w('#### 1.4.2 阶段划分')
w('')
w(phase_table('G'))
w('')
w('#### 1.4.3 时间步明细（13 步）')
w('')
w(step_table('G'))
w('')
w('#### 1.4.4 决策点明细（4 个）')
w('')
ds, hit, miss = decision_section('G')
w(ds)
w('')
w('---')
w('')

# 1.5 综述·算子
w('### 1.5 综述 · 算子开发场景旅程（串 5 次搜索 · 最弱 D .41）')
w('')
w('用**时序图独有的「时间 + 协同」视角**（横截面 19 看不出的）收敛成 **3 个判断 + 行动建议**——'
  '可用性**逐段在变·被最弱环节拖着**、人机**交接质量**、体感**前松后紧**。')
w('')
w('#### 判断 1 · 一个算子开发是 5 次搜索的串联，被最弱、又最靠前的「写 kernel」拖着')
w('')
w('> 核心一问：开发一个算子，AI 的可用性是一个数，还是一路在变？')
w('')
w('开发一个算子**不是搜一次**，是沿时间撞上 **5 次搜索**：写 kernel(D) → Tiling(M) → 内存越界(X) → 注册集成(O) → 精度排查(L)。可用性**一路在变**，不是一个数。')
w('')
w('5 次里 **4 次官方都抓得到**（M.63 / X.74 / O.72 / L.69，各有版本 / 二手的小坑），**只有写 kernel 的 D 官方真受阻（.41）**。'
  '但整条路的体感被 D 拖着——因为它**又最弱、又最靠前**：kernel 写不出，后面 Tiling / 编译 / 精度全建在二手地基上，到编译才报错。'
  '**场景可用性 ≈ 最弱且最靠前的那一搜。**')
w('')
w('**怎么改**：优先修**最靠前的瓶颈**——把写 kernel 那页（opdevg）静态化（治本，见 19）；在此之前，AI 抓取为空时**显式报「官方未取得、以下二手」**，别让错误地基静默往下传。')
w('')
w('**5 次搜索的可用性**（原页是 5 根横向条形，数值＝该搜的综合置信度 ×100）：')
w('')
w(xychart('算子开发 · 5 次搜索的可用性', ['写 kernel D', 'Tiling M', '内存越界 X', '注册集成 O', '精度排查 L'], [41, 63, 74, 72, 69]))
w('')
w('| 次序 | 搜索 | 值 | 原页标注 |')
w('| --- | --- | --- | --- |')
for i, (nm, v, lab) in enumerate([('写 kernel', 41, 'D .41 受阻'), ('Tiling', 63, 'M .63'),
                                  ('内存越界', 74, 'X .74'), ('注册集成', 72, 'O .72'), ('精度排查', 69, 'L .69')], 1):
    w(f'| {i} | {nm} | **{v} / 100** | {lab} |')
w('')
w('> 4 次官方都抓得到，唯独写 kernel 的 D 受阻、且最靠前——整条路被它拖着（横截面 19 给不出这条「逐段」曲线）。')
w('')
w('**供给侧治本 / 使用侧治标**（原页两张 lo-fi 卡）：')
w('')
w('| 侧 | 位置 | 现状 | 改后 |')
w('| --- | --- | --- | --- |')
w('| 昇腾社区侧 · 治根 | 官方文档站 · opdevg 写 kernel 页 | 现状（SPA）：`web_fetch` 只回导航 + meta、**正文 0 字**——AI 抓取为空，错误地基由此而起 | 改后（静态化）：正文 HTML 内含 msopgen 命令 + 参数表，**AI 一次抓全**、不必转二手 |')
w('| AI 使用侧 · 治标 | AI 助手 · 回答 | 未加防护：抓不到就静默往下写 | 显式警示：`⚠ 官方 how-to 页未取得（SPA 抓取为空）；以下据二手 + 自带知识，请核对官方`；步骤逐条标来源（步骤一 `二手` / 步骤二 `自带知识`） |')
w('')
w('#### 判断 2 · 真正卡住 D 的不是「技术难」，是人机「交接」的质量')
w('')
w('> 核心一问：一次 D 开发，AI 和人交接了多少次？哪里最容易出问题？')
w('')
w('时序图数得出来：全旅程**人机交接 10 次**（档①；原页文案写「约 8–10 次」，档②为 8 次、档③为 2 次），'
  '每一次交接都是一道**信息可能丢失的关口**：AI 给的命令带占位、人填错；人回灌的报错不全、AI 解读偏。'
  '**卡的不是「算子难写」，是这条人机流水线的接口质量。**')
w('')
w('**怎么改**：把**交接做成产品的一等公民**——AI 主动标「这里要你填什么」、报错能**一键完整回灌**、每个交接点留 checkpoint。')
w('')
w('**交接热度**（原页是「P2 检索 / P3 生成 / P4 核函数 / P5 编译部署 / P6 接入」的圆点行；'
  '该处阶段名是**另一套旧口径**，与当前 7 阶段对不上。下表按当前节点划分现算）：')
w('')
w('| 档 | 阶段内交接分布（P1→P7） | 合计 |')
w('| --- | --- | --- |')
w('| ① 人主笔 | 0 · 1 · 1 · **2** · 1 · **2** · 0 | **10** |')
w('| ② AI 主写 | 0 · 1 · 1 · 0 · 1 · 1 · 0 | **8** |')
w('| ③ 人委派 | 0 · 0 · 0 · 0 · 0 · 0 · 0 | **2** |')
w('')
w('> 算法：`handoffs(lvl)` = 相邻节点归属方发生变化的次数；「阶段内」为落在同一阶段内的相邻变化。'
  '按此口径，档①**最密的是 P4 编译内存 与 P6 精度（各 2 次）**，并非原页文案所说的「P5 编译部署段最密」——'
  '原页该处引用的是一套已被替换的阶段划分（检索 / 生成 / 核函数 / 编译部署 / 接入）。')
w('')
w('| 侧 | 位置 | 现状 | 改后 |')
w('| --- | --- | --- | --- |')
w('| 昇腾社区侧 | 官方文档站 · 命令示例 | 命令散在正文、soc_version 不说怎么取 → AI 只能现编占位、人填错 | 一个可照抄块 + 内联「npu-smi info 查芯片」步骤 → 少一次人机来回 |')
w('| AI 使用侧 | AI 助手 · 交接点 | 无标注：`msopgen … -c ai_core_` 直接给出，占位不显眼 | 运行处挂 `▢ 需你填 soc_version`；报错区提供「粘到这里，自动回灌给我解读」+ `一键回灌 ⟳` |')
w('')
w('> 交接占位的根源一半在官方命令不完整——供给侧把命令做全，使用侧的交接负担自然轻。')
w('')
w('#### 判断 3 · 体感「前松后紧」：AI 在检索段给虚假信心，落地段把人独自留下')
w('')
w('> 核心一问：开发者走完这条路，「顺 / 难」的体感曲线是什么形状？')
w('')
w('把旅程当一条体感曲线：**前段（检索 / 起草）AI 很顺、很能干**，给人「这件事 AI 能完成」的**虚假信心**；'
  '**后段（编译 / 部署 / 精度）越来越是人独自承担**，AI 退成旁边解读报错的副驾。')
w('')
w('曲线最低点是 **A 类决策**（soc_version / 版本 / 精度）——AI 够不着本机 / 业务事实、只能猜，恰好都落在后半段：**前面越顺，这里落差越大**。'
  '真正的风险不是「AI 不行」，而是**「先让你以为可行、到深水区才发现得自己来」**。')
w('')
w('**怎么改**：把这条**落差曲线显式化**——旅程一开始就告诉用户「这条路后段有 3 处只能你来（要本机芯片 / 版本 / 业务阈值）」，**别让落差到深水区才暴露**。')
w('')
w('**体感弧线**（原页是一条 SVG 曲线 + 最低点标记；本文按段还原）：')
w('')
w('| 旅程段 | 主导内容 | 谁在承担 | 体感 |')
w('| --- | --- | --- | --- |')
w('| 前段 · 检索 / 起草（P2） | 写 kernel 的 how-to 检索、拼骨架 | AI | **很顺、很能干** → 产生「这件事 AI 能完成」的虚假信心 |')
w('| 中段 · 生成 / 执行（P3–P5） | Tiling、编包、集成 | 人机交替 | 逐步转向人执行 |')
w('| 后段 · 编译 / 部署 / 精度（P4–P6） | 内存越界、版本、精度 | **人独自承担** | **落到最低点**；AI 退成解读报错的副驾 |')
w('| 最低点 · A 类决策 ×3 | soc_version / 版本 / 精度阈值 | 人（AI 只能猜） | 恰好都在后半段 → **前面越顺，落差越大** |')
w('')
w('| 侧 | 位置 | 现状 | 改后 |')
w('| --- | --- | --- | --- |')
w('| 昇腾社区侧 | 官方文档站 · 版本 | 多版本号并存、URL 还会漂——AI 锁不准版本 | 一个 canonical + 配套查询器（选机型 → 唯一命令） |')
w('| AI 使用侧 | 开始前 · 本任务路线预览 | 无预告 | 路线图：`检索·起草（AI 主导）→ 生成工程（AI）→ ⚠ 选芯片（需你来）→ 编译·部署（协同）→ ⚠ 版本·精度（需你来）` |')
w('')
w('> 但 soc_version / 精度阈值这两处 A 类**本质是本机 / 业务事实，供给侧治不了**——只能靠使用侧前置告知。'
  '「版本」是其中唯一能被供给侧治的一处。前段 AI 顺，后段有 3 处只能你亲自来——开始就告知，不到深水区才暴露。')
w('')
w('**行动建议 · Agent / 产品体验侧**（供给侧文档站的 ROI 排序见 19）：')
w('')
w('| 优先级 | 建议 | 对应节点 | 预期收益 |')
w('| --- | --- | --- | --- |')
w('| P0 | 先修**最靠前的瓶颈**：写 kernel 页 opdevg 静态化 + 抓不到「响亮」标注 | 判断 1 · `sD` | 把最弱且最靠前的环节抬起来 |')
w('| P0 | 人机**交接做成一等公民**：AI 标需填项 + 报错一键完整回灌 | 判断 2 · 编译段 | 降交接处信息丢失 |')
w('| P1 | **「前松后紧」前置告知**：旅程开头标后段需人核验的点 | 判断 3 · A 类 | 管理预期、不在深水区才报错 |')
w('| P1 | 供给侧治本（opdevg 静态化 / 版本收口 / 补二手） | → 见 19 | 把原料做好，所有 AI 工具受益 |')
w('')
w('> **总论：AI 能搬来知识，搬不动你的机器**——而且这条路是**「前松后紧」**的：真正的问题不是某个分数低，'
  '是**早期一次静默失败沿时间放大 + 后段人独自承担**。这是只有走一遍旅程才看得出的体感结论。')
w('')
w('---')
w('')

# 1.6 综述·训练
w('### 1.6 综述 · 训练场景旅程（串 5 次搜索 · 最弱 .72，无受阻深谷）')
w('')
w('同样用**时序图独有的「时间 + 协同」视角**看**训练**这条路：单卡脚本扩到多卡昇腾训练，沿时间串过 **5 次搜索**——'
  '版本兼容(I) → 分布式 HCCL(F) → 混合精度(P) → 显存 OOM(Q) → 收敛排查(R)。与算子开发对照：'
  '**5 搜全在中高/高带、官方都抓得到，没有 D 那种「最弱且最靠前」的受阻深谷**。')
w('')
w('#### 判断 1 · 换个场景，「逐段曲线」就从深谷变成平稳波动——可用性是任务相关的')
w('')
w('> 核心一问：同一套 AI，换到训练场景，这条逐段可用性曲线长什么样？')
w('')
w('训练也是 **5 次搜索的串联**，但和算子开发是**两种地形**：5 搜里**官方全部抓得到（②全 4）**，最弱的 F 分布式也有 .72（中高）、只是版本散；'
  '没有 D 写 kernel 那种 .41 受阻、又最靠前、把全程拖下水的深谷。')
w('')
w('连**二手社区**这条线在两个场景里的角色都不同：D 是「官方塌了被迫转二手、二手还薄」（受阻兜底）；'
  '训练是「**官方够用、二手再添 ranktable 实例 / 收敛经验**」（健康补充）。而且训练里**人也直接和昇腾社区交互**——'
  '去官方配套表 / Gitee 样例对齐版本拓扑、撞 OOM 时自己翻 CSDN 实战贴。同一条线，地形不同、角色就不同。')
w('')
w('这正印证**「可用性是任务相关的」**：越靠**采纳漏斗的上手 / 训练侧**（迁移、分布式、显存），华为投入越足、官方做得越厚；'
  '越往深处自研（写 kernel）越塌。**同一个 AI、同样按时间走，体感差一个量级**——这是横截面 19 的均值掩盖、只有逐段旅程才显出来的。')
w('')
w('**怎么改**：训练这条路官方都抓得到，**治本重点不在「抓不到」而在「版本散」**——收口 F/I 的版本（一个 canonical + 配套查询器）最能把 .72 抬起来。')
w('')
w(xychart('训练 · 5 次搜索的可用性', ['版本兼容 I', '分布式 HCCL F', '混合精度 P', '显存 OOM Q', '收敛排查 R'], [73, 72, 83, 86, 75]))
w('')
w('| 次序 | 搜索 | 值 | 原页标注 |')
w('| --- | --- | --- | --- |')
for i, (nm, v, lab) in enumerate([('版本兼容', 73, 'I .73'), ('分布式 HCCL', 72, 'F .72 最弱'),
                                  ('混合精度', 83, 'P .83'), ('显存 OOM', 86, 'Q .86'), ('收敛排查', 75, 'R .75')], 1):
    w(f'| {i} | {nm} | **{v} / 100** | {lab} |')
w('')
w('> 对照算子开发的 D .41 受阻：训练 5 搜全是平稳小波动，最弱 .72 也远在受阻线之上——同一 AI、不同场景，曲线形状完全不同。')
w('')
w('#### 判断 2 · 训练顺，那摩擦在哪？不在「抓不到」，在「版本对齐 + 本机拓扑」')
w('')
w('> 核心一问：既然官方都抓得到，训练落地真正卡人的是什么？')
w('')
w('训练的真实摩擦不是文档受阻，是**两类 AI 够不着的事实**：')
w('')
w('- ① **版本对齐**——torch_npu 必须与本机已装的 CANN / PyTorch 严格配套，版本号又并存（④散乱），AI 给得了配套表、给不了本机装的是哪个；')
w('- ② **本机拓扑**——多卡几张卡、怎么组网，AI 只能给 HCCL 模板。')
w('')
w('这跟算子开发的 A 类决策同源（都是本机 / 业务事实回到人），但训练里它们**每一处都有官方文档兜着**、不叠加受阻——'
  '所以是「摩擦」而非「深谷」。**真正能被供给侧改善的，正是其中的「版本散」。**')
w('')
w('**怎么改**：供给侧收口版本（治根）；使用侧把版本声明**前置**——开训前先核对本机 CANN / torch_npu 版本，别等 import 失败才发现配错。')
w('')
w('| 侧 | 位置 | 现状 | 改后 |')
w('| --- | --- | --- | --- |')
w('| 昇腾社区侧 | 官方文档站 · 版本配套表 | CANN / torch_npu / PyTorch 版本号并存、配套关系散 → AI 锁不准、人对不齐 | canonical 配套表 + 查询器（选 CANN 版本 → 唯一 torch_npu） |')
w('| AI 使用侧 | AI 助手 · 环境卡 | 无主动核对 | 显示「本机 CANN：`8.0.RC3` → 建议 torch_npu `2.1.0.post*` `需核对`」，并提供「跑 npu-smi info / pip show 把本机版本贴来，我帮你对配套表」+ `核对版本 ✓` |')
w('')
w('#### 判断 3 · 体感是「平稳协同」，不是算子那条「前松后紧」')
w('')
w('> 核心一问：两个场景的体感曲线，差在哪？')
w('')
w('把训练当一条体感曲线：**全程都是「AI 给方案 → 人按本机调 → 验证」的均匀协同**，每段都有官方文档兜着，'
  'A 类决策（版本 / 拓扑 / 精度）**分散在各段、各自独立**，不像算子那样在后半段集中爆发。')
w('')
w('所以训练**没有「检索段虚假信心 + 落地段独自承担」的落差**——它的难是**均匀分布的、可预期的**。'
  '对开发者体感而言：算子开发要管理的是「别被前段的顺骗了」，训练要管理的是「每段都得备好本机事实」。'
  '**同一个 AI，副驾的称职程度取决于这条路有没有官方兜底。**')
w('')
w('**怎么改**：训练侧顺，重点是把**每段需要的本机事实清单前置**（版本 / 卡数 / 显存 / 精度阈值），让协同更省来回；供给侧继续收口版本即可。')
w('')
w('**体感弧线对照**（原页两条 SVG 曲线：训练绿实线全程平稳、算子橙虚线前段高后段塌）：')
w('')
w('| 场景 | 形状 | 说明 |')
w('| --- | --- | --- |')
w('| **训练**（绿实线） | 全程平稳、无回落 | 「AI 给方案 → 人按本机调 → 验证」均匀协同；每段都有官方文档兜着 |')
w('| **算子**（橙虚线，对照） | 前段高 → 后段塌进受阻 | 检索段虚假信心、落地段独担；A 类决策在后半段集中爆发 |')
w('')
w('**界面 lo-fi · 改法：开训前先列本机事实清单**')
w('')
w('| # | 本机事实 | 状态 |')
w('| --- | --- | --- |')
w('| ① | CANN / torch_npu 版本 | ▢ 需你核对 |')
w('| ② | 卡数 / 组网拓扑 | ▢ 需你填 |')
w('| ③ | 单卡显存上限 / 业务精度阈值 | ▢ 需你填 |')
w('')
w('> 训练的难是均匀、可预期的——开训前一次性备齐本机事实，每段协同都更省来回。')
w('')
w('**行动建议 · 训练场景（Agent / 产品体验侧）**：')
w('')
w('| 优先级 | 建议 | 对应节点 | 预期收益 |')
w('| --- | --- | --- | --- |')
w('| P0 | 供给侧**收口版本**：CANN / torch_npu canonical 配套表 + 查询器（治训练第一坑） | 判断 2 · `sF`/`sI` | 把最弱的 F .72 抬起来 |')
w('| P0 | 使用侧**本机事实清单前置**：开训前核对版本 / 拓扑 / 显存 / 精度阈值 | 判断 3 · A 类 | 减少每段协同来回 |')
w('| P1 | **版本声明前置**：环境卡先对配套表，别等 import 失败 | 判断 2 · `dVerT` | 避免「看着对、装不上」 |')
w('| P1 | 补**带版本号的分布式 / HCCL 二手**（救 F 的 ⑤⑥ 同质） | → 见 19 | 降二手回声、抬可信度 |')
w('')
w('---')
w('')

# -------- ② --------
w('## ② Agent 底层系统工程 · 跳出业务表层看技术实现')
w('')
w('前三节是「业务层看到的旅程」；本节下沉到「P2 检索区段里，Agent 内部究竟如何运转」。')
w('')
w('### 4.1 工具调用策略：为什么是有限次检索，而非更多 / 更少')
w('')
w('时序图 `sD`–`sD2` 那几步里，AI 没有把检索工具刷到上限，实测 D 任务只搜了 ~1–2 轮就转入拼装。背后是两层机制叠加：')
w('')
w('- **硬上限 = `max_uses`**：`web_search` 是 Anthropic Messages API 的**服务端工具**，注册时带 `max_uses` 封顶（如 5）；'
  '超过会返回 `max_uses_exceeded`，模型不能无限刷。')
w('- **软停止 = 模型自主判断「信息已足够」**：服务端工具在**同一轮**内自带 loop——模型决定检索内容 → 平台执行并回灌结果 → '
  '模型判断信息是否足够 → 不足则续检索、足够则停止并生成终答（`stop_reason: end_turn`；耗时较长会先 `pause_turn` 再继续）。'
  '所以「调用 N 次」不是写死的常量，而是 **min(max_uses, 模型判断收敛点)**。')
w('- **为什么 D 任务收敛得早**：实测前 1–2 条结果（知乎 / ai6s.net / MindSpore 官方 / CSDN）已能拼出步骤骨架，边际信息递减；'
  '继续搜更多只会拿到同质 CSDN 互抄（D 的二手本就薄），模型据此判断「再搜性价比低」→ 提前停。**检索次数少 ≠ 偷懒，而是边际收益判断。**')
w('')
w('### 输入优化：用户怎么写指令能显著抬升输出精准度')
w('')
w('| 优化手段 | 对这条旅程的具体作用 |')
w('| --- | --- |')
w('| **补约束**：写明「要**可照抄的完整命令 + 锁定版本号**」 | 逼 AI 在给出 msopgen 命令那一步（现 `gD`）带上真实 soc_version 占位说明，而非泛泛描述，减少来回。 |')
w('| **限范围**：写明芯片型号 / CANN 版本（如 910B1 + 8.0.RC3） | 直接消解版本对齐这个卡点（现 `dVer`）——AI 不必在多版本间猜，输出一次到位。 |')
w('| **限渠道**：写明「优先官方文档，无法取得则说明受阻、不得编造」 | 触发 AI 在 `sD` 受阻时**诚实标注 SPA 无法抓取**并转二手，而不是用记忆补全一个看似正确、实则无法运行的步骤。 |')
w('| **给反馈**：把编译报错**原文**贴回 | AI 解读的准确度直接取决于报错原文（现 `eC`），而非「我编译失败了」这类模糊描述。 |')
w('')
w('> ⚠ 原页此表的节点引用是**旧 id**（`s5` / `d1` / `d2` / `s3` / `s9`），本文已按现节点标注，对应关系见附录 A。')
w('')
w('### 4.2 大模型每一轮内部在做什么')
w('')
w('把 P2 检索区段拆成模型的内部动作循环，逐轮对应到时序图节点。')
w('')
w('| 轮次 | 内部动作 | 原页标注的图节点（旧 id） | 现节点 |')
w('| --- | --- | --- | --- |')
w('| 第 1 轮 | **规划**：解析「Ascend C 自定义算子 + 接 PyTorch」→ 拆成「找官方 how-to → 找工程脚手架 → 找 PyTorch 绑定方式」三个子目标；**决定先发 `web_search`**。 | `s2` | `sD` |')
w('| （服务端） | **读结果 + 研判**：扫一遍搜索摘要，识别出官方页 + 知乎 + MindSpore + CSDN；判断官方页最权威 → **决定 `web_fetch` 官方 URL**。 | `s2→s3` | `sD` |')
w('| 第 2 轮 | **遇阻分支判断**：fetch 回来只有 meta、正文缺失 → 识别为 SPA 受阻 → **不编造**，改判「靠二手 + 自带知识拼」→ 决定再读 MindSpore / CSDN。 | `s3（受阻）→s4` | `sD`（受阻）→ `sD2` |')
w('| 第 3 轮 | **结果生成**：把二手碎片 + 自带知识合成步骤骨架，按「环境→msopgen→核函数→编包→部署→绑定」排序，**给占位 + 标注哪些需用户核验**（soc_version / 版本）→ 输出，`end_turn`。 | `s5` | `gD` |')
w('')
w('关键内部动作 = **「研判信息是否足够」与「遇阻是否编造」两个判断点**。D 任务的特殊性在于：官方受阻 + 二手薄 + 自带知识在 Ascend C 深处也不厚 → '
  '模型在第 2 轮就进入「没有强证据」状态，只能给骨架而非可照抄全程，这是综合分低的技术根因。')
w('')
w('### 4.3 Agent 循环架构（图）+ 最小实现代码')
w('')
w('> 示范实现 · 基于公开 Anthropic Messages API，**非 Claude 内部源码**。')
w('')
w('「我平常如何运行」的 agent 循环流程：**输入**（原始问句 + system 约束 → messages，不预处理）→ 模型推理 '
  '**①意图解析 → ②子目标拆解 → ③工具路由** → **需要工具?**（`stop_reason`）→ 是：调 **`web_search`**（服务端）/ **`web_fetch`**（客户端）→ '
  '**`tool_result` 回灌** → **④ 证据是否充分?** → 充分：**⑥ 收敛 → 终答**；不足：**能否继续检索**'
  '（未达上限且预期有效，则换检索词回 ③ 再检索一轮，官方与二手仍一并返回）。检索穷尽后若仍无可靠证据，模型**无法可靠识别「自身不知道」，'
  '会凭记忆填补空缺 = 杜撰**（看似正确、实则有误）。否（`end_turn`）则不检索、直接依据自带知识作答。')
w('')
w('#### 4.3.1 架构图（原图）')
w('')
w('![Agent 循环架构图（原页静态内联 SVG，原样抽出）](figs/20-agent-loop.svg)')
w('')
w('#### 4.3.2 架构图（Mermaid 结构化等价）')
w('')
w(arch_flowchart())
w('')
w('> **① 官方与二手由一次检索一并返回**，并非先检索官方、失败后才转二手；**② 自带知识无需检索亦在其中** —— 三者即矩阵中的三来源。')
w('')
w('#### 4.3.3 节点职责（原页悬浮详情，逐项展开）')
w('')
w('| 环节 | 职责 |')
w('| --- | --- |')
for k in ARCH_ORDER:
    t, b = ANODE[k]
    w(f'| **{t}** | {b} |')
w('')
w('#### 4.3.4 受阻链路图（原页挂在 `sD` 节点上的迷你流程）')
w('')
w('> 原页 `ARCHFLOW` 仅对 `D` 场景的 `sD` 配了链路图（训练 / 迁移的场景 `ARCHFLOW` 为空对象）。')
w('')
w('**链路图 · 写 kernel 的官方 how-to 在哪一环受阻**')
w('')
w(archflow_mini())
w('')
w('> **红＝出问题的环节** · **橙＝架构的应对**；节点名对应上面 4.3.1 的架构图。')
w('')
w('#### 4.3.5 最小实现代码（A–D 段对应架构图各环节）')
w('')
w('```python')
w('import anthropic')
w('client = anthropic.Anthropic()')
w('')
w('# ① 工具注册：web_search 是服务端工具，max_uses 即 §4.1 的硬上限')
w('TOOLS = [')
w('    {"type": "web_search_20250305", "name": "web_search", "max_uses": 5},')
w('    {"name": "web_fetch", "description": "抓取一个 URL 的正文",   # 客户端工具：演示通用 agent 循环')
w('     "input_schema": {"type": "object",')
w('         "properties": {"url": {"type": "string"}}, "required": ["url"]}},')
w(']')
w('')
w('def run_agent(user_question):')
w('    # A. 接收并解析用户原始自然语言输入 —— 直接进 messages，模型负责理解')
w('    messages = [{"role": "user", "content": user_question}]')
w('')
w('    while True:')
w('        # B. 调度：模型自己决定这一轮是搜 / 抓 / 还是直接答（§4.2 的「规划」）')
w('        resp = client.messages.create(')
w('            model="claude-opus-4-8", max_tokens=4096,')
w('            system="优先给可照抄命令、锁定版本号；官方抓不到就说明受阻，绝不编造。",')
w('            tools=TOOLS, messages=messages)')
w('        messages.append({"role": "assistant", "content": resp.content})')
w('')
w('        # C. 终止条件：模型不再要工具 → 收敛、返回终答（对应图中的 end_turn）')
w('        if resp.stop_reason != "tool_use":')
w('            return "".join(b.text for b in resp.content if b.type == "text")')
w('')
w('        # D. 多轮循环：执行客户端工具并把结果回灌（受阻时如实标注，不编造 → 图 sD）')
w('        results = []')
w('        for b in resp.content:')
w('            if b.type == "tool_use" and b.name == "web_fetch":')
w('                body = fetch_url(b.input["url"])')
w('                results.append({"type": "tool_result", "tool_use_id": b.id,')
w('                    "content": body or "（SPA / robots：正文抽不到）"})')
w('        messages.append({"role": "user", "content": results})')
w('```')
w('')
w('| 段 | 职责 |')
w('| --- | --- |')
w('| **A 段** | 接收解析用户自然语言：原始问句直接进 `messages`，不做模板化预处理——理解交给模型本身。 |')
w('| **B 段** | 调度逻辑：每轮 `messages.create` 让模型自主决定搜 / 抓 / 答。`web_search` 的多轮在服务端同一次调用内闭环（§4.1 软停止）。 |')
w('| **C 段** | 终止逻辑：`stop_reason != "tool_use"` 即模型判断信息足够、收敛产出终答——对应图中 `end_turn`。 |')
w('| **D 段** | 多轮循环 + 受阻处理：客户端工具结果回灌；**抓不到正文时显式写「正文抽不到」而非留空或臆造**，这是「绝不编造」铁律在代码层的落点（图 `sD` 受阻）。 |')
w('')
w('**诚实边界：** 上述为**公开 Messages API 的忠实示范**，用于解释 agent 循环骨架，**不是 Claude 产品的内部源码**；'
  '服务端 `web_search` 的内部检索 / 排序实现不可见，这里只能就「对外可观测的调用契约」作解。')
w('')
w('---')
w('')

# -------- ③ --------
w('## ③ 交付物汇总')
w('')
w('> ⚠ 原页此节**未被 Mermaid 化的图形覆盖**（纯文字总结），原文保留；其中计数为旧口径，见文首「校订提示（3）」。')
w('')
w('1. **全链路时序图**（本页 §1）：4 参与者（昇腾社区 ｜ AI ｜ 人类用户 ｜ 本机工具）、14 主节点 + 9 决策点'
  '（A 类 3 非人不可 + B 类 6 技术路线）+ 6 用户独立分支（人→昇腾官方，多数从决策块指出 + `sD` 安全网，'
  '对应 ascend step1/3/4/6）、人机交接连线（① 档 10 处、随档位变少）、7 阶段色带、主导方色带、逐节点悬浮详情——均锚定 D 任务实测事实。')
w('2. **业务分析全部折进上图交互**：任务分工·四轴**折进生命线名悬浮**、协同交接量化**折进图例「消息·涉及 AI」悬浮**；'
  '用户决策依据 / 前置条件 / 决策链（含每步信息来源、随滑块在「人做」「AI 接管」两版切换）**折进 ◆ 节点悬浮**；'
  '人机主导权边界逐阶段**折进左侧阶段条悬浮**。结论见 §1 下方综述。')
w('3. **技术拆解**（§2 Agent 系统工程）：工具调用策略（`max_uses` 硬上限 + 模型自主软停止）、输入优化、大模型逐轮内部动作、'
  'agent 循环架构图 + 代码；每个时序节点悬浮还标出「对应架构环节」。')
w('')
w('**诚实声明与局限：**')
w('')
w('① 旅程节点的**受阻 / 卡点 / 版本号 / 二手来源均为 D 任务实测检索所得**（见 `task_run_log.md`，也正是本项目真正测的「知识可用性」），'
  '但「一次完整开发」的**线性步骤顺序是基于实测骨架的合理重构**（开发步骤 msopgen / 编包 / aclnn 按官方文档复述、未实际运行验证），'
  '真实开发中 P4–P7 可能多次回退迭代（`d3` 驳回即触发），图为主路径示意。**滑块 3 档的分工差异为建模**'
  '（仅「① 人主笔」对应实测的这次检索，另两档非实测）；而**受阻事实在三档下不变**（同一 CANN 生态），变的只是「谁执行、人是否核查」。')
w('')
w('② §4.3 代码是**公开 Messages API 的示范实现**，解释 agent 循环契约，**非 Claude 内部源码**；服务端 `web_search` 的检索 / 排序内部实现不可观测。')
w('')
w('③ 工作量占比按**节点计数**而非真实工时；不同开发者熟练度会显著改变人侧耗时。')
w('')
w('④ 本页只刻画 D 这一个「最难」任务的旅程；成熟任务（如 G 迁移、Z 概念对照）的人机协同形态会大不相同'
  '（AI 主导区段更长、卡点更少），详见热力矩阵与启发与方向。')
w('')
w('---')
w('')


# ================= 附录 B：原图绘制代码 =================
SRC_HTML = REPO / '20_human_ai_journey.html'
raw = SRC_HTML.read_text(encoding='utf-8')
_rawlines = raw.split('\n')


def cut(start_marker, end_marker, include_end=False):
    i = raw.index(start_marker)
    j = raw.index(end_marker, i)
    if include_end:
        j += len(end_marker)
    return raw[i:j].rstrip()


def cut_lines(startswith, endswith):
    a = next(k for k, l in enumerate(_rawlines) if l.startswith(startswith))
    b = next(k for k, l in enumerate(_rawlines) if k > a and l.startswith(endswith))
    return '\n'.join(_rawlines[a:b]).rstrip()


RENDER_CODE = cut_lines('const phaseColors=', 'function syncLvlUI(){')
ARCHFLOW_DATA = cut('const D_ARCHFLOW={', '/* ===== 注册场景 D')
ARCHFLOW_FN = cut('function archFlowHtml(id){', '/* 决策节点的「横向阶段链」')
SVG43 = cut('<svg viewBox="0 0 720 712"', '</svg>', include_end=True)
HARNESS = (HERE / 'render20.mjs').read_text(encoding='utf-8')

w('## 附录 A · 图是怎么画出来的（原始代码，可直接复用）')
w('')
w('三张/几张图的来源不同，分别列出。**这些代码没有改动，都是原页原文**。')
w('')
w('### A.1 §① 时序图的绘制代码（原页 d3）')
w('')
w('原页用 `d3.select("#journey")` + 下面这段函数现场生成 SVG。整段可直接复制到任何装了 d3 v7 的页面里用——'
  '渲染前需要先 `setScenario(<场景>)` 把 `NODES / FLOW / PHASE / BRANCH` 等全局量挂上（见 §1 各表，数据源同名同义）。')
w('')
w('```js')
w(RENDER_CODE)
w('```')
w('')
w('### A.2 §4.3 架构图的源码（静态内联 SVG）')
w('')
w('**这张图不是 d3 画的**，是页面里手写的 `<svg viewBox="0 0 720 712">` 静态标记，因此可以整段搬走。'
  '每个节点的悬浮详情由 `data-k` 属性 + `ANODE` 表驱动（表已展开在 §4.3.3）。')
w('')
w('```html')
w(SVG43)
w('```')
w('')
w('### A.3 受阻链路图的生成器（`ARCHFLOW` + `archFlowHtml()`）')
w('')
w('```js')
w(ARCHFLOW_DATA)
w('```')
w('')
w('```js')
w(ARCHFLOW_FN)
w('```')
w('')
w('### A.4 本次出图的复现脚本（用原页代码跑出 SVG）')
w('')
w('原时序图不可静态抽取（是 d3 现场画的），所以用 jsdom + d3 v7 **把原页内联 `<script>` 端到端跑起来**，'
  '再序列化 `#journey` 元素。这样出来的图与页面里看到的**逐像素同源**，不是重画。')
w('')
w('依赖：`npm i d3 jsdom`（本机在 `/Users/hsin/.workbuddy/binaries/node/workspace`）。')
w('')
w('```js')
w(HARNESS.rstrip())
w('```')
w('')
w('> 数据层（`D_NODES` / `D_BRANCH` / `D_PHASE` / `D_FLOW` / `D_NDETAIL` / `TR_*` / `G_*` / `ARCHIVED_G` / `ANODE`）'
  '体量较大，已全部展开为本文 §1 / §4.3 的表；如需原文，直接看 `20_human_ai_journey.html` 的内联 `<script>`。')
w('')
w('#### 保真度自检（逐条比对，不是目视）')
w('')
w('把页面**实时渲染出的 SVG** 抓下来，与 `figs/` 里的文件比**文本节点**与**几何坐标**：')
w('')
w('| 图 | 文本节点（文件 / 页面） | 几何坐标（文件 / 页面） | 结果 |')
w('| --- | --- | --- | --- |')
w('| `20-seq-D-l0.svg` · 算子 档① 人主笔 | 109 / 109 | 126 / 126 | 逐条一致 |')
w('| `20-seq-D-l1.svg` · 算子 档② AI 主写 | 109 / 109 | 121 / 121 | 逐条一致 |')
w('| `20-seq-D-l2.svg` · 算子 档③ 人委派 | 103 / 103 | 109 / 109 | 逐条一致 |')
w('| `20-seq-TR-l0.svg` · 训练 档① | 107 / 107 | 120 / 120 | 逐条一致 |')
w('| `20-agent-loop.svg` · §4.3 架构图 | 38 / 38 | 73 / 73 | 逐条一致 |')
w('')
w('抓取与比对：')
w('')
w('```bash')
w('agent-browser open "file:///<repo>/20_human_ai_journey.html"')
w('agent-browser wait --load load && sleep 5          # d3 动画跑完再取')
w('agent-browser eval "setScenario(\'D\'); curLvl=1; draw(); document.getElementById(\'journey\').outerHTML"')
w('agent-browser eval "document.querySelector(\'#archView svg\').outerHTML"   # 架构图')
w('```')
w('')
w('两条注意：')
w('')
w('1. `agent-browser eval` 返回的是 **JSON 转义串**（属性里的 `"` 成了 `\\"`），比对前必须先 `json.loads`，'
  '否则几何坐标会全部匹配不上；用 `unicode_escape` 去转义则会把中文变成乱码。')
w('2. 只调 `setScenario()` **不会重绘**（`draw()` 在页面的 tab 点击处理里），'
  '所以档②③ 要先 `setScenario(\'D\'); curLvl=<1|2>; draw();`。')
w('')
w('---')
w('')

# -------- 附录 B --------
w('## 附录 B · 「算子开发」场景未挂载的节点详情（旧 ID 数据）')
w('')
w('以下内容存放在原页的 `D_NDETAIL` 中，**键名是旧一套节点 id**，与当前 `D_NODES` 无交集，因此在「算子开发」场景下**不会渲染**。'
  '此处按原文保留，并给出**推定的现节点对应**（推定列仅供参考，勿当结论引用）。')
w('')
w('| 旧 ID | 类别 | 推定对应现节点 | 决策依据 | 前置条件 |')
w('| --- | --- | --- | --- | --- |')
GUESS = {'s2': '`sD`', 's3': '`sD`', 's4': '`sD2`', 's5': '`gD`', 's7': '`gD`', 's9': '`eC`',
         's11': '`gO`', 'd1': '`dSoc`', 'd2': '`dVer`', 'd3': '`dAcc`', 'dT': '`dTil`',
         'dR': '（无对应）', 'dP': '（无对应）', 'dF': '（无对应）', 'dB': '（无对应）', 'dQ': '（无对应）'}
ND = D['D_NDETAIL']
for k, v in ND.items():
    tier = {'A': 'A 类 · 非人不可', 'B': 'B 类 · 技术路线'}.get(v.get('tier'), '非决策节点')
    w(f'| `{k}` | {tier} | {GUESS.get(k, "—")} | {cell(v.get("intro")) or "—"} | {cell(v.get("pre")) or "—"} |')
w('')
w('**旧 ID 的节点 → 架构环节映射**（`arch` 字段，当前同样不生效）：')
w('')
w('| 旧 ID | 推定对应现节点 | 对应架构环节 |')
w('| --- | --- | --- |')
for k, v in ND.items():
    if v.get('arch'):
        w(f'| `{k}` | {GUESS.get(k, "—")} | {clean(v["arch"])} |')
w('')
w('**旧 ID 的决策链**（`chain`＝人做版、`chainAI`＝AI 接管版）：')
w('')
for k, v in ND.items():
    if not v.get('chain'):
        continue
    t = {'A': 'A 类 · 非人不可', 'B': 'B 类 · 技术路线'}[v['tier']]
    guess = GUESS.get(k, '—')
    w(f'##### `{k}`（{t} · 推定对应 {guess}）')
    w('')
    w('| 版本 | ① 接收 | ② 研判 | ③ 决策 | ④ 反馈 |')
    w('| --- | --- | --- | --- | --- |')
    w('| **人做版（档①②）** | ' + ' | '.join(
        f'{c["st"]}<br>*{re.sub(r"<[^>]+>", "", c["plat"])}*<br>{cell(c["d"])}' for c in v['chain']) + ' |')
    if v.get('chainAI'):
        w('| **AI 接管版（档③·推演）** | ' + ' | '.join(
            f'{c["st"]}<br>*{re.sub(r"<[^>]+>", "", c["plat"])}*<br>{cell(c["d"])}' for c in v['chainAI']) + ' |')
    w('')
w('---')
w('')
w('> 本文整理自 `20_human_ai_journey.html`。如有出入，以原文件为准。')

# 顺手把 §4.3 那张静态内联 SVG（原样抽出，不做任何重绘）落到 figs/，
# 并把它原有的 style 里并进中文字体（源页字体来自 body，序列化后不带）。
FIGS = MD / 'figs'
if not FIGS.is_dir():
    FIGS.mkdir(parents=True)
FONT = ("font-family:'Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif;")
arch = re.sub(r'(<svg[^>]*?)style="', lambda m: m.group(1) + 'style="' + FONT, SVG43, count=1)
# 内联在 HTML 里时可以省 xmlns，独立成 .svg 文件就得补上。
if 'xmlns=' not in arch[:arch.index('>')]:
    arch = arch.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
(FIGS / '20-agent-loop.svg').write_text(arch + '\n', encoding='utf-8')

OUT.write_text('\n'.join(H) + '\n', encoding='utf-8')
print('写出', OUT, len(OUT.read_text(encoding='utf-8')), '字符', len(OUT.read_text(encoding='utf-8').splitlines()), '行')
