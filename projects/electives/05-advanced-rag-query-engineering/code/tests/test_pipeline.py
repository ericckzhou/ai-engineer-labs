"""[provided] Guiding tests for M4 (fusion + pipeline). Fail with NotImplementedError until done.

Asserts: rewrite rescues the paraphrase case the baseline misses; multi-hop decomposition fuses
both bridge chunks; fusion dedupes and respects top_n.
"""
import advanced_rag
from config import load_config

PARAPHRASE = "how do I get my money back?"
MULTIHOP = "Did any founder attend the same school as our chief technology officer?"


def _ids(res):
    return [c.id for c in res.contexts]


def test_baseline_misses_paraphrase():
    res = advanced_rag.answer(PARAPHRASE, transform="none")
    assert "c1" not in _ids(res), "the bare query should miss the refund chunk (that's why we rewrite)"


def test_rewrite_rescues_paraphrase():
    res = advanced_rag.answer(PARAPHRASE, transform="rewrite")
    assert "c1" in _ids(res), "rewriting the query should retrieve the refund chunk"


def test_decompose_fuses_multihop_bridge_chunks():
    res = advanced_rag.answer(MULTIHOP, transform="decompose")
    assert {"c5", "c6", "c7"}.issubset(set(_ids(res))), "decomposition must retrieve all bridge chunks"


def test_fusion_dedupes_and_respects_top_n():
    cfg = load_config()
    res = advanced_rag.answer(MULTIHOP, transform="decompose", cfg=cfg)
    ids = _ids(res)
    assert len(ids) == len(set(ids)), "fused contexts must be deduped (no repeated chunk ids)"
    assert len(ids) <= cfg.rerank_top_n, "fused contexts must respect rerank_top_n"
