"""advanced_rag.py — [partial] Orchestrate the query-engineering pipeline.

PROVIDED: the result type, the entry-point signature, the effective-query selection (which calls
your transforms), and the read() call. LEARNER (TODOs, M4): the retrieve-per-(sub)query loop and
the FUSION — dedupe the union, then re-rank it (provided rerank) to top_n. See lesson §6.

FUSION = dedupe + re-rank, NOT concatenate-everything. Concatenation dilutes relevance and lowers
faithfulness.
"""
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
    """[provided] Map a transform to (retrieval_queries, rerank_query).

    - none:      retrieve with the raw query; rerank by the raw query.
    - rewrite:   retrieve with the rewrite; rerank by the rewrite.
    - hyde:      retrieve with the hypothetical doc; rerank by it.
    - decompose: retrieve with each sub-question; rerank by all sub-questions joined (so the bridge
                 chunks — which the raw query doesn't lexically match — score above distractors).
    """
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
    """Run: transform → retrieve(per query) → fuse(dedupe + re-rank) → read.

    TODO(M4):
      1. retrieval_queries, rerank_query = _effective_queries(query, transform, cfg=cfg)
      2. retrieve cfg.retrieve_k chunks for EACH retrieval query and take the UNION.
      3. FUSE: dedupe the union by chunk id, then rerank(rerank_query, union, cfg.rerank_top_n).
         (Do NOT just concatenate — dedupe + re-rank.)
      4. ans = read(query, fused); return RagResult(ans, fused, transform).
    """
    cfg = cfg or load_config()
    raise NotImplementedError("M4: retrieve per query, dedupe the union, rerank to top_n, then read.")
