"""Apply the four 2026-09-22 review-comment revisions to the archived 审阅稿.

Source (read-only):  ../manuscript-cn-review-changes/
Target:              this folder

The four revision items are taken from
revisions/full-rerun-20260921/comment-revision-notes-20260922.md:

1. related work did not state why the study is still needed  -> new "research gap" paragraph
2. eleven indicators appeared without selection logic        -> new "indicator selection" subsection
3. rubric, weights and formula appeared without derivation   -> new "how the rubric was formed" paragraph
4. the case section read like an ecosystem ranking           -> retitled case and findings sections,
                                                                bounded claims, rewritten first conclusion paragraph

Only the HTML reading pages and the Markdown manuscripts are changed; the Word and
PDF editions stay in the archive folder. Wording that referred to the newer
full-rerun rubric (pre-retrieval answer freezing, C=S+F effort counting, pilot material
in rubric formation) is written here in the form that is true of this manuscript.
"""
from pathlib import Path
import re
import shutil

SRC = Path(__file__).resolve().parent.parent / 'manuscript-cn-review-changes'
DST = Path(__file__).resolve().parent

CN_HTML, EN_HTML = 'index.html', 'manuscript-en-review-changes.html'
CN_MD, EN_MD = 'manuscript-cn-v0.2.md', 'manuscript-en-v0.2.md'

# ---------------------------------------------------------------- new text (CN)
CN_GAP = ('<strong>研究缺口与本文的增量。</strong> 现有研究分别讨论开发者如何寻找信息、文档如何支持API学习、'
          '检索增强系统是否取得相关上下文，以及Agent是否完成任务；这些工作提供了重要的概念和结果指标，'
          '但通常没有把“发现了什么、实际取得了什么、哪些任务需求得到支持、版本关系是否足以定版，'
          '以及最终回答还需怎样修正”放在同一条可追溯的证据链中。尤其是，检索结果、页面返回形态、'
          '来源归属和回答属性往往分别报告，因而难以判断问题究竟来自入口、正文交付、内容缺口、来源冲突还是回答组织。'
          '本文的额外贡献不是再提出一个答案正确率，而是提出面向AI的知识可得性构念，把上述条件按任务连接起来，'
          '并用冻结问句、实际工具返回和最终答案保存可复核证据。随后以CANN/CUDA案例检验这套诊断框架能否定位'
          '文档和Agent需要改进的环节；生态间差异是案例中的诊断输出，不是本文的唯一目标或总体排名。')

CN_IND_TITLE = '指标选择逻辑与相互关系'
CN_IND_P1 = ('11项指标不是互相独立的“分数清单”，而是从任务知识链条逐层拆出：官方渠道由M1–M4覆盖发现、'
             '实际取得、内容详尽度和版本适用关系；第三方渠道由M5–M6覆盖来源数量与关键说法的证据质量；'
             '模型先验由M7单独记录；M8记录取得这些材料的检索与获取成本；M9–M10检查外部知识进入最终回答后的'
             '版本定版与操作补改；M11只把M1–M8透明地汇总为一个综合指数。这样安排是为了让每个分数对应一种'
             '可修复的缺口，而不是重复测量同一件事。')
CN_IND_P2 = ('指标之间的边界也预先固定。M1问“能否找到官方来源”，M2问“实际取得的官方正文有多少”；'
             'M3问正文是否覆盖任务内容，M4问资料是否给出必要的版本—组件关系；M5是相关独立第三方来源的数量，'
             'M6是关键说法能否被支持或反驳；M7不使用本轮取得的资料，M8只记录实际发生的检索轮次、获取调用'
             '与失败次数；M9和M10只看最终答案，分别对应定版和操作补改。因此，正文很长不自动提高M3，'
             '来源很多不自动提高M6，官方资料清楚也不自动提高M9。本文没有把人类导航易用性、开发者满意度/信任、'
             '端到端硬件执行成功率、延迟或token成本并入这11项，因为这些问题需要不同的观察单位和独立证据；'
             '遗漏它们是构念边界，而不是暗示它们不重要。')

