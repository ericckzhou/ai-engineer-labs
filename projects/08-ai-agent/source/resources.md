# Resources & Sources

> All sources used for this lesson, organized by tier.
> Every claim in lesson.agent.md traces back to one of these.
> Project 08 is **Project 06's loop made reliable** — the agent sources carry over, with the
> emphasis shifted from *how the loop works* to *how to make an autonomous loop safe and when to
> use one at all*.

---

## Tier 1: Official Documentation

> Primary sources. Check these first.

- **Anthropic — Building Effective Agents** — `sources/articles/building-effective-agents.md`
  - URL: https://www.anthropic.com/engineering/building-effective-agents
  - What to read: **workflows vs. agents** (predefined code paths vs. the LLM directing its own process); "the most successful implementations use simple, composable patterns"; **"add complexity only when it demonstrably improves outcomes"** (the *when not to* lesson); agents suit "open-ended problems where it's difficult or impossible to predict the required number of steps"; the named patterns (prompt chaining, routing, **orchestrator-workers**, **evaluator-optimizer**). The source for *whether* and *when* to build an agent.

- **Anthropic — Tool Use (Function Calling) Overview** — `sources/official-docs/anthropic-tool-use.md`
  - URL: https://platform.claude.com/docs/en/docs/build-with-claude/tool-use/overview
  - What to read: the tool-use protocol and the **agentic loop** that repeats until a stop condition; `tool_choice`; why the loop must be **bounded**. Carried from Project 06; in Project 08 the bound generalizes from a step cap to a full budget.

- **Anthropic — Pricing** — `sources/official-docs/anthropic-pricing.md`
  - URL: https://www.anthropic.com/pricing
  - What to read: per-MTok input/output pricing and the cost formula — for a real `max_usd` cost budget. Do **not** invent per-token prices; read them here (carried from Project 01).

- **LiteLLM — completion()** — `sources/official-docs/litellm-completion.md` (carried from Project 01/06)
  - URL: https://docs.litellm.ai/docs/completion/input
  - What to read: the `tools` / `tool_choice` params, the OpenAI-style `tool_calls` shape (`arguments` as a JSON string), and `usage` for live token accounting in the budget.

---

## Tier 2: Foundational Papers

> Academic papers that established the concepts in this lesson.

- **ReAct** — `sources/papers/react-paper.md`
  - Title: ReAct: Synergizing Reasoning and Acting in Language Models
  - Authors: Yao, Zhao, Yu, Du, Shafran, Narasimhan, Cao
  - Year: 2022
  - URL: https://arxiv.org/abs/2210.03629
  - Why it matters: the loop's grammar (Thought → Action → Observation), and specifically that **"reasoning traces help the model … handle exceptions"** — the basis for tool-error recovery. Also why a reasoning step makes the loop *terminate* (decide it's done) rather than thrash.

- **MT-Bench / LLM-as-a-Judge** — `sources/papers/mt-bench.md` (carried from Project 07)
  - Title: Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
  - Authors: Zheng et al.
  - Year: 2023
  - URL: https://arxiv.org/abs/2306.05685
  - Why it matters: evaluating with **numbers, not impressions** — applied here to *runs* (completion + efficiency across a task set) instead of single answers. The discipline behind `evaluate_run`.

- **Generative Agents** — `sources/papers/generative-agents.md` (carried from Project 05)
  - Title: Generative Agents: Interactive Simulacra of Human Behavior
  - Authors: Park et al.
  - Year: 2023
  - URL: https://arxiv.org/abs/2304.03442
  - Why it matters: **reflection** — synthesizing a higher-level judgment from raw steps — for the optional reflection/evaluator-optimizer loop.

---

## Tier 3: Engineering Guides

> Practical engineering perspectives.

- (None specific to this lesson beyond the Anthropic engineering guidance in Tier 1. "Building
  Effective Agents" is itself the primary engineering source for agent reliability patterns.)

---

## Tier 4: Educational Sources

> Tutorials, courses, and explanatory content useful for learning.

- (None specific to this lesson. The ReAct paper and the Anthropic agent guidance are the primary
  teaching sources; Project 06 is the conceptual prerequisite for the loop itself.)

---

## Optional — Going Deeper

> Read **after** the reliable loop works. Your agent runs a single linear ReAct trajectory and stops;
> these four are the principled versions of the extensions a learner reaches for next — self-improvement
> and alternative control architectures. Treat them as *design options*, not requirements, and keep
> "use the simplest thing that works" as the default.

- **Reflexion** — `sources/papers/reflexion.md` *(optional — depth)*
  - URL: https://arxiv.org/abs/2303.11366
  - Why it matters: verbal self-feedback stored across attempts — the agent writes a lesson from a failed run and conditions the next on it, no weight updates. The principled version of "retry, but smarter."
  - Where you'll see this: agents that learn within a session from their own failed runs (self-correcting coding/task agents).

- **Self-Refine** — `sources/papers/self-refine.md` *(optional — depth)*
  - URL: https://arxiv.org/abs/2303.17651
  - Why it matters: generate → self-critique → revise *within* a single run — the evaluator-optimizer pattern applied to one answer (and the bridge from Project 07's judge).
  - Where you'll see this: pipelines that loop "draft → critique → revise" before returning a result.

- **Tree of Thoughts** — `sources/papers/tree-of-thoughts.md` *(optional — depth)*
  - URL: https://arxiv.org/abs/2305.10601
  - Why it matters: search and backtracking over multiple reasoning paths instead of one linear trajectory — what to reach for when a single ReAct chain gets stuck.
  - Where you'll see this: planning/search agents on problems where one greedy path is brittle (puzzles, multi-constraint tasks).

- **ReWOO** — `sources/papers/rewoo.md` *(optional — depth)*
  - URL: https://arxiv.org/abs/2305.18323
  - Why it matters: plan-execute — plan all tool calls up front, then execute, decoupling reasoning from observation. The architectural contrast to ReAct's per-step interleaving: fewer model calls, different failure modes.
  - Where you'll see this: efficiency-oriented agent frameworks that batch planning to cut token cost and latency.

---

## Recommended Reading Order

For a learner new to this topic:

1. Start with: `sources/articles/building-effective-agents.md` — workflows vs. agents and *when not to* build one. Read this before writing any code.
2. Then re-read: `sources/papers/react-paper.md` — focus on the exception-handling and termination claims (the basis for recovery and a clean stop).
3. Reference: `sources/official-docs/anthropic-tool-use.md` — the loop and why it must be bounded (carried from Project 06).
4. Reference: `sources/papers/mt-bench.md` — evaluating with numbers, applied to runs.
5. For the cost budget: `sources/official-docs/anthropic-pricing.md` — real per-MTok prices.

---

## Further Reading

Topics adjacent to this lesson worth exploring later:

- Orchestrator-workers and evaluator-optimizer agents — composing multiple agents (Building Effective Agents; bridge to Project 09).
- Reflection and self-critique loops (Generative Agents; the optional extension here).
- Observability for agents: full run traces, structured logs, and replay for debugging autonomous runs.
- Sandboxing and permissioning real *acting* tools (shell, network, write access) — the security surface beyond P06's read-only file tools.
- Cost/latency budgeting and wall-clock limits in production agent runtimes.
