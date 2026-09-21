"""Record-specific parent decisions after reading every saved source and answer."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NAME='A-cann-glm-5_3-standard-20260921T094947'
d=ROOT/'batch'/NAME
p=json.loads((ROOT.parent/'inputs'/(NAME+'.json')).read_text())
f=json.loads((d/'facts.json').read_text())
a=json.loads((d/'assessment.json').read_text())
texts={s['event_id']:s['text'] for s in p['sources']+p['prior']}
texts.update({e:p['final'] for e in p['final_event_ids']})
def ev(e,q):
    assert q in texts[e],(e,q)
    return dict(event_id=e,quote=q)
def metric(k,status,score,reason,evidence):
    a['metrics'][k]=dict(status=status,score=score,reason=reason,evidence=evidence)
q1='call_4cbea904b4754282afb418b6.result'; body='call_7f7f606fad0c462dbcaa2c61.result'; quick='call_960c228cecc44aefa48405f5.result'; query3='call_b45f917dd87d4d2fb8841ae3.result'
f['m1']=dict(budget_exhausted=False,decisive_records_verified=True,first_hit_source_id='source-0001-rank-4',first_query=1,first_rank=4)
metric('M1','scored',4,'第一次搜索第4位为相关官方ONNX→OM转换文档。', [ev(q1,'## 4. [将ONNX模型转换为OM模型-CANN商用版8.0.0-昇腾社区]')])
scores=[5,5,2,5,2,2,5,1]
for item,score in zip(f['fetches'],scores):
    item.update(ownership='official',representation='body' if score==5 else 'title',target_match='matched' if score!=1 else 'wrong',observed_defect=False)
metric('M2','scored',27/8,'8次实际派发：4份直接正文、3份目标标题、1份错误官网壳；27/8=3.375。第9次fetch被预算拦截未派发，不参与文档均值。', [x['evidence'] for x in f['fetches']])
a['metrics']['M2']['documents']=[dict(id=x['request_url'],status='scored',score=s,observations={'completeness_verification':'not_independently_verified'}) for x,s in zip(f['fetches'],scores)]
metric('M3','scored',3,'取得官方转换命令、参数解释、芯片查询和成功验证段落；主流程的环境准备具体操作及ONNX适用约束未在已取得正文中齐备。安装和set_env说明只见搜索摘要，不能冒充正文覆盖。', [ev(body,'--framework：原始框架类型，5表示ONNX。'),ev(quick,'ATC run success, welcome to the next use.'),ev(body,'请在服务器执行**npu-smi info**命令进行查询')])
f['m4']=dict(conflicts=[],missing_relations=['ONNX opset与所选CANN/ATC适用关系'],mode='partial')
metric('M4','scored',3,'官方给出8.5.0之后ops算子包匹配要求、跨版本周期规则和芯片查询方法，但缺ONNX opset与CANN/ATC关系。', [ev(quick,'**针对8.5.0及之后版本**：使用ATC工具进行模型转换时，必须安装与目标昇腾AI处理器匹配的ops算子包，否则会导致编译失败。'),ev(body,'实际配置的*<soc_version>*值为Ascend*xxxyy*。')])
for s in f['source_items']:
    if s.get('url'): s['content_group']=s['url'].split('#')[0]
    else:s['relevant']=False
    if s['source_id']=='source-0011-rank-4':s['relevant']=False
    if s['source_id']=='source-0011-rank-5':s['ownership']='unknown'
f['m5']['possible_counts']=[4,5]
metric('M5','needs_review',None,'4个确定相关第三方内容组；gitcode cann/docs相关但官方内容归属未由包内记录确认，纳入与否会使来源数4或5跨档。SiP信号处理库环境变量文章不直接对应ATC转换任务，排除。', [ev(query3,'https://gitcode.com/cann/docs/blob/master/docs/zh/env-vars/install.md')])
support=ev(body,'用CANN提供的ATC工具将其转换为昇腾AI处理器能识别的OM模型。')
f['m6']['claims']=[
 dict(source_id='source-0001-rank-1',claim='ONNX可转OM用于昇腾离线模型',claim_evidence=[ev(q1,'本章节主要介绍如何将ONNX模型转化为昇腾AI处理器支持的OM模型')],support_evidence=[support],verdict='supported',independent_crosscheck=True),
 dict(source_id='source-0001-rank-2',claim='该踩坑片段称某问题可由导出时numpy版本大于0.2解决，但问题对象与替代分支未保存完整',claim_evidence=[ev(q1,'那解决这个问题，要么在保留pth模型转换onnx时使用的numpy版本要大于0.2，要么就在Ubantu子系统里把numpy版')],support_evidence=[],verdict='unresolved',independent_crosscheck=False),
 dict(source_id='source-0001-rank-3',claim='ATC将ONNX模型编译为OM文件',claim_evidence=[ev(q1,'ATC将ONNX等模型编译为OM文件')],support_evidence=[support],verdict='supported',independent_crosscheck=True),
 dict(source_id='source-0001-rank-3',claim='模型编译包含图优化；后续算子融字样截断不扩写',claim_evidence=[ev(q1,'包含图优化、算子融')],support_evidence=[],verdict='unsupported',independent_crosscheck=False)]
f['m6']['checked_event_ids']=[s['event_id'] for s in p['sources']]
f['m6']['no_third_party_material']=False
f['m6']['excluded_fragments']=['CSDN安装文章只述作者遇到版本/环境变量问题，无可识别的解决方法断言。']
metric('M6','needs_review',None,'ONNX→OM获官方支持，图优化未获本包明确核对支持；numpy片段的问题对象与后半句未明，适用意义未定。已逐条检查保存来源，保留该具体未决项。', [e for c in f['m6']['claims'] for e in c['claim_evidence']])
metric('M7','needs_review',None,'先验的转换命令和framework=5可由官方正文核对；set_env确切路径以及ACL部署所指接口细节未由固定材料充分确认，尚不能裁决完整正确主流程档位。自报不确定不扣分，未核清不等于已知错误。',[ev('client-note-00005','source /usr/local/Ascend/ascend-toolkit/set_env.sh'),ev('client-note-00005','用 `atc --model=xxx.onnx --framework=5 --output=xxx --soc_version=Ascend310` 转换')])
metric('M8','scored',1,'实际派发3 search+8 fetch=11；预算拦截的第9次fetch不计。',[])
a['metrics']['M8']['event_refs']=[x['id'] for x in p['dispatch_events']]
metric('M9','scored',3,'最终答案列出CANN8.5.0算子包与芯片关系、8.0.0查询方法，但没有ONNX适用版本关系或选定范围；只有部分必要关系具备依据。',[ev('run-end','8.5.0 及之后版本：使用 ATC 转换时**必须安装与目标昇腾 AI 处理器匹配的 ops 算子包**'),ev('run-end','在查询结果的 "Name" 前加 "Ascend" 即为 `<soc_version>` 取值。')])
f['m10']=dict(content_check_complete=True,content_repairs=[],environment_substitutions=['模型路径','input_shape中的输入名和形状','soc_version','实际安装目录'],unresolved=['主路线set_env脚本准确位置和ONNX/CANN适用关系'])
metric('M10','needs_review',None,'转换命令及用户参数有具体说明，但答案明确保留set_env路径未核实，主路线ONNX/CANN适用性也未完整建立；按主路线待核查分支保留null，不以未运行或可选分支缺项判3。',[ev('run-end','此 set_env.sh 步骤基于我的既有知识'),ev('run-end','atc --model=resnet50.onnx --framework=5 --output=resnet50 --input_shape="actual_input_1:1,3,224,224" --soc_version=<soc_version>')])
metric('M11','needs_review',None,'M5/M6/M7必要输入未决，按规则不计算综合点值。',[])
a['metrics']['M11']['derived_from']=[f'M{i}' for i in range(1,9)]
f['task_requirements']={'main':['已有ONNX经环境准备、芯片选择、ATC转换并验证.om输出'],'secondary':['转换约束与部署入口'],'version_relations':['ONNX与CANN/ATC适用关系','目标芯片与转换参数关系']}
for name,obj in [('facts',f),('assessment',a)]: (d/(name+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
(d/'interpretation.md').write_text('# Parent content review\n\nAll three search returns, eight dispatched fetches, the blocked fetch response, prior and final were read. The initial draft incorrectly assigned all official returns body5 and reused a final heading as evidence; those judgments were rejected. M2 is now 27/8 with a wrong-target shell and three title-only returns. Source ownership for cann/docs remains unresolved, unlike explicit hiascend documents. The numpy problem snippet retains its missing referent rather than being weakened into generic ONNX conversion. Claims were not verified with their own text. M7/M10 retain specifically identified environment and compatibility uncertainty, not unperformed scoring. No new collection or hardware execution.\n')
