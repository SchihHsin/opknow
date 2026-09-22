#!/usr/bin/env python3
"""Draw bilingual paper illustrations adapted from the existing design demos.

These are proposed interfaces, not screenshots or new experimental records.
Uses the paper's SVG/ReportLab drawing surface for editable, vector outputs.
"""
from build_paper_figures import Drawing

INK = '#243447'
MUTED = '#586575'
LINE = '#c9d3dc'
PALE = '#f4f7f9'
TEAL = '#21675d'
GREEN = '#eaf3ef'
GOLD = '#895b17'
AMBER = '#fbf2e2'


def choose(lang, cn, en):
    return en if lang == 'en' else cn


def lines(d, x, y, values, size=19, step=27, **kw):
    for i, value in enumerate(values):
        d.text(x, y+i*step, value, size, **kw)


def button(d, x, y, w, label, filled=False):
    d.rect(x, y, w, 39, TEAL if filled else '#ffffff', TEAL, r=5)
    d.text(x+w/2, y+26, label, 18, fill='#ffffff' if filled else TEAL,
           bold=True, anchor='middle')


def window(d, title, lang, height):
    d.rect(12, 12, 976, height-48, '#ffffff', LINE, r=8)
    d.rect(13, 13, 974, 54, PALE, r=7)
    d.text(35, 47, title, 24, bold=True)
    d.text(963, 46, choose(lang, '设计示意', 'Design illustration'), 16,
           fill=MUTED, anchor='end')


def compatibility(lang):
    d = Drawing('figure-6-compatibility-design', 1000, 560, lang,
                'Proposed compatibility lookup based on tasks A and I')
    tr = lambda cn, en: choose(lang, cn, en)
    window(d, tr('版本与配套查询', 'Version and compatibility lookup'), lang, 560)
    d.text(35, 105, tr('1  声明任务环境', '1  Specify the task environment'), 21, bold=True)
    for x, label, value in [(35, tr('目标设备', 'Target device'), tr('选择设备', 'Select device')),
                            (350, tr('框架版本', 'Framework version'), tr('选择已安装版本', 'Select installed version'))]:
        d.text(x, 138, label, 17, fill=MUTED)
        d.rect(x, 150, 285, 43, '#ffffff', LINE, r=4)
        d.text(x+13, 178, value, 19)
        d.line([(x+259, 167), (x+267, 175), (x+275, 167)], MUTED)
    button(d, 676, 151, 286, tr('查找受支持组合', 'Find supported combinations'), True)
    d.text(35, 235, tr('2  比较组合及其依据', '2  Compare combinations and their supporting sources'), 21, bold=True)
    d.text(35, 264, tr('下方仅展示返回字段；不填入未经核实的配套值。',
                      'Result structure shown below; compatibility values are placeholders.'), 17, fill=MUTED)
    d.rect(35, 281, 927, 44, PALE, r=0)
    columns = [(50, tr('工具包', 'Toolkit')), (239, tr('驱动范围', 'Driver range')),
               (425, tr('框架', 'Framework')), (610, tr('集成包', 'Integration package')),
               (817, tr('依据', 'Evidence'))]
    for x, label in columns:
        d.text(x, 309, label, 18, bold=True)
    for i in range(2):
        y=352+i*45
        for x, value in [(50,'<version>'),(239,'<range>'),(425,'<version>'),(610,'<version>')]:
            d.text(x,y,value,18,fill=MUTED)
        d.text(817,y,tr('查看来源', 'Inspect sources'),18,fill=TEAL)
        d.line([(35,y+13),(962,y+13)],LINE,width=1)
    d.rect(35, 435, 927, 65, GREEN, r=5)
    lines(d, 50, 460, [tr('保留每条配套关系的来源、适用范围与验证日期。',
                          'Each relation retains its source, applicability scope, and verification date.'),
                         tr('缺少受支持组合时，说明尚未确定的条件。',
                            'If no supported match is documented, identify the unresolved conditions.')],
          size=18,step=25,fill=TEAL)
    d.text(14,548,tr('案例依据：A / I 的版本资料分散；对应 M4。',
                     'Motivation: fragmented version information in A / I; linked indicator: M4.'),16,fill=MUTED)
    d.save()


