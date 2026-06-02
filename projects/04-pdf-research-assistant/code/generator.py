"""generator.py — [learner] Milestones M3 + M4 — grounded generation with citations. The CORE of RAG.

Retrieval found the chunks; now you must make the LLM answer FROM them, not from its own memory — and
cite which chunk each claim came from. The trap is silent: if your grounding instruction is weak, the
model "helpfully" answers from parametric memory and ignores the context, and the answer still LOOKS
right (sources/papers/rag-paper.md). Two jobs:
  1. build_prompt — construct messages that (a) carry the retrieved chunks + their ids as context,
     (b) instruct "answer ONLY from the context", and (c) PERMIT refusal ("say you don't know").
  2. answer — call the model and return the text plus the chunk ids it cited (provenance).

PROVIDED: Answer dataclass, _CITE regex, main() demo.
LEARNER: build_prompt() (offline-testable) and answer() (needs a provider — behavioral).

Run:  python generator.py      (needs a chat provider: USE_OLLAMA=1 or a cloud key)
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from chunker import Chunk
from config import load_config

# Matches inline citations like "[c0]" or "[c12]" in the model's answer text.
_CITE = re.compile(r"\[(c\d+)\]")


@dataclass(frozen=True)
class Answer:
    """[provided] A grounded answer plus the chunk ids it cited."""
    text: str
    citations: list[str]   # chunk ids referenced in `text`, e.g. ["c0", "c2"]


def build_prompt(query: str, chunks: list[Chunk]) -> list[dict]:
    """[learner] Build the grounded chat messages: a system instruction + a user turn with context.

    Steps:
      1. Compose a SYSTEM message that pins three rules:
           - answer USING ONLY the provided context,
           - cite the chunk id(s) you used in square brackets, e.g. [c0],
           - if the answer is NOT in the context, say you don't know (refusal) — do not guess.
      2. Render the context block: each chunk as "[<id>] <text>" on its own line, so the model can
         see and cite the ids. (These ids came from chunker.py and flow through retriever.py.)
      3. Compose a USER message containing the context block and then the question.
      4. Return [{"role": "system", "content": ...}, {"role": "user", "content": ...}].

    Example (mirrors tests/test_generator.py::test_build_prompt_grounds_and_cites):
        chunks = [Chunk("c0", "Q3 revenue was 4.2M, up 8% YoY."),
                  Chunk("c1", "Opened a Berlin office in July.")]
        msgs = build_prompt("What was Q3 revenue?", chunks)
        msgs[0]["role"] == "system"            # grounding + refusal instruction
        "[c0]" in msgs[-1]["content"]          # chunk ids are present to cite
        "Q3 revenue was 4.2M" in msgs[-1]["content"]   # chunk text is in the prompt
        # the system text mentions answering only from context AND saying "don't know" when absent
    """
    system = (
        "You answer questions using ONLY the provided context. "
        "Cite the chunk id(s) you used in square brackets, e.g. [c0]. "
        "If the answer is not in the context, say you don't know — do not guess."
    )
    context_block = "\n".join(f"[{c.id}] {c.text}" for c in chunks)
    user = f"Context:\n{context_block}\n\nQuestion: {query}"
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def answer(query: str, chunks: list[Chunk]) -> Answer:
    """[learner] Call the LLM with the grounded prompt and return the answer text + cited chunk ids.

    Steps:
      1. messages = build_prompt(query, chunks)
      2. cfg = load_config(); call litellm.completion(model=cfg.model, messages=messages,
         temperature=cfg.temperature)  (temperature defaults to 0.0 — faithful, not creative).
      3. text = response.choices[0].message.content
      4. citations = the chunk ids found in `text` via _CITE (use _CITE.findall(text); dedupe, keep order).
      5. return Answer(text=text, citations=citations).

    Example (behavioral — needs a provider; mirrors the grounded contract):
        answer("What was Q3 revenue?", [Chunk("c0", "Q3 revenue was 4.2M, up 8% YoY.")])
        -> Answer(text="Q3 revenue was 4.2M [c0].", citations=["c0"])
        # off-document question -> text says it doesn't know, citations == []
    """
    import litellm

    messages = build_prompt(query, chunks)
    cfg = load_config()
    response = litellm.completion(model=cfg.model, messages=messages, temperature=cfg.temperature)
    text = response.choices[0].message.content
    citations: list[str] = []
    for cid in _CITE.findall(text):
        if cid not in citations:  # dedupe, keep first-seen order
            citations.append(cid)
    return Answer(text=text, citations=citations)


def main() -> None:
    from chunker import chunk_text
    from pdf_loader import SAMPLE_DOC
    from retriever import build_index, retrieve

    cfg = load_config()
    chunks = chunk_text(SAMPLE_DOC, chunk_size=cfg.chunk_size, overlap=cfg.chunk_overlap)
    col = build_index(chunks)
    hits = retrieve(col, "What was Q3 revenue?", k=cfg.top_k)
    ans = answer("What was Q3 revenue?", hits)
    print("Project 04 — Generator")
    print("answer   :", ans.text)
    print("citations:", ans.citations)


if __name__ == "__main__":
    main()
