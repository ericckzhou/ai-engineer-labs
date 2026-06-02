# Lesson 07: AI Evaluation Framework
<!-- lesson.agent.md — Agent-optimized canonical source. Do not simplify; this is the truth layer. -->

## Metadata

| Field | Value |
|-------|-------|
| Project | 07-ai-evaluation-framework |
| Core Concepts | LLM-as-a-judge, judge biases (position / verbosity / self-enhancement), reasoning-before-score, reference-guided judging, score aggregation (mean + pass-rate), regression testing, eval dataset design |
| Prerequisites | See PROJECT.md (Project 01: chat completions via LiteLLM; Project 04: faithfulness/RAGAS as a worked metric; any prior project as a system to evaluate) |
| Difficulty | Intermediate |
| Estimated Time | See PROJECT.md (8–12 hours total) |
| Last Updated | 2026-06-01 |

---

## Learning Objectives

By completing this lesson, the learner will be able to:

1. Explain why "it seemed to work" is not an evaluation, and why text outputs with **no single right answer** need a different measurement strategy than `assert ==` (source: `sources/papers/mt-bench.md`).
2. Implement **LLM-as-a-judge**: construct a judge prompt that scores an answer on a scale, and justify why a strong LLM judge is usable (~80% agreement with humans — "the same level of agreement between humans") (source: `sources/papers/mt-bench.md`).
3. Name and reproduce the **biases of an LLM judge** — position bias, verbosity bias, self-enhancement bias, weak math/reasoning grading — and say which one a given bad score is caused by (source: `sources/papers/mt-bench.md`).
4. Apply the standard **mitigations**: ask for **reasoning before the score** (chain-of-thought), **reference-guided** judging, and position-swapping for pairwise (source: `sources/papers/mt-bench.md`).
5. **Parse a judge's free-text reply robustly** into a numeric score (JSON, "Score: 4", "4/5"), clamping out-of-range values — the unglamorous step that makes the whole harness work.
6. **Aggregate** per-case scores into a decision: a mean score and a **pass-rate** against a threshold, not a wall of individual numbers.
7. Build a **regression test**: freeze an eval dataset, score a baseline, re-score after a prompt/model change, and flag the cases that **got worse** (source: `sources/papers/mt-bench.md`).
8. Distinguish **reference-free** metrics (faithfulness/relevance — RAGAS) from **reference-based** and **judge-based** scoring, and pick the right one per task (source: `sources/papers/ragas.md`).

---

## Prerequisite Knowledge Check

Before beginning, the learner should be able to answer:

1. From Project 01: how do you send a chat completion through `litellm.completion` and read the reply at `response.choices[0].message.content`? (The judge is one more such call.)
2. From Project 04: what is **faithfulness** (`F = |V|/|S|`), and why is it a *reference-free* way to detect hallucination? (That was your first metric; this project generalizes the idea.)
3. Why can't you evaluate "summarize this article" with `assert output == expected`? What would a "correct" summary even be?

If the learner has not built faithfulness in Project 04, skim `sources/papers/ragas.md` first — it is the worked example this project generalizes.

---

## Core Concepts

| Concept | Definition | Why It Matters |
|---------|-----------|----------------|
| LLM-as-a-judge | Using a strong LLM to score or compare answers in place of a human or a fixed metric | The only scalable way to grade open-ended text; ~80% human agreement (source: `sources/papers/mt-bench.md`) |
| Single-answer grading | The judge assigns a score (e.g. 1–5) to one answer | What this project builds; simpler than pairwise (source: `sources/papers/mt-bench.md`) |
| Position bias | The judge favors an answer by its order, not its quality | A named judge failure; cancel via position-swap (source: `sources/papers/mt-bench.md`) |
| Verbosity bias | The judge prefers longer answers regardless of correctness | A wordier prompt can fake an "improvement"; watch length (source: `sources/papers/mt-bench.md`) |
| Self-enhancement bias | The judge favors its own model family / style | Don't always judge a model with itself (source: `sources/papers/mt-bench.md`) |
| Reasoning-before-score | Make the judge explain, then score (chain-of-thought) | Cheapest, highest-leverage mitigation; also auditable (source: `sources/papers/mt-bench.md`) |
| Reference-guided judging | Give the judge a reference answer/context to grade against | Sharply improves agreement, esp. math (source: `sources/papers/mt-bench.md`) |
| Pass-rate | Fraction of cases scoring ≥ a threshold | Turns a list of scores into a ship/no-ship decision |
| Regression test | Re-score a frozen dataset after a change; flag drops | "Did my prompt change help or hurt?" answered with numbers |
| Reference-free metric | Score without a gold answer (faithfulness, relevance) | Grade when no human reference exists (source: `sources/papers/ragas.md`) |

