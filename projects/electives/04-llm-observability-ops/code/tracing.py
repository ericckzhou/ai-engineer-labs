"""tracing.py — [learner] GenAI span emission. Learning target (M1–M2).

Build spans with the STANDARD OpenTelemetry GenAI attribute names — that standardization is the
whole point (any tool can read them). See source/lesson.agent.md §4 and
sources/official-docs/opentelemetry-genai-semconv.md.

An error is a SPAN ATTRIBUTE, not a swallowed exception — record error=True so the monitor can
later see the error-rate rise.
"""
from __future__ import annotations

import time
from collections.abc import Callable


def build_span(
    operation: str,
    *,
    model: str | None,
    route: str,
    input_tokens: int,
    output_tokens: int,
    finish_reason: str | None,
    latency_ms: float,
    cost: float = 0.0,
    error: bool = False,
) -> dict:
    """Return a span dict keyed by the STANDARD gen_ai.* attributes (plus latency/route/cost/error).

    Required keys (exact names — interoperability depends on them):
        "gen_ai.operation.name"          -> operation         (e.g. "chat", "execute_tool")
        "gen_ai.request.model"           -> model
        "gen_ai.usage.input_tokens"      -> input_tokens
        "gen_ai.usage.output_tokens"     -> output_tokens
        "gen_ai.response.finish_reasons" -> [finish_reason]   (a list)
    Plus operational fields the monitor aggregates: "route", "latency_ms", "cost", "error".

    Example:
        build_span("chat", model="m", route="chat", input_tokens=100, output_tokens=50,
                   finish_reason="stop", latency_ms=120.0, cost=0.01)
        -> {"gen_ai.operation.name": "chat", "gen_ai.request.model": "m",
            "gen_ai.usage.input_tokens": 100, "gen_ai.usage.output_tokens": 50,
            "gen_ai.response.finish_reasons": ["stop"],
            "route": "chat", "latency_ms": 120.0, "cost": 0.01, "error": False}
    """
    raise NotImplementedError("M1: build the span dict with the standard gen_ai.* attribute names.")


def traced(operation: str, route: str, *, collector) -> Callable:
    """Decorator: time the wrapped call, build a span, and add it to `collector`.

    The wrapped function returns a dict with keys: model, input_tokens, output_tokens,
    finish_reason, cost. On success: build a span (error=False) from those + the measured latency.
    On exception: build a span with error=True (zeros/None for the call fields) BEFORE re-raising,
    so the failure is recorded — never swallow it.

    Example:
        c = SpanCollector()
        @traced("chat", "chat", collector=c)
        def call(): return {"model": "m", "input_tokens": 10, "output_tokens": 5,
                            "finish_reason": "stop", "cost": 0.001}
        call(); assert c.spans[0]["route"] == "chat" and c.spans[0]["error"] is False
    """
    def decorator(fn: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            raise NotImplementedError(
                "M2: time fn, build a span (error attr on failure), collect it; re-raise on error."
            )
        return wrapper
    return decorator


# Provided helper: a millisecond timer you may use inside `traced`.
def now_ms() -> float:
    return time.perf_counter() * 1000.0
