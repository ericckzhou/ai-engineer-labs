"""tracing.py — [REFERENCE SOLUTION] verified copy (solns branch). Starter (NotImplementedError) on main."""
from __future__ import annotations

import functools
import time
from collections.abc import Callable


def build_span(operation, *, model, route, input_tokens, output_tokens, finish_reason,
               latency_ms, cost=0.0, error=False) -> dict:
    return {
        "gen_ai.operation.name": operation,
        "gen_ai.request.model": model,
        "gen_ai.usage.input_tokens": input_tokens,
        "gen_ai.usage.output_tokens": output_tokens,
        "gen_ai.response.finish_reasons": [finish_reason] if finish_reason is not None else [],
        "route": route,
        "latency_ms": latency_ms,
        "cost": cost,
        "error": error,
    }


def traced(operation: str, route: str, *, collector) -> Callable:
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            start = now_ms()
            try:
                result = fn(*args, **kwargs)
            except Exception:
                collector.add(build_span(
                    operation, model=None, route=route, input_tokens=0, output_tokens=0,
                    finish_reason="error", latency_ms=now_ms() - start, cost=0.0, error=True))
                raise
            collector.add(build_span(
                operation, model=result.get("model"), route=route,
                input_tokens=result.get("input_tokens", 0),
                output_tokens=result.get("output_tokens", 0),
                finish_reason=result.get("finish_reason"),
                latency_ms=now_ms() - start, cost=result.get("cost", 0.0), error=False))
            return result
        return wrapper
    return decorator


def now_ms() -> float:
    return time.perf_counter() * 1000.0