def acquisition(lang):
    d = Drawing('figure-9-acquisition-design', 1000, 554, lang,
                'Proposed agent feedback for an unavailable body versus insufficient diagnostic content')
    tr = lambda cn, en: choose(lang, cn, en)
    d.text(15,31,tr('两类知识缺口，两种后续行动', 'Different knowledge gaps call for different next actions'),24,bold=True)
    for x in [15,515]:
        d.rect(x,53,470,455,'#ffffff',LINE,r=7)
        d.rect(x+1,54,468,48,PALE,r=6)
    d.text(31,85,tr('(a) 正文未取得 · 基于任务 D', '(a) Body unavailable · based on task D'),20,bold=True)
    d.text(531,85,tr('(b) 诊断内容不足 · 基于任务 E', '(b) Content insufficient · based on task E'),20,bold=True)
    # The interface wording below is proposed; task conditions come from observations.
    content = [
        (15, [tr('找到相关官方指南', 'Relevant official guide found'),
              tr('返回了导航与元数据', 'Navigation and metadata returned'),
              tr('核心操作指南正文未取得', 'Core how-to body not obtained')],
         tr('缺口：实现步骤缺少官方正文支撑', 'Gap: the core implementation guide is missing'),
         [tr('我已取得相关资料，但尚不能据此', 'I found related material, but cannot verify'),
          tr('核对这份指南中的完整实现过程。', 'the full procedure from this guide.')],
         [tr('我会先查找正文链接或可读来源，', 'I will first look for body links or readable'),
          tr('你也可以按需查看原始指南。', 'sources. You may also inspect the guide.')],
         tr('按需查看原始指南', 'Inspect original guide (optional)')),
        (515,[tr('找到官方 EZ9999 页面', 'Official EZ9999 page found'),
              tr('页面正文已取得', 'Page body obtained'),
              tr('仅有通用诊断建议', 'Only generic diagnostic advice supplied')],
         tr('缺口：无法据此缩小报错原因', 'Gap: the cause cannot yet be narrowed down'),
         [tr('这页未给出具体原因，请补充', 'This page does not identify a specific cause.'),
          tr('触发情境与相关日志片段。', 'Please share the trigger and relevant logs.')],
         [tr('我会结合这些信息查找相关案例，', 'I can use those details to find matching'),
          tr('并建议下一步诊断检查。', 'cases and suggest the next diagnostic check.')],
         tr('补充情境与日志', 'Add context and logs'))]
    for x, states, gap, explanation, action, label in content:
        for i,state in enumerate(states):
            yy=140+i*36
            d.rect(x+17,yy-18,25,25,GREEN if i<2 else AMBER,r=4)
            d.text(x+29,yy,str(i+1),16,bold=True,fill=TEAL if i<2 else GOLD,anchor='middle')
            d.text(x+54,yy,state,18)
        d.rect(x+16,237,438,51,AMBER,r=4)
        d.text(x+29,268,gap,17,bold=True,fill=GOLD)
        lines(d,x+20,319,explanation,18,27)
        lines(d,x+20,389,action,18,27)
        button(d,x+20,447,430,label)
    d.text(15,539,tr('基于任务 D / E 的观察。界面消息为设计示意；对应 M1-M3，重试过程关联 M8。',
                     'Based on observations in D / E. Proposed messages; M1-M3, with retry effort linked to M8.'),16,fill=MUTED)
    d.save()


