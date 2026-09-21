M1: 4 (scored) 第1次查询第2位出现相关昇腾官方迁移文档。

M2: 4.4 (scored) 五个独立官方fetch：4个直接正文=5，GPU2Ascend同名CANN页只有标题/导航=2，等权平均22/5=4.4。

M3: 5 (scored) 官方正文覆盖三种迁移方式、自动迁移约束、完整GPU2Ascend命令参数、安装与版本步骤；单个title-only fetch不改变其他正文覆盖。

M4: 3 (scored) CANN7.0 installation and automatic-migration pages give scoped PyTorch/TorchNPU choices; the full tool-command page is MindStudio7.0RC1 with only partial stack linkage. Necessary cross-page tool/CANN applicability is not fully resolved; absence of latest releases is not a deduction.

M5: 5 (scored) 去重后至少6个相关第三方内容组：迁移CSDN、迁移Juejin、迁移devpress、训练营CSDN、版本表转载组、安装CSDN；官方结果与官方代码仓库排除。

M6: 3 (scored) 可识别第三方主张中，三种迁移/transfer_to_npu主张获官方同向支持；精确2.4/CANN8.0、get_cann_version、驱动安装/段错误等完整限定未充分支持，无矛盾。

M7: None (unscorable) Device replacement and HCCL concepts have support. The tentative CLI is expressly uncertain, not a proven false assertion; positive torch.npu.amp/API installation assertions have no sufficient applicable verification in this packet, so correctness cannot be promoted to a complete correct route merely because no contradiction was found.

M8: 1 (scored) 实际派发9次：4次搜索、5次fetch。

M9: 3 (scored) Final supplies scoped CANN7.0/PyTorch/TorchNPU package choices and tool PyTorch versions, but explicitly leaves MindStudio7.0RC1 tool equivalence to chosen CANN7.0 route unverified. Missing latest releases alone does not lower the score.

M10: 3 (scored) Concrete automatic/tool routes are present. Manual-route instruction offers set_device as an alternative to moving x to NPU, which selects a device but does not move the existing tensor. Rewrite to retain tensor/model movement. Source-build alternative also omits the documented dependency-installation step. Content repair is required; lack of hardware execution is not a deduction.

M11: None (unscorable) Material prior API correctness cannot be established in fixed packet.