CN_RUBRIC = ('<strong>量规与权重如何形成。</strong> 量规先从构念边界和冻结任务需求列出每项需要观察的对象，'
             '再为每项规定证据边界、缺失状态和可修复的判定条件；随后用边界案例检查容易混淆的分支，冻结规则，'
             '最后用结构、引文定位和算术检查验证执行一致性。文献为“应测量什么、如何区分证据与推断、'
             '如何披露聚合假设”提供参照，但没有一篇文献直接给出本研究的五档阈值。M11在渠道内采用乘法，'
             '是为了保留发现、取得或支撑任一环节不足的限制；渠道之间采用噪声OR，是为了表达官方、第三方和'
             '模型先验可能互相补充。版本系数0.30和成本系数0.10是预先指定的工作基线，作为对主要支撑渠道的'
             '有限修正，不是从本批结果拟合出来的最优权重；敏感性分析和未校准限制因此单独报告。这样可说明'
             '分数是如何形成的，也避免把精细的数字写成已经验证的客观量表。')

CN_CASE_TITLE_OLD = '案例应用：CANN 与 CUDA 开发生态的案例分析'
CN_CASE_TITLE_NEW = '案例应用：用 CANN 与 CUDA 检验知识诊断框架'
CN_CASE_LEAD = ('本案例把 CANN 与 CUDA 作为压力测试场景：两个生态在文档、版本和工具链条件上不同。'
                '其目的不是给出脱离任务范围的生态总体排名，而是检验这些指标能否定位可修复的知识缺口，'
                '并把缺口连接到文档和Agent的改进动作。')

CN_FIND_TITLE_OLD = '发现：跨开发任务的知识条件'
CN_FIND_TITLE_NEW = '发现：用跨生态对照定位知识条件'
CN_FIND_TAIL_OLD = '下面依次呈现场景对比、具体知识缺口及来源之间的互补情况。'
CN_FIND_TAIL_NEW = ('下面依次呈现场景对比、具体知识缺口及来源之间的互补情况。CANN/CUDA的差异用于暴露诊断线索：'
                    '它们描述本任务集和访问配置下的条件，不构成生态整体能力排名，也不是本文核心构念的替代物。')

CN_CONC_OLD = ('本文定义面向AI的知识可得性，并通过十一项指标连接知识来源、获取过程与回答属性。CANN与CUDA的'
               '任务级比较识别了不同开发场景中的知识支撑差异，包括CANN在深入自研场景中的较弱支撑，并进一步'
               '揭示了正文交付、诊断内容、版本组织及补充来源方面的具体条件。将评分与任务需求、实际取得的材料'
               '联系起来，使研究能够形成关于生态如何支持开发活动，以及哪些知识需要完善的具体认识。')
CN_CONC_NEW = ('本文的核心贡献是把面向AI的知识可得性定义为可检查的任务关系，并用十一项指标把知识来源、'
               '获取过程、证据支撑和最终回答连接起来。它服务于文档团队和Agent建设者：帮助他们定位资料未被发现、'
               '正文未被取得、关键任务内容缺失、版本关系不清或回答仍需补改的具体环节。CANN/CUDA案例提供了一个'
               '压力测试场景：任务级比较识别了不同开发场景中的知识支撑差异，并进一步揭示了正文交付、诊断内容、'
               '版本组织及补充来源方面的具体条件；这些差异是本任务集和访问配置下的诊断输出，不能脱离任务范围'
               '解释为生态整体排名。将评分与任务需求、实际取得的材料联系起来，使研究能够形成关于生态如何支持'
               '开发活动，以及哪些知识需要完善的具体认识。')