def verification(lang):
    d = Drawing('figure-11-verification-design',1000,662,lang,
                'Proposed source inspection and corrective feedback for model conversion')
    tr = lambda cn, en: choose(lang, cn, en)
    window(d,tr('核验转换指导', 'Inspect the conversion guidance'),lang,662)
    d.rect(35,85,927,65,PALE,r=5)
    d.text(50,111,tr('当前任务：模型转换', 'Current task: model conversion'),18,bold=True)
    d.text(50,137,tr('回答、来源与本次反馈保持关联',
                    'Keep the response, source passage, and feedback linked'),18,fill=MUTED)
    button(d,754,98,190,tr('查看任务', 'View task'))
    d.text(35,187,tr('回答中的转换命令（节选）', 'Conversion command in the response (excerpt)'),21,bold=True)
    d.rect(35,202,927,45,PALE,r=4)
    d.text(50,231,'atc --model=resnet50.onnx --framework=5 ...',20)
    d.rect(35,264,927,205,'#ffffff',LINE,r=5)
    d.text(50,293,tr('官方快速入门 · CANN 8.0.RC2', 'Official quickstart · CANN 8.0.RC2'),20,bold=True,fill=TEAL)
    d.text(50,323,tr('展开来源段落', 'Expanded source passage'),17,fill=MUTED)
    lines(d,50,353,['atc --model=resnet50.onnx --framework=5 --output=resnet50',
                    '--input_shape="actual_input_1:1,3,224,224" --soc_version=<soc_version>'],
          size=18,step=27)
    d.text(50,415,tr('来源入口：官方模型转换快速入门', 'Source entry: official model-conversion quickstart'),17,fill=MUTED)
    d.text(50,449,tr('前往原始页面', 'Open the original page'),18,bold=True,fill=TEAL)
    d.rect(35,486,927,57,AMBER,r=5)
    lines(d,50,510,[tr('这条指导与你观察到的情况不一致？',
                      'Does this guidance differ from what you observed?'),
                     tr('关联本条命令提交报错或修正，保留原来源与任务环境。',
                        'Attach an error or correction to this command, retaining its source and task context.')],size=17,step=23,fill=GOLD)
    d.text(35,570,tr('下一轮检查将同时使用原建议与新增反馈。',
                    'The next check uses both the original suggestion and the new feedback.'),18)
    button(d,35,582,300,tr('添加报错或修正', 'Add error or correction'))
    d.text(14,650,tr('命令节选来自任务 A 中取得的快速入门；界面交互为示意。对应 M4、M9、M10。',
                     'Command from the quickstart acquired in A; proposed interaction. Linked to M4, M9, M10.'),16,fill=MUTED)
    d.save()


def diagnostic(lang):
    tr=lambda cn,en:choose(lang,cn,en)
    d=Drawing('figure-7-diagnostic-content-design',1000,590,lang,
              'Proposed task-oriented diagnostic content based on the generic error page in E')
    window(d,tr('EZ9999：诊断资料的组织方式','EZ9999: organizing diagnostic guidance'),lang,590)
    d.text(35,98,tr('任务 E 中观察到：已有专属错误页，原因与处理建议泛化。',
                    'Observed in task E: a dedicated error page with generic diagnostic advice.'),18,fill=MUTED)
    d.rect(35,116,927,64,AMBER,r=5)
    lines(d,50,141,[tr('诊断起点：错误码本身不足以确定具体原因。',
                      'Starting point: the error code alone does not identify a specific cause.'),
                     tr('适用范围：<版本 / 组件>    更新依据：<来源 / 日期>',
                        'Applies to: <version / component>    Updated from: <source / date>')],18,26,fill=GOLD)
    d.text(35,219,tr('1  明确需要收集的现场信息','1  Identify the local information needed'),21,bold=True)
    lines(d,50,251,[tr('报错前后的日志、触发操作、相关组件与实际版本。',
                      'Logs around the error, the triggering operation, components, and installed versions.'),
                     tr('标明每项信息用于区分哪类情境。',
                        'Explain which diagnostic distinction each item helps resolve.')],18,26)
    d.text(35,317,tr('2  按可观察现象组织排查路径','2  Organize investigation around observable symptoms'),21,bold=True)
    d.rect(35,335,927,42,PALE,r=0)
    for x,s in [(50,tr('现象 / 条件','Symptom / condition')),(345,tr('下一步检查','Next check')),(648,tr('案例与适用依据','Case and applicability evidence'))]:
        d.text(x,363,s,18,bold=True)
    for x,s in [(50,tr('<日志特征 / 触发情境>','<log pattern / trigger>')),(345,tr('<检查步骤与预期观测>','<check and expected observation>')),(648,tr('<案例链接 / 版本 / 来源>','<case link / version / source>'))]:
        d.text(x,407,s,17,fill=MUTED)
    d.line([(35,425),(962,425)],LINE,width=1)
    d.text(35,463,tr('3  保留未解决分支与后续支持入口','3  Retain unresolved branches and a support route'),21,bold=True)
    d.text(50,496,tr('未能定位时，说明还缺哪些证据，并带上已有记录继续求助。',
                    'If the cause remains unresolved, identify missing evidence and carry the record into support.'),18)
    d.text(14,578,tr('示例依据：E；对应 M3、M4。排查结构为建议，案例字段为占位。',
                     'Motivation: E; M3, M4. Proposed diagnostic structure with placeholder case fields.'),16,fill=MUTED)
    d.save()


