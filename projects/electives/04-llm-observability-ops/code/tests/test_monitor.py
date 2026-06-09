"""[provided] Guiding tests for M3/M4. Fail with NotImplementedError until implemented.

Asserts PER-ROUTE aggregation and that drift is flagged on the regressed route only — and not on
a healthy baseline-vs-baseline comparison (no false alarm).
"""
from config import load_config
from monitor import aggregate, detect_drift


def test_aggregate_is_per_route(baseline_spans):
    m = aggregate(baseline_spans)
    assert set(m) == {"chat", "search", "tool"}
    assert m["search"].count == 3
    assert m["search"].error_rate == 0.0
    assert m["chat"].avg_latency_ms > 0


def test_detect_drift_flags_regressed_route(cfg, baseline_spans, window_spans):
    baseline = aggregate(baseline_spans)
    window = aggregate(window_spans)
    alerts = detect_drift(window, baseline, cfg=cfg)
    routes = {a.route for a in alerts}
    assert "search" in routes, "the regressed route must be flagged"
    assert "chat" not in routes, "a healthy route must not be flagged"


def test_no_false_alarm_on_baseline(cfg, baseline_spans):
    baseline = aggregate(baseline_spans)
    assert detect_drift(baseline, baseline, cfg=cfg) == [], "a healthy window must produce no alerts"
