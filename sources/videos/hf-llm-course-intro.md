# Hugging Face LLM Course — Introduction

**Type:** video / course (educational)
**Tier:** 4 (Educational)
**Author(s):** Hugging Face (Abubakar Abid, Ben Burtenshaw, Lewis Tunstall, Leandro von Werra, et al.)
**Date:** Accessed 2026-06-01
**URL:** https://huggingface.co/learn/llm-course/chapter1/1
**Accessed:** 2026-06-01

## Why This Source Matters

A free, widely used educational source that frames LLMs within the broader NLP field. Useful for the ELI-Engineer framing in Project 1: it cleanly distinguishes NLP (the field) from LLMs (a powerful subset) and names the model families a learner will encounter. Tier 4 — it explains and points to primary sources rather than being authoritative itself.

## Key Claims

- **NLP** is the broad field of enabling computers to understand, interpret, and generate human language (sentiment analysis, NER, translation, etc.).
- **LLMs** are a subset of NLP models characterized by massive size, extensive training data, and the ability to perform many language tasks with minimal task-specific training. Llama, GPT, and Claude are cited examples.
- Understanding NLP foundations remains important for working effectively with LLMs.
- The course teaches the `pipeline()` abstraction, the Transformer architecture, and the distinction between encoder, decoder, and encoder-decoder architectures.
- Released under Apache 2.0; assumes good Python knowledge.

## Relevant To

- concepts: [large-language-model, nlp, transformer, text-generation]
- projects: [01-ai-chatbot, 02-token-embedding-explorer]

## Notes

- Use for conceptual framing only. For the concrete API contract a chatbot depends on, cite the Tier-1 Anthropic/LiteLLM docs instead.
- Chapters 1–4 cover Transformers fundamentals; later chapters cover tokenizers, RAG, fine-tuning — relevant to Projects 2–4.
