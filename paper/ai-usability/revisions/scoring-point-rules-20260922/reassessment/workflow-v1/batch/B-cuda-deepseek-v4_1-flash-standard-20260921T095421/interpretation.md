# B-cuda-deepseek-v4_1-flash-standard-20260921T095421

M1: 5 (scored). 第1次搜索第1位即命中 NVIDIA Nsight Systems User Guide。

M2: 3.3333333333333335 (scored). 3个独立官方URL合并重试后分别评定：User Guide直接正文但含[...]截断为4，Get Started明确为提取报告3，Analysis Guide明确为不完整提取报告3；第三方抓取不纳入官方均值。

M3: 4 (scored). Official sources give a default profile capture route, trace/capture options, analysis command and gap/low-utilization diagnosis. Full manual timeline-navigation detail remains absent. The alternative stats syntax gap is recorded but is not itself an extra requirement imposed on the original task.

M4: 5 (scored). Get Started 官方页直接给出 Nsight Systems 2026.5.1、CUDA 12.0+（CUDA trace）、Driver 418+、Turing+ 及平台/OS条件；这些是本题 Nsight Systems 采集环境所需的完整直接规则，无需另拼兼容矩阵。

M5: 5 (scored). 固定包搜索结果去重后有7个相关独立第三方来源组，达到 n≥6。

M6: 3 (scored). The complete visible third-party ledger contains one independently supported profile/trace command and twelve assertions without sufficient fixed-packet support. A generic help flag, a differently spelled report identifier, or CLI postprocessing description does not verify the exact help invocation, legacy identifiers, or GUI workflow. Historical stats behavior is not declared false without a matching version. This is mixed support, not a truthfulness certification.

M7: None (unscorable). 先验回答给出 nsys profile、capture-range、CUDA/NVTX 和 timeline 分析主流程，但 -o/--output、nsys stats 完整语法及 torch.cuda.cudart/NVTX API 在固定包中未逐字核实；这些事实可能改变可执行性档位，不能给4分。

M8: 1 (scored). 3次搜索+6次抓取共9次实际派发，C≥9。

M9: 4 (scored). 最终答案给出 Nsight Systems 2026.5.1 及 CUDA 12.0+、Driver 418+、Turing+ 的官方范围；组件有依据但仍是范围而非单一锁定版本。

M10: None (unscorable). 最终答案给出 profile、stats/analyze/recipe 主路线，但答案明确承认 profile -o/--output 和 nsys stats usage 未从固定官方正文核实；这些未决语法可能改变是否可执行，不能把它当成纯环境替换或直接判内容错误。

M11: None (unscorable). M7 为 unscorable，按规则不能计算综合指数；M10 不进入 M11 公式。
