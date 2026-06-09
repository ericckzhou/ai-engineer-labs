# FAILURE_ANALYSIS.md — Elective 02

> Break your own guard on purpose. ≥3 experiments. **Two are required:** (a) a fail-open bug, and
> (b) an indirect-injection case. For each: what you changed, what happened, why, and the
> production implication.

## Experiment 1 — Fail OPEN (required)
*Remove a fail-closed default (make a guard return the original text on error), feed hostile input.*
- Change:
- What happened:
- Why it's worse than no guard:
- Production implication:

## Experiment 2 — Indirect injection (required)
*Move an attack string from the user prompt into `retrieved`. Does your scanner still catch it?*
- Setup:
- Result:
- What this proves about scanning only user input:

## Experiment 3 — Over-broad rule (precision)
*Make a scan rule too broad; watch a benign input get blocked. Measure the false-positive jump.*
- Change:
- Benign input wrongly blocked:
- Tradeoff observed:

## (Optional) Experiment 4 — Canary / exfiltration trap
- Setup:
- Result:

## What I learned about the limits of guardrails
*(Tie back to: OWASP "bypassable"; Greshake "mitigations lacking"; Presidio "no guarantee".)*
