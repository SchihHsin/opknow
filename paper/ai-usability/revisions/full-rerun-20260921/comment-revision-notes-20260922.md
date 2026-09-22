# 批注修改说明

日期：2026-09-22  
对应批注：`codex-clipboard-16537870-5b08-495b-a18d-19b539ee98a8.jpg`、`codex-clipboard-311d2482-49fe-467e-ad2b-67bf58e4f9a3.jpg`、`codex-clipboard-89eb2d9c-b71c-4e15-a5ab-d66f88ac5522.jpg`、`codex-clipboard-f875c54f-7c07-4b56-91d6-957843d7e523.jpg`

本文档记录四张审阅截图对应的修改位置和修改内容。截图中的旧稿文件名是 `manuscript-en-v0.2-before-indicator-rework-reviewed`；本次修改写入全量重跑后的中英文工作副本，未修改原始老版本网页。

## 批注一：相关研究没有说明为什么还需要本研究

批注指出，原相关研究主要说明问题重要，但没有交代既有研究的不足、本文相对于前人工作的增量价值，以及为什么需要一个新的研究和方法。

已修改位置：

- 中文：`manuscript-cn.md` → “相关研究与构念边界”下的“检索、归因与可得性构念”之前。
- English：`manuscript-en.md` → “Related Work and Construct Boundaries”下、定义构念之前。

新增内容明确区分了四类已有工作：开发者信息寻找与文档研究、AI回答或检索增强评价、Agent任务结果评价，以及开发者与AI建议交互研究。新增段落指出它们通常没有把以下内容放在同一条可追溯证据链中：

1. 发现了什么；
2. 工具实际返回了什么；
3. 哪些任务需求得到支持；
4. 版本关系是否足以定版；
5. 最终回答还需要怎样修正。

随后明确本文的增量不是再提出一个答案正确率，而是定义“面向 AI 的知识可得性”，在任务层连接来源、获取、证据支撑和回答属性，并用 CANN/CUDA 案例检验这个诊断框架能否定位文档和 Agent 的改进缺口。

## 批注二：直接进入11个指标，没有说明指标来源、关系和遗漏

批注指出，11项指标缺少选择逻辑，读者不知道指标之间是否重复，也不知道是否遗漏了重要方面。

已修改位置：

- 中文：`manuscript-cn.md` → “操作化与测量协议” → “十一项指标及其证据角色”下新增“指标选择逻辑与相互关系”。
- English：`manuscript-en.md` → “Operationalization and Measurement Protocol” → “Eleven indicators and their evidential roles”下新增“Indicator selection and relationships”。

新增内容把指标组织成任务知识链条：

| 层次 | 指标 | 诊断问题 |
| --- | --- | --- |
| 官方渠道 | M1–M4 | 能否发现、实际取得、充分解释，并建立版本适用关系？ |
| 第三方渠道 | M5–M6 | 有多少相关独立来源，关键说法是否有证据支持？ |
| 模型先验 | M7 | 不检索时，模型是否已经给出正确且覆盖任务的知识？ |
| 获取过程 | M8 | 取得这些材料实际付出了多少搜索和获取调用？ |
| 最终回答 | M9–M10 | 回答是否有据定版，操作方案还需多少补改？ |
| 综合摘要 | M11 | 如何透明汇总 M1–M8，且不解释为正确概率？ |

同时逐组说明了边界：M1 与 M2、M3 与 M4、M5 与 M6、M7 与检索后回答、M8 与答案质量、M9 与 M10 分别测量不同对象，不能互相替代。新增内容还明确列出本研究没有纳入的方面：人类文档导航易用性、开发者满意度或信任、端到端硬件执行成功率、延迟和 token 成本。这些不是被忽略，而是需要不同观察单位和独立证据的构念边界。

## 批注三：分级、权重和公式很细，但没有说明如何形成

批注指出，评分档位、权重和综合公式会影响结论，不能只给出结果，还要说明形成依据和方法过程。

已修改位置：

- 中文：`manuscript-cn.md` → “评分规则与综合置信度”下新增“量规与权重如何形成”。
- English：`manuscript-en.md` → “Scoring rules and composite confidence”下新增“How the rubric and weights were formed”。

新增内容说明形成流程：

1. 先界定构念和冻结任务需求；
2. 为每项指标规定评价对象、证据边界、缺失状态和可修复的判定条件；
3. 用试跑材料和边界案例检查容易混淆的分支；
4. 冻结评分规则；
5. 用结构检查、引文定位检查和算术检查验证执行一致性。

文中同时明确：

- 文献支持测量对象、证据边界、事实核验和聚合假设，但没有直接给出本研究的五档阈值；
- M11 渠道内相乘是为了保留发现、取得或支撑任一环节的限制；
- 渠道间 noisy-OR 用来表达官方、第三方和模型先验之间可能存在互补；
- 0.30 的版本系数和 0.10 的成本系数是预先指定的工作基线，不是从本批结果拟合出的最优权重；
- M11 未经概率校准，敏感性分析和限制单独报告。

