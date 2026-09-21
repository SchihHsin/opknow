M1: 5 (scored) First query rank1 is the translated reproduction of the official PyTorch multi-node tutorial; rank2 is original publisher. Reproduction classification concerns content, not control of the mirror domain.

M2: 4.666666666666667 (scored) 官方三个独立fetch分别为直接正文5、含明确[...]缺损的直接正文4、完整官方代码正文5；等权平均14/3。

M3: 5 (scored) The env/NCCL+torchrun rendezvous route has initialization/code, shared launch arguments, local/global identity, full launcher environment table and basic NCCL diagnostics. A second classic launcher syntax or the complete NCCL tuning catalogue is not required by this task.

M4: 3 (scored) 捕获了 PyTorch 2.14/cu130 文档版本标识，但没有完成 CUDA/PyTorch/NCCL 的全部适用关系。

M5: 2 (scored) 搜索摘要中仅1个相关第三方内容组（vk032503 GitHub）；docs.pytorch.ac.cn为官方镜像再现，官方仓库与文档不计第三方。

M6: None (unscorable) A related third-party repository is present, but its snippet contains only generic challenge/promotion and a truncated production-grade phrase. No identifiable key technical assertion can be checked; unscorable, not absence of third-party material.

M7: None (unscorable) 先验主流程正确，但tcp/file init_method、torchrun 1.9+/1.10 deprecated、NCCL_IB_DISABLE/NCCL_NET_GDR_LEVEL等关键适用断言在固定证据包中未核实；不同裁决会影响档位。

M8: 4 (scored) 实际派发4次：1 search + 3 fetch。

M9: 3 (scored) 最终答案锁定了 PyTorch 2.14/cu130 文档线，但没有锁定 NCCL/CUDA 所需全部适用版本关系。

M10: 3 (scored) Specific initialization and rendezvous launch route exists, but unqualified DataLoader has no import in supplied code and requires a content fix. Classic-method/default-init claims are not declared false from absent evidence; no-execution is not a deduction.

M11: None (unscorable) M6和M7均为unscorable，不能计算综合指数。
