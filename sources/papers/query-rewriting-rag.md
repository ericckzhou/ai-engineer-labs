# Query Rewriting for Retrieval-Augmented Large Language Models (Rewrite-Retrieve-Read)

**Type:** paper
**Authors:** Xinbei Ma, Yeyun Gong, Pengcheng He, Hai Zhao, Nan Duan
**Year:** 2023 (EMNLP 2023)
**arXiv:** 2305.14283 — https://arxiv.org/abs/2305.14283

> Primary source for **Elective 05 — Advanced RAG / Query Engineering** (query rewriting, M1).
> Faithful summary; arXiv PDF is canonical.

---

## Core idea

Standard RAG is **retrieve-then-read**: take the user's question as-is, retrieve, answer. But
"there is inevitably a **gap between the input text and the needed knowledge** in retrieval" — the
way a user phrases a question is often not the best *query* for the index. This paper inserts a
step: **Rewrite → Retrieve → Read.** Reformulate the question into a better retrieval query first.

## Approach

Two forms:
1. **LLM rewriter** — prompt an LLM to produce one (or several) search queries from the question.
2. **Trainable rewriter** — a small LM trained with **reinforcement learning from the reader's
   feedback** (the black-box LLM reader's answer quality is the reward signal).

## Result

Consistent improvement over retrieve-then-read across open-domain and multiple-choice QA — the
rewrite closes the question↔query gap before retrieval ever runs.

## Why it anchors the elective

It is the first and most general query transform: the user's words are an input to be *engineered*,
not a fixed query. It pairs with HyDE (rewrite the query text vs. embed a hypothetical answer) and
multi-hop decomposition (one query vs. several). And like all of them, it can drift — a rewrite can
wander off the user's intent — so it is measured against the eval, not assumed good.

## Known issues / cautions

- A rewrite can *change the meaning* (drift) and retrieve the wrong thing — gate on faithfulness.
- Costs a generation per query (Elective 03 cost lever interacts here).
- The reader's feedback is a noisy reward; a prompt-only rewriter is the cheap starting point.