### Concept Relationships

```
  eval dataset (frozen)         the system under test (a prompt/model)
        │                                │
        └────────────┬───────────────────┘
                     ▼   for each case: produce an answer
              ┌──────────────────────────────────────────────┐
              │  LLM-AS-A-JUDGE                               │
              │  build_judge_prompt(question, answer, ref?)   │  ← reasoning-before-score,
              │      │  (scale 1–5, ask reasoning THEN score) │     reference-guided  (mitigations)
              │      ▼                                        │
              │  model → free text → parse_judge_score → int  │  ← robust parsing (JSON / "4/5")
              └──────────────────────────────────────────────┘
                     │  per-case JudgeResult(case_id, score, reasoning)
        ┌────────────┴───────────────┐
        ▼                            ▼
   summarize → (mean, pass-rate)   compare_runs(baseline, candidate)
   "how good is it?"               "did it get better or worse?" → regressions
```

Critical framing: **the judge is one more LLM call (Project 01) whose job is to output a score instead of an answer — but it is a *biased* grader, so the engineering is in the prompt (reasoning-before-score, reference-guided) and in turning many scores into a decision (pass-rate, regression).** Faithfulness from Project 04 was your first metric; here you generalize to "score anything," and then you make scores actionable.

---

## Section 1: Motivation

### Why This Exists
You changed your system prompt. Is the assistant better or worse? With code you'd run the tests — but there is no `assert summary == expected`, because a good summary, a good answer, a good explanation has no single correct string. "Most AI developers ship based on vibes and demo impressions. Production failures happen because no one built evals" (PROJECT.md). The breakthrough is **LLM-as-a-judge**: a strong model can grade open-ended answers and "match both controlled and crowdsourced human preferences well, achieving over 80% agreement — the same level of agreement between humans" (source: `sources/papers/mt-bench.md`). That makes quality *measurable*, and measurable means improvable.

### The Problem We're Solving
Two problems, really. First, **scoring**: turn "is this answer good?" into a number, at scale, without a human in the loop for every example. Second, **regression**: once you can score, freeze a dataset and detect when a change makes things *worse* — the silent failure that ships when no one was measuring. The catch is that the judge is not a neutral oracle: it has **biases** (position, verbosity, self-enhancement) that will quietly corrupt your numbers if you don't design around them (source: `sources/papers/mt-bench.md`).

### Real-World Stakes
Every serious AI product has an eval harness behind it; the ones that don't ship regressions they can't see. "Evaluation infrastructure is the invisible moat… Braintrust, LangSmith, and others are built on selling evaluation infrastructure" (PROJECT.md). The judgment that separates a pro from an amateur: do you trust a single demo, or do you have a dataset, a judge you've validated, and a pass-rate you watch on every change? And do you know your judge prefers longer answers — so the "improvement" you just shipped isn't just verbosity?

### Would Users Pay For This?
Eval infrastructure is a standalone product category precisely because it is the thing that lets a team ship fast *without* breaking quality. Internally it's the moat; externally it's a business. Either way, the unit of value is: a number you trust, attached to a change, before it reaches users.

---

## Section 2: Mental Model

### ELI12 (Explain Like I'm 12)
Imagine grading 500 essays. There's no answer key — a good essay can be written a thousand ways — so you hire a really sharp teaching assistant to read each one and give it a 1–5. That TA (the **judge**) is fast and mostly agrees with you. But the TA has quirks: they give higher marks to *longer* essays, and to whichever essay they read *first*. So you make two rules: "write down your reasons **before** you give the number," and "if you're comparing two, read them in both orders." Now their grades are trustworthy enough that when you change how you teach, you can re-grade the same 500 essays and see whether scores went **up or down**. That up-or-down check is a regression test; the TA-with-rules is LLM-as-a-judge.

