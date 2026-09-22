# Can AI Find What Developers Need? Defining and Measuring Knowledge Availability for AI in Developer Ecosystems

> **Full-rerun revision:** This separate copy updates measurement details, experimental settings, and results from experiment commit 87e04c1. All 156 episodes completed collection and both assessment phases; unknown evidence states remain. Original review pages are preserved.

## Abstract

Developers increasingly use AI agents across software development activities, from retrieving technical resources and generating or modifying code to executing tasks through tools. Assisting developers with these tasks requires access to usable technical knowledge. We conceptualize these conditions as knowledge availability for AI and introduce a task-level protocol with eleven indicators covering knowledge sources, acquisition effort, and response properties. We apply the method to 26 categories of software development tasks for AI-accelerated computing, with 25 CANN/CUDA pairs in the main comparison and a separate migration analogy. Results distinguish compatibility relations not yet obtained, readable procedural content with essential gaps, and complementary support acquired through different sources or paths. Some average differences recur across models, while scenario ordering and source complementarity vary. These findings connect information needed to assess technical suggestions with knowledge gaps and suggest improvements to technical knowledge provision and agents' acquisition and use of that knowledge. The contribution is a conceptual framework, an inspectable protocol, and a case application for diagnosing the knowledge conditions on which agent-assisted development depends.

## Keywords

knowledge availability for AI; developer ecosystems; technical documentation; information foraging; AI agents; measurement methods

## Introduction

In traditional software development workflows, developers often need to consult documentation, code examples, search results, and community explanations themselves to decide what to do next. Research on opportunistic programming and developers' information needs shows that finding and interpreting information is part of programming itself [@brand2009; @ko2007; @sillito2008]. A useful result must fit the current task: a command needs the right options, an API example needs the right version, and an explanation of an error needs enough context to guide investigation. The existence of documentation is therefore only one condition for its usefulness.

Development agents with retrieval and tool-use capabilities introduce another collaborative route through this knowledge environment. A recent study of GitHub projects found adoption of coding agents across projects with different maturity levels and technical characteristics [@robbes2026]. A developer may ask about an error or a code fragment, or state a desired change or outcome and delegate information seeking, documentation reading, implementation planning, and portions of code modification to an agent. To advance such a task, the agent may search, read, and combine material across official sites, documentation, repositories, and communities before drafting a response, an implementation approach, or a code change. Studies of code-generation tools, conversational programming assistance, and agent support describe opportunities for this support alongside difficulties in understanding and checking generated suggestions [@vaithilingam2022; @barke2023; @programmerAssistant2023]. Delegating the search changes how supporting material reaches the developer, while leaving a need to judge whether a suggestion has an identifiable basis, fits the local environment, and requires further information. The agent's access to technical material is one condition for making that basis available for inspection. Measuring this access can therefore identify gaps in the knowledge on which AI-mediated guidance depends.

Agents can usually produce answers to development questions, but the accuracy and applicability of those answers depend in part on the knowledge they acquire. For example, when implementing a custom operator, an agent may find an official guide without obtaining its procedural content. When investigating an error, it may retrieve a complete page that offers only generic advice to inspect logs. In either case, the agent may continue to answer using prior knowledge or inference while lacking external evidence for specific steps. Even detailed instructions may yield inapplicable suggestions if the toolkit and framework versions they reference are incompatible. Assessment therefore needs to examine not only the answers agents produce but also gaps in their supporting knowledge, identifying concrete opportunities to improve technical resources and the feedback agents provide.

Those building developer ecosystems need to understand not only whether an agent can provide usable technical guidance, but also which knowledge conditions constrain that guidance and where improvements are needed. Similar shortcomings in answers may arise from different conditions: official resources were not discovered, procedural content was not obtained, acquired content lacked task-specific detail, or the basis for selecting a version remained unclear. A usable answer may also rely on alternative sources, masking gaps in official resources. Final answers or task outcomes alone offer limited grounds for distinguishing these conditions. Taking developers’ task-specific knowledge needs as a reference, we compare how ecosystems support different development activities and examine sources, acquisition events, and acquired content to identify problems in resource provision, information organization, and complementary sources, informing ecosystem development and agent interaction.

We define **knowledge availability for AI** as the extent to which task-relevant technical knowledge can be discovered, obtained, and assessed for applicability by a specified agent and tool configuration under stated retrieval conditions. The construct is relational: it concerns a task, a knowledge environment, and a means of accessing that environment at a particular time. We operationalize it through an evidence-recording protocol and eleven indicators. The indicators distinguish source conditions, acquisition effort, response checks, and a composite confidence score calculated from M1-M8. The method is intended for professionals such as product managers, designers, technical writers, and software engineers who develop and maintain developer platforms, technical knowledge resources, or AI agents. It aims to help them identify gaps in the discovery, acquisition, and task support provided by technical resources, and locate opportunities to improve knowledge provision and agent feedback. The case application demonstrates diagnostic distinctions for these uses; their value in teams' work requires evaluation.

We ask two research questions. **RQ1:** How can knowledge availability for AI be defined and operationalized so that task-specific access conditions and evidence gaps can be systematically recorded and reviewed? **RQ2:** What patterns of knowledge availability does the method reveal across development tasks, and how can those patterns inform documentation and agent design?

We address these questions through a methodological framework and its application to software development tasks for AI-accelerated computing. The case covers 26 task categories: 25 compare CANN and CUDA development contexts, and one migration category uses ROCm/HIP as the comparison destination and is treated separately. The case application connects task-level measurement to cross-task patterns and design implications. We contribute (1) a construct that distinguishes knowledge conditions from retrieval success and answer correctness; (2) a task-level protocol, indicator definitions, and portable analysis materials; and (3) worked cases and a cross-task synthesis that distinguish different breakdowns and connect them to documentation and agent design.

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

The method retains official, third-party, and model-prior sources and the purposes of assessing discovery, acquisition, content support, version conditions, effort, and response properties. The batch uses the frozen `three-model-pilot-20260921+execution-checks` rubric; this inherited rule-version name does not make the full batch a pilot. The batch protocol is `full-rerun-protocol-20260921`, with rules.md and execution-checks.md as the scoring authority rather than the installed Skill defaults. Table 2 distinguishes the indicators' assessment objects.

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

Unknown, inapplicable, and blocked inputs are not automatically zero; blocked M3 alone does not set OFF=0. A channel contributes zero only when evidence review confirms no usable support in that episode and retains its reason and evidence. M5=1, M6 being inapplicable, or one failed page is insufficient. A prespecified inapplicable M4 receives a neutral version factor of 1 while M4 remains N/A. Usable input bounds propagate through the formula's monotonicity: inserting all lower and all upper endpoints gives M11 evidence bounds, not confidence intervals. Missing inputs without usable bounds leave M11 uncomputable.

