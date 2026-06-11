---
name: run-cann-task
description: 跑一个或多个「CANN vs CUDA AI 可用性」开发者任务的标准流程——真实检索打分、记录过程、落进 17/18 矩阵并 push。当用户说「再跑 X 任务 / 跑下一批 / 把 XX 任务也跑了 / 继续跑待跑清单」时使用。封装本 opknow 项目的全流程：选任务→编配对问句→实测检索 web_search/web_fetch→按 score_metrics.py 公式打分→记 task_run_log.md→更新 17/index/18→验证→commit/push→更新 CLAUDE.md。
---

# run-cann-task — 跑任务并落库的标准作业

> 先读项目记忆 `CLAUDE.md`（§3 指标、§3a/§3b 公式、§4 已跑、§7b 待跑、§8 house style）。本 Skill 是「怎么做」的操作手册，不复述「为什么」。**全程中文。铁律见 CLAUDE.md §2，尤其「绝不编造」——来源标题/URL/日期/版本号无把握就重新检索拿到再写。**

## 0. 适用与不适用
- 适用：跑 CANN/CUDA 配对的开发者任务、补打分、把结果呈现进矩阵。
- 一次跑几个：单会话**顺序安全批量 = 4 个**（每任务两栈各多次 fetch，原文吃上下文，4 个接近压缩红线）。要更多 → 见 §7「批量与并行」。

## 1. 选任务
- 从 `CLAUDE.md §7b` 的 22 个待跑清单挑（用户没指定就挑「最可能改变结论」的：报错码/分布式/迁移已跑，剩余优先访存优化、动态 shape、精度排查等）。
- 给每个任务定**版本敏感度**（高/中/低）——这是任务属性、与栈无关，两栏取值相同，**不进矩阵当列**，只做任务名旁小标签。
- 续编代号：A–H 已用，新任务接 I、J…

## 2. 编配对问句（关键：本质相同，仅换栈）
- 每任务设计**一对**问题：CUDA 一句、CANN 一句，**解决的是同一类开发问题、只是技术栈不同**（例：A=「PyTorch 模型导出部署，CUDA 走 TensorRT｜昇腾走 ATC→.om」）。
- 像我平常被开发者问到那样自然措辞，写进 `task_run_log.md`。

## 3. 实测检索（不可省、不可编造）
对**每栈**按我平常解题工作流跑：
1. `web_search` 关键词（记**轮数 rounds**、官方文档命中**排名 rank**、是否需要**改写重搜 refine**）。
2. 对最相关的官方页 `web_fetch`（记**抓取形态 core_fetch**：`static` 纯静态 / `ssr` 服务端渲染可抓 / `partial` 部分可抓 / `spa` 只回导航+meta / `robots` 被 robots 拦；记 **fetch 次数**、**fetch_fail** 失败次数）。
3. 判**正文详尽度 ref_level**：`exhaustive` 穷尽（参数表+命令+可跑代码）/ `core_only` 主路径 how-to / `overview` 概述 / `fragment` 碎片/兜底页 / `none`。**SPA 抓不到正文 → 记「受阻」中性态，不打推断分**。
4. 数**二手来源**：逐条记 `标题·域名·日期·版本号`，分类型（official_*=官方渠道**不计二手**；qa_reputation/cloud_vendor/arxiv/tech_blog/aggregator 见 §4 SOURCE_CRED）；记**平台 platforms**（判去重独立性）、**发表日期 dates**（拿不到留 `None`、**绝不杜撰**）、**一致性 consist** high/mid/low。
5. 记**版本扩散 n_versions**（并存版本号个数）、是否有**版本矩阵 ver_matrix**、是否**版本无关 ver_irrelev**、是否**双轴 two_axis**。
6. 自评**模型自带知识 own**（1–5，唯一显式自评、注明无法外部量测）+ 该领域**迭代节奏 churn** stable/moderate/fast。
7. 记**产出**：能否锁版本 pin（exact/mostly/range/none）、命令能否照抄跑通 repro（copyrun/params/partial/skeleton）。

> **边跑边写 `task_run_log.md`**（防压缩丢证据）：每任务一段，含版本敏感度、使用的问题(CUDA/CANN 对)、CUDA侧过程(编号步骤)、CANN侧过程、评分行、小结。格式照搬已有 A–H 段。

