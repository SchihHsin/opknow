# C-cuda-deepseek-v4_1-flash-standard-20260921T100035

M1: 4 (scored). 第一轮第5位命中官方 NVIDIA CUDA Libraries 文档索引。

M2: 4.142857142857143 (scored). 七个官方fetch按实际表示等权平均为29/7。

M3: 3 (scored). 三库选型与概念完整，但GEMM参数和卷积主调用workflow缺正文。

M4: 3 (scored). 部分cuDNN矩阵、cuBLAS硬件/CUDA与cuSPARSE nvJitLink关系有依据，具体版本硬件接口关系仍缺。

M5: None (unscorable). Four definite independent content groups, possible fifth cuda-samples revision and sixth NBKomputer article. The two frontend topics remain separate. Ownership/deduplication changes the M5 band.

M6: 3 (scored). DeepWiki定位与Graph API可由官方支持；知乎CUTLASS限定无本包支持，完成可见断言核对后为部分支持。

M7: None (unscorable). legacy卷积/GEMM参数、cuSPARSE_OP_N及cublasSetMathMode layout替代含义无法仅凭本包核清关键流程档位。

M8: 1 (scored). 实际派发4次search+7次fetch=11，final中称8 fetch为错误。

M9: 3 (scored). cuDNN及硬件版本有依据，其余兼容关系未锁定。

M10: 3 (scored). 存在具体GEMM/legacy卷积代码但缺descriptor、output、workspace与数据准备，graph路线无具体操作。

M11: None (unscorable). M5和M7为unscorable，不能计算综合指数。
