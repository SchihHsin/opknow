M1: 5 (scored) First query rank1 is the relevant official multi-device training guide.

M2: 4.25 (scored) Three direct-body returns without observable fetch omission (5 each) and one title/rating-only return (2):17/4=4.25. Reused-code ellipses in0086 are explained examples, not missing page content.

M3: 3 (scored) NPU/HCCL initialization, samplers, network setup and launcher alternatives are explained in full sections. The main multi-node route still lacks explicit global-rank/world-size construction and complete matching per-node startup; the RC2 linked two-node appendix returned only its title. These are main workflow gaps rather than optional detail.

M4: 3 (scored) Official RC1/RC2 bodies state torchrun needs PyTorch>=1.11.0 and torch_npu_run only1.11.0; full TorchNPU/PyTorch/CANN pairing is absent, so launcher applicability is partial.

M5: 3 (scored) Three distinct third-party articles found in one query: devpress HCCL experience, hwcomputing multi-node instructions and forceinjection DDP tutorial. No visible reproduction identity across these entries.

M6: 3 (scored) HCCL role/use supported by official distributed-training sections; full replica/data/gradient statement lacks explicit support for every qualifier in saved examples. Checked unsupported is not false.

M7: None (unscorable) Correct HCCL initialization fragments are present, but asserted mandatory import order, old visibility-variable replacement by ASCEND_SLOG_PRINT_TO_STDOUT, HCCL_IF_IP and whitelist generator behavior lack fixed-packet verification. The=1 sample does not prove=0 invalid under a configured whitelist. These material correctness questions can change a key-error versus correct-fragment grade; preserve unresolved, not inferred false.

M8: 3 (scored) One search plus four fetch dispatches=5; score3.

M9: 3 (scored) Final identifies RC1/RC2 guide scope and torchrun>=1.11.0, but does not establish CANN/TorchNPU/PyTorch package pairing. The suggested interpretation of only1.11.0 as >= is explicitly unverified and cannot extend applicability.

M10: 3 (scored) Concrete DDP and network instructions exist, but global rank/world_size are undefined, the shell route sets onlyLOCAL_RANK, and the torchrun command remains standalone single-node. DataLoader import is also absent. These require code/launch additions beyond environment values.

M11: None (unscorable) M7 unresolved correctness blocks full point input.
