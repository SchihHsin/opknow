"""Keep the archived HTML reading pages in sync with the added note sections."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

CN_BASIS = '''<h4 id="指标项的文献依据">指标项的文献依据</h4>
<table><thead><tr><th>指标</th><th>文献提供的概念或方法参照</th><th>本研究自行规定的部分</th></tr></thead><tbody>
<tr><td>M1、M5</td><td>Manning、Raghavan与Schütze；Kelly；Treude与Robillard</td><td>官方入口与独立第三方来源的渠道分类、查询预算和五档边界</td></tr>
<tr><td>M2</td><td>Wang与Strong；Kohlschütter等</td><td>正文交付状态、完整性区间和独立文档等权聚合</td></tr>
<tr><td>M3、M6、M9、M10</td><td>Wang与Strong；Es等；Min等；Uddin与Robillard；Reddy与Andrade</td><td>冻结任务需求、关键说法核验、版本定版和操作补改的判定条件</td></tr>
<tr><td>M4</td><td>Wang与Strong；Uddin与Robillard；Maalej与Robillard</td><td>版本—组件适用关系的五档规则</td></tr>
<tr><td>M7</td><td>Kadavath等；Min等</td><td>检索前无工具回答、任务覆盖和未知状态的处理</td></tr>
<tr><td>M8</td><td>Kelly；OECD/JRC</td><td><em>C=S+F</em>、失败调用计数和成本五档</td></tr>
<tr><td>M11</td><td>OECD/JRC；Boateng等；AERA/APA/NCME</td><td>渠道内乘法、跨渠道 noisy-OR、0.30/0.10系数及连续指数公式</td></tr>
</tbody></table>
<p>文献支持测量对象、证据边界、事实核验和聚合假设，但没有直接验证本研究的阈值、权重或概率解释。</p>'''

EN_BASIS = '''<h4 id="indicator-specific-literature-basis">Indicator-specific literature basis</h4>
<table><thead><tr><th>Indicators</th><th>Conceptual or methodological reference</th><th>Specified by this study</th></tr></thead><tbody>
<tr><td>M1, M5</td><td>Manning, Raghavan, and Schütze; Kelly; Treude and Robillard</td><td>Channel classification, search budget, and five-level boundaries</td></tr>
<tr><td>M2</td><td>Wang and Strong; Kohlschütter et al.</td><td>Body-delivery states, completeness bounds, and equal-weight document aggregation</td></tr>
<tr><td>M3, M6, M9, M10</td><td>Wang and Strong; Es et al.; Min et al.; Uddin and Robillard; Reddy and Andrade</td><td>Frozen task requirements, claim checking, version selection, and operational-correction criteria</td></tr>
<tr><td>M4</td><td>Wang and Strong; Uddin and Robillard; Maalej and Robillard</td><td>Five-level rules for version–component applicability</td></tr>
<tr><td>M7</td><td>Kadavath et al.; Min et al.</td><td>Pre-retrieval answer, task coverage, and unresolved-state handling</td></tr>
<tr><td>M8</td><td>Kelly; OECD/JRC</td><td><em>C=S+F</em>, failed-call counting, and effort bands</td></tr>
<tr><td>M11</td><td>OECD/JRC; Boateng et al.; AERA/APA/NCME</td><td>Within-channel multiplication, cross-channel noisy-OR, 0.30/0.10 coefficients, and the continuous index</td></tr>
</tbody></table>
<p>The literature supports the measurement objects, evidence boundaries, fact checking, and aggregation assumptions; it does not directly validate this study's thresholds, weights, or probability interpretation.</p>'''

CN_DIAG = '''<h4 id="从差异到诊断根因分类与不确定性">从差异到诊断：根因分类与不确定性</h4>
<p>跨生态差异本身不是根因。只有把任务需求与搜索结果、返回形态、关键来源说法和最终答案连接起来，才能提出更具体的诊断；否则应把解释保留为待核验假设。</p>
<table><thead><tr><th>观测组合</th><th>可以支持的诊断方向</th><th>不能直接推出的结论</th><th>下一步核验或改进</th></tr></thead><tbody>
<tr><td>M1低，且保存的搜索列表没有相关官方命中</td><td>本次查询和预算下官方入口未被发现</td><td>文档不存在或生态缺少相关知识</td><td>重查查询词、官方索引和已知目标的直接获取</td></tr>
<tr><td>M1高但M2仅返回框架、摘要或不完整正文</td><td>入口可见，但正文交付或表示形态存在问题</td><td>正文一定缺失，或页面技术类型本身就是原因</td><td>检查返回表示、正文边界、重试和同文档的其他官方出口</td></tr>
<tr><td>M2可评但M3低</td><td>已取得的官方正文没有覆盖冻结任务中的步骤、参数或约束</td><td>整个生态都缺少该知识</td><td>将缺口映射到任务需求，并核查对应版本章节</td></tr>
<tr><td>M2/M3较高但M4低</td><td>操作内容存在，但必要的版本—组件适用关系缺失</td><td>相关版本必然不兼容</td><td>查找兼容表、适用条件和冲突，并检查答案是否臆造关系</td></tr>
<tr><td>M5高但M6低</td><td>来源数量不等于关键说法可核验</td><td>未核验说法一定为假</td><td>保留原子说法，补充独立核验和来源归属证据</td></tr>
<tr><td>M7低而外部资料与最终答案较强</td><td>本题无检索先验不足，外部获取部分补偿</td><td>训练数据密度或生态文档质量</td><td>保留冻结先验与外部证据，做同模型重复或专家核查</td></tr>
<tr><td>来源支撑充分而M9/M10低</td><td>知识可得，但回答合成中的定版或操作组织失败</td><td>缺陷一定来自文档</td><td>逐条回溯回答主张、版本条件、代码和修正清单</td></tr>
</tbody></table>
<p>因此，“没有找到”“没有取得”“没有识别”和“文档没有提供”不是同义词。任务起点和范围、模型能力与检索策略、搜索提供方与预算、页面返回形态、来源归属、评分判断都会影响观察；本批每个模型每侧只有一次有效运行，不能把条件化差异写成生态因果结论。每项修复建议都应同时给出下一项验证，例如重查官方目标、补充独立来源核验、进行同模型重复，或在可行时执行操作。</p>'''

EN_DIAG = '''<h4 id="from-differences-to-diagnosis-root-causes-and-uncertainty">From differences to diagnosis: root causes and uncertainty</h4>
<p>Cross-ecosystem differences are not causes by themselves. A more specific diagnosis requires connecting task requirements with search results, returned representations, key source claims, and the final answer; otherwise the interpretation remains a hypothesis for verification.</p>
<table><thead><tr><th>Observed combination</th><th>Supported diagnostic direction</th><th>What it does not establish</th><th>Next verification or repair</th></tr></thead><tbody>
<tr><td>Low M1 and no relevant official hit in the saved search lists</td><td>The official entry path was not discoverable under this query and budget</td><td>That the documentation does not exist or that the ecosystem lacks the knowledge</td><td>Inspect query terms, official indexes, and direct retrieval of a known target</td></tr>
<tr><td>High M1 but M2 is scaffolding, summary, or incomplete body</td><td>The entry is visible but body delivery or target representation is a problem</td><td>That the body itself is missing, or that page technology is the cause</td><td>Check representation type, body boundaries, retries, and other official exits</td></tr>
<tr><td>M2 is assessable but M3 is low</td><td>The acquired official body omits steps, parameters, or constraints required by the frozen task</td><td>That the whole ecosystem has the same gap</td><td>Map the omission to task requirements and inspect the relevant version section</td></tr>
<tr><td>M2/M3 are adequate but M4 is low</td><td>The material explains an operation but lacks a necessary version–component applicability relation</td><td>That the versions are necessarily incompatible</td><td>Locate compatibility tables, applicability conditions, and conflicts; check whether the answer invented a relation</td></tr>
<tr><td>M5 is high but M6 is low</td><td>Source quantity is not verifiable support</td><td>That an unverified claim is false</td><td>Preserve atomic claims and add independent checking and ownership evidence</td></tr>
<tr><td>M7 is low while external material and the final answer are relatively strong</td><td>Unaided knowledge for this task is limited and external acquisition partly compensates</td><td>Training-data density or documentation quality</td><td>Retain the frozen prior and external evidence; repeat the same model or seek expert checking</td></tr>
<tr><td>Key source claims are supported but M9/M10 are low</td><td>Knowledge was available, but version selection or answer organization failed</td><td>That the defect came from documentation</td><td>Trace answer claims back to sources, version conditions, code, and corrections</td></tr>
</tbody></table>
<p>Accordingly, “not found,” “not obtained,” “not recognized,” and “not provided by the documentation” are not synonyms. Task scope and starting conditions, model capability and retrieval strategy, search provider and budget, page representation, source ownership, and assessment judgment all affect the observation. Each model has one effective episode per side in this pilot, so these conditional differences cannot be written as ecosystem-level causal effects. A repair recommendation should state the explanations still not ruled out and name the next check: revisit the official target, add independent source verification, repeat the same model, or execute the operation when feasible.</p>'''


def insert_once(path: Path, marker: str, addition: str, label: str) -> None:
    text = path.read_text()
    if addition in text:
        return
    if text.count(marker) != 1:
        raise RuntimeError(f'{label}: marker count={text.count(marker)}')
    path.write_text(text.replace(marker, addition + '\n' + marker, 1))


cn = ROOT / 'index.html'
en = ROOT / 'manuscript-en-review-changes.html'
insert_once(cn, '<p>M1–M7描述三类知识来源', CN_BASIS, 'CN literature table')
insert_once(en, '<p>M1–M7 describe support from the three knowledge sources', EN_BASIS, 'EN literature table')
insert_once(cn, '<h3\nid="不同生态在开发场景中的知识支撑分布存在差异">', CN_DIAG, 'CN diagnosis')
insert_once(en, '<h3\nid="knowledge-support-distributions-differ-between-ecosystems-across-development-scenarios">', EN_DIAG, 'EN diagnosis')
print('HTML additions synchronized')
