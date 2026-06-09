"""rag_backend.py — [reference] Project 04's retriever + corpus + reader, condensed. Provided whole.

OFFLINE and deterministic so the elective is gradeable with no provider:
  - a small corpus with paraphrase, factual, and MULTI-HOP items (+ distractors),
  - a token-overlap embedder/retriever (Project 02/03, deterministic),
  - a crude reader that assembles an answer from the retrieved chunks,
  - CANNED transform outputs (a fixture) so the offline core needs no LLM.

The query-transformation stage (query_transforms.py) and the fusion (advanced_rag.py) are the
learner's job. Re-ranking is provided in rerank.py (it's Project 03 — already learned).
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass

_WORD = re.compile(r"[a-z0-9]+")


def norm(text: str) -> str:
    return " ".join(_WORD.findall(text.lower()))


@dataclass(frozen=True)
class Chunk:
    id: str
    text: str


# Corpus. Order matters only for zero-overlap ties: distractors first so a bare query that
# matches nothing retrieves distractors (and a transform is what rescues retrieval).
CORPUS: list[Chunk] = [
    Chunk("c2", "Shipping is free on orders over fifty dollars."),
    Chunk("c4", "Our mission is to make learning durable."),
    Chunk("c8", "Customer support is available by email."),
    Chunk("c9", "Pride and Prejudice was written by Jane Austen."),
    Chunk("c3", "The company was founded in 2011 in Boston."),
    Chunk("c5", "The CTO is Dana Lee."),
    Chunk("c6", "Dana Lee studied at Caltech."),
    Chunk("c7", "Alex studied at Caltech; Sam studied at Yale."),
    Chunk("c1", "Refund policy: returns are accepted within 30 days with a receipt for a full refund."),
]


def embed(text: str) -> dict[str, int]:
    v: dict[str, int] = {}
    for w in _WORD.findall(text.lower()):
        v[w] = v.get(w, 0) + 1
    return v


def cosine(a: dict[str, int], b: dict[str, int]) -> float:
    if not a or not b:
        return 0.0
    dot = sum(cnt * b.get(term, 0) for term, cnt in a.items())
    na = math.sqrt(sum(c * c for c in a.values()))
    nb = math.sqrt(sum(c * c for c in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def retrieve(query: str, k: int) -> list[Chunk]:
    """Top-k chunks by token-overlap similarity (stable: ties keep corpus order)."""
    qv = embed(query)
    scored = [(cosine(qv, embed(c.text)), i, c) for i, c in enumerate(CORPUS)]
    scored.sort(key=lambda t: (-t[0], t[1]))
    return [c for _s, _i, c in scored[:k]]


def read(query: str, chunks: list[Chunk]) -> str:
    """A crude grounded reader: the answer is assembled from the (fused) chunks."""
    if not chunks:
        return "I don't have enough information to answer."
    return " ".join(c.text for c in chunks)


# ---- Canned transform outputs (offline fixture). query_transforms reads these; the live LLM
# version is an extension. Keys are normalized queries. ----
REWRITES: dict[str, str] = {
    "how do i get my money back": "refund policy return window receipt full refund",
    "what year was the company founded": "company founding year founded boston",
    "did any founder attend the same school as our chief technology officer":
        "founder same university as CTO Dana Lee Caltech",
}

HYDES: dict[str, str] = {
    "how do i get my money back":
        "Returns are accepted within thirty days for a full refund if you keep the receipt.",
    "what year was the company founded": "The company was founded in 2011 in Boston.",
    "did any founder attend the same school as our chief technology officer":
        "Alex, a founder, studied at Caltech, the same school the CTO attended.",
}

DECOMPOSITIONS: dict[str, list[str]] = {
    "did any founder attend the same school as our chief technology officer":
        ["who is the CTO", "where did Dana Lee study", "which founder studied at Caltech"],
}
