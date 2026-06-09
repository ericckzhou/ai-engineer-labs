# Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection

**Type:** paper
**Tier:** 2 (Foundational Paper)
**URL:** https://arxiv.org/abs/2310.11511
**Accessed:** 2026-06-09
**Authors:** Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, Hannaneh Hajishirzi (UW / AI2 / IBM)
**Year:** 2023
**arXiv:** 2310.11511 — https://arxiv.org/abs/2310.11511

> Primary source for **Elective 05 — Advanced RAG / Query Engineering** (the retrieve-or-not gate +
> self-critique; the M5/extension). Faithful summary; arXiv PDF is canonical.

---

## Core idea

Standard RAG **always** retrieves a fixed number of passages and stuffs them in — even when the
query needs no retrieval, and regardless of whether the passages are any good. Self-RAG makes
retrieval **adaptive and self-critiqued** using special **reflection tokens** that let the model:

1. **Retrieve-or-not** — decide *whether* external knowledge is needed before fetching anything
   (skip retrieval on queries that don't need it).
2. **Critique relevance** — judge whether each retrieved passage is actually relevant.
3. **Critique support** — judge whether the generated answer is *supported* by the passages.

## Why it beats always-retrieve RAG

Indiscriminately adding a fixed number of passages "diminishes LM versatility or can lead to
unhelpful response generation." Selective, critiqued retrieval keeps factuality up *and* avoids
the degradation of forcing irrelevant context into the answer. It also makes behavior controllable
at inference (tune how aggressively to retrieve).

## Result

7B/13B Self-RAG models outperformed ChatGPT and retrieval-augmented Llama2-chat on multiple
benchmarks.

## Why This Source Matters

It is the capstone idea of query engineering: the most advanced move is sometimes **not to
retrieve**, and always to **critique what you retrieved** rather than trust it. It reframes the
faithfulness metric (Project 04 / RAGAS) as an *inline* decision, not just a post-hoc score —
"is this supported?" asked during generation. In this elective it is the extension: a
retrieve-or-not gate plus a relevance/support check over the transformed pipeline.

## Key Claims

- Standard RAG always retrieves a fixed number of passages and stuffs them in; Self-RAG makes retrieval adaptive and self-critiqued via special reflection tokens.
- Three decisions: retrieve-or-not (skip retrieval when unneeded), critique each passage's relevance, and critique whether the answer is *supported* by the passages.
- Selective, critiqued retrieval keeps factuality up and avoids degradation from forcing irrelevant context; 7B/13B Self-RAG models beat ChatGPT and retrieval-augmented Llama2-chat on several benchmarks.

## Relevant To

- Elective 05 — Advanced RAG / Query Engineering (retrieve-or-not gate + self-critique, M5/extension).
- Related: Project 04 / RAGAS faithfulness, reframed as an *inline* "is this supported?" decision; Elective 03 (the critique is an extra LLM cost).

## Known issues / cautions

- Full Self-RAG trains reflection tokens; the elective approximates the *behavior* (a retrieve-or-
  not gate + a relevance/support critique) with prompting, not training.
- The critique is itself an LLM judgment — fallible, and a cost (Elective 03).
- "Don't retrieve" is a real option, but a wrong skip loses grounding — measure on the eval.
