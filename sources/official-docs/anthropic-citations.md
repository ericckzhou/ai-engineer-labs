# Anthropic Citations (Messages API)

**Type:** official documentation
**Tier:** 1 (Official Docs)
**Author(s):** Anthropic
**Date:** accessed 2026-06-01
**URL:** https://docs.anthropic.com/en/docs/build-with-claude/citations
**Accessed:** 2026-06-01

## Why This Source Matters

RAG's promise is not just "answer from documents" but "answer from documents *and show me where*." Project 04 builds a citation system that traces each claim back to the source passage. This doc is the primary source for how a production API does exactly that — mapping spans of the answer to exact character/page/block locations in the source documents — and is the model for the (provider-agnostic) citation contract the learner builds. It grounds the lesson's citations section and the "answers must be verifiable" stake.

## Key Claims

### What citations do
- Claude "is capable of providing detailed citations when answering questions about documents, helping you track and verify information sources in responses."
- Each answer text block "can contain a claim that Claude is making and a list of citations that support the claim." Citations "reference specific locations in source documents."

### How it works (three steps)
1. **Provide documents, enable citations.** Attach documents (plain text, PDF, or custom content) with `citations.enabled = true`.
2. **Documents get chunked.** "Document contents are 'chunked' in order to define the minimum granularity of possible citations." Plain text and PDFs are "chunked into sentences"; custom content blocks "are used as-is and no further chunking is done." (Note: the *citation* granularity is sentence-level chunking — distinct from, but conceptually the same operation as, the *retrieval* chunking in `sources/articles/chunking-strategies.md`.)
3. **Claude returns a cited response.** Answer is split into multiple text blocks; cited blocks carry a `citations` list pointing into the source.

### Citation format — answer span → source location
- Plain text → `char_location` with `start_char_index` / `end_char_index` (0-indexed, exclusive end).
- PDF → `page_location` with `start_page_number` / `end_page_number` (1-indexed, exclusive end).
- Custom content → `content_block_location` with `start_block_index` / `end_block_index` (0-indexed).
- Each citation carries `cited_text` ("The exact text being cited") and a `document_index` (0-indexed across all documents in the request).
- `cited_text` "is provided for convenience and does not count towards output tokens" — and "is guaranteed to contain valid pointers to the provided documents."

### Citable vs. non-citable content
- Only text in a document's `source` "can be cited from." Optional `title` and `context` fields "will be passed to the model but not used towards cited content" — `context` is a place for document metadata.

### Why the feature beats prompt-only "please quote the source"
- "Better citation reliability: ... citations are guaranteed to contain valid pointers to the provided documents." (Prompt-asked quotes can be subtly wrong or fabricated.)
- "Improved citation quality: ... significantly more likely to cite the most relevant quotes ... as compared to purely prompt-based approaches."

## Relevant To

- concepts: [citations, grounding, provenance, attribution, hallucination-detection, document-qa, verifiability]
- projects: [04-pdf-research-assistant, 07-ai-evaluation-framework]

## Notes

- **Two kinds of "chunking" live in a RAG system and learners conflate them.** (1) *Retrieval chunking* — how you split a PDF into vectors for the vector DB (`sources/articles/chunking-strategies.md`). (2) *Citation chunking* — the sentence-level granularity at which an answer span maps back to source text (this doc). Project 04 uses the same chunk ids for both: retrieve a chunk, then cite the chunk it came from.
- **The portable lesson** (provider-agnostic, since the lab defaults to Groq/Ollama via LiteLLM): a citation is a pointer from a span of the answer to a `(document, chunk/char/page range, exact quoted text)`. The learner builds this by keeping each retrieved chunk's id/source and having the generator attach the supporting chunk id to each claim.
- **Caveat learners hit:** citations are incompatible with strict Structured Outputs in this API, because "citations require interleaving citation blocks with text output." If you force a rigid JSON schema you lose inline citations — a real design tension.
- Pairs with `sources/papers/ragas.md`: citations make faithfulness *checkable* — if a claim cites chunk 7, you can verify the claim against chunk 7's text.
