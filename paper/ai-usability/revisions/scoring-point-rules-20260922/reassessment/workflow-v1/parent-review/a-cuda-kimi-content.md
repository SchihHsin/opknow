# A-cuda-kimi-k3-2 内容核对（workflow-v1 / parent-review）

- run_id: `A-cuda-kimi-k3-2-standard-20260921T095515`
- 输入：`inputs/A-cuda-kimi-k3-2-standard-20260921T095515.json`
- 范围：完整读取 packet 的 source inventory、prior、final；复核 M2/M3/M4/M5/M6/M7/M8/M9/M10/M11。
- 证据边界：只使用固定 JSON 的 `sources`、`prior`、`final` 和派发记录；未执行硬件或新采集。

## parent adjudication

原独立 review 中建议 M4/M9 给 4 分不采纳。固定规则要求所有必要版本适用关系有依据；本包缺少 TensorRT 与 CUDA 的可核对映射，孤立的 CUDA 12.9 脚注不能补足该关系，因此 M4=3、M9=3。原独立 review 提出的 engine 文件名不一致也不采纳：final 实际包含保存 `resnet_engine_intro.engine` 的匹配构建命令，不能把该点当作必然错误。M7 的 TensorRT API（如 `BuilderFlag.kFP16`、`enqueue_v3/enqueueV3`）在固定包中未获证实，且可能影响方法档位，维持 `unscorable`，不以先验自述强给分。

## M3 官方正文详尽度：5

官方正文覆盖 PyTorch 导出 ONNX、ONNX 校验/简化、`trtexec` 构建 engine、helper 获取与修补、runtime 预测，以及 ONNX opset 和动态 shape 约束。版本关系另由 M4 评价，不因未执行硬件降低 M3。

证据包括：

- WebFetch_1_683b8443.result：`This subsection walks through the export steps. Once you have an ONNX file, follow the steps in [Example Deployment Using \`ONNX\`]`
- WebFetch_1_683b8443.result：`trtexec --onnx=resnet50/model.onnx --saveEngine=resnet_engine_intro.engine --stronglyTyped`
- WebFetch_1_683b8443.result：`Download the helper that provides \`ONNXClassifierWrapper\` into the same directory as \`resnet_engine_intro.engine\``
- WebFetch_8_4812079d.result：`--minShapes` / `--optShapes` / `--maxShapes` / `--shapes`

## M4 版本清晰度：3

ONNX 1.20.0、opset 9–25、TensorRT 11.x 和 GPU SM 7.5+ 有材料支持；TensorRT↔CUDA 的必要适用关系缺失，不能直接确定完整组合。

## M5 二手丰富度：5

已确认至少 6 个相关、独立的第三方内容组；另有归属不明候选，但是否纳入不改变 ≥6 档。torch2trt 等绕过题目指定 ONNX 路线的内容未计入。

## M6 二手可信度／一致性：3

已检查全部可识别关键说法。ONNX→TensorRT 路线和格式操作有可追溯支持；吞吐量比较和旧 `ExportOptions` API 说法没有本包核对支持。未发现已确证直接矛盾，未把未支持说法擅自判错。

## M7 模型自带知识：unscorable

先验包含 PyTorch→ONNX→TensorRT 主流程及 `torch.onnx.export`、`trtexec`、动态 shape 和 runtime 方向，但 `BuilderFlag.kFP16`、`enqueue_v3/enqueueV3` 及 TRT8/10 边界没有固定证据核实。这些属于方法性主张，可能改变档位，因此保留 `unscorable`。

## M9 版本可锁定性：3

final 给出 TensorRT 11.3、ONNX 1.20/opset 9–25 与 SM≥7.5，但 CUDA 12.9 脚注与 TensorRT 11.3 的关联未证实；必要组件仅部分有依据。

## M10 操作可执行性：3

final 有具体导出、engine 构建、helper 下载和预测方案；helper 元组返回补丁仍需补写代码，因而不满足仅替换环境值的 4 分条件。final 确实有保存 `resnet_engine_intro.engine` 的匹配构建命令，不判定文件名必然不一致。`dynamic_shapes` 键及裸 API 的适用性仍未核清，未声称运行通过。

## M11

M7 为 `unscorable`，综合指标不计算，保持 `unscorable`。

## 复核与限制

`facts.json`、`assessment.json`、`check.json` 已通过机械 check（`issues=[]`、`mechanical_pass=true`）。`review.json` 与 `review-receipt.json` 已按固定四文件哈希生成。限制是：M7 的旧版本 API 仍未证实；未执行硬件；本记录不是全面专家认证。每条本文件引文均来自固定 packet 的对应事件正文，未进行新采集。
