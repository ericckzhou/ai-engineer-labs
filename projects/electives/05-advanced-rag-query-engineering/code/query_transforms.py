"""query_transforms.py — [learner] The query-transformation stage. Learning target (M1–M3).

Three transforms that change WHAT you retrieve with — applied BEFORE retrieval. Offline, read the
canned transform for a known query from rag_backend; if the query isn't in the fixture, fall back
to a sensible default (return the query unchanged / a single-element list). The live LLM version is
an extension. See source/lesson.agent.md §4–§6.
"""
from __future__ import annotations

from config import Config, load_config
from rag_backend import DECOMPOSITIONS, HYDES, REWRITES, norm


def rewrite(query: str, *, cfg: Config | None = None) -> str:
    """Reformulate the question into a better RETRIEVAL query (Rewrite-Retrieve-Read, M1).

    Offline: return rag_backend.REWRITES[norm(query)] if present, else the original query.

    Example:
        rewrite("how do I get my money back?")
            -> "refund policy return window receipt full refund"
        rewrite("an unknown question") -> "an unknown question"   # fallback: unchanged
    """
    cfg = cfg or load_config()
    raise NotImplementedError("M1: return the canned rewrite for norm(query), else the query unchanged.")


def hyde(query: str, *, cfg: Config | None = None) -> str:
    """Generate a HYPOTHETICAL ANSWER to embed instead of the query (HyDE, M2).

    Offline: return rag_backend.HYDES[norm(query)] if present, else the original query.
    (You embed THIS text, not the question — that's the whole idea. Never surface it as the answer.)

    Example:
        hyde("how do I get my money back?")
            -> "Returns are accepted within thirty days for a full refund if you keep the receipt."
    """
    cfg = cfg or load_config()
    raise NotImplementedError("M2: return the canned hypothetical doc for norm(query), else the query.")


def decompose(query: str, *, cfg: Config | None = None) -> list[str]:
    """Split a multi-hop question into sub-questions to retrieve separately (M3).

    Offline: return rag_backend.DECOMPOSITIONS[norm(query)] if present, else [query] (single-hop).

    Example:
        decompose("Did any founder attend the same school as our chief technology officer?")
            -> ["who is the CTO", "where did Dana Lee study", "which founder studied at Caltech"]
        decompose("what year was the company founded?") -> ["what year was the company founded?"]
    """
    cfg = cfg or load_config()
    raise NotImplementedError("M3: return the canned decomposition for norm(query), else [query].")
