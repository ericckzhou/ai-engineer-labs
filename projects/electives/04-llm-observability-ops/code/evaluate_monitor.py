"""evaluate_monitor.py — [provided] Score the drift monitor on the replayable fixtures.

Two checks (lesson §7):
  1. detect_drift(window, baseline) must FLAG the regressed route ("search").
  2. detect_drift(baseline, baseline) must be EMPTY (no false alarm on a healthy window).

Run AFTER implementing tracing.py/monitor.py: python evaluate_monitor.py
"""
from __future__ import annotations

from pathlib import Path

from config import load_config
from exporter import load_spans
from monitor import aggregate, detect_drift

FIX = Path(__file__).parent / "fixtures"


def main() -> None:
    cfg = load_config()
    baseline = aggregate(load_spans(FIX / "baseline.jsonl"))
    window = aggregate(load_spans(FIX / "window_regressed.jsonl"))

    print("=== Per-route metrics (window) ===")
    for route, m in sorted(window.items()):
        print(f"  {route:8s} n={m.count} err={m.error_rate:.0%} "
              f"lat={m.avg_latency_ms:.0f}ms tok={m.avg_tokens:.0f} cost={m.total_cost:.4f}")

    print("\n=== Drift: window vs baseline ===")
    alerts = detect_drift(window, baseline, cfg=cfg)
    for a in alerts:
        print(f"  ALERT [{a.route}] {a.metric}: {a.baseline:.3g} -> {a.current:.3g}")
    if not alerts:
        print("  (no alerts — did the monitor miss the regression?)")

    print("\n=== False-alarm check: baseline vs baseline ===")
    clean = detect_drift(baseline, baseline, cfg=cfg)
    print(f"  alerts on healthy window: {len(clean)} (must be 0)")

    routes = {a.route for a in alerts}
    ok = ("search" in routes) and (len(clean) == 0)
    print(f"\nRESULT: {'PASS' if ok else 'CHECK'} — caught the regressed route AND no false alarm."
          if ok else
          f"\nRESULT: CHECK — flagged {routes or 'nothing'}; false alarms on baseline: {len(clean)}.")


if __name__ == "__main__":
    main()
