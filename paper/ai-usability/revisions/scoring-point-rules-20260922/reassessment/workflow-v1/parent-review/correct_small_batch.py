"""Explicit parent adjudications after reading both complete archived packets.

This is a record-specific correction, not a reusable automatic scoring engine.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT.parent / 'inputs'

def read(name):
    directory = ROOT / 'batch' / name
    p = json.loads((INPUTS / (name + '.json')).read_text())
    f = json.loads((directory / 'facts.json').read_text())
    a = json.loads((directory / 'assessment.json').read_text())
    texts = {s['event_id']: s['text'] for s in p['sources'] + p['prior']}
    texts.update({e: p['final'] for e in p['final_event_ids']})
    def ev(e, q):
        assert q in texts[e], (e, q)
        return {'event_id': e, 'quote': q}
    return directory, p, f, a, ev

def put(a, name, status, score, reason, evidence):
    a['metrics'][name] = dict(status=status, score=score, reason=reason, evidence=evidence)

def save(d, f, a, notes):
    for name, value in [('facts', f), ('assessment', a)]:
        (d / (name + '.json')).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    (d / 'interpretation.md').write_text(notes)

d,p,f,a,ev = read('J-cuda-kimi-k3-2-standard-20260921T113432')
f['task_requirements'] = {
    'main': ['Ubuntu从零安装CUDA toolkit的完整主路线', '安装后PATH和LD_LIBRARY_PATH配置'],
    'secondary': ['验证安装与生效方法'],
    'version_relations': ['Ubuntu版本与CUDA toolkit支持关系', 'CUDA toolkit与驱动兼容关系']}
f['m4'] = {'conflicts': [], 'missing_relations': ['返回材料未给出CUDA 13.4.1所需驱动版本下限或兼容范围'], 'mode': 'partial'}
put(a,'M3','scored',3,'官方保存内容提供完整安装段落和驱动命令，但核心环境变量章节只返回缺失说明，未取得PATH/LD_LIBRARY_PATH正文；此为本次取得内容的缺口。',[
    ev('WebFetch_1_0fbc4b45.result','# apt install cuda-toolkit'),
    ev('WebFetch_5_89b8172e.result','# apt install nvidia-open'),
    ev('WebFetch_2_c7536ba8.result','- ❌ Environment Setup 中关于 `PATH` 的 export 命令')])
put(a,'M4','scored',3,'已给出CUDA 13.4.1对应Ubuntu支持列表及驱动单独安装原则，但未给出该toolkit所需驱动版本下限或兼容范围；branch 615指南标题不等于二者兼容规则。',[
    ev('WebFetch_1_0fbc4b45.result','| Ubuntu 24.04 LTS | `ubuntu2404` | amd64 / arm64 |'),
    ev('WebFetch_1_0fbc4b45.result','To run CUDA applications, install a compatible driver separately'),
    ev('WebFetch_3_37e2f4e5.result','This guide provides installation instructions for the NVIDIA driver (branch 615).')])
put(a,'M9','scored',3,'最终答案给出CUDA 13.4.1和Ubuntu支持范围；驱动分支只转述指南标题并标注未核实，未建立所选toolkit与驱动的适用范围。因此是部分组件有依据，而不是所有组件都有范围但未锁具体版本的4分。',[
    ev('run-end','- 当前 CUDA 版本：**13.4 Update 1（13.4.1）**'),
    ev('run-end','3. 当前驱动分支号：驱动指南标题称 branch 615，正文 warning 提及 branch 590 起包名变更，具体最新版本号未进一步核实。')])
f['m10'] = {'content_check_complete': True, 'content_repairs': ['主路线URL的<arch>未解释应取x86_64还是sbsa；需补充仓库架构值映射'], 'environment_substitutions': ['<distro>'], 'unresolved': ['未建立所选CUDA toolkit与驱动的兼容依据']}
put(a,'M10','needs_review',None,'有完整安装命令，但<arch>缺少取值说明，另主路线的toolkit/驱动兼容适用性仍未核清。按不可核查的主路线兼容断言分支保留待复核；不把未运行或二手出处本身作为错误。',[
    ev('run-end','wget https://developer.download.nvidia.com/compute/cuda/repos/<distro>/<arch>/cuda-keyring_1.1-1_all.deb'),
    ev('run-end','sudo apt install nvidia-open'),
    ev('run-end','sudo apt install cuda-toolkit')])
f['m6']['checked_event_ids'] = [s['event_id'] for s in p['sources']]
f['m6']['claims'][2]['claim'] = 'Ubuntu 22.04配置CUDA需在.bashrc添加PATH、CUDA_HOME、LD_LIBRARY_PATH及LIBRARY_PATH四个导出设置'
f['m6']['claims'][2]['claim_evidence'] = [ev('WebFetch_8_4b7a9994.result', 'Linux-Ubuntu22.04在配置cuda时，还需要在~/.bashrc末尾增加以下内容：'), ev('WebFetch_8_4b7a9994.result','export PATH=/usr/local/cuda/bin:$PATH\nexport CUDA_HOME=/usr/local/cuda\nexport LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH\nexport LIBRARY_PATH=$LIBRARY_PATH:/usr/local/cuda/lib64')]
f['m6']['excluded_fragments'] = ['其他搜索条目仅介绍文章主题，未保存可识别的具体操作断言；HF_ENDPOINT与本题CUDA安装无关。']
a['metrics']['M6']['reason'] = '已检查全部保存来源。共享库路径定义与博客四项导出设置缺少可追溯的外部核对支持；PyTorch摘要“此错误”对象不明，不能核清限定条件。保留待复核，不把源文重引作支持，也不从未支持推断为假。'
put(a,'M7','needs_review',None,'先验确有network/runfile路线和环境命令，官方归档支持keyring及部分安装步骤，第三方支持环境导出形式；但其CUDA 12.x元包包含驱动与ldconfig条件未由固定材料核清，不能据当前13.4规则反推旧版本正确或错误。未核清内容会影响完整正确主路线判定，保留待复核。',[
    ev('client-note-00005','sudo apt update && sudo apt -y install cuda-toolkit-12-x（或 cuda 元包，含驱动）'),
    ev('client-note-00005','APT 方式通常库已通过 ldconfig 注册，LD_LIBRARY_PATH 有时非必需；runfile 安装时需要。')])
a['metrics']['M11']['reason'] = 'M6、M7为needs_review，必要输入未定，不计算综合指数。'
for doc in a['metrics']['M2']['documents']:
    doc.setdefault('observations', {})['completeness_verification'] = 'not_independently_verified'
save(d,f,a,'# Parent-reviewed interpretation\n\nThe full question includes installation and environment setup. M4/M9 retain Ubuntu–toolkit and toolkit–driver relations; branch titles are not compatibility proof. M2 uses the last return per fragment-normalized URL (2,5,1,5,2), distinct from M3 content coverage. All two searches and seven fetches were read. M6 retains the unresolved PyTorch referent and does not use a claim to verify itself. M7 old-version package behavior was not established by the current-version excerpt. M10 has an unexplained architecture placeholder and unresolved main-route driver compatibility; no hardware execution deduction was made. These uncertainties remain null; this is not a claim that the experiment lost its logs.\n')

d,p,f,a,ev = read('A-cann-deepseek-v4_1-flash-standard-20260921T094956')
f['task_requirements'] = {'main': ['已有ONNX模型经环境准备、目标芯片选择、ATC命令转换为.om并验证输出'], 'secondary': ['说明转换约束和部署推理入口'], 'version_relations': ['CANN/ATC与ONNX适用关系', 'ATC目标芯片与运行芯片匹配关系']}
f['m4']['mode'] = 'partial'
for s in f['source_items']:
    if s.get('url') and s.get('ownership') == 'official': s['content_group'] = s['url'].split('#')[0]
    if s.get('query_index') == 3 and s.get('rank') in (1,2,3): s['relevant'] = False
put(a,'M3','scored',4,'保存官方正文已覆盖静态ONNX转换主流程、环境、芯片查询、命令参数和成功输出；ONNX opset/算子支持细节以及实际部署推理步骤仍指向外部资料。主流程可识别，题目相关约束与后续参考未齐，不能给5。',[
    ev('call_00_POOXi7ifGKggeNbMhbGX4701.result','atc --model=model.onnx --framework=5 --output=model --soc_version=Ascend310B4'),
    ev('call_00_IgX7yN9qUkFuwhqigYGK8655.result','只支持算子清单中的算子，并需满足算子限制条件。'),
    ev('call_00_XSB6JXroa7MhGGWXPIJK7421.result','获取msame工具，参考该工具配套的README，进行体验。')])
a['metrics']['M4']['evidence'] = [ev('call_00_p1UVBLh6Ls84YB0EQZ3y5529.result','请使用与芯片名相对应的*<soc_version>*取值进行模型转换，然后再进行推理。'),ev('call_00_XSB6JXroa7MhGGWXPIJK7421.result','若用户使用6.0.1之前的CANN版本进行的模型转换，无法在6.0.1及之后CANN版本进行推理')]
a['metrics']['M9']['evidence'] = [ev('run-end','**CANN 8.0.RC2.alpha002（社区版）**'),ev('run-end','**ONNX opset 上限与 ONNX→昇腾算子支持清单**：本次未取得直接正文，无法给出具体 opset 数值范围。')]
f['m10'] = {'content_check_complete': True, 'content_repairs': [], 'environment_substitutions': ['模型文件与输出路径', 'soc_version实际芯片值', 'CANN安装路径', '动态输入时的节点名称与固定shape'], 'unresolved': ['所用ONNX模型与CANN/ATC的opset适用范围未给出']}
put(a,'M10','needs_review',None,'静态转换主路线和环境替换已给出，动态多档位是额外分支，不能仅因该分支未核清判已知错误；但ONNX与选定ATC的适用范围未核清，影响任意输入模型能否沿主路线转换，按兼容性待复核分支保留null。',[
    ev('run-end','atc --model=model.onnx --framework=5 --output=model --soc_version=Ascend310B4'),
    ev('run-end','**ONNX opset 上限与 ONNX→昇腾算子支持清单**：本次未取得直接正文，无法给出具体 opset 数值范围。')])
claims=[]
def claim(sid, text, ce, se, verdict='supported'):
    claims.append(dict(source_id=sid,claim=text,claim_evidence=ce,support_evidence=se,verdict=verdict,independent_crosscheck=bool(se) and verdict=='supported'))
q1='call_00_antJV6qc0qWDBUKCiftM5340.result';q2='call_00_tTMXtlfzDKQzojifeULb5655.result';intro='call_00_t9KESpmVakYHRaTaksNj7661.result';example='call_00_POOXi7ifGKggeNbMhbGX4701.result'
support=ev(intro,'它可以将开源框架的网络模型以及Ascend IR定义的单算子描述文件（json格式）转换为昇腾AI处理器支持的.om格式离线模型。')
claim('source-0001-rank-1','ONNX模型可转换为OM并用于昇腾离线推理',[ev(q1,'本章节主要介绍如何将ONNX模型转化为昇腾AI处理器支持的OM模型，并进行离线推理。')],[ev(example,'atc --model=model.onnx --framework=5 --output=model --soc_version=Ascend310B4'),ev(intro,'通过**AscendCL接口加载模型文件**实现推理过程')])
claim('source-0001-rank-2','ATC将不同框架模型转换为OM格式',[ev(q1,'它的核心任务，就是把用不同“方言”（框架）写的模型，翻译成昇腾AI处理器能直接听懂的“机器语言”（OM格式）。')],[support])
claim('source-0001-rank-3','ONNX转OM用于昇腾离线推理',[ev(q1,'本章节介绍 ONNX 模型如何转化为 OM 模型，并在昇腾AI处理器上做离线推理。')],[ev(example,'atc --model=model.onnx --framework=5 --output=model --soc_version=Ascend310B4'),ev(intro,'通过**AscendCL接口加载模型文件**实现推理过程')])
claim('source-0002-rank-3','soc_version场景中310B4是设备名，需匹配芯片',[ev(q2,'得到的310B4就是设备名称')],[ev(example,'atc --model=model.onnx --framework=5 --output=model --soc_version=Ascend310B4'),ev('call_00_p1UVBLh6Ls84YB0EQZ3y5529.result','在查询到的“Name”前增加Ascend信息')])
f['m6']['claims']=claims
f['m6']['checked_event_ids']=[s['event_id'] for s in p['sources']]
f['m6']['excluded_fragments']=['其他第三方摘要介绍文章所覆盖的主题，未保存可识别的具体额外操作断言；未知作者论坛单列归属争议，不能作为已确认第三方。']
put(a,'M6','scored',5,'四条可识别第三方操作说法经保存的官方ONNX转换示例、OM部署解释和芯片命名规则交叉支持；其余摘要仅介绍文章主题。未据标题虚构性能或PyTorch直接转换断言，未发现这四项的关键矛盾。', [x for c in claims for x in c['claim_evidence']+c['support_evidence']])
a['metrics']['M7']['evidence']=[ev('client-note-00005','ONNX→OM 的整体流程：准备 ONNX（固定/明确输入维度）→ 配置环境变量 → 调用 `atc` 指定 `--framework=5`（5 代表 ONNX）→ 指定 `--model`、`--output`、`--soc_version` → 生成 `.om` → 用 `msame`/`benchmark`/`acl` 接口加载推理。'),ev('client-note-00005','支持的 ONNX opset 上限、CANN 版本与 ATC 参数差异')]
a['metrics']['M7']['reason']='先验给出经官方材料支持的ONNX静态转换主流程和主要参数；精确版本/opset及部分芯片枚举与可选参数未核清，未达到完整约束的5分。4分仅指已核对主流程，不为全部附加说法背书；自报不确定本身不扣分。'
save(d,f,a,'# Parent-reviewed interpretation\n\nThe question emphasizes ONNX → ATC → .om conversion; deployment is a follow-on pointer, not an invented full application implementation requirement. M3=4 reflects completed conversion flow but missing explicit compatibility/reference detail. M4/M9 retain the missing ONNX opset relation. The first-query forum author is unknown, so M1 is unresolved; generic query-three portals are not task-specific evidence. M6 was rebuilt from complete saved snippet assertions with substantive official support, replacing title-only claims. M7=4 is scoped to the supported static conversion route, not every optional assertion. M10 retains main-route compatibility uncertainty and does not manufacture an error from optional dynamic-shape discussion or lack of execution. M11 remains null.\n')