### ELI-Engineer (Explain to a Software Engineer)
- A **judge** is an LLM call whose output is a *score*, not an answer. `build_judge_prompt(question, answer, reference?)` → `litellm.completion` → free text → `parse_judge_score` → an int in `[1, scale]`.
- The judge prompt encodes the mitigations: a fixed **scale** (1–5), **reasoning before the score** (chain-of-thought — improves agreement and is auditable), and the **reference** when you have one (reference-guided) (source: `sources/papers/mt-bench.md`).
- The model returns prose, so you must **parse robustly**: it might emit JSON `{"score": 4}`, "Score: 4", or "I'd give this 4/5." Extract the integer, clamp to range, fail loudly only when truly unparseable.
- A run produces `list[JudgeResult]` (`case_id`, `score`, `reasoning`). **`summarize`** → `(mean, pass_rate@threshold)`. **`compare_runs(baseline, candidate)`** → which `case_id`s dropped beyond a tolerance = **regressions**.
- The judge's biases are real: **verbosity** (longer scores higher), **position** (order matters in pairwise), **self-enhancement** (favors its own family). Your harness must account for them, not pretend they're absent (source: `sources/papers/mt-bench.md`).

### Real-World Analogy
A judge is a **restaurant health inspector with a known soft spot**. They're trained, consistent, and mostly right — you can run a whole city's restaurants past them. But suppose they unconsciously score bigger kitchens higher. If you don't know that, you'll conclude "big kitchens are cleaner" when you've just measured the inspector's bias. The fix isn't to fire the inspector (they're 80% reliable) — it's to standardize the rubric, make them write findings before the grade, and audit for the soft spot. Same with an LLM judge.

### Intuition Diagram
```
 ONE CASE:
   question: "Summarize the refund policy."
   answer:   "<the system-under-test's output>"
   reference?: "<gold summary, if you have one>"
        │
        ▼  build_judge_prompt  (scale 1–5, "reason FIRST, then score", include reference)
   judge LLM ──► "The answer covers X and Y but misses the 30-day window. Score: 3"
        │
        ▼  parse_judge_score  → 3   (robust to JSON / '3/5' / 'Score: 3'; clamp to [1,5])
   JudgeResult(case_id, score=3, reasoning="...misses the 30-day window")

 MANY CASES:
   summarize([...]) → mean=3.8, pass_rate@4 = 0.62
   compare_runs(baseline, candidate, tolerance=0) → regressions=[case_7, case_12]
```

---

## Section 3: Technical Explanation

### Formal Definition
- An **LLM judge** is a function `(question, answer[, reference]) → score ∈ {1..N}` realized by an LLM call. **Single-answer grading** scores one answer; **pairwise** compares two (source: `sources/papers/mt-bench.md`).
- **Agreement** is how often the judge's verdict matches a human's; GPT-4 reaches ">80% agreement, the same level of agreement between humans" (source: `sources/papers/mt-bench.md`).
- **Pass-rate** `= |{c : score(c) ≥ t}| / |C|` for threshold `t`. **Mean score** `= (1/|C|) Σ score(c)`.
- A **regression** (given tolerance `τ`) is a case where `candidate.score < baseline.score − τ`.
- A **reference-free metric** scores without a gold answer; faithfulness `F = |V|/|S|` (supported claims / total claims) is the canonical example (source: `sources/papers/ragas.md`).

### How It Works (Mechanically)

**Design the dataset.** A test case is `(id, question[, reference])`. Good cases are representative, include hard/edge inputs, and are *frozen* — the dataset must not change between baseline and candidate or the comparison is meaningless.

**Build the judge prompt.** A system message defining the judge's role and the scale; a user message with the question, the answer, and the reference if present. Bake in the mitigations: **ask for reasoning, then the score** (source: `sources/papers/mt-bench.md`), and request a parseable format (JSON or "Score: N").

**Call the judge.** One `litellm.completion`, ideally at `temperature=0` for repeatability. The judge model can (and often should) differ from the model under test — avoid self-enhancement bias (source: `sources/papers/mt-bench.md`).

