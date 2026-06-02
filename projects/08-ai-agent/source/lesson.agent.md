# Lesson 08: AI Agent
<!-- lesson.agent.md — Agent-optimized canonical source. Do not simplify; this is the truth layer. -->

## Metadata

| Field | Value |
|-------|-------|
| Project | 08-ai-agent |
| Core Concepts | the agent vs. workflow distinction, multi-step autonomy, loop/stuck detection, budget enforcement (steps + tokens + cost), tool-error recovery, agent evaluation (task completion, efficiency, cost), "use the simplest thing that works" |
| Prerequisites | See PROJECT.md (Project 06: tool use + the agentic loop — this project assumes it and *provides* it) |
| Difficulty | Intermediate |
| Estimated Time | See PROJECT.md (12–16 hours total) |
| Last Updated | 2026-06-02 |

---

## Learning Objectives

By completing this lesson, the learner will be able to:

1. State the **workflow vs. agent** distinction — a workflow runs through "predefined code paths," an agent "dynamically direct[s] [its] own processes and tool usage" — and decide which a given task needs (source: `sources/articles/building-effective-agents.md`).
2. Explain why an autonomous, multi-step loop is **fundamentally riskier** than P06's single-question copilot: the model now controls *how many* steps, *which* tools, and *when to stop* — so cost, correctness, and termination are all the model's to get wrong (source: `sources/articles/building-effective-agents.md`, `sources/papers/react-paper.md`).
3. Implement **loop/stuck detection** — recognize when the agent is repeating the same action with no progress — and explain why a `max_steps` cap alone does not catch an agent that *oscillates* productively-looking-but-uselessly (source: `sources/papers/react-paper.md`).
4. Implement a **budget** over steps **and** tokens (and, optionally, cost), and explain why an autonomous agent without a budget is a runaway-cost incident waiting to happen (source: `sources/official-docs/anthropic-tool-use.md`, `sources/official-docs/anthropic-pricing.md`).
5. Implement **tool-error recovery** — catch a failing tool, feed the error back as an *observation*, and let the model adapt — and explain why crashing the loop on one bad tool call wastes every step that came before it (source: `sources/papers/react-paper.md`).
6. **Evaluate an agent run** quantitatively — task completion, step count, tool calls, and efficiency (steps vs. optimal) — instead of eyeballing "it seemed to work" (source: `sources/papers/mt-bench.md`).
7. Apply the discipline **"add complexity only when it demonstrably improves outcomes"** — name concrete tasks where a single LLM call or a fixed workflow beats an agent, and justify *not* reaching for the loop (source: `sources/articles/building-effective-agents.md`).
8. Name the major **failure modes** of an autonomous agent (runaway cost, productive-looking oscillation, a single tool error killing the run, an agent used where a function call would do) and say which design decision prevents each.

---

## Prerequisite Knowledge Check

Before beginning, the learner should be able to answer:

1. From Project 06: what *is* an agent in one sentence, and what are the two halves of the tool-use protocol (the model emits a *call*; you execute it and feed the *result* back)?
2. From Project 06: why must the agentic loop be bounded, and why is `arguments` parsed with `json.loads`? (This project **provides** the P06 tool layer — `safe_resolve`, `parse_tool_calls`, `dispatch_tool`, the file tools — so you must already understand it.)
3. From Project 01: how is token cost computed from usage (per-MTok pricing × tokens)? Project 08's budget is this, enforced live.

If the learner cannot build P06's basic tool loop from scratch, do that first. Project 08 is **P06's loop made reliable and autonomous** — it assumes the loop and spends the learner's effort on everything that keeps a *multi-step* loop from going wrong.

---

## Core Concepts

| Concept | Definition | Why It Matters |
|---------|-----------|----------------|
| Workflow vs. agent | Workflow = LLM steps on "predefined code paths"; agent = the LLM "dynamically direct[s] [its] own processes and tool usage" | The first design decision: an agent is more capable *and* more failure-prone; pick the simpler one when it suffices (source: `sources/articles/building-effective-agents.md`) |
| Multi-step autonomy | The model decides how many steps to take, which tools to call, and when it's done | Every one of those decisions is a thing it can get wrong — the source of all the failure modes below (source: `sources/articles/building-effective-agents.md`) |
| Loop / stuck detection | Detecting that the agent is repeating the same action with no new information | A `max_steps` cap stops a runaway *eventually*; stuck detection stops a no-progress agent *immediately*, before it wastes the budget (source: `sources/papers/react-paper.md`) |
| Budget (steps + tokens + cost) | A hard ceiling on resources, checked every step, that ends the run when crossed | The model controls the loop, so an unbounded autonomous agent is an open-ended bill; the budget is the seatbelt (source: `sources/official-docs/anthropic-tool-use.md`) |
| Tool-error recovery | Catch a raising/failing tool, feed the error back as an observation, let the model try another approach | One bad tool call shouldn't discard every step before it; ReAct's "reasoning… help[s]… handle exceptions" (source: `sources/papers/react-paper.md`) |
| Agent evaluation | Scoring a *run*: did it complete the task, in how many steps/tool-calls, how efficiently, at what cost | "It worked once in the demo" is not evaluation; you need numbers to know if a change made the agent better or worse (source: `sources/papers/mt-bench.md`) |
| "Simplest thing that works" | Add agentic complexity *only* when it demonstrably beats a single call or a fixed workflow | The most valuable agent skill is knowing when **not** to build one (source: `sources/articles/building-effective-agents.md`) |

