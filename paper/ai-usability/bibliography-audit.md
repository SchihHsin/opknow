# CHI 论文参考文献核验与引用边界

核验日期：2026-09-09。对应 `references.bib` 的 16 篇文献：保留原稿 11 篇，补充 5 篇构念直接相关文献。仅核验文献与可支持的引用范围，未重跑 CANN/CUDA 网页审计，也未改写正文。

本轮采用 Crossref、OpenAlex、ACL Anthology、NeurIPS/ICLR 官方论文集、arXiv 作者版本及 IBM Research 作者机构页面。**书目核实不等于全文精读**：下表逐项区分元数据与摘要阅读。这里提出的 related-work 比较仅使用已读摘要明确陈述的研究对象和评价维度，不将摘要之外的方法细节或结果补造成已知事实。本轮是围绕现稿的定向核验，不是完整的系统文献综述，也不能证明“首次提出”或“无相关工作”。

## 1. 必须修正的书目信息

1. **Robillard 2009 原稿混用了两条出版记录。** 正式卷期版的标题为 *What Makes APIs Hard to Learn? Answers from Developers*，IEEE Software 26(6), 27–34，DOI **10.1109/MS.2009.193**。原稿的 *The Answers of Developers* 和 DOI `10.1109/MS.2009.116` 对应另一条元数据不完整记录：Crossref 返回 2011 年、无卷期页；不能与正式版 2009 年卷期页拼接。现 BibTeX 已使用 `.193`。核验：[正式记录](https://api.crossref.org/works/10.1109/MS.2009.193)、[原稿所用记录](https://api.crossref.org/works/10.1109/MS.2009.116)。
2. **Ko 的作者姓名采用当前 Crossref 记录中的 Amy J. Ko**，不沿用历史姓名；原稿缩写 A. J. 本身不冲突。
3. 补齐 Sillito 2008 的 DOI `10.1109/TSE.2008.26`；补齐各论文的作者全名单或来源明确提供的姓名缩写，不再用 `et al.` 写入 BibTeX 作者字段。
4. **Vaithilingam 2022 属于 CHI Extended Abstracts**，不能改写成 CHI Papers 正会长文。RAGAs 2024 属于 EACL System Demonstrations，也应保留准确 track。
5. SWE-agent 官方 NeurIPS 页面已经给出 DOI `10.52202/079017-1601`，已收录。ReAct、WebArena、SWE-bench、Lewis 2020 的所核验会议记录未取得会议版 DOI，保留稳定 URL；没有把 arXiv 的 DOI 伪装成会议 DOI。

## 2. 原 11 篇核验表

| 原编号 / BibTeX key | 核验后的文献 | 核验源与阅读范围 | 本文可以用来支持 | 不可以据此声称 |
| --- | --- | --- | --- | --- |
| 1 / `brand2009` | Brandt, Guo, Lewenstein, Dontcheva & Klemmer. 2009. *Two Studies of Opportunistic Programming: Interleaving Web Foraging, Learning, and Writing Code*. CHI, 1589–1598. | [Crossref 元数据](https://api.crossref.org/works/10.1145/1518701.1518944)；[OpenAlex 摘要](https://api.openalex.org/works/https://doi.org/10.1145/1518701.1518944)。 | 编程中的在线信息获取、学习、提醒细节与写代码相互交织；开发任务不是一个孤立检索查询。 | 这项早期研究证明了今天开发者对 Agent 的委托方式；或它已测量 AI 的知识可得性。 |
| 2 / `ko2007` | Ko, DeLine & Venolia. 2007. *Information Needs in Collocated Software Development Teams*. ICSE, 344–353. | [Crossref](https://api.crossref.org/works/10.1109/ICSE.2007.45)；[OpenAlex 摘要](https://api.openalex.org/works/https://doi.org/10.1109/ICSE.2007.45)。 | 开发者的信息需求与信息来源受工作情境制约；所需知识未能取得可能导致任务延后。 | 同事知识不可得等价于网页正文不可抓取；本文已复现其开发者工作场景。 |
| 3 / `sillito2008` | Sillito, Murphy & De Volder. 2008. *Asking and Answering Questions during a Programming Change Task*. IEEE TSE 34(4), 434–451. | [Crossref](https://api.crossref.org/works/10.1109/TSE.2008.26)；[OpenAlex 摘要](https://api.openalex.org/works/https://doi.org/10.1109/TSE.2008.26)。 | 围绕具体变更任务刻画开发者问题及工具支持；支持以任务为分析单位的动机。 | 本文 26 任务是其 44 问题类型的验证、覆盖或直接继承；本稿没有建立这种映射。 |
| 4 / `robillard2009` | Robillard. 2009. *What Makes APIs Hard to Learn? Answers from Developers*. IEEE Software 26(6), 27–34. | [正式版 Crossref](https://api.crossref.org/works/10.1109/MS.2009.193)；原 DOI 的 [OpenAlex 摘要](https://api.openalex.org/works/https://doi.org/10.1109/MS.2009.116)描述 API 学习、资料与可信示例问题。正式版题名/卷页已核实；本轮未取得正式版全文作逐句比对。 | API 学习资料与示例是开发者工具可用性的相关研究背景。 | 以该摘要为依据引用正式版某页的精确句子；或声称它测量了 Agent 的版本核验能力。 |
| 5 / `vaithilingam2022` | Vaithilingam, Zhang & Glassman. 2022. *Expectation vs. Experience: Evaluating the Usability of Code Generation Tools Powered by Large Language Models*. CHI EA, 1–7. | [Crossref](https://api.crossref.org/works/10.1145/3491101.3519665)；[OpenAlex 摘要](https://api.openalex.org/works/https://doi.org/10.1145/3491101.3519665)，摘要报告 24 人研究。 | Copilot 可成为有用起点并节省在线搜索努力，但生成片段的理解、修改和调试仍可能困难。 | AI 助手普遍提高完成率/速度；本文已有对应开发者实验；现有审计分数能预测人类表现。 |
| 6 / `barke2023` | Barke, James & Polikarpova. 2023. *Grounded Copilot: How Programmers Interact with Code-Generating Models*. PACMPL 7(OOPSLA1), 85–111. | [Crossref 元数据及出版方摘要](https://api.crossref.org/works/10.1145/3586030)，摘要报告 20 人 grounded-theory 分析。 | 加速与探索两种使用模式，为 Agent 作为知识探索入口提供 HCI 背景。 | 该研究证明了本文的三渠道公式、版本折扣或文档改进收益；本文进行过 grounded-theory 用户研究。 |
| 7 / `lewis2020` | Lewis et al. 2020. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS 33, 9459–9474. | [NeurIPS 官方元数据及摘要](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html)。12 位作者已完整列入 BibTeX。 | 参数化与非参数化记忆相结合的技术背景；为何外部资料能参与生成。 | 模型参数知识可被直接观测为本文的⑦分数；参数、官方、第三方三源相互独立；RAG 能保证无幻觉。 |
| 8 / `yao2023` | Yao et al. 2023. *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR. | [arXiv v3](https://arxiv.org/abs/2210.03629v3)的元数据及摘要，页面明确说明 v3 为 ICLR camera-ready。OpenReview 页面/API 本轮受阻，未据此捏造内容。 | 交织推理轨迹与外部动作的 Agent 工作方式，是图 1 的技术背景之一。 | 本文观测到了模型内部真实推理过程；或其检索工具实现与 ReAct 实验配置相同。 |
| 9 / `zhou2024webarena` | Zhou et al. 2024. *WebArena: A Realistic Web Environment for Building Autonomous Agents*. ICLR, 15585–15606. | [ICLR 官方元数据及摘要](https://proceedings.iclr.cc/paper_files/paper/2024/hash/4410c0711e9154a7a2d26f9b3816d1ef-Abstract-Conference.html)。12 位作者已完整列入。 | 以网页任务完成的功能正确性评价 Agent 的代表性基准。 | WebArena 完全不研究工具、环境或外部知识；审计分可以与它的任务成功率直接比较。 |
| 10 / `yang2024sweagent` | Yang et al. 2024. *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*. NeurIPS 37, 50528–50652. | [NeurIPS 官方元数据、DOI及摘要](https://proceedings.neurips.cc/paper_files/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html)。 | Agent 可被视为有自身需求和能力的接口使用者；接口设计会影响 Agent 软件工程任务表现。该文是现稿“AI usability”主线的重要连接。 | “面向 Agent 设计接口”由本文首次提出；本文验证了网页或社区改造带来的性能增益；本文实现并测试了 SWE-agent。 |
| 11 / `jimenez2024swebench` | Jimenez et al. 2024. *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?*. ICLR, 54107–54157. | [ICLR 官方元数据及摘要](https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract-Conference.html)。官方页面大小写作 Real-world Github，BibTeX 仅规范专名大小写。 | 真实仓库 issue 修复与执行环境中的解决能力评价，说明它与供给侧任务审计的评价对象不同。 | 该论文只看流畅性或完全不分析上下文；本文综合分是 SWE-bench 式 issue 解决率。 |

## 3. 新增 5 篇及必要性

| BibTeX key | 文献与核验源 | 已读范围及可支持的陈述 | 引用边界 |
| --- | --- | --- | --- |
| `pirolli1999` | Pirolli & Card. 1999. *Information Foraging*. Psychological Review 106(4), 643–675. [Crossref](https://api.crossref.org/works/10.1037/0033-295X.106.4.643)。 | **本轮仅元数据核验**；APA 摘要/全文受阻，OpenAlex 未返回摘要。保留为信息寻径概念的理论出处。 | 不据此新增其具体实验结果、数学模型或对 Agent 的外推；需要这些细节时应补读原文。 |
| `ragas2024` | Es, James, Espinosa Anke & Schockaert. 2024. *RAGAs: Automated Evaluation of Retrieval Augmented Generation*. EACL System Demonstrations, 150–158. DOI [10.18653/v1/2024.eacl-demo.16](https://doi.org/10.18653/v1/2024.eacl-demo.16)。 | 已读 [ACL 官方摘要和书目](https://aclanthology.org/2024.eacl-demo.16/)。明确分别讨论检索的相关/聚焦上下文、生成对上下文的忠实利用、生成质量，并提供无参考标注的评价框架。 | **不能继续写“既有 RAG 评价只有单一检索命中率或最终答案正确性”。** RAGAs 的 reference-free 不等于其各项分数是经过校准的概率，也不验证本文公式。 |
| `ares2024` | Saad-Falcon, Khattab, Potts & Zaharia. 2024. *ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems*. NAACL-HLT Long Papers, 338–354. DOI [10.18653/v1/2024.naacl-long.20](https://doi.org/10.18653/v1/2024.naacl-long.20)。 | 已读 [ACL 官方摘要和书目](https://aclanthology.org/2024.naacl-long.20/)。区分 context relevance、answer faithfulness、answer relevance；使用合成训练数据、模型裁判及少量人工标注支持的 PPI。 | 不能称其完全无需人工标注；不能说现有评价从不分解检索/回答；不能把其可靠性移植给本文未校准的综合指标。 |
| `gao2023alce` | Gao, Yen, Yu & Chen. 2023. *Enabling Large Language Models to Generate Text with Citations*. EMNLP, 6465–6488. DOI [10.18653/v1/2023.emnlp-main.398](https://doi.org/10.18653/v1/2023.emnlp-main.398)。 | 已读 [ACL 官方摘要和书目](https://aclanthology.org/2023.emnlp-main.398/)。ALCE 同时衡量流畅性、正确性和引用质量，研究检索支撑证据并生成带引文回答。 | 不能把“有链接”等同于充分的引文支持；不能将本文的来源可追溯性宣称为新的 citation-correctness 指标或已经完成 ALCE 式验证。 |
| `programmerAssistant2023` | Ross, Martinez, Houde, Muller & Weisz. 2023. *The Programmer's Assistant: Conversational Interaction with a Large Language Model for Software Development*. IUI, 491–514. DOI [10.1145/3581641.3584037](https://doi.org/10.1145/3581641.3584037)。 | [Crossref 书目](https://api.crossref.org/works/10.1145/3581641.3584037)；已读 [IBM Research 作者机构摘要](https://research.ibm.com/publications/the-programmers-assistant-conversational-interaction-with-a-large-language-model-for-software-development)。42 人研究围绕代码上下文中的多轮对话，呈现超出单次代码生成的交互能力。 | 不把参与者对潜在效率的看法改写为客观生产率提升；不声称它测试了外部技术资料抓取、知识供给或版本兼容正确性。 |

## 4. 重点相关工作比较：本文应在哪里定位

以下“本文差异”是论文定位建议，不表示已进行相关工作的穷尽性排除，也不表示本审计优于这些工作的指标。

| 研究线 / 代表文献 | 主要分析对象与已读摘要中的评价范围 | 与本文的重叠 | 本文应说明的差异与边界 |
| --- | --- | --- | --- |
| 开发者信息需求与在线寻径：Brandt、Ko、Sillito、Robillard | 人的编程任务、信息需求、在线资源、API 学习材料及工具支持。 | 开发任务需要组合不同信息；所需知识的可获得性与任务情境有关。 | 本文审计 Agent 能接触到的外部证据条件，不以源材料评分代替开发者体验研究。 |
| AI 编程交互：Vaithilingam、Barke、Ross | 人如何理解、使用、探索与修改模型输出；具体用户研究和原型。 | 生成代码与建议是开发者活动中的输入，需要理解和处理。 | 本文是任务日志的供给侧案例审计；不从分数推断人的信任、接管或效率。 |
| RAG：Lewis | 参数化和检索记忆结合的生成机制。 | 外部证据与模型知识共同参与生成。 | “官方/独立第三方/模型先验”的审计分类是本文的分析选择，不是 Lewis 提供的三个独立随机事件。 |
| RAGAs、ARES | 已经分解上下文质量、回答相关性、忠实性等，并构建自动评价方法。 | 多维度诊断、区分来源和产出。 | 将增量说清：本文聚焦版本敏感开发目标下，官方与社区知识的可发现、正文可读、适用版本及替代支撑条件；不是首次拆解 RAG 评价，也没有与这两个框架做实测优劣比较。 |
| ALCE：Gao | 检索证据、生成带引用回答、衡量正确性与引用质量。 | 可追溯证据与答案支撑的关系。 | 本文保留来源追溯并审计证据取得条件，没有做逐句 citation entailment/完整性验证，因此不能宣称与 ALCE 同等级的答案正确性证据。 |
| ReAct | 推理轨迹与动作交织，接触外部环境或知识源。 | 以外显检索—读取—回答过程组织审计记录。 | 图 1 是可观察流程的分析结构，不是对内部推理的观测，也不证明实现了原文 Agent。 |
| SWE-agent | 为 Agent 设计文件编辑、仓库导航与执行接口，测量软件工程任务表现。 | Agent 是具有特定能力与需求的工具/信息接口使用者。 | 本文将视角放到网页文档与社区证据环境；贡献是审计操作与案例，不是新的接口干预效应。 |
| WebArena、SWE-bench | 网页任务功能正确性、真实仓库 issue 解决能力。 | 面向具体任务而非只评估脱离语境文本。 | 本文没有实际任务执行成功率；启发式指标只说明既定观测与假设下的知识条件。 |

## 5. 可直接用于相关工作的英文定位句

> Existing RAG evaluations already distinguish properties of retrieved context from answer relevance, faithfulness, and citation support (RAGAs, ARES, and ALCE). Our audit complements this work by operationalizing the knowledge-supply conditions encountered in version-sensitive development tasks: whether official and community materials can be discovered and read, whether their applicability can be determined, and what alternative support remains when a source is insufficient. We do not validate a new answer-correctness metric or claim that our heuristic index is a calibrated probability.

> Prior studies describe how programmers seek information and interact with code-generating assistants, while SWE-agent demonstrates the relevance of interface design for agents as software users. We examine a different empirical object: traceable observations of the technical knowledge environment available to one retrieval-enabled agent. Implications for developer-facing interaction remain design considerations rather than measured human outcomes.

建议引用顺序按正文实际使用安排；不能仅为凑 16 篇使用 `nocite{*}`。若正文未用某篇，BibTeX 可以保留，但最终参考文献应由真实引用生成。

## 6. 访问限制与交付校验

- Crossref 对部分并发查询返回 429；后续使用逐项 DOI 查询，成功获取实际采用的记录。429 不是文献不存在的证据。
- OpenReview 页面返回浏览器校验页/API 返回 403，改用 ICLR 官方论文集和 arXiv camera-ready 元数据核验，不将受阻页面当成正文。APA 与部分 IEEE/作者站页面亦受阻；各项阅读范围已在表中注明。
- Lewis 2020、ReAct、WebArena、SWE-bench 未填写未经确认的会议版 DOI。ReAct 使用已核验的 arXiv v3 稳定 URL，并在 venue/year 保留其页面声明的 ICLR 2023 camera-ready 信息。
- 16 个固定 keys：`brand2009`、`ko2007`、`sillito2008`、`robillard2009`、`vaithilingam2022`、`barke2023`、`lewis2020`、`yao2023`、`zhou2024webarena`、`yang2024sweagent`、`jimenez2024swebench`、`pirolli1999`、`ragas2024`、`ares2024`、`gao2023alce`、`programmerAssistant2023`。
- 本轮没有引用不存在的已完成用户研究，也没有把别人的实验人数、执行成功率或验证结果写成本文结果。

## v0.3 additions (2026-09-10)

- Wang and Strong (1996), Beyond Accuracy: Crossref DOI metadata verified for authors, title, journal, volume, issue and pages. Used for the established consumer/context framing of information quality; no new empirical findings attributed to it. https://doi.org/10.1080/07421222.1996.11518099
- W3C PROV-Overview, Working Group Note, 30 April 2013: dated official document checked for provenance entities, activities and agents. https://www.w3.org/TR/2013/NOTE-prov-overview-20130430/
