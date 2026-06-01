# Operating Rules

These are the rules Claude follows when reasoning within this repository.

PHILOSOPHY.md says what we believe. This document says what Claude must do.

---

## Layer Hierarchy

The following hierarchy governs all reasoning and content decisions in this repo:

```
PHILOSOPHY.md          ← Beliefs. Never overridden.
  ↓
OPERATING_RULES.md     ← This file. Operational constraints.
  ↓
ARCHITECTURE.md        ← Structural decisions. Change via decision record only.
  ↓
sources/               ← Ground truth. Highest epistemic authority.
  ↓
docs/ + projects/      ← Teaching materials derived from sources.
  ↓
evaluations/           ← Judgments about learner work. Based on rubrics.
  ↓
memory/learner/        ← Personalization context. Never overrides truth.
```

Higher layers override lower layers when they conflict.

---

## Truth Rules

1. **Prefer source-backed claims over memory-backed claims.**
   If a claim appears in `sources/` and also in `memory/learner/reflections/`, the source is authoritative.

2. **Never derive truth from learner memory.**
   A learner believing X does not make X true. Learner memory informs instruction style, not content accuracy.

3. **Never invent citations.**
   If a claim needs a source and no source is available, say so explicitly. Do not fabricate URLs, paper titles, or author names.

4. **If a source cannot be found, state that clearly.**
   "I cannot find a primary source for this claim" is correct behavior. Proceeding without a source is not.

---

## Conflict Protocol

When a conflict between layers is detected:

**Step 1 — Identify.** Name the conflicting files or claims explicitly.
> Example: "UNDERSTANDING.md states X, but sources/papers/attention.md states Y."

**Step 2 — Prioritize.** State which layer has higher authority.
> Example: "sources/ outranks memory/learner/ in the hierarchy."

**Step 3 — Follow the higher layer.** Act on the authoritative source.
> Example: Teach Y, not X.

**Step 4 — Propose a record (if durable).** If the conflict implies a lasting change, propose a decision record.
> Example: "This learner's misconception about X is documented in memory/learner/misconceptions/. No architecture change needed."
> Example: "This conflict suggests the lesson in docs/ is outdated. Propose updating it."

---

## Personalization Rules

5. **Memory may influence instruction style, not truth.**
   Knowing the learner struggles with embeddings means: explain more carefully, use more analogies, check understanding more often. It does not mean: simplify the actual definition.

6. **Learner misconceptions are recorded, not adopted.**
   When a learner states something incorrect, record it in `memory/learner/misconceptions/`. Do not write content that reflects the misconception as if it were true.

7. **Assessments are based on rubrics, not impressions.**
   Grading a learner's understanding requires comparing against `evaluations/rubrics/`. Personal rapport or effort does not adjust the score.

---

## Architecture Rules

8. **Architecture may change only through a decision record.**
   If a structural change to the repo is needed (new directory, renamed convention, changed hierarchy), it must be documented in `memory/project/decisions/` before being made.

9. **Catalogs are indexes, not truth.**
   `catalogs/*.md` files contain pointers to where truth lives. They do not contain the truth itself. Never use a catalog entry as a primary claim.

10. **Source structure follows the tier system.**
    Sources are organized by type: `sources/papers/`, `sources/books/`, `sources/videos/`, `sources/articles/`, `sources/official-docs/`. Do not place sources in other directories.

---

## Teaching Rules

11. **Teach intuition before terminology.**
    Introduce the concept with an analogy or simple explanation before naming it formally.

12. **Acknowledge what the learner doesn't know yet.**
    "We haven't covered X yet, but it will become relevant in Project N" is correct behavior. Introducing a concept without foundation creates confusion, not learning.

13. **Do not confirm misunderstanding.**
    If a learner's explanation in `UNDERSTANDING.md` contains an error, flag it — do not reinforce it even partially. Partial reinforcement of wrong models is worse than no feedback.

---

## Scope Rules

14. **This repo is separate from StarcallOS.**
    Do not build StarcallOS components here. Do extract patterns that StarcallOS could use. The `STARCALLOS_REFLECTION.md` in each project is the only place this connection is made.

15. **Projects are self-contained.**
    Each project in `projects/` must run independently. Do not create dependencies between projects unless explicitly designed.

---

## Scaffolding Rules

These rules govern what Claude provides versus what the learner must build. The repository removes accidental friction and preserves essential struggle. They apply to every project under `projects/`.

16. **Solve setup; leave the learning target incomplete.**
    - Setup should be solved (dependencies, environment, run/test commands, project skeleton).
    - Interfaces should be clear (function signatures, contracts, types).
    - The learning target should be incomplete — the learner implements the core logic.

17. **Always provide; never provide.**
    *Always provide:* clear project brief, starter files, dependency setup, `.env.example` when environment variables are needed, a one-command run workflow, a one-command test workflow, tests or checks that guide the learner, rubric, reflection prompts, optional hints, extension tasks.
    *Never provide:* a complete working solution for the learner-owned core component, copy-paste final answers, hidden "magic" code that bypasses the intended learning, or excessive scaffolding that removes the main design decision.

18. **Label every project file or section with exactly one role.**
    - `provided` — complete scaffolding or support code (setup, plumbing, fixtures).
    - `partial` — starter code with TODOs marking learner-owned gaps.
    - `learner` — the core implementation the learner must write.
    - `reference` — explanatory material, rubric, hints, or docs.
    Mark learner-owned work concretely: TODOs, `NotImplementedError`, failing tests, or empty functions/classes.

19. **Choose the incomplete component from the learning objective.**
    - API wiring → leave message construction and model-call logic incomplete.
    - Prompt design → provide model-call plumbing; leave prompt construction incomplete.
    - Conversation memory → provide model-call plumbing; leave history management incomplete.
    - Evaluation → provide chatbot behavior; leave eval design/instrumentation incomplete.

---

## When Rules Conflict With Each Other

Apply the most specific rule. If equally specific, apply the rule that preserves truth.

If you cannot resolve the conflict, surface it explicitly rather than silently choosing.
