# Project 4: PDF Research Assistant

## What We're Building

A RAG (Retrieval-Augmented Generation) system that ingests PDF documents and answers questions about them. Users upload a PDF; the system chunks it, embeds it, indexes it, retrieves relevant sections, and generates grounded answers with citations.

## Why We're Building It

RAG is the most commercially deployed AI architecture. It solves the fundamental problem of LLM knowledge cutoffs and hallucination — by grounding answers in real documents. Understanding RAG deeply opens up enterprise AI work, document intelligence, and research tools.

## Learning Objectives

- [ ] Implement the full RAG pipeline: ingest → chunk → embed → index → retrieve → generate
- [ ] Design and compare chunking strategies (fixed, semantic, recursive)
- [ ] Detect hallucination by checking answer faithfulness to retrieved context
- [ ] Build a citation system that traces answers back to source passages
- [ ] Evaluate RAG quality with faithfulness, relevance, and groundedness metrics
- [ ] Identify the 5 failure modes of RAG systems

## Key Concepts

RAG, chunking, document parsing, semantic retrieval, prompt stuffing, faithfulness, groundedness, hallucination detection, citations

## Core Engineering Problem

**Problem:** LLMs hallucinate when they don't know something. How do you make an LLM answer only from real documents and tell you when it can't?

## Time Estimate

**Total:** 10–15 hours

## Startup Lens

Every enterprise AI product either is RAG or contains RAG. Legal research, medical documentation, financial analysis, support automation — all RAG. Getting retrieval quality right is the difference between a demo and a shipped product.

## Key Files

```
code/
  pdf_parser.py         — Extract text from PDFs
  chunker.py            — Chunking strategies
  indexer.py            — Embed and store chunks
  retriever.py          — Query retrieval
  generator.py          — Answer generation with citations
  faithfulness.py       — Hallucination detection
  evaluate.py           — RAG evaluation harness
  requirements.txt
  README.md
```
