# Domain evidence index for reassessment

建立日期：2026-09-22。用途：为后续 156 份重评快速定位原实验中已经保存的内容证据与归属核验材料。本文只索引已存在的 `inputs` 与原实验归档；没有联网，也没有读取旧 scores 或 reviewer 建议作为事实来源。这里不提供任何 M 分数。

## 使用边界

- `检索来源` 是原模型当时看到的 search/fetch 事件；它可支持“当时返回了什么内容”，不能把域名本身自动升级为官方归属。
- `reference` 是跨 run 或实验后的 ownership 核验材料，只能作为事后核验，不能回填成模型当时的检索来源，也不能扩大原模型的检索上下文。
- 引文均为保存文本中的逐字片段；省略处用 `…` 标明。URL、文件名和 `event_id` 是定位键。
- “不能确定”表示当前归档没有独立、足够的所有权证据；不等于断言该域名一定非官方。

## 域名与证据

### `asc.gitcode.com`

归类：Ascend C 文档镜像/托管内容；**归属不能仅由本归档确定**。原实验保存了完整 WebFetch 正文，但没有同一检索事件中的独立官方 ownership 证明。可作为内容证据，不能只凭域名写成“官方”。

- 文件：`paper/ai-usability/revisions/scoring-point-rules-20260922/reassessment/inputs/Z-cann-glm-5_3-standard-20260921T151251.json`
- event：`call_629fcd32435242cebc8da634.result`
- URL：`https://asc.gitcode.com/guide/programming_guide/programming_model/programming_model_overview.html`
- 逐字引文：`基于昇腾处理器的应用程序通常分为两部分：**Host代码**与**Device代码**。其中，Host代码运行在CPU上，负责设备资源管理、Host Memory与Device Memory间的数据搬运及任务调度等；Device代码运行在NPU（神经网络处理器）上，专门执行实际的计算任务。`
- 文件/event：同上，`call_3cedafe5c2064a6b9475f29f.result`
- URL：`https://asc.gitcode.com/guide/programming_guide/programming_model/ai_core_simd_programming/kernel_function.html`
- 逐字引文：`核函数（Kernel）是在设备侧并行执行的C/C++函数。它由主机端代码调用，调用时被实例化为多份并行副本，分别调度到多个AI Core上运行（每个AI Core被抽象为一个Block）。`
- 另有同一 run 的 `call_e6b5520b1c6f4a888e4c3fe4.result`（基本架构正文），可按 URL 定位；不重复展开引文。

### `pytorch.ac.cn` / `docs.pytorch.ac.cn`

归类：PyTorch 中文镜像/本地化文档内容；**镜像归属不能仅由本归档确定**。页面正文和搜索结果可证明保存时返回的技术内容，不单独证明域名所有权或官方授权。

- 文件：`paper/ai-usability/revisions/scoring-point-rules-20260922/reassessment/inputs/D-cuda-deepseek-v4_1-flash-standard-20260921T100330.json`
- event：`call_00_QfVWQJhhXrghGDbrt19L0943.result`
- URL：`https://pytorch.ac.cn/tutorials/advanced/cpp_extension.html`
- 逐字引文（连续子串 1）：`本教程自 PyTorch 2.4 起已弃用。`
- 逐字引文（连续子串 2）：`请参阅 PyTorch 自定义操作符`
- 同一事件中的逐字引文：`您用于构建 C++ 扩展的编译器必须与构建 PyTorch 的编译器 ABI 兼容。`
- 文件：`paper/ai-usability/revisions/scoring-point-rules-20260922/reassessment/inputs/F-cuda-deepseek-v4_1-flash-standard-20260921T101319.json`
- event：`call_00_T1hzOGcegMT8uO4LulVn7418.result`（search 结果；不是正文抓取）
- URL：`https://docs.pytorch.ac.cn/docs/2.14/elastic/run.html`
- 逐字引文：`torchrun 是主模块 torch.distributed.run 的 python 控制台脚本，在 setup.py 的 entry_points 配置中声明。`

### `docs.pytorch.org`（原实验中的直接英文文档域）

归类：原实验检索到的 PyTorch 直接文档域。此条只证明原实验返回/抓取的内容，不把本索引当作新的官方归属审计。

