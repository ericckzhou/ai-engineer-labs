"""advanced_rag.py — [REFERENCE SOLUTION] verified copy (solns branch). Starter (TODOs) on main."""
from __future__ import annotations

from dataclasses import dataclass, field

from config import Config, load_config
from query_transforms import decompose, hyde, rewrite
from rag_backend import Chunk, read, retrieve
from rerank import rerank


@dataclass
class RagResult:
    answer: str
    contexts: list[Chunk] = field(default_factory=list)
    transform: str = "none"


def _effective_queries(query: str, transform: str, *, cfg: Config) -> tuple[list[str], str]:
    if transform == "rewrite":
        rq = rewrite(query, cfg=cfg)
        return [rq], rq
    if transform == "hyde":
        h = hyde(query, cfg=cfg)
        return [h], h
    if transform == "decompose":
        subs = decompose(query, cfg=cfg)
        return subs, " ".join(subs)
    return [query], query


def answer(query: str, *, transform: str = "none", cfg: Config | None = None) -> RagResult:
    cfg = cfg or load_config()
    retrieval_queries, rerank_query = _effective_queries(query, transform, cfg=cfg)

    seen: set[str] = set()
    union: list[Chunk] = []
    for q in retrieval_queries:
        for c in retrieve(q, cfg.retrieve_k):
            if c.id not in seen:           # FUSION: dedupe the union
                seen.add(c.id)
                union.append(c)

    fused = rerank(rerank_query, union, cfg.rerank_top_n)   # FUSION: re-rank (provided P03)
    return RagResult(read(query, fused), fused, transform)
