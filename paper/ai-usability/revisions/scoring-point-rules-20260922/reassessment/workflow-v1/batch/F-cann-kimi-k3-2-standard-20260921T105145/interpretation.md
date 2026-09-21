M1: 5 (scored) 第1次查询第1位为相关昇腾官方文档。

M2: 5 (scored) 三个独立官方fetch均取得直接目标正文；0086中的“......”是示例明确说明复用前段代码的省略，不是工具抓取缺损。

M3: 3 (scored) 官方正文覆盖初始化和多种启动方式，但多机global-rank初始化/完整多机启动参数仍缺，单机示例的local_rank不能直接完成多机要求。

M4: 4 (scored) Official table specifies CANN/PyTorch/TorchNPU pairs; launcher rules separately constrain torchrun>=1.11.0 and torch_npu_run to1.11.0. Combining the selected launcher with a table row establishes the necessary stack. Multiple valid combinations are allowed; uniqueness is not required.

M5: 4 (scored) Five independent groups: q1devpressHCCL, HCCL fault article, hwcomputing multi-node article, q2version-pairing reproduction group and driver/CANN installation article. verse_armour is identifiable official-example reproduction and excluded.

M6: 3 (scored) HCCL distributed-training role/use is supported. High fault-frequency assertion, exact2.4.0.x/CANN8.0 pairing, segmentation-fault cause/remedy, get_cann_version checking and driver prerequisite lack full fixed-packet support. They are checked unsupported, not false.

M7: None (unscorable) Correct HCCL/DDP/device-binding fragments are supported and multi-node rank setup is incomplete. The positive prior claim that ASCEND_RT_VISIBLE_DEVICES controls visible cards is not verifiable in the fixed packet and can affect device selection correctness. Explicit questions about ascend-dmi/msnpureport are not treated as false assertions. Material prior correctness remains unresolved.

M8: 3 (scored) 实际派发5次：2 search + 3 fetch。

M9: 4 (scored) 最终答案给出6.0RC1下CANN/PyTorch/torch_npu具体配套范围，但没有把单一PyTorch版本锁为一个值。

M10: 3 (scored) 最终初始化代码world_size未定义且使用local_rank作为多机rank；torchrun示例只有单机standalone，缺多机nnodes/node_rank/master参数，需内容补写。

M11: None (unscorable) M7 material correctness remains unresolved; do not impute.
