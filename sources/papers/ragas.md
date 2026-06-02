# RAGAS: Automated Evaluation of Retrieval Augmented Generation

**Type:** paper
**Tier:** 2 (Foundational Paper)
**Author(s):** Shahul Es, Jithin James, Luis Espinosa-Anke, Steven Schockaert
**Date:** 2023 (submitted 2023-09-26)
**URL:** https://arxiv.org/abs/2309.15217
**Accessed:** 2026-06-01

## Why This Source Matters

A RAG system has two places it can fail — retrieval (wrong context) and generation (right context, wrong answer) — and "it seemed to work" is not an evaluation. RAGAS is the primary source for the **reference-free** metrics that turn RAG quality into numbers, especially **faithfulness**, the metric that detects hallucination by checking whether the answer is actually grounded in the retrieved context. It grounds Project 04's evaluation milestone and its hallucination-detection component. "Reference-free" matters: you can score a RAG answer without a human-written gold answer, using the LLM itself as the judge.

## Key Claims

### The framework
- RAGAS is "a framework for reference-free evaluation of Retrieval Augmented Generation (RAG) pipelines" — "a suite of metrics which can be used to evaluate these different dimensions without having to rely on ground truth human annotations."
- It scores three dimensions, mapping to the two failure surfaces: generation faithfulness, answer relevance, and retrieval context relevance.

### (1) Faithfulness — is the answer grounded in the context?
- Procedure: an LLM extracts "a set of statements" from the answer, decomposing it into "shorter and more focused assertions." For each statement, a verification step decides whether it "can be inferred from the context."
- **Formula:** `F = |V| / |S|` — supported statements over total statements. Range [0, 1].
- **This is the hallucination metric.** A claim in the answer that the retrieved context does not support is, by definition, ungrounded — a hallucination. Low faithfulness = the model invented something.

### (2) Answer Relevance — does the answer address the question?
- Procedure: prompt the LLM to "generate n potential questions" from the answer, embed them, and "calculate the similarity `sim(q, qi)` with the original question q, as the cosine between the corresponding embeddings."
- **Formula:** `AR = (1/n) Σ sim(q, qi)`. A faithful but evasive/off-topic answer scores low here.

### (3) Context Relevance — did retrieval return useful context?
- Procedure: the LLM "extracts a subset of sentences" from the retrieved context "that are crucial to answer q."
- **Formula:** `CR = (# extracted sentences) / (total sentences in context)`. Low CR means retrieval dumped in mostly noise — a chunking/retrieval problem, not a generation one.

## Relevant To

- concepts: [faithfulness, groundedness, hallucination-detection, answer-relevance, context-relevance, rag-evaluation, llm-as-judge, reference-free-evaluation]
- projects: [04-pdf-research-assistant, 07-ai-evaluation-framework]

## Notes

- **Faithfulness vs. answer relevance separate the two ways RAG fails.** Faithfulness asks "is the answer supported by the context?" (hallucination). Answer relevance asks "does the answer address the question?" (usefulness). An answer can be perfectly faithful and useless, or fluent and entirely hallucinated.
- **Context relevance is a retrieval/chunking diagnostic.** If faithfulness is high but answers are weak, look at context relevance — bad chunking or bad retrieval starves the generator.
- The faithfulness check (extract claims → verify each against context) is implementable as a second LLM call. In Project 04 the learner builds a simplified version: decompose the answer into claims and ask the model whether each is entailed by the retrieved chunks.
- Uses the LLM as the judge — connects to `sources/papers/sentence-bert.md` (embeddings for answer-relevance similarity) and forward to Project 07's evaluation framework.