**Parse the score.** The reply is prose. Try JSON; else regex "score: N" or "N/scale"; else first integer in range. **Clamp** to `[1, scale]`. Raise only when there is no number at all — silent `0`s poison your mean.

**Aggregate.** `summarize` → mean + pass-rate. One number you trust beats 200 you scroll past.

**Regression-test.** Score the baseline once and store it. After a change, score the candidate on the *same* dataset and `compare_runs`: per `case_id`, flag drops beyond `τ`. Report regressions, improvements, and the mean delta.

### The Math (When Necessary)
- Pass-rate and mean as above. Regression flag: `Δ = candidate − baseline`; regression iff `Δ < −τ`, improvement iff `Δ > +τ`.
- Faithfulness (carried from Project 04): `F = |V| / |S|` (source: `sources/papers/ragas.md`).
- Note on judge calibration: an LLM's absolute 1–5 scale is **not** well-calibrated across runs/models — which is why **pairwise** is more robust and why you watch *relative* change (regression) more than the absolute mean (source: `sources/papers/mt-bench.md`).

### Implementation Details
- **Reasoning before score.** Put the reasoning field first in the requested output; a score emitted before its justification is a worse score (source: `sources/papers/mt-bench.md`).
- **`temperature=0` for the judge.** You want the same answer to get the same score; sampling noise turns a regression test into a coin flip.
- **Parse defensively.** Models drift in format. Handle JSON and plain text; clamp out-of-range; never silently coerce an unparseable reply to `0`.
- **Freeze the dataset.** Comparing runs over *different* cases measures nothing. Version the dataset.
- **Don't judge a model with itself by default.** Self-enhancement bias inflates scores; use a different (often stronger) judge model (source: `sources/papers/mt-bench.md`).
- **Watch length.** Verbosity bias means a change that only lengthens answers can raise scores. Log answer length next to score (source: `sources/papers/mt-bench.md`).
- **Reference-guided when you can.** If you have a gold answer or retrieved context, give it to the judge — grading against something concrete beats grading from memory, especially for facts/math (source: `sources/papers/mt-bench.md`, `sources/papers/ragas.md`).
- **A judge is not ground truth.** ~80% agreement means ~1 in 5 verdicts may differ from a human. Treat scores as a strong signal, not gospel — spot-check (source: `sources/papers/mt-bench.md`).

---

## Section 4: Guided Examples

> The lab stack: `litellm` (the judge call via `config.py`), pure-Python parsing/aggregation, and a small frozen dataset. See `code/`. Examples below mirror the guiding tests.

### Example 1: Simple Case — parse a judge's reply into a score
```python
from llm_judge import parse_judge_score

parse_judge_score('{"reasoning": "covers it well", "score": 4}', scale=5)  # (4, "covers it well")
parse_judge_score("Reasoning: solid but terse.\nScore: 5", scale=5)        # (5, "Reasoning: solid but terse.")
parse_judge_score("I'd rate this 3/5.", scale=5)                            # (3, "I'd rate this 3/5.")
parse_judge_score("Score: 9", scale=5)                                      # (5, ...)  ← clamped to scale
```
**What to observe:** the judge replies in prose, and the format varies. `parse_judge_score` extracts the integer (JSON or text), **clamps** it into `[1, scale]`, and keeps the reasoning. The harness is only as reliable as this parsing step — a model that says "9/5" must not become a `9` in your mean.

### Example 2: Real-World Case — aggregate scores into a decision
```python
from llm_judge import JudgeResult
from metrics import summarize

results = [
    JudgeResult("c1", 5, "..."), JudgeResult("c2", 4, "..."),
    JudgeResult("c3", 3, "..."), JudgeResult("c4", 2, "..."),
]
s = summarize(results, pass_threshold=4)
print(s.n, s.mean_score, s.pass_rate)   # 4  3.5  0.5   (two of four scored >= 4)
```
**What to observe:** four scores become a **mean** (3.5) and a **pass-rate** (50% at threshold 4). The pass-rate is the ship/no-ship number — "half my answers are good enough" is a decision; a list of four integers is not.

