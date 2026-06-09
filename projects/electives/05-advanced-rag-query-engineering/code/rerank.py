"""rerank.py — [provided] Project 03's re-ranking. NOT the learning target here — USE it.

A cross-encoder re-ranker, condensed to a deterministic token-overlap scorer for offline use. Its
role in this elective is the FUSION stage: turn the noisy union of multi-query results into a
clean, relevance-ordered top-n. Do not rebuild this — call it from advanced_rag.fuse.
"""
from __future__ import annotations

from rag_backend import Chunk, cosine, embed


def rerank(query: str, chunks: list[Chunk], top_n: int) -> list[Chunk]:
    """Re-score `chunks` against `query` and return the top_n (stable on ties)."""
    qv = embed(query)
    scored = [(cosine(qv, embed(c.text)), i, c) for i, c in enumerate(chunks)]
    scored.sort(key=lambda t: (-t[0], t[1]))
    return [c for _s, _i, c in scored[:top_n]]
