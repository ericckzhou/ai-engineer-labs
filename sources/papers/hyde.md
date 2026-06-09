# HyDE: Precise Zero-Shot Dense Retrieval without Relevance Labels

**Type:** paper
**Authors:** Luyu Gao, Xueguang Ma, Jimmy Lin, Jamie Callan (CMU / Waterloo)
**Year:** 2022
**arXiv:** 2212.10496 — https://arxiv.org/abs/2212.10496

> Primary source for **Elective 05 — Advanced RAG / Query Engineering** (the HyDE transform, M2).
> Faithful summary; arXiv PDF is canonical.

---

## Core idea

A bare query and a relevant document live in *different* regions of embedding space — a question
and its answer don't look alike. HyDE bridges that gap by embedding a **hypothetical answer**
instead of the question:

1. **Generate** — zero-shot instruct an LLM to write a *hypothetical document* that would answer
   the query (it may contain factual errors — that's fine).
2. **Embed that document** (not the query) with an unsupervised contrastive encoder (e.g.
   Contriever).
3. **Retrieve** the real documents nearest that embedding.

## Why it works

The hypothetical document "looks like" a relevant document, so its embedding lands in the
neighborhood of genuinely relevant corpus documents — closer than the bare query would. The
encoder's **dense bottleneck filters out the hallucinated specifics**: the generated doc grounds
the *shape* of a good answer, and the nearest real documents supply the *facts*. No relevance
labels, no fine-tuning.

## Result

HyDE substantially beats unsupervised dense retrievers and approaches fine-tuned systems, across
languages and tasks — entirely zero-shot.

## Why it anchors the elective

It is a query-transformation lever: change *what you embed* to fix retrieval. But it is not free —
it costs a generation per query and can *hurt* on short factual lookups (the hypothetical adds
noise). That is exactly why the elective measures each transform against the eval rather than
assuming it helps.

## Known issues / cautions

- Costs an extra LLM generation per query (latency/cost) — connects to Elective 03.
- Can hurt on queries where the bare term match was already good; measure, don't assume.
- The hypothetical doc's hallucinations are tolerated only because the encoder + real corpus
  filter them — do not surface the hypothetical as an answer.
