"""monitor.py — [learner] Aggregate traces and detect drift. Learning target (M3–M4).

The non-negotiable design choice: aggregate and compare PER ROUTE, never on a global mean. A
healthy overall average hides one route gone to a 0% pass-rate / 10x latency (same trap as P09).
See source/lesson.agent.md §6–§7 and sources/articles/llm-online-evaluation-drift.md.
"""
from __future__ import annotations

from dataclasses import dataclass

from config import Config, load_config


@dataclass
class RouteMetrics:
    count: int
    error_rate: float
    avg_latency_ms: float
    avg_tokens: float
    total_cost: float


@dataclass
class Alert:
    route: str
    metric: str        # "error_rate" | "latency" | "cost"
    baseline: float
    current: float


def aggregate(spans: list[dict]) -> dict[str, RouteMetrics]:
    """Roll spans up PER ROUTE.

    For each distinct span["route"], compute:
        count        — number of spans
        error_rate   — fraction with span["error"] truthy
        avg_latency  — mean of span["latency_ms"]
        avg_tokens   — mean of (input_tokens + output_tokens)   (gen_ai.usage.* keys)
        total_cost   — sum of span["cost"]

    Example: aggregate(spans)["search"].error_rate == 0.0   (a healthy route)
    """
    raise NotImplementedError("M3: group spans by route and compute per-route metrics.")


def detect_drift(
    current: dict[str, RouteMetrics],
    baseline: dict[str, RouteMetrics],
    *,
    cfg: Config | None = None,
) -> list[Alert]:
    """Compare a live window to the baseline PER ROUTE; return alerts for regressions.

    For each route present in both, raise an Alert when:
      - error_rate rose by more than cfg.error_rate_delta (absolute), or
      - avg_latency_ms > baseline.avg_latency_ms * cfg.latency_ratio, or
      - total_cost     > baseline.total_cost     * cfg.cost_ratio.

    detect_drift(baseline, baseline, cfg=cfg) must return [] (no false alarm on a healthy window).
    """
    cfg = cfg or load_config()
    raise NotImplementedError("M4: per-route comparison vs cfg thresholds → list[Alert].")