### Concept Relationships

```
                       ┌─────────────────── BUDGET (steps + tokens) ── checked every step
                       │                              │
   task ──► run_agent LOOP  (P06's loop, now made reliable):                
        │   │  call model ──► parse calls (provided, P06)                    
        │   │     │                                                          
        │   │     ├─ no calls ──────────────────────────► RETURN (answered)  
        │   │     └─ tool calls ─► dispatch (provided) ── try/except ─►       
        │   │            │            RECOVERY: on error, feed the error      
        │   │            │            string back as the observation         
        │   │            ▼                                                    
        │   │     record action in history                                   
        │   │            │                                                    
        │   │     ├─ detect_stuck(history)? ─────────────► RETURN (stuck)     
        │   │     └─ budget.over_budget()?  ─────────────► RETURN (budget)    
        │   └──── loop (structurally bounded by max_steps) ─► RETURN (max_steps)
        ▼
   evaluate_run(result, expected) ─► {completed, steps, tool_calls, efficiency, stop_reason}
```

Critical framing: **Project 06 gave the model eyes and a loop. Project 08 makes that loop safe to leave running.** The new work is not the loop — it's the four guards around it (stuck detection, budget, error recovery, evaluation) and the judgment to not deploy a loop where a single call would do. An agent is the highest-capability *and* highest-blast-radius pattern in this course; this lesson is about earning the right to use it.

---

## Section 1: Motivation

### Why This Exists
Project 06's copilot answers one question: it reads a few files and replies. But "refactor this module and make the tests pass," "research this topic across these sources and write a summary," or "triage this bug" are not one question — they are *open-ended* tasks where you "can't predict the required number of steps" (source: `sources/articles/building-effective-agents.md`). That is exactly the case an **agent** is for: the model plans, acts, observes, and decides *for itself* when it's done. But the moment you hand the model control over the loop, you hand it control over your bill, your correctness, and whether the program ever terminates. The single hardest thing in AI engineering is not making an agent that works on the happy path — it's making one that *fails safely* on every other path. That is what this project teaches.

### The Problem We're Solving
A bare autonomous loop has three ways to ruin your day that the happy-path demo never shows: (1) it gets **stuck** — calling the same tool with the same arguments forever because it can't make progress; (2) it **runs away** — taking 80 steps and $4 of tokens on a task that needed 4 steps; (3) it **dies on one bad tool call** — a single tool raises an exception and the whole multi-step run, and every token spent on it, is lost. A reliable agent detects the stuck state, enforces a budget, and recovers from tool errors. And the fourth problem is the meta one: engineers reach for an agent when a single function call would have been faster, cheaper, and more reliable. "The most successful implementations use simple, composable patterns" (source: `sources/articles/building-effective-agents.md`).

### Real-World Stakes
This is the product category everyone is racing to ship: autonomous coding agents, research agents, computer-use agents, customer-ops agents. The PROJECT.md framing is exact: "users forgive bad suggestions, but not autonomous actions that cause damage." A copilot that suggests a wrong line costs you nothing; an agent that loops 200 times overnight costs you real money, and an agent that takes a destructive action without a budget or a guard is an incident. Every production agent has the machinery you build here — step/token budgets, loop detection, retries with recovery, and an evaluation harness — because without it, the agent is a liability, not a feature.

### Would Users Pay For This?
"Autonomous agents are the highest-value AI product category. A coding agent that saves 2 hours per day at $100/hour is worth $500/month to a developer" (PROJECT.md). But the value is gated entirely on **reliability**: an agent that occasionally burns $20 and produces nothing destroys the trust that the $500/month depends on. The reliability layer in this project — budgets, stuck detection, recovery, evaluation — is not polish on top of the product; it *is* the product. The model is a commodity; the discipline around the loop is the moat.

---

## Section 2: Mental Model

