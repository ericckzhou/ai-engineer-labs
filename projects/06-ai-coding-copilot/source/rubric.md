# Assessment Rubric — Project 06: AI Coding Copilot

> Used to evaluate the learner's completed project.
> Self-assessment first. Mentor review second.
> Dimensions and weights are the lab-standard master rubric; the **Project-06 evidence prompts**
> under each dimension are specific to this lesson (`source/lesson.agent.md`).

---

## Dimension 1: Understanding (25%)

Evaluated by reviewing UNDERSTANDING.md and UNDERSTANDING_FEEDBACK.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Explains all concepts clearly in own words. Analogy is original and accurate. No gaps in understanding. Can answer follow-up questions. | 25 |
| 3 — Good | Explains most concepts correctly. Minor gaps or oversimplifications. | 20 |
| 2 — Developing | Some correct understanding but significant gaps or misconceptions present. | 15 |
| 1 — Beginning | Surface-level understanding only. Heavy reliance on lesson language without internalization. | 10 |

**Project-06 evidence prompts — look for whether the learner can:**
- Explain why giving the model **tools** beats a cleverer prompt, connecting *acting* to **hallucination reduction** (ReAct).
- Describe the **tool-use protocol**: tool schema → the model emits a *call* → your code *executes* → you feed the *result* back → repeat.
- Articulate "the **description is the API**" — that the model picks tools from the schema alone (the agent-computer interface).
- Explain why the loop must be **bounded** and why every file path must be **sandboxed**, and which failure each prevents.

**Score: ___ / 25**

**Evidence:**

---

## Dimension 2: Implementation (30%)

Evaluated by reviewing code/ and IMPLEMENTATION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Code is correct, clean, and runnable. Architecture demonstrates understanding of the underlying concepts. No magic — learner understands every line. | 30 |
| 3 — Good | Code works correctly. Minor style or architecture issues. | 24 |
| 2 — Developing | Code partially works. Key components missing or incorrect. | 18 |
| 1 — Beginning | Code does not run or produces incorrect results. | 12 |

**Project-06 evidence prompts — look for whether the implementation:**
- `tools.safe_resolve` resolves under the repo root and **rejects traversal** (`../…`) with `ValueError`. (M1)
- `agent_loop.parse_tool_calls` `json.loads` the `arguments` **string** into a dict and returns `[]` when the model answered. (M2)
- `tools.dispatch_tool` routes to the right file op and returns an **error string** (not a raise) on an unknown tool. (M3)
- `agent_loop.run_agent` appends the **assistant turn before** the tool results and is **bounded by `max_steps`**. (M4)
- The live copilot answers using files it actually **read via tools** (M5), ideally with a file/line citation.
- Guiding tests in `code/tests/` pass.

**Score: ___ / 30**

**Evidence:**

---

## Dimension 3: Failure Analysis (20%)

Evaluated by reviewing FAILURE_ANALYSIS.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | 3+ intentional experiments. Each experiment correctly diagnoses why the failure occurred. Clear production implications. | 20 |
| 3 — Good | 2+ experiments with good analysis. | 16 |
| 2 — Developing | 1 experiment with shallow analysis. | 12 |
| 1 — Beginning | No intentional breakage, or breakage without analysis. | 8 |

**Project-06 evidence prompts — strong analyses typically include:**
- A **no-cap ablation** (remove `max_steps`) with a model/scenario that loops, showing the runaway and the token/cost blow-up.
- A **no-sandbox ablation** showing `read_file` returning a path outside the repo (`../…`) — and why `safe_resolve` closes it.
- A **no-feedback ablation** (don't append tool results) showing the model ignore its own actions or the provider erroring on an orphan tool result.
- A **no-tools ablation** (ask the bare model) showing a confident **hallucination** about code it never read — the ReAct argument made concrete.

**Score: ___ / 20**

**Evidence:**

---

## Dimension 4: Evaluation (15%)

Evaluated by reviewing EVALUATION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Quantitative results for all major criteria. Honest assessment of production readiness. Cost analysis included. | 15 |
| 3 — Good | Most criteria measured quantitatively. Minor gaps. | 12 |
| 2 — Developing | Mostly qualitative ("it seemed to work"). Few numbers. | 9 |
| 1 — Beginning | No meaningful evaluation. | 6 |

**Project-06 evidence prompts — quantitative means actual numbers/traces, e.g.:**
- **Tool-call traces** for a handful of questions: which tools were called, in what order, how many steps.
- **Grounding check**: across test questions, did the answer cite a real file/line that actually contains the claim (vs. a hallucination)?
- **Step counts** and how often the loop hit `max_steps`; effect of injecting context vs. tools-only on steps-to-answer.
- An honest production note: token cost per question (tool schemas + tool results add input tokens — source: `sources/official-docs/anthropic-tool-use.md`), and what breaks on a large repo without chunked retrieval.

**Score: ___ / 15**

**Evidence:**

---

## Dimension 5: StarcallOS Reflection (10%)

Evaluated by reviewing STARCALLOS_REFLECTION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Identifies 2+ concrete, non-obvious patterns applicable to StarcallOS. Explains mechanism and implementation path. | 10 |
| 3 — Good | Identifies 1 concrete applicable pattern with good explanation. | 8 |
| 2 — Developing | Reflection is generic or surface-level. | 6 |
| 1 — Beginning | No meaningful StarcallOS connection made. | 4 |

**Project-06 evidence prompts — concrete connections include:**
- A StarcallOS capability that **acts on the user's behalf** framed as a tool loop — naming the tools, their schemas (the ACI), and the sandbox/permission boundary each needs.
- How a **bounded loop + grounded answers** keep a StarcallOS agent safe and trustworthy (no runaway cost, no hallucinated actions) — mechanism + implementation path, not "we could add an agent."

**Score: ___ / 10**

**Evidence:**

---

## Total Score

**___ / 100**

| Range | Level |
|-------|-------|
| 90–100 | Ready for next project |
| 75–89 | Ready with minor gaps — document them |
| 60–74 | Revisit the weak dimensions before proceeding |
| Below 60 | Return to the lesson and rebuild |

---

## Mentor Notes

**Overall assessment:**

**Strongest dimension:**

**Area most needing work:**

**Recommended next steps:**
