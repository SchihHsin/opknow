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
2. **区分"实测 / 推断 / 理想化"**。我没有昇腾专有知识库，只有训练先验（可能过时）+ 实时检索。凡推断必须标注（曾用 `*`），能实测就实测。
3. **文件只往后编号，绝不覆盖**之前的（03、04…15…）。
4. **容器会在会话间清空**：`/home/claude` 等临时目录会丢失。**所有产出直接写 `/mnt/user-data/outputs/`**，写完用 present_files 呈现。改旧文件前先确认它还在，必要时重建。
5. 结论要诚实标注**局限**（样本薄、主观评分等）。

---

## 3. 度量体系（9 分指标 + 综合）

由最初的 7 维细化而来（把"打包"的维度拆开）。按组：

| 组 | 指标 | 说明 |
|---|---|---|
| 官方一手源 | ① 官方可发现性 | 官方文档排名 / 几轮命中 |
| | ② 官方可抓取性 | 静态页可抓 vs SPA/被 robots 拦 |
| | ③ 版本清晰度 | 是否容易选对版本（还是多版本号散乱） |
| 二手源 | ④ 二手数量 | GitHub/SO/博客等丰富度 |
| | ⑤ 二手可信度 / 一致性 | 各源是否对得上 |
| 模型 | ⑥ 模型先验强度 | 训练数据覆盖密度，能否凭知识答 |
| 检索 | ⑦ 检索成本 | 轮数 + fetch（反向：越少越好） |
| 产出 | ⑧ 版本可锁定性 | 能否定到确切版本 |
| | ⑨ 步骤可复现性 | 命令能否照抄跑通 |
| 汇总 | ⑩ 综合置信度 | 前 9 项汇总 |

- 评分 1–5，越高越好；⑦ 为反向。着色 v5 绿→v1 红。
- **版本敏感度**是"任务属性、与栈无关"（两栏取值相同），**不放进矩阵当列**，只做任务名旁的小标签。这是被用户纠正过的：它对"区分两个栈"贡献为零。
- 真正区分两栈的是 ②③④⑤（+⑥先验、⑦成本）。

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
2. **官方可抓取性是 CANN 的平台级短板（实测）：** hiascend 的 `/document/detail/` 是 JS 单页应用（SPA），web_fetch 只回导航 + meta 摘要、**抓不到正文**；备用 `/doc_center/source/` 被 **robots.txt 拦**。两条路都堵。→ CANN 此项**统一记 2**；CUDA 静态站记 5。
   - **已纠正的错误**：早期给 D 可抓取性记 1、A/B/C 记 3*，是把"失败有没有咬到结果"误当成"可抓取性本身的差异"。它是公共常量；D 垫底真因是 ①可发现性 + ④二手厚度低，叠加这个公共短板才致命；A/B/C 靠厚二手绕过去了。
3. **"找得到"≠"抓得到"≠"够用"**：A/B/C 官方都搜得到(④≈4)、但都 SPA 抓不到(②=2)，只是搜索片段/二手够厚没触发短板。
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
| **`15_heatmap_hover.html`** | **当前主交互**：去掉点击楼层/FAB，改为**逐格悬浮**看详情（每格说明过程，低分说问题），类别在左列 |

**当前最新主文件 = `15_heatmap_hover.html`。**

---

## 7. 进行中的任务（未完成）

用户要求：**悬浮卡片要更具体**——不能只说"正文抽不出""在某平台找到"，要写清：
- 可抓取性：**具体抽到了什么 / 缺失什么**；
- 二手/官方源：**具体哪几篇**（标题 + 域名 + **日期**）、**版本号**；
- 这个深度要应用到**所有指标**，不只是官方一手源。

为此正在重新检索拿准确数据，准备据此做 `16`（在 15 基础上把每格 tooltip 写详细）。已重新拉到的具体数据见下方附录，**还需补**：CUDA A(TensorRT)、CUDA B(Nsight)、CUDA D(PyTorch custom ops)、CANN C(AOL/ATB) 的准确标题/日期。

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

_最后更新：本轮（正在为 file 16 收集 tooltip 的具体来源数据）。_
