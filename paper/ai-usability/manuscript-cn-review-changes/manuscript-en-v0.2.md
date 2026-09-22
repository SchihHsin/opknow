# Can AI Find What Developers Need? Defining and Measuring Knowledge Availability for AI in Developer Ecosystems

> **Revision status (21 September 2026):** Scoring rules, figures, and methodological references are updated. Current experimental material comprises 18 pilot runs on three tasks. The full experiment section awaits the author’s completion notice; results and conclusions will be discussed then.

## Abstract

Developers increasingly use AI agents across software development activities, from retrieving technical resources and generating or modifying code to executing tasks through tools. Assisting developers with these tasks requires access to usable technical knowledge. We conceptualize these conditions as knowledge availability for AI and introduce a task-level protocol with eleven indicators covering knowledge sources, acquisition effort, and response properties. The historical application covers 26 categories of software development tasks for AI-accelerated computing. This revision adds an exploratory 18-run pilot with GLM-5.3, DeepSeek V4.1 Flash, and Kimi across three tasks and two ecosystems to inspect revised-rule execution and evidence retention. The retained historical analysis distinguishes unclear version information, failures to obtain core instructions, readable but insufficient guidance, and supported main procedures with unavailable references. These findings connect developers’ information needs when assessing technical suggestions with knowledge gaps, informing improvements in technical knowledge provision and agents’ acquisition and use of knowledge. We contribute a conceptual framework, an inspectable protocol, and a case application for diagnosing the knowledge conditions underlying agents’ assistance with development tasks.

## Keywords

knowledge availability for AI; developer ecosystems; technical documentation; information foraging; AI agents; measurement methods

## Introduction

In traditional software development workflows, developers often need to consult documentation, code examples, search results, and community explanations themselves to decide what to do next. Research on opportunistic programming and developers' information needs shows that finding and interpreting information is part of programming itself [@brand2009; @ko2007; @sillito2008]. A useful result must fit the current task: a command needs the right options, an API example needs the right version, and an explanation of an error needs enough context to guide investigation. The existence of documentation is therefore only one condition for its usefulness.

Development agents with retrieval and tool-use capabilities introduce another collaborative route through this knowledge environment. A recent study of GitHub projects found adoption of coding agents across projects with different maturity levels and technical characteristics [@robbes2026]. A developer may ask about an error or a code fragment, or state a desired change or outcome and delegate information seeking, documentation reading, implementation planning, and portions of code modification to an agent. To advance such a task, the agent may search, read, and combine material across official sites, documentation, repositories, and communities before drafting a response, an implementation approach, or a code change. Studies of code-generation tools, conversational programming assistance, and agent support describe opportunities for this support alongside difficulties in understanding and checking generated suggestions [@vaithilingam2022; @barke2023; @programmerAssistant2023]. Delegating the search changes how supporting material reaches the developer, while leaving a need to judge whether a suggestion has an identifiable basis, fits the local environment, and requires further information. The agent's access to technical material is one condition for making that basis available for inspection. Measuring this access can therefore identify gaps in the knowledge on which AI-mediated guidance depends.

Agents can usually produce answers to development questions, but the accuracy and applicability of those answers depend in part on the knowledge they acquire. For example, when implementing a custom operator, an agent may find an official guide without obtaining its procedural content. When investigating an error, it may retrieve a complete page that offers only generic advice to inspect logs. In either case, the agent may continue to answer using prior knowledge or inference while lacking external evidence for specific steps. Even detailed instructions may yield inapplicable suggestions if the toolkit and framework versions they reference are incompatible. Assessment therefore needs to examine not only the answers agents produce but also gaps in their supporting knowledge, identifying concrete opportunities to improve technical resources and the feedback agents provide.

Those building developer ecosystems need to understand not only whether an agent can provide usable technical guidance, but also which knowledge conditions constrain that guidance and where improvements are needed. Similar shortcomings in answers may arise from different conditions: official resources were not discovered, procedural content was not obtained, acquired content lacked task-specific detail, or the basis for selecting a version remained unclear. A usable answer may also rely on alternative sources, masking gaps in official resources. Final answers or task outcomes alone offer limited grounds for distinguishing these conditions. Taking developers’ task-specific knowledge needs as a reference, we compare how ecosystems support different development activities and examine sources, acquisition events, and acquired content to identify problems in resource provision, information organization, and complementary sources, informing ecosystem development and agent interaction.

We define **knowledge availability for AI** as the extent to which task-relevant technical knowledge can be discovered, obtained, and assessed for applicability by a specified agent and tool configuration under stated retrieval conditions. The construct is relational: it concerns a task, a knowledge environment, and a means of accessing that environment at a particular time. We operationalize it through an evidence-recording protocol and eleven indicators. The indicators distinguish source conditions, acquisition effort, response checks, and a composite confidence score calculated from M1-M8. The method is intended for professionals such as product managers, designers, technical writers, and software engineers who develop and maintain developer platforms, technical knowledge resources, or AI agents. It aims to help them identify gaps in the discovery, acquisition, and task support provided by technical resources, and locate opportunities to improve knowledge provision and agent feedback. The case application demonstrates diagnostic distinctions for these uses; their value in teams' work requires evaluation.

We ask two research questions. **RQ1:** How can knowledge availability for AI be defined and operationalized so that task-specific access conditions and evidence gaps can be systematically recorded and reviewed? **RQ2:** What patterns of knowledge availability does the method reveal across development tasks, and how can those patterns inform documentation and agent design?

We address these questions through a methodological framework and its application to software development tasks for AI-accelerated computing. The historical case covers 26 task categories, yielding 52 task-side records. This revision separately reports an 18-run exploratory pilot across three models, three tasks (A, I, E), and two ecosystems; it is not a full-task rerun. Twenty-five categories compare CANN and CUDA development contexts; one migration category uses ROCm/HIP as the comparison destination and is treated separately. The case application connects task-level measurement to cross-task patterns and design implications. We contribute (1) a construct that distinguishes knowledge conditions from retrieval success and answer correctness; (2) a task-level protocol, indicator definitions, and portable analysis materials; and (3) worked cases and a cross-task synthesis that distinguish different breakdowns and connect them to documentation and agent design.

## Related Work and Construct Boundaries

### Developer information seeking and documentation

Information foraging theory relates information-seeking behavior to the structure and expected value of available information [@pirolli1999]. Programming studies show how developers interleave searching, learning, and implementation, and how their questions depend on the work they are performing [@brand2009; @ko2007; @sillito2008]. API-learning difficulties further motivate attention to the explanatory resources surrounding a technical interface [@robillard2009]. Uddin and Robillard identify ambiguity, incompleteness, and incorrectness as severe API-documentation problems [@uddin2015]. Aghajani et al. develop a taxonomy of documentation issues from mailing lists, Stack Overflow discussions, issue repositories, and pull requests [@aghajani2019]. Treude and Robillard demonstrate the potential to supplement formal API documentation with useful information extracted from Stack Overflow that the documentation does not contain [@treude2016]. Maalej and Robillard further classify knowledge types in API reference documentation [@maalej2013]. These studies show that developers’ information needs are closely tied to their current tasks. We therefore organize the assessment around specific development tasks, examining whether agents can find and obtain the required resources and whether those resources provide the explanations, parameter descriptions, and procedures needed for the task.

Our method does not infer human usability from machine access. Research with developers who are visually impaired likewise finds benefits from AI coding assistance alongside accessibility challenges involving excessive suggestions and context switching, underscoring the need to examine experience in specific usage contexts [@flores2025]. A page readable by a browser can be inaccessible to a particular extraction tool; conversely, text readily extracted by an agent can still be difficult for a person to navigate. We examine the conditions of the delegated knowledge route. Claims about developers' time, trust, satisfaction, or task completion require separate evidence.

### AI support for programming

Studies of AI programming assistance distinguish obtaining a suggestion from understanding, adapting, and checking it. Vaithilingam et al. describe difficulties in understanding, editing, and debugging generated code [@vaithilingam2022]; Barke et al. distinguish acceleration and exploration in programmers' use of code-generating models [@barke2023]. Ross et al. examine conversational assistance around code context [@programmerAssistant2023]. In a survey of 410 developers, Liang et al. identify unmet functional or non-functional requirements and difficulty controlling generated output as important barriers to use [@liang2024]. Mozannar et al. use a taxonomy of programmer activities to analyze interaction behavior and time costs around code suggestions, motivating assessment of the usage process beyond suggestion generation [@mozannar2024]. In security-related programming tasks, Perry et al. find that participants using an AI assistant produced less secure code while being more likely to believe that their code was secure, indicating a need to distinguish subjective confidence from actual quality [@perry2023]. These findings motivate attention to the supporting information available when a suggestion is considered. Our protocol examines whether relevant source passages, version conditions, and procedural details can be obtained and connected to that suggestion. It supplies an account of those knowledge conditions alongside studies of how developers engage with AI assistance.

