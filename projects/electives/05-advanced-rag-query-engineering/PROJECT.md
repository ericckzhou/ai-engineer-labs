# Elective 05 — Advanced RAG / Query Engineering

> **Production & Hardening track** (off the 1–9 spine; after the P09 capstone) — a depth elective
> on retrieval. Teaching: [source/lesson.agent.md](source/lesson.agent.md) · Contracts:
> [source/project.md](source/project.md) · Human lesson: [rendered/lesson.html](rendered/lesson.html).

## What you're building

Add a **query-transformation stage** in front of Project 04's retrieval — **rewriting**, **HyDE**,
and **multi-hop decomposition + fusion** — and prove on P04's **faithfulness eval** which transforms
help (and which don't). The retriever, corpus, re-ranker (P03), and eval are provided; you build the
**query stage** and the **fusion**.

## Why it matters

Naive RAG treats the user's question as a perfect query. It isn't — paraphrases miss and multi-hop
questions need more than one retrieval. The query is a thing you engineer. But fancier isn't free or
always better, so every transform is measured against the eval.

## The rules that matter most

**Fusion = dedupe + re-rank, not concatenate.** **Not every transform helps** (HyDE can hurt
factual queries). **Faithfulness, not raw recall, is the gate.** **Don't rebuild re-ranking** — it's
P03, provided.

## Prerequisites
Project 04 (RAG + faithfulness eval), Project 03 (re-ranking — provided), Project 02 (embeddings).

## Milestones
1. M1 rewrite · 2. M2 HyDE · 3. M3 decompose · 4. M4 fuse + orchestrate · 5. M5 prove per-transform ·
Extension: Self-RAG retrieve-or-not + critique, hybrid BM25+dense, GraphRAG.

## How to start
1. Read the lesson. 2. Complete [UNDERSTANDING.md](UNDERSTANDING.md) before coding. 3.
`cd code && pip install -r requirements.txt && python -m pytest` — implement until green. 4.
`python code/evaluate_rag.py` — read faithfulness per transform. 5. Reflect: FAILURE_ANALYSIS →
EVALUATION → STARCALLOS_REFLECTION.

## File roles (code/)
`config.py` provided · `rag_backend.py` reference · `rerank.py` provided · **`query_transforms.py`
learner** · `advanced_rag.py` partial · `eval_set.jsonl` provided · `evaluate_rag.py` provided ·
`tests/` provided.
