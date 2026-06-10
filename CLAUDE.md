# CLAUDE.md — 昇腾社区 vs CUDA 生态「AI 可用性」分析项目

> 本文件是项目记忆。新会话接手时**先读本文件**，不必重读全部对话历史。
> 全程中文沟通，产出物也用中文。

---

## 1. 项目目标

回答一个问题：**当我（Claude）回答昇腾（CANN / 昇腾社区）开发问题时，知识从哪来、可用性如何，与 CUDA / NVIDIA 生态相比差在哪。**
最终以一系列**带编号的交互式 HTML**呈现：任务清单 → 度量体系 → 逐任务实测 → 可下钻/可悬浮的热力图。

核心方法：选取若干开发者任务，每个任务在 **CUDA 生态**和**昇腾社区**各真实检索一遍（web_search / web_fetch），按统一指标打分并记录每一步。

---

## 2. 铁律（这些是反复被用户强调、踩过坑的）

1. **绝不编造**。来源标题、URL、日期、版本号若无把握，**重新检索拿到**再写，不能凭记忆杜撰。
2. **区分"实测 / 推断 / 理想化"**。我没有昇腾专有知识库，只有模型自带知识（训练得来、可能过时）+ 实时检索。凡推断必须标注（曾用 `*`），能实测就实测。
3. **（已更新 2026-06-09）默认基于现有主文件原地改 + git push，不再每次新建编号文件**。原「只往后编号、绝不覆盖」是旧容器环境(产出会丢)的规矩；现工作目录 `/Users/hsin/Documents/Coding/opknow` 已是 git 仓库(远程 `git@github.com:SchihHsin/opknow.git`，经 GitHub Pages 发布)，历史由 commit 保留，原地改安全。只有用户显式要「新版本/保留对比」才新建。
4. **本地 git 工作流**：改完主文件提交并 push 到 main(用户已授权，用于 Pages 发布)；若改主文件需同步把 `index.html` 更新为其副本，根地址才会刷新。本地预览 `python3 -m http.server` 会被沙箱拦，需关沙箱起(规则已写进 `.claude/settings.json` 的 `sandbox.excludedCommands`，重载配置后生效)。
   - **（2026-06-09 用户要求）每次有实质改动都要：① 同步更新本 CLAUDE.md 反映当前现状（主文件是哪个、改了什么、结论有无变化）② commit 并 push。不要攒着不更新、不要改完不 push。**
5. 结论要诚实标注**局限**（样本薄、主观评分等）。

---

## 3. 度量体系（11 项 + 综合；2026-06-09 重新定义）

**核心被测对象**：当我（Claude）回答某栈某开发任务时，能否把一份**正确、具体、可锁版本、可复现**的答案搬进回复，以及花多大力气。这是「AI 可用性」（站在会检索的 AI 助手视角，不是"栈好不好用"）。

**概念模型**：一条"把知识搬进答案"的价值链——**触达（搜得到→抓得到）→ 内容质量（够细→版本清楚）→ 检索成本（摩擦）→ 产出（锁版本/可复现）**。知识有三个来源渠道（官方一手 / 二手社区 / 模型自带知识），**前两关对每个渠道分别看** → "三源 × 两关"网格。

| 渠道 / 段 | 指标 | 说明 |
|---|---|---|
| 官方·触达 | ① 官方可发现性 | 官方文档排名 / 几轮命中 |
| | ② 官方可抓取性 | 静态可抓 vs SPA/robots 拦（CANN 公共常量级短板，统一记 2；CUDA 5） |
| 官方·质量 | ③ 官方正文详尽度 | 取回正文够不够细（参数表/命令/JSON）。**CANN 因②受阻→记「受阻·无法实测」中性态，不打推断分** |
| | ④ 版本清晰度 | 是否容易选对版本（还是多版本号散乱） |
| 二手·触达 | ⑤ 二手丰富度 | GitHub/SO/博客等数量与可发现度 |
| 二手·质量 | ⑥ 二手可信度 / 一致性 | 权威/够新/彼此对得上 |
| 自带·触达 | ⑦ 模型自带知识 | 训练覆盖密度，能否凭知识答（质量面并入本项） |
| 过程 | ⑧ 检索成本 | 轮数 + fetch（反向：越少越好） |
| 产出（因变量） | ⑨ 版本可锁定性 | 能否定到确切版本 |
| | ⑩ 步骤可复现性 | 命令能否照抄跑通 |
| 汇总 | ⑪ 综合置信度 | 前述汇总（非简单平均） |

