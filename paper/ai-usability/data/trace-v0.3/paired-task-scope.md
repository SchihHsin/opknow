# Paired task scope / 任务对范围

The paired questions are functional analogies; the table does not assert controlled equivalence. Source questions are retained in Chinese.

| Task | CUDA question (G: ROCm/HIP) | CANN question | Requirement boundary |
| --- | --- | --- | --- |
| A | 我有一个训练好的 PyTorch 模型，怎么导出成 TensorRT engine 做推理部署？给出 PyTorch → ONNX → TensorRT 的完整步骤和命令。 | 我有一个 ONNX 模型，怎么在昇腾（Ascend）上转换成 .om 离线模型做推理部署？给出 ONNX → ATC → .om 的完整步骤和命令。 | Advanced reference and target-machine applicability require separate evidence |
| B | 我训练的 PyTorch 模型 GPU 利用率不高，怎么用 Nsight Systems 抓 timeline 定位性能瓶颈？给出采集命令和分析步骤。 | 我在昇腾上跑 PyTorch 模型想定位性能瓶颈，怎么用 msprof / Ascend PyTorch Profiler 采集并分析？给出代码和步骤。 | Commands and workflow interpretation are separate requirements |
| C | 我要做稠密矩阵乘 / 卷积，CUDA 上有哪些官方加速库（cuBLAS/cuDNN/cuSPARSE）？怎么选、怎么调用？ | 昇腾上做矩阵乘 / 卷积 / Transformer，有哪些官方算子加速库（AOL/ATB）？怎么选、怎么调用？ | Library overview does not establish invocation coverage |
| D | 怎么写一个自定义 CUDA kernel 并集成进 PyTorch（C++ extension）？给出完整步骤、setup.py 和注册代码。 | 怎么用 Ascend C 开发一个自定义算子并集成进 PyTorch（msOpGen/aclnn）？给出完整步骤。 | Check linked implementation material; do not infer site-wide absence |
| E | 我的 PyTorch/CUDA 程序报 `RuntimeError: CUDA error: device-side assert triggered`，怎么定位是哪一行、哪个 kernel 出的问题？ | 我在昇腾上跑训练/推理，报 `EZ9999` 之类的错误码，怎么定位根因、怎么排查？ | Specific diagnosis is not supported by the generic entry |
| F | 怎么用 PyTorch 做多机多卡分布式训练（DDP + NCCL）？给出初始化、启动命令和环境变量。 | 怎么在昇腾上做多机多卡分布式训练（DDP + HCCL）？给出初始化和启动方式。 | Local multi-node configuration remains task-specific |
| G | 跨平台移植 | 我有一份 GPU(PyTorch CUDA) 训练脚本，怎么迁移到昇腾 NPU？给出迁移方式和工具。 | Separate migration analogy, not CANN/CUDA benchmark pair |
| H | 怎么用 TensorRT 把模型量化成 INT8 做推理部署？给出校准（calibration）流程。 | 怎么在昇腾上把大模型量化（W8A8）做推理部署？给出量化工具和流程。 | Find operational guidance in the appropriate official repository |
| I | 我的 PyTorch 跟 CUDA/cuDNN 版本对不上，怎么查 PyTorch、CUDA toolkit、cuDNN、驱动之间的版本配套关系？ | 我装了 torch_npu 报版本不匹配，怎么查 CANN、torch_npu、固件驱动、PyTorch 之间的版本配套关系？ | Pairing table supports named relations; complete local stack fit is separate |
| J | Ubuntu 上从零安装 CUDA toolkit，装完要配哪些环境变量（PATH / LD_LIBRARY_PATH）？ | Ubuntu 上从零安装 CANN toolkit，装完要 source 哪个 set_env.sh、配哪些环境变量？ | Select the path for the actual installation |
| K | 怎么用 nvidia-docker / NGC 镜像跑一个带 GPU 的 PyTorch 容器？要装 nvidia-container-toolkit、加 `--gpus` 吗？ | 怎么用昇腾官方镜像 / Ascend docker 跑一个带 NPU 的 PyTorch 容器？要挂哪些 `/dev` 设备、用 ascend-docker-runtime 吗？ | Mount table alone is not a full container launch command |
| L | 我的自定义 CUDA 算子结果和 CPU/PyTorch 参考不一致，怎么定位数值精度问题（逐层/逐元素比对）？ | 我的昇腾算子输出和标杆不一致，怎么用昇腾精度比对工具（msaccucmp / 精度比对 / dump）定位？ | Data conversion alone does not complete numerical comparison |
| M | TensorRT/CUDA kernel 处理动态 shape 输入怎么做（optimization profile / 运行时 shape）？ | Ascend C 自定义算子做动态 shape，Tiling 怎么写、TilingData 怎么定义和传递？ | Different subgoals; conceptual/structural material should not require a runnable command |
| N | TensorRT/CUDA 里算子融合（layer/kernel fusion）怎么发生、怎么观察和控制？ | 昇腾 GE 图编译里算子融合规则怎么看、怎么自定义融合 pass（UB 融合/图融合）？ | Configuration switches do not by themselves establish custom-pass implementation |
| O | 我写了个自定义算子，怎么注册进 PyTorch 让 `torch.ops` 能调（TORCH_LIBRARY / dispatcher / autograd 注册）？ | 我用 Ascend C 写了算子，怎么注册成 aclnn 接口并集成进 torch_npu / PyTorch 让框架能调？ | Readable alternate source precedes the later navigation-only entry check |
| P | PyTorch 训练怎么开混合精度（AMP）？`torch.cuda.amp.autocast` / GradScaler 怎么用？ | 昇腾上 PyTorch 训练怎么开混合精度？用 torch_npu 的 amp / apex，loss scale 怎么配？ | Match example API to installed version |
| Q | PyTorch 训练报 CUDA out of memory，怎么排查和优化显存（max_split_size_mb / 梯度检查点 / empty_cache）？ | 昇腾训练报 NPU out of memory，怎么排查和优化显存（PYTORCH_NPU_ALLOC_CONF / 梯度检查点 / 显存碎片）？ | Allocator settings cover one branch of the broader OOM question |
| R | 我的模型在 GPU 上训练 loss 不收敛 / 出现 NaN，怎么系统排查（梯度爆炸/学习率/数据）？ | 我的模型迁到昇腾 NPU 后 loss 不收敛 / 精度对不齐 GPU，怎么排查（loss scale / 溢出检测 / 算子精度）？ | General accuracy guidance and a concrete diagnostic case have different scope |
| S | 怎么把模型部署成推理服务？用 Triton Inference Server / TensorRT，怎么配 model repository 和起服务？ | 怎么把模型在昇腾上部署成推理服务？用 MindIE / 昇腾推理服务，怎么配和起服务？ | Connect service startup to model/configuration requirements |
| T | 我用 TensorRT/Triton 部署模型，怎么配置动态 batch / 动态 shape 推理（optimization profile / dynamic batching / min-opt-max shape）？ | 我用昇腾 MindIE/ACL/ATC 部署模型，怎么配置动态 batch / 动态 shape 推理（dynamic_dims / 分档 / 动态分辨率）？ | Batching and dynamic-shape requirements must be distinguished |
| U | 我的 kernel occupancy 低、访存受限，怎么用 Nsight Compute 分析并优化（memory coalescing / shared memory / occupancy calculator / bank conflict）？ | 我的昇腾算子访存是瓶颈、AI Core 利用率低，怎么分析并优化（UB/L1 数据搬运、Cube/Vector 利用率、double buffer）？ | Deep task with useful official material; not proof of version-insensitivity |
| V | 我想用 CUDA streams + 异步内存拷贝（`cudaMemcpyAsync`）让 H2D/D2H 数据传输与 kernel 计算重叠，怎么做（stream / event / pinned memory）？ | 我想在昇腾上让数据传输与计算重叠，怎么做（多 stream / 异步内存拷贝 `aclrtMemcpyAsync` / event 同步）？ | API reference is not an end-to-end overlap demonstration |
| W | 我的多卡 NCCL all-reduce 通信慢，怎么调优（NCCL_ALGO/NCCL_PROTO/拓扑感知/NVLink/NCCL_DEBUG 诊断）？ | 我的多卡 HCCL all-reduce 通信慢，怎么调优（HCCL 拓扑/RoCE 网络/HCCL_ALGO/hccn_tool 诊断）？ | Algorithm descriptions do not supply the full tuning-command workflow |
| X | 我的 CUDA kernel 报 illegal memory access / 内存越界，怎么用 compute-sanitizer（旧 cuda-memcheck）定位是哪一行越界？ | 我的昇腾算子内存越界 / 踩内存，怎么用昇腾工具（msSanitizer / mem check / 算子内存检测）定位？ | Examples support available guidance, not execution on the target device |
| Y | 我的模型/代码从一代 NVIDIA GPU 迁到另一代（如 Volta→Hopper、不同 compute capability），要注意什么（重编译 `-arch/sm_xx`、PTX 兼容、TensorRT engine 不跨架构复用）？ | 我的模型从一款昇腾芯片迁到另一款（如 310→910 或不同昇腾型号），要注意什么（soc_version 重新 ATC 转 .om、算子支持差异、精度/性能重测）？ | Parameter evidence covers part of the broader migration requirement |
| Z | 请讲清 CUDA 编程模型的核心概念（grid / block / thread / warp / SM / global·shared·register memory），它们怎么映射到硬件？ | 请讲清昇腾 AI Core 编程模型的核心概念（AI Core / Cube / Vector / Scalar 单元、UB·L1·GM 存储层级），并与 CUDA 的 grid/block/thread/SM/shared-mem 概念怎么对应？ | CANN counterpart does not cover all requested memory/hardware concepts in this return |

A differs in conversion starting artifacts; M compares TensorRT optimization profiles with CANN TilingData; H compares different quantization workflows. Event counts are not controlled comparative task costs.