### ELI12 (Explain Like I'm 12)
In Project 06 you gave a friend who can't see your computer some buttons to press ("show me a file," "search"), and they pressed buttons until they could answer one question. That was great for *one question*. Now imagine you give that friend a *whole chore* — "clean up my messy folder" — and you leave the room. Three bad things can happen. One: they get **stuck**, opening the same drawer over and over because they don't know what to do, forever. Two: they **never stop** — they keep working for ten hours and you get a giant bill for their time. Three: one drawer is **jammed**, and instead of skipping it they just give up on the whole chore. A *good* helper notices "I keep opening this same drawer — that's not working, let me stop," has a rule like "you get 20 minutes and that's it," and when a drawer jams says "okay, skip it, I'll do the rest." This project is teaching your friend those three habits — and teaching *you* the wisdom to not send a friend to do a chore that you could have done yourself in one move.

### ELI-Engineer (Explain to a Software Engineer)
- An **agent** is P06's loop — `call model → dispatch requested tools → feed results back → repeat` — but for *open-ended* tasks where the number of steps is unknown. The loop, tools, parsing, and sandbox are **provided** (you built them in P06). The learning target is the control layer.
- **Stuck detection** (`detect_stuck(history)`): keep a history of `(tool, arguments)` actions; if the last *N* are identical, the agent is making no progress — stop now, don't wait for `max_steps`. A `max_steps` cap bounds the worst case; stuck detection catches the common case early.
- **Budget** (`BudgetTracker`): a hard ceiling on **steps** and **tokens** (cost = tokens × per-MTok rate), `tick()`'d each step and checked with `over_budget()`. The model controls the loop, so the budget is what makes "autonomous" not mean "unbounded."
- **Recovery**: dispatch each tool inside `try/except`; on failure, feed `f"Error: {e}"` back as the tool's observation instead of letting the exception kill the run. ReAct: "reasoning traces help the model … handle exceptions" — the model reads the error and adapts (source: `sources/papers/react-paper.md`).
- **Evaluation** (`evaluate_run`): a run produces a `RunResult` (answer, action history, steps, tokens, `stop_reason`). Score it: did it complete (`stop_reason == "answered"` and the answer contains what was expected)? How many steps vs. optimal (efficiency)? How many tool calls? At what token cost?
- **Judgment**: before any of this, ask whether the task needs an agent at all. "Find the user's email" is a function call. "Summarize this PDF" is one retrieval-augmented call (P04). The loop is for tasks whose step count you genuinely cannot predict.

### Real-World Analogy
An agent is a **self-driving delivery vehicle**, where P06's copilot was **cruise control**. Cruise control does one bounded thing on demand and hands back control. A self-driving vehicle is given a *destination* and makes its own decisions the whole way — which is enormously more useful and enormously more dangerous. So you don't ship it without: a **fuel gauge that forces a stop** (the budget), a **"you've been circling this block 5 times, pull over" detector** (stuck detection), **the sense to route around a closed road instead of parking forever** (error recovery), and a **trip log you can audit afterward** (evaluation). And the wisest dispatcher of all knows that to move a box across the room, you don't summon the self-driving vehicle — you carry it (the single call).

### Intuition Diagram
```
 TASK: "What model does this repo default to, and where is it set?"  (multi-step)
   │
   ▼  run_agent(budget = steps≤10, tokens≤20k)
   step 1: model ─► search_code("default_model")     ── budget.tick ── history=[search]
   step 2: model ─► read_file("config.py")            ── budget.tick ── history=[search, read]
           (tool raises? → caught → "Error: ..." fed back → model adapts)   ← RECOVERY
   step 3: model ─► (no tool call) "Defaults to groq/llama-3.3-70b; config.py:24." ─► RETURN answered

 vs. a BROKEN run on a confusing task:
   step 1..3: model ─► search_code("x"), search_code("x"), search_code("x")  ← detect_stuck → STOP (stuck)
   ... or 50 productive-looking steps with no end ─► budget.over_budget() → STOP (budget)

 evaluate_run(result, expected={answer_contains:"groq", optimal_steps:3})
   ─► {completed: True, steps: 3, tool_calls: 2, efficiency: 1.0, stop_reason: "answered"}
```

---

## Section 3: Technical Explanation

