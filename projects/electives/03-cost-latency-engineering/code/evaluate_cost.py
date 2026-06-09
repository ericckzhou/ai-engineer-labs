"""evaluate_cost.py — [provided] Prove the optimization on the frozen eval set.

Runs the same eval two ways and prints the FRONTIER side by side:
  - baseline:  always the strong model, no cache (the correct-but-expensive reference),
  - optimized: cache + cascade (cheap-first, escalate on doubt, cache repeats).

Reports BOTH numbers — quality (pass-rate) AND cost — plus latency-proxy (model calls) and
cache-hit rate. A cost win without the paired quality number is half a result (lesson §3/§8).

Run AFTER implementing the cores: python evaluate_cost.py
"""
from __future__ import annotations

import json
from pathlib import Path

import cascade
from budget import CostTracker
from cache import SemanticCache
from config import load_config
from feature_backend import strong_answer

EVAL = Path(__file__).parent / "eval_set.jsonl"


def load_rows() -> list[dict]:
    return [json.loads(line) for line in EVAL.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    cfg = load_config()
    rows = load_rows()

    # Baseline: always strong, no cache.
    base_correct = 0
    base_cost = 0.0
    base_calls = 0
    for r in rows:
        ans = strong_answer(r["query"])
        base_cost += cfg.strong_price
        base_calls += 1
        base_correct += int(ans == r["expected"])

    # Optimized: cache + cascade.
    cache = SemanticCache()
    tracker = CostTracker()
    opt_correct = 0
    hits = 0
    for r in rows:
        res = cascade.answer(r["query"], cfg=cfg, cache=cache, tracker=tracker)
        opt_correct += int(res.text == r["expected"])
        hits += int(res.cache_hit)

    n = len(rows)
    print("=== Cost/Quality Frontier (baseline vs optimized) ===")
    print(f"{'':18}{'baseline':>12}{'optimized':>12}")
    print(f"{'quality (pass)':18}{_pct(base_correct, n):>12}{_pct(opt_correct, n):>12}")
    print(f"{'total cost':18}{base_cost:>12.4f}{tracker.total:>12.4f}")
    print(f"{'model calls':18}{base_calls:>12}{tracker.calls:>12}")
    print(f"{'cache hits':18}{'-':>12}{hits:>12}")
    if base_cost:
        print(f"\ncost reduction: {(100 * (base_cost - tracker.total) / base_cost):.0f}%  "
              f"(quality {_pct(base_correct, n)} -> {_pct(opt_correct, n)})")
    print("\nShip the optimization only if quality held. A cost win beside a quality drop is a "
          "regression (lesson §3).")


def _pct(n: int, d: int) -> str:
    return f"{(100.0 * n / d):.0f}%" if d else "n/a"


if __name__ == "__main__":
    main()