- 评分 1–5，越高越好；⑧ 反向。着色 v5 绿→v1 红；**受阻态用独立中性色，"未测"≠"低分"**。
- **③ 是本轮新增**（用户指"内容质量只有一个指标太少"）：抓得到（②）≠ 够用（③），两者正交。
- **版本敏感度**是"任务属性、与栈无关"（两栏取值相同），**不进矩阵当列**，只做任务名旁小标签（贡献为零，已被纠正）。
- 真正区分两栈：②③④⑤⑥（+⑦自带知识、⑧成本）。⑨⑩是因变量、勿与输入项重复加权。
- **完整方法论说明书 = `18_metric_definition.html`**（2026-06-10 升级：不再只是"指标定义书"，现覆盖全链路①任务怎么选→②问题怎么编→③指标体系怎么形成(价值链→三源×两关→三道形成准则→5 次演化纠偏时间线)→④11 项逐项定义/打分口径→⑤评分 1–5 怎么判定(硬实测/半实测/自评三档+锚定法+受阻态+局限)→⑥6 条设计决定。§6.2/6.3 已同步"可抓取性子树相关、仅 D 受阻"最新结论）。

---

## 4. 已跑的 4 个任务（每个 CUDA + CANN 各跑）

| 代号 | 任务 | 版本敏感 | CUDA 综合 | CANN 综合 |
|---|---|---|---|---|
| A | 模型转换 / 导出（PyTorch→ONNX→TensorRT ｜ ONNX→ATC→.om） | 高 | 高 | 中高 |
| B | Profiling 定位瓶颈（Nsight ｜ msprof / Ascend PyTorch Profiler） | 中 | 高 | 中高 |
| C | 算子库选型（cuBLAS/cuDNN/… ｜ AOL/ATB/TBE） | 低 | 高 | 高 |
| D | 自定义算子开发（CUDA kernel+ext ｜ Ascend C+msOpGen+aclnn） | 高 | 高 | 中 |

---

## 5. 关键结论

1. **昇腾社区可用性是"任务相关"的，不是一刀切的低。** 成熟工具/通识类（A 转换、B Profiling、C 库选型）两边差距小；**前沿开发（D 自定义算子）差距被拉满**。
2. **（2026-06-10 真跑实测修正）官方可抓取性是「子树相关」，不是平台公共常量。** 旧说「hiascend `/document/detail/` 全站 SPA、②统一记 2」被本轮活体复核推翻：
   - **可抓子树**（服务端渲染、正文可抓）：`quickstart/`(A，atc 命令+参数表+npu-smi)、`modeldevpt/ptmigr/`(B，torch_npu.profiler 完整代码+参数表)；`doc_center/`(C-ATB ascendtb_0001) **部分可抓**（概述+接口机制有、算子列表/调用码无）。
   - **SPA 子树**（只回导航+meta）：`devaids/`(A-ATC 参考)、`devguide/devtools/`(B-msprof 原生)、`apiref/aolapi/`(C-AOL 算子表)、`devguide/opdevg/`(D-Ascend C)。
   - **据此矩阵打分（已落进 17）**：A.cann ②2→4 ③受阻→4；B.cann ②2→4 ③受阻→4；C.cann ②2→4 ③受阻→3；**D.cann 仍 ②2 ③受阻**（核心 how-to 整个压在 `devguide/opdevg/` SPA，无可抓子树兜底）。CUDA 静态站全部 ②5。
   - **含义更精准**：SPA 短板**只在 D 真正咬到结果**——A/B 有可抓子树兜住主路径 how-to、C 靠厚二手绕过；只有 D 既无兜底子树、二手又稀、版本又散 → 三重坑叠加。即「不是 CANN 文档一律抓不到，而是越深入前沿开发越掉进坑」。