### Formal Definition
- A **workflow** is a system where "LLMs and tools are orchestrated through predefined code paths." An **agent** is a system where "LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks" (source: `sources/articles/building-effective-agents.md`). Project 08 builds the latter.
- An **agent run** is a sequence of steps; each step is one model call that either yields a final answer or one-or-more tool calls. The run has a **stop reason** ∈ {`answered`, `stuck`, `budget`, `max_steps`}.
- A run is **stuck** when the last *N* actions are identical `(tool, arguments)` — the agent is recycling state with no new observation.
- A run is **over budget** when its cumulative steps or tokens cross a pre-set ceiling. Cost is `tokens × price_per_token`; pricing comes from the provider's official page, not invented (source: `sources/official-docs/anthropic-pricing.md`).
- **Recovery**: a tool that raises is converted into an error observation `f"Error: {e}"` fed back into the conversation, so the loop continues and the model can react (the ReAct exception-handling property — source: `sources/papers/react-paper.md`).

### How It Works (Mechanically)

**Decide if you even need a loop.** If the task has a known, fixed shape — one lookup, one summary, a classify-then-route — use a single call or a workflow. Reach for the agent only when "it's difficult or impossible to predict the required number of steps" (source: `sources/articles/building-effective-agents.md`).

**Set a budget.** Construct a `BudgetTracker(max_steps, max_tokens)` before the run. This is the contract: the agent may spend up to this and no more.

**Run the loop (provided base + your guards).** Each iteration: call the model (`complete`), `tick` the budget with the step's token usage, `parse_tool_calls` (provided). If there are no calls, the model answered — return a `RunResult(stop_reason="answered")`. Otherwise append the assistant turn, then for each call: record the `(tool, arguments)` action, `dispatch_tool` it **inside try/except** (recovery), and append the result (or error string) as a `tool` message.

**Guard after each step.** Call `detect_stuck(history)` — if true, return `stop_reason="stuck"`. Call `budget.over_budget()` — if it returns a reason, return `stop_reason="budget"`. If the loop exhausts its structural `max_steps` bound, return `stop_reason="max_steps"`.

**Evaluate the run.** Pass the `RunResult` and an `expected` spec to `evaluate_run`: `completed` (answered + expected substring present), `steps`, `tool_calls`, `efficiency` (`optimal_steps / steps`, capped at 1.0). Now a prompt or model change can be scored, not guessed at — this is Project 07's discipline applied to a *run* instead of a single answer.

### The Math (When Necessary)
There is almost no math here — like P06, this is a control-flow lesson. Two small formulas matter:
- **Cost:** `cost_usd = (tokens / 1_000_000) × price_per_mtok`. Do not invent `price_per_mtok`; read it from the provider's pricing page or leave cost disabled (source: `sources/official-docs/anthropic-pricing.md`).
- **Efficiency:** `efficiency = min(1.0, optimal_steps / max(steps, 1))`. `1.0` means the agent solved it in the optimal number of steps; `0.5` means it took twice as long as it should have. It is a *unitless ratio*, deliberately simple — the point is to make "the agent wandered" a number you can track across runs.

### Implementation Details
- **`max_steps` is a backstop, not the primary guard.** It bounds the absolute worst case. The *primary* guards are `detect_stuck` (catches no-progress immediately) and the token budget (catches expensive-but-progressing runs). An agent that hits `max_steps` every time is an agent you haven't tuned.
- **Stuck ≠ slow.** An agent taking many *different* productive steps is not stuck — it may just be a hard task. `detect_stuck` must compare *identical* actions; comparing only the tool *name* would wrongly flag an agent that reads ten different files.
- **Recovery means feeding the error back, not swallowing it.** A bare `try/except: pass` is *worse* than crashing — the model never learns the tool failed and may repeat it (→ stuck). The error must become an *observation* the model reads.
- **Append the assistant turn before tool results** — same provider rule as P06 (an orphan tool result is rejected). Carried, still mandatory.
- **`complete` is injected.** `run_agent` takes the model-call function as a parameter so the whole loop is testable offline with a scripted model — no network, no key. The real app passes a LiteLLM-backed `complete`.
- **Token accounting offline.** Real providers return `usage`; offline you estimate from message length. The budget logic is identical — only the token source differs.
- **The stop reason is the most important field in the result.** "Answered" vs. "stuck" vs. "budget" vs. "max_steps" is the difference between success and four distinct failures. Evaluation keys off it; never collapse them into a bare bool.

---

## Section 4: Guided Examples

> The lab stack: `litellm` (chat + tools via `config.py`), the **provided** P06 tool layer (`safe_resolve`, `parse_tool_calls`, `dispatch_tool`, file tools), and a pure-Python loop. Examples below mirror the guiding tests.

