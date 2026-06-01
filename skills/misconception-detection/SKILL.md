# Skill: Misconception Detection

**Type:** Method  
**Used by:** Reviewer, Misconception Analyst

## Purpose

Identify incorrect or incomplete beliefs in learner-written documents.

## Procedure

1. Read the ground truth: `source/lesson.agent.md` for the project
2. Read the learner's claim in `UNDERSTANDING.md`
3. For each statement, evaluate:
   - Is it factually correct?
   - Is it complete, or does it omit a critical qualifier?
   - Does it use the right words for the right things?
   - Does the analogy map correctly to the mechanism?
4. Flag any that are wrong or misleading
5. Do not partially confirm — a statement is correct or it is not

## Common Misconception Patterns

- Confusing what something does with how it works
- Confusing correlation with causation in AI behavior
- Treating probability as certainty ("the model knows X" vs "the model predicts X")
- Confusing the training process with inference behavior
- Treating a high-level abstraction as a primitive

## Output

For each misconception found:
```
Claim: [what the learner said]
Issue: [what is wrong or incomplete]
Truth: [what is actually true, with source if available]
Why it matters: [what breaks if you believe the wrong thing]
```
