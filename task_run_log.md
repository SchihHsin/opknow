# 任务真跑过程记录（CANN vs CUDA · AI 可用性）

> 本文件记录**每个开发任务的实际检索过程**：用的问题、每一步 web_search / web_fetch、命中了什么、按指标怎么打分。
> 方法：每个任务设计**本质相同、仅技术栈不同**的一对问题，用我（Claude）平常解答问题的真实工作流跑一遍，如实记录——能实测就实测，抓不到就如实说「受阻」。
> 指标定义见 `18_metric_definition.html`；热力图见 `17_official_site_focus.html`。
> 工具说明：`web_search` = 一轮检索；`web_fetch` = 抓取某 URL 正文（用小模型把 HTML 转写）。日期：2026-06-10。

---

## 中途重要修正：②可抓取性是「子树相关」，不是平台公共常量

跑 A 时做了一次**活体复核**（不是凭旧记录），结论推翻了此前「hiascend `/document/detail/` 全站 SPA、②统一记 2」的说法：

| 页面 | 子树 | web_fetch 正文 |
|---|---|---|
| A `quickstart_18_0012`（商用 80RC2） | `quickstart/` | **抓到** ✓（atc 命令 + 参数表 + npu-smi 步骤） |
| A `quickstart_18_0010`（社区 800alpha001） | `quickstart/` | **抓到** ✓（同上，换版本号一致） |
| A ATC 参考 `atlasatc_16_0001` | `devaids/auxiliarydevtool/` | SPA ✗（只回导航 + meta） |
| B msprof `atlasprofiling_16_0010` | `devguide/devtools/` | SPA ✗ |
| C AOL `operatorlist_0001` | `apiref/aolapi/` | SPA ✗ |
| D Ascend C `atlas_ascendc_10_0006` | `devguide/opdevg/` | SPA ✗ |

**规律（quickstart 可抓 2/2，深层 SPA 4/4）：**
- `quickstart/` 子树 = 服务端渲染，正文可抓。
- `devaids/` `devguide/` `apiref/` 等深层子树 = 客户端 SPA，只回导航 + meta，正文缺失；备用 `/doc_center/source/` 仍被 robots 拦。

**含义**：SPA 短板**恰好卡在前沿 / 参考深层页**（算子开发、Profiling、API 参考），而入门 quickstart 不受影响——这让「前沿差距被拉满」这一中心论点更精准，而非削弱。据此：A.cann ② 由 2→4、③由「受阻」→实测分；B/C/D 仍 2 / 受阻（其核心 how-to 在深层 SPA 页）。

---

## 任务 A · 模型转换 / 导出

**版本敏感度：高**

**使用的问题（本质相同，仅栈不同）：**
- **CUDA**：「我有一个训练好的 PyTorch 模型，怎么导出成 TensorRT engine 做推理部署？给出 PyTorch → ONNX → TensorRT 的完整步骤和命令。」
- **CANN**：「我有一个 ONNX 模型，怎么在昇腾（Ascend）上转换成 .om 离线模型做推理部署？给出 ONNX → ATC → .om 的完整步骤和命令。」

### CUDA 侧过程

1. **web_search**：`PyTorch model export to TensorRT engine ONNX trtexec deployment steps`
   - 命中：NVIDIA 官方 *Quick Start Guide*（docs.nvidia.com）、官方 *Transformer Engine — Export to ONNX and inference using TensorRT*（2.15）、二手 Medium(zergtant)、GitHub(sithu31296/PyTorch-ONNX-TRT)、Seeed wiki 等。**1 轮即官方 + 多篇二手齐备**。
   - 片段已给出三段式：`torch.onnx.export()`（opset_version / dynamic_axes）→ 编译 engine → `trtexec --onnx=<f> --saveEngine=<f>`。
2. **web_fetch**：`docs.nvidia.com/.../quick-start-guide.html`（静态站）
   - **正文实测抓到**：`trtexec --onnx=resnet50/model.onnx --saveEngine=resnet_engine.engine --stronglyTyped` 等完整命令；完整 C++/Python 运行时代码（反序列化 → 推理 → 取输出）。
   - 缺：「常用命令行旗标」全表为跳转链接、未内联。

**CUDA-A 评分**：①5 ②5 ③5(实测) ④4 ⑤5 ⑥5 ⑦先验4 ⑧成本5(1搜) ⑨5 ⑩5 → 综合**高**。

### CANN 侧过程