# ---------------------------------------------------------------- new text (EN)
EN_GAP = ('<strong>Research gap and incremental contribution.</strong> Existing work separately examines how '
          'developers seek information, how documentation supports API learning, whether retrieval-augmented systems '
          'obtain relevant context, and whether agents complete tasks. These studies provide important concepts and '
          'outcome measures, but they usually do not place “what was discovered, what was actually returned, which '
          'task requirements were supported, whether version relations were sufficient for selection, and what the '
          'final answer still requires” in one traceable evidence chain. Search results, returned representations, '
          'source ownership, and answer properties are often reported separately, making it difficult to tell whether '
          'a problem lies in the entry point, body delivery, content coverage, source conflict, or answer organization. '
          'Our additional contribution is therefore not another answer-correctness score. We define knowledge '
          'availability for AI and connect these conditions at the task level, preserving the frozen question, actual '
          'tool returns, and final answer for review. The CANN/CUDA case then tests whether the diagnostic framework '
          'can locate repairable documentation and agent-design gaps; ecosystem differences are diagnostic outputs of '
          'the case, not the sole objective or a population-wide ranking.')

EN_IND_TITLE = 'Indicator selection and relationships'
EN_IND_P1 = ('The eleven indicators are not an undifferentiated list of scores. They decompose the task-knowledge chain '
             'into diagnostic layers: official material is covered by M1–M4 (discovery, actual acquisition, content '
             'detail, and version applicability); third-party material by M5–M6 (source quantity and evidential '
             'quality of consequential claims); model prior by M7; retrieval effort by M8; and the final response by '
             'M9–M10 (version lockability and required operational corrections). M11 is only a transparent summary '
             'of M1–M8. This decomposition gives each grade a potentially repairable meaning rather than counting the '
             'same property repeatedly.')
EN_IND_P2 = ('The boundaries are fixed in advance. M1 asks whether an official source can be found, whereas M2 asks '
             'how much official body content was actually obtained. M3 asks whether the body covers the task, whereas '
             'M4 asks whether it establishes the required version–component relationships. M5 counts relevant '
             'independent third-party sources, whereas M6 checks whether consequential claims are supported or '
             'contradicted. M7 is recorded without the material obtained in this run, M8 records only the search '
             'rounds, acquisition calls, and failures that actually occurred, and M9–M10 inspect only the final answer, '
             'respectively for version selection and operational corrections. A long body therefore does not '
             'automatically raise M3, many sources do not automatically raise M6, and clear official material does not '
             'automatically raise M9. Human navigation usability, developer satisfaction or trust, end-to-end hardware '
             'execution success, latency, and token cost are outside these eleven indicators because they require '
             'different units of observation and independent evidence; their omission is a construct boundary, not a '
             'claim that they are unimportant.')

EN_RUBRIC = ('<strong>How the rubric and weights were formed.</strong> We first decomposed the construct and froze the '
             'task requirements, then specified the evidence boundary, missing states, and repairable decision '
             'conditions for each indicator. Boundary cases were used to expose ambiguous branches; the rules were '
             'then frozen, and structural, quotation-location, and arithmetic checks were used to verify execution '
             'consistency. The literature supplies references for what to measure, how to separate evidence from '
             'inference, and how to disclose aggregation assumptions; no cited work directly supplies these five-grade '
             'thresholds. Within a channel, multiplication in M11 preserves the limitation imposed by a missing '
             'discovery, acquisition, or support step. Across channels, the noisy-OR expresses the possibility that '
             'official, third-party, and prior knowledge can complement one another. The 0.30 version coefficient and '
             '0.10 effort coefficient are prespecified working baselines, limited modifiers of the main support '
             'channels rather than weights fitted to these results. Sensitivity analysis and the lack of calibration '
             'are therefore reported separately. This makes the formation of the numbers explicit without presenting '
             'a detailed rubric as a validated objective scale.')