3. **"找得到"≠"抓得到"≠"够用"**：三关正交。A/B/C/D 官方多数搜得到(①≈4)，但**抓不抓得到看落在哪个子树**（前沿/参考深层页 SPA），抓到了还要看正文够不够细(③)。
4. **版本清晰度是 CANN 跨任务普遍弱项**（多版本号并存）。
5. 对社区的启示（按本度量，性价比最高的改进）：**把官方文档站做成可抓取（静态化/纯文本入口）抬升②**；**在前沿开发场景补带版本号的完整二手抬升④**。

---

## 6. 产出文件清单（均在 /mnt/user-data/outputs/）

| 文件 | 内容 |
|---|---|
| `claude_ascend_answer_journey.html` | 早期：回答昇腾算子问题的用户旅程图 |
| `cuda_vs_cann_answer_workflow.html` | 早期：按阶段对齐的 CUDA vs CANN 流程 |
| `03_ai_engineering_principles.html` | 方法论：分析问题→找社区信息→识别原则→找不到的兜底阶梯 |
| `04_task_metric_structure.html` | 度量体系（最初 7 维）+ 范例 |
| `community-grounded-answer_SKILL.md` | 可复用 SKILL.md（4 阶段方法 + 评分） |
| `05_developer_task_taxonomy.html` | 26 个任务 × 7 大类的清单，每个标版本敏感度 |
| `06_task_stack_metric_matrix.html` | 4 任务 × 2 栈 × 7 维评分矩阵 |
| `07_metric_drilldown_report.html` | 全任务覆盖总览 + 4 任务逐个下钻 |
| `08_stepwise_run_traces.html` | 8 次运行的每一步 workflow（input/output 节点） |
| `09_interactive_drilldown.html` | 可点击矩阵 → 任务详情（首版） |
| `10_interactive_drilldown_v2.html` | 同上，去掉版本敏感度独立列 |
| `11_fine_grained_indicators.html` | 9 分指标热力图（指标为行） |
| `12_heatmap_interactive.html` | 行列对调（任务×栈为行、指标为列）+ 可点击 |
| `13_full_heatmap_measured.html` | 全 26 任务（22 待跑）+ 可抓取性改实测 |
| `14_full_heatmap_anchored.html` | 类别移到左列 + 点击定位楼层 + 回到顶部 FAB |
| `15_heatmap_hover.html` | 逐格悬浮看详情（每格说明过程，低分说问题），类别在左列 |
| `16_detailed_hover.html` | 在 15 基础上把每格 tooltip 写**详细**——可抓取格写「抽到✓/缺失✕」、来源类格列「标题·域名·日期·版本号」、版本清晰格列实际并存版本号串；CUDA 四项缺口已重新检索补齐 |
| **`17_official_site_focus.html`** | **当前主交互**：把「官方网站」提为左侧醒目大组（NVIDIA docs ｜ hiascend），内部分「能否触达（可发现·可抓取）/ 内容质量（**正文详尽·版本清晰**）」；二手/模型/检索/产出视觉弱化；矩阵格已去掉描边。**2026-06-10 加③官方正文详尽度列**：CUDA 四任务逐一 web_fetch 官方页**实测=5**。**2026-06-10 再修正（真跑 B/C/D 后）**：可抓取性证实「子树相关」，CANN A.cann ②4③4、B ②4③4、C ②4③3 改为实测分（quickstart/modeldevpt/doc_center 可抓），**仅 D 仍 ②2③受阻**（核心 how-to 压在 devguide/opdevg SPA、无可抓子树兜底）。banner/各格 tooltip/TASKOVER 已同改。**2026-06-10 再加「评分标尺」**：每格悬浮在分数下新增评分标尺块（`RUBRIC[ci]` 列出该指标 5→1 锚点、与 18 §4 一致），高亮本格所在档位（由色类 v5–v1 推出），并加「本格落在第 N 档·依据见上文」脚注；受阻格单列中性态说明（受阻≠低分），⑪综合标注「整体研判非简单平均」——回答用户「为什么是 X 分、怎么算的」。**全站术语「先验」→「模型自带知识」**。**2026-06-10 加「点击固定·模态」交互**：悬浮照旧；**点击任意矩阵格/任务名 → 卡片固定成模态**（`pinned` 标志 + `#tipmask` 暗化遮罩 + 卡内 × 关闭键 + 「点击空白处或 × 关闭」脚注），点空白处/遮罩/Esc 关闭；固定态 `pointer-events:auto` 可滚动、`showTip` 在 pinned 时不被悬浮抢占。**2026-06-10 加「综合置信度怎么算出来的」推导块 + 外推风险加权**：解决用户质疑「C 外推20%却置信度高、A 外推10%却中高，标准很奇怪」——⑪格悬浮在来源构成下新增橙色推导块（`confDeriv()` + `RISKW`），写明 **置信度 ≈ 触达+内容质量基线 − 有效外推风险 − 留白/受阻**，其中**有效外推风险 = 类比外推占比 × 任务风险权重**（风险权重由版本敏感/容错定：高=1.0、中=0.6、低=0.3）。据此 C 20%×0.3=**6.0** ＜ A 10%×1.0=**10.0** → C「高」反而高于 A「中高」；B 13%×0.6=7.8；D 35%×1.0=**35**叠加受阻+留白15%→「中」。四者有效外推风险与⑪档位单调一致，外推%数据不变、只补可复核研判主线 |
| **`18_metric_definition.html`** | **完整方法论说明书（单独材料，2026-06-10 升级）**：把原"指标定义书"扩成全链路一份讲全——0 到底测什么 / 1 任务怎么形成(26 任务清单里沿"成熟→前沿"光谱挑 4 个+三条挑选准则+ABCD 表) / 2 问题怎么形成("本质相同仅换栈"配对原则 + 4 对 8 条原始问句) / 3 指标怎么形成(被测对象→价值链四段→三源×两关网格→三道形成准则→v1-v5.1 演化纠偏时间线) / 4 指标逐项定义+口径 / 5 评分 1–5 怎么判定(硬实测①②③⑧·半实测④⑤⑥·自评因变量⑦⑨⑩⑪三档 + 锚定法 + 受阻≠低分 + CUDA=5 相对锚 + 4 条局限) / 6 设计决定。**§6.2/6.3 已同步最新结论：②可抓取性子树相关(A/B/C=4、D=2)、③正文详尽仅 D 受阻**。顶部加目录锚点导航。**2026-06-10 §4 评分标尺补全为完整 5→1 五档**（原仅 5/3/1 或 5/4/2，现 4/2 等中间档全部补齐，与 17 矩阵悬浮的 `RUBRIC[ci]` 逐字对齐；⑪综合也补标尺），两份材料标尺自此完全一致。**2026-06-10 加「来源构成」堆叠条**：悬浮 ⑪ 综合置信度格时，在卡内出一条**五段来源构成**（官方一手/二手社区/自带·有把握/**类比外推·未验证(风险区,橙色斜条纹警示色)**/诚实留白·受阻；和=100、回顾性估计），与综合置信度互证（D.cann 外推35%+留白15% 印证其综合「中」）。`SRC_MIX[k][stack].m` 存五段比例、`srcMixBlock()` 渲染、`SEGDEF` 定义段。**关键诚实修正**：用户追问「你平常回答开发者会不会按 CUDA 经验外推编」→ 承认平常默认行为里那块「留白」常被**类比外推填上、且置信度标注常不足**（≈幻觉高发区），故把「外推·未验证」从「留白」里**显式拆出单列警示**；「凭空瞎编」≈0（拿不准不杜撰），但外推≠0 才是真正风险。角标已注明。**2026-06-10 §4 ⑪ 卡新增「怎么算出来的」推导块（方法论级，落库不只在对话）**：写明 综合置信度 ≈ 触达+内容质量基线 − 有效外推风险 − 留白/受阻；**有效外推风险 = 暴露面（外推占比）× 后果严重度（任务风险权重 高1.0/中0.6/低0.3）**；并专门论证**「为什么是乘不是加」——风险=暴露×后果、风险权重是放大器非独立扣分项，边界判据「外推=0→风险=0」（相加会让高敏感任务零外推也被白扣）**；附四任务单调对照（C6.0高/B7.8中高/A10.0中高/D35中），与 17 矩阵 ⑪ 悬浮 `confDeriv()` 同源。回应用户「公式只在对话里输出没意义、应落进 17/18」 |