### Example 3: Edge Case — a regression hides inside a flat average
```python
from llm_judge import JudgeResult
from regression_runner import compare_runs

baseline  = [JudgeResult("a", 4, ""), JudgeResult("b", 5, ""), JudgeResult("c", 3, "")]
candidate = [JudgeResult("a", 4, ""), JudgeResult("b", 2, ""), JudgeResult("c", 5, "")]

report = compare_runs(baseline, candidate, tolerance=0)
print(report.regressions)    # ['b']   — dropped 5 → 2
print(report.improvements)   # ['c']   — rose 3 → 5
print(round(report.baseline_mean, 2), round(report.candidate_mean, 2))  # 4.0 3.67
```
**What to observe:** the mean barely moved (4.0 → 3.67), but case `b` **regressed hard** (5 → 2) while `c` improved — they nearly cancel in the average. A flat mean can hide a real regression; `compare_runs` surfaces it **per case**. This is why a regression test is not just "did the average drop?" (source: `sources/papers/mt-bench.md`).

---

## Section 5: Reflection Before Building

> The learner should fill UNDERSTANDING.md before proceeding to implementation.

**Questions to answer in UNDERSTANDING.md:**

1. In your own words, why can't you evaluate an open-ended answer with `assert output == expected`? What does LLM-as-a-judge do instead?
2. The judge agrees with humans ~80% of the time. Why is that "good enough to use" but "not safe to fully trust"? What do you do about the other 20%?
3. Pick two judge biases (position, verbosity, self-enhancement). For each, describe a concrete scenario where it gives the wrong score, and the mitigation.
4. Why ask the judge for reasoning *before* the score? Why `temperature=0`?
5. Predict what breaks if `parse_judge_score` silently returns `0` on an unparseable reply instead of raising. What happens to your mean and your pass-rate?
6. Why must the eval dataset be *frozen* between baseline and candidate? What does a regression test measure if the cases change?
7. Why can a regression be invisible in the mean score but obvious in `compare_runs`? (Use the Example 3 numbers.)
8. The one thing you still don't fully understand about evaluating AI systems.

---

## Section 6: Project Assignment

See PROJECT.md and source/project.md for the full specification.

### Core Requirement
Build a reusable evaluation harness in `code/`:
- **`llm_judge.py`** — `build_judge_prompt` (construct a bias-mitigated judge prompt) and `parse_judge_score` (robustly extract the score) are the *learner core*; `judge` (the model call) and the `JudgeResult` dataclass are *provided*.
- **`metrics.py`** — `summarize` (mean + pass-rate) is the *learner core*; simple `exact_match`/`contains` metrics are *provided* examples.
- **`regression_runner.py`** — `compare_runs` (baseline vs candidate → regressions) is the *learner core*; the run-a-dataset harness is *provided*.
- **`dataset.py`** — `TestCase` + a small frozen sample. *(Provided.)*
- **`report.py`** — format a summary / regression report. *(Provided.)*