**Literature basis for the indicators.** The table below identifies the concepts or methods actually borrowed for each indicator and separates them from this study's own design choices. The cited works motivate the measurement object, evidence boundary, or recording practice; they do not supply this study's grade thresholds, M2 aggregation rule, or M11 formula.

| Indicator | References | What is borrowed | What is specified by this study |
| --- | --- | --- | --- |
| M1 Official discoverability | Manning, Raghavan, and Schütze (2008) [@manning2008]; Kelly (2009) [@kelly2009] | Ranked retrieval, fixed search depth, relevance judgments, and recording interactive retrieval processes. | The five-grade mapping from first-hit round and top-five position, and the four-query experimental cap. |
| M2 Official retrievability | Wang and Strong (1996) [@wang1996]; Kohlschütter, Fankhauser, and Nejdl (2010) [@kohlschutter2010] | Separating accessibility from content quality, and distinguishing document body from page templates and navigation. | The error/scaffolding/summary/body grades, completeness audit, equal weighting of independent documents, and thresholds. |
| M3 Official content detail | Wang and Strong (1996) [@wang1996]; Es et al. (2024) [@ragas2024]; Reddy and Andrade (2010) [@reddy2010] | Contextual content quality, separating source content from answer quality, and clear rubric descriptions. | Freezing task requirements for explanations, steps, parameters, and constraints, then mapping them to five grades. |
| M4 Version clarity | Wang and Strong (1996) [@wang1996]; Uddin and Robillard (2015) [@uddin2015]; Maalej et al. (2013) [@maalej2013] | Contextual applicability, API-documentation problems, and types of knowledge developers need. | The version–component applicability checklist and five-grade mapping; the cited works do not provide this technical scale. |
| M5 Third-party richness | Manning et al. (2008) [@manning2008]; Treude and Robillard (2016) [@treude2016] | Fixed retrieval depth, relevance judgments, set counting, and third-party material as a complement to formal documentation. | Deduplication and independence rules, plus the 0, 1–2, 3–4, 5, and ≥6 thresholds. |
| M6 Third-party credibility / consistency | Wang and Strong (1996) [@wang1996]; Es et al. (2024) [@ragas2024]; Min et al. (2023) [@min2023factscore] | Information quality, separating retrieved evidence from answers, atomic claim checking, and independent support. | The key-claim inventory, supported/contradicted/unknown states, and aggregation into five grades. |
| M7 Model prior knowledge | Kadavath et al. (2022) [@kadavath2022]; Min et al. (2023) [@min2023factscore] | Separating self-assessment from actual correctness and checking answer claims individually. | Freezing the pre-retrieval answer, grading task coverage, and handling unresolved correctness. |
| M8 Retrieval effort | Kelly (2009) [@kelly2009]; OECD, EU, and EC-JRC (2008) [@oecd2008] | Recording interactive retrieval processes and disclosing assumptions when converting quantitative observations. | C=S+F, counting failed calls, and the 1–2 through ≥9 grades; call count is not time or monetary cost. |
| M9 Version lockability | Wang and Strong (1996) [@wang1996]; Es et al. (2024) [@ragas2024]; Uddin and Robillard (2015) [@uddin2015] | Contextual applicability, source evidence versus final-answer properties, and version/applicability problems in API documentation. | Component coverage, ranges, and specific-version grades for the final answer; M4 is not counted again in M11. |
| M10 Operational executability | Es et al. (2024) [@ragas2024]; Min et al. (2023) [@min2023factscore]; Uddin and Robillard (2015) [@uddin2015] | Separating retrieval evidence, factual support, and answer quality, with attention to operational gaps in documentation. | The five grades from goal to no required correction, and no deduction merely because hardware execution was not performed. |
| M11 Composite confidence | OECD, EU, and EC-JRC (2008) [@oecd2008]; Boateng et al. (2018) [@boateng2018]; AERA, APA, and NCME (2014) [@standards2014] | Construct definition, normalization, weight disclosure, sensitivity analysis, and validity boundaries for composite measures. | The noisy-OR structure, 0.30/0.10 coefficients, continuous percentage scale, and missing-input rules; it is not interpreted as a probability. |

: Table 2a. Literature basis for each indicator and boundary of this study's design.

M2 asks what was actually acquired; M3 asks how thoroughly the acquired body explains the task; M4 asks whether official applicability relationships permit version selection; M9 asks whether the final answer fixes versions with evidence; and M10 asks what operational content still needs additions or corrections. Code in a return does not prove body completeness. A supported version range is less specific than a fixed version, and content inspection does not establish successful execution.

### Applying the protocol

**First, fix tasks and conditions.** Identify each episode by task, ecosystem, requested model, repetition, and run_id. Preserve both questions, starting conditions, requirements, version-selection scope, and components requiring version specifications. Record model and tool identities, search depth, search/fetch budgets, timing, and stopping conditions. Pairing establishes a shared development intent, not strictly equal difficulty. Unexposed tool parameters remain unknown.

**Second, freeze the prior answer and record acquisition.** Before encountering this run's search results, the model answers the same question without tools for subsequent M7 assessment. The client then preserves actual requests and returns, including every query and all ordered results, unopened and repeated entries, URLs, titles, snippets, positions, and available dates. Specify the target document or section before fetching; do not narrow it retrospectively to the returned fragment. Record resource format, returned representation, body content, and errors separately. Missing body content alone does not establish SPA, robots, or dynamic rendering as the cause.

**Third, connect requirements, sources, and the final answer.** Preserve initial obstacles, subsequent alternatives, recovery status, and requirements still unmet. Obtaining other content neither erases an earlier failure nor establishes task resolution. M3/M4 concern acquired official material; M9/M10 concern the actual final answer. A source passage cannot substitute for an answer quotation.

**Fourth, preserve assessment layers.** Each run retains `process.jsonl` and `evaluation.json`; original automated assessments, reviewed derivatives, and post-run references remain separately stored and linked. Scores require event identifiers, locatable quotations, and rationales. Literal matching establishes text location, not technical correctness. A later same-URL reference may inform a completeness audit of the original return, but its timing and purpose must be identified; it cannot be added to the model's runtime context.

**Fifth, report scores and unavailable states.** Use points when grades can be determined and evidence bounds when the available evidence restricts but does not determine a grade. Preserve not-assessed, insufficient-evidence, missing, inapplicable, and blocked states separately. Do not remove unknown M2 documents before averaging. Propagate usable input bounds through the monotone M11 formula, rounding outward without midpoint substitution or zero imputation; inputs without usable bounds leave M11 incomplete. Record execution success, failure, content-only checking, or unverified status separately from M10.

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