1. **web_search**：`昇腾 Ascend ONNX 转 om 模型 ATC 工具 推理部署 步骤 命令`
   - 命中：阿里云(developer.aliyun.com/article/1662723，**2025-05-06**，动静态 shape)、知乎(zhuanlan/p/393169777)、**hiascend 官方** quickstart_18_0012(商用80RC2) 与 quickstart_18_0010(社区800alpha001)、博客园×2、CSDN。官方搜得到但**夹在二手中、非绝对置顶**。
   - 片段已给出：`atc --model=resnet50.onnx --framework=5 --output=resnet50 --input_shape="actual_input_1:1,3,224,224" --soc_version=<soc_version>` + 各参数说明 + `source set_env.sh` + `npu-smi info` 取 soc_version。
2. **web_fetch**：hiascend `quickstart_18_0012`（商用80RC2，`quickstart/` 子树）
   - **正文实测抓到**（推翻旧「SPA抓不到」）：完整 atc 命令 + `--model/--framework/--output/--input_shape/--soc_version` 参数说明表 + `npu-smi info` 查询步骤。
3. **web_fetch 复核**：换版本 `quickstart_18_0010`（社区800alpha001）→ 同样抓到，一致。
4. **web_fetch 对照**：ATC 完整参考 `atlasatc_16_0001`（`devaids/` 子树）→ **SPA、正文缺失**（AIPP 配置、完整参数表抽不到）。

**含义**：模型转换的**常用路径 how-to 就在可抓的 quickstart 里**，只有 AIPP / 高级参数的**穷尽参考**落在 SPA 的 devaids 页。

**CANN-A 评分（据本次实测修正）**：①4 **②4(quickstart 可抓，仅深层参考 SPA)** **③4(实测：命令+参数表+npu-smi；缺穷尽 AIPP 参考)** ④4 ⑤4 ⑥先验3 ⑦成本5(1搜) ⑧3 ⑨4 → 综合**中高**。
版本号跨度证据：8.0.RC2 / 8.0.RC3 / 800alpha001 / 旧 V100R020C10 / 5.0.1 并存（④版本清晰仍弱）。

**A 小结**：差距小。两边模型转换都好查、官方都搜得到；CANN 的入门正文这次实测**可抓**，命令统一，综合中高。SPA 在 A 上**没**咬到结果（核心在 quickstart）。

---

## 任务 B · Profiling 定位瓶颈

**版本敏感度：中**

**使用的问题（本质相同，仅栈不同）：**
- **CUDA**：「我训练的 PyTorch 模型 GPU 利用率不高，怎么用 Nsight Systems 抓 timeline 定位性能瓶颈？给出采集命令和分析步骤。」
- **CANN**：「我在昇腾上跑 PyTorch 模型想定位性能瓶颈，怎么用 msprof / Ascend PyTorch Profiler 采集并分析？给出代码和步骤。」

### CUDA 侧过程

1. **web_search**：`Nsight Systems profile PyTorch GPU bottleneck nsys profile command steps timeline`
   - 命中：NVIDIA dev-discuss(PyTorch Developer Mailing List)、**mcarilli GitHub gist**(经典 nsys 命令集)、Medium(Yuanzhe Dong 分步)、Harvard Kempner Handbook、Practical ML(arikpoz，2025-05-25)、Modular GPU Puzzles。**1 轮即官方论坛 + 多篇高质二手齐备**。
   - 片段已给出整条命令：`nsys profile --delay 10 --duration 10 --pytorch=autograd-shapes-nvtx --python-sampling=true --backtrace=none python train.py`，以及 timeline 看 CUDA HW 行找周期性空隙的分析法。
2. **web_fetch**：`docs.nvidia.com/nsight-systems/UserGuide/index.html`（静态站）
   - **正文实测抓到**：`nsys [global-options] profile [options] [application]` 完整语法 + 选项全表（`--trace/--sample/--backtrace/--capture-range/--duration/--delay/--cuda-memory-usage` 等，含取值说明）。
   - 缺：官方页**未内联具体执行示例命令**（示例在 mcarilli gist 等二手里，已搜到）。

**CUDA-B 评分**：①4(官方论坛非绝对置顶，但二手极厚) ②5 ③5(实测：完整选项表；示例命令由 gist 二手补) ④4 ⑤5 ⑥5 ⑦先验4 ⑧成本5(1搜) ⑨5 ⑩5 → 综合**高**。

### CANN 侧过程

