# Interpretation — A-cuda-deepseek-v4_1-flash-standard-20260921T111713

## Scope and evidence boundary

本次修订只使用固定 packet `A-cuda-deepseek-v4_1-flash-standard-20260921T111713`；未重新检索、抓取或执行命令。先验回答仅用于 M7，最终回答仅用于 M9/M10，第三方说法及官方核对材料仅用于 M6。

## Adjudication

- **M1=5：** 第一次搜索第 1 位即为 NVIDIA 官方 ONNX 部署页。
- **M2=4.0：** 7 个官方 URL 合并重试后为 5、5、4、4、3、3、4；Support Matrix/PyTorch/Python API 有可观察缺损，Runtime/trtexec 是明确摘录报告。
- **M3=5：** 官方 ONNX 部署、Opset、Python API、Runtime 与 trtexec 材料覆盖导出、engine 构建、运行、动态 shape/精度与调试主流程。
- **M4=3：** TRT 11.x 的 ONNX 1.20、opset 9–25 和 SM 7.5+ 有依据，但 Support Matrix 交互行及所选 TRT↔CUDA 适用链路未取回。
- **M5=5：** 去重后 6 个相关第三方来源组，达到至少 6 组。
- **M6=unscorable：** 24项可见断言已核对；部分有官方支持，timingCache量化内容等检查后仍不获支持。Case 5 engine的batch模式与TensorRT代际没有锁定，不能将条件性冲突判为已确证矛盾。该事实会改变分档，因此保留不可评分；Runebook残片、文章计划和样例性能观察不补写为技术断言。
- **M7=unscorable：** 固定包已核查完毕，TensorRT 8/10 API迁移及Jetson soc_version断言仍无法判定；记录缺失具体反证/支持，不以低分代替未知。
- **M8=1：** 4 次搜索 + 8 次抓取 = 12 次派发。
- **M9=3：** 最终答案锁定 TRT 11.x、ONNX 1.20/opset 9–25、PyTorch exporter 与 SM 7.5+，但 TRT↔CUDA 适用关系仍缺。
- **M10=3：** 最终答案的 Python `build_engine` 没有 CLI 入口，runtime 片段缺少 engine_path/shape/buffer/stream 分配和拷贝同步，导出的 `resnet50_pytorch.onnx` 也未接到后续 `trtexec` 文件名；这些是内容补改，不是“未实际运行”扣分。
- **M11=unscorable：** M6 与 M7 均为 unscorable，按规则不能计算综合指数。

M6 的每项 `claim_evidence`、`support_evidence` 均为固定 packet event 的逐字子串，且支持与 claim 分开保存于 `facts.json`；没有用第三方材料自证。
