"""[provided] Guiding test for Milestone M5 — evaluate.recall@k of ANN vs exact baseline.

Offline: in-memory cosine collection + fake embed (skips if chromadb absent). On this tiny, clean
corpus the ANN index matches the exact baseline, so recall is 1.0 — the point is that evaluate()
computes the number. Fails until evaluate() (and the baseline functions it uses) are implemented.
Mirrors the docstring example in evaluate.py. Run: python -m pytest tests/test_evaluate.py
"""
import pytest

import evaluate
from conftest import fake_embed_many, fake_embed_one


def test_evaluate_recall(cosine_collection, monkeypatch):
    col, docs, ids = cosine_collection
    monkeypatch.setattr(evaluate, "embed_one", fake_embed_one)
    monkeypatch.setattr(evaluate, "embed_many", fake_embed_many)

    report = evaluate.evaluate(col, docs, ids, ["interest rates", "magic school"], k=1)

    assert report["per_query"]["interest rates"] == pytest.approx(1.0)
    assert report["per_query"]["magic school"] == pytest.approx(1.0)
    assert report["mean_recall"] == pytest.approx(1.0)