**当前最新主交互 = `17_official_site_focus.html`；完整方法论说明书 = `18_metric_definition.html`。**

> 本地工作目录：`/Users/hsin/Documents/Coding/opknow`（已是 git 仓库，远程 `git@github.com:SchihHsin/opknow.git`，经 GitHub Pages 发布；`index.html` 为根地址展示用的副本，**已同步到 17**）。注意：03–14 等早期文件目前只在旧容器 `/mnt/user-data/outputs/`，本地仅有 15/16/17/18/index/CLAUDE.md。

> **CUDA 官方正文详尽度实测记录（2026-06-10 web_fetch）**：A TensorRT Quick Start → `trtexec --onnx=... --saveEngine=... --stronglyTyped` + 完整 C++/Python 运行时代码（旗标全表为跳转链接）；B Nsight Systems UserGuide → `nsys profile` 语法 + `--trace`/`--backtrace` 选项全表 + 环境变量模式；C cuBLAS → 完整 API 签名 + 状态码/参数表 + 两段 C 示例；D PyTorch cpp_custom_ops → setup.py + C++ 算子定义 + `STABLE_TORCH_LIBRARY` 注册 + 分步骤。四者均静态可抓、正文详尽 → ③=5（实测）。

---

## 7. 进行中的任务（未完成）