Agents can interleave reasoning and tool use, and retrieval-augmented generation provides a way to incorporate external information into generation [@lewis2020; @yao2023]. WebArena, SWE-bench, and SWE-agent evaluate or develop agents in realistic web and software-engineering settings [@zhou2024webarena; @jimenez2024swebench; @yang2024sweagent]. Their task outcomes are valuable evidence of system performance. Our framework offers a complementary description of the knowledge conditions under which such systems operate. A failure can involve unavailable evidence, inadequate interpretation of available evidence, or unsuccessful execution; the present method directly addresses the first of these and records information relevant to separating them.

### Retrieval, attribution, and the availability construct

Existing research evaluates AI systems at several levels. ALCE examines the fluency, correctness, and citation quality of generated answers; RAGAs and ARES additionally assess the relevance of retrieved context and the faithfulness of answers to that context [@gao2023alce; @ragas2024; @ares2024]. AgentBoard analyzes agents’ action processes through measures such as fine-grained task progress, demonstrating the value of process information beyond final success rates [@ma2024agentboard]. In programming, RepoBench separately evaluates cross-file code retrieval, code completion, and their combined pipeline, distinguishing context acquisition from generation performance [@liu2024repobench]. Its focus is completion within code repositories; our method examines whether the official and third-party technical resources needed for development tasks can be discovered, obtained, and provide adequate support. These approaches provide a foundation for understanding system performance. Developing and maintaining a developer ecosystem also requires connecting performance to specific knowledge conditions: whether technical resources are readily discoverable, whether the required content is actually obtained, whether it supplies procedural detail, and whether versions have clear selection and compatibility guidance. We organize task-level measurement around these relationships to distinguish conditions calling for better acquisition paths, fuller content, or clearer version relations.

The distinctions in Table 1 position the construct. Availability can be necessary for an evidence-grounded answer without being sufficient for correctness. An agent can misinterpret an available source. It can also produce a correct answer from prior knowledge without obtaining any external evidence. These outcomes should remain distinguishable.

| Object of assessment | Central question | Relationship to this method |
| --- | --- | --- |
| Retrieval success | Was a relevant result returned? | One acquisition condition; not proof that required content was obtained. |
| Documentation usability | Can intended readers navigate and understand the material? | A related human-facing property requiring its own evaluation. |
| Knowledge availability for AI | What task-relevant knowledge was obtainable under the recorded conditions? | The construct operationalized here. |
| Answer correctness and attribution | Is the response correct, and do its sources support its claims? | A downstream evaluation that may use the acquired evidence. |
| Execution success | Do the proposed actions work in the target environment? | Requires execution or other independent outcome evidence. |

: Construct boundaries and neighboring objects of assessment.

## Methodological Framework

### Unit of analysis and task requirements

The unit is a **task-side acquisition episode**: a development objective pursued in a particular technical ecosystem using a stated agent and retrieval configuration. A task specification records the desired outcome, starting artifacts, constraints, version dependencies, and evidence required to support a next action. For example, model conversion may require a conversion command, an input-shape specification, a target-device setting, and a way to check the generated artifact. These requirements guide inspection; a long page is not automatically adequate.

Task selection and sampling should be explicit and follow the purpose of the evaluation [@kelly2009]. An ecosystem assessment may seek coverage across workflows; a documentation-team audit may focus on recurring support questions. Neither establishes the population frequency of those tasks without additional sampling evidence. For cross-ecosystem use, analysts record differences in starting conditions and task scope rather than assuming that similar names make tasks equivalent. The framework can also be applied within one ecosystem, across versions, or across retrieval configurations, provided the comparison conditions are made explicit.

Figure 1 locates the measurements in an observable tool-use loop. It is an analytic model, not a reconstruction of hidden model reasoning: the agent searches for candidate sources, selects URLs, fetches content or records a failure, then integrates evidence and assesses task adequacy and version applicability. When evidence is insufficient but remains searchable, the loop returns to query refinement. Model prior is registered as a separate branch; the current protocol also freezes a pre-retrieval answer without tools for M7 inspection. A prior answer need not produce an observable source and it is therefore not automatically treated as traceable evidence.

