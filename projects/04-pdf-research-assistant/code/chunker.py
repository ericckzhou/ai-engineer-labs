"""chunker.py — [learner] Milestone M1 — split document text into overlapping, id-tagged chunks.

Chunking is the upstream gate of RAG. You can't embed a whole PDF as one vector (too big for the
model's context window, and too diffuse to match a question), so you split it first. Chunk SIZE trades
precision (small = specific meaning) against context (large = broader themes), and OVERLAP keeps a fact
that straddles a boundary from being lost by both chunks. (sources/articles/chunking-strategies.md)

Every chunk carries a stable `id` and its `source` — those are what a citation points to (M4) and what
the faithfulness check verifies against (M5). Lose them and you can't cite or verify.

PROVIDED: the Chunk dataclass, main() demo.
LEARNER: chunk_text() — fixed-size windows with overlap. Pure logic; tests/test_chunker.py runs offline.

Run:  python chunker.py
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    """[provided] One retrievable passage. `id` is cited and verified against; keep it stable."""
    id: str
    text: str
    source: str = "doc"   # where it came from (e.g. "page 3", a filename) — carried into citations
    start: int = 0        # token index where this chunk begins (for char/page citations later)


def chunk_text(
    text: str,
    chunk_size: int,
    overlap: int,
    source: str = "doc",
) -> list[Chunk]:
    """[learner] Split `text` into fixed-size, overlapping Chunks (split on whitespace tokens).

    Steps:
      1. tokens = text.split()            (whitespace tokenization is fine for this lab)
      2. step = chunk_size - overlap      (must be > 0 — guard against overlap >= chunk_size)
      3. Slide a window of `chunk_size` tokens forward by `step`:
         window i = tokens[start : start + chunk_size], joined back with spaces.
         Give each chunk a stable id "c0", "c1", ... and record its `start` token index + `source`.
      4. Stop after the window that reaches the end (start + chunk_size >= len(tokens)) so you don't
         emit a redundant tail chunk. Empty text -> [].

    Why overlap: with overlap=2, "...D E F..." appears in both the chunk ending at E-F and the next
    one starting at E-F, so a fact on the seam survives in at least one chunk.

    Example (mirrors tests/test_chunker.py::test_chunk_overlap — 10 tokens, size 4, overlap 2):
        chunk_text("A B C D E F G H I J", chunk_size=4, overlap=2)
        -> [Chunk("c0","A B C D",...), Chunk("c1","C D E F",...),
            Chunk("c2","E F G H",...), Chunk("c3","G H I J",...)]
        # step = 2; adjacent chunks share 2 tokens; 4 chunks, no redundant tail
    """
    tokens = text.split()
    if not tokens:
        return []
    step = chunk_size - overlap
    if step <= 0:
        raise ValueError("overlap must be smaller than chunk_size (step would be <= 0)")

    chunks: list[Chunk] = []
    start = 0
    while True:
        window = tokens[start : start + chunk_size]
        chunks.append(
            Chunk(id=f"c{len(chunks)}", text=" ".join(window), source=source, start=start)
        )
        if start + chunk_size >= len(tokens):
            break  # this window reached the end — no redundant tail chunk
        start += step
    return chunks


def main() -> None:
    demo = "A B C D E F G H I J"
    chunks = chunk_text(demo, chunk_size=4, overlap=2)
    print("Project 04 — Chunker")
    for c in chunks:
        print(f"  {c.id}  [{c.source}]  {c.text!r}")


if __name__ == "__main__":
    main()