## 4. 打分（用 score_metrics.py 公式，非主观）
- 把 §3 观测填进 `score_metrics.py` 的 `RAW` 字典新键（照搬已有任务的字段结构：`rounds,rank,refine,fetch,fetch_fail,core_fetch,exec,ref_level,n_versions,ver_matrix,ver_irrelev,two_axis,sources,platforms,dates,consist,own,churn,pin,repro`）。在字段上方写 `#` 注释标来源。
- 把新代号加进 `TASKS = [...]`。
- 跑 `python3 score_metrics.py --diff` → 得①–⑪ 各分（⑪=三源噪声-OR：综合=K×版本因子×成本因子，见 CLAUDE §3a）。**这是权威分，UI 必须与它逐值一致**。
- ⑥可信度用 `SOURCE_CRED` 锚定表：official_doc/repo 5.0、official_forum 4.5、cloud_vendor/arxiv 4.0、qa_reputation 3.5、tech_blog 3.0、aggregator 2.5；并入 `recency_factor`(中位月龄只罚不奖) + `independence_factor`(平台去重只罚不奖)。
- **去重铁律**：官方文档/官方代码仓/官方论坛属①官方渠道，**不计入⑤⑥**。

## 5. 呈现（落进 17/index/18）
在 `17_official_site_focus.html` 加：
- **ROWS{}**：`代号:{name,cuda:[11个 N() 格],cann:[11个 N() 格]}`。格用 `N(colorClass, dataText, tooltip, extra)`；色类 v5→v1 对应分 5→1、受阻用 `blk`；11 列顺序 = ①发现②抓取③详尽④版本清⑤二手量⑥二手信⑦自带⑧成本⑨版本锁⑩复现⑪综合。tooltip 写实测细节（抽到✓/缺失✕、来源标题·域名·日期·版本号、并存版本号串、⑪写 K/版本/成本推导）。
- **TASKOVER{}**：`{q,cu,ca,v}` 概览。
- **CATS[]**：把任务挂到对应类别（k:'代号'）。
- **ROLES[]**：给对应角色的任务束 chip 加 `run:'代号'`（已实测红底✓可点跳行）。
- **SRC_MIX{}**：五段来源构成 `m:[官方,二手,自带,外推,留白]`（和=100，前三段≈K×100 自洽校验）。
- **K 值笔误自查**：tooltip 里手写的 K/分值必须等于 `score_metrics.py` 实算（曾踩坑写错 K，务必比对）。

在 `18_metric_definition.html` 加：
- §1 抽样表加行（任务·栈·版本敏感·CANN 综合档+分）。
- §4「N 格复算结果」表加行：`cu: K×版本×成本=.xx ｜ ca: …` + 落档。

## 6. 验证 → 同步 → push → 更新记忆
```
cp 17_official_site_focus.html index.html      # 根地址才刷新
node /tmp/validate17.js                         # tipCol 0-10 OK / JS parse OK
python3 score_metrics.py --diff | tail -20      # ⑪档位与 17/18 逐值一致?
diff -q 17_official_site_focus.html index.html  # 17==index
```
- 全过校验后：`git add` 改动的文件 → **新建** commit（**绝不 --amend、绝不 --no-verify**）→ `git push origin main`。
- **同步更新 `CLAUDE.md`**：§4 任务表加行、记本批发现、footer changelog 加一条、若结论有变改 §5。
- 提交信息中文、说清跑了哪些任务+关键发现，结尾带 `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>`。

## 7. 批量与并行（回答「能不能一起跑」）
- **单会话顺序**：稳到 4 个；要 6–8 个必须严格§3「边跑边写盘」，否则压缩丢证据。
- **真·并行**：用 sub-agent，每任务一个 agent（独立上下文）。代价：冷启动耗 token、跨 agent 难盯「绝不编造」→ **并行产出后逐个抽检来源真实性**再合并打分。Skill 只省方法论复述的外围 token，**核心 web 检索成本不可压缩**。
- **⚠ sub-agent 必须回传「问句原文」**（2026-06-11 踩坑补）：第三批 I–S 并行跑时 sub-agent 只回传了结构化观测，9 个任务的问句原文随会话丢失、无法复原（后只能补编、存 18 §2 HTML 注释）。并行模板里**问句原文是必传字段**，主会话落 task_run_log.md 时逐字记录。

## 8. house style（CLAUDE §8）
Noto Sans SC；`--nv:#76B900`/`--hw:#C8102E`；色阶 v5→v1 `#BBF0D4/#DCF5E5/#FCEFC7/#FBE0CE/#F9D2D2`；不旋转/倒置文字；卡片 `align-items:start` 不强行拉伸；emoji 仅 ⚠/✓；**不用 localStorage/sessionStorage**；未核实的官方数字（如 260+ 算子）一律不写、要用先 web 核实。
