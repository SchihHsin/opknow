#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
score_metrics.py — 「AI 可用性」11 项指标的量化打分管线
==========================================================

目的：把原先靠「主观研判」打的 ①–⑩ 分，换成**可复现的公式**——
每个指标一个 score_N() 函数，输入是从 task_run_log.md 实测得到的
**可量化原始观测**（检索轮数、命中排名、抓到的正文构件、并存版本号个数、
每条二手来源的可信度评分……），输出 1–5（⑧反向；⑪由①–⑧噪声-OR汇总）。

运行：  python3 score_metrics.py            # 打印全矩阵
       python3 score_metrics.py --diff     # 额外打印与旧手评的差异
       python3 score_metrics.py --json      # 输出 JSON（供 HTML 落库）

设计原则
--------
1. 原始数据只来自真跑记录（task_run_log.md）；绝不为凑分而编。
2. 凡天然是判断的输入（⑦自带知识、⑥一致性档），用**显式子档表**量化、注明是自评。
3. ⑨⑩是产出/因变量，照打分但**不进⑪**（进了=重复加权）。
4. 受阻（SPA 抓不到正文）记 BLOCKED，归一时按 0，且**不等于给③打1分**。
"""

import sys, json

BLK = "受阻"   # 受阻态（③ 在官方 SPA 抓不到正文时）

# ============================================================
# 0. 二手来源可信度评分表（回答「每条来源可信度多少、怎么算」）
#    按来源**类型**定基准分；ⓘ 这是一张可复核的锚定表，不是逐条拍脑袋。
# ============================================================
SOURCE_CRED = {
    "official_doc":   5.0,  # 一手官方文档镜像（docs.nvidia.com / hiascend）
    "official_repo":  5.0,  # 官方代码仓（github.com/pytorch、gitee ascend 蓝区仓）
    "official_forum": 4.5,  # 官方论坛/邮件列表（dev-discuss.pytorch.org、NVIDIA 论坛）
    "cloud_vendor":   4.0,  # 大厂云技术博客（aliyun developer、华为云 bbs）
    "arxiv":          4.0,  # 学术论文
    "qa_reputation":  3.5,  # 有声誉的问答/专栏（zhihu 专栏、StackOverflow）
    "tech_blog":      3.0,  # CSDN / 博客园 / Medium 个人技术博客
    "aggregator":     2.5,  # 聚合站/科普号（ai6s、53ai、天翼云转载）
}
# 一致性因子：各源对「命令/版本/写法」是否对得上。high=互证、mid=深度参差、low=彼此矛盾
CONSIST = {"high": +1.0, "mid": 0.0, "low": -1.0}

# ------------------------------------------------------------
# 时效性（recency）—— ⑥ 二手可信度的「只罚不奖」修正项
#   设计取舍：① 够新是基线、不是加分（给加分会把临界格虚高地推过整数档）；
#            ② 过时才是缺陷、扣分；③ 阈值按二手来源**发表日期中位数**的月龄。
#   today 固定为 (2026,6) 与 task_run_log 真跑日同月，便于复算。
#   各源真实发表日期由 web_search 实测取得，None=未拿到确切日期(诚实留空、不参与中位)。
# ------------------------------------------------------------
TODAY = (2026, 6)

def _age_months(ym, today=TODAY):
    y, m = int(ym[:4]), int(ym[5:7])
    return (today[0] - y) * 12 + (today[1] - m)

def recency_factor(dates, today=TODAY):
    """二手来源发表日期中位月龄 → ⑥ 罚分。≤36mo 不罚、≤48mo −0.25、>48mo −0.5。
       dates 为 'YYYY-MM' 串列表；None/空跳过；全空→0(无据不罚)。"""
    ages = sorted(_age_months(d, today) for d in dates if d)
    if not ages:
        return 0.0
    n = len(ages)
    med = ages[n // 2] if n % 2 else (ages[n // 2 - 1] + ages[n // 2]) / 2
    if med <= 36:  return 0.0
    if med <= 48:  return -0.25
    return -0.5

# ------------------------------------------------------------
# 因子 B：来源独立性 / 平台多样性 —— ⑥ 二手可信度的「只罚不奖」修正项
#   动机：3 条来源若全挤在一个平台(CSDN×2…)、彼此互抄，则「一致性 high」
#         可能只是回声、并非独立互证；真实覆盖被高估。
#   量化：去重平台域名数 / 来源总数 = 独立度 indep。
#         indep≥0.8 不罚 / ≥0.6 −0.25 / <0.6 −0.5（只罚不奖：多样是基线）。
#   platforms = 每条二手来源的平台/域名 token 列表（与 sources 一一对应）。
# ------------------------------------------------------------
def independence_factor(platforms):
    if not platforms:
        return 0.0
    indep = len(set(platforms)) / len(platforms)
    if indep >= 0.8:  return 0.0
    if indep >= 0.6:  return -0.25
    return -0.5

# ------------------------------------------------------------
# 因子 A：知识截止 gap —— ⑦ 模型自带知识的「只罚不奖」修正项
#   动机：⑦ 原是全 11 项里唯一纯自评、无客观锚。技术迭代越快，
#         我的训练知识越可能落后于最新版本(知识截止 gap 越大)。
#   量化：按该任务相关工具/API 的迭代节奏 churn 给罚分——
#         stable(API 早已稳定、知识可靠) 0 / moderate −0.25 / fast(alpha/RC 高频刷新) −0.5。
#   churn 由 task_run_log 观测的版本扩散 + 各生态公开发布节奏判定(非纯主观自评)。
# ------------------------------------------------------------
CHURN = {"stable": 0.0, "moderate": -0.25, "fast": -0.5}

def cutoff_gap_factor(churn):
    return CHURN[churn]


# ============================================================
# 1. 原始观测数据（每格 = 一个任务×一个栈；字段全部来自 task_run_log.md 实测）
# ============================================================
# 字段说明：
#  rounds        检索轮数（web_search 次数）
#  rank          首条官方结果在 SERP 的大致名次（1=首条；越大越靠后）
#  refine        是否需要换关键词二次检索才浮出官方源
#  fetch         web_fetch 次数
#  fetch_fail    web_fetch 抓取失败次数（SPA 抓空）
#  core_fetch    核心 how-to 页抓取形态：static/ssr/partial/spa/robots
#  exec          官方正文是否含可执行核心（命令或可跑代码）
#  ref_level     正文参考完整度：exhaustive / core_only / overview / fragment / none
#  n_versions    检索中并存的版本号个数（去重）
#  ver_matrix    官方是否给出清晰支持矩阵
#  ver_irrelev   该任务是否本质与版本无关（选型类）
#  two_axis      是否需同时定「芯片+框架」两轴但可锁
#  sources       二手来源类型清单（用于 ⑤数量 与 ⑥可信度）
#  platforms     每条二手来源的平台/域名 token（与 sources 一一对应；因子 B 算独立性）
#  dates         每条二手来源发表月份 'YYYY-MM'（None=未拿到确切日；⑥时效罚分用）
#  consist       二手一致性档：high/mid/low
#  own           ⑦自带知识自评档 1–5（唯一显式自评项，注明）
#  churn         相关工具/API 迭代节奏：stable/moderate/fast（因子 A 算知识截止 gap）
#  pin           版本可锁定性：exact / range / none
#  repro         步骤可复现性：copyrun / minor_fix / skeleton / sketch
# ⚠ sources 只列**真正的二手**（非一手）：官方文档/官方代码仓(github.com/pytorch、
#   gitee.com/ascend 蓝区仓)/官方论坛属①官方渠道，**不计入二手**，避免与①重复加权。
RAW = {
 "A": {
  "cuda": dict(rounds=1, rank=1, refine=False, fetch=1, fetch_fail=0,
     core_fetch="static", exec=True, ref_level="exhaustive",
     n_versions=2, ver_matrix=True, ver_irrelev=False, two_axis=False,
     # learnopencv / towardsdatascience / medium / github-sithu(个人仓) / seeed-wiki
     sources=["tech_blog","tech_blog","tech_blog","tech_blog","aggregator"],
     platforms=["learnopencv","towardsdatascience","medium","github","seeed"],
     # learnopencv 2023-01-24（PyTorch→TensorRT），余无确切发表日
     dates=["2023-01", None, None, None, None],
     consist="high", own=4, churn="moderate", pin="exact", repro="copyrun"),
  "cann": dict(rounds=1, rank=4, refine=False, fetch=3, fetch_fail=0,
     core_fetch="ssr", exec=True, ref_level="core_only",
     n_versions=5, ver_matrix=False, ver_irrelev=False, two_axis=False,
     # zhihu / aliyun / cnblogs×2 / csdn
     sources=["qa_reputation","cloud_vendor","tech_blog","tech_blog","tech_blog"],
     platforms=["zhihu","aliyun","cnblogs","cnblogs","csdn"],
     # aliyun 1662723 2025-05-06、racesnail 飞桨x昇腾 2025-05；zhihu p/393169777 引 EOL 旧版无确切日
     dates=[None, "2025-05", "2025-05", None, None],
     consist="high", own=3, churn="moderate", pin="range", repro="params"),
 },
 "B": {
  "cuda": dict(rounds=1, rank=3, refine=False, fetch=1, fetch_fail=0,
     core_fetch="static", exec=True, ref_level="exhaustive",
     n_versions=2, ver_matrix=True, ver_irrelev=False, two_axis=False,
     # mcarilli-gist / medium-Yuanzhe / harvard-handbook / practical-ml-arikpoz / aceCloud
     sources=["tech_blog","tech_blog","cloud_vendor","tech_blog","tech_blog"],
     platforms=["github","medium","harvard","practical-ml","acecloud"],
     # medium Yuanzhe Dong nsys 2022-07-07、practical-ml arikpoz 2025-05-25、AceCloud ~2026-01
     dates=[None, "2022-07", None, "2025-05", "2026-01"],
     consist="high", own=4, churn="stable", pin="mostly", repro="copyrun"),
  "cann": dict(rounds=1, rank=4, refine=False, fetch=2, fetch_fail=0,
     core_fetch="ssr", exec=True, ref_level="core_only",
     n_versions=6, ver_matrix=False, ver_irrelev=False, two_axis=False,
     # aliyun / csdn×2 / zhihu
     sources=["cloud_vendor","tech_blog","tech_blog","qa_reputation"],
     platforms=["aliyun","csdn","csdn","zhihu"],
     # CSDN msprof 2025-06，余无确切日
     dates=[None, "2025-06", None, None],
     consist="mid", own=3, churn="moderate", pin="range", repro="partial"),
 },
 "C": {
  "cuda": dict(rounds=1, rank=1, refine=False, fetch=1, fetch_fail=0,
     core_fetch="static", exec=True, ref_level="exhaustive",
     n_versions=1, ver_matrix=True, ver_irrelev=True, two_axis=False,
     # siboehm / abhik.ai / toolscope / matlab-gpucoder / medium / 53ai
     sources=["tech_blog","tech_blog","aggregator","cloud_vendor","tech_blog","aggregator"],
     platforms=["siboehm","abhik","toolscope","mathworks","medium","53ai"],
     # siboehm CUDA-MMM 2022-12-31，余无确切日
     dates=["2022-12", None, None, None, None, None],
     consist="high", own=5, churn="stable", pin="exact", repro="copyrun"),
  "cann": dict(rounds=1, rank=4, refine=False, fetch=1, fetch_fail=0,
     core_fetch="partial", exec=False, ref_level="overview",
     n_versions=2, ver_matrix=False, ver_irrelev=False, two_axis=False,
     # csdn / zhihu / 华为云bbs （Gitee 蓝区仓属官方、不计二手）
     sources=["tech_blog","qa_reputation","cloud_vendor"],
     platforms=["csdn","zhihu","huaweicloud"],
     # 53ai AOL/ATB 2024-07-18、arxiv 2506.12708 2025-06
     dates=["2024-07", "2025-06", None],
     consist="high", own=3, churn="moderate", pin="mostly", repro="params"),
 },
 "D": {
  "cuda": dict(rounds=1, rank=1, refine=False, fetch=1, fetch_fail=0,
     core_fetch="static", exec=True, ref_level="exhaustive",
     n_versions=2, ver_matrix=False, ver_irrelev=False, two_axis=True,
     # apxml课程 / 个人博客×2 / medium / learn-blog （pytorch/extension-cpp 属官方仓）
     sources=["aggregator","tech_blog","tech_blog","tech_blog","tech_blog"],
     platforms=["apxml","blog-a","blog-b","medium","learn-blog"],
     # 二手均无确切发表日（pytorch 官方教程属①、不计二手）
     dates=[None, None, None, None, None],
     consist="high", own=5, churn="moderate", pin="exact", repro="copyrun"),
  "cann": dict(rounds=2, rank=8, refine=True, fetch=1, fetch_fail=1,
     core_fetch="spa", exec=None, ref_level="none",
     n_versions=3, ver_matrix=False, ver_irrelev=False, two_axis=False,
     # csdn / ai6s / cnblogs （MindSpore官方doc 属官方、不计二手）
     sources=["tech_blog","aggregator","tech_blog"],
     platforms=["csdn","ai6s","cnblogs"],
     # CSDN xyz3120 2024-11-09、ai6s 2025-12-05、ZOMI cnblogs 2024-11-21
     dates=["2024-11", "2025-12", "2024-11"],
     consist="low", own=2, churn="fast", pin="none", repro="partial"),
 },
 # ── 第二批真跑（2026-06-10）：E/F/G/H 四任务 ──────────────────
 "E": {  # 报错码 / 异常排查（调试类，版本敏感 中）
  "cuda": dict(rounds=1, rank=2, refine=False, fetch=1, fetch_fail=0,
     core_fetch="static", exec=True, ref_level="exhaustive",
     n_versions=1, ver_matrix=False, ver_irrelev=False, two_axis=False,
     # StackOverflow / vLLM 博客 / medium / towardsdatascience / 调试科普
     #（NVIDIA 论坛=官方论坛①、pytorch issues=官方仓①，均不计二手）
     sources=["qa_reputation","tech_blog","tech_blog","tech_blog","aggregator"],
     platforms=["stackoverflow","vllm-blog","medium","tds","aggr"],
     dates=[None, "2025-08", None, None, None],
     consist="high", own=4, churn="stable", pin="mostly", repro="copyrun"),
  "cann": dict(rounds=2, rank=3, refine=False, fetch=1, fetch_fail=0,
     # 官方 EZ9999 页可抓(ssr)但泛化兜底(Inner Error/cause N/A)→正文骨架化(fragment)
     core_fetch="ssr", exec=False, ref_level="fragment",
     n_versions=3, ver_matrix=False, ver_irrelev=False, two_axis=False,
     # CSDN×2 / 知乎（MindSpore 教程=官方doc①、vllm-ascend issues=官方仓①，不计二手）
     sources=["tech_blog","tech_blog","qa_reputation"],
     platforms=["csdn","csdn","zhihu"],
     dates=["2024-12", "2025-03", None],
     consist="mid", own=2, churn="moderate", pin="range", repro="partial"),
 },
 "F": {  # 分布式训练 HCCL（训练类，版本敏感 中）
  "cuda": dict(rounds=1, rank=1, refine=False, fetch=1, fetch_fail=0,
     core_fetch="static", exec=True, ref_level="exhaustive",
     n_versions=2, ver_matrix=False, ver_irrelev=False, two_axis=False,
     # medium / StackOverflow / 训练博客 / lambda labs（pytorch tutorials+examples=官方①）
     sources=["tech_blog","qa_reputation","tech_blog","cloud_vendor"],
     platforms=["medium","stackoverflow","blog","lambda"],
     dates=[None, None, None, None],
     consist="high", own=4, churn="stable", pin="mostly", repro="copyrun"),
  "cann": dict(rounds=1, rank=3, refine=False, fetch=1, fetch_fail=0,
     # 官方 PT_LMTMOG_0024 可抓且详尽：hccl init_process_group+DDP+5种拉起+hccn_tool
     core_fetch="ssr", exec=True, ref_level="core_only",
     n_versions=3, ver_matrix=False, ver_irrelev=False, two_axis=False,
     # CSDN×3 / 知乎（torchtitan-npu 社区仓计二手不在此、归官方风格外；此处只列真二手）
     sources=["tech_blog","tech_blog","tech_blog","qa_reputation"],
     platforms=["csdn","csdn","csdn","zhihu"],
     dates=["2025-06", None, None, None],
     consist="mid", own=3, churn="moderate", pin="range", repro="partial"),
 },
 "G": {  # CUDA→昇腾迁移（迁移类，版本敏感 高）
  "cuda": dict(rounds=1, rank=1, refine=False, fetch=1, fetch_fail=0,
     # CUDA→ROCm/HIP 移植类比（同栈无关、跨平台迁移的对照）
     core_fetch="static", exec=True, ref_level="exhaustive",
     n_versions=2, ver_matrix=False, ver_irrelev=False, two_axis=False,
     # hipify_torch 社区仓 / medium / SO / 博客（rocm.docs.amd.com=官方doc①）
     sources=["tech_blog","tech_blog","qa_reputation","tech_blog"],
     platforms=["github","medium","stackoverflow","blog"],
     dates=[None, None, None, None],
     consist="high", own=4, churn="moderate", pin="mostly", repro="copyrun"),
  "cann": dict(rounds=1, rank=2, refine=False, fetch=1, fetch_fail=0,
     # 官方自动迁移页可抓且详尽：transfer_to_npu import+步骤+NCCL→HCCL+ms_fmk_transplt，
     # 明列支持 PyTorch 1.11/2.1/2.2（→ver_matrix）
     core_fetch="ssr", exec=True, ref_level="core_only",
     n_versions=3, ver_matrix=True, ver_irrelev=False, two_axis=False,
     # 华为云 ModelArts 最佳实践 / 知乎 / 博客园 / CSDN
     #（hiascend 页=官方①、ms_fmk_transplt=官方工具，不计二手）
     sources=["cloud_vendor","qa_reputation","tech_blog","tech_blog"],
     platforms=["huaweicloud","zhihu","cnblogs","csdn"],
     dates=[None, None, None, None],
     consist="high", own=3, churn="moderate", pin="mostly", repro="params"),
 },
 "H": {  # 量化 / 推理部署（推理部署类，版本敏感 中）
  "cuda": dict(rounds=1, rank=1, refine=False, fetch=1, fetch_fail=0,
     core_fetch="static", exec=True, ref_level="exhaustive",
     n_versions=2, ver_matrix=False, ver_irrelev=False, two_axis=False,
     # NVIDIA 开发者博客 / medium / github 示例 / SO（Torch-TensorRT docs=官方doc①）
     sources=["cloud_vendor","tech_blog","tech_blog","qa_reputation"],
     platforms=["nvidia-blog","medium","github","stackoverflow"],
     dates=[None, None, None, None],
     consist="high", own=4, churn="moderate", pin="mostly", repro="copyrun"),
  "cann": dict(rounds=2, rank=4, refine=False, fetch=1, fetch_fail=0,
     # 官方 AMCT 页可抓(ssr)但仅讲量化算法原理(对称/非对称公式)、无落地命令→概述级
     core_fetch="ssr", exec=False, ref_level="overview",
     n_versions=3, ver_matrix=False, ver_irrelev=False, two_axis=False,
     # msmodelslim 命令在 Gitee 蓝区仓(①)+CSDN；CSDN×3 / 知乎 / 53ai
     #（Gitee msmodelslim=官方仓①、vLLM-Ascend=官方仓①，不计二手）
     sources=["tech_blog","tech_blog","tech_blog","qa_reputation","aggregator"],
     platforms=["csdn","csdn","csdn","zhihu","53ai"],
     dates=["2025-01", "2025-05", None, None, None],
     consist="mid", own=3, churn="moderate", pin="mostly", repro="copyrun"),
 },
}

# 旧手评矩阵（从 17_official_site_focus.html 的 ROWS 提取，用于对比 diff）
OLD = {
 "A":{"cuda":[5,5,5,4,5,5,4,5,5,5],"cann":[4,4,4,2,4,4,3,5,3,4]},
 "B":{"cuda":[5,5,5,4,5,5,4,5,4,4],"cann":[4,4,4,2,3,3,3,5,3,3]},
 "C":{"cuda":[5,5,5,5,5,5,5,5,5,5],"cann":[4,4,3,3,3,4,3,5,4,4]},
 "D":{"cuda":[5,5,5,3,5,5,5,5,5,5],"cann":[2,2,BLK,2,2,2,2,1,2,3]},
}


# ============================================================
# 2. 每个指标一个公式函数（①–⑩）
# ============================================================

def score1_discover(r):
    """① 官方可发现性 = f(命中排名, 轮数, 是否需二次检索)。"""
    if r["rounds"] >= 2 and r["refine"]:        # 官方排不到首屏、靠二手关键词二搜
        return 2
    if r["rounds"] >= 2:
        return 3
    # 一轮内：按官方首条名次分档
    rk = r["rank"]
    if rk == 1:  return 5      # 首屏首条即官方
    if rk <= 3:  return 4      # 首屏但夹在二手中
    if rk <= 6:  return 4
    if rk <= 10: return 3
    return 2

def score2_fetch(r):
    """② 官方可抓取性 = 核心 how-to 页抓取形态映射。"""
    return {"static":5, "ssr":4, "partial":4, "spa":2, "robots":1}[r["core_fetch"]]

def score3_detail(r):
    """③ 官方正文详尽度。② 为 SPA/robots（抓不到正文）→ 受阻中性态。"""
    if r["core_fetch"] in ("spa", "robots"):
        return BLK
    exec_ok = bool(r["exec"])
    ref = r["ref_level"]
    if exec_ok and ref == "exhaustive":  return 5   # 命令/代码全 + 穷尽参考，照抄即用
    if exec_ok and ref == "core_only":   return 4   # 主路径详尽，仅穷尽参考表缺
    if ref == "overview":                return 3   # 有正文但偏概述，要东拼西凑
    if ref == "fragment":                return 2
    return 1

def score4_version(r):
    """④ 版本清晰度 = f(并存版本数, 支持矩阵, 是否版本无关/双轴)。"""
    if r["ver_irrelev"]:                  return 5   # 选型类，与版本无关
    if r["n_versions"] <= 1:              return 5
    if r["ver_matrix"]:                   return 4   # 多版本但官方列支持矩阵
    if r["two_axis"]:                     return 3   # 需定芯片+框架双轴但可锁
    if r["n_versions"] >= 3:              return 2   # 多版本号散乱
    return 3

def score5_sec_qty(r):
    """⑤ 二手丰富度 = 去重二手来源条数分档。"""
    n = len(r["sources"])
    if n >= 6: return 5
    if n >= 5: return 4
    if n >= 3: return 3
    if n >= 1: return 2
    return 1

def score6_sec_cred(r):
    """⑥ 二手可信度/一致性 = 来源可信度均分 + 一致性因子 + 时效罚分 + 独立性罚分，clamp 1..5。
       —— 用 SOURCE_CRED 表给每条来源打基准分取均值；按一致性档加减；
          按二手发表日期中位月龄「只罚不奖」(够新基线、过时才扣)；
          再按来源平台独立度「只罚不奖」(平台多样基线、互抄回声才扣，因子 B)。"""
    creds = [SOURCE_CRED[s] for s in r["sources"]]
    mean = sum(creds) / len(creds)
    val = (mean + CONSIST[r["consist"]]
           + recency_factor(r.get("dates", []))
           + independence_factor(r.get("platforms", [])))
    return max(1, min(5, round(val)))

def score7_own(r):
    """⑦ 模型自带知识 = 自评档 own + 知识截止 gap 罚分（因子 A），clamp 1..5。
       —— own 是唯一显式自评；cutoff_gap_factor(churn) 按相关工具迭代节奏「只罚不奖」
          给客观锚：迭代越快(fast)、我的训练知识越可能落后于最新版本。"""
    val = r["own"] + cutoff_gap_factor(r.get("churn", "stable"))
    return max(1, min(5, round(val)))

def score8_cost(r):
    """⑧ 检索成本（反向，越省越高）= f(轮数, 抓取次数, 抓取失败惩罚)。"""
    cost = r["rounds"] + 0.5 * r["fetch"] + 4.0 * r["fetch_fail"]
    if cost <= 1.5: return 5
    if cost <= 2.5: return 4
    if cost <= 4.0: return 3
    if cost <= 6.0: return 2
    return 1

def score9_pin(r):
    """⑨ 版本可锁定性（产出/因变量，不进⑪）。
       exact=能写出确切版本号+opset；mostly=工具版本基本可定；range=给范围/部分可锁；none=抽不出无法定死。"""
    return {"exact":5, "mostly":4, "range":3, "none":2}[r["pin"]]

def score10_repro(r):
    """⑩ 步骤可复现性（产出/因变量，不进⑪）。
       copyrun=照抄即跑；params=替好参数即可照抄；partial=大体能跑需小修/部分依赖环境；skeleton=仅骨架可述。"""
    return {"copyrun":5, "params":4, "partial":3, "skeleton":2}[r["repro"]]


# ============================================================
# 3. ⑪ 综合置信度 = 三源噪声-OR（与 17/18 的 confCompute 同源）
# ============================================================
def nm(v):
    """归一：1–5 → 0.2–1.0；受阻 → 0。"""
    return 0.0 if v == BLK else v / 5.0

def score11_overall(s):
    """s = 已算出的 ①–⑩ 分列表。返回 (综合分, 档位, 中间量)。"""
    OFF = nm(s[0]) * nm(s[1]) * nm(s[2])     # 官方：发现×抓取×详尽
    SEC = nm(s[4]) * nm(s[5])                # 二手：数量×可信
    OWN = nm(s[6])                           # 自带知识
    K = 1 - (1 - OFF) * (1 - SEC) * (1 - OWN)
    vf = 0.7 + 0.3 * nm(s[3])                # 版本因子
    cf = 0.9 + 0.1 * nm(s[7])                # 成本因子
    score = K * vf * cf
    band = ("高",5) if score>=0.80 else ("中高",4) if score>=0.63 else \
           ("中",3) if score>=0.45 else ("低",2) if score>=0.24 else ("很低",1)
    return score, band, dict(OFF=OFF,SEC=SEC,OWN=OWN,K=K,vf=vf,cf=cf)


# ============================================================
# 4. 跑全矩阵
# ============================================================
METRICS = [score1_discover, score2_fetch, score3_detail, score4_version,
           score5_sec_qty, score6_sec_cred, score7_own, score8_cost,
           score9_pin, score10_repro]
LABELS = ["①发现","②抓取","③详尽","④版本清","⑤二手量","⑥二手信",
          "⑦自带","⑧成本","⑨版本锁","⑩复现","⑪综合"]

TASKS = ["A","B","C","D","E","F","G","H"]

def compute():
    out = {}
    for t in TASKS:
        out[t] = {}
        for st in ["cuda","cann"]:
            r = RAW[t][st]
            s = [f(r) for f in METRICS]
            sc, band, mid = score11_overall(s)
            out[t][st] = dict(scores=s, overall=round(sc,3), band=band[0],
                              band_n=band[1], mid={k:round(v,3) for k,v in mid.items()})
    return out

def fmt(v):
    return "受阻" if v == BLK else str(v)

def main():
    res = compute()
    diff = "--diff" in sys.argv
    if "--json" in sys.argv:
        print(json.dumps(res, ensure_ascii=False, indent=1)); return
    print("量化公式复算矩阵（score_metrics.py）")
    print("="*108)
    print("格    " + "  ".join(f"{l:>5}" for l in LABELS))
    for t in TASKS:
        for st in ["cuda","cann"]:
            row = res[t][st]
            cells = [fmt(x) for x in row["scores"]] + [f'{row["overall"]:.2f}{row["band"]}']
            print(f"{t}.{st:4} " + "  ".join(f"{c:>5}" for c in cells))
    if diff:
        print("\n与旧手评的差异（新→旧；仅 A–D 有旧手评）：")
        for t in [k for k in TASKS if k in OLD]:
            for st in ["cuda","cann"]:
                new = res[t][st]["scores"]; old = OLD[t][st]
                for i,(n,o) in enumerate(zip(new,old)):
                    if fmt(n) != fmt(o):
                        print(f"  {t}.{st} {LABELS[i]}: {fmt(o)} → {fmt(n)}")
        # ⑪ 档位对比
        print("\n⑪ 综合档位：")
        oldband={"A":["高","中高"],"B":["高","中高"],"C":["高","中高"],"D":["高","低"]}
        for t in TASKS:
            for j,st in enumerate(["cuda","cann"]):
                ob = f"  (旧手评 {oldband[t][j]})" if t in oldband else "  (新跑·无旧手评)"
                print(f"  {t}.{st}: {res[t][st]['overall']:.2f} {res[t][st]['band']}{ob}")

if __name__ == "__main__":
    main()
