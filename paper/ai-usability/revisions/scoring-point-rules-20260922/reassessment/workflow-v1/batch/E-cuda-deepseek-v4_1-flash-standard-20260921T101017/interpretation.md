M1: 2 (scored) 首次相关官方结果在第3次查询第4位。

M2: 3.625 (scored) 按八个官方fetch最终表示计分：[2,3,3,5,5,5,5,1]：入口页仅标题/导航，两个提取返回是excerpt（第二页明确为组织化Extracted Content），PyTorch CUDA页也是分析性摘录，四个源码返回正文，1.13.0路径为404。

M3: 5 (scored) Official extracts and source bodies together cover blocking to localize the caller, memcheck invocation/filtering/line info, DSA file/line/kernel launch reporting and instrumentation/hardware limitations. Coverage is based on content, not a claim that the fetched extracts were full pages.

M4: 3 (scored) 已取得CUDA toolkit匹配、PyTorch运行时变量与当前源码条件，但DSA变量改名/引入版本和完整软件组合未锁定。

M5: 5 (scored) Distinct articles kept separate regardless of shared domain/topic. Only qq420/Tencent2469157 identical-title reproduction candidate enumerated; repeat URLs merge. All counts>=6.

M6: 3 (scored) Complete synchronization, GPU assertion and CPU/GPU async-stack claims checked against official semantics and DSA code. NCCL-specific later manifestation lacks packet support. Midword continuations and tutorial promises excluded without completing them; all identifiable technical clauses covered.

M7: 1 (scored) 先验给出CUDA_LAUNCH_BLOCKING和sanitizer等正确片段，但把TORCH_USE_CUDA_DSA=1说成运行时开关；固定包当前源码直接读取PYTORCH_USE_CUDA_DSA，因此该关键定位方法错误，按关键主张被可靠证据否定计1。

M8: 1 (scored) 4搜索+8抓取=12。

M9: 3 (scored) 最终答案给出CUDA toolkit匹配与DSA当前main条件，但变量重命名引入版本和wheel构建配置未核实。

M10: 3 (scored) Concrete commands supplied, but saved code prints Launch stacktracing disabled when gather_launch_stacktrace is true, conflicting with the final promise that enabling PYTORCH_CUDA_DSA_STACKTRACING shows the CPU launch stack. Resolve or qualify this behavior. TORCH_DSA_KERNEL_LAUNCH limitation is already stated. Lack of execution is separately recorded, not a deduction.

M11: 62.565888 (scored) Calculated from corrected adjudicated M1–M8 point inputs; not a probability.