EN_CASE_TITLE_OLD = 'Case Study of the CANN and CUDA Developer Ecosystems'
EN_CASE_TITLE_NEW = 'Case application: stress-testing the knowledge-diagnostic framework with CANN and CUDA'
EN_CASE_LEAD = ('The case application uses CANN and CUDA as a stress test: the two ecosystems differ in documentation, '
                'version, and toolchain conditions. The purpose is not to produce an ecosystem-wide ranking detached '
                'from task scope, but to test whether the indicators can locate repairable knowledge gaps and connect '
                'them to documentation and agent improvements.')

EN_FIND_TITLE_OLD = 'Findings: Knowledge Conditions Across Development Tasks'
EN_FIND_TITLE_NEW = 'Findings: Using cross-ecosystem contrast to locate knowledge conditions'
EN_FIND_TAIL_OLD = ('We present scenario comparisons, specific knowledge gaps, and complementarity among sources in '
                    'that order.')
EN_FIND_TAIL_NEW = ('We present scenario comparisons, specific knowledge gaps, and complementarity among sources in '
                    'that order. The CANN/CUDA contrasts are diagnostic clues for this task set and access '
                    'configuration; they are not a replacement for the construct or a population-wide ecosystem '
                    'ranking.')

EN_CONC_OLD = ('We define knowledge availability for AI through eleven indicators connecting knowledge sources, '
               'acquisition processes, and response properties. Task-level comparisons of CANN and CUDA identify '
               'differences in knowledge support across development scenarios, including weaker support for in-depth '
               'development in CANN, and reveal specific conditions involving content delivery, diagnostic detail, '
               'version organization, and supplementary sources. Connecting scores with task requirements and '
               'acquired material produces concrete insights into how ecosystems support development activities and '
               'which knowledge resources require improvement.')
EN_CONC_NEW = ('The core contribution is a task-relational definition of knowledge availability for AI and an '
               'eleven-indicator protocol that connects knowledge sources, acquisition processes, evidence support, '
               'and final responses. It is intended for documentation teams and agent builders: to locate whether a '
               'gap lies in discovery, body delivery, task coverage, version relations, source support, or response '
               'repair. The CANN/CUDA case provides a stress test of that diagnostic framework: task-level '
               'comparisons identify differences in knowledge support across development scenarios and specific '
               'conditions involving content delivery, diagnostic detail, version organization, and supplementary '
               'sources; those differences are diagnostic outputs under this task set and access configuration, not '
               'an ecosystem-wide ranking detached from task scope. Connecting scores with task requirements and '
               'acquired material produces concrete insights into how ecosystems support development activities and '
               'which knowledge resources require improvement.')


def once(text, old, new, label):
    assert text.count(old) == 1, f'{label}: expected one occurrence, found {text.count(old)}'
    return text.replace(old, new)


def once_wrapped(text, old, new, label):
    """Same as once(), for anchors inside HTML source lines that Pandoc may have wrapped."""
    pattern = re.compile(r'\s+'.join(re.escape(part) for part in old.split()))
    matches = list(pattern.finditer(text))
    assert len(matches) == 1, f'{label}: expected one occurrence, found {len(matches)}'
    return text[:matches[0].start()] + new + text[matches[0].end():]


def heading(text, anchor, old_title, new_title, label, level='2'):
    """Replace a heading and its table-of-contents entry, keeping ids and links in step."""
    pattern = re.compile(rf'<h{level}\s+id="{re.escape(anchor)}">.*?</h{level}>', re.S)
    text, n = pattern.subn(f'<h{level} id="{new_title[0]}">{new_title[1]}</h{level}>', text)
    assert n == 1, f'{label}: heading {anchor} not found'
    old_li = f'<li class="toc-{"main" if level == "2" else "sub"}"><a href="#{anchor}">{old_title}</a></li>'
    new_li = (f'<li class="toc-{"main" if level == "2" else "sub"}">'
              f'<a href="#{new_title[0]}">{new_title[1]}</a></li>')
    return once(text, old_li, new_li, label + ' (outline)')


