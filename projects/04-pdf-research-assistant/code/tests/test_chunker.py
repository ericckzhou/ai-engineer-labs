"""[provided] Guiding tests for Milestone M1 — chunker.chunk_text(). Fully OFFLINE (pure string logic).

Fails (NotImplementedError) until chunk_text is implemented. The docstring example in chunker.py
mirrors test_chunk_overlap exactly. Run: python -m pytest tests/test_chunker.py
"""
import chunker


def test_chunk_overlap():
    # 10 tokens, window 4, step = 4 - 2 = 2 -> starts at 0,2,4,6 -> 4 chunks, each overlapping the last by 2.
    chunks = chunker.chunk_text("A B C D E F G H I J", chunk_size=4, overlap=2)
    assert [c.text for c in chunks] == ["A B C D", "C D E F", "E F G H", "G H I J"]


def test_chunk_ids_are_stable_and_ordered():
    chunks = chunker.chunk_text("A B C D E F G H I J", chunk_size=4, overlap=2)
    assert [c.id for c in chunks] == ["c0", "c1", "c2", "c3"]


def test_chunk_carries_source():
    chunks = chunker.chunk_text("one two three four", chunk_size=2, overlap=0, source="page 1")
    assert all(c.source == "page 1" for c in chunks)


def test_chunk_empty_text_is_empty():
    assert chunker.chunk_text("", chunk_size=4, overlap=2) == []


def test_no_redundant_tail_chunk():
    # The last window reaches the end; there must be no extra chunk made only of overlap tokens.
    chunks = chunker.chunk_text("A B C D E F G H I J", chunk_size=4, overlap=2)
    assert len(chunks) == 4
