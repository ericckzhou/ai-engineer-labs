"""evaluate.py — [provided] Measure reliability: naive strict-parse baseline vs the robust coerce loop.

Run (offline; needs structured_output.py implemented):  python evaluate.py

The point of M5: a metric, not a vibe. It reports, per failure kind, how often a NAIVE
`json.loads(raw_output)` succeeds vs how often the full extract->validate->repair loop produces a
schema-valid object. Robust should reach ~100% EXCEPT the 'unfixable' kind — which must FAIL CLOSED
(stay 0%), never pass an unvalidated object. The gap between the two columns is the value of the loop;
the repair attempts it costs are the price (connects to Elective 03 — cost & latency).
"""
from __future__ import annotations

import collections
import json
import pathlib

import fake_backend
from structured_output import StructuredOutputError, coerce, parse_strict, validate

HERE = pathlib.Path(__file__).parent


def load_set() -> list[dict]:
    rows = []
    for line in (HERE / "eval_set.jsonl").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def main() -> None:
    rows = load_set()
    by_kind: dict[str, dict] = collections.defaultdict(lambda: {"n": 0, "baseline": 0, "robust": 0})

    for r in rows:
        case = next(c for c in fake_backend.CASES if c.cid == r["id"])
        k = by_kind[r["kind"]]
        k["n"] += 1
        # naive baseline: is the RAW first output directly usable? (parses AND satisfies the schema)
        # NB: the 'schema' cases parse fine but are INVALID — "it parsed" is not "it's valid".
        try:
            if validate(parse_strict(case.raw)) == []:
                k["baseline"] += 1
        except Exception:
            pass
        # robust: the full extract -> validate -> repair loop
        fake_backend.reset()
        try:
            out = coerce(case.text)
            if validate(out) == []:
                k["robust"] += 1
        except StructuredOutputError:
            pass

    print(f"{'kind':<11}{'n':>3}{'naive':>8}{'robust':>9}")
    print("-" * 31)
    tot = {"n": 0, "baseline": 0, "robust": 0}
    for kind, k in sorted(by_kind.items()):
        print(f"{kind:<11}{k['n']:>3}{k['baseline'] / k['n']:>8.0%}{k['robust'] / k['n']:>9.0%}")
        for f in tot:
            tot[f] += k[f]
    print("-" * 31)
    print(f"{'ALL':<11}{tot['n']:>3}{tot['baseline'] / tot['n']:>8.0%}{tot['robust'] / tot['n']:>9.0%}")
    print("\nnaive  = raw output parses AND satisfies the schema (directly usable)")
    print("robust = extract -> validate -> repair loop yields a schema-valid object")
    print("The 'unfixable' kind SHOULD stay 0% under robust: failing closed is correct, not a bug.")


if __name__ == "__main__":
    main()