def style_h4(text, label):
    """The reading stylesheet styles h1-h3 only; give the new subsection heading a matching rule."""
    text = once(text, 'h3{font-size:19px;line-height:1.6;margin:28px 0 12px;color:var(--accent)}',
                'h3{font-size:19px;line-height:1.6;margin:28px 0 12px;color:var(--accent)}'
                'h4{font-size:17px;line-height:1.6;margin:22px 0 10px;color:var(--accent)}', label)
    return once(text, 'h3{font-size:12pt;break-after:avoid}',
                'h3{font-size:12pt;break-after:avoid}h4{font-size:11pt;break-after:avoid}', label + ' (print)')


# ------------------------------------------------------------------------- copy
for name in (CN_HTML, EN_HTML, CN_MD, EN_MD):
    shutil.copy2(SRC / name, DST / name)

# ------------------------------------------------------------- Chinese HTML page
p = DST / CN_HTML
t = p.read_text()
t = once(t, '<p>我们将<strong>面向 AI', f'<p>{CN_GAP}</p>\n<p>我们将<strong>面向 AI', 'CN html: gap paragraph')
t = once(t, '<table>\n<caption>表2　', f'<h4 id="{CN_IND_TITLE}">{CN_IND_TITLE}</h4>\n'
                                        f'<p>{CN_IND_P1}</p>\n<p>{CN_IND_P2}</p>\n<table>\n<caption>表2　',
         'CN html: indicator selection subsection')
t = once(t, '<p><strong>官方资料（M1–M4）。</strong>\n官方可发现性综合结果位置',
         f'<p>{CN_RUBRIC}</p>\n<p><strong>官方资料（M1–M4）。</strong>\n官方可发现性综合结果位置',
         'CN html: rubric paragraph')
t = heading(t, '案例应用cann-与-cuda-开发生态的案例分析', CN_CASE_TITLE_OLD,
            ('案例应用用-cann-与-cuda-检验知识诊断框架', CN_CASE_TITLE_NEW), 'CN html: case title')
t = re.sub(r'(?s)(<h2 id="案例应用用-cann-与-cuda-检验知识诊断框架">.*?</h2>\n)',
           lambda m: m.group(1) + f'<p>{CN_CASE_LEAD}</p>\n', t, count=1)
t = heading(t, '发现跨开发任务的知识条件', CN_FIND_TITLE_OLD,
            ('发现用跨生态对照定位知识条件', CN_FIND_TITLE_NEW), 'CN html: findings title')
t = once_wrapped(t, CN_FIND_TAIL_OLD, CN_FIND_TAIL_NEW, 'CN html: findings bound')
t = once_wrapped(t, CN_CONC_OLD, CN_CONC_NEW, 'CN html: conclusion opening')
t = style_h4(t, 'CN html: h4 style')
t = once(t, '<div class="edition">中文审阅稿 · 当前版本</div>',
         '<div class="edition">中文审阅稿 · 2026-09-22 批注修订</div>', 'CN html: edition label')
t = once(t, '<title>中文审阅稿 · 当前版本</title>',
         '<title>中文审阅稿 · 2026-09-22 批注修订</title>', 'CN html: title')
t = once(t, '<a href="manuscript-cn-review-changes.html" data-language="cn" aria-current="page">中文</a>',
         '<a href="index.html" data-language="cn" aria-current="page">中文</a>', 'CN html: language switch')
p.write_text(t)

# ---------------------------------------------------------------- English page
p = DST / EN_HTML
t = p.read_text()
t = once(t, '<p>We define <strong>', f'<p>{EN_GAP}</p>\n<p>We define <strong>', 'EN html: gap paragraph')
t = once(t, '<table>\n<caption>The eleven indicators and the evidence each can',
         f'<h4 id="{EN_IND_TITLE}">{EN_IND_TITLE}</h4>\n<p>{EN_IND_P1}</p>\n<p>{EN_IND_P2}</p>\n'
         '<table>\n<caption>The eleven indicators and the evidence each can',
         'EN html: indicator selection subsection')
