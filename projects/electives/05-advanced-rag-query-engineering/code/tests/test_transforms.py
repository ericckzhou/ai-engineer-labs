"""[provided] Guiding tests for M1–M3. Fail with NotImplementedError until implemented."""
from query_transforms import decompose, hyde, rewrite

PARAPHRASE = "how do I get my money back?"
FACTUAL = "what year was the company founded?"
MULTIHOP = "Did any founder attend the same school as our chief technology officer?"


def test_rewrite_reformulates_known_query():
    rq = rewrite(PARAPHRASE)
    assert rq != PARAPHRASE
    assert "refund" in rq.lower()


def test_rewrite_falls_back_to_query():
    assert rewrite("an utterly unknown question") == "an utterly unknown question"


def test_hyde_returns_a_hypothetical_doc():
    h = hyde(PARAPHRASE)
    assert h and h != PARAPHRASE
    assert "refund" in h.lower() or "return" in h.lower()


def test_decompose_multihop_yields_subquestions():
    subs = decompose(MULTIHOP)
    assert isinstance(subs, list)
    assert len(subs) >= 2


def test_decompose_singlehop_is_identity():
    assert decompose(FACTUAL) == [FACTUAL]
