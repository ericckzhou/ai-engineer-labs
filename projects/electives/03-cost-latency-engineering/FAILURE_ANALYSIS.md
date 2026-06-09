# FAILURE_ANALYSIS.md — Elective 03

> ≥3 experiments. **Two required:** (a) a semantic **false hit**, (b) a **never-escalating cascade**.

## Experiment 1 — Semantic false hit (required)
*Lower `cache_threshold` until "what is the capital of austria" returns the cached "Paris".*
- Threshold at which it false-hit:
- The wrong answer served:
- Production implication (a confident, cached, wrong answer):

## Experiment 2 — Never-escalate cascade (required)
*Raise `cascade_threshold` above the cheap model's confidence on hard items (or accept cheap always).*
- Change:
- Quality drop on the eval (hard items now wrong):
- Lesson: a cascade without escalation is just "use the cheap model".

## Experiment 3 — Cache a variable prefix (prompt caching)
*Conceptual or live: what happens to savings when the cached prefix changes every request?*
- Observation:

## What I learned about the cost/quality frontier