~~用户要求悬浮卡片更具体~~ → **已在 `16_detailed_hover.html` 完成**：可抓取格写「抽到✓/缺失✕」，来源类格列「标题·域名·日期·版本号」，覆盖所有指标。CUDA A(TensorRT)/B(Nsight)/D(PyTorch custom ops)、CANN C(AOL/ATB) 的来源已重新检索补齐（见 16 内数据 + 下方附录）。
- 待办：16 尚未在真实浏览器目测（本地 `python http.server` 被沙箱拦，仅用 node 跑通数据/渲染逻辑验证）。

### 7a. （2026-06-10 完成）真跑 4 任务并记录问题+过程 → `task_run_log.md`
用户要求「实际跑这些任务，把每个任务用的问题和过程记录下来（md 即可）」。已在 **`task_run_log.md`** 完整记录 A/B/C/D 四个任务：每个任务设计「本质相同、仅技术栈不同」的一对问题，按我平常解题工作流真跑 web_search / web_fetch，逐步记命中与打分。

**本次真跑得到的关键修正（比旧记录更精确，⚠ 17/18 HTML 尚未同步）：**
- **②可抓取性是「子树相关」，不是平台公共常量**。实测：`quickstart/`(A)、`modeldevpt/ptmigr/`(B `AImpug_000068`，torch_npu.profiler 完整代码+参数表) = 服务端渲染**可抓**；`doc_center/`(C-ATB) = **部分可抓**（概述+接口机制有、算子列表/调用码无）；`devaids/`(A-ATC参考)、`devguide/devtools/`(B-msprof)、`apiref/aolapi/`(C-AOL)、`devguide/opdevg/`(D-AscendC) = SPA。
- 据此 **B、C 的 CANN ②③ 应由旧「2 / 受阻」上修**（B ②4③4、C ②4③3，均实测有正文）；**A 此前已上修**；**只有 D 仍 ②2、③受阻**（核心 how-to 整个压在 devguide/opdevg SPA，无可抓子树兜底）。
- 即：**SPA 短板只在 D 真正咬到结果**（A/B 有可抓子树兜主路径、C 靠厚二手绕过）。中心论点更精准 = **越深入前沿开发，越同时掉进 SPA + 二手碎片 + 版本散乱三重坑**。
- **（2026-06-10 已落矩阵）** 上述修正已同步进 `17_official_site_focus.html` + `index.html`：A.cann ②2→4③受阻→4、B ②2→4③受阻→4、C ②2→4③受阻→3、D 保持 ②2③受阻；头条 banner、各格 tooltip（抽到/缺失/来源）、TASKOVER 概览均改。node 校验四行各 11 格、数据解析通过。

