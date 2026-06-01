"""[provided] Guiding test for Milestone M6 (extended) — rerank.rerank().

Stubs the cross-encoder so the test is OFFLINE (no model download). Fails until rerank() is
implemented. Mirrors the docstring example in rerank.py. Run: python -m pytest tests/test_rerank.py
"""
import rerank


class _StubCrossEncoder:
    """Fake: scores a (query, doc) pair high if the doc looks on-topic for 'interest rates'."""
    def predict(self, pairs):
        scores = []
        for _query, doc in pairs:
            on_topic = ("central bank" in doc) or ("rates" in doc) or ("interest" in doc)
            scores.append(8.2 if on_topic else -6.1)
        return scores


def test_rerank_orders_on_topic_first(monkeypatch):
    monkeypatch.setattr(rerank, "get_cross_encoder", lambda: _StubCrossEncoder())
    out = rerank.rerank("interest rates", ["A wizard cast a spell.",
                                           "The central bank raised rates."])
    assert out[0][0] == "The central bank raised rates."   # on-topic re-ranked to the top
    assert out[0][1] > out[1][1]                            # scores descending
