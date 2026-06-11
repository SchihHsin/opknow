#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 score_metrics.py 的 RAW + 复算结果，生成 17/index 的 I–Z 行 JS（ROWS/TASKOVER/SRC_MIX）。
所有 tooltip 文本均由 RAW 实测观测派生，不杜撰标题/URL；srcs 仅用真实 platform+date。
SRC_MIX 五段为公式派生的回顾性估计（off/sec/own 按 K 分配、剩余按受阻形态分 extra/gap）。"""
import score_metrics as sm

NAMES = {
 "I":"版本兼容排查","J":"安装与环境变量","K":"容器 / 镜像搭建","L":"算子精度排查",
 "M":"动态 shape / Tiling","N":"算子融合","O":"注册与框架集成","P":"混合精度训练",
 "Q":"显存 / OOM 优化","R":"精度 / 收敛排查","S":"推理服务部署","T":"动态 batch / shape 推理",
 "U":"访存 / occupancy 优化","V":"计算与传输重叠","W":"多卡通信优化","X":"内存越界定位",
 "Y":"跨芯片迁移","Z":"概念心智模型对照",
}
# 配对问句（简述，本质相同仅换栈）
QPAIR = {
 "I":"CUDA/cuDNN/驱动版本匹配 ｜ CANN×torch_npu×固件版本匹配",
 "J":"CUDA Toolkit 安装+PATH/LD_LIBRARY ｜ CANN 安装+ASCEND 环境变量",
 "K":"NGC CUDA 镜像 ｜ Ascend 容器镜像 + Ascend Docker Runtime",
 "L":"算子数值精度对齐排查 ｜ Ascend C 算子精度比对(msaccucmp)",
 "M":"TensorRT 动态 shape profile ｜ Ascend C Tiling/动态 shape",
 "N":"TensorRT/torch.compile 融合 ｜ 昇腾图融合/算子融合",
 "O":"torch 自定义算子注册框架集成 ｜ aclnn/Ascend C 注册接框架",
 "P":"AMP autocast/GradScaler ｜ 昇腾 AMP/apex 混合精度",
 "Q":"CUDA OOM 显存优化 ｜ 昇腾 NPU 显存/OOM 优化",
 "R":"训练不收敛/精度排查 ｜ 昇腾训练精度/收敛排查",
 "S":"Triton 推理服务部署 ｜ MindIE 推理服务部署",
 "T":"TensorRT 动态 batch ｜ ATC dynamic_batch/ais_bench 动态推理",
 "U":"Nsight 访存/occupancy 优化 ｜ Ascend C double-buffer/访存优化",
 "V":"CUDA streams 计算传输重叠 ｜ aclrtMemcpyAsync 计算传输重叠",
 "W":"NCCL 多卡通信调优 ｜ HCCL 多卡通信调优",
 "X":"compute-sanitizer 内存越界定位 ｜ msSanitizer 内存越界定位",
 "Y":"跨 GPU 架构迁移(-arch/PTX) ｜ 跨昇腾芯片迁移(soc_version)",
 "Z":"CUDA 线程/内存层级心智模型 ｜ Ascend C SPMD/UB/GM 心智模型",
}
LETTERS = list("IJKLMNOPQRSTUVWXYZ")
SC = sm.compute()

def vcls(s): return 'v%d' % s
def esc(t): return t.replace('\\','\\\\').replace("'","\\'")

def core_fetch_txt(cf):
    return {
     "static":"官方静态站，web_fetch 正文可直接抓取。",
     "ssr":"官方页服务端渲染、正文可抓（实测非 SPA）。",
     "partial":"<code>/document/detail</code> 子树 SPA，但 <code>/doc_center</code> 镜像兜住正文 → 部分可抓。",
     "spa":"官方页 SPA，正文（参数表/命令/代码）抽不到。",
     "robots":"robots 拦截，无法抓取。",
    }[cf]

def ref_txt(rl, exec_ok):
    base = {
     "exhaustive":"抓到正文穷尽（参数表/命令/代码齐全）。",
     "core_only":"抓到核心机制，但非端到端穷尽走查。",
     "overview":"仅抓到概述/概念，缺落地命令。",
     "fragment":"仅抓到片段。",
     "none":"正文无有效内容。",
    }[rl]
    return base + ("可执行验证。" if exec_ok else "")

def disc_txt(r):
    rk, rd, rf = r["rank"], r["rounds"], r["refine"]
    t = f"{rd} 轮检索、官方命中名次 rank={rk}"
    if rf: t += "；官方排不到首屏、靠二搜关键词定位（refine）"
    return t + "。"

def ver_txt(r):
    n = r["n_versions"]; t = f"检索中并存版本号 {n} 个"
    if r["ver_irrelev"]: t += "，但概念与版本基本无关"
    if r["two_axis"]: t += "，且跨双轴（CANN 版 × 插件/芯片）"
    if r["ver_matrix"]: t += "，官方给出版本矩阵、可对照"
    return t + "。"

def sec_srcs(r):
    out = []
    srcs, plats, dates = r["sources"], r["platforms"], r["dates"]
    for i in range(len(srcs)):
        plat = plats[i] if i < len(plats) else srcs[i]
        dt = dates[i] if i < len(dates) and dates[i] else ' '
        out.append([plat, '', dt, ''])
    return out

CRED = {"official_doc":5.0,"official_repo":5.0,"official_forum":4.5,"cloud_vendor":4.0,
        "arxiv":4.0,"qa_reputation":3.5,"tech_blog":3.0,"aggregator":2.5}
def sec6_txt(r):
    types = r["sources"]
    avg = sum(CRED.get(t,3.0) for t in types)/max(1,len(types))
    return f"按来源类型可信度均分≈{avg:.1f} + 一致性 {r['consist']}；来源类型 {','.join(types)}。"

def own_txt(r):
    t = f"自带知识自评 {r['own']}/5"
    ch = r["churn"]
    if ch=="fast": t += "；该领域迭代快(fast)，训练知识易落后 −0.5"
    elif ch=="moderate": t += "；迭代中(moderate) −0.25"
    return t + "。"

def cost_txt(r):
    c = r["rounds"] + 0.5*r["fetch"] + 4*r["fetch_fail"]
    t = f"成本 = 轮数{r['rounds']} + 0.5×抓取{r['fetch']}"
    if r["fetch_fail"]: t += f" + 4×抓取失败{r['fetch_fail']}"
    return t + f" = {c:g}。"

def pin_txt(p):
    return {"exact":"可锁定到确切版本。","mostly":"大体可锁、个别取值依芯片/版本。",
            "range":"只能锁到版本区间。","none":"概念/无版本可锁。"}[p]
def repro_txt(p):
    return {"copyrun":"命令可直接照抄运行。","params":"主命令可抄、部分参数依环境。",
            "partial":"骨架可述、细节需查证。","skeleton":"仅能给思路骨架。"}[p]

def cost_label(r):
    s = f"{r['rounds']}搜·{r['fetch']}抓"
    if r["fetch_fail"]: s += "✗"
    return s

def cell_js(c, d, t, extra_js=''):
    return f"N('{c}','{esc(d)}','{esc(t)}'{extra_js})"

def srcs_js(srcs):
    if not srcs: return ''
    inner = ','.join('['+','.join("'"+esc(str(x))+"'" for x in s)+']' for s in srcs)
    return ',{srcs:['+inner+']}'

def stack_cells(r, sc):
    s = sc["scores"]
    cells = []
    # ① discover
    cells.append(cell_js(vcls(s[0]), str(s[0]), disc_txt(r), srcs_js(sec_srcs(r)) if False else ''))
    # ② fetch
    cells.append(cell_js(vcls(s[1]), str(s[1]), core_fetch_txt(r["core_fetch"])))
    # ③ detail
    cells.append(cell_js(vcls(s[2]), str(s[2]), ref_txt(r["ref_level"], r["exec"])))
    # ④ version
    cells.append(cell_js(vcls(s[3]), str(s[3]), ver_txt(r)))
    # ⑤ secondary (with srcs)
    cells.append(cell_js(vcls(s[4]), str(s[4]), f"二手 {len(r['sources'])} 条（官方一手已剔除、不计二手）。"+("" ), srcs_js(sec_srcs(r))))
    # ⑥ credibility
    cells.append(cell_js(vcls(s[5]), str(s[5]), sec6_txt(r)))
    # ⑦ own
    cells.append(cell_js(vcls(s[6]), str(s[6]), own_txt(r)))
    # ⑧ cost (reverse)
    cells.append(cell_js(vcls(s[7]), cost_label(r), cost_txt(r)))
    # ⑨ pin
    cells.append(cell_js(vcls(s[8]), str(s[8]), pin_txt(r["pin"])))
    # ⑩ repro
    cells.append(cell_js(vcls(s[9]), str(s[9]), repro_txt(r["repro"])))
    # ⑪ overall
    band = sc["band"]; bcls = 'v%d' % sc["band_n"]
    cells.append(cell_js(bcls, band, f"综合置信度公式复算 = {sc['overall']:.2f} → {band}（由①–⑧ 实时代入，见下方推导）。"))
    return "[\n   "+",\n   ".join(cells)+"]"

def rows_js():
    out = []
    for L in LETTERS:
        cu = stack_cells(sm.RAW[L]["cuda"], SC[L]["cuda"])
        ca = stack_cells(sm.RAW[L]["cann"], SC[L]["cann"])
        out.append(f" {L}:{{name:'{NAMES[L]}',\n  cuda:{cu},\n  cann:{ca}}}")
    return ",\n".join(out)

def taskover_js():
    out = []
    for L in LETTERS:
        cu = SC[L]["cuda"]["band"]; ca = SC[L]["cann"]["band"]
        ca_sc = SC[L]["cann"]["overall"]
        r = sm.RAW[L]["cann"]
        # 一句话研判，从 CANN 短板派生
        bits = []
        if r["core_fetch"] in ("spa","robots"): bits.append("官方正文受阻")
        elif r["core_fetch"]=="partial": bits.append("官方 detail 子树 SPA、镜像兜底")
        else: bits.append("官方页 ssr 可抓")
        if r["ref_level"] in ("overview","fragment","none"): bits.append("正文偏概述")
        if r["n_versions"]>=3: bits.append(f"版本散乱({r['n_versions']})")
        if len(r["sources"])<=2: bits.append("二手薄")
        if r["own"]<=2: bits.append("自带知识弱")
        v = f"公式复算 {ca_sc:.2f}→{ca}。" + "；".join(bits) + "。"
        out.append(f" {L}:{{q:'{esc(QPAIR[L])}',cu:'{cu}',ca:'{ca}',v:'{esc(v)}'}}")
    return ",\n".join(out)

def srcmix_js():
    out = []
    for L in LETTERS:
        seg = {}
        for st in ("cuda","cann"):
            x = SC[L][st]["mid"]; r = sm.RAW[L][st]
            OFF, SEC, OWN, K = x["OFF"], x["SEC"], x["OWN"], x["K"]
            avail = round(K*100)
            tot = OFF+SEC+OWN or 1e-9
            off = round(avail*OFF/tot); sec = round(avail*SEC/tot); own = avail-off-sec
            rem = 100-avail
            cf = r["core_fetch"]
            gfrac = 0.6 if cf in ("spa","robots") else 0.4 if cf=="partial" else 0.15
            if r["ref_level"] in ("overview","fragment","none"): gfrac += 0.15
            gap = round(rem*min(gfrac,0.8)); extra = rem-gap
            note = (f"公式派生估计：官方渠道 OFF={OFF:.2f}、二手 SEC={SEC:.2f}、自带 OWN={OWN:.2f} → "
                    f"有把握来源≈K={K*100:.0f}%；剩余按"
                    + ("受阻/SPA" if cf in("spa","robots","partial") else "正文可抓")
                    + "形态分入类比外推与留白。")
            seg[st] = (off,sec,own,extra,gap,note)
        cu=seg["cuda"]; ca=seg["cann"]
        out.append(
         f" {L}:{{cuda:{{m:[{cu[0]},{cu[1]},{cu[2]},{cu[3]},{cu[4]}],n:'{esc(cu[5])}'}},\n"
         f"    cann:{{m:[{ca[0]},{ca[1]},{ca[2]},{ca[3]},{ca[4]}],n:'{esc(ca[5])}'}}}}")
    return ",\n".join(out)

if __name__ == "__main__":
    import sys
    what = sys.argv[1] if len(sys.argv)>1 else "rows"
    print({"rows":rows_js,"taskover":taskover_js,"srcmix":srcmix_js}[what]())