def readable_export(lang):
    tr=lambda cn,en:choose(lang,cn,en)
    d=Drawing('figure-8-readable-export-design',1000,555,lang,
              'Proposed document content and machine-readable export preserving the same task relations')
    d.text(15,31,tr('同一任务资料，保留关系的两种出口',
                    'Two views of task material, preserving the same relationships'),24,bold=True)
    for x,w in [(15,444),(540,444)]:
        d.rect(x,55,w,442,'#ffffff',LINE,r=7)
        d.rect(x+1,56,w-2,45,PALE,r=6)
    d.text(32,85,tr('文档正文：转换快速入门','Document body: conversion quickstart'),20,bold=True)
    d.text(557,85,tr('机器可读视图：结构化文本','Machine-readable view: structured text'),20,bold=True)
    d.text(32,134,tr('适用范围与来源身份','Applicability and source identity'),19,bold=True,fill=TEAL)
    d.text(32,164,tr('CANN 8.0.RC2 · 官方快速入门','CANN 8.0.RC2 · official quickstart'),18)
    d.text(32,209,tr('命令（节选）','Command (excerpt)'),19,bold=True)
    lines(d,32,240,['atc --model=resnet50.onnx','--framework=5 ...'],18,27)
    d.text(32,311,tr('参数与关联说明','Parameters and their instructions'),19,bold=True)
    lines(d,32,342,['--input_shape',tr('输入名称与形状','Input name and shape'),'--soc_version',tr('关联设备信息查询步骤','Linked device-information step')],18,30)
    d.line([(469,269),(528,269)],TEAL,arrow=True,width=2)
    lines(d,557,134,['task: model conversion','version: CANN 8.0.RC2','source: official quickstart','command: atc ...','parameters:','  input_shape: <name and shape>','  soc_version: <target value>','related_step: npu-smi info','reference: <original entry>'],18,34)
    d.text(557,466,tr('入口：文本导出 / 结构化接口','Access: text export / structured endpoint'),17,fill=TEAL)
    d.text(15,533,tr('结构示意；命令与参数依据 A。导出应保留正文、版本及引用关系，对应 M2-M4。',
                     'Proposed structure; command and parameters from A. Preserve body, version, and links; M2-M4.'),16,fill=MUTED)
    d.save()


def environment(lang):
    tr=lambda cn,en:choose(lang,cn,en)
    d=Drawing('figure-10-environment-design',1000,506,lang,
              'Proposed environment declaration and explicit version comparison before recommending commands')
    window(d,tr('先明确环境，再核对建议','Declare the environment and check applicability'),lang,506)
    d.text(35,105,tr('当前任务的环境记录','Environment recorded for this task'),21,bold=True)
    for x,label,value in [(35,tr('设备型号','Device model'),'<device>'),(349,tr('工具包版本','Toolkit version'),'<local version>'),(663,tr('框架与集成包','Framework and integration'),'<local versions>')]:
        d.text(x,140,label,18,fill=MUTED);d.rect(x,154,297,42,PALE,LINE,r=4);d.text(x+12,183,value,18)
    d.text(35,231,tr('来源材料的适用范围','Applicability stated by the source'),21,bold=True)
    d.text(50,263,tr('版本 / 组件 / 兼容条件：由引用材料提供','Version / component / compatibility conditions: taken from the cited material'),18)
    d.rect(35,282,927,81,AMBER,r=5)
    lines(d,50,309,[tr('当前状态：尚未完成环境匹配','Current state: environment match not yet established'),
                     tr('请补充缺失版本；已知不匹配的材料不直接用于当前命令建议。',
                        'Supply missing versions; known mismatches should not directly support the proposed command.')],18,28,fill=GOLD)
    d.text(35,402,tr('核对结果可分别记录：匹配 / 不匹配 / 信息不足。',
                    'Record the check as matched, mismatched, or insufficient information.'),18)
    button(d,35,419,314,tr('更新任务环境','Update task environment'))
    d.text(14,494,tr('依据 A / I 的版本条件；字段为示意。来源范围与本机事实分别记录，关联 M4、M9。',
                     'Motivated by A / I; illustrative fields. Separate source scope from local facts; M4, M9.'),16,fill=MUTED)
    d.save()


if __name__ == '__main__':
    for language in ['en','cn']:
        compatibility(language)
        diagnostic(language)
        readable_export(language)
        acquisition(language)
        environment(language)
        verification(language)
    print('Built six bilingual design illustrations and English vector PDFs.')
