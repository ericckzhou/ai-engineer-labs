"""[provided] Guiding tests for M1/M2. Fail with NotImplementedError until implemented.

Asserts the standard gen_ai.* attribute names and that `traced` records latency + route, and an
error as an attribute (not a swallowed exception).
"""
import pytest

from exporter import SpanCollector
from tracing import build_span, traced


def test_build_span_uses_standard_attribute_names():
    s = build_span("chat", model="m", route="chat", input_tokens=100, output_tokens=50,
                   finish_reason="stop", latency_ms=120.0, cost=0.01)
    assert s["gen_ai.operation.name"] == "chat"
    assert s["gen_ai.request.model"] == "m"
    assert s["gen_ai.usage.input_tokens"] == 100
    assert s["gen_ai.usage.output_tokens"] == 50
    assert s["gen_ai.response.finish_reasons"] == ["stop"]
    assert s["route"] == "chat"
    assert s["error"] is False


def test_traced_records_a_span():
    c = SpanCollector()

    @traced("chat", "chat", collector=c)
    def call():
        return {"model": "m", "input_tokens": 10, "output_tokens": 5,
                "finish_reason": "stop", "cost": 0.001}

    res = call()
    assert res["model"] == "m"
    assert len(c.spans) == 1
    span = c.spans[0]
    assert span["route"] == "chat"
    assert span["error"] is False
    assert span["latency_ms"] >= 0


def test_traced_records_error_as_attribute_and_reraises():
    c = SpanCollector()

    @traced("execute_tool", "tool", collector=c)
    def boom():
        raise RuntimeError("tool failed")

    with pytest.raises(RuntimeError):
        boom()
    assert len(c.spans) == 1
    assert c.spans[0]["error"] is True
    assert c.spans[0]["route"] == "tool"
