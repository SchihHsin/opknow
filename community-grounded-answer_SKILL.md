---
name: community-grounded-answer
description: Use when answering a version-sensitive or ecosystem-specific developer question (e.g. operator development, training/inference deployment, performance tuning on stacks like CUDA/PyTorch, Ascend/CANN, ROCm) by grounding the answer in official + community sources. Trigger when the user wants a transparent, traceable answer; wants to compare how the same task differs across two tech stacks; or wants to assess "from a user-task perspective, how usable is community X's documentation/AI support". Produces a step-by-step workflow with input/output per step, honest notes on what was and wasn't done, and (for comparisons) a 7-dimension metric scorecard. Do NOT use for stable general-knowledge questions that need no retrieval.
---

# Community-Grounded Answer

Answer a concrete, version-sensitive technical question by *running* a grounded retrieval workflow, recording every step transparently, and (when two stacks are compared) scoring the experience on a fixed metric structure. The point is traceability: the user should see exactly which sources were hit, which step fell short, and how confident the final answer is.

## When to use vs. not

Use when the answer depends on a specific toolchain version, hardware, or fast-moving ecosystem content, OR when the user asks to compare stacks / assess a community's usability. Do **not** use for timeless conceptual questions (definitions, math, settled history) — those need no retrieval and this skill would be overkill.

## The four phases (run in order)

1. **Analyze the question.** Classify it: stable-concept vs version-sensitive vs toolchain-specific vs time-sensitive. Extract searchable entities (product / tool / version / chip / framework). Flag missing constraints the user didn't state (which version? what hardware? which call path?). Decide the path: concept → may answer from knowledge; version-sensitive/uncertain → **must retrieve, never give commands from memory**.

2. **Find community info.** Search broad → narrow, evolving keywords (add "official / docs / version / exact error"). Prefer sources by this hierarchy: (1) first-party official docs, (2) official tutorials/repos, (3) high-reputation secondary (well-known GitHub, top Stack Overflow), (4) ordinary blogs (CSDN, 博客园, Medium — cross-check against official), (5) forums/UGC/aggregators (last resort). Search each sub-question separately.

3. **Identify / judge sources.** Apply: authority (official > secondary), recency (check date AND version — a version-mismatched "correct" answer is wrong), consistency (cross-check multiple sources; conflict → stay skeptical), completeness (if snippets don't confirm details, `web_fetch` the full page), copyright (paraphrase, don't copy), and self-check (*am I answering from memory or from evidence I just retrieved? familiarity ≠ currently correct*).

4. **Fallback ladder when not found / not fetchable** (climb only as needed, never fabricate): (a) reformulate keywords/angle; (b) switch source if official is unreachable (e.g. JS single-page-app whose body won't extract → try official tutorial, static mirror, or a different extraction); (c) `web_fetch` full text of the most authoritative hit; (d) ask the user to fill the missing constraint; (e) fall back to priors **but explicitly mark "not verified against official docs"** and link the official source; (f) if still nothing, say so plainly — no invented commands, parameters, or citations.

## Record the run as a workflow

As you execute, log each step as a node with **input → action → output**. Mark honestly:
- real tool calls (which query, which sources actually hit),
- steps you skipped and why (e.g. "did not ask user for version", "skipped web_fetch"),
- steps whose output was degraded (e.g. "official site is SPA, body not extracted → fell back to meta summary").

Never depict a step (like a `web_fetch`) that you did not actually perform. The workflow is a faithful log, not an idealized diagram.

## Score on the metric structure (for comparisons / usability assessment)

Rate the run on 7 dimensions (1–5; ⑤ is reverse — higher = worse):
1. **Version sensitivity** — how much the answer changes with version/hardware (high → must retrieve).
2. **Authoritative-source reachability** — how easily official docs are found (rounds) AND fetched (static vs SPA).
3. **Secondary-ecosystem depth** — abundance + reliability of good third-party content.
4. **Model prior strength** — coverage density in training data → how much can be answered from knowledge.
5. **Retrieval cost** *(reverse)* — number of search/fetch rounds to a reliable answer.
6. **Answer verifiability** — can the version be pinned and steps be made reproducible?
7. **Final confidence** — overall trustworthiness (the outcome the other six predict).

Quick read: ②③④ all low → expect high ⑤ and low ⑥⑦ (effortful, lower-confidence run); ②③④ all high → fast convergence. ② alone low (paywall/SPA/fetch fail) → trigger fallback even if the ecosystem is rich. ⑥ low (can't pin version) → must ask the user; otherwise cap confidence at "medium".

## Output format

Default: a transparent step-by-step workflow (input/output per node) + a short prose answer with official links and stated prerequisites/version caveats. When comparing two stacks or assessing usability: also emit the 7-dimension scorecard and a one-line takeaway. When rendering visually, align corresponding steps across stacks in the same column so differences and their causes can be read together; size cards to content (don't force-stretch short cards).

## Honesty bar (non-negotiable)

State which searches were run, which sources were hit, where a step fell short, and the final confidence — every time. Traceable, therefore trustworthy.
