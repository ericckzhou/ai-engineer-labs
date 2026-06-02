"""[provided] Test fixtures for Project 04.

Makes code/ importable from tests/. The learner cores tested offline here — chunk_text, build_prompt,
faithfulness_score — are pure logic and need no network or provider. A deterministic fake embed is
provided for anyone extending the suite to the (provided) retriever without a real embedding model.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Deterministic stand-in "embeddings" (3-D), direction encodes topic. Only needed if you write a
# retriever test (retriever.py is provided, so its tests are optional).
FAKE_VECTORS = {
    "Q3 revenue was 4.2M, up 8% YoY.": [1.0, 0.0, 0.0],
    "Opened a Berlin office in July.": [0.0, 1.0, 0.0],
    "What was Q3 revenue?": [0.98, 0.05, 0.0],
}


def fake_embed_many(texts: list[str]) -> list[list[float]]:
    return [list(FAKE_VECTORS.get(t, [0.0, 0.0, 1.0])) for t in texts]


def fake_embed_one(text: str) -> list[float]:
    return fake_embed_many([text])[0]
