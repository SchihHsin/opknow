# Supplementary analysis notes / 补充分析说明

## Scope and calculation / 范围与计算

The paper's main comparison uses 25 CANN/CUDA task pairs. Task G concerns migration to ROCm/HIP on the comparison side and remains a separately labelled analogy in the 26-row archive. The table below reports means from exact recomputation, rounded only after aggregation. These are descriptive summaries of the retained tasks.

正文主比较使用25组 CANN/CUDA 任务对。G 的对照侧涉及向 ROCm/HIP 迁移，在26行档案中作为单列类比保留。下表由未预先取整的公式结果求均值，最后统一舍入，描述保留任务的评分分布。

| Scope / 范围 | Calculation / 计算 | CANN | Comparison / 对照 |
| --- | --- | ---: | ---: |
| 25 pairs / 25对 | Historical composite confidence / 历史综合置信度 | 0.731902 | 0.922067 |
| 25 pairs / 25对 | Model-prior contribution set to zero / 模型自带知识贡献置零 | 0.602049 | 0.846369 |
| 26 archive rows / 26行档案 | Historical composite confidence / 历史综合置信度 | 0.736236 | 0.920449 |
| 26 archive rows / 26行档案 | Model-prior contribution set to zero / 模型自带知识贡献置零 | 0.605873 | 0.847663 |

The comparison column is CUDA throughout the 25-pair summary; the 26-row summary additionally includes G's ROCm/HIP analogy. Means of the already rounded historical scores differ slightly: 0.731920/0.922040 for 25 pairs and 0.736269/0.920423 for 26 rows. The paper uses exact recomputation before final rounding. Workflow means in Table 3 use the same 25-pair scope and the original workflow groups; differences are calculated before rounding the displayed means.

25对汇总的对照列均为 CUDA；26行汇总则额外包含 G 的 ROCm/HIP 类比。若对已舍入的历史评分再求均值，结果略有不同：25对为0.731920/0.922040，26行为0.736269/0.920423。正文使用精确复算后再舍入的结果。表3沿用25对范围及原工作流分组；差值在展示值舍入前计算。

## Formula sensitivity / 公式敏感性

M11, the Composite Confidence Score, aggregates the historical M1-M8 codes. M9 (response version specificity) and M10 (procedural actionability of responses) are reported separately. The formula combines official support O, third-party support C, and estimated model prior P through 1-(1-O)(1-C)(1-P), then applies source-version and inverse-effort factors.

M11 综合置信度汇总历史 M1-M8 编码；M9（回答版本明确性）与 M10（回答步骤可操作性）单列。公式以1-(1-O)(1-C)(1-P)合并官方支撑 O、第三方支撑 C 与模型自带知识估计 P，再乘以资料版本与逆向成本因子。

Setting P to zero examines the aggregate's sensitivity to its estimated model-prior channel while preserving all other inputs. It is an arithmetic change of assumption, rather than a new retrieval run or a measurement of a model without prior knowledge. When P=1, the channel-combination term is exactly 1 regardless of O and C. The final score can still vary through the version and effort factors, but differences in external support disappear from the channel-combination term. This saturation property is one reason to read the source indicators alongside the composite.

将 P 置零是在保持其他输入不变的条件下，检查汇总对模型自带知识估计的敏感性。这是改变公式假设的算术分析，并非重新检索或测量一个没有先验知识的模型。当 P=1 时，无论 O 和 C 如何，渠道合并项均等于1。最终评分仍受版本与成本因子影响，但渠道合并项不再体现外部支撑的差异。这一饱和性质说明了为何需要结合来源指标阅读综合分。

The factors are transformed ordinal codes. The formula expresses a compensatory aggregation choice; its values are not calibrated probabilities of answer correctness or execution success, and statistical independence of the channels has not been established.

公式因子来自有序编码的变换，表达渠道可相互补偿的汇总选择；其值未经答案正确性或执行成功率的概率校准，渠道之间的统计独立性也尚未确立。

## Historical codes and descriptive corrections / 历史编码与描述性修订

- **H.cuda source ownership:** the `nvidia-blog` entry is vendor-owned material. Excluding this known entry changes the mean third-party candidate count from 3.48 to 3.44 in the 25-pair CUDA records; CANN remains 3.16. The remaining entries are recorded candidates, with their independence, accessibility, and support for individual claims requiring inspection. Historical scores are retained unchanged.
- **A.cann acquisition count:** the structured record has `fetch=3` and `fetch_fail=0`, while the compiled log reports a missing body on the third read. The exact historical counting boundary cannot be recovered; both records and the discrepancy are preserved.
- **Content acquisition:** the descriptive profile groups `static` and `ssr` returns as core text obtained; `partial` remains partial, and `spa`/`robots` indicate core text not obtained. The unequal historical M2 scores remain in the full matrix and composite calculation for traceability. Access route is recorded independently and remains unknown where the archive does not identify it.

- **H.cuda 来源归属：** `nvidia-blog` 属于厂商官方材料。排除这一已知条目后，25对 CUDA 记录中的第三方候选来源均值从3.48变为3.44，CANN仍为3.16。其余条目为已记录候选来源，是否独立、可访问及支撑具体主张需要结合记录检查。历史评分保持不变。
- **A.cann 获取计数：** 结构化记录为 `fetch=3`、`fetch_fail=0`，汇编日志却记载第三次阅读未取得正文。无法恢复当时精确的计数边界，因此同时保留记录与差异说明。
- **正文获取：** 描述性剖面将 `static` 和 `ssr` 都归为核心正文已取得；`partial` 为部分取得，`spa`/`robots` 为核心正文未取得。完整矩阵及综合计算保留不等值的历史 M2 编码，以便追溯。访问路径独立记录，档案未标明时保持未知。

## Interpreting proposed improvements / 如何解释拟议改进

The findings distinguish improvements that affect many tasks from repairs to a localized acquisition or content gap. A hypothetical change to one or more input codes can illustrate the formula's response to an assumed improvement. Such calculations describe scenarios under fixed assumptions; they do not establish realized benefits, implementation costs, or return on investment. The paper therefore uses the observed task profiles to identify targets and proposes task-level checks for subsequent evaluation.

正文区分影响多项任务的改进与针对局部获取或内容缺口的修复。假设调整某些输入编码，可以展示公式如何响应设定的改进。这类计算描述固定假设下的情境，并不确立实际收益、实施成本或投资回报。因此，正文依据已观察的任务剖面定位改进对象，并提出后续可按任务检查的变化。

## Reproduction / 复现

The packaged `scripts/build_paper_analysis.py` reproduces the numerical summaries from frozen inputs using Python 3 and no network access. Inspect `data/generated/paper_analysis.json` for aggregate values and `data/generated/units.json` for task-side details. The source-ownership and count decisions are documented in `data/corrections.json`. These notes add interpretation without changing the frozen inputs or their manifest.

补充包中的 `scripts/build_paper_analysis.py` 使用 Python 3 从冻结输入复现汇总，无需联网。汇总见 `data/generated/paper_analysis.json`，逐单元数据见 `data/generated/units.json`，来源归属与计数处理见 `data/corrections.json`。本说明补充解释，不更改冻结输入及其清单。
