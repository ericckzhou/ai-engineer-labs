"""monitor.py — [REFERENCE SOLUTION] verified copy (solns branch). Starter (NotImplementedError) on main."""
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
    metric: str
    baseline: float
    current: float


def aggregate(spans: list[dict]) -> dict[str, RouteMetrics]:
    groups: dict[str, list[dict]] = {}
    for s in spans:
        groups.setdefault(s["route"], []).append(s)
    out: dict[str, RouteMetrics] = {}
    for route, items in groups.items():
        n = len(items)
        errors = sum(1 for s in items if s.get("error"))
        lat = sum(s["latency_ms"] for s in items) / n
        toks = sum(s.get("gen_ai.usage.input_tokens", 0) + s.get("gen_ai.usage.output_tokens", 0)
                   for s in items) / n
        cost = sum(s.get("cost", 0.0) for s in items)
        out[route] = RouteMetrics(n, errors / n, lat, toks, cost)
    return out


def detect_drift(current, baseline, *, cfg: Config | None = None) -> list[Alert]:
    cfg = cfg or load_config()
    alerts: list[Alert] = []
    for route, cur in current.items():
        base = baseline.get(route)
        if base is None:
            continue
        if cur.error_rate - base.error_rate > cfg.error_rate_delta:
            alerts.append(Alert(route, "error_rate", base.error_rate, cur.error_rate))
        if base.avg_latency_ms > 0 and cur.avg_latency_ms > base.avg_latency_ms * cfg.latency_ratio:
            alerts.append(Alert(route, "latency", base.avg_latency_ms, cur.avg_latency_ms))
        if base.total_cost > 0 and cur.total_cost > base.total_cost * cfg.cost_ratio:
            alerts.append(Alert(route, "cost", base.total_cost, cur.total_cost))
    return alerts