### Example 1: Simple Case — detect a stuck agent (`detect_stuck`)
```python
from safety import Action, detect_stuck

# An agent making progress: three DIFFERENT actions → not stuck.
progress = [Action("search_code", {"query": "x"}),
            Action("read_file", {"path": "a.py"}),
            Action("read_file", {"path": "b.py"})]
detect_stuck(progress, window=3)   # -> False

# An agent spinning: the last three actions are IDENTICAL → stuck.
spinning = [Action("read_file", {"path": "a.py"}),
            Action("search_code", {"query": "foo"}),
            Action("search_code", {"query": "foo"}),
            Action("search_code", {"query": "foo"})]
detect_stuck(spinning, window=3)   # -> True
```
**What to observe:** stuck detection compares *whole actions* (tool **and** arguments), not just the tool name — an agent reading ten different files is working, not stuck. This catches the no-progress case immediately, long before a `max_steps` cap would.

### Example 2: Real-World Case — enforce a budget (`BudgetTracker`)
```python
from safety import BudgetTracker

b = BudgetTracker(max_steps=5, max_tokens=10_000)
b.tick(2_000)          # step 1
b.tick(2_000)          # step 2
b.over_budget()        # -> None        (2 steps, 4k tokens — within budget)

b.tick(7_000)          # step 3, now 11k tokens
b.over_budget()        # -> "token budget exhausted (11000/10000)"   (a reason string — truthy)
```
**What to observe:** the budget is checked, not assumed. `over_budget()` returns `None` while there's room and a *reason string* once a ceiling is crossed — the loop uses that truthiness to stop and records *why*. An autonomous loop without this is an open-ended invoice.

### Example 3: Edge Case — one tool error must not kill the run (recovery in `run_agent`)
```python
from types import SimpleNamespace
from safety import BudgetTracker
from agent import run_agent
import agent

# Force the (provided) dispatch to RAISE on the first call, as a flaky real tool would:
calls = {"n": 0}
def exploding_dispatch(name, args, repo_root):
    calls["n"] += 1
    if calls["n"] == 1:
        raise RuntimeError("network down")
    return "ok"
agent.dispatch_tool = exploding_dispatch   # monkeypatch for the demo

turns = iter([
    SimpleNamespace(content=None, tool_calls=[_tc("c1", "read_file", '{"path": "a.py"}')]),  # raises
    SimpleNamespace(content="Recovered and answered.", tool_calls=None),                      # adapts
])
result = run_agent([{"role": "user", "content": "go"}], ".", lambda m, t: next(turns),
                   BudgetTracker(max_steps=5, max_tokens=10_000))
print(result.stop_reason)   # 'answered'  — the raise became an observation, the model adapted
print(result.answer)        # 'Recovered and answered.'
```
**What to observe:** the tool raised, but `run_agent` caught it, fed `"Error: network down"` back as the observation, and the model recovered on the next step. Without the `try/except`, that single exception would have discarded the whole run. This is the failure you reproduce in M6 by *removing* the recovery.

---

## Section 5: Reflection Before Building

> The learner should fill UNDERSTANDING.md before proceeding to implementation.

**Questions to answer in UNDERSTANDING.md:**

1. In your own words, what is the difference between a *workflow* and an *agent*, and what specifically does an agent gain control of that makes it both more powerful and more dangerous?
2. Project 06 already bounded its loop with `max_steps`. So why isn't `max_steps` enough for Project 08 — what failure does `detect_stuck` catch that a step cap doesn't, and what failure does a *token* budget catch that a step cap doesn't?
3. Walk the recovery path: a tool raises an exception mid-run. What are the exact steps `run_agent` takes so the run survives, and why is `try/except: pass` *worse* than letting it crash?
4. Predict the three failure modes of removing, respectively: (a) the budget, (b) `detect_stuck`, (c) tool-error recovery. Which design decision prevents each?
5. Give one concrete task you would solve with a single LLM call (no agent), one with a fixed workflow, and one that genuinely needs the agent loop. Justify each — why is the loop *overkill* for the first two?
6. `evaluate_run` reports `efficiency = optimal_steps / steps`. Why is a bare "did it answer?" boolean insufficient for deciding whether a prompt change made your agent better or worse?
7. The one thing you still don't fully understand about making an autonomous loop safe.

---

## Section 6: Project Assignment

See PROJECT.md and source/project.md for the full specification.

### Core Requirement
Build the **reliability layer** that turns P06's tool loop into a trustworthy autonomous agent, in `code/`:
- **`safety.py`** — `detect_stuck` (M1) and `BudgetTracker` (M2) are the *learner core*: the no-progress detector and the step/token ceiling. The `Action` record and the dataclass fields are *provided*.
- **`agent.py`** — `run_agent` (M3) is the *learner core* — the generalized loop with **tool-error recovery** and the stuck/budget guards wired in. `RunResult`, `parse_tool_calls`, and the token estimator are *provided* (carried from P06).
- **`evaluate.py`** — `evaluate_run` (M4) is the *learner core*: score a run on completion, steps, tool calls, and efficiency.
- **`tools.py`** — the entire P06 tool layer (`safe_resolve`, `read_file`, `list_directory`, `search_code`, `dispatch_tool`, `TOOL_SCHEMAS`). *(Provided — you built this in Project 06.)*
- **`agent_app.py`** — the orchestrator: build a real LiteLLM `complete`, set a budget, run the agent on a multi-step task against a repo, print the ReAct trace + final answer + the `evaluate_run` summary. *(Provided.)*