### 7b-续. 可能的后续
- 继续跑 22 个待跑任务（清单见下）；优先：报错码排查、分布式训练 HCCL、CUDA→昇腾迁移。
- 把 4 个已跑任务的 CUDA 侧也逐一 web_fetch 实测可抓取性（目前 A/B fetch 过，C/D 由片段+既有记录佐证）。

## 7b. 全部待跑任务（22 个，矩阵中标"待跑"）

- 环境与安装：版本兼容排查、安装与环境变量、容器/镜像搭建
- 算子开发：算子精度排查、动态 shape/Tiling、算子融合、注册与框架集成
- 训练：分布式训练配置、混合精度训练、显存/OOM 优化、精度/收敛排查
- 推理与部署：推理服务部署、量化、动态 batch/shape 推理
- 性能优化：访存/occupancy 优化、计算与传输重叠、多卡通信优化
- 调试：内存越界定位、报错码/异常排查
- 迁移：CUDA→昇腾迁移、跨芯片迁移、概念心智模型对照

建议优先跑（最可能改变结论）：报错码排查、分布式训练 HCCL、CUDA→昇腾迁移。

---

## 8. House style（所有 HTML 统一）

- 字体 `Noto Sans SC`；CSS 变量 `--nv:#76B900`(NVIDIA 绿) / `--hw:#C8102E`(华为红)。
- 色阶 v5→v1：`#BBF0D4 / #DCF5E5 / #FCEFC7 / #FBE0CE / #F9D2D2`。
- **不要旋转/倒置文字**（用户投诉过 `transform:rotate(180deg)` 导致倒字）。
- 卡片 `align-items:start`，**不强行拉伸**短卡（用户投诉过）。
- 标题左侧竖条、克制的留白、干净卡片/热力图风格。
- 谨慎用 emoji，仅 `⚠ / ✓` 已在用。
- **不要用 localStorage/sessionStorage**（artifact 环境不支持）；状态用 JS 内存。

---

## 9. 附录：已核实的真实来源数据（可直接用于 tooltip，勿改动事实）

### 官方站可抓取性（实测）
- `/document/detail/` 三棵子树均 SPA：A=`canncommercial/80RC2/.../quickstart_18_0012.html`、B=`CANNCommunityEdition/80RC3alpha003/.../atlasprofiling_16_0010.html`、D=`CANNCommunityEdition/82RC1alpha003/.../atlas_ascendc_10_0006.html` → web_fetch 仅得导航 + meta 摘要，正文（参数表/JSON/分步命令）抓不到。
- `/doc_center/source/...` → ROBOTS_DISALLOWED。
- 抓到 vs 缺失举例（A-ATC）：**抓到** = meta 里那条 `atc --model=resnet50.onnx --framework=5 ...` 命令；**缺失** = 各参数说明表、soc_version 获取步骤、完整正文。