The version coefficient 0.30 and effort coefficient 0.10 are prespecified working settings, not claimed optima. This batch does not refit coefficients or tune them to M9/M10 or a desired ecosystem ordering. Earlier pilots and separate coefficient explorations are not pooled with the formal sample. The distinction between model selection and evaluation, and assumptions and sensitivity in composite weighting, should be disclosed [@hastie2009; @oecd2008]. We report components, comparable task coverage, and evidence bounds; retaining the formula does not establish intended-use validity or probability calibration.

Ranked-retrieval evaluation supports fixed depth and explicit position and relevance judgments [@manning2008]. Body extraction research distinguishes substantive text from templates and navigation [@kohlschutter2010]. Information-quality and API-documentation research distinguish accessibility, context-dependent content quality, and required detail [@wang1996; @uddin2015; @maalej2013]. These principles help delimit M1, M2, and M3/M4, respectively; they do not supply this study's five-level thresholds.

Research on supplementing formal documentation with third-party material motivates examining source complementarity [@treude2016]. Claim-level factual checking provides a methodological reference for verifiable statements in M6 and M7, while evaluating retrieved context separately from answers helps preserve the boundaries of M9/M10 [@min2023factscore; @ragas2024]. The five levels of no-retrieval task knowledge in M7 and required operational corrections in M10 are this study's operationalizations. Factual support does not establish completeness or successful code execution. Interactive-retrieval evaluation supports recording process and effort, but does not prescribe S+F, its cutoffs, or equal call duration [@kelly2009].

The composite-indicator handbook supports disclosure of aggregation and weighting assumptions and sensitivity analysis, not this noisy-OR formula, its 0.30/0.10 coefficients, or a probability interpretation [@oecd2008]. Measurement-development and validity literature supports defining the assessment domain, checking content coverage, and accumulating evidence for particular interpretations and uses; this multi-object framework is not treated as a single psychological latent-variable scale [@boateng2018; @standards2014]. The literature ledger records actual reading scope—metadata, abstracts, selected chapters, or relevant full-text passages—without claiming every work was read in full. Methodological principles, passing log checks, and similar observations across models do not validate particular thresholds, coefficients, or the entire rubric.

## Case Study of the CANN and CUDA Developer Ecosystems

### Task coverage and comparison scope

The case application was conducted on 21 September 2026 across 26 development-task categories. Each model completed both sides of each task, yielding 26×2×3=156 valid acquisition episodes. Twenty-five CANN/CUDA pairs constitute the main comparison (150 episodes). Task G compares migration from CUDA/PyTorch GPU programs to CANN and to ROCm/HIP; its six episodes are reported separately. The existing task set covers different development activities rather than a random population sample. Earlier pilots and historical assessments are not pooled with the present formal results.

| Workflow | Task IDs | Count | Shared development intent |
| --- | --- | ---: | --- |
| Environment and installation | I, J, K | 3 | Compatibility lookup, toolkit installation, and containers |
| Operator development | C, D, L, M, N, O | 6 | Library selection, implementation, numerical checks, dynamic shapes, fusion, and registration |
| Training | F, P, Q, R | 4 | Distributed training, mixed precision, memory, and convergence |
| Inference and deployment | A, H, S, T | 4 | Conversion, quantization, serving, and dynamic inputs |
| Performance and optimization | B, U, V, W | 4 | Profiling, memory access, transfer overlap, and communication |
| Debugging | E, X | 2 | Error diagnosis and out-of-bounds localization |
| Migration and concepts | Y, Z | 2 | Cross-chip migration and programming-model explanation |
| Separate migration analogy | G | 1 | Migration to CANN and ROCm/HIP; outside the main comparison |

