M1: 4 (scored) The first query has a relevant official PyTorch translation at rank 2 (and another at rank 3); the rank-1 DeepWiki result is third-party.

M2: 3.7142857142857144 (scored) Seven independent official fetches score [3,3,3,4,5,5,3]. Analysis/extraction returns remain excerpts even when they claim completeness; the DDP tutorial has an explicit [...] omission, while the multi-node and multi-GPU tutorials provide direct bodies.

M3: 5 (scored) Official bodies cover the requested route: initialize an NCCL process group, bind one GPU per process, wrap DDP, shard input with DistributedSampler/set_epoch, launch the same torchrun rendezvous command on all nodes, and set NCCL diagnostics/interfaces. The task does not require every unrelated collective or every NCCL variable.

M4: 3 (scored) The packet identifies PyTorch v2.15.0 unstable and v2.14.0 tutorial/API material plus NCCL 2.31.2, but no complete official CUDA/PyTorch/NCCL compatibility relation or exact stack selection is available.

M5: 5 (scored) The deduplicated search inventory has at least six independent relevant third-party URL/content groups; the sulao entry remains ownership/content uncertain, yielding possible counts [6,7], which both map to the >=6 band.

M6: 3 (scored) The visible third-party claims were checked atomically: DeepWiki and Juejin generic DDP multi-GPU/multi-node applicability are supported by official tutorial text; the cnblogs qualitative acceleration claim has no quantitative or model-general support in the fixed packet. No key contradiction is established.

M7: None (unscorable) Prior has supported DDP/NCCL/device-binding fragments, but its static --node_rank launch route and positive NCCL_IB_DISABLE/CUDA_VISIBLE_DEVICES/OMP_NUM_THREADS details are not sufficiently verified by captured materials. Expressly tentative API-history questions are not errors; init ordering alone is not treated as a proven defect. Material correctness uncertainty remains.

M8: 1 (scored) Actual dispatch log contains 3 searches and 7 fetches (C=10).

M9: 3 (scored) The final names PyTorch v2.14 documentation/tutorials and NCCL 2.31.2, but the required CUDA/PyTorch/NCCL stack compatibility and exact selected runtime are not locked.

M10: 3 (scored) The final gives concrete initialization, DDP, sampler, torchrun and environment examples, but requires content repairs: ddp_setup is only defined, checkpoint code uses model.module after wrapping a different variable, local gpu_id is unsafe for multi-node ownership, and the NCCL_IB_HCA exact-match explanation is wrong. Environment substitutions remain separate.

M11: None (unscorable) M7 is unscorable after fixed-packet adjudication; the composite index is not imputed.