### Extended Requirements
- **Explicit planning:** add a `plan_task` step that asks the model to decompose the task into sub-steps first, then execute — and measure whether planning reduces steps-to-answer (source: `sources/articles/building-effective-agents.md`).
- **Reflection loop:** after the agent answers, add a self-check step ("does this actually satisfy the task? if not, continue") — the evaluator-optimizer pattern (source: `sources/articles/building-effective-agents.md`; reflection: `sources/papers/generative-agents.md`).
- **Structured final output:** force a final `emit_answer(answer, steps_taken, confidence)` tool so the result is schema-validated, not free text (source: `sources/official-docs/anthropic-tool-use.md`).
- **Cost budget:** extend `BudgetTracker` with a real `max_usd` ceiling using your provider's official per-MTok price (source: `sources/official-docs/anthropic-pricing.md`).
- **Retry with backoff:** on a *transient* tool error, retry the same call once before feeding the error back.

### Start Building

**Open [`code/README.md`](../code/README.md)** for setup, the milestone build order, and the file roles (which files are *provided* vs. *learner-owned*). Run `python -m pytest` to see the failing guiding tests, then implement the learner-owned functions in milestone order until they pass.

---

## Section 7: Project Milestones

| Milestone | What You Build | Validation |
|-----------|---------------|------------|
| M1: Stuck detection | `safety.detect_stuck(history, window)` — True iff the last `window` actions are identical | three different actions → False; three identical → True (offline test) |
| M2: Budget | `safety.BudgetTracker.tick()` + `.over_budget()` — count steps/tokens, return a reason when a ceiling is crossed | within budget → `None`; over steps or tokens → a reason string (offline test) |
| M3: Reliable loop | `agent.run_agent(messages, repo_root, complete, budget)` — call→dispatch(**recover**)→feed back→guard→repeat | scripted `complete`: tool-then-answer → `answered`; a raising dispatch → still `answered` (recovered); an always-same-call model → `stuck`; an always-tool model → `budget`/`max_steps` (offline tests) |
| M4: Evaluate a run | `evaluate.evaluate_run(result, expected)` — completion, steps, tool calls, efficiency | an answered run with the expected substring → `completed=True`, `efficiency≤1.0`; a stuck run → `completed=False` (offline test) |
| M5: Agent end-to-end | `agent_app.py` runs the agent on a real multi-step task against a repo | give it a task; it acts over several steps, answers, and prints the trace + the eval summary |
| M6: Break / Evaluate | Remove the budget, remove `detect_stuck`, remove recovery, **and** run the agent on a task a single call would solve | runaway cost / infinite oscillation / one error kills the run / agent is slower-and-costlier-for-nothing — each recorded in FAILURE_ANALYSIS.md |

---

## Section 8: Self-Evaluation

| Criterion | Does your implementation... | Pass? |
|-----------|---------------------------|-------|
| Stuck detection | flag *identical* repeated actions (tool **and** args), and **not** flag many different productive steps? | |
| Budget enforced | check a steps **and** tokens ceiling every step, and return *why* it stopped? | |
| Recovery | catch a raising tool, feed the error back as an observation, and keep looping (not crash, not swallow)? | |
| Distinct stop reasons | return `answered` / `stuck` / `budget` / `max_steps` — never collapse a failure into "done"? | |
| Message order | append the assistant turn *before* the tool results (carried from P06)? | |
| Evaluation is quantitative | report completion, steps, tool calls, and efficiency — numbers, not "it seemed to work"? | |
| Right tool for the job | can you name a task where you deliberately did **not** use the agent loop, and why? | |

**Red flags (your implementation may have problems if):**
- Your loop has no budget and relies on `max_steps` alone — one expensive step pattern blows your bill.
- `detect_stuck` compares only the tool name, so a productive multi-file read gets killed as "stuck."
- A single tool exception ends the whole run (no recovery), or you `except: pass` and the model spins.
- Your run returns a bare `True/False` — you can't tell a stuck run from a budget stop from a real answer.
- You used the agent loop for a task that was one lookup or one summary, and it's slower and costlier with no benefit.

---

## Section 9: Common Mistakes

