# Skill: Mentor Reviewer

**Type:** Method  
**Used by:** Reviewer, Misconception Analyst

## Purpose

Review a learner's `UNDERSTANDING.md` for accuracy, depth, and completeness. Produce coaching feedback. This is not formal grading — that is the Grader agent's job.

## Governing Documents

1. `OPERATING_RULES.md` — especially rule: do not confirm misconceptions, even partially
2. `skills/misconception-detection/SKILL.md` — procedure for identifying incorrect beliefs

## Ground Truth Source

**Always read `source/lesson.agent.md` for the current project before reviewing.**

The lesson is the standard. The learner's understanding is compared against it. Do not compare against memory or general knowledge — compare against the lesson as written.

## Procedure

1. Read `projects/XX/source/lesson.agent.md` — internalize what is correct
2. Read `projects/XX/UNDERSTANDING.md` — the learner's claims
3. For each learner statement, evaluate against the lesson:
   - Factually correct?
   - Complete, or missing a critical qualifier?
   - Right words used for the right things?
   - Does the analogy map accurately to the mechanism?
4. Identify strengths, weaknesses, misconceptions, and gaps
5. Write `UNDERSTANDING_FEEDBACK.md` using the structure below

## Critical Constraint

**Do not partially confirm incorrect statements.**

If a learner's explanation is mostly right but contains a meaningful error, the error must be flagged clearly — not softened by leading with how much they got right. A partially confirmed wrong model is worse than no feedback, because the learner leaves believing they understood when they didn't.

Correct: "Your analogy for embeddings is close, but it misrepresents one thing: ..."  
Incorrect: "Great intuition! Just a small note: ..."

## Output: `UNDERSTANDING_FEEDBACK.md`

Write to `projects/XX/UNDERSTANDING_FEEDBACK.md`.

Structure:

```markdown
# Understanding Feedback

**Project:** [number and name]
**Date:** YYYY-MM-DD
**Reviewer:** Mentor (Claude)

---

## Strengths

[Quote what the learner got right. Be specific — quote their words, confirm they're correct, say why they matter.]

---

## Weaknesses

[What is incomplete, vague, or stated without sufficient depth. Not wrong — just not enough yet.]

---

## Misconceptions

[For each: quote the learner's claim, state what is actually true, cite the lesson section, explain why the wrong model causes real problems.]

Format per misconception:
> Learner said: "..."
> Issue: ...
> Truth: ... (see lesson.agent.md §X)
> Why it matters: ...

---

## Missing Concepts

[Concepts present in the lesson that the learner did not address at all.]

---

## Suggested Improvements

[Specific, actionable. "Re-read section X and rewrite your explanation of Y in terms of Z."]

---

## Recommended Next Steps

[ ] Re-read: [specific section of lesson.agent.md]
[ ] Rewrite: [specific part of UNDERSTANDING.md]
[ ] Clarify: [specific concept]
[ ] Ready to implement — no blockers

---

## Confidence Assessment

Rate overall understanding readiness:

- **Beginner** — Significant misconceptions present. Must revise before implementing.
- **Developing** — Mostly correct but missing depth or key concepts. Can implement with caution.
- **Competent** — Understands the core. Ready to implement. Minor gaps won't block progress.
- **Strong** — Accurate, complete, and shows insight. Ready to implement independently.
- **Advanced** — Demonstrates understanding beyond the lesson. Can explain tradeoffs and failure modes.

**Assessment:** [level]

**Rationale:** [one paragraph of evidence]
```

## What This Skill Is Not

- **Not grading** — no numerical score. Use the Grader agent + `evaluations/rubrics/master-rubric.md` for formal assessment.
- **Not rewriting** — do not rewrite the learner's explanation for them. Point to the gap; let them fix it.
- **Not validating effort** — the quality of the understanding matters, not how much time was spent.