![An agent starts from a task and context, interprets intent, decomposes subgoals, and routes to retrieval or model prior; a retrieval branch searches, selects URLs, fetches content or fetches a known URL directly, then integrates evidence and assesses adequacy. Insufficient evidence can trigger retry; exhausted retrieval distinguishes whether reliable evidence remains.](figures/figure-1-framework-en.svg){#fig:framework description="A conceptual process diagram starts with a development task and context, showing intent interpretation, subgoal decomposition, routing, and a Need retrieval? decision. The retrieval branch shows web search for official and third-party candidates, URL selection, web fetch for content, and a direct-fetch route for a known URL; the other branch is model prior. Sources feed back to a current-evidence record, then pass through Is evidence adequate?, Can retrieval continue?, and Any reliable evidence left? decisions to converge, retry, or a risk-marked final answer. All M1 through M11 labels use the same style and name their measurement location."}

### Knowledge sources and task support

The framework examines three knowledge sources: official material, third-party material, and model prior knowledge. Official and third-party material are distinguished by publisher identity. For example, documentation, repositories, and blogs published by a vendor belong to the official channel, while tutorials and practical accounts from independent authors belong to the third-party channel. The hosting platform alone does not determine source ownership.

For official and third-party material, the framework examines whether the agent can find relevant sources, obtain their content, and use that content to support the current task. Specific checks concern whether the material includes the required procedures, parameter explanations, or diagnostic information, and whether applicable versions and component compatibility are clear. For model prior knowledge, the current protocol freezes an answer before retrieval without tools, then checks correctness and task coverage separately from the external material acquired.

Considering the three sources together makes it possible to examine which sources supply the knowledge required for a task, which requirements remain unsupported, and whether sources complement one another. For example, when official content is not obtained, does third-party material provide usable instructions? When several sources contain relevant information, are their versions and compatibility statements consistent? Acquisition counts and failed attempts describe the effort required to obtain this knowledge.

### An evidence record

The evidence record connects each judgment to its basis. Its minimum fields are the task question and starting conditions; agent and tool configuration when known; collection time; queries and selected URLs; publisher and source role; returned content or a relevant excerpt; access outcome; applicable versions; task requirements supported by that content; acquisition counts; and the coding decision with a rationale. A field also identifies whether an entry is directly recorded, subsequently coded, estimated, or unavailable.

This distinction prevents a common reporting error: transforming an interpretation into an observation merely because a script assigns it a number. A logged extraction failure is an observation of the tool-source interaction. Labeling an explanation as sufficient is a judgment against task requirements. Estimating a model's familiarity with a toolkit is an inference unless a separate test supports it. Numerical coding does not erase these differences.

## Operationalization and Measurement Protocol

### Eleven indicators and their evidential roles

The method retains three knowledge sources—official material, third-party material, and model prior knowledge—and the purposes of assessing discovery, acquisition, content support, version conditions, effort, and response properties. The current operationalization follows `three-model-pilot-20260921`, defined by the pilot's `frozen-skill/references/rules.md`, rather than the older installed Skill. Table 2 separates the objects of assessment.

| ID | Indicator | Evidence and interpretation |
| --- | --- | --- |
| M1 | Official source discoverability | Query sequence and list position of the first relevant official result within a common search budget; rewriting a query incurs no separate penalty. |
| M2 | Official content retrievability | Representation and body completeness actually obtained for each independent official document, distinguishing errors, page scaffolding, summaries, and direct body returns. |
| M3 | Official content detail | Detail of acquired official content against the original question's explanations, steps, parameters, and constraints; blocked when no body can be assessed. |
| M4 | Version clarity | Whether acquired official material establishes the applicability relationships needed to select versions; version and page counts do not determine scores. |
| M5 | Third-party source richness | Relevant independent third-party sources discovered within budget; first position and query count are also recorded. Body acquisition is not required for counting. |
| M6 | Third-party credibility / consistency | Traceable support, contradiction, and uncertainty for consequential claims, including corroboration by independent sources. |
| M7 | Model prior knowledge | Correctness and task coverage of a frozen, same-question answer produced before retrieval without tools; neither self-confidence nor inferred training density. |
| M8 | Retrieval effort | Actual search queries S plus dispatched fetch calls F: C=S+F. Failed calls count once, without an additional penalty; lower effort receives a higher score. |
| M9 | Version lockability | Evidence-supported ranges or specific versions for required components in the final answer, assessed separately from clarity in official material. |
| M10 | Operational executability | Additions or corrections still needed in the final answer's commands, code, parameters, and prerequisites; actual execution status is recorded separately. |
| M11 | Composite confidence score | A continuous 0–100 index derived from M1–M8 using a fixed formula. M9/M10 are reported independently; the index is not a probability of correctness. |

: Objects and evidential boundaries of the indicators. M1–M10 use ordinal five-level rubrics; M2 additionally retains the equal-weight document mean. Unknown, inapplicable, and blocked states are not low scores.

M2 asks what was actually acquired; M3 asks how thoroughly the acquired body explains the task; M4 asks whether official applicability relationships permit version selection; M9 asks whether the final answer fixes versions with evidence; and M10 asks what operational content still needs additions or corrections. Code in a return does not prove body completeness. A supported version range is less specific than a fixed version, and content inspection does not establish successful execution.

### Applying the protocol

**First, fix tasks and conditions.** Identify each episode by task, ecosystem, requested model, repetition, and run_id. Preserve both questions, starting conditions, requirements, version-selection scope, and components requiring version specifications. Record model and tool identities, search depth, search/fetch budgets, timing, and stopping conditions. Pairing establishes a shared development intent, not strictly equal difficulty. Unexposed tool parameters remain unknown.

**Second, freeze the prior answer and record acquisition.** Before encountering this run's search results, the model answers the same question without tools for subsequent M7 assessment. The client then preserves actual requests and returns, including every query and all ordered results, unopened and repeated entries, URLs, titles, snippets, positions, and available dates. Specify the target document or section before fetching; do not narrow it retrospectively to the returned fragment. Record resource format, returned representation, body content, and errors separately. Missing body content alone does not establish SPA, robots, or dynamic rendering as the cause.

**Third, connect requirements, sources, and the final answer.** Preserve initial obstacles, subsequent alternatives, recovery status, and requirements still unmet. Obtaining other content neither erases an earlier failure nor establishes task resolution. M3/M4 concern acquired official material; M9/M10 concern the actual final answer. A source passage cannot substitute for an answer quotation.

**Fourth, preserve assessment layers.** Each run retains `process.jsonl` and `evaluation.json`; original automated assessments, reviewed derivatives, and post-run references remain separately stored and linked. Scores require event identifiers, locatable quotations, and rationales. Literal matching establishes text location, not technical correctness. A later same-URL reference may inform a completeness audit of the original return, but its timing and purpose must be identified; it cannot be added to the model's runtime context.

**Fifth, report scores and non-scorable states.** Assign a point only when its grade is supported; retain bounds and reasons when a grade is unresolved. Distinguish pending assessment, insufficient evidence, missing measurement, inapplicability, and blocked access. Do not average M2 after discarding unknown documents. The current M11 calculator requires usable point values for all M1–M8 inputs; otherwise leave the composite pending, without zero imputation or rankings based on a small computable subset. Record execution passed, failed, content inspection only, or unverified separately from M10.

### Scoring rules and composite confidence

The figures summarize the frozen rules; Appendix A supplies all grades and decision boundaries. These ordinal levels are study operationalizations, without validated equal spacing between adjacent grades.

**Official material (M1–M4).** M1 uses the first successful query and position among its first five results. The pilot's maximum of four queries is an experimental condition, not a universal definition. M2 assesses each independent document's final acquisition state: 1, no identifiable target content; 2, title/navigation/metadata only; 3, an explicitly identified summary or excerpt; 4, a direct body return with evidence of truncation or missing content; 5, a direct body return with verifiable full-document or complete-target-section boundaries. A direct return of unknown completeness remains bounded at 4–5. Code within a summary does not increase its grade. Static and server-rendered pages follow the same content criteria. Retries do not increase the document count; independent documents receive equal weight, preserving full precision. Unknown documents remain in the denominator of a bounded mean.

M3 checks the original task requirements, progressing from an overview through isolated details and complete passages to the main procedure and all required constraints; it does not add exhaustive requirements beyond the question. M4 progresses through no version information; versions without selection criteria or with unresolved contradictions; partial applicability relationships missing a necessary correspondence; selection requiring combination of supported official constraints; and explicit official relationships permitting direct lookup or rule application. A supported choice may be a single version or a range. Retrieval effort belongs to M8 and final-answer version specificity to M9.

![Official-material rubrics (M1–M4): discovery, returned representation and completeness, content detail, and version applicability are assessed separately.](figures/figure-scoring-official-en.svg){#fig:scoring-official description="Four rows of grades 1–5. M2 progresses from no target content through scaffolding and summary/excerpt to incomplete direct body and direct body with verifiable complete boundaries. M4 progresses from absent versions through missing criteria, partial relationships, combining official constraints, and direct lookup or rule application. Unknown completeness remains bounded."}

**Third-party material (M5–M6).** M5 counts deduplicated relevant independent third-party sources discovered within budget: 0, 1–2, 3–4, 5, and at least 6 yield grades 1–5. Official repositories and forums are excluded under the frozen channel classification. Reposts and mirrors are not independent; unresolved relevance produces count bounds. M6 examines traceable support and contradiction for consequential claims, from unresolved key contradictions to support for all key claims with independent corroboration. Author identity, first-hand material, and inspectable experimental evidence inform credibility. Platform names, publication age alone, and repost counts do not directly determine a score. M6 is inapplicable when there is no third-party material.

**Model prior knowledge (M7).** Inspect the pre-retrieval answer's correctness and coverage of the original task, assigning the highest satisfied grade. Self-confidence is retained as a record, not a score, and performance without retrieval does not reveal training-data density. Historical runs without a pre-retrieval answer are missing measurements; unresolved correctness remains pending.

**Retrieval effort (M8).** Let $C=S+F$, where $S$ is the actual search-query count and $F$ the number of dispatched fetch calls, including failures. Costs of 1–2, 3–4, 5–6, 7–8, and at least 9 receive grades 5, 4, 3, 2, and 1. Requests blocked before dispatch are not actual fetches. Failures incur no additional penalty; zero calls or abnormal interruption do not automatically earn a high score. Elapsed time and available token usage are retained separately. Call counts are not complete computational cost and do not assume equal search and fetch durations.

![M5–M8: independent-source counts, credibility of key claims, pre-retrieval knowledge performance, and actual search/fetch effort.](figures/figure-scoring-support-en.svg){#fig:scoring-support description="M5 uses counts 0, 1–2, 3–4, 5, and at least 6. M6 grades claim support and independent corroboration. M7 checks the pre-retrieval answer rather than self-rating. M8 uses C=S+F with no extra penalty for a failed call."}

**Response properties (M9–M10).** M9 distinguishes missing required versions; mentioned versions without supported applicability or with contradictions; supported versions for some components; supported ranges for every component; and supported specific versions for every component. A correct range is not an incorrect answer, but is less specific than a fixed version; arbitrary version selection must not increase the score. M10 distinguishes a goal description, an operational skeleton, a concrete plan requiring additions or corrections, instructions requiring only explained environment-value substitutions, and instructions requiring no additions or corrections. Grade 4 cannot include fixing content errors. Whether hardware execution occurred does not separate grades 4 and 5. Both indicators require final-answer quotations; M10 is inapplicable for purely conceptual tasks and M9 when version specification is unnecessary.

![Version lockability (M9) and operational executability (M10).](figures/figure-scoring-answers-en.svg){#fig:scoring-answers description="M9 distinguishes missing, unsupported, partial-component, all-component ranges, and specific versions. M10 distinguishes goals, skeletons, required corrections/additions, explained environment-value substitutions, and no required additions/corrections. Execution status is separate; inspection does not establish execution success."}

**Composite confidence (M11).** Let $x_i=M_i/5$. Multiplication within each channel retains the constraints imposed by its components. A noisy-OR form combines channels to express the possibility that one source compensates for another:

$$
OFF=x_1x_2x_3,\qquad SEC=x_5x_6,\qquad OWN=x_7,
$$

$$
K=1-(1-OFF)(1-SEC)(1-OWN),
$$

$$
M11=100K(0.7+0.3x_4)(0.9+0.1x_8).
$$

The version coefficient remains 0.30 and the effort coefficient 0.10. Preserve computational precision and display one decimal place. M11 is continuous on a 0–100 reporting scale, without five-level bins; neither $(M_i-1)/4$ normalization nor a three-channel mean is used. M9/M10 remain separate. The index is uncalibrated: the noisy-OR form does not establish channel independence or justify interpreting the value as a probability of correctness.

Unknown, inapplicable, or blocked inputs are not imputed as zero; blocked M3 does not automatically set OFF to zero. The frozen calculator does not implement a special encoding for a confirmed unavailable channel. If any M1–M8 input lacks a usable point value, this pilot leaves M11 pending. Component bounds, including those of M2, remain visible without being presented as a calculated M11 point.

![M11 continuous score strip: light-to-dark shading represents the continuous 0–100 index; the calculation is given in the text.](figures/figure-scoring-confidence-en.svg){#fig:scoring-confidence description="x_i=M_i/5. OFF=x1*x2*x3, SEC=x5*x6, OWN=x7. Combine to K, then multiply by 100, 0.7+0.3*x4, and 0.9+0.1*x8. No five-level bins; unresolved required inputs leave M11 pending; M9/M10 are independent."}

The coefficients remain prespecified working settings, without an optimality claim. A separate `m11-uniform-fit-20260921` batch completed 48 runs, including 24/32 development and 12/16 held-out records. Its primary analysis selected the original coefficients; a post-hoc sensitivity analysis correcting answer-event identifiers selected another candidate and did not establish a stable improvement over baseline. Accordingly, fitted replacements are not adopted. That batch and the present 18-run, three-model pilot are reported separately, without pooling samples or treating a formula's comparison with itself as validity evidence. Model selection should be separated from held-out assessment, and composite weighting assumptions and sensitivity should be disclosed [@hastie2009; @oecd2008].

Ranked-retrieval evaluation supports fixed depth and explicit position and relevance judgments [@manning2008]. Body extraction research distinguishes substantive text from templates and navigation [@kohlschutter2010]. Information-quality and API-documentation research distinguish accessibility, context-dependent content quality, and required detail [@wang1996; @uddin2015; @maalej2013]. These principles help delimit M1, M2, and M3/M4, respectively; they do not supply this study's five-level thresholds.

Research on supplementing formal documentation with third-party material motivates examining source complementarity [@treude2016]. Claim-level factual checking provides a methodological reference for verifiable statements in M6 and M7, while evaluating retrieved context separately from answers helps preserve the boundaries of M9/M10 [@min2023factscore; @ragas2024]. The five levels of no-retrieval task knowledge in M7 and required operational corrections in M10 are this study's operationalizations. Factual support does not establish completeness or successful code execution. Interactive-retrieval evaluation supports recording process and effort, but does not prescribe S+F, its cutoffs, or equal call duration [@kelly2009].

The composite-indicator handbook supports disclosure of aggregation and weighting assumptions and sensitivity analysis, not this noisy-OR formula, its 0.30/0.10 coefficients, or a probability interpretation [@oecd2008]. Measurement-development and validity literature supports defining the assessment domain, checking content coverage, and accumulating evidence for particular interpretations and uses; this multi-object framework is not treated as a single psychological latent-variable scale [@boateng2018; @standards2014]. The literature ledger records actual reading scope—metadata, abstracts, selected chapters, or relevant full-text passages—without claiming every work was read in full. Methodological principles, passing log checks, and similar observations across models do not validate particular thresholds, coefficients, or the entire rubric.

## Case Study of the CANN and CUDA Developer Ecosystems

### Task coverage and comparison scope

Evidence for executing the current rules comes from the 21 September 2026 pilot: GLM-5.3, DeepSeek V4.1 Flash, and Kimi each completed the CANN and CUDA questions for model conversion (A), version compatibility (I), and error diagnosis (E), giving 3 models × 3 tasks × 2 ecosystems = 18 runs, once per cell. Task types were selected before collection and reused historical questions to inspect rule execution and evidence retention. This is neither a rerun of all 26 historical tasks nor independent held-out validation or population sampling.

| Task and shared intent | CUDA question (translation) | CANN question (translation) |
| --- | --- | --- |
| A: model conversion and deployment | How can a trained PyTorch model be exported to a TensorRT engine for deployment? Provide complete PyTorch→ONNX→TensorRT steps and commands. | How can an ONNX model be converted to an offline .om model on Ascend? Provide complete ONNX→ATC→.om steps and commands. |
| I: version compatibility | My PyTorch and CUDA/cuDNN versions do not match. How can I check compatibility among PyTorch, CUDA toolkit, cuDNN, and the driver? | Installing torch_npu produces a version mismatch. How can I check compatibility among CANN, torch_npu, firmware/driver, and PyTorch? |
| E: error diagnosis | My PyTorch/CUDA program reports `RuntimeError: CUDA error: device-side assert triggered`. How can I locate the failing line or kernel? | Training/inference on Ascend reports an error code such as `EZ9999`. How can I identify and investigate its root cause? |

: The pilot's three paired questions. The frozen tasks.json retains the original Chinese wording and six requirements per task side. Shared intent does not establish equal difficulty; task A still differs in starting artifact and conversion scope.

The historical audit was conducted on 10–11 June 2026 and covered 26 task categories and 52 task-side records, using the then-recorded Claude model and earlier scoring rules. Twenty-five pairs formed the CANN/CUDA comparison; G used ROCm/HIP on the comparison side and was treated separately. Historical identities and values are retained, neither relabeled as three-model results nor pooled directly with scores under the new rules. The existing historical results and conclusions below remain subject to discussion in light of the new evidence.

### Task execution and data analysis

WorkBuddy CLI requested `glm-5.3`, `deepseek-v4.1-flash`, and `kimi-k3-2`, and returned matching aliases. Their display names are GLM-5.3, DeepSeek V4.1 Flash, and Kimi. The recorded client alias `kimi-k3-2` does not guarantee an immutable backend model snapshot. All models used WebSearch and WebFetch with the same frozen tasks, rubric, and budgets: at most four searches and eight fetches, enforced before dispatch, with 22 maximum turns, a 600-second timeout, and generator effort set to low. The client managed the search provider, which was not independently locked. Language/region, result-count configuration, and temperature were not exposed; all actual ordered results were preserved. These are model–tool configurations, so differences cannot all be attributed to the model alone.

Each run used a fresh temporary directory and session with memory-disable environment flags; these measures do not guarantee operating-system isolation. Batch records preserve execution order and three-way concurrency. Models produced a pre-retrieval answer, tool calls, a final answer, and a stop reason. Original process logs and evaluations remain separate. The batch dispatched 54 searches and 102 fetches, retaining 270 ordered search results. Requests blocked by the budget were distinguished from actual calls. All 18 records passed the retained correspondence, budget, and input-hash checks, which establish structural properties rather than technical correctness.

GLM-5.3 assessed every run, using separate contexts for sources/prior answers and final answers. There are 36 valid assessments and three retained failed attempts; tasks were not rerun to obtain preferred scores. One pre-retrieval answer lacked its closing tag and was recovered from actual events preceding the first tool call; only M7 was taken from its additional assessment. `assessments/` retains original automatic judgments, `reviewed/` retains quotation/rule-review derivatives, and `evaluation.json` records revisions. The automated assessor is not an independent expert panel.

The M2 audit inventories identified official fetch targets and combines same-URL retries, producing 95 within-run independent-document observations, including repeated visits across runs. Fourteen full-body matches use same-URL HTTP references obtained after the runs. Those references audit the original return's completeness; they were not new evidence available to the model during execution. Other observations retain error, scaffolding, summary, or unresolved-completeness states. Unknown documents remain in bounded aggregation.

The collection protocol did not fix the scope of version selection for E before execution, and assessments disagreed between scoring M4 and treating it as inapplicable. All six E/M4 comparisons are therefore withheld, preserving original judgments and reasons without forcing a common score. This is an omission in applicability specification, not evidence of model inability. M9 and other indicators also retain unresolved applicability or evidence entries rather than forced scores.

Analysis first inspects component evidence, bounds, and missingness within each model's paired ecosystem tasks, then examines recurring obstacle types and recovery paths across models. A model that did not visit a source has no observation of that source, not evidence of no problem. Three tasks and one run per model–task–ecosystem cell do not establish population rankings or measurement validity. Only 1/18 records currently has usable point values for every M1–M8 input, so no three-model M11 ranking is produced. M9/M10 remain separate. No hardware execution was performed; M10 concerns operational content inspection only.

> **Historical results retained for discussion:** The following results, Figures 6–15, and associated discussion retain the earlier audit and rubric. Values have not been recomputed under the 21 September 2026 rules and do not represent the 18-run pilot. Interpretations and conclusions await discussion of the new evidence; the revised Figures 2–5 must not be used to reconstruct historical matrix scores.

### Task-level assessment results

The main comparison includes 25 CANN tasks: core content was obtained in 22 tasks, partial content in two, and no core content in one. Core content was obtained in all 25 corresponding CUDA tasks. Figures 6–8 present all eleven indicator scores and group tasks by environment and installation, operator development, training, inference and deployment, performance and optimization, debugging, and migration. G is shown as a separately marked CANN/ROCm-HIP migration analogy and is excluded from CANN/CUDA summaries.

![Full indicator matrix (1/3): M1–M4 scores for official discoverability, official content accessibility, official content detail, and source version clarity, organized by workflow with CANN and CUDA columns for each task. G uses ROCm/HIP in the second column.](figures/figure-2-full-matrix-a-en.svg){#fig:fullmatrixa description="A workflow-grouped task matrix. Each row is a development task and each metric has CANN and CUDA columns. This facet shows M1 official source discoverability, M2 official content accessibility, M3 official content detail, and M4 source version clarity. G is a separately marked CANN and ROCm/HIP migration analogy and is excluded from CANN/CUDA summaries."}

![Full indicator matrix (2/3): M5–M8 scores for third-party source count, third-party source credibility, estimated model prior knowledge, and search and acquisition effort, in the same workflow and task order.](figures/figure-2-full-matrix-b-en.svg){#fig:fullmatrixb description="The second facet of a workflow-grouped task matrix. Rows correspond to the first facet and each metric has CANN and CUDA columns. This facet shows M5 third-party source count, M6 third-party source credibility, M7 estimated model prior knowledge, and M8 search and acquisition effort. G is a separately marked CANN and ROCm/HIP migration analogy."}

![Full indicator matrix (3/3): M9–M11 values for response version specificity, procedural actionability of responses, and the composite confidence score from M1–M8, in the same workflow and task order.](figures/figure-2-full-matrix-c-en.svg){#fig:fullmatrixc description="The third facet of a workflow-grouped task matrix. Rows correspond to the first two facets and each metric has CANN and CUDA columns. This facet shows M9 response version specificity, M10 procedural actionability of responses, and the composite confidence score from M1–M8. G is a separately marked CANN and ROCm/HIP migration analogy."}

Figures 6–8 present the ordinal scores for M1–M10 and composite confidence calculated from M1–M8. Figure 9 adds content-acquisition states to support interpretation of the corresponding scores.

![Access-profile detail placing content-acquisition states beside official-content-detail and source-version-clarity scores. It follows the workflow groups and task order of Figures 6–8 to support interpretation of acquisition outcomes.](figures/figure-3-access-profile-en.svg){#fig:accessprofile description="A workflow-grouped auxiliary matrix. Each row compares CANN and CUDA in content acquisition, official content detail, and source version clarity. C, P, and N indicate core content obtained, partial content obtained, and not obtained. The figure complements the indicator scores in Figures 6–8; specific entry paths are described in the corresponding task records. G is a separately marked CANN and ROCm/HIP migration analogy."}

Across the 25 task pairs, mean composite confidence is $\bar{x}=0.731$ for CANN and $\bar{x}=0.922$ for CUDA. Indicator-level summaries show differences of varying sizes in content detail, source version clarity, search and acquisition effort, and procedural actionability of responses. Table 4 reports the means and standard deviations of these four indicators. The findings below interpret the corresponding knowledge conditions using score distributions and specific resources.

| Indicator | CANN $\bar{x}$ ($SD$) | CUDA $\bar{x}$ ($SD$) |
| --- | ---: | ---: |
| M3 Official content detail | 4.21 (0.83) | 4.80 (0.41) |
| M4 Source version clarity | 2.88 (1.01) | 4.24 (0.83) |
| M8 Search and acquisition effort | 3.24 (1.36) | 3.88 (1.51) |
| M10 Procedural actionability of responses | 4.00 (0.76) | 4.72 (0.68) |

: Descriptive statistics for four indicators, scored from 1 to 5. $SD$ denotes the sample standard deviation. For M3, CANN has $n=24$, excluding the blocked-content record D, and CUDA has $n=25$. Both sides have $n=25$ for the other indicators. Higher M8 scores indicate lower search and acquisition effort. Means and standard deviations describe the ordinal score distributions.

## Findings: Knowledge Conditions Across Development Tasks

Task-level comparisons reveal three connected findings. First, the ecosystems show different distributions of knowledge support across development scenarios. Second, differences in specific tasks involve official-source discovery, content delivery, detail, and version organization. Finally, third-party material and estimates of model prior knowledge also vary by task and require examination alongside official resources. We present scenario comparisons, specific knowledge gaps, and complementarity among sources in that order.

### Knowledge-support distributions differ between ecosystems across development scenarios

Across workflows, CANN's mean composite confidence is $\bar{x}=0.799$ for environment and installation, $\bar{x}=0.658$ for operator development, and $\bar{x}=0.646$ for debugging; the corresponding CUDA means are $\bar{x}=0.904$, $\bar{x}=0.891$, and $\bar{x}=0.933$ (Table 5). Debugging has the largest between-ecosystem difference, at 0.287. The comparison directs attention to specific development activities: in this task set, CANN provides stronger knowledge support for environment configuration than for operator development and debugging.

| Workflow | Tasks | CANN $\bar{x}$ | CUDA $\bar{x}$ | Difference |
| --- | ---: | ---: | ---: | ---: |
| Environment and installation | 3 | 0.799 | 0.904 | 0.106 |
| Operator development | 6 | 0.658 | 0.891 | 0.233 |
| Training | 4 | 0.791 | 0.945 | 0.154 |
| Inference and deployment | 4 | 0.722 | 0.920 | 0.198 |
| Performance and optimization | 4 | 0.752 | 0.957 | 0.205 |
| Debugging | 2 | 0.646 | 0.933 | 0.287 |
| Migration | 2 | 0.787 | 0.921 | 0.133 |

: Workflow means of the composite confidence score for 25 task pairs. Differences are calculated as CUDA minus CANN using unrounded means, then rounded to three decimal places; G is excluded.

| Development scenario | Task pairs | CANN $\bar{x}$ ($SD$) | CUDA $\bar{x}$ ($SD$) |
| --- | ---: | ---: | ---: |
| Getting started and environment setup | 9 | 0.762 (0.078) | 0.915 (0.038) |
| Training and routine use | 5 | 0.743 (0.121) | 0.953 (0.045) |
| Operators and in-depth development | 11 | 0.699 (0.113) | 0.914 (0.062) |

: Mean composite confidence and sample standard deviation for 25 task pairs grouped by development scenario. Getting started and environment setup comprises A, H, I, J, K, S, T, Y, Z; training and routine use comprises E, F, P, Q, R; operators and in-depth development comprises B, C, D, L, M, N, O, U, V, W, X. Both ecosystems use identical assignments, excluding G.

Scenario grouping further shows CANN's mean composite confidence decreasing from $\bar{x}=0.762$ for getting started and environment setup to $\bar{x}=0.743$ for training and routine use and $\bar{x}=0.699$ for operators and in-depth development. CUDA's corresponding means are $\bar{x}=0.915$, $\bar{x}=0.953$, and $\bar{x}=0.914$, without the same descending pattern. This comparison identifies weaker knowledge support for in-depth development in CANN, allowing the assessment to produce specific insights into how an ecosystem supports different development activities.

Cases within the groups clarify the knowledge these scenarios require. CANN's tiling task M and custom-operator task D score 0.628 and 0.410, respectively. Memory-access and utilization task U, also in the in-depth development group, scores 0.881 and obtained official best-practice material. Error-code task E in the training and routine-use group scores 0.554; its acquired official explanation lacked diagnostic detail. We next examine acquisition and content records to identify the knowledge-provision issues involved in these scenario differences.

### Official-source discovery, acquisition, content, and version organization reveal distinct gaps

Official-source discoverability also differs. Across the 25 task pairs, mean M1 is $\bar{x}=3.56$ for CANN and $\bar{x}=4.40$ for CUDA, with 12 and five tasks, respectively, using two search rounds. In task A, the first official CANN result appeared at rank 4, compared with rank 1 for the corresponding CUDA task. These differences concern the position of official material in task-related search results and the number of rounds used in the retrieval process.

After official material is found, the next question is whether the required body content is actually obtained. In the main comparison, 22 of the 25 CANN tasks obtained core content, two obtained partial content, and one did not obtain core content; all 25 CUDA tasks obtained core content. Most tasks acquired official material, while acquisition obstacles were concentrated in a few paths. Those paths require examination against task requirements to identify the missing procedural material.

Task D requires creating an Ascend C operator and integrating it with a framework, with implementation code, configuration-field explanations, and compilation and deployment steps. In task D, when the agent read the official Ascend C development page through web_fetch, it obtained only page scaffolding, including navigation, a brief description, and documentation links, without the implementation steps, configuration explanations, or compilation and deployment instructions. web_fetch explicitly reported “No code blocks, no implementation details, no step-by-step commands.” The corresponding CUDA task obtained detailed official content, with M3 = 5. M1 records official-source discovery conditions, M2 records the acquisition outcome, and M3 for the CANN side of D is marked as blocked. This difference highlights the need for official webpages to deliver procedural content in a form that agents can actually read, so that the available technical material can provide a basis for their answers.

Once content is obtained, its task support still differs. Among CANN's 24 assessable records, ten each have M3 = 4 and M3 = 5, and four have M3 = 2 or 3; all 25 CUDA records have M3 = 4 or 5. In CANN task E, the content the agent obtained through web_fetch from the official EZ9999 explanation listed the cause as “N/A” and suggested “Check whether the CANN package is correct” and “Check whether the environment variable is correct.” It did not provide specific environment-variable names, checking commands, or criteria for interpreting the results. The content acquired by the agent contained only generic checking suggestions and lacked diagnostic information specific to this error, making it difficult to determine the next action, with M3 = 2. The corresponding CUDA task obtained a checking-tool guide with specific commands, tool options, and report formats, with M3 = 5. This difference concerns whether the acquired material supplies the steps and explanations needed for diagnosis.

Task X, also a debugging task, obtained detailed official guidance in both ecosystems, with M3 = 5 on each side. Comparing E and X locates the issue in specific task content: CANN's memory-checking task already has substantial official guidance, while its error-code diagnosis task lacks information needed to select the next check. The improvement target is the content of error explanations and diagnostic guidance.

Task A shows how useful main-path material and unavailable references can coexist. When the agent read the official conversion quickstart through web_fetch, it obtained an ATC conversion command and parameter explanations, including `--input_shape` for the input shape, `--soc_version` for the target processor, and guidance on querying processor information with `npu-smi info`. This content supplied a basis for the conversion command and its parameter settings. A more extensive ATC/AIPP reference returned navigation and metadata. The worked recording example links the quickstart to supported conversion requirements and the missing reference to unresolved advanced settings. In task Y, accessing chip-migration information through the document center likewise yielded only partial content. These cases motivate recording both the content obtained and its relation to a task requirement, with the access route recorded separately where available. For a developer assessing the conversion guidance, this distinction identifies a supported main procedure and advanced settings that still require reference material. It bounds which parts of a proposed action the acquired sources can substantiate.

The supplement’s “Selected web_fetch evidence” provides the URLs, timestamps, requests, and relevant return excerpts for A’s quickstart, D’s development entry, and E’s error entry. These excerpts show the web_fetch content actually received by the agent in each read, providing concrete evidence for the case analysis above.

Acquisition effort can differ even when core content is obtained. Both sides of K obtained official core content, but CANN recorded four fetches and one fetch failure, whereas CUDA recorded two fetches without failure, yielding M8 = 1 and M8 = 4, respectively. These records include additional attempts along resource-entry and acquisition paths in the analysis of knowledge-provision conditions.

Version organization affects a broader range of tasks. Mean M4 is $\bar{x}=2.88$ for CANN and $\bar{x}=4.24$ for CUDA. Twelve CANN tasks score 2, spanning conversion, installation, training, operator development, inference, optimization, and debugging. In A, similar quickstarts appear in different version trees, leaving a version choice after content acquisition; its M4 is 2, compared with 4 for the corresponding CUDA task. These differences direct attention to the organization of recommended versions, applicability scopes, and compatibility evidence.

Both sides of I obtained compatibility information, with M4 = 4 and response-version explicitness M9 = 5. The CANN task combined sources about the toolkit, driver, framework, and integration package; the acquired compatibility matrix supplied a basis for connecting these relations. Version assessment can thus identify insufficient selection guidance and record how existing compatibility information supports a task. For ecosystem development, the relevant object is the set of queryable and verifiable relations among resources.

After retrieval is delegated to an agent, the applicability declared by a source still needs comparison with the developer's device and software combination. Source applicability and local environment facts supply different information for this comparison: missing compatibility relations require source investigation, while unspecified installed versions require a local environment check.

### Complementary support and limitations across knowledge sources

Across the 25 task pairs, the mean number of third-party candidate sources per task is $\bar{x}=3.16$ for CANN and $\bar{x}=3.44$ for CUDA; five and six tasks, respectively, have only one or two candidates. Complementary support requires task-specific examination. In X, both ecosystems obtained detailed official guidance, with one and three third-party candidates, respectively; I has three and two. Differences in counts do not run in the same direction for every task.

Source records further show that platform distribution and acquisition conditions affect candidate entries. For K, both CANN candidates come from CSDN, while CUDA's four candidates span different platforms. CANN records for N, O, and Q include blocked acquisition of Zhihu content. Platform distribution helps identify source relationships to inspect, while returned content determines whether entries can supply usable explanations. Whether different articles on the same platform are independent still requires content examination.

Source combinations make complementarity between official and community knowledge concrete. CANN task X has few third-party candidates but detailed official guidance; D lacks core official content and also has a low third-party credibility score. E records continued searching for cases after the official error explanation proved insufficient. These cases point, respectively, to experience supplementing official guidance, jointly limited core guidance and alternative support, and a need for diagnostic information from other sources. Ecosystem knowledge development therefore needs to examine which task requirements official resources support and which still depend on discoverable, obtainable practical cases and independent explanations.

Model prior-knowledge estimates provide another support indicator. In the main comparison, mean M7 is $\bar{x}=2.84$ for CANN and $\bar{x}=4.56$ for CUDA. CANN tasks D, E, I, M, N, S, and X score 2, while all CUDA tasks score 4 or 5. Reading this estimate alongside source records identifies tasks whose external knowledge support warrants closer inspection. We did not separately test performance without retrieval; the estimate describes the configuration of knowledge support and does not validate independent task completion by the model.

M9 and M10 further record the guidance formed during tasks. For example, X has M10 = 5 in both ecosystems, whereas E has M10 = 3 and M10 = 5, respectively. These response properties and the acquired materials provide joint grounds for inspection, extending analysis from knowledge sources to the version statements and procedural conditions in the resulting guidance.

## Discussion: Design Implications for Knowledge Provision and Agent Interaction

The comparisons develop an account of ecosystem knowledge support through development scenarios, specific knowledge gaps, and complementary sources. We use these results to discuss development priorities, improvements to official resources and agent feedback, and community knowledge and source inspection. The design illustrations make potential applications concrete; their effects have not been evaluated.

### Setting development priorities through scenarios and knowledge requirements

The scenario comparison identifies limited knowledge support for in-depth development in CANN as an area requiring attention. Examining D, M, and related tasks locates specific needs for implementation guides, procedural detail, and supplementary cases; E also identifies diagnostic knowledge as task content requiring development. This demonstrates the diagnostic value of task-level research: comparing development activities and their knowledge requirements produces specific insights into ecosystem development priorities.

These insights imply different scopes of improvement. Version issues recurring across workflows motivate shared recommended entries and organized compatibility relations; the core content not obtained in D and the limited diagnostic detail in E call for improved content delivery and more complete task guidance, respectively. Tasks with limited third-party support also require examination of practical-case and independent-explanation coverage. Improvements can be checked by returning to the original tasks and examining whether their knowledge requirements receive stronger support.

### Improving official knowledge provision and agent feedback

Recurring version issues suggest treating applicability as a property of a documentation system. A stable recommended-version entry can coexist with clearly indexed documentation for earlier versions, while each page states its applicable versions and verification date. Compatibility relations among drivers, toolkits, frameworks, and integration packages can be published in a queryable form. For a task such as I, this would let a developer or agent request the supported combinations for a stated environment, reducing the need to assemble the relation from several disconnected records.

Figure 10 makes this proposal concrete through a compatibility lookup interface. Device and framework constraints define the query, and each returned combination retains its sources, applicability scope, and verification date. Where no supported match is documented, the interface identifies unresolved conditions. The version problem registered by M4 becomes an inspectable relation, providing a basis for subsequently checking the applicability of a response.

![Proposed version and compatibility lookup, motivated by fragmented version information in A and I. Query constraints, result fields, and source inspection illustrate the proposed information structure; compatibility values are placeholders.](figures/figure-6-compatibility-design-en.svg){#fig:compatibilitydesign description="A proposed compatibility lookup interface has target-device and framework-version selectors, followed by result fields for toolkit, driver range, framework, integration package, and supporting sources. Placeholder fields illustrate the structure without asserting compatibility values. Each relation retains provenance, applicability scope, and a verification date; unmatched queries identify unresolved conditions. The motivation is fragmented version information in tasks A and I."}

Version-dependent guidance should connect a source's applicability to the available task environment. Before proposing a toolkit/framework combination, an agent can use device and software facts already supplied in the task, requesting only information that remains necessary to establish the match. The response indicators then ask whether the recommendation states its applicable version conditions and provides actionable steps with explicit substitutions or modifications.

Figure 11 illustrates version checking through a separate environment record. It distinguishes developer-supplied local facts from the applicability declared by a source, then records the comparison as matched, mismatched, or insufficient information. The record is reused within the task and updated with additional user input to support applicability checks before specific commands are recommended.

![Proposed environment declaration and version checking, motivated by A and I. Device, toolkit, and framework fields represent developer-supplied local facts, separate from source applicability. The illustrated state has insufficient information to establish a match.](figures/figure-10-environment-design-en.svg){#fig:environmentdesign description="An environment record contains placeholder fields for device model, toolkit, framework, and integration versions. A separate area presents the cited material's version and compatibility conditions and identifies the missing information needed to establish a match. Checks can be matched, mismatched, or insufficient information, and the developer can update the task's environment record."}

Localized acquisition and content gaps call for task-specific repairs. For the content-acquisition gap illustrated by D, documentation systems should ensure that agents reading official development pages can obtain the complete procedural content. Options include ensuring that HTML pages directly return the full content or providing Markdown or plain-text versions updated alongside the webpages. Whichever approach is used, it should preserve the steps, parameter explanations, and applicable versions needed for the task, with corresponding tasks used to check whether the agent can actually obtain this content. E already has a dedicated error page; its improvement requires more informative content within that entry: error semantics, possible triggers, diagnostic steps, links to issue cases, and applicable versions. For a catch-all error, a guide can state what the code alone leaves unresolved and specify which logs or local observations are needed next. Such a page supports diagnosis by organizing available evidence around the user's problem.

Figure 12 illustrates task-oriented content through E's error page. It starts with what the code can establish, identifies local information to collect, links observable symptoms to checks and attributed cases, and retains a support route for unresolved situations. Domain maintainers would need to establish the actual causes, checks, and cases; the structure helps locate the knowledge that needs to be supplied.

![Proposed task-oriented diagnostic content, motivated by E's dedicated error page with generic guidance. The structure connects a diagnostic starting point, local information, checks, case evidence, and unresolved branches. Specific cases and version scopes remain fields to populate.](figures/figure-7-diagnostic-content-design-en.svg){#fig:diagnosticdesign description="A proposed EZ9999 diagnostic page first states that the code alone does not identify a cause, then organizes logs, triggering operations, and environment information. A table connects observable conditions to checks and attributed cases, followed by unresolved branches and support. The content structure is illustrative and asserts no verified causes or cases."}

The same task-oriented structure can guide other documentation units. An intended outcome, prerequisites, minimal commands or code, parameter explanations, expected output, and recovery information provide concrete material for both human reading and agent retrieval. Machine-readable exports and indexes should preserve those relationships and their version scope. Their success can be checked against the relevant content-acquisition and detail fields for the task that motivated the change.

Figure 13 illustrates delivery of the same task material through a document body and a machine-readable export. Using the command and parameter relations in the conversion quickstart acquired in task A, the export preserves the task, applicable version, source, parameter explanations, and related steps. For a route such as D's, the aim is to deliver the missing core guidance; where a readable body already exists, the aim is to preserve its context during export. Acceptance checks should compare acquired content with task requirements, rather than only checking for a particular file format.

![Proposed document body and machine-readable export. Command, parameter, and device-query relations come from the conversion quickstart acquired in task A; the structured text is a proposed export. Both views preserve the task's version, source, and step relationships.](figures/figure-8-readable-export-design-en.svg){#fig:readableexportdesign description="The left side structures a model-conversion quickstart with version, official source, an ATC command excerpt, and input_shape and soc_version instructions. The right side is a proposed structured export retaining task, version, source, command, parameters, related steps, and original entry. The arrow indicates preservation of content relationships, not a new acquisition or a demonstrated site repair."}

An agent interface can preserve the difference between finding a relevant source, obtaining its body, and supporting a proposed step. For D, an informative status would identify the missing implementation guide. For E, it would indicate that the official explanation is generic and request the logs or trigger context needed for further diagnosis. For A, it could retain the usable conversion path while marking advanced reference settings as unresolved. These statuses connect a retrieval event to its consequence for the developer's current task.

Figure 14 contrasts proposed responses to D and E. For D, the agent first seeks a linked body page or another readable source, while retaining the original entry for optional inspection. For E, it explains how trigger context and relevant log excerpts would guide a search for diagnostic cases. Developer-supplied content is a fallback for acquisition failures; accessible core guidance remains a responsibility of the knowledge provider. M1-M3 locate the gap, while M8 records the effort of subsequent attempts.

![Proposed agent feedback for two knowledge gaps: (a) a missing core body, based on D; (b) readable but diagnostically insufficient content, based on E. Task observations supply the problem conditions; interface messages and next actions are design proposals.](figures/figure-9-acquisition-design-en.svg){#fig:acquisitiondesign description="Two side-by-side subfigures show proposed feedback for distinct knowledge gaps. The left, based on D, shows a found guide returning only navigation and metadata, then proposes looking for body links or readable sources and retains optional access to the original entry. The right, based on E, shows the official EZ9999 body obtained but containing only generic advice, then requests trigger context and logs. Both are design illustrations, not original dialogue screenshots."}

Knowledge provision also involves entry points and maintenance. Stable, searchable official entries affect whether candidate materials are discovered; explicit ownership, revision dates, and compatibility relations support subsequent assessment. Teams can use representative tasks as recurring inspection units, tracking whether queries reach the intended material, its body is delivered, version relations have changed, and community cases remain applicable. Such maintenance also addresses source governance and third-party knowledge provision beyond the illustrated interfaces.

To address differences in search visibility, documentation teams can inspect search-engine indexing and the alignment of page titles and summaries with development-task terminology, assessing search engine optimization (SEO) improvements through official-result positions and the rounds needed to discover material for task queries.

### Expanding community knowledge and supporting source inspection

Community knowledge development can address task situations that lack adequate support, including specific failures, operating experience under different configurations, and alternative implementations. This direction connects to research on augmenting API documentation with Stack Overflow insights [@treude2016]; the present study additionally examines whether agents can discover and acquire such material and whether it supports specific task requirements. Tasks with few candidate sources require checking which supplementary explanations are missing; concentrated or inaccessible sources require checking independent practical evidence and content-delivery conditions. The aim is for task-relevant experience to be discoverable, obtainable, and attributable, beyond simply increasing the number of entries.

Consistent with human–AI interaction guidelines on explaining behavior and supporting correction [@amershi2019], agents can retain source passages, applicability conditions, and their relationships to suggestions to help developers inspect available support. Where content remains missing, they should identify unsupported parts of the task and direct further searches or requests for necessary local information accordingly. The source-inspection and corrective-feedback illustration makes these information relationships concrete.

Because explanations can increase acceptance without improving team performance [@bansal2021], source presentation should be evaluated by developers’ ability to identify unsupported or inapplicable suggestions.

Figure 15 further illustrates source inspection and corrective feedback. A developer can expand the cited passage for a command, inspect its applicable version, and attach an encountered error or correction to the suggestion. The original source, task environment, and new feedback remain connected so the next check can address the specific discrepancy. This provides inspectable support for the response properties described by M9 and M10 and for subsequent revision.

![Proposed source inspection and corrective feedback. The conversion-command excerpt comes from the quickstart acquired in task A; source expansion, an original-page entry, and error feedback linked to the suggestion are proposed interactions.](figures/figure-11-verification-design-en.svg){#fig:verificationdesign description="Within a model-conversion task, the response command expands into a cited passage from the official CANN 8.0.RC2 quickstart and an original-page entry. A developer can attach an error or correction to that command, retaining the source and task context for the next check. The command excerpt comes from that quickstart material; the interface interaction is proposed."}

These proposals treat checking suggestions as part of programming work, consistent with the information-seeking and AI-assistance studies discussed earlier [@brand2009; @vaithilingam2022; @barke2023]. Exposing every retrieval event or source passage could add reading effort without clarifying the next action. An interface could first show the supported step, relevant version scope, and unresolved condition, with source passages available on demand. This prioritizes the information needed for the current judgment while retaining a route to detailed inspection.

Requests for environment facts can likewise interrupt a task, especially when they repeat information already provided. A request should explain which recommendation depends on the missing fact and reuse task context where available, with confirmation when it may be stale. For diagnostic logs, it should request relevant excerpts and allow sensitive details to be removed. Missing compatibility relations and generic error explanations require work by documentation and system teams; collecting more local facts cannot supply those missing explanations. The balance between inspection, interruption, and useful guidance remains a question for evaluating these proposals.

### Reusing the diagnostic method

The method connects a task requirement to a source or acquisition event, an indicator code, and a diagnosis of the information needed to assess a proposed action. Professionals such as product managers, designers, technical writers, and software engineers who develop and maintain developer platforms, technical knowledge resources, or AI agents could use the profile to locate missing guidance or applicability relations and distinguish further source retrieval from a request for a local fact. Analysts can reuse the record structure with domain-specific requirements, such as client-server compatibility in a database SDK or deployment prerequisites in a web framework. These are intended applications of the method.

Subsequent evaluation can examine whether independent analysts produce comparable profiles, whether the diagnoses correspond to expert assessments of missing information, and whether documentation teams find them useful for planning repairs. These questions follow directly from the intended use of the method. The present application supplies the task-level distinctions, worked records, and cross-task synthesis on which such evaluation can build.

## Limitations and Research Transparency

This three-model pilot examines rule execution and evidence retention on three tasks, once per cell. Tasks are neither a random population sample nor new held-out cases, and paired questions are not guaranteed equally difficult. The historical audit, coefficient-fitting batch, and current pilot differ in purpose and conditions and cannot be pooled as full-task multi-model validation. Model aliases do not fix backend snapshots, the search provider was not independently locked, and tool effects are intertwined with model performance.

Every automatic assessment used GLM-5.3, allowing same-model assessor bias. Original judgments, reviewed derivatives, and unresolved quotation and applicability issues remain separate. Literal quotation checks and file/budget checks do not establish technical correctness or independent expert validation. Some M2 completeness evidence is post hoc, and the omitted E/M4 scope prevents that comparison. Most records cannot yield an M11 point; dropping missing inputs or using only computable records cannot establish ecosystem or model superiority. Scoring consistency, validity for intended uses, and coefficient applicability require further evaluation.

No hardware execution was performed, so command or code reproduction success cannot be reported. How developers use these distinctions to assess local applicability, and how proposed feedback affects reading burden, interruptions, and task completion, requires user research. The literature supplies conceptual and methodological support, not validation of this study's specific five-level thresholds or coefficients.

## Conclusion

We define knowledge availability for AI through eleven indicators connecting knowledge sources, acquisition processes, and response properties. Task-level comparisons of CANN and CUDA identify differences in knowledge support across development scenarios, including weaker support for in-depth development in CANN, and reveal specific conditions involving content delivery, diagnostic detail, version organization, and supplementary sources. Connecting scores with task requirements and acquired material produces concrete insights into how ecosystems support development activities and which knowledge resources require improvement.

The method makes the basis for AI-mediated technical guidance an object of inspection: which source supports a proposed step, which applicability relation remains unresolved, and what additional information is needed. The framework, protocol, and case analysis provide a way to locate these conditions and relate them to knowledge provision and agent feedback. Documentation repairs, source retrieval, and requests for local facts follow from different diagnoses, offering concrete directions for subsequent evaluation.


## Appendix A: Scoring calculations {.unnumbered}

The following M1–M10 grades and decision boundaries follow the pilot’s frozen rules.md. The grades are study conventions, not thresholds directly validated by cited literature. Raw records preserve pending, missing, inapplicable, blocked, and insufficient-evidence states.

**M1 Official source discoverability**

1. No relevant official source within the prespecified common search budget
2. First relevant official source on query 3 or later
3. First relevant official source on query 2
4. First query: relevant official source at position 2–5
5. First query: relevant official source at position 1

The pilot inspects five results per query, with at most four queries; these are experimental conditions. Count queries, not differently batched calls. Later searches after the first hit do not lower the score. Earlier timeouts, missing lists, or stopping before exhausting the budget without a hit leave the score pending. Preserve every ordered URL and exact position.

**M2 Official content retrievability**

1. No identifiable target-page content: failed request, denial, error page, or no return
2. Target title, navigation, or metadata, with no identifiable body
3. Explicit summary or excerpt representation, without a direct body return
4. Direct body return with tool-reported truncation, missing pages, or verifiable missing boundaries
5. Direct body with verifiable full-document or complete-target-section start/end boundaries and no truncation or missing-page evidence

Score the final acquisition state of each independent official document. Summary code is not direct body; a tool claiming complete extraction does not prove completeness. Direct body with unknown completeness remains bounded at 4–5, not forced to 4. Fix the target before reading. A composite return with complete body and summary follows the body evidence; a summary containing original fragments remains grade 3. Do not infer acquisition from answer quality. Give independent documents equal weight, keep the unrounded mean, combine retries, and retain unknown documents in aggregation.

**M3 Official content detail**

1. Acquired body offers only an overview, without relevant explanation or operational details
2. Relevant but isolated parameters, fragments, or descriptions do not form a complete explanatory or operational passage
3. Complete explanatory or operational passages exist, but key steps, parameters, or constraints needed for the original task are missing
4. Main procedure, parameters, and prerequisites are explained, but branches, constraints, or reference details explicitly involved in the task remain incomplete
5. All explanations, steps, parameters, and constraints required by the original task are complete without consulting additional material to fill those requirements

Derive required content from the original question without extra exhaustive demands. Locate each omission and use the highest satisfied grade. Missing body is blocked, not grade 1; navigation belongs to M2 and version selection to M4. Record content errors separately; length alone does not establish detail.

**M4 Version clarity**

1. No version information
2. Versions are present, but no selection criteria are given, or official statements conflict without resolution
3. Some applicability relationships are explicit, but a correspondence required to complete version selection is missing
4. Applicable versions can be determined only by combining official constraints
5. Official applicability relationships are explicit: direct lookup or rule application determines applicable versions

Assess acquired official material. Missing assessable body is blocked; tasks without version selection are not_applicable. Check only required version conditions; one version or a range may be appropriate. Page and version counts do not incur penalties. Combined constraints require official support without unstated assumptions. Locate conditions, missing relationships, and contradictions. Effort belongs to M8, final-answer specification to M9. Preserve bounds and reasons when a grade cannot be distinguished.

**M5 Third-party source richness**

1. 0 relevant independent third-party sources
2. 1–2 relevant independent third-party sources
3. 3–4 relevant independent third-party sources
4. 5 relevant independent third-party sources
5. At least 6 relevant independent third-party sources

Deduplicate relevant sources discovered within the common budget; body acquisition is not required. Exclude official repositories and official forums under the frozen channel classification. Reposts/mirrors of the same content count once. Unresolved relevance gives count bounds; bounds spanning grades remain pending. Separately report first position and query count.

**M6 Third-party credibility / consistency**

1. A key claim directly contradicts a reliable checking basis and remains unresolved
2. No confirmed key contradiction, but key claims lack a traceable checking basis
3. Traceable evidence supports some key claims; others remain unverified
4. All key claims have traceable support, with no unresolved contradiction, but lack corroboration by independent sources
5. All key claims have traceable support and independent-source corroboration, with no unresolved contradiction

Limit key claims to verifiable statements that change operations, explanations, or version choices. Record support, contradiction, and uncertainty claim by claim. Credibility uses author identity, first-hand material, or inspectable experimental evidence, not platform labels. Reposts do not independently corroborate; older material counts against a claim only when obsolete. No third-party material means N/A. This evidence-credibility rubric is uncalibrated.

**M7 Model prior knowledge**

1. The pre-retrieval answer contains no verifiable correct task knowledge, or its key claims are contradicted by checking evidence
2. The pre-retrieval answer gives correct concepts only, without a concrete method or explanation
3. The pre-retrieval answer gives correct method or explanation fragments, but key details require external material
4. The pre-retrieval answer gives a correct complete procedure or explanation, but task-specific parameters or constraints still need supplementation
5. The pre-retrieval answer accurately covers all procedures, explanations, parameters, and constraints required by the task

Freeze a same-question no-tool answer before retrieval, then separately inspect correctness and completeness. The model must not see this run’s retrieval beforehand. Self-confidence is recorded only. Historical records without that answer are missing measurements. This measures performance without retrieval, not training-data coverage density. Unresolved correctness remains pending.

**M8 Retrieval effort**

1. C ≥ 9
2. C = 7–8
3. C = 5–6
4. C = 3–4
5. C = 1–2

C=S+F counts actual search queries and fetch calls. A failed call counts once, without an added penalty. Enforce equal budgets in the client; retain time and available token counts. C=0 or abnormal interruption does not automatically earn a high score. Calls do not capture full computational cost.

**M9 Version lockability**

1. The final answer lacks version information required by the original task
2. Versions are mentioned without supported applicable versions/ranges, or a key version choice contradicts evidence
3. Some required components have explicit version support; others remain unresolved
4. Every required component has a supported applicable range, but at least one is not fixed to a specific version
5. Every required component has a supported specific version, without unresolved compatibility conflicts

Assess only the final answer after fixing which components actually require versions; do not require an irrelevant opset. A supported range is not an incorrect answer, but is less specific than an exact version. No version requirement means N/A. Do not specify arbitrary versions to increase the score. Clear official material does not imply that the answer has fixed versions.

**M10 Operational executability**

1. No executable plan: only a goal description or illustration
2. An operational skeleton only; a key operation cannot be determined from the answer
3. A concrete operational plan requires corrections or missing content before execution
4. Complete operational guidance requires only substitution of clearly marked, explained user-environment values
5. Operational guidance and applicability prerequisites are explicit; no additions or corrections are needed for direct execution

Inspect final-answer commands, code, parameters, and prerequisites for required additions or corrections. Grade 4 permits explained paths/device values, not correction of content errors. Grade 3 identifies the missing or incorrect content; grade 2 identifies the indeterminate key operation. Every grade needs an answer quotation. Actual execution passed/failed, content inspection only, or unverified is recorded separately and does not distinguish 4 from 5. Inspection cannot establish successful reproduction; insufficient evidence stays pending, and purely conceptual tasks are N/A.

**M11 Composite confidence score**

Use the continuous percentage-scale formula in the main text: $x_i=M_i/5$, $OFF=x_1x_2x_3$, $SEC=x_5x_6$, $OWN=x_7$; $M11=100[1-(1-OFF)(1-SEC)(1-OWN)](0.7+0.3x_4)(0.9+0.1x_8)$. Report M9/M10 separately. Preserve full precision, display one decimal, and do not bin into five levels. The current calculator requires usable point values for all M1–M8 inputs; unknown, inapplicable, or blocked states are not zero-imputed. Unfinished assessment leaves M11 pending. The 0.30/0.10 settings are a working baseline, without optimality or probability-calibration claims.
