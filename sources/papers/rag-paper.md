# Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

**Type:** paper
**Tier:** 2 (Foundational Paper)
**Author(s):** Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela
**Date:** 2020 (submitted 2020-05-22; NeurIPS 2020)
**URL:** https://arxiv.org/abs/2005.11401
**Accessed:** 2026-06-01

## Why This Source Matters

This is the paper that named **RAG** and is the primary source for the architecture behind Project 04. It frames the exact problem the PDF research assistant solves: a language model that "stores factual knowledge in its parameters" cannot *precisely* access or update that knowledge, and "providing provenance for [its] decisions and updating [its] world knowledge remain open research problems." RAG's answer — couple a generator with a retrieved, non-parametric knowledge store — is the design every production document-QA system still uses. It grounds the lesson's motivation, the parametric-vs-non-parametric mental model, and the "answers must be grounded and attributable" claim.

## Key Claims

### The problem with parametric-only models
- LLMs "store factual knowledge in their parameters" but "their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures."
- Two open problems with parametric-only memory: "providing provenance for their decisions and updating their world knowledge." (You cannot cite *why* a parametric model said something, and you cannot edit a fact without retraining.)

### What RAG is
- RAG models "combine pre-trained parametric and non-parametric memory for language generation."
- **Parametric memory:** a pre-trained seq2seq model (BART) — the generator's learned weights.
- **Non-parametric memory:** "a dense vector index of Wikipedia, accessed with a pre-trained neural retriever" (DPR). This is the swappable, updatable knowledge store — in Project 04, *your* indexed PDF chunks.
- The retriever finds relevant passages; the generator conditions on the query **and** those passages to produce the answer.

### Two formulations
- **RAG-Sequence:** "conditions on the same retrieved passages across the whole generated sequence."
- **RAG-Token:** "can use different passages per token."
- (Project 04 uses the practical modern form: retrieve top-k chunks once, stuff them into the prompt, generate one grounded answer — closest in spirit to RAG-Sequence.)

### The payoff
- Sets "the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures."
- "RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline." Grounding in retrieved text reduces hallucination and makes answers attributable.

## Relevant To

- concepts: [retrieval-augmented-generation, rag, parametric-vs-non-parametric-memory, grounding, provenance, hallucination, knowledge-intensive-qa]
- projects: [04-pdf-research-assistant, 05-personal-memory-system, 07-ai-evaluation-framework]

## Notes

- **The modern "RAG" most engineers build is a simplification of this paper:** retrieve top-k chunks from a vector DB (Project 03), concatenate them into the prompt as context, and ask the LLM to answer *only* from that context with citations. The end-to-end differentiable training in the paper is usually dropped; the retrieve-then-generate skeleton is kept.
- **Why it beats a bigger model / longer context:** non-parametric memory is *updatable* (re-index, don't retrain) and *attributable* (you know which passage produced the answer). Those are the two open problems the abstract names.
- The retriever here is exactly the bi-encoder + dense vector index pattern from `sources/papers/sentence-bert.md` and `sources/official-docs/chromadb.md`. RAG = Project 03's retrieval feeding an LLM.