| Mistake | Why It Happens | Consequence | Fix |
|---------|---------------|-------------|-----|
| No budget, only `max_steps` | "P06 capped steps and that was fine" | An agent taking few but huge steps blows the token bill | Track tokens *and* steps; check `over_budget()` every step (source: `sources/official-docs/anthropic-tool-use.md`) |
| `detect_stuck` compares tool name only | "Same tool = stuck" | Kills a productive agent reading many different files | Compare the whole action — tool **and** arguments |
| `try/except: pass` on tool errors | "Swallow the error so it doesn't crash" | Model never sees the failure, repeats it → stuck | Feed `f"Error: {e}"` back as the observation (source: `sources/papers/react-paper.md`) |
| One tool raise kills the run | No `try/except` around dispatch | Every prior step's tokens are wasted on one bad call | Wrap dispatch; convert the exception into an observation |
| Collapsing stop reasons to a bool | "Did it finish? yes/no" | Can't distinguish answered from stuck from budget | Return an explicit `stop_reason`; evaluate keys off it |
| Using an agent where a call would do | "Agents are the cool pattern" | Slower, costlier, less reliable than one call | "Add complexity only when it demonstrably improves outcomes" (source: `sources/articles/building-effective-agents.md`) |
| Evaluating by eyeballing one demo | "It worked when I ran it" | A prompt change silently regresses the agent | `evaluate_run` over a fixed task set — numbers, per run (source: `sources/papers/mt-bench.md`) |
| Inventing a token price for the cost budget | "Roughly a few dollars per million?" | Wrong cost numbers, wrong budget decisions | Use the provider's official per-MTok price or disable cost (source: `sources/official-docs/anthropic-pricing.md`) |

---

## Section 10: Connections

### How This Connects to Previous Projects
This is **Project 06's loop, made reliable.** The tool layer (sandbox, schemas, dispatch), the parsing, and the basic call→dispatch→feed-back cycle are all carried over *provided* — which is the whole point: you already learned them, so here you spend your effort on the control layer instead. The **budget** is Project 01's token-cost arithmetic, enforced live. The **evaluation** is Project 07's discipline (score, don't eyeball) applied to a *run* rather than a single answer. The optional **reflection** loop is Project 05's reflection (synthesize a higher-level judgment from raw steps — source: `sources/papers/generative-agents.md`). The agent is where the whole course converges.

### How This Connects to Future Projects
**Project 09 (Personal Learning OS)** orchestrates memory (P05), retrieval (P03/P04), this agent (P08), and evaluation (P07) into one system. The reliability layer you build here is what makes it safe for P09 to let an agent act over a user's personal data: a bounded, stuck-aware, recoverable agent with an auditable run log. Everything P09 routes *to* an agent inherits the guards from this project.

### How This Connects to StarcallOS
StarcallOS doing anything *autonomous on the user's behalf* — multi-step research, organizing files, executing a chore across several tools — is this loop. The reliability layer is the difference between a feature and an incident: a **budget** so StarcallOS never burns the user's money on a confused agent; **stuck detection** so it bails out of a no-progress spiral instead of grinding; **recovery** so one flaky integration doesn't abort a long task; **evaluation** so a change to StarcallOS's agent can be measured, not hoped at; and the **judgment** to route a simple request to a single call instead of spinning up a loop. P08 is the smallest complete instance of "StarcallOS can be trusted to act."

### Production Patterns
Real agents are this loop plus production engineering: hard budgets on steps/tokens/cost/wall-clock; loop and stuck detection; retries with backoff and graceful tool-error recovery; structured, validated final output; a full run trace for observability; and an evaluation harness gating every change (sources: `sources/articles/building-effective-agents.md`, `sources/official-docs/anthropic-tool-use.md`). Anthropic's own guidance is to bias toward the *simplest* pattern that works — single call, then workflow, then agent — and to "invest in the agent-computer interface." The named patterns (prompt chaining, routing, orchestrator-workers, evaluator-optimizer) are the composable pieces; the autonomous loop you build here is the most general and the one to reach for last (source: `sources/articles/building-effective-agents.md`).

---

## Assessment Rubric

See source/rubric.md for the complete grading rubric.

**Summary criteria:**
- [ ] Implementation runs correctly (loop: call → dispatch with recovery → feed back → guard → repeat; returns a `RunResult` with a distinct `stop_reason`)
- [ ] `detect_stuck` flags identical repeated actions and not productive different ones; `BudgetTracker` enforces steps **and** tokens
- [ ] Tool errors are recovered (fed back as observations), not swallowed and not fatal
- [ ] Understanding document completed in learner's own words
- [ ] Failure analysis demonstrates intentional experimentation (remove budget / stuck detection / recovery, **and** the agent-where-a-call-would-do ablation)
- [ ] Evaluation is quantitative (completion, steps, tool calls, efficiency, cost), not impressionistic
- [ ] StarcallOS reflection identifies at least one concrete applicable pattern

