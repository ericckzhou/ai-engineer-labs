# Elective 05 — Advanced RAG / Query Engineering (code)

Add a **query-transformation stage** (rewrite, HyDE, multi-hop decompose) in front of Project 04's
retrieval, and prove **per transform** which ones help. The retriever, corpus, re-ranker (P03), and
faithfulness eval are provided; **you build `query_transforms.py` and the fusion in
`advanced_rag.py`.**

> Brief: `../source/project.md` · Lesson: `../source/lesson.agent.md` · Rubric: `../source/rubric.md`.
> Do `../UNDERSTANDING.md` **before** coding.

## Setup (offline — no API key)

```bash
python -m venv .venv && .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest
```

`test_config.py` passes; the rest fail with `NotImplementedError` until you implement, in order:

| Milestone | File / symbol | Tests |
|-----------|---------------|-------|
| M1 rewrite | `query_transforms.rewrite` | `tests/test_transforms.py` |
| M2 HyDE | `query_transforms.hyde` | `tests/test_transforms.py` |
| M3 decompose | `query_transforms.decompose` | `tests/test_transforms.py` |
| M4 fusion/pipeline | `advanced_rag.answer` | `tests/test_pipeline.py` |

## Prove which transform helped

```bash
python evaluate_rag.py
```

Reports **per transform**: retrieval-hit, context-precision, answer-relevance. Rewrite should
rescue the paraphrase case; decompose the multi-hop; factual needs neither.

## File roles

| File | Role |
|------|------|
| `config.py` | provided — retrieval params |
| `rag_backend.py` | reference — corpus + retriever + reader + canned transforms |
| `rerank.py` | provided — P03 re-ranker (use it for fusion; don't rebuild) |
| `query_transforms.py` | **learner** — rewrite / hyde / decompose |
| `advanced_rag.py` | partial — fusion + pipeline (TODOs) |
| `eval_set.jsonl` | provided — frozen QA set |
| `evaluate_rag.py` | provided — per-transform scorer |
| `tests/` | provided |

## The rules that matter most

**Fusion = dedupe + re-rank, not concatenate.** **Not every transform helps** — HyDE can hurt
factual queries; the eval is the referee. **Faithfulness, not raw recall, is the gate.**