t = once(t, '<p><strong>Official material (M1–M4).</strong> Discoverability combines',
         f'<p>{EN_RUBRIC}</p>\n<p><strong>Official material (M1–M4).</strong> Discoverability combines',
         'EN html: rubric paragraph')
t = heading(t, 'case-study-of-the-cann-and-cuda-developer-ecosystems', EN_CASE_TITLE_OLD,
            ('case-application-stress-testing-the-knowledge-diagnostic-framework-with-cann-and-cuda',
             EN_CASE_TITLE_NEW), 'EN html: case title')
t = re.sub(r'(?s)(<h2 id="case-application-stress-testing-the-knowledge-diagnostic-framework-with-cann-and-cuda">'
           r'.*?</h2>\n)', lambda m: m.group(1) + f'<p>{EN_CASE_LEAD}</p>\n', t, count=1)
t = heading(t, 'findings-knowledge-conditions-across-development-tasks', EN_FIND_TITLE_OLD,
            ('findings-using-cross-ecosystem-contrast-to-locate-knowledge-conditions', EN_FIND_TITLE_NEW),
            'EN html: findings title')
t = once_wrapped(t, EN_FIND_TAIL_OLD, EN_FIND_TAIL_NEW, 'EN html: findings bound')
t = once_wrapped(t, EN_CONC_OLD, EN_CONC_NEW, 'EN html: conclusion opening')
t = style_h4(t, 'EN html: h4 style')
t = once(t, '<div class="edition">English manuscript · Current version</div>',
         '<div class="edition">English manuscript · 22 September 2026 comment revisions</div>',
         'EN html: edition label')
t = once(t, '<title>English manuscript · Current version</title>',
         '<title>English manuscript · 22 September 2026 comment revisions</title>', 'EN html: title')
t = once(t, '<a href="manuscript-cn-review-changes.html" data-language="cn">中文</a>',
         '<a href="index.html" data-language="cn">中文</a>', 'EN html: language switch')
p.write_text(t)

# ------------------------------------------------------------- Chinese Markdown
p = DST / CN_MD
t = p.read_text()
t = once(t, '我们将**面向 AI 的知识可得性**定义为',
         f"**研究缺口与本文的增量。** {CN_GAP.replace('<strong>研究缺口与本文的增量。</strong> ', '')}\n\n"
         '我们将**面向 AI 的知识可得性**定义为', 'CN md: gap paragraph')
t = once(t, '| 编号 | 指标 | 证据与解释 |',
         f'#### {CN_IND_TITLE}\n\n{CN_IND_P1}\n\n{CN_IND_P2}\n\n| 编号 | 指标 | 证据与解释 |',
         'CN md: indicator selection subsection')
t = once(t, '**官方资料（M1–M4）。** M1依据首次命中的查询',
         f"**量规与权重如何形成。** {CN_RUBRIC.replace('<strong>量规与权重如何形成。</strong> ', '')}\n\n"
         '**官方资料（M1–M4）。** M1依据首次命中的查询', 'CN md: rubric paragraph')
t = once(t, f'## {CN_CASE_TITLE_OLD}\n\n### 任务覆盖与比较范围',
         f'## {CN_CASE_TITLE_NEW}\n\n{CN_CASE_LEAD}\n\n### 任务覆盖与比较范围', 'CN md: case title and lead')
t = once(t, f'## {CN_FIND_TITLE_OLD}', f'## {CN_FIND_TITLE_NEW}', 'CN md: findings title')
t = once(t, CN_FIND_TAIL_OLD, CN_FIND_TAIL_NEW, 'CN md: findings bound')
t = once(t, CN_CONC_OLD, CN_CONC_NEW, 'CN md: conclusion opening')
p.write_text(t)