---

## Sources

See source/resources.md for the full annotated source list.

**Required reading:**
- `sources/articles/building-effective-agents.md` — workflows vs. agents, "the most successful implementations use simple, composable patterns," "add complexity only when it demonstrably improves outcomes," and the named patterns (orchestrator-workers, evaluator-optimizer). The source for *when* and *whether* to build an agent.
- `sources/papers/react-paper.md` — the reasoning↔acting loop; "reasoning traces help the model … handle exceptions" (the basis for recovery), and why a reasoning step makes the loop terminate instead of thrashing.
- `sources/official-docs/anthropic-tool-use.md` — the tool-use protocol and the agentic loop; `tool_choice`; why the loop must be bounded (carried from P06, here generalized to a budget).

**Recommended reading:**
- `sources/papers/mt-bench.md` — evaluating with numbers (applied here to *runs*: completion + efficiency, not a single answer).
- `sources/papers/generative-agents.md` — reflection (synthesizing a higher-level judgment from raw steps) for the optional reflection loop.
- `sources/official-docs/anthropic-pricing.md` — per-MTok pricing for a real cost budget (don't invent prices).
- `sources/official-docs/litellm-completion.md` — the `tools` / `tool_calls` shape and `usage` for live token accounting (carried from P06).

**Optional — going deeper (after the reliable loop works):**
> Your agent runs a single linear ReAct trajectory and stops. These four papers are the principled versions of the extensions a learner reaches for next — self-improvement and alternative control architectures. Read them as *design options*, and keep "use the simplest thing that works" as the default.
- `sources/papers/reflexion.md` *(optional — depth)* — verbal self-feedback stored across attempts: the agent writes a lesson from a failed run and conditions the next one on it. The principled version of "retry, but smarter."
- `sources/papers/self-refine.md` *(optional — depth)* — generate → self-critique → revise *within* a run (no extra training). The evaluator-optimizer pattern applied to a single answer.
- `sources/papers/tree-of-thoughts.md` *(optional — depth)* — search and backtracking over multiple reasoning paths instead of one linear trajectory. When a single ReAct chain gets stuck, ToT explores alternatives.
- `sources/papers/rewoo.md` *(optional — depth)* — plan-execute: decouple reasoning from observation by planning all tool calls up front, then executing. The architectural contrast to ReAct's per-step interleaving — fewer model calls, different failure modes.

---

## Instructor Notes

<!-- Hidden context for the mentor reviewing the learner's work. -->

**Common misconceptions:**
- That Project 08 is "Project 06 again." It is not — the loop is *provided*; the entire learning target is the reliability layer (stuck, budget, recovery, evaluation) and the judgment of when to use an agent. A learner who re-implements the tool loop and stops has missed the lesson.
- That `max_steps` is sufficient. It bounds the worst case but misses early no-progress (stuck) and expensive-but-progressing (token) runs.
- That recovery means swallowing errors. `except: pass` is worse than crashing — the model must *see* the error to adapt.
- That more autonomy is always better. The strongest answer in this lesson is often "I would not use an agent here" — and they can say why.
- That "it worked in my demo" is evaluation. One happy-path run is an anecdote; `evaluate_run` over a task set is a measurement.

**Diagnostic questions (reveal genuine vs. surface understanding):**
- "Your agent passed `max_steps` but still cost $5 on a 3-step task. What guard was missing and why didn't `max_steps` catch it?" (token budget; few steps can be huge.)
- "Your `detect_stuck` killed an agent that was correctly reading ten different files. What did it compare, and what should it compare?" (tool name only vs. the whole action.)
- "A tool raised and your run survived — show me the exact lines that made that happen and the one that lets the model *learn* the tool failed." (`try/except` + feeding the error string back.)
- "Give me a task you would NOT solve with this agent, and tell me what you'd use instead." (single call / workflow; the judgment objective.)
- "What does `efficiency = 0.4` tell you that `completed = True` doesn't?" (it answered but wandered — a regression signal a bool hides.)

**Signs of genuine understanding:**
- The learner treats the budget and stuck detection as the *primary* guards and `max_steps` as a backstop — and can articulate the distinct failure each catches.
- They recover from tool errors by feeding observations back and can explain why swallowing is worse than crashing.
- They return and reason about distinct stop reasons, and their evaluation uses numbers per run.
- They can name, unprompted, a task where they'd skip the agent — and defend "use the simplest thing that works."
- They connect every guard back to a concrete production incident it prevents (runaway bill, hung agent, aborted long task).
