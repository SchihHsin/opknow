M1: 5 (scored) 第一轮第1位即为相关NVIDIA官方CUDA安装指南。

M2: 2.3333333333333335 (scored) Six URL-deduplicated official documents: four explicit analyses/extractions3 and two failed targets1. Same root URL retry uses last return. Wrongtarget failure and PDF bytes dropped are not title-only. Mean14/6.

M3: 3 (scored) 官方材料覆盖了部分主流程或命令，但抓取缺失使安装分支、完整变量解释或前提约束仍需补齐。

M4: 3 (scored) Saved13.4 Ubuntu instructions explicitly require a separate driver but give no applicable driver version relation for this toolkit.

M5: 2 (scored) One independent third-party tutorial; NVIDIA .cn PDF is official and identified translated installation guide is official-content reproduction.

M6: None (unscorable) Only independent third-party item has generic tutorial scope and an unfinished installation/download clause; no complete assessable technical assertion. Official/translated documentation is not third-party support.

M7: None (unscorable) Prior env-variable form is recognizable, but asserts apt nvcc installation into/usr/bin and no PATH setup, CUDA_HOME use and symlink/library behavior without applicable verification. Older-version uncertainty cannot be resolved from13.4 extraction alone. Do not count only supported fragments then assume main correctness.

M8: 2 (scored) 实际派发事件共8次，按成本档位计分。

M9: 3 (scored) 最终答案锁定CUDA 13.4路径并覆盖Ubuntu安装分支，但未锁定toolkit与驱动的具体兼容版本。

M10: 3 (scored) Final provides exports but omits a complete Ubuntu toolkit install route despite from-zero request. The continued LD_LIBRARY_PATH line has leading whitespace after newline: shell removes backslash-newline, leaving a separate word, so existing LD_LIBRARY_PATH is not concatenated correctly. Write one continuous quoted assignment and provide actual install steps.

M11: None (unscorable) No identifiable independent third-party claim; prior material assertions unverified.
