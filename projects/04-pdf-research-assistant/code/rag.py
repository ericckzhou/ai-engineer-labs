"""rag.py — [provided] The end-to-end RAG pipeline that wires the milestones together.

This orchestrator is provided so you can see the whole flow at once: it calls the functions YOU
implement (chunk_text, build_prompt/answer, check_faithfulness) and the retriever you reused from
Project 03. It will raise NotImplementedError until you implement those — that is the point: fill in the
learner modules milestone by milestone and watch this come alive.

Pipeline:   ingest -> CHUNK -> embed+index -> retrieve -> GENERATE(grounded+cite) -> VERIFY(faithfulness)
            (chunker.py)        (retriever.py — provided)   (generator.py)            (faithfulness.py)

Run:  python rag.py "What was Q3 revenue?"      (needs a provider: USE_OLLAMA=1 or a cloud key)
"""
from __future__ import annotations

import sys

from chunker import chunk_text
from config import load_config
from faithfulness import check_faithfulness
from generator import answer
from pdf_loader import SAMPLE_DOC, load_pdf
from retriever import build_index, retrieve


def run(question: str, document: str) -> None:
    cfg = load_config()
    # 1. CHUNK (M1)
    chunks = chunk_text(document, chunk_size=cfg.chunk_size, overlap=cfg.chunk_overlap)
    # 2. INDEX + 3. RETRIEVE (M2 — provided, Project 03)
    col = build_index(chunks)
    hits = retrieve(col, question, k=cfg.top_k)
    # 4. GENERATE grounded answer with citations (M3/M4)
    ans = answer(question, hits)
    # 5. VERIFY faithfulness (M5)
    report = check_faithfulness(ans.text, hits)

    print(f"Project 04 — PDF Research Assistant   (model: {cfg.model})")
    print(f"Q: {question}")
    print(f"A: {ans.text}")
    print(f"citations : {ans.citations}")
    print(f"faithfulness: {report.score:.3f}  ({sum(report.verdicts)}/{len(report.verdicts)} claims grounded)")


def main() -> None:
    question = sys.argv[1] if len(sys.argv) > 1 else "What was Q3 revenue?"
    # Use a real PDF if a path is given as the 2nd arg; otherwise the built-in sample document.
    document = load_pdf(sys.argv[2]) if len(sys.argv) > 2 else SAMPLE_DOC
    run(question, document)


if __name__ == "__main__":
    main()
