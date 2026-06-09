# EVALUATION.md — Elective 04

> From `python code/evaluate_monitor.py`.

## Detection on the fixtures

| Check | Result |
|-------|--------|
| Regressed route flagged (`search`) | |
| Metrics that triggered (error_rate / latency / cost) | |
| False alarms on baseline-vs-baseline (must be 0) | |

## Per-route metrics (window)

| Route | count | error_rate | avg latency | avg tokens | total cost |
|-------|-------|-----------|-------------|------------|------------|
| chat | | | | | |
| search | | | | | |
| tool | | | | | |

## One threshold-tuning move
*Change a threshold; show the alert sensitivity shift (caught vs false-alarm).*

## Conclusion
*One sentence: did the monitor catch the regression without crying wolf?*
