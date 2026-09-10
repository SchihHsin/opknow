# Task-linked application of the protocol / 协议的任务级应用

Each row links a stated requirement to a selected original tool return. The full eleven-field records are in applications.json. Historical ordinal values and categorical evidence codes are different outputs; no new composite score is calculated from these categories.

| Unit | Event | M2 delivered content | Documented elements (M3/M10) | Requirement boundary |
| --- | --- | --- | --- | --- |
| A.cuda | MAIN-E007 | substantive_text_obtained | trtexec commands and runtime code | Advanced reference and target-machine applicability require separate evidence |
| A.cann | MAIN-E013 | substantive_text_obtained | ATC command, parameter explanations and npu-smi step | Advanced reference and target-machine applicability require separate evidence |
| B.cuda | MAIN-E023 | substantive_text_obtained | nsys profile syntax and collection options | Commands and workflow interpretation are separate requirements |
| B.cann | MAIN-E022 | substantive_text_obtained | torch_npu.profiler code and output/export settings | Commands and workflow interpretation are separate requirements |
| C.cuda | MAIN-E009 | substantive_text_obtained | cuBLAS signatures and parameter descriptions | Library overview does not establish invocation coverage |
| C.cann | MAIN-E028 | substantive_text_obtained | ATB architecture and capabilities; no operator list or invocation example in this return | Library overview does not establish invocation coverage |
| D.cuda | MAIN-E010 | substantive_text_obtained | PyTorch C++/CUDA setup and operator code | Check linked implementation material; do not infer site-wide absence |
| D.cann | MAIN-E014 | navigation_only | Selected return contains navigation/metadata without implementation code | Check linked implementation material; do not infer site-wide absence |
| E.cuda | compiled only | not_reassessed_from_a_selected_read | Search results are retained; no separate official WebFetch selected for this task | Specific diagnosis is not supported by the generic entry |
| E.cann | MAIN-E039 | substantive_text_obtained | Error definition, cause N/A and two generic package/environment checks | Specific diagnosis is not supported by the generic entry |
| F.cuda | compiled only | not_reassessed_from_a_selected_read | Search results and compiled assessment retained | Local multi-node configuration remains task-specific |
| F.cann | MAIN-E046 | substantive_text_obtained | HCCL initialization, device settings and launch guidance | Local multi-node configuration remains task-specific |
| G.cuda | compiled only | not_reassessed_from_a_selected_read | ROCm/HIP search and compiled assessment retained | Separate migration analogy, not CANN/CUDA benchmark pair |
| G.cann | MAIN-E049 | substantive_text_obtained | Supported PyTorch versions and transfer_to_npu limitations | Separate migration analogy, not CANN/CUDA benchmark pair |
| H.cuda | compiled only | not_reassessed_from_a_selected_read | Search and compiled assessment retained | Find operational guidance in the appropriate official repository |
| H.cann | MAIN-E047 | substantive_text_obtained | Quantization algorithms rather than a deployment command sequence | Find operational guidance in the appropriate official repository |
| I.cuda | I-A02-E008 | substantive_text_obtained | Driver requirements in release notes; overview alone lacks the matrix | Pairing table supports named relations; complete local stack fit is separate |
| I.cann | I-A02-E005 | substantive_text_obtained | CANN/PyTorch/torch_npu pairing table | Pairing table supports named relations; complete local stack fit is separate |
| J.cuda | J-A02-E003 | substantive_text_obtained | PATH and library-path commands | Select the path for the actual installation |
| J.cann | J-A02-E004 | substantive_text_obtained | set_env.sh commands for root and non-root installations | Select the path for the actual installation |
| K.cuda | K-A01-E003 | substantive_text_obtained | NGC docker run invocation | Mount table alone is not a full container launch command |
| K.cann | K-A02-E008 | substantive_text_obtained | Default device and host-library mount table | Mount table alone is not a full container launch command |
| L.cuda | L-A02-E007 | substantive_text_obtained | assert_close signature, tolerances and formula | Data conversion alone does not complete numerical comparison |
| L.cann | L-A02-E005 | substantive_text_obtained | msaccucmp convert syntax and parameter table | Data conversion alone does not complete numerical comparison |
| M.cuda | M-A02-E003 | substantive_text_obtained | Optimization-profile configuration and runtime dimensions | Different subgoals; conceptual/structural material should not require a runnable command |
| M.cann | M-A02-E008 | substantive_text_obtained | TilingData structure declarations and examples | Different subgoals; conceptual/structural material should not require a runnable command |
| N.cuda | N-A02-E009 | substantive_text_obtained | Official blog explains vertical/horizontal fusion | Configuration switches do not by themselves establish custom-pass implementation |
| N.cann | N-A02-E003 | substantive_text_obtained | Fusion configuration arguments and rule descriptions | Configuration switches do not by themselves establish custom-pass implementation |
| O.cuda | O-A01-E003 | substantive_text_obtained | Dispatcher schema and implementation registrations | Readable alternate source precedes the later navigation-only entry check |
| O.cann | O-A01-E005 | substantive_text_obtained | YAML registration, EXEC_NPU_CMD and build elements | Readable alternate source precedes the later navigation-only entry check |
| P.cuda | P-A01-E004 | substantive_text_obtained | AMP recipe with autocast and scaler | Match example API to installed version |
| P.cann | P-A01-E009 | substantive_text_obtained | NPU AMP adaptation and scaler code | Match example API to installed version |
| Q.cuda | Q-A01-E007 | substantive_text_obtained | Allocator options and their descriptions | Allocator settings cover one branch of the broader OOM question |
| Q.cann | Q-A01-E006 | substantive_text_obtained | NPU allocator parameters and constraints | Allocator settings cover one branch of the broader OOM question |
| R.cuda | R-A01-E005 | substantive_text_obtained | Numerical accuracy guidance | General accuracy guidance and a concrete diagnostic case have different scope |
| R.cann | R-A01-E004 | substantive_text_obtained | NaN/overflow case material and diagnostic settings | General accuracy guidance and a concrete diagnostic case have different scope |
| S.cuda | S-A01-E003 | substantive_text_obtained | Model-repository layout and startup command | Connect service startup to model/configuration requirements |
| S.cann | S-A01-E004 | substantive_text_obtained | MindIE startup command and success indication | Connect service startup to model/configuration requirements |
| T.cuda | T-A02-E009 | substantive_text_obtained | Dynamic batching configuration | Batching and dynamic-shape requirements must be distinguished |
| T.cann | T-A02-E005 | substantive_text_obtained | ATC batch-size values and runtime setter requirement | Batching and dynamic-shape requirements must be distinguished |
| U.cuda | U-A02-E005 | substantive_text_obtained | Memory workload analysis guidance | Deep task with useful official material; not proof of version-insensitivity |
| U.cann | U-A02-E011 | substantive_text_obtained | Double-buffer explanation and buffer initialization example | Deep task with useful official material; not proof of version-insensitivity |
| V.cuda | V-A02-E004 | substantive_text_obtained | Asynchronous transfer, streams and pinned-memory requirements | API reference is not an end-to-end overlap demonstration |
| V.cann | V-A02-E009 | substantive_text_obtained | Async copy signature, stream parameter and constraints | API reference is not an end-to-end overlap demonstration |
| W.cuda | W-A02-E003 | substantive_text_obtained | NCCL algorithm variables and options | Algorithm descriptions do not supply the full tuning-command workflow |
| W.cann | W-A02-E007 | substantive_text_obtained | HCCL algorithm explanations | Algorithm descriptions do not supply the full tuning-command workflow |
| X.cuda | X-A02-E003 | substantive_text_obtained | Compute Sanitizer command and line-information options | Examples support available guidance, not execution on the target device |
| X.cann | X-A02-E005 | substantive_text_obtained | msSanitizer commands and output example | Examples support available guidance, not execution on the target device |
| Y.cuda | Y-A02-E003 | substantive_text_obtained | Architecture compilation flags and compatibility guidance | Parameter evidence covers part of the broader migration requirement |
| Y.cann | Y-A02-E008 | substantive_text_obtained | soc_version values and device-specific parameter information | Parameter evidence covers part of the broader migration requirement |
| Z.cuda | Z-A02-E015 | substantive_text_obtained | Thread/block/grid and memory definitions | CANN counterpart does not cover all requested memory/hardware concepts in this return |
| Z.cann | Z-A02-E006 | substantive_text_obtained | SPMD/block concepts | CANN counterpart does not cover all requested memory/hardware concepts in this return |