1. **web_search**：`昇腾 Ascend PyTorch Profiler msprof 采集 性能瓶颈 定位 步骤 命令`
   - 命中：**hiascend 官方**(CANN商用版700 `modeldevpt/ptmigr/AImpug_000068`)、CSDN×4、MindSpore 教程、Gitee(ascend/pytorch 训练调优指南)、昇腾社区专区。官方搜得到、夹在二手中。
   - 片段已给出：msprof 是各工具底座；Ascend PyTorch Profiler 对标 GPU 用法（CPU/NPU activities + schedule）；msprof-analyze 的 module_analysis 分层定位。
2. **web_fetch**：hiascend `AImpug_000068`（商用700，**`modeldevpt/ptmigr/` 子树**）
   - **正文实测抓到（重要新发现，推翻"Profiling 页一律 SPA"）**：完整 `torch_npu.profiler.profile(...)` 代码（`activities=[CPU,NPU]`、`schedule(wait=1,warmup=1,active=2,repeat=2,skip_first=10)`、`tensorboard_trace_handler("./result")`、`experimental_config` 配 `AiCMetrics.PipeUtilization`/`ProfilerLevel.Level1`）+ 三种采集方式（TB 自动解析 / export_chrome_trace / 离线 analyse）+ 参数说明表。
   - 对照：原 msprof 命令参考 `atlasprofiling_16_0010`（`devguide/devtools/` 子树）= SPA，正文缺失。

**含义（与 A 同构）**：面向 PyTorch 用户的 Profiling **常用 how-to（torch_npu.profiler）就在可抓的 `modeldevpt/` 子树**；只有 msprof 原生命令的穷尽参考落在 SPA 的 `devguide/` 页。**可抓取性确认是"子树相关"，不是平台公共常量**——B 与 A 都命中可抓子树。

**CANN-B 评分（据本次实测修正）**：①4 **②4(modeldevpt 可抓，仅 msprof 原生参考 SPA)** **③4(实测：torch_npu.profiler 完整代码+三方式+参数表；缺 msprof 原生穷尽参考)** ④3(商用700/社区80RC3alpha003/8.1RC1/MindStudio7.0RC2 等并存) ⑤4 ⑥先验3 ⑦成本5(1搜) ⑧3 ⑨4 → 综合**中高**。
亮点：Ascend PyTorch Profiler 与 PyTorch-GPU 用法**几乎逐项对标**（with / schedule / on_trace_ready），迁移成本低。

**B 小结**：差距小。两边面向 PyTorch 的 profiling 都好查、官方都搜得到；CANN 的 PyTorch Profiler 正文这次实测**可抓且完整**，且 API 对标 GPU。SPA 只咬到 msprof 原生命令参考（非主路径）。

---

## 任务 C · 算子库选型

**版本敏感度：低**

**使用的问题（本质相同，仅栈不同）：**
- **CUDA**：「我要做稠密矩阵乘 / 卷积，CUDA 上有哪些官方加速库（cuBLAS/cuDNN/cuSPARSE）？怎么选、怎么调用？」
- **CANN**：「昇腾上做矩阵乘 / 卷积 / Transformer，有哪些官方算子加速库（AOL/ATB）？怎么选、怎么调用？」

### CUDA 侧过程

1. **web_search**：`CUDA math libraries cuBLAS cuDNN cuSPARSE matrix multiply convolution how to choose call`
   - 命中：**cuBLAS 13.3 官方文档**(docs.nvidia.com)、**cuSPARSE 13.2 官方**、siboehm 经典 worklog、abhik.ai、ToolScopeAI、MATLAB GPUCoder。官方库文档**直接命中**。
   - 片段已给出清晰选型：稠密 GEMM→cuBLAS（>90% 峰值）、卷积/池化/归一化→cuDNN（FFT/Winograd/implicit-GEMM 可选）、稀疏→cuSPARSE（但 DL 形状不适用）。映射干净、职责清楚。
2. **web_fetch（先验已强，未逐一新 fetch；引用既有实测）**：CLAUDE.md 记录 cuBLAS 官方页静态可抓——完整 API 签名 + 状态码/参数表 + 两段 C 示例。

**CUDA-C 评分**：①5(官方库文档直接命中) ②5 ③5(实测：API 签名+参数表+示例) ④4 ⑤5 ⑥5 ⑦先验5(库选型是通识、训练覆盖密) ⑧成本5(1搜) ⑨5 ⑩5 → 综合**高**。

### CANN 侧过程

