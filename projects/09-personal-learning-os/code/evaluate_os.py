"""evaluate_os.py — [learner] Milestone M4 — evaluate the SYSTEM's front door (the router).

"The router feels right" is not evaluation. To know whether a routing change helped or hurt, you need
NUMBERS on a frozen labeled set — and crucially, numbers PER ROUTE, not just an overall mean. A router
can score 90% overall while being silently 0% on SAVE (dropping every "remember this"). Only the
per-route breakdown exposes that. This is Project 07/08's "measure per case, not just the average"
discipline pointed at the system's front door (sources/papers/mt-bench.md).

PROVIDED: nothing to implement but this function — it's pure logic over your route function.
LEARNER:  evaluate_routing (M4).

Run:  python -m pytest tests/test_evaluate_os.py
"""
from __future__ import annotations

from typing import Callable


def evaluate_routing(cases: list[dict], route_fn: Callable) -> dict:
    """[learner] Score `route_fn` on labeled routing `cases`. Overall + per-route + misroutes. (M4)

    cases: [{"query": str, "expected_route": str}, ...]  — a FROZEN labeled set.
    route_fn: a function query -> Route (e.g. router.route_query); use route_fn(case["query"]).name.

    Return a dict with EXACTLY these keys:
      - "accuracy":  correct / total   (overall; 0.0 if there are no cases)
      - "per_route": {expected_route: correct_for_that_route / total_for_that_route}
                     — one entry per DISTINCT expected_route that appears in `cases`. This is the
                       breakdown that reveals a silently-broken route a mean would hide.
      - "misroutes": [{"query", "expected", "got"} for every case the router got wrong]

    Steps:
      1. total = len(cases). If total == 0: return {"accuracy": 0.0, "per_route": {}, "misroutes": []}.
      2. Track per-expected-route counters: total_r and correct_r (e.g. two dicts, or a dict of pairs).
      3. For each case: got = route_fn(case["query"]).name; expected = case["expected_route"].
           - bump total_r[expected]; if got == expected: bump correct_r[expected] (and an overall counter).
           - else: append {"query": case["query"], "expected": expected, "got": got} to misroutes.
      4. accuracy = overall_correct / total.
         per_route = {r: correct_r[r] / total_r[r] for r in total_r}.
      5. Return {"accuracy", "per_route", "misroutes"}.

    The trap: don't report only the overall mean. The per-route map is the point — it's how you catch
    the route that's at 0% while the average still looks healthy.

    Example (mirrors tests/test_evaluate_os.py::test_evaluate_*):
        cases = [{"query": "note: milk", "expected_route": "SAVE"},
                 {"query": "summarize my week", "expected_route": "TASK"}]
        # suppose route_fn sends "summarize my week" to RECALL by mistake:
        evaluate_routing(cases, route_fn)
          -> {"accuracy": 0.5,
              "per_route": {"SAVE": 1.0, "TASK": 0.0},
              "misroutes": [{"query": "summarize my week", "expected": "TASK", "got": "RECALL"}]}
    """
    total = len(cases)
    if total == 0:
        return {"accuracy": 0.0, "per_route": {}, "misroutes": []}

    total_r: dict[str, int] = {}
    correct_r: dict[str, int] = {}
    misroutes: list[dict] = []
    overall_correct = 0

    for case in cases:
        expected = case["expected_route"]
        got = route_fn(case["query"]).name
        total_r[expected] = total_r.get(expected, 0) + 1
        if got == expected:
            correct_r[expected] = correct_r.get(expected, 0) + 1
            overall_correct += 1
        else:
            misroutes.append({"query": case["query"], "expected": expected, "got": got})

    per_route = {r: correct_r.get(r, 0) / total_r[r] for r in total_r}
    return {"accuracy": overall_correct / total, "per_route": per_route, "misroutes": misroutes}
