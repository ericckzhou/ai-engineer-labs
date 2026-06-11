# EVALUATION.md — Elective 06: Structured Output & Reliability

> [learner] Measured results from `python code/evaluate.py`. Numbers, not vibes.

## Reliability per failure kind

| Kind | n | naive (parses+valid) | robust (coerce) | mean repair attempts |
|------|---|----------------------|-----------------|----------------------|
| clean | | | | |
| fenced | | | | |
| prose | | | | |
| schema | | | | |
| unfixable | | | | |
| **ALL** | | | | |

## Reading the table
*Which kinds were fixed by extraction alone (0 repairs)? Which needed a repair round? Did the unfixable
case correctly stay failed (fail closed)?*

## The honest part
*Where did naive "parse success" lie (parsed but invalid)? What did the repair loop cost in extra
generations, and when would that cost not be worth it (→ Elective 03)?*

## Conclusion
*Is the layer trustworthy enough to put in front of P06/P08? What's the residual failure rate?*