: Table 3. Task coverage. Groups organize observations; they do not establish task frequency, a strict difficulty hierarchy, or independent knowledge requirements. Exact frozen Chinese questions and applicability scopes are retained in the [task and evidence supplement](supplement.html#tasks).

Pairs share development goals but not necessarily starting artifacts, implementation levels, or requested outputs. For example, A includes PyTorch→ONNX export on the CUDA side but starts from ONNX on CANN; H asks about large-model W8A8 quantization versus TensorRT INT8 calibration; M specifies Tiling implementation on CANN versus TensorRT/CUDA dynamic shapes; N explicitly requests a custom fusion pass on CANN; and Z additionally requests mappings to CUDA concepts on CANN. Each side is assessed against its frozen question, without adding the other side's requirements after execution. Differences describe this task set and access configuration; they do not isolate an ecosystem causal effect after controlling for scope.

The task package fixes M4/M9 applicability: E concerns the diagnostic interfaces and tools used, while I concerns compatibility among the named components. Missing local version facts do not make an applicable task inapplicable. Z is conceptual, with M4, M9, and M10 not applicable. Where the question permits alternatives, assessment follows the route actually adopted rather than requiring every possible option.

### Task execution and data analysis

WorkBuddy CLI requested `glm-5.3`, `deepseek-v4.1-flash`, and `kimi-k3-2`, displayed as GLM-5.3, DeepSeek V4.1 Flash, and Kimi. Identity is based on requested aliases and client response records; aliases do not guarantee immutable backend snapshots. All models used WebSearch, WebFetch, the same frozen tasks and rubric, at most four searches and eight fetches per episode, enforced before dispatch. The maximum was 22 turns with a 600-second collection timeout and generation effort set to low. The client managed the search provider without an independently locked backend; language/region, result-count configuration, and temperature were not exposed. The observed systems are model-and-tool configurations.

Each episode used a new temporary working directory and session with memory-disable flags, not an operating-system isolation guarantee. Three scheduling lanes interleaved tasks and ecosystems. Models produced and froze an unaided answer before the first tool call, then retrieved evidence and supplied an independent final answer; coordination subagents were not tested models. Selected episodes contain 491 searches and 942 fetches. All ordered search results and actual tool returns are retained. Budget-denied requests are not counted as dispatched calls; failed fetches count once, and initial obstacles remain separate from later recovery.

GLM-5.3 assessed every episode, with sources/prior answers and final outcomes evaluated separately. All 156 episodes have both predictors and outcome assessments, totaling 312 phase results. Original automated judgments, reviewed derivatives, and revision reasons remain separate. Technical retries were bounded and the first valid result was selected. Prior-only episodes without retrieval and an independent final answer were excluded. During targeted completion of two collection gaps and one assessment gap, an accidentally dispatched duplicate collection was also isolated and retained without entering analysis. Selection did not optimize scores.

The batch marks all 156 assessments as having no quotation-audit issues; 149 pass structural gates. A separate manuscript-preparation check compared 3,986 metric evidence entries in results.json with their named raw events, including nested JSON decoding: 3,960 matched literally; 26 entries across 23 episodes did not, including abbreviated or paraphrased excerpts and a protocol reference. The supplement flags each entry. The batch flag does not establish that every metric quotation has been verified. Statistics reproduce this commit without regrading these entries. Source ownership remains unresolved in seven CANN episodes: GLM J/X, DeepSeek T/W, and Kimi A/C/T. Targeted content review covered 149 episodes with M10 grades 3/4/5, task I, and identified issues; it is not expert verification of every technical claim. Review distinguished environment substitutions, missing substantive content, and code errors, and restored M9 judgments inconsistent with frozen applicability. There was no end-to-end hardware execution. M10 describes the content-level additions or corrections required.

M2 inventories cover actual fetch returns and equally aggregate the final states of independent official documents. Retries merge by requested URL without fragments; unknown mirrors or redirects are not presumed identical. Direct bodies without independent completeness evidence retain bounds. Unknown ownership cannot be silently dropped before averaging. Post-run ownership or body references may support evaluation but cannot enter the model's earlier context or retrieval-effort count.

Statistics first pair the two sides of the same task within each model. Main summaries follow the batch records, requiring both episodes to pass structural gates and carry a clean quotation-audit flag and to have a point or usable bounds for the indicator. Thus, an ownership issue also excludes that episode from other indicator pairs, and denominators vary. The supplement retains all 156 cells and exclusion reasons. Inapplicability, blockage, insufficient evidence, and unfinished assessment are not low scores. Differences are CUDA minus CANN, with bounds $[L_{CUDA}-U_{CANN},U_{CUDA}-L_{CANN}]$. Mean bounds average paired lower and upper endpoints separately; interval midpoints are not treated as observed scores. Means of ordinal M1–M10 grades are descriptive summaries without a claim of validated equal spacing.

Cross-model analysis examines average directions, task-level counterexamples, and the common eligible-task subset. Model observations do not turn 25 task pairs into 75 independent task types or substitute for repeated runs of the same model. All tasks belong to the prespecified analysis set, without a held-out set, hardware success-rate evaluation, or coefficient refitting. Source snapshots, derived calculations, and evidence locations are provided in the [revision supplement](supplement.html); the experiment reference is commit `87e04c1`.

### Task-level assessment results

All 150 episodes in the 25-pair main comparison completed collection and assessment; 143 pass structural gates. The six completed G episodes remain separate. Table 4 reports within-model eligible-pair differences; Figures 6–8 show the complete task-by-indicator matrices for the three models, retaining records and states excluded from the statistics. The supplementary matrix retains every task cell, unavailable state, and evidential reason rather than displaying only eligible observations.

| Indicator | GLM Δ (n) | DeepSeek Δ (n) | Kimi Δ (n) |
| --- | ---: | ---: | ---: |
| M1 Official discoverability | +0.04–+0.09 (23) | -0.13 (23) | +0.04–+0.28 (22) |
| M2 Official retrievability | -0.31–+0.85 (23) | -0.29–+0.93 (23) | +0.07–+1.15 (22) |
| M3 Official content detail | +0.48 (23) | +0.43–+0.57 (23) | +0.63–+0.69 (22) |
| M4 Version clarity | +0.23 (22) | +0.81–+0.87 (22) | +0.43 (21) |
| M5 Third-party richness | +0.13–+0.44 (23) | -0.18–+0.00 (23) | -0.50–-0.31 (22) |
| M6 Third-party credibility | +0.10–+0.40 (20) | -0.15–+0.40 (20) | -0.15–+0.20 (20) |
| M7 Model prior knowledge | +0.52–+0.57 (23) | +0.60–+0.70 (23) | +0.63–+0.69 (22) |
| M8 Retrieval effort | +0.30 (23) | +0.48 (23) | +1.05 (22) |
| M9 Version lockability | -0.37–-0.31 (22) | +0.32 (22) | +0.04–+0.15 (21) |
| M10 Operational executability | +0.14 (22) | +0.14 (22) | +0.09–+0.15 (21) |
| M11 Composite confidence | +4.73–+6.94 (20) | +6.80–+9.16 (18) | +8.00–+9.84 (18) |

: Table 4. Within-model mean difference Δ=CUDA−CANN, with task-pair counts in parentheses. M1–M10 range from 1 to 5 and M11 from 0 to 100. Ranges are evidence bounds on means, not statistical confidence intervals; endpoints are rounded outward to two decimals and point means to nearest. Higher M8 means fewer calls.

![Task-by-indicator matrix for GLM-5.3. CANN is above CUDA for each task. Solid cells encode points; hatched cells report evidence bounds; unavailable states remain explicit.](figures/figure-matrix-glm-en.svg){#fig:fullmatrixa description="25 tasks by 11 indicators, excluding G. M1–M10 use 1–5; M11 uses 0–100. Gate failures retain recorded values with a dagger. No midpoint coloring."}

![Task-by-indicator matrix for DeepSeek V4.1 Flash. CANN is above CUDA for each task. Solid cells encode points; hatched cells report evidence bounds; unavailable states remain explicit.](figures/figure-matrix-deepseek-en.svg){#fig:fullmatrixb description="25 tasks by 11 indicators, excluding G. M1–M10 use 1–5; M11 uses 0–100. Gate failures retain recorded values with a dagger. No midpoint coloring."}

![Task-by-indicator matrix for Kimi kimi-k3-2. CANN is above CUDA for each task. Solid cells encode points; hatched cells report evidence bounds; unavailable states remain explicit.](figures/figure-matrix-kimi-en.svg){#fig:fullmatrixc description="25 tasks by 11 indicators, excluding G. M1–M10 use 1–5; M11 uses 0–100. Gate failures retain recorded values with a dagger. No midpoint coloring."}

Average M3, M4, M7, and M8 differences favor CUDA in all three models, but individual tasks do not invariably agree. M1, M5, M6, and M9 show no uniform ecosystem advantage. M2 difference bounds cross zero for GLM and DeepSeek; Kimi favors CUDA on its eligible pairs, but interpretation on common tasks remains dependent on evidence bounds and task composition. After review, M10 mean differences are small, approximately 0.09–0.15 points, and do not establish execution success rates or a general answer-quality advantage.

Across all episodes, M11 has 29 points, 106 evidence-bounded results, and 21 insufficient-input results. The main comparison contains 29, 101, and 20 respectively; G contains five bounded and one insufficient-input result. The 21 insufficient cases comprise seven unresolved-ownership episodes and 14 additional episodes without usable M6 inputs. An independent expanded noise-OR polynomial check found no arithmetic discrepancies in the 135 computable results. Agreement in calculation does not validate the input judgments.

| Model | Pairs | CANN mean bounds | CUDA mean bounds | CUDA higher / CANN higher / unresolved |
| --- | ---: | ---: | ---: | ---: |
| GLM | 20 | 76.37–77.96 | 82.69–83.32 | 15 / 2 / 3 |
| DeepSeek | 18 | 77.48–78.38 | 85.18–86.64 | 12 / 3 / 3 |
| Kimi | 18 | 76.94–77.82 | 85.81–86.78 | 14 / 1 / 3 |

: Table 5. Mean M11 evidence bounds and task-direction counts for eligible pairs. An ecosystem is counted as higher only when its lower bound strictly exceeds the other's upper bound; overlapping bounds leave direction unresolved. No eligible task pair has point values on both sides.

The models share ten tasks with eligible M11 pairs: B, D, E, H, I, K, L, Q, U, and Y. On this identical subset, CUDA−CANN mean bounds are 3.29–5.45 for GLM, 5.41–7.95 for DeepSeek, and 5.34–7.28 for Kimi. Directions persist, but the subset covers only 40% of main tasks. This task-composition sensitivity check does not eliminate nonrandom missingness or validate coefficients. Z has no applicable M4 and receives a neutral version factor of 1; it is marked separately, with results excluding Z in the supplement.

![M11 matrix for 25 tasks, arranged by model and ecosystem. Evidence bounds, insufficient inputs, and gate failures remain visible; statistics still use eligible pairs.](figures/figure-matrix-m11-en.svg){#fig:accessprofile description="M11 matrix for 25 tasks, arranged by model and ecosystem. Evidence bounds, insufficient inputs, and gate failures remain visible; statistics still use eligible pairs."}

A conservative sensitivity check excludes every pair with an unresolved metric quotation on either side. M11 retains 15 GLM, 13 DeepSeek, and 14 Kimi pairs, with CUDA-minus-CANN mean bounds of 3.09–5.23, 7.59–9.94, and 7.84–9.68. M3, M7, and M8 retain their average direction; GLM M4 and M10 differences become zero, indicating that smaller component differences depend more on inclusion. This is not a formal adjudication of the quotations; see the [sensitivity calculation](quotation-sensitivity.json).

## Findings: Knowledge Conditions Across Development Tasks

Task-level comparisons organize knowledge conditions by development scenario, specific gaps, and source complementarity. The following separates repeated average directions, path-dependent task observations, and unresolved evidence, rather than treating a single acquisition outcome as an invariant ecosystem property.

### Knowledge-support distributions differ between ecosystems across development scenarios

Table 6 retains the existing three development scenarios and aggregates M11 separately on each model's eligible task pairs. Getting started/environment includes A/H/I/J/K/S/T/Y/Z; training/routine use includes E/F/P/Q/R; operators/in-depth development includes B/C/D/L/M/N/O/U/V/W/X. Labels describe activities without assuming a difficulty ladder. Eligible task composition differs across groups and models.

| Model | Development scenario | Pairs | CANN mean bounds | CUDA mean bounds |
| --- | --- | ---: | ---: | ---: |
| GLM | Getting started / environment | 8 | 79.57–81.26 | 86.75–87.37 |
| GLM | Training / routine use | 4 | 77.05–79.11 | 83.45–83.71 |
| GLM | Operators / in-depth development | 8 | 72.84–74.09 | 78.24–79.08 |
| DeepSeek | Getting started / environment | 6 | 76.12–76.98 | 84.01–85.95 |
| DeepSeek | Training / routine use | 4 | 82.76–83.54 | 88.40–88.57 |
| DeepSeek | Operators / in-depth development | 8 | 75.86–76.85 | 84.43–86.19 |
| Kimi | Getting started / environment | 6 | 84.40–84.82 | 88.09–88.56 |
| Kimi | Training / routine use | 4 | 70.99–72.40 | 90.27 |
| Kimi | Operators / in-depth development | 8 | 74.31–75.29 | 81.88–83.70 |

: Table 6. Evidence bounds on within-scenario paired M11 means, excluding G. Each row uses tasks eligible on both sides for that model. Z receives a neutral version factor; group means are not task-difficulty rankings.

For GLM, CANN means decline from getting started through routine use to in-depth development. DeepSeek's routine group is highest, whereas Kimi's is lowest. The observations therefore do not support a uniform declining sequence as a general CANN pattern. The workflow debugging group has only E/X and not every model retains both pairs, also preventing a stable claim that debugging has the largest gap. Scenario groupings help identify tasks for investigation but do not replace task evidence.

Implementation tasks such as D and M still reveal concrete gaps, with variation within groups. For D, CANN M3 is 3, 4, and 3 for GLM, DeepSeek, and Kimi, versus CUDA 4, 5, and 5. Acquired project-generation, build/deployment, and framework-integration material varies by path, as do unresolved Kernel or Tiling details. Conversely, H quantization has CANN M10=4 and CUDA M10=3 in all models, providing a counterexample. Its quantization targets and question scopes differ, so it cannot establish a general quantization-ecosystem ranking.

### Official-source discovery, acquisition, content, and version organization reveal distinct gaps

Mean M1 differences do not share a direction across GLM, DeepSeek, and Kimi. Earlier single-model search differences therefore cannot be presented as a stable ecosystem-wide visibility gap. Models choose queries, rewrites, and sources; M1 records official-result positions along those paths, rather than a fixed-query search-ranking experiment.

Discovering an official source can lead to scaffolding, a summary, or a direct body with uncertain completeness. M2 aggregates independent documents within episodes and is not interchangeable with the earlier task-level proportion obtaining core content. Both ecosystems require inspection of the target, request, and returned representation. An absent body establishes a failure of that acquisition, not SPA, robots, or a particular delivery technology as its cause.

All CANN D episodes obtained some official procedural content, so D is no longer an instance of the entire core official channel being unavailable. Kimi acquired build/install commands, PyTorch packaging steps, and integration instructions, but essential Kernel/Tiling implementation detail remained missing. DeepSeek acquired additional project and invocation material, with gaps such as adaptation-function implementation. Although GLM's CUDA side has M3=4, the final setup.py source names disagree with the displayed file layout, yielding reviewed M10=3; its CANN M10 is 4. Detailed sources do not ensure that generated guidance needs no correction. [Task D evidence](supplement.html#task-D) retains the event references and assessment reasons.

E distinguishes support from an error-code entry and from diagnostic guides. GLM acquired an EZ9999 entry with generic checks plus a troubleshooting flow and asys collection commands, yielding M3=3. DeepSeek obtained log collection, `msnpureport -f`, `python3 msaicerr.py -p ... -out ...`, and hardware-diagnostic material, yielding M3=4. Kimi obtained error-field explanations and some investigation guidance, yielding M3=3. All CUDA sides have M3=4. The gap belongs to specific entries, obtained steps, and unresolved branches; it does not establish that the CANN ecosystem lacks concrete diagnostic guidance. [Task E evidence](supplement.html#task-E) links the original events.

A still illustrates supported main steps alongside local acquisition obstacles. GLM's CANN run obtained ATC commands, `--input_shape`, `--soc_version`, and the `npu-smi info` selection rule, while some installation or reference material returned only scaffolding. DeepSeek obtained environment setup and conversion parameters through other official paths. Models did not inspect identical resource combinations, and obtaining another body does not erase earlier obstacles. Kimi A-CANN has unresolved ownership and is excluded from quantitative pairs, while its original process remains in the supplement.

Call-count differences share a direction across models. On the same M8 paired tasks, average dispatched search-plus-fetch counts for CANN/CUDA are 9.74 / 8.96 (n=23) for GLM, 10.78 / 9.26 (n=23) for DeepSeek, and 8.95 / 6.36 (n=22) for Kimi. These include failures and recovery attempts. They are not elapsed time, token use, or total computational cost, and fewer calls do not necessarily mean a better answer.

Version assessment concerns obtained applicability relations rather than counts of versions. All CANN I runs obtained torch_npu/PyTorch/CANN compatibility tables, but not the complete firmware/driver relation. CUDA runs obtained several pairwise tables without establishing the full relation between the selected PyTorch wheel and its actual cuDNN dependency. After review, M4 and M9 are both 3 on both sides in all models. Shared support for a CUDA version does not establish PyTorch-wheel/cuDNN compatibility, and a lookup entry is not an acquired relation. [Task I evidence](supplement.html#task-I) separates acquired tables, target-page returns, and final answers.

Source applicability and local environment facts remain distinct after retrieval is delegated. Missing compatibility relations require further source inspection; missing installed-version facts require environment checks. M9 describes the scope and granularity of supported version choices. A conditional range can be appropriate for a methodological question without local facts; failure to select a unique version is not automatically a technical error.

### Complementary support and limitations across knowledge sources

M5 direction varies by model: GLM paired means favor CUDA, DeepSeek's bounds reach zero, and Kimi favors CANN. Counts represent relevant deduplicated third-party sources actually discovered within the common budget, not the ecosystem's total community size. Official repositories and publishers remain official regardless of GitHub or blog hosting, while uncertain ownership remains unknown.

Source numbers do not directly establish verifiable support. Besides seven ownership issues, 14 episodes lack usable M6 inputs and cannot yield M11. Insufficient acquisition or checking of consequential claims cannot automatically set the third-party channel to zero. DeepSeek and Kimi mean M6 differences cross zero; GLM's small difference also requires inspection of claims and common-task results.

M7 uses the frozen pre-retrieval answer. All models have higher mean knowledge performance on the CUDA questions, describing correctness and coverage without tools rather than training-data density or ability across all development tasks. M7 and M9/M10 evaluate different objects and cannot be subtracted to measure retrieval gain. Sources, prior answers, and final responses must remain connected through specific requirements and evidence.

Of the 29 point M11 results, 26 have M7=5, setting OWN=1, and three have M5=M6=5, setting SEC=1; the channel combination K is consequently 1. Twenty-six points are CUDA and three CANN. A point index does not imply that uncertainty in every source indicator has disappeared, and point-only ecosystem comparisons would be selective. Channel fallback explains the aggregation while also showing why it cannot replace separate body, version, and final-answer checks.

Reviewed M10 mean differences are small. Concrete errors can occur even when detailed material is available, including inconsistent source filenames in D and an incorrect automatic-differentiation expression in O. Presenting final-answer checks alongside source conditions distinguishes tasks needing better documentation from those needing corrected generated guidance. A high M11 neither guarantees a high M10 nor establishes reproduction on target hardware.

## Discussion: Design Implications for Knowledge Provision and Agent Interaction

The comparisons develop an account of ecosystem knowledge support through development scenarios, specific knowledge gaps, and complementary sources. We use these results to discuss development priorities, improvements to official resources and agent feedback, and community knowledge and source inspection. The design illustrations make potential applications concrete; their effects have not been evaluated.

### Setting development priorities through scenarios and knowledge requirements

The results locate priorities in the knowledge required by specific tasks. D, M, and related tasks still motivate checking implementation guides, procedural detail, and supplementary cases, but model-dependent scenario ordering does not establish a uniform priority ranking. E likewise shows that different paths obtain different diagnostic support. Comparing acquired material with remaining requirements makes task-level diagnoses inspectable and actionable.

These insights imply different scopes of improvement. Missing necessary relations in I motivate queryable compatibility information. D requires distinguishing procedural material already acquired from implementation gaps, then checking coverage, links, and delivery. E motivates connecting error entries to existing diagnostic guides and clarifying unresolved branches. Tasks without verifiable third-party support require inspection of practical evidence and source ownership. Improvements can be assessed by returning to the original task requirements.

### Improving official knowledge provision and agent feedback

Recurring version issues suggest treating applicability as a property of a documentation system. A stable recommended-version entry can coexist with clearly indexed documentation for earlier versions, while each page states its applicable versions and verification date. Compatibility relations among drivers, toolkits, frameworks, and integration packages can be published in a queryable form. For a task such as I, this would let a developer or agent request the supported combinations for a stated environment, reducing the need to assemble the relation from several disconnected records.

Figure 10 makes this proposal concrete through a compatibility lookup interface. Device and framework constraints define the query, and each returned combination retains its sources, applicability scope, and verification date. Where no supported match is documented, the interface identifies unresolved conditions. The version problem registered by M4 becomes an inspectable relation, providing a basis for subsequently checking the applicability of a response.

![Proposed version and compatibility lookup, motivated by fragmented version information in A and I. Query constraints, result fields, and source inspection illustrate the proposed information structure; compatibility values are placeholders.](figures/figure-6-compatibility-design-en.svg){#fig:compatibilitydesign description="A proposed compatibility lookup interface has target-device and framework-version selectors, followed by result fields for toolkit, driver range, framework, integration package, and supporting sources. Placeholder fields illustrate the structure without asserting compatibility values. Each relation retains provenance, applicability scope, and a verification date; unmatched queries identify unresolved conditions. The motivation is necessary applicability relations to verify in tasks A and I."}

Version-dependent guidance should connect a source's applicability to the available task environment. Before proposing a toolkit/framework combination, an agent can use device and software facts already supplied in the task, requesting only information that remains necessary to establish the match. The response indicators then ask whether the recommendation states its applicable version conditions and provides actionable steps with explicit substitutions or modifications.

Figure 11 illustrates version checking through a separate environment record. It distinguishes developer-supplied local facts from the applicability declared by a source, then records the comparison as matched, mismatched, or insufficient information. The record is reused within the task and updated with additional user input to support applicability checks before specific commands are recommended.

![Proposed environment declaration and version checking, motivated by A and I. Device, toolkit, and framework fields represent developer-supplied local facts, separate from source applicability. The illustrated state has insufficient information to establish a match.](figures/figure-10-environment-design-en.svg){#fig:environmentdesign description="An environment record contains placeholder fields for device model, toolkit, framework, and integration versions. A separate area presents the cited material's version and compatibility conditions and identifies the missing information needed to establish a match. Checks can be matched, mismatched, or insufficient information, and the developer can update the task's environment record."}

Localized acquisition and content gaps call for task-specific repairs. D already obtained some official procedural content; the next step is to locate missing Kernel, Tiling, or framework-integration requirements and check whether the relevant guides exist, can be discovered, and are actually delivered. Complete HTML or synchronized Markdown and plain-text exports are possible delivery mechanisms, but a file format does not establish task coverage. E motivates stronger links from an error entry to existing log-collection, AI Core error-analysis, and hardware-diagnostic guides, with explicit tool applicability. A catch-all error entry should explain what the code alone cannot establish and which logs or observations are needed next. This organizes existing knowledge while identifying remaining diagnostic branches.

Figure 12 illustrates task-oriented content through E's error page. It starts with what the code can establish, identifies local information to collect, links observable symptoms to checks and attributed cases, and retains a support route for unresolved situations. Domain maintainers would need to establish the actual causes, checks, and cases; the structure helps locate the knowledge that needs to be supplied.

![Proposed task-oriented diagnostic content, motivated by E's dedicated error page with generic guidance. The structure connects a diagnostic starting point, local information, checks, case evidence, and unresolved branches. Specific cases and version scopes remain fields to populate.](figures/figure-7-diagnostic-content-design-en.svg){#fig:diagnosticdesign description="A proposed EZ9999 diagnostic page first states that the code alone does not identify a cause, then organizes logs, triggering operations, and environment information. A table connects observable conditions to checks and attributed cases, followed by unresolved branches and support. The content structure is illustrative and asserts no verified causes or cases."}

The same task-oriented structure can guide other documentation units. An intended outcome, prerequisites, minimal commands or code, parameter explanations, expected output, and recovery information provide concrete material for both human reading and agent retrieval. Machine-readable exports and indexes should preserve those relationships and their version scope. Their success can be checked against the relevant content-acquisition and detail fields for the task that motivated the change.

Figure 13 proposes delivery of the same task material through a document body and a machine-readable export. ATC conversion steps, parameters, and device-query relations acquired in A illustrate the information types to preserve; the figure’s commands and version fields are structural examples, not quotations from this batch. Exports should retain task, applicability, source, parameter explanations, and related steps. For a partially acquired route such as D, acceptance checks should establish whether missing implementation requirements are delivered, beyond checking for a particular file format.

![Proposed document body and machine-readable export. The structure follows command, parameter, and device-query relationships involved in A. Commands and versions are illustrative examples, and the export is a design proposal.](figures/figure-8-readable-export-design-en.svg){#fig:readableexportdesign description="Both views retain task, applicability, source, and step relationships. Example contents illustrate the structure and are not literal quotations from this batch."}

An agent interface can preserve the difference between finding a source, obtaining its body, and supporting a proposed step. For D, useful feedback would state both the procedural material acquired and the implementation requirements still missing. For E, it would distinguish a generic error entry from the diagnostic guides acquired and identify branches requiring further sources or local logs. For A, it could retain the conversion path while identifying localized acquisition obstacles. These statuses connect retrieval events to specific task requirements.

Figure 14 contrasts proposed responses to D and E. For D, the agent seeks specific sections addressing missing implementation requirements while retaining acquired sources. For E, it links the error entry to diagnostic guides and explains how local information helps select the next check. Developer-supplied content is a fallback when necessary material cannot be acquired. M1–M3 locate the gaps, while M8 records subsequent call effort.

![Proposed feedback for two knowledge gaps: (a) partial procedural acquisition with essential implementation gaps in D; (b) connecting a generic error entry to diagnostic guides and local observations in E. Messages and actions are design proposals.](figures/figure-9-acquisition-design-en.svg){#fig:acquisitiondesign description="The left seeks missing implementation sections after partial procedural acquisition; the right links an error entry to diagnostic guides and necessary local information. These are design illustrations, not original dialogues."}

Knowledge provision also involves entry points and maintenance. Stable, searchable official entries affect whether candidate materials are discovered; explicit ownership, revision dates, and compatibility relations support subsequent assessment. Teams can use representative tasks as recurring inspection units, tracking whether queries reach the intended material, its body is delivered, version relations have changed, and community cases remain applicable. Such maintenance also addresses source governance and third-party knowledge provision beyond the illustrated interfaces.

To address differences in search visibility, documentation teams can inspect search-engine indexing and the alignment of page titles and summaries with development-task terminology, assessing search engine optimization (SEO) improvements through official-result positions and the rounds needed to discover material for task queries.

### Expanding community knowledge and supporting source inspection

Community knowledge development can address task situations that lack adequate support, including specific failures, operating experience under different configurations, and alternative implementations. This direction connects to research on augmenting API documentation with Stack Overflow insights [@treude2016]; the present study additionally examines whether agents can discover and acquire such material and whether it supports specific task requirements. Tasks with few candidate sources require checking which supplementary explanations are missing; concentrated or inaccessible sources require checking independent practical evidence and content-delivery conditions. The aim is for task-relevant experience to be discoverable, obtainable, and attributable, beyond simply increasing the number of entries.

Consistent with human–AI interaction guidelines on explaining behavior and supporting correction [@amershi2019], agents can retain source passages, applicability conditions, and their relationships to suggestions to help developers inspect available support. Where content remains missing, they should identify unsupported parts of the task and direct further searches or requests for necessary local information accordingly. The source-inspection and corrective-feedback illustration makes these information relationships concrete.

Because explanations can increase acceptance without improving team performance [@bansal2021], source presentation should be evaluated by developers’ ability to identify unsupported or inapplicable suggestions.

Figure 15 further illustrates source inspection and corrective feedback. A developer can expand the cited passage for a command, inspect its applicable version, and attach an encountered error or correction to the suggestion. The original source, task environment, and new feedback remain connected so the next check can address the specific discrepancy. This provides inspectable support for the response properties described by M9 and M10 and for subsequent revision.

![Proposed source inspection and corrective feedback. Commands and versions are illustrative examples; source expansion, original-page access, and error feedback linked to a suggestion are proposed interactions.](figures/figure-11-verification-design-en.svg){#fig:verificationdesign description="Expand a source and its version scope from a suggestion, attach a reported error, and preserve task context. Commands and versions illustrate the structure rather than quote this batch."}

These proposals treat checking suggestions as part of programming work, consistent with the information-seeking and AI-assistance studies discussed earlier [@brand2009; @vaithilingam2022; @barke2023]. Exposing every retrieval event or source passage could add reading effort without clarifying the next action. An interface could first show the supported step, relevant version scope, and unresolved condition, with source passages available on demand. This prioritizes the information needed for the current judgment while retaining a route to detailed inspection.

Requests for environment facts can likewise interrupt a task, especially when they repeat information already provided. A request should explain which recommendation depends on the missing fact and reuse task context where available, with confirmation when it may be stale. For diagnostic logs, it should request relevant excerpts and allow sensitive details to be removed. Missing compatibility relations and generic error explanations require work by documentation and system teams; collecting more local facts cannot supply those missing explanations. The balance between inspection, interruption, and useful guidance remains a question for evaluating these proposals.

### Reusing the diagnostic method

The method connects a task requirement to a source or acquisition event, an indicator code, and a diagnosis of the information needed to assess a proposed action. Professionals such as product managers, designers, technical writers, and software engineers who develop and maintain developer platforms, technical knowledge resources, or AI agents could use the profile to locate missing guidance or applicability relations and distinguish further source retrieval from a request for a local fact. Analysts can reuse the record structure with domain-specific requirements, such as client-server compatibility in a database SDK or deployment prerequisites in a web framework. These are intended applications of the method.

Subsequent evaluation can examine whether independent analysts produce comparable profiles, whether the diagnoses correspond to expert assessments of missing information, and whether documentation teams find them useful for planning repairs. These questions follow directly from the intended use of the method. The present application supplies the task-level distinctions, worked records, and cross-task synthesis on which such evaluation can build.

## Limitations and Research Transparency

The study covers 26 prespecified task categories, retaining one valid episode per model and side. Twenty-five pairs enter the CANN/CUDA comparison and G remains separate. Tasks are neither a random population sample nor an independent held-out set; starting conditions, scope, and implementation levels are not guaranteed equally difficult. Three models provide cross-model observations under one protocol, not repeated runs of the same model or estimates of within-cell stochastic variation. Aliases do not guarantee fixed snapshots, the search provider and some sampling parameters were not independently locked, and model and tool effects are intertwined.

All automatic assessments used GLM-5.3, allowing same-model assessor bias. Original judgments and reviewed revisions remain available; targeted M10 and version review is not independent expert verification of all content. Quotation matching, structural gates, and arithmetic audits concern evidence location, structure, and calculation respectively, not technical correctness. The supplement identifies 26 unresolved quotation-location issues; current statistics do not change batch eligibility on that basis. Some ownership and body-completeness judgments remain unknown. Failure to obtain content cannot establish its absence from the website or a particular delivery technology.

All seven unresolved-ownership episodes are CANN, and the main summaries exclude entire affected episodes. Fourteen additional episodes lack usable M6 inputs for M11. Eligible samples may consequently favor tasks whose evidence is easier to establish. Descriptive checks on common tasks and after excluding Z do not remove selection bias. M11 evidence bounds do not incorporate run randomness, assessor error, or unmodeled uncertainty and are not statistical confidence intervals. A saturated noise-OR channel can produce a point composite even when other inputs remain bounded. Coefficients, scoring consistency, and validity for intended uses require independent evaluation; this batch neither refits coefficients nor establishes weight validity.

There was no end-to-end hardware execution, so M10 is not a command or code reproduction success rate. How developers use the evidence to judge local applicability, and how proposed feedback affects reading burden, interruptions, and actual task completion, requires user research. The literature provides conceptual and methodological support, not direct validation of the study's five-level thresholds, coefficients, or design effects.

## Conclusion

We define knowledge availability for AI through eleven indicators connecting knowledge sources, acquisition processes, and response properties. Task-level comparisons of CANN and CUDA identify average differences in official content detail, version relations, pre-retrieval knowledge performance, and call effort, alongside model- and task-dependent scenario distributions and source complementarity. Cases distinguish partial procedural acquisition with essential gaps, limited error entries supplemented by other diagnostic guides, and incomplete acquisition of compatibility relations. Connecting scores with task requirements and acquired material produces concrete insights into how ecosystems support development activities and which knowledge resources require improvement.

The method makes the basis for AI-mediated technical guidance an object of inspection: which source supports a proposed step, which applicability relation remains unresolved, and what additional information is needed. The framework, protocol, and case analysis provide a way to locate these conditions and relate them to knowledge provision and agent feedback. Documentation repairs, source retrieval, and requests for local facts follow from different diagnoses, offering concrete directions for subsequent evaluation.

## Appendix A: Scoring calculations {.unnumbered}

The following M1–M10 grades and decision boundaries follow this batch’s frozen rules.md and execution-checks.md. The grades are study conventions, not thresholds directly validated by cited literature. Raw records preserve pending, missing, inapplicable, blocked, and insufficient-evidence states.

**M1 Official source discoverability**

1. No relevant official source within the prespecified common search budget
2. First relevant official source on query 3 or later
3. First relevant official source on query 2
4. First query: relevant official source at position 2–5
5. First query: relevant official source at position 1

The batch inspects five results per query, with at most four queries; these are experimental conditions. Count queries, not differently batched calls. Later searches after the first hit do not lower the score. Earlier timeouts, missing lists, or stopping before exhausting the budget without a hit leave the score pending. Preserve every ordered URL and exact position.

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

Use the continuous formula in the main text: $x_i=M_i/5$, $OFF=x_1x_2x_3$, $SEC=x_5x_6$, $OWN=x_7$, and $M11=100[1-(1-OFF)(1-SEC)(1-OWN)](0.7+0.3x_4)(0.9+0.1x_8)$. Report M9/M10 separately. Retain full precision, display points to one decimal, and round interval endpoints outward without five-level conversion. Propagate usable bounds by monotonicity, without substituting midpoints. A confirmed unavailable channel contributes zero only with reviewed reasons and evidence. Prespecified inapplicable M4 makes its factor 1 while M4 remains N/A; missing M8 is not neutral. Inputs without usable bounds remain incomplete rather than zero. Coefficients 0.30/0.10 are working settings, not fitted optima or calibrated probabilities. Evidence bounds do not encompass run randomness or all assessment error.
