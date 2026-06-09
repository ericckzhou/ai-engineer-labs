# FAILURE_ANALYSIS.md — Elective 05

> ≥3 experiments. **Two required:** (a) a transform that **didn't help / hurt**, (b) a
> **naive-concatenation fusion** diluting relevance.

## Experiment 1 — A transform that doesn't help (required)
*Run HyDE (or rewrite) on the factual query. Compare hit / context-precision / faithfulness vs baseline.*
- Transform + query:
- Result (did it help, hurt, or no-op?):
- Lesson: fancier isn't always better.

## Experiment 2 — Concatenation fusion (required)
*Replace fusion (dedupe + re-rank) with concatenate-all on the multi-hop query. What happens to context-precision / faithfulness?*
- Change:
- Result (distractor dilution):
- Why re-ranking the union matters:

## Experiment 3 — Rewrite drift
*Force a rewrite that changes the meaning. Watch retrieval go to the wrong place.*
- Change:
- Result:

## What I learned about engineering the query vs. the index