此前新增的“指标项的文献依据”表也保留在指标表之后，逐项列出 M1–M11 的参考文献、借鉴范围和本研究自行规定的部分。新增的 `reddy2010` 和 `kadavath2022` 条目位于工作副本 `references.bib`。

## 批注四：案例部分过度像生态排名，弱化了论文核心目的

批注指出，论文核心应是帮助文档团队和 Agent 建设者定位知识缺口、改进知识供给和反馈；CANN/CUDA比较应是案例和分析手段，而不应成为论文唯一落脚点。

已修改位置：

- 中文案例标题改为“案例应用：用 CANN 与 CUDA 检验知识诊断框架”。
- English 案例标题改为“Case application: stress-testing the knowledge-diagnostic framework with CANN and CUDA”。
- 中英文案例开头新增说明：CANN/CUDA 是具有不同文档、版本和工具链条件的压力测试场景，目的在于检验指标能否定位可修复的知识缺口，而不是给生态做脱离任务范围的总体排名。
- “发现”章节标题改为“用跨生态对照定位知识条件”/“Using cross-ecosystem contrast to locate knowledge conditions”。
- 发现章节开头新增限定：跨生态差异是本任务集和访问配置下的诊断线索，不是构念的替代物，也不是生态整体能力排名。
- 中英文结论首段改为先陈述方法的核心用途：服务文档团队和 Agent 建设者，定位发现、正文交付、任务覆盖、版本关系、来源支撑和回答修复中的具体缺口；随后才说明 CANN/CUDA 案例及其有界的差异输出。

## 文献出处表

工作副本中的指标出处表明确了以下对应关系：

- M1、M5：Manning 等、Kelly、Treude；
- M2：Wang & Strong、Kohlschütter 等；
- M3、M6、M9、M10：Wang & Strong、RAGAs、FActScore、Uddin、Reddy；
- M4：Wang & Strong、Uddin、Maalej；
- M7：Kadavath、FActScore；
- M8：Kelly、OECD/JRC；
- M11：OECD/JRC、Boateng、AERA/APA/NCME。

文中明确区分“文献提供的概念或方法依据”和“本研究自行设定的阈值、权重与公式”，避免把引用误写成对本量规的直接验证。

## 产出文件

- 中文正文：[manuscript-cn.md](manuscript-cn.md)
- English 正文：[manuscript-en.md](manuscript-en.md)
- 中文阅读页：[manuscript-cn-review.html](manuscript-cn-review.html)
- English 阅读页：[manuscript-en-review.html](manuscript-en-review.html)
- 工作副本文献库：[references.bib](references.bib)

原始老版本 `paper/ai-usability/manuscript-cn-review-changes.html` 和 `paper/ai-usability/manuscript-en-review-changes.html` 未修改。

## 校验与提交

中英文阅读页已由 `scripts/render.py` 重新生成，Pandoc 引用解析正常。`scripts/validate.py` 的保护文件检查目前发现工作区原有的 `.DS_Store` 哈希与 `protected-files.json` 不一致；这些文件不在本次修改范围内，也未被修改。正文、引用和阅读页的静态生成已完成。

本说明文件与正文修改一起提交并 push。

## 2026-09-22补充：不确定性与根因诊断批注

新增批注指出，生态差异本身回答不了“所以应该怎么办”，还需要区分问题是文档没有提供、没有被找到、没有被取得、没有被识别，还是 Agent 在回答合成时出错。为此，中英文 Findings 章节新增“从差异到诊断：根因分类与不确定性”/“From differences to diagnosis: root causes and uncertainty”。

新增诊断表按以下组合解释结果：

- M1低：只说明本次查询和预算下没有发现相关官方入口，不能推出文档不存在；
- M1高而M2低：入口可见但正文交付或返回形态有问题，不能直接归因于文档内容缺失；
- M2可评而M3低：已取得正文没有覆盖冻结任务需求中的关键内容；
- M2/M3较高而M4低：操作内容存在，但必要的版本—组件适用关系缺失；
- M5高而M6低：来源数量不等于关键说法可核验；
- M7低而外部资料和最终答案较强：说明本题无检索先验不足，不能推断训练数据密度；
- 来源支持充分而M9/M10低：应检查回答定版、代码、参数和合成过程；
- 只有跨生态均值差异：只能作为条件化诊断信号，不能直接写成生态整体排名或因果结论。

正文还明确列出不确定性来源：任务起点和范围、模型能力与检索策略、搜索提供方和预算、页面返回形态、来源归属、评分判断以及每个模型每侧只有一次有效运行。每项改进建议都要求给出下一步验证，例如重查官方目标、补充独立来源核验、同模型重复或实际执行。
