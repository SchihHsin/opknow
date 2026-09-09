# Retained task formulations

English targets below are editorial summaries of the archived Chinese formulations, not prompts used in new runs. Full archived question text is preserved in `../tasks.json`. G is retained as a migration analogy and excluded from the 25-pair summary. Workflow groups reproduce the original report's taxonomy; they are not asserted to be a sequential journey.

| ID | Task | Workflow group | CUDA-labelled target | CANN target | Paper scope |
| --- | --- | --- | --- | --- | --- |
| A | Model conversion and export | Inference and deployment | PyTorch → ONNX → TensorRT engine | ONNX → ATC → .om model | 25-pair summary |
| B | Profiling and bottleneck diagnosis | Performance optimization | Profile PyTorch with Nsight Systems | Profile PyTorch with msprof / Ascend PyTorch Profiler | 25-pair summary |
| C | Operator library selection | Operator development | Select and call CUDA libraries such as cuBLAS / cuDNN | Select and call Ascend libraries such as AOL / ATB | 25-pair summary |
| D | Custom operator development | Operator development | Develop a CUDA kernel and integrate it into PyTorch | Develop an Ascend C operator and integrate it into PyTorch | 25-pair summary |
| E | Error-code troubleshooting | Debugging | Locate a CUDA device-side assertion | Investigate an Ascend EZ9999 error | 25-pair summary |
| F | Distributed training configuration | Training | Configure PyTorch DDP with NCCL | Configure torch_npu DDP with HCCL | 25-pair summary |
| G | Cross-platform migration analogy | Migration and conceptual comparison | Migrate CUDA code / PyTorch GPU code to AMD ROCm with HIP tools | Migrate a PyTorch GPU training script to Ascend NPU | Analogy only (AMD ROCm / HIP on CUDA-labelled side) |
| H | Quantization for deployment | Inference and deployment | Quantize with TensorRT INT8 post-training calibration | Quantize an Ascend large model to W8A8 | 25-pair summary |
| I | Version compatibility diagnosis | Environment and installation | Resolve PyTorch / CUDA / cuDNN / driver compatibility | Resolve CANN / torch_npu / firmware / driver / PyTorch compatibility | 25-pair summary |
| J | Installation and environment variables | Environment and installation | Install CUDA Toolkit and configure Ubuntu environment variables | Install CANN Toolkit and configure set_env.sh / environment variables | 25-pair summary |
| K | Container setup | Environment and installation | Run a GPU PyTorch container using NVIDIA container tooling | Run an NPU PyTorch container using Ascend Docker Runtime | 25-pair summary |
| L | Operator numerical-accuracy diagnosis | Operator development | Compare a custom CUDA operator with CPU / PyTorch reference output | Compare an Ascend operator with reference output using accuracy-comparison tools | 25-pair summary |
| M | Dynamic shapes and tiling | Operator development | Handle dynamic shapes in TensorRT / CUDA kernels | Define and pass TilingData for a dynamic-shape Ascend C operator | 25-pair summary |
| N | Operator fusion | Operator development | Observe and control TensorRT / CUDA layer or kernel fusion | Inspect and customize Ascend GE / UB fusion rules | 25-pair summary |
| O | Operator registration and framework integration | Operator development | Register an operator in PyTorch using TORCH_LIBRARY / dispatcher / autograd | Register an Ascend C operator as an aclnn interface and integrate it into torch_npu | 25-pair summary |
| P | Mixed-precision training | Training | Configure PyTorch AMP / autocast / GradScaler | Configure torch_npu AMP / apex and loss scaling | 25-pair summary |
| Q | Out-of-memory optimization | Training | Diagnose and reduce CUDA training memory use | Diagnose and reduce NPU training memory use | 25-pair summary |
| R | Accuracy and convergence diagnosis | Training | Diagnose GPU training non-convergence / NaNs | Diagnose non-convergence or accuracy differences after migration to Ascend | 25-pair summary |
| S | Inference service deployment | Inference and deployment | Configure and start Triton / TensorRT inference serving | Configure and start MindIE / Ascend inference serving | 25-pair summary |
| T | Dynamic-batch and dynamic-shape inference | Inference and deployment | Configure TensorRT / Triton optimization profiles and dynamic batching | Configure MindIE / ACL / ATC dynamic dimensions and batching | 25-pair summary |
| U | Memory-access and occupancy optimization | Performance optimization | Use Nsight Compute to diagnose occupancy and memory bottlenecks | Optimize AI Core utilization and UB / L1 transfers / double buffering | 25-pair summary |
| V | Overlapping computation and transfers | Performance optimization | Overlap transfers and CUDA kernels with streams / events / asynchronous copies | Overlap transfers and Ascend computation with streams / events / aclrtMemcpyAsync | 25-pair summary |
| W | Multi-device communication optimization | Performance optimization | Tune NCCL all-reduce communication | Tune HCCL all-reduce communication | 25-pair summary |
| X | Out-of-bounds memory diagnosis | Debugging | Locate illegal memory accesses with Compute Sanitizer | Locate Ascend operator memory errors with msSanitizer | 25-pair summary |
| Y | Migration across chip generations | Migration and conceptual comparison | Migrate across NVIDIA GPU generations / compute capabilities | Migrate across Ascend chip models / soc_version settings | 25-pair summary |
| Z | Programming-model concepts | Migration and conceptual comparison | Explain CUDA grid / block / warp / SM and memory hierarchy | Explain Ascend AI Core units and memory hierarchy in relation to CUDA | 25-pair summary |