1. **web_search**：`昇腾 AOL ATB 算子加速库 矩阵乘 卷积 Transformer 选型 调用 aclnn`
   - 命中：**hiascend 官方**(ATB `doc_center/.../ascendtb_0001`、MindIE 安装加速库页)、**Gitee `ascend/ascend-transformer-boost` 蓝区代码仓**、CSDN×3(含 ATB 实现原理/代码级实战)、AtomGit、华为云 bbs。命名体系搜得到。
   - 片段已给出选型骨架：AOL（NN/BLAS/DVPP 等基础算子库，对标 cuBLAS/cuDNN）、ATB（Transformer/大模型，封装 Encoder/Decoder + 矩阵乘/注意力优化，上层对接 PyTorch/MindSpore/Paddle）、TBE（较老）。
2. **web_fetch**：hiascend ATB `ascendtb_0001`（**`doc_center/source/` 路径**）
   - **部分抓到（新发现：doc_center 非一律被 robots 拦）**：抓到 ATB 能力概述 + 三大接口机制（基础算子 Operation / 插件 Plugin / 图算子 Graph）+ 框架支持。
   - **缺**：具体算子列表、调用示例代码（这些落在二手 Gitee 仓 + CSDN 代码级文章里，已搜到）。
   - 对照：AOL 算子列表参考 `operatorlist_0001`（`apiref/aolapi/` 子树）= 早测 SPA，穷尽算子表抽不到。

**含义**：算子库**选型这一层（叫什么、怎么对标、怎么对接框架）官方概述可抓 + 二手极厚**；只有**穷尽算子签名表**落在 SPA(apiref)。选型任务对穷尽表依赖低，所以短板没咬到结果。

**CANN-C 评分**：①4(命名体系官方搜得到) ②4(ATB 概述可抓，仅 AOL 穷尽算子表 SPA) ③3(实测：抓到概述+接口机制，缺算子列表/调用码；二手补) ④4(C 版本敏感度低，命名相对稳) ⑤4(Gitee 蓝区仓+CSDN 厚) ⑥先验3 ⑦成本5(1搜) ⑧4 ⑨4 → 综合**高**。

**C 小结**：差距小。选型是通识层任务，两边命名体系都查得到、映射清楚（cuBLAS↔AOL-BLAS、cuDNN↔AOL-NN、transformer↔ATB）；CANN 二手（Gitee 官方蓝区仓）厚，绕过 apiref 的 SPA。综合高。

---

## 任务 D · 自定义算子开发

**版本敏感度：高**

**使用的问题（本质相同，仅栈不同）：**
- **CUDA**：「怎么写一个自定义 CUDA kernel 并集成进 PyTorch（C++ extension）？给出完整步骤、setup.py 和注册代码。」
- **CANN**：「怎么用 Ascend C 开发一个自定义算子并集成进 PyTorch（msOpGen/aclnn）？给出完整步骤。」

### CUDA 侧过程

1. **web_search**：`custom CUDA kernel PyTorch C++ extension setup.py complete steps tutorial`
   - 命中：**PyTorch 官方教程多版本**(docs.pytorch.org `cpp_custom_ops` 2.12 / `cpp_extension` 2.7 / 历史 1.0~1.8)、**官方 GitHub `pytorch/extension-cpp`**(完整可跑示例)、apxml 课程、个人博客。**官方教程 + 官方示例仓双命中、绝对置顶**。
   - 片段已给出完整范式：C++ 文件 pybind11 绑定 + 声明 .cu → .cu 写 kernel → `setup.py`(`CUDAExtension` + `BuildExtension` cmdclass) → `python setup.py install` → import 调用。目录结构清楚。
2. **web_fetch（引用既有实测）**：CLAUDE.md 记录 `cpp_custom_ops` 官方页静态可抓——setup.py + C++ 算子定义 + `STABLE_TORCH_LIBRARY` 注册 + 分步骤齐全（注意 2.10+ ABI-stable vs 旧 THCudaTensor）。

**CUDA-D 评分**：①5(官方教程+官方示例仓置顶) ②5 ③5(实测：setup.py+注册+分步全) ④4(2.10+ ABI 变更已标注) ⑤5(extension-cpp 等多仓) ⑥5 ⑦先验5 ⑧成本5(1搜) ⑨5 ⑩5 → 综合**高**。

### CANN 侧过程

