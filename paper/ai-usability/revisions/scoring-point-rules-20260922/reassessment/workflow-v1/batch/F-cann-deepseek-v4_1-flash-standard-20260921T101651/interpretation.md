M1: 5 (scored) The first query rank-1 result is a relevant official TorchNPU multi-card training document.

M2: 3.2 (scored) The five final official fetches score [2,5,2,5,2]: 6.0.RC1 and both launch-demo URLs returned title/navigation only, while 26.0 multi-GPU and 7.2 multi-node pages returned direct bodies. The ForceInjection and Gitee fetches are third-party and excluded from the official-fetch mean.

M3: 5 (scored) The direct official 26.0 and 7.2 bodies cover device binding, HCCL process-group initialization, DDP/sampler integration, HCCL port reservation and network setup, and concrete two-node torchrun commands. The missing title-only 6.0/launch pages do not remove this complete main route.

M4: 3 (scored) Official pages identify TorchNPU branches and link CANN9 installation, but do not establish complete PyTorch/torch_npu/CANN selection relations. Missing optional torch_npu_run syntax is not the version deduction.

M5: 5 (scored) After merging blob/raw and same-URL discoveries and excluding identified official-example reproduction, remaining independent content groups stay above the >=6 threshold. Possible official reproduction retained as ownership uncertainty without changing the score.

M6: 1 (scored) A saved community executable shell example has an unmatched done and NNONES typo; static syntax check fails. This unresolved operational contradiction takes priority1. Other qualified assertions are separately supported or checked unsupported; unsupported does not mean false.

M7: 3 (scored) Prior gives supported HCCL initialization, device binding and node0 torchrun methods, but lacks the other-node invocation, DDP/data integration and cluster network setup needed for a full route. Score3 rests on correct fragments and actual omitted steps, not on self-reported uncertainty about optional variables.

M8: 1 (scored) Four WebSearch and eight WebFetch dispatches were recorded (C=12).

M9: 3 (scored) Final identifies selected official branches and a third-party environment, but does not establish the required PyTorch/torch_npu/CANN compatibility relationship for its main torchrun route.

M10: 3 (scored) The final provides concrete initialization, DDP/sampler and torchrun commands, but needs content fixes in the final itself: its multi-node sampler uses local devices_per_node/local_rank instead of global WORLD_SIZE/RANK, and the core snippet leaves required training objects implicit. The displayed shell block’s corrected syntax is not downgraded from raw Gitee defects; the official init/set_device ordering is not counted as an error.

M11: 71.633408 (scored) Calculated from adjudicated M1–M8 points; composite index, not probability.
