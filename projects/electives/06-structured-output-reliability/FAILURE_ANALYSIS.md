# FAILURE_ANALYSIS.md — Elective 06: Structured Output & Reliability

> [learner] Break it on purpose. ≥3 experiments, **including the two required** below. For each:
> hypothesis → change → observation → diagnosis → implication.

## Required experiment A — blind retry (no error feedback)
*Make `build_repair_prompt` return a generic "please try again" with NO specific errors. Re-run the
schema case. Does it converge? Why does carrying the validation errors matter?*

- Hypothesis:
- Change:
- Observation:
- Diagnosis:
- Implication:

## Required experiment B — the bool/int trap
*Reorder `validate` so the int check runs before the bool check (or use a bare `isinstance(v, int)`).
Feed `{"priority": true, ...}`. Does the invalid object pass? What downstream bug would that cause?*

- Hypothesis:
- Change:
- Observation:
- Diagnosis:
- Implication:

## Experiment C — (your choice)
*E.g. drop the attempt budget to 1 and watch a fixable schema case fail; or remove fail-closed and see
an unvalidated object reach the caller; or feed truncated JSON (max_tokens cutoff).*

- Hypothesis:
- Change:
- Observation:
- Diagnosis:
- Implication:

## What this taught me about reliability