### Extended Requirements
- **Pairwise judging** with **position-swap** to cancel position bias (source: `sources/papers/mt-bench.md`).
- **Reference-guided** judging: thread a reference answer/context through the prompt and measure the agreement lift (source: `sources/papers/mt-bench.md`).
- **Faithfulness metric** as a reference-free judge (decompose answer → verify each claim against context), reusing Project 04 (source: `sources/papers/ragas.md`).
- **Cost/latency tracking** per eval run (reuse Project 01's cost math).
- **Verbosity audit:** log answer length next to score and check the correlation.

### Start Building

**Open [`code/README.md`](../code/README.md)** for setup, the milestone build order, and the file roles (which files are *provided* vs. *learner-owned*). Run `python -m pytest` to see the failing guiding tests, then implement the learner-owned functions in milestone order until they pass.

---

## Section 7: Project Milestones

| Milestone | What You Build | Validation |
|-----------|---------------|------------|
| M1: Judge prompt | `llm_judge.build_judge_prompt` — scale, reasoning-before-score, optional reference | prompt contains the answer, the scale, asks for reasoning then score; includes the reference when given (offline test) |
| M2: Parse score | `llm_judge.parse_judge_score` — JSON / "Score: N" / "N/scale", clamp to range | parses each format to the right int; "9" with scale 5 → 5; garbage → ValueError (offline test) |
| M3: Aggregate | `metrics.summarize` — mean score + pass-rate at a threshold | `[5,4,3,2]`@4 → mean 3.5, pass_rate 0.5 (offline test) |
| M4: Regression | `regression_runner.compare_runs` — per-case drops beyond tolerance | baseline vs candidate flags the regressed case and the improved one; means computed (offline test) |
| M5: End-to-end eval | wire dataset → system-under-test → judge → summarize → report | run the harness on a prior project's outputs; get a mean + pass-rate report |
| M6: Break / Evaluate | reproduce a judge bias (verbosity/position) and a hidden regression | a wordier-but-not-better answer scores higher; a regression hidden in a flat mean; recorded in FAILURE_ANALYSIS.md |

---

## Section 8: Self-Evaluation

| Criterion | Does your implementation... | Pass? |
|-----------|---------------------------|-------|
| Judge prompt | define a fixed scale and ask for **reasoning before the score**? | |
| Reference-guided | include the reference in the prompt when one is provided? | |
| Robust parse | handle JSON and plain-text replies, and **clamp** out-of-range scores? | |
| Fail loud | raise (not silently `0`) when the reply has no score? | |
| Aggregate | report a mean **and** a pass-rate against a threshold? | |
| Regression | flag per-case drops, not just a change in the average? | |
| Frozen dataset | compare baseline and candidate over the **same** cases? | |
| Judge ≠ subject | use a judge model that isn't the model under test (or note the bias)? | |

**Red flags (your implementation may have problems if):**
- Your judge emits a score with no reasoning (or scores before reasoning).
- `parse_judge_score` returns `0` on an unparseable reply — your mean is now a lie.
- You report only a mean and miss a per-case regression (Example 3).
- You judge a model with itself and call the inflated score a win (self-enhancement).
- A prompt change "improved" scores but only made answers longer (verbosity bias).
- Your baseline and candidate were scored on different cases.

---

## Section 9: Common Mistakes

| Mistake | Why It Happens | Consequence | Fix |
|---------|---------------|-------------|-----|
| Trusting the judge as ground truth | "GPT-4 agrees 80% of the time" | The other ~20% silently corrupts decisions | Treat scores as a strong signal; spot-check (source: `sources/papers/mt-bench.md`) |
| Score before reasoning | Asking for a number first | Worse, less consistent scores | Reasoning first, then score (CoT) (source: `sources/papers/mt-bench.md`) |
| Silent parse fallback to 0 | "Handle the error quietly" | A few `0`s tank the mean; false regression | Clamp valid scores; raise on no-score |
| Mean-only reporting | A single number feels clean | A real regression hides in a flat average | Add per-case `compare_runs` (Example 3) |
| Judging a model with itself | Convenient, one model | Self-enhancement bias inflates the score | Use a different/stronger judge (source: `sources/papers/mt-bench.md`) |
| Ignoring verbosity | Longer looks more thorough | A wordier prompt fakes an "improvement" | Log length next to score; audit it (source: `sources/papers/mt-bench.md`) |
| Changing the dataset between runs | Adding cases as you go | Baseline vs candidate is no longer comparable | Freeze and version the dataset |
| `temperature` > 0 on the judge | Default sampling | Same answer gets different scores; flaky regression | Judge at `temperature=0` |

---

## Section 10: Connections

### How This Connects to Previous Projects
The judge **is** Project 01's `litellm.completion` — same call, but its job is to output a *score*. The **faithfulness** metric you build as an extension is Project 04's RAGAS work generalized (`F = |V|/|S|`), and **reference-guided** judging is the same instinct as grounding an answer in retrieved context (Projects 03/04). Any prior project (the chatbot, the RAG assistant, the copilot, the memory system) is a *system under test* you can now measure instead of eyeball.

### How This Connects to Future Projects
**Project 08 (agent)** needs evaluation badly — agents fail in long multi-step trajectories, and "did the agent succeed?" is itself a judge call over a transcript. **Project 09 (personal learning OS)** uses evaluation to know whether the system is actually helping the learner. The regression harness here is what lets every later project change prompts and models without flying blind. The LLM-rated **importance** from Project 05 was a special case of LLM-as-a-judge; this project is the general tool.

### How This Connects to StarcallOS
StarcallOS will change prompts, swap models, and add features constantly. Without this harness, every change is a gamble — you ship and hope. With it, every change is gated by a number: a frozen eval dataset of real StarcallOS tasks, an LLM judge you've validated and de-biased, a pass-rate you watch, and a regression report that blocks a merge when quality drops. The disciplines here — reasoning-before-score, frozen datasets, per-case regression, bias audits — are what make StarcallOS improvable instead of merely changeable.

### Production Patterns
Real eval stacks (Braintrust, LangSmith, OpenAI Evals) are this plus scale: versioned datasets, LLM-as-judge with validated prompts, pairwise + position-swap, reference-guided scoring, per-case dashboards, regression gates in CI, and cost/latency tracking per run (source: `sources/papers/mt-bench.md`). The frontier adds human-in-the-loop spot-checks to calibrate the judge and catch the ~20% it gets wrong.

---

## Assessment Rubric

See source/rubric.md for the complete grading rubric.

**Summary criteria:**
- [ ] Implementation runs correctly (dataset → judge → parse → summarize → regression report)
- [ ] The judge prompt asks for **reasoning before the score**, uses a fixed scale, and is reference-guided when a reference exists
- [ ] `parse_judge_score` is robust (JSON + text), clamps range, and fails loud on no-score
- [ ] Reporting includes a pass-rate and a **per-case** regression comparison, not just a mean
- [ ] Understanding document completed in learner's own words
- [ ] Failure analysis reproduces a judge bias and a hidden regression (quantified)
- [ ] Evaluation is quantitative (means, pass-rates, deltas, agreement spot-checks), not impressionistic
- [ ] StarcallOS reflection identifies at least one concrete applicable pattern

---

## Sources

See source/resources.md for the full annotated source list.

**Required reading:**
- `sources/papers/mt-bench.md` — LLM-as-a-judge: ~80% human agreement, the named biases (position/verbosity/self-enhancement), and the mitigations (reasoning-before-score, reference-guided, position-swap)
- `sources/papers/ragas.md` — reference-free metrics: faithfulness (`F = |V|/|S|`) and answer/context relevance; the worked metric this project generalizes

**Recommended reading:**
- `sources/official-docs/litellm-completion.md` — the judge is one `litellm.completion` call; `temperature=0` for repeatability (carried from Project 01)
- `sources/papers/sentence-bert.md` — embeddings behind answer-relevance similarity (carried from Projects 02/04)

---

## Instructor Notes

<!-- Hidden context for the mentor reviewing the learner's work. -->

**Common misconceptions:**
- That the judge is ground truth. It agrees with humans ~80% of the time — a strong signal, not an oracle (source: `sources/papers/mt-bench.md`).
- That a higher mean means "better." Verbosity bias and a hidden per-case regression both break that inference (source: `sources/papers/mt-bench.md`).
- That parsing is trivial. The judge replies in prose; robust extraction + clamping is the load-bearing, unglamorous step.
- That you can judge a model with itself for free. Self-enhancement bias inflates the score (source: `sources/papers/mt-bench.md`).
- That regression testing is "did the average drop?" It's per-case — a flat mean can hide a real drop.

**Diagnostic questions (reveal genuine vs. surface understanding):**
- "Your judge gives answer A (first) a 5 and answer B (first) a 5, but swaps to 4/5 when you reverse the order. What bias is this and how do you fix it?" (position bias; swap and average.)
- "Your mean score went 3.9 → 3.95 after a prompt change. Did it improve?" (can't tell from the mean — run `compare_runs`; also check length for verbosity.)
- "The judge replied 'This is excellent work, easily a 9 out of 10!' on a 1–5 scale. What should `parse_judge_score` return?" (clamp to 5 — not 9, not 0.)
- "Why reasoning before the score, and why temperature 0?" (CoT improves agreement + auditability; t=0 makes regression deterministic.)

**Signs of genuine understanding:**
- The learner reproduces a bias (e.g. pads an answer and watches the score rise) rather than asserting it exists.
- They show a regression that is invisible in the mean but caught per-case.
- Their judge prompt puts reasoning before the score and threads the reference through, and they can say why.
- They parse defensively and fail loud on no-score, and can explain how a silent `0` corrupts the mean.
- They use a different judge model than the one under test, or explicitly flag the self-enhancement risk.