### A 模型转换 / ATC — 真实来源
官方（多版本并存）：
- `canncommercial/80RC2` quickstart_18_0012（`atc --model=resnet50.onnx --framework=5 --output=resnet50 --input_shape="actual_input_1:1,3,224,224" --soc_version=<soc_version>`）
- `canncommercial/80RC3` quickstart_18_0010；`CANNCommunityEdition/800alpha001` quickstart_18_0010
- ATC 完整参考 `atlasatc_16_0001`
二手：
- 知乎 zhuanlan/p/393169777（引用旧版 CANN V100R020C10 / 5.0.1）
- 阿里云 developer/article/1662723（**2025-05-06**，Ascend910B4 动静态 shape 实例）
- 博客园 racesnail/18860625（飞桨x昇腾）、huaweiyun/17163186、小宅博客
- 版本号跨度证据：V100R020C10、5.0.1、8.0.RC2、8.0.RC3、800alpha001/003

### B Profiling / msprof — 真实来源
官方版本跨度（同一工具散落多版本）：CANN 商用版 5.0.4.6 / 6.0.1 / 8.0.RC2；社区版 8.0.RC3.alpha003 / 8.1.RC1.alpha001 / 8.0.0.alpha001；MindStudio 7.0.RC2（其一 **2025-04-07**）/ 8.1.RC1。
实测：`atlasprofiling_16_0010` → SPA，仅 meta 摘要（"msprof 采集通用命令…AI 任务运行性能数据…采集和解析能力"）。
亮点：有**完全对标 PyTorch-GPU 用法**的 Ascend PyTorch Profiler（with / start-stop / schedule）。
二手：阿里云、CSDN×2、知乎。

### C 算子库选型 / AOL·ATB — 待补全准确日期
官方：hiascend AOL API 参考（CANN 社区版 8.0.RC3）、ATB 文档。命名：**AOL**(NN/BLAS/DVPP/FlashAttention)、**ATB**(Transformer/大模型)、TBE(较老)。映射：cuBLAS↔AOL-BLAS、cuDNN↔AOL-NN、transformer↔ATB。二手：知乎、博客园(ZOMI)、华为云 bbs。

### D 自定义算子开发 / Ascend C — 真实来源
官方（多版本并存）：
- `canncommercial/80RC3` atlas_ascendc_10_0064（`msopgen gen -i $HOME/sample/add_custom.json -c ai_core-<soc_version> -lan cpp -out $HOME/sample/AddCustom`）
- `CANNCommunityEdition/82RC1alpha003` atlas_ascendc_10_0006（编译 → `custom_opp_ubuntu_x86_64.run` → 部署到 OPP `vendors/customize`）
- `CANNCommunityEdition/80RC2alpha001` atlas_ascendc_10_0005（**完整 add_custom.json**：op=AddCustom，x/y fp16 ND，输出 z fp16 ND）
- `CANNCommunityEdition/82RC1alpha003` atlas_ascendc_10_0101（简易工程，`-f aclnn`）
二手：
- MindSpore 2.3.1 教程（mindspore.cn op_custom_ascendc；`ops.Custom`，func_type="aot"，aclnn / c++ infer）
- CSDN xyz3120/143643855「AscendC 从入门到精通系列（三）」（**2024-11-09**）
- ai6s.net 69322a96「Ascend C 算子开发全流程揭秘」（**2025-12-05**，Copy-In/Compute/Copy-Out 三段流水线 + msopgen 脚手架结构）
- 版本号跨度证据：80RC2alpha001、80RC3、82RC1alpha003

### CUDA 侧 — 待补全准确标题/日期
- A TensorRT：docs.nvidia.com（其一约一周前更新）、Torch-TensorRT、GitHub(qbxlvnf11 / sithu31296)、LearnOpenCV、Medium、ridgerun
- B Nsight：PyTorch dev-discuss、NVIDIA 论坛、PyTorch Lightning 文档、AceCloud(2026-01)、Practical ML
- D custom ops：docs.pytorch.org 官方教程、GitHub×4（extension-script 等）；注意 2.10+ ABI-stable vs 旧 THCudaTensor
- 官方为静态站、可抓取 → ②记 5（CUDA 侧未逐一 fetch 实测，由片段为完整正文佐证）

---

_最后更新：2026-06-10（17 加点击固定·模态交互；⑪加「置信度怎么算」推导块 + 外推按任务风险加权，解释 C 高/A 中高之差；index.html 已同步）。_