# ------------------------------------------------------------- English Markdown
p = DST / EN_MD
t = p.read_text()
t = once(t, 'We define **knowledge availability for AI**',
         f"**Research gap and incremental contribution.** "
         f"{EN_GAP.replace('<strong>Research gap and incremental contribution.</strong> ', '')}\n\n"
         'We define **knowledge availability for AI**', 'EN md: gap paragraph')
t = once(t, '| ID | Indicator | Evidence and interpretation |',
         f'#### {EN_IND_TITLE}\n\n{EN_IND_P1}\n\n{EN_IND_P2}\n\n| ID | Indicator | Evidence and interpretation |',
         'EN md: indicator selection subsection')
t = once(t, '**Official material (M1–M4).** M1 uses the first successful query',
         f"**How the rubric and weights were formed.** "
         f"{EN_RUBRIC.replace('<strong>How the rubric and weights were formed.</strong> ', '')}\n\n"
         '**Official material (M1–M4).** M1 uses the first successful query', 'EN md: rubric paragraph')
t = once(t, f'## {EN_CASE_TITLE_OLD}\n\n### Task coverage and comparison scope',
         f'## {EN_CASE_TITLE_NEW}\n\n{EN_CASE_LEAD}\n\n### Task coverage and comparison scope',
         'EN md: case title and lead')
t = once(t, f'## {EN_FIND_TITLE_OLD}', f'## {EN_FIND_TITLE_NEW}', 'EN md: findings title')
t = once(t, EN_FIND_TAIL_OLD, EN_FIND_TAIL_NEW, 'EN md: findings bound')
t = once(t, EN_CONC_OLD, EN_CONC_NEW, 'EN md: conclusion opening')
p.write_text(t)

# ------------------------------------------------------------------- checks
print('files written:')
for name in (CN_HTML, EN_HTML, CN_MD, EN_MD):
    print(f'  {name:40s} {(DST / name).stat().st_size:>10,} bytes')

for name, checks in {
        CN_HTML: ['研究缺口与本文的增量', CN_IND_TITLE, '量规与权重如何形成', CN_CASE_TITLE_NEW,
                  CN_FIND_TITLE_NEW, '2026-09-22 批注修订'],
        EN_HTML: ['Research gap and incremental contribution', EN_IND_TITLE,
                  'How the rubric and weights were formed', EN_CASE_TITLE_NEW, EN_FIND_TITLE_NEW,
                  '22 September 2026 comment revisions'],
        CN_MD: ['**研究缺口与本文的增量。**', f'#### {CN_IND_TITLE}', '**量规与权重如何形成。**',
                f'## {CN_CASE_TITLE_NEW}', f'## {CN_FIND_TITLE_NEW}'],
        EN_MD: ['**Research gap and incremental contribution.**', f'#### {EN_IND_TITLE}',
                '**How the rubric and weights were formed.**', f'## {EN_CASE_TITLE_NEW}',
                f'## {EN_FIND_TITLE_NEW}'],
}.items():
    t = (DST / name).read_text()
    missing = [c for c in checks if c not in t]
    assert not missing, f'{name}: missing {missing}'
    if name.endswith('.html'):
        ids = re.findall(r'<h[1-4]\b[^>]*\bid="([^"]+)"', t)
        dupes = {i for i in ids if ids.count(i) > 1}
        anchors = set(re.findall(r'<a href="#([^"]+)">', t))
        broken = sorted(a for a in anchors if a not in set(ids))
        assert not dupes, f'{name}: duplicate ids {dupes}'
        assert not broken, f'{name}: outline anchors without a target {broken}'
        print(f'  {name}: {len(ids)} headings, {len(anchors)} outline anchors, no duplicates, no broken anchors')
    else:
        print(f'  {name}: all four revision markers present')
print('ok')
