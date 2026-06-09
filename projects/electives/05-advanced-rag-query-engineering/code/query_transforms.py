"""query_transforms.py — [REFERENCE SOLUTION] verified copy (solns branch). Starter (NotImplementedError) on main."""
from __future__ import annotations

from config import Config, load_config
from rag_backend import DECOMPOSITIONS, HYDES, REWRITES, norm


def rewrite(query: str, *, cfg: Config | None = None) -> str:
    cfg = cfg or load_config()
    return REWRITES.get(norm(query), query)


def hyde(query: str, *, cfg: Config | None = None) -> str:
    cfg = cfg or load_config()
    return HYDES.get(norm(query), query)


def decompose(query: str, *, cfg: Config | None = None) -> list[str]:
    cfg = cfg or load_config()
    return DECOMPOSITIONS.get(norm(query), [query])
