# FAILURE_ANALYSIS.md — Elective 04

> ≥3 experiments. **Two required:** (a) a **global-mean blind spot**, (b) a **swallowed error**.

## Experiment 1 — Global-mean blindness (required)
*Aggregate across ALL routes (one global mean) instead of per route. Does the search regression still show?*
- Change:
- What disappeared:
- Production implication:

## Experiment 2 — Swallowed error (required)
*Make `traced` catch the tool error and NOT record error=true. What does the monitor now see?*
- Change:
- Result (monitor blind to the failure):
- Lesson: the error must be a span attribute.

## Experiment 3 — Threshold tuning
*Tighten `error_rate_delta` / `latency_ratio` until the healthy baseline false-alarms; loosen until the regression is missed.*
- Observation (alert fatigue vs missed regression):

## What I learned about operating an unattended system