1. **web_search**：`昇腾 Ascend C 自定义算子开发 msOpGen aclnn PyTorch 集成 完整步骤`
   - 命中：知乎(zhuanlan/p/1946230593403745334「接入 PyTorch 有几种实现方式」)、ai6s.net(Add 算子实战)、**MindSpore 官方**(op_custom_ascendc AOT)、CSDN/昇腾专区×3、Monsoon 博客(910B 自定义算子)、天翼云、华为云 bbs(CANN 训练营)。**官方 hiascend 主文档未直接置顶**，靠二手 + MindSpore 拼。
   - 片段已给出步骤骨架：环境(CANN≥7.0.RC1 + msopgen) → `msopgen gen -i add_custom.json -c ai_core_Ascend910B1 -lan cpp -out ./custom_op` 生成工程 → 写核函数 + Tiling(GM/Local/寄存器三级) → `bash build.sh` 编包 → 部署 OPP → cpp_extension 方式 `TORCH_LIBRARY`/`TORCH_LIBRARY_IMPL`/`PYBIND11_MODULE` 接 PyTorch → 调 autogen 的 aclnn API。
2. **web_fetch（引用既有实测）**：hiascend Ascend C how-to `atlas_ascendc_10_0006`（**`devguide/opdevg/` 子树**）= **SPA，正文缺失**——核函数模板、完整 add_custom.json、Tiling 写法、编译部署细节均抽不到（穷尽 how-to 恰好压在 SPA 深层页）。

**含义（与 A/B/C 相反——短板这次咬到了）**：D 的核心价值在**穷尽的开发 how-to**（核函数/Tiling/工程结构/注册细节），而它**正好落在 SPA 的 `devguide/opdevg/` 深层页**；官方入门 quickstart 这层覆盖不到算子开发深度；二手虽有（CSDN/ai6s/MindSpore/Gitee）但**版本号散乱（80RC2alpha001/80RC3/82RC1alpha003）、门槛高、彼此不完全一致**。①可发现性低 + ④版本乱 + ②深层 SPA **三者叠加**，短板被拉满。

**CANN-D 评分**：①3(官方主文档未置顶，靠二手拼) **②2(核心 how-to 在 devguide/opdevg SPA，无可抓子树兜底)** **③受阻·无法实测(正文取不回，按口径记中性态，不打推断分)** ④2(版本号严重散乱) ⑤3(二手有但碎、门槛高) ⑥先验3(Ascend C 训练覆盖薄) ⑦成本5(1搜但需多方拼) ⑧3 ⑨2 → 综合**中**。

**D 小结**：**差距被拉满**。CUDA 侧官方教程+示例仓置顶、静态可抓、版本变更标注清楚；CANN 侧官方主文档不置顶、核心 how-to 压在 SPA 深层页（无 quickstart/modeldevpt 那样的可抓子树兜底）、版本号散乱、二手碎片化。这是四个任务里唯一"SPA 短板真正咬到结果"的——印证中心论点：**前沿/深层开发场景差距最大**。

---

## 四任务总览（本次真跑后）

| 代号 | 任务 | CUDA | CANN | 可抓取性是否咬到结果 | 关键 |
|---|---|---|---|---|---|
| A | 模型转换/ATC | 高 | 中高 | 否（核心在可抓 quickstart） | 命令统一、好查 |
| B | Profiling | 高 | 中高 | 否（核心在可抓 modeldevpt，torch_npu.profiler 对标 GPU） | PyTorch Profiler 几乎逐项对标 |
| C | 算子库选型 | 高 | 高 | 否（选型层官方概述可抓+二手厚） | 命名映射清楚、Gitee 蓝区仓厚 |
| D | 自定义算子 | 高 | 中 | **是（核心 how-to 压在 devguide/opdevg SPA）** | 版本散乱+不置顶+深层SPA 三叠加 |

**跨任务规律（实测，比旧记录更精确）：**
- **②可抓取性是"子树相关"不是平台常量**：`quickstart/`(A)、`modeldevpt/ptmigr/`(B)= 服务端渲染可抓；`doc_center/`(C-ATB)= 部分可抓（概述有、算子表无）；`devaids/`(A-ATC参考) `devguide/devtools/`(B-msprof) `apiref/aolapi/`(C-AOL) `devguide/opdevg/`(D-AscendC) = SPA。
- **SPA 短板恰好卡在"前沿/参考深层页"**：A/B 有可抓子树兜住主路径 how-to → 短板没咬到；C 靠厚二手绕过；**只有 D 没有兜底子树、核心 how-to 整个压在 SPA → 差距拉满**。
- 这让中心论点更精准：**不是 CANN 文档一律抓不到，而是越深入前沿开发、越掉进 SPA + 二手碎片 + 版本散乱的三重坑**。