- 文件：`paper/ai-usability/revisions/scoring-point-rules-20260922/reassessment/inputs/F-cuda-deepseek-v4_1-flash-standard-20260921T101319.json`
- event：`call_00_4tQczy8LQgMB4eAk6ddq0145.result`
- URL：`https://docs.pytorch.org/docs/main/elastic/run.html`
- 逐字引文：`Changed in version 2.0.0: torchrun will pass the --local-rank=<rank> argument to your script.`

### `bbs.huaweicloud.com`（华为云开发者社区）

归类：平台托管的社区文章；**文章/作者的官方归属不能仅凭平台域名、署名或内容判断**。归档的博客页明确包含平台免责声明，因此文章内容可作技术内容证据，不能自动作华为官方立场证据。

- 文件：`paper/ai-usability/revisions/scoring-point-rules-20260922/reassessment/inputs/A-cann-kimi-k3-2-standard-20260921T095009.json`
- event：`WebFetch_9_b2d0fc77.result`
- URL：`https://bbs.huaweicloud.com/blogs/393282`
- 逐字引文：`昇腾张量编译器（Ascend Tensor Compiler，简称ATC）是昇腾CANN架构体系下的模型转换工具`
- 同一事件中的逐字引文：`它可以将开源框架的网络模型（例如TensorFlow、ONNX等）转换为昇腾AI处理器支持的模型文件（.om格式），用于后续的模型推理。`
- 同一原文保存的免责声明逐字引文：`【声明】本内容来自华为云开发者社区博主，不代表华为云及华为云开发者社区的观点和立场。`

### `developer.huaweicloud.com`（文章内的文件资源 host）

归类：华为云社区文章引用的 `FileServer` 图片/附件 host；**不能据此确定发布者、作者或技术内容的官方归属**。它只出现在已保存文章正文的资源 URL 中，不能替代文章页或独立 ownership 证据。

- 文件：`paper/ai-usability/revisions/scoring-point-rules-20260922/reassessment/inputs/I-cann-deepseek-v4_1-flash-standard-20260921T102748.json`
- event：`call_00_GYUCvrfrHf9M48qqOo2x5848.result`
- 关联文章 URL：`https://bbs.huaweicloud.com/blogs/454517`
- 逐字引文：`**3.确认固件驱动和CANN版本配套：**   点击[链接](https://www.hiascend.com/hardware/firmware-drivers/community?product=4&model=32&cann=8.1.RC1.beta1&driver=Ascend%20HDK%2025.0.RC1)`
- 说明：该 event 中的 `fileserver.developer.huaweicloud.com/FileServer/...` 是嵌入资源 URL；不要把它当作独立文档域。

## 事后 reference ownership 核验（不属于模型检索来源）

原实验目录：`/Users/hsin/Documents/Coding/ai-usability-benchmark/experiments/full-rerun-protocol-20260921/ownership-references/`。

- `index.json` 记录：`https://readthedocs.org/api/v3/projects/ascend/` → `official`，依据是 Read the Docs API 指向 `https://github.com/ascend/docs`。这是外部 ownership reference，不是任何模型 run 的 search/fetch event，不能回填到原答案的检索上下文。
- `huaweicloud-author-1560754383728560.html` 保存的页面标题/元描述逐字为：`昇腾CANN的博客_云社区-华为云`、`昇腾CANN在华为云社区的个人主页`。该档案核验只表明页面显示的账号名称和页面元数据；`index.json` 的结论仍为 `unknown`，因为未找到独立、可验证的官方账号标识。
- `huaweicloud-blog-393282.html` 保存的页面声明逐字为：`本内容来自华为云开发者社区博主，不代表华为云及华为云开发者社区的观点和立场。` `index.json` 对该文章归属结论为 `unknown`。

## 不能确定的域名清单（当前归档层面）

至少包括：`asc.gitcode.com`、`pytorch.ac.cn`、`docs.pytorch.ac.cn`、`bbs.huaweicloud.com` 的具体博主/文章、`developer.huaweicloud.com` 的 FileServer 资源。对这些域名，后续重评可引用保存的正文来判断“内容是否支持答案”，但不应仅据域名把来源标注为官方；若需要官方归属，应单独引用明确的 ownership reference，并标为 `reference`。
