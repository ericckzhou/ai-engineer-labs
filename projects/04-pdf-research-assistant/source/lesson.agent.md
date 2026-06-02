# Lesson 04: PDF Research Assistant (RAG)
<!-- lesson.agent.md — Agent-optimized canonical source. Do not simplify; this is the truth layer. -->

## Metadata

| Field | Value |
|-------|-------|
| Project | 04-pdf-research-assistant |
| Core Concepts | RAG pipeline, chunking, grounded generation, citations/provenance, faithfulness & hallucination detection, refusal |
| Prerequisites | See PROJECT.md (Project 03 complete: build + query a Chroma index; Project 01: chat completions via LiteLLM) |
| Difficulty | Intermediate |
| Estimated Time | See PROJECT.md (10–15 hours total) |
| Last Updated | 2026-06-01 |

---

## Learning Objectives

By completing this lesson, the learner will be able to:

1. Explain **RAG** as combining **parametric** memory (the LLM's weights) with **non-parametric** memory (a retrieved, updatable document store), and why that beats a bigger model for document QA (source: `sources/papers/rag-paper.md`).
2. Implement the full pipeline: **ingest → chunk → embed → index → retrieve → generate → cite → verify**.
3. Design a **chunking** strategy and reason about the **size tradeoff** (small = precise but context-poor; large = rich but imprecise), including **overlap** (source: `sources/articles/chunking-strategies.md`).
4. Construct a **grounded-generation prompt** that answers *only* from the retrieved context and **refuses** ("I don't know") when the answer is not present.
5. Build a **citation** system that traces each claim in the answer back to the source chunk it came from (source: `sources/official-docs/anthropic-citations.md`).
6. Detect **hallucination** by measuring **faithfulness** — decompose the answer into claims and verify each against the retrieved context: `F = |supported| / |total|` (source: `sources/papers/ragas.md`).
7. Name and reproduce the major **failure modes** of RAG (retrieval miss, bad chunking, lost-in-context, confident hallucination, no-refusal) and tell *which stage* caused each.

---

## Prerequisite Knowledge Check

Before beginning, the learner should be able to answer:

1. From Project 03: how do you build a persistent Chroma collection and retrieve the top-k nearest chunks for a query? (RAG's "R" is exactly this.)
2. From Project 01: how do you send a chat completion through LiteLLM with a system + user message and read the text back?
3. Why must the corpus and the query be embedded with the **same** model? (Carries straight into chunk indexing here.)

If the learner cannot retrieve top-k from a vector DB (Project 03), complete that first — Project 04 *is* that retrieval feeding an LLM.

---

## Core Concepts

| Concept | Definition | Why It Matters |
|---------|-----------|----------------|
| RAG | Retrieval-Augmented Generation: condition an LLM's answer on passages fetched from an external store at query time | Combines "parametric and non-parametric memory for language generation"; makes knowledge **updatable** and **attributable** (source: `sources/papers/rag-paper.md`) |
| Parametric vs non-parametric memory | Parametric = facts baked into weights; non-parametric = a swappable document index | You update non-parametric memory by re-indexing, not retraining — and you can cite it (source: `sources/papers/rag-paper.md`) |
| Chunking | Splitting a document into smaller passages before embedding | Embedding a whole PDF as one vector is too diffuse to match a question; chunk size sets the precision/context tradeoff (source: `sources/articles/chunking-strategies.md`) |
| Chunk overlap | Repeating a slice of text across adjacent chunks | Stops a sentence split across a boundary from being lost by both chunks (source: `sources/articles/chunking-strategies.md`) |
| Grounding / context stuffing | Putting retrieved chunks into the prompt and instructing the model to answer only from them | The mechanism that turns "the model's opinion" into "what the document says" (source: `sources/papers/rag-paper.md`) |
| Refusal | Answering "I don't know" when the context doesn't contain the answer | A RAG system that never refuses will confidently hallucinate off-document questions |
| Citation / provenance | A pointer from a span of the answer to the source chunk that supports it | Lets a human verify the claim; "track and verify information sources in responses" (source: `sources/official-docs/anthropic-citations.md`) |
| Faithfulness | Fraction of the answer's claims that the retrieved context supports: `F = |V|/|S|` | The hallucination metric — an unsupported claim is, by definition, made up (source: `sources/papers/ragas.md`) |

### Concept Relationships

```
PDF ─[parse]→ text ─[CHUNK + overlap]→ chunks ─[embed]→ vectors ─[index]→ Chroma   (build once)
question ─[embed]→ q ─[retrieve top-k]→ chunks ─[stuff into prompt]→ LLM ─→ grounded answer + citations
                                                                              │
answer ─[decompose into claims]→ verify each against retrieved chunks ─→ FAITHFULNESS score
```

Critical framing: **RAG is Project 03's retrieval feeding Project 01's chat completion, with three new disciplines wrapped around it** — chunk well (so the right text *can* be retrieved), ground hard (so the LLM answers from context, not memory), and verify (so you catch it when it doesn't).

---

## Section 1: Motivation

### Why This Exists
An LLM "stores factual knowledge in its parameters," but "its ability to access and precisely manipulate knowledge is still limited," and "providing provenance for [its] decisions and updating [its] world knowledge remain open research problems" (source: `sources/papers/rag-paper.md`). Translation: ask a raw LLM about *your* PDF — a contract, a research paper, last quarter's report — and it cannot. The document isn't in its weights; it has a training cutoff; and even when it guesses right, it can't tell you *where* it got the answer. RAG fixes all three by giving the model a retrieved, non-parametric memory at query time.

### The Problem We're Solving
You have documents the model has never seen and answers that must be *grounded* (from the document, not invented) and *attributable* (you can check the source). Stuffing the whole document into the prompt doesn't scale (PDFs blow past context limits and cost) and buries the answer in noise. The RAG answer: **chunk** the document, **retrieve** only the few passages relevant to the question, and have the model **answer from those passages with citations.**

### Real-World Stakes
"Every enterprise AI product either is RAG or contains RAG" — legal research, medical documentation, financial analysis, support automation. The dangerous part is silent: a RAG system that retrieves the wrong chunk, or answers from the model's memory instead of the chunk, produces a fluent, confident, **wrong** answer with no error. In a contract or a clinical setting that is not a bug ticket — it's liability. The engineering judgment that separates a demo from a shipped product is: did retrieval find the right text, did the model stay grounded in it, and can you *prove* the answer came from the source (source: `sources/papers/ragas.md`, `sources/official-docs/anthropic-citations.md`).

### Would Users Pay For This?
This is the most commercially deployed AI architecture. "Chunks returned from searches over databases ... ground the agent's responses" (source: `sources/articles/chunking-strategies.md`) — and getting that grounding right is the entire value proposition of document-intelligence companies. Users pay for *trustworthy* answers over *their* documents; faithfulness and citations are what they're actually buying.

---

## Section 2: Mental Model

### ELI12 (Explain Like I'm 12)
Imagine an open-book test. A student who memorized the textbook (that's a plain LLM) can answer general questions but will confidently make things up about a book they never read. Now give them **your** specific book and one rule: *"Before you answer, find the exact pages that talk about the question, read only those, write your answer, and underline the sentence you got it from. If the book doesn't say, write 'not in the book.'"* That's RAG. **Chunking** is tearing the book into index cards so they can find the right card fast. **Citations** are the underlines. **Faithfulness** is the teacher checking that every sentence the student wrote is actually backed by an underlined card — and catching the ones that aren't.

### ELI-Engineer (Explain to a Software Engineer)
- **RAG** = retrieve-then-generate. At query time: embed the question, retrieve the top-k nearest chunks from a vector DB (Project 03), concatenate them into the prompt as context, and ask the LLM to answer **only** from that context. It "combine[s] pre-trained parametric and non-parametric memory" — the weights are parametric, your indexed chunks are non-parametric (source: `sources/papers/rag-paper.md`).
- **Chunking** is the upstream gate. You cannot embed a 40-page PDF as one vector ("exceeding [the] context window means the excess tokens are truncated ... before being processed into a vector") and a single document-level vector is too diffuse to match a specific question. So you split into chunks; chunk size trades precision against context (source: `sources/articles/chunking-strategies.md`).
- **Grounding** is a prompt-engineering discipline: provide the chunks, instruct "answer using only the context; if it's not there, say you don't know," and tag each chunk with an id so the model can cite it.
- **Faithfulness** is a second pass: extract the answer's claims, check each against the retrieved context, score `F = |V|/|S|` (source: `sources/papers/ragas.md`). It is the automated hallucination detector.

### Real-World Analogy
RAG is a **paralegal with a filing cabinet**, not a know-it-all. Ask a question and the paralegal doesn't answer from memory — they pull the relevant files (retrieval), read only those, draft an answer, and **staple a photocopy of the exact paragraph** to each claim (citations). A good paralegal also writes "the file doesn't address this" instead of guessing (refusal). Faithfulness is the partner who reads the draft and checks every claim against the stapled photocopies.

### Intuition Diagram
```
 INGEST (once):
   report.pdf ──parse──► raw text ──CHUNK(size, overlap)──► [c0 c1 c2 ... cN]
                                                              │ embed each
                                                              ▼
                                                       Chroma index (cosine)

 ASK (per question):
   "What was Q3 revenue?"
        │ embed
        ▼
     q-vector ──retrieve top-k──► [c7, c2, c9]   (the chunks most likely to hold the answer)
                                      │ stuff into prompt as CONTEXT + ids
                                      ▼
                          LLM: "answer ONLY from context; cite chunk ids; else say I don't know"
                                      │
                                      ▼
                       "Q3 revenue was $4.2M [c7]."  ──verify──► claim 'Q3 revenue $4.2M'
                                                                  supported by c7?  yes → faithful
```

---

## Section 3: Technical Explanation

### Formal Definition
- **RAG**: given a question `q` and a document store, retrieve a set of passages `Z = top-k(q)` and generate the answer from `p(answer | q, Z)`. The store is **non-parametric memory** — "a dense vector index ... accessed with a ... neural retriever" — coupled to the **parametric** seq2seq generator (source: `sources/papers/rag-paper.md`).
- **Faithfulness** (RAGAS): extract the set of statements `S` the answer makes; let `V ⊆ S` be the statements that "can be inferred from the context." Then `F = |V| / |S| ∈ [0, 1]` (source: `sources/papers/ragas.md`).
- **Context relevance** (RAGAS): of the sentences in the retrieved context, the fraction "crucial to answer q" — a retrieval/chunking diagnostic, `CR = |extracted| / |total sentences|` (source: `sources/papers/ragas.md`).

### How It Works (Mechanically)

**Ingest & chunk.** Parse the PDF to text, then split into chunks of roughly fixed size with overlap. "Fixed-sized chunking will be the best path in most cases" — start there (source: `sources/articles/chunking-strategies.md`). Each chunk keeps an **id** and its **source** (e.g. page) so it can be cited later.

**Embed & index.** Embed each chunk once and add it to a Chroma collection with `space="cosine"` (Project 03). Index built once; queried many.

**Retrieve.** Embed the question, `collection.query(query_embeddings=[q], n_results=k)`, get back the top-k chunks (with ids). This is the entire "R" of RAG — your Project 03 retriever.

**Generate (grounded).** Build a prompt: a system instruction ("answer using only the provided context; cite the chunk ids you used; if the answer is not in the context, say you don't know"), then the retrieved chunks labeled with their ids, then the question. Call the LLM (Project 01).

**Cite.** A citation is a pointer from a span of the answer to "specific locations in source documents" — the chunk id (and its page/char range) that supports the claim (source: `sources/official-docs/anthropic-citations.md`).

**Verify (faithfulness).** Decompose the answer into claims; for each, ask whether the retrieved context entails it; `F = |V|/|S|`. A low score flags hallucination (source: `sources/papers/ragas.md`).

### The Math (When Necessary)
- Faithfulness: `F = |V| / |S|`, supported claims over total claims; `F = 1.0` means every claim is grounded, `F = 0.0` means the answer is entirely unsupported (source: `sources/papers/ragas.md`).
- Context relevance: `CR = |S_ext| / |S_context|` (source: `sources/papers/ragas.md`).
- Chunking has no formula — it's a design choice. Rough default: ~500-token chunks, ~10–20% overlap, then iterate (source: `sources/articles/chunking-strategies.md`).

### Implementation Details
- **Same embedding model for chunks and query** — carries from Project 03; mixing models makes retrieval meaningless (silent bug).
- **Keep chunk ids stable and carry the source.** The id is what a citation points to and what faithfulness verifies against. Lose it and you can't cite or check.
- **Overlap matters at boundaries.** Without it, a fact spanning a chunk cut is unfindable. With it, the fact lives intact in at least one chunk (source: `sources/articles/chunking-strategies.md`).
- **Grounding is in the prompt, and it's fragile.** If the instruction is weak, the model "helpfully" answers from its own memory and ignores the context — the hardest RAG bug because the answer often *looks* right.
- **Refusal must be explicit.** Tell the model to say "I don't know" when the context lacks the answer, or it will never refuse.
- **Low temperature for grounded answers.** You want faithful extraction, not creativity — set temperature low.
- **Faithfulness is a separate LLM call**, not a vibe. Extract claims, verify against context, compute the ratio (source: `sources/papers/ragas.md`).

---

## Section 4: Guided Examples

> The lab stack: `pypdf` (parse), `chromadb` (retrieve, Project 03), `litellm` (embeddings + chat via `config.py`). See `code/`. Examples below mirror the guiding tests.

### Example 1: Simple Case — chunk text with overlap
```python
from chunker import chunk_text

text = "A B C D E F G H I J"          # 10 "tokens" (words) for the demo
chunks = chunk_text(text, chunk_size=4, overlap=2)
for c in chunks:
    print(c.id, repr(c.text))
# c0 'A B C D'
# c1 'C D E F'      # overlaps c0 by 2 tokens — nothing falls in a crack
# c2 'E F G H'
# c3 'G H I J'
```
**What to observe:** consecutive chunks **share** `overlap` tokens, so a fact straddling a boundary (say "E F") survives intact in a chunk. Each chunk has a stable `id` — that id is what you'll cite and what faithfulness checks against.

### Example 2: Real-World Case — a grounded prompt that cites and can refuse
```python
from chunker import Chunk
from generator import build_prompt

chunks = [
    Chunk("c0", "Q3 revenue was $4.2M, up 8% YoY."),
    Chunk("c1", "The company opened a Berlin office in July."),
]
messages = build_prompt("What was Q3 revenue?", chunks)
# system message instructs: answer ONLY from context, cite chunk ids, else say "I don't know"
print(messages[0]["role"])                       # 'system' → grounding + refusal instruction
print("[c0]" in messages[-1]["content"])         # True: chunk ids are in the prompt to cite
# A grounded model answers: "Q3 revenue was $4.2M [c0]."  — note the citation to c0, not c1.
```
**What to observe:** the retrieved chunks **and their ids** are in the prompt, and the system message both demands citations and *permits refusal*. The model is being told to answer from the context, not from its own memory.

### Example 3: Edge Case — faithfulness catches a hallucination
```python
from faithfulness import faithfulness_score

# Claims extracted from an answer, each already verified against the retrieved context:
verdicts = [True, True, False]   # 3rd claim ("revenue was $9M") is NOT supported by any chunk
print(faithfulness_score(verdicts))      # 0.6667  →  2 of 3 claims grounded

# A fully grounded answer:
print(faithfulness_score([True, True, True]))   # 1.0
# An answer the context doesn't support at all (pure hallucination):
print(faithfulness_score([False, False]))       # 0.0
```
**What to observe:** `F = |V|/|S|` turns "did it hallucinate?" into a number. The third claim was fluent and confident — and unsupported. Without the faithfulness pass you'd ship it. This is the metric, not a feeling (source: `sources/papers/ragas.md`).

---

## Section 5: Reflection Before Building

> The learner should fill UNDERSTANDING.md before proceeding to implementation.

**Questions to answer in UNDERSTANDING.md:**

1. In your own words, what does RAG add over (a) a raw LLM and (b) just stuffing the whole PDF into the prompt? Use "parametric vs non-parametric memory" in your answer.
2. Draw the ingest-once vs ask-per-question data flow. Which steps happen once, which per question?
3. Chunk size: predict what goes wrong if chunks are *too small*, and what goes wrong if they're *too large*. Why does overlap help?
4. Grounding can fail silently — the model answers from its own memory and ignores the context, and the answer still looks right. How would you *detect* that this happened?
5. What is faithfulness, in your own words, and why is `F = |V|/|S|` a hallucination detector? What's the difference between a *faithful* answer and a *relevant* one?
6. A RAG system is asked something the document doesn't cover. What should happen, and what makes a system fail to do that?
7. The one thing you still don't fully understand about RAG.

---

## Section 6: Project Assignment

See PROJECT.md and source/project.md for the full specification.

### Core Requirement
Build a PDF research assistant in `code/` that answers questions about a document with grounded, cited answers and a faithfulness check:
- **`chunker.py`** — split document text into overlapping, id-tagged chunks (`chunk_text`). *Learner core.*
- **`retriever.py`** — build a Chroma index of the chunks and retrieve top-k for a query. *(Provided — this is your Project 03 retriever, reused.)*
- **`generator.py`** — construct the grounded prompt (context + ids + refusal instruction) and produce an answer with citations (`build_prompt`, `answer`). *Learner core.*
- **`faithfulness.py`** — decompose the answer into claims, verify each against the retrieved context, and compute `F = |V|/|S|` (`faithfulness_score`, `check_faithfulness`). *Learner core.*
- **`rag.py`** — the end-to-end pipeline that wires ingest → chunk → index → retrieve → answer → verify. *(Provided orchestrator.)*

### Extended Requirements
- Add **char/page citations** (not just chunk ids) so a claim points to an exact location, mirroring `char_location`/`page_location` (source: `sources/official-docs/anthropic-citations.md`).
- Compare **two chunking strategies** (e.g. fixed-size vs recursive/sentence) on the same questions and report the difference in retrieval + faithfulness.
- Add **context relevance** scoring (`CR`) to diagnose whether a weak answer is a retrieval problem or a generation problem (source: `sources/papers/ragas.md`).

### Start Building

**Open [`code/README.md`](../code/README.md)** for setup, the milestone build order, and the file roles (which files are *provided* vs. *learner-owned*). Run `python -m pytest` to see the failing guiding tests, then implement the learner-owned functions in milestone order until they pass.

---

## Section 7: Project Milestones

| Milestone | What You Build | Validation |
|-----------|---------------|------------|
| M1: Chunk | `chunker.py` splits text into overlapping, id-tagged chunks | Adjacent chunks overlap by `overlap`; every chunk has a stable id + source |
| M2: Index & Retrieve | Build a Chroma index of chunks; retrieve top-k for a query (Project 03 reuse) | A question retrieves the chunk that actually contains the answer |
| M3: Grounded answer | `generator.build_prompt` stuffs context + ids and instructs answer-only-from-context | The prompt contains the chunks, their ids, and an explicit refusal instruction |
| M4: Citations | `answer()` attaches the supporting chunk id(s) to the answer | Each claim in the answer points to the chunk it came from |
| M5: Faithfulness | `faithfulness.py` decomposes the answer into claims and scores `F = |V|/|S|` | A grounded answer scores ~1.0; an injected false claim drops the score |
| M6: Break / Evaluate | Ask an out-of-document question; force a hallucination; measure the drop | Off-doc question → refusal; faithfulness number recorded in FAILURE_ANALYSIS.md |

---

## Section 8: Self-Evaluation

| Criterion | Does your implementation... | Pass? |
|-----------|---------------------------|-------|
| Real chunking | split documents into overlapping, id-tagged chunks (not one vector per doc)? | |
| Retrieval reuse | build a persistent Chroma index and retrieve top-k by meaning? | |
| Actually grounded | instruct the model to answer **only** from context, and pass the chunks in the prompt? | |
| Refuses | answer "I don't know" when the document doesn't contain the answer? | |
| Cites | trace each claim back to the supporting chunk id/source? | |
| Measures faithfulness | compute `F = |V|/|S|` over the answer's claims, as a number? | |

**Red flags (your implementation may have problems if):**
- The model answers off-document questions confidently instead of refusing.
- You never pass the retrieved chunks into the prompt (the model is answering from memory).
- Answers have no citations, so a human can't verify them.
- You report "it works" with no faithfulness number and no broken-case test.
- Chunks have no stable id/source, so you can't cite or verify against them.
- You embed chunks with one model and the query with another.

---

## Section 9: Common Mistakes

| Mistake | Why It Happens | Consequence | Fix |
|---------|---------------|-------------|-----|
| No grounding instruction (or a weak one) | Assuming "context in prompt" is enough | Model answers from its own memory; fluent but ungrounded | System message: "answer ONLY from the context; if absent, say you don't know" (source: `sources/papers/rag-paper.md`) |
| Chunks too large | "More context is better" | Diffuse embeddings; retrieval can't find precise matches; answer buried in noise | Smaller fixed-size chunks; iterate (source: `sources/articles/chunking-strategies.md`) |
| Chunks too small / no overlap | Maximizing precision | A fact spanning a boundary is unfindable | Add ~10–20% overlap so boundary facts survive (source: `sources/articles/chunking-strategies.md`) |
| Never refusing | No "I don't know" path in the prompt | Confident hallucination on off-document questions | Explicit refusal instruction + test it on an off-doc question |
| No citations | Treating the answer as the deliverable | Unverifiable answers — useless in legal/medical/finance | Tag chunks with ids; have the model cite the id per claim (source: `sources/official-docs/anthropic-citations.md`) |
| "It works" with no faithfulness check | Eyeballing a few good answers | Hallucinations ship silently | Score `F = |V|/|S|`; verify each claim against context (source: `sources/papers/ragas.md`) |
| Mixing embedding models | Index and query embedded differently | Retrieval returns garbage; whole pipeline fails silently | Pin one embedding model for chunks and query (carries from Project 03) |

---

## Section 10: Connections

### How This Connects to Previous Projects
Project 03 built **retrieval** — index chunks, query top-k. Project 04 *is* that retriever feeding an LLM (Project 01's chat completion), with chunking in front and grounding/citation/faithfulness around it. The "same embedding model both sides" rule and the persistent Chroma index come straight from Project 03; the system+user message construction comes from Project 01.

### How This Connects to Future Projects
**Project 05 (memory)** is RAG over your *own past* instead of a PDF — chunk and index conversations/notes, retrieve relevant memories, ground responses in them. **Project 07 (evaluation framework)** generalizes the faithfulness pass here into a full LLM-as-judge eval suite (source: `sources/papers/ragas.md`). The retrieve-then-rerank pattern from Project 03 plugs in directly when retrieval precision isn't enough.

### How This Connects to StarcallOS
Any StarcallOS feature that answers from *your* documents, notes, or history — "what did I decide about X," "summarize this spec," "what does this contract say about termination" — is RAG. The disciplines built here decide whether StarcallOS gives a **grounded, cited** answer you can trust or a confident hallucination: chunk your knowledge well, ground hard, cite the source, and refuse when the answer isn't there.

### Production Patterns
The deployed pattern is exactly this pipeline plus guardrails: chunk (often recursive/semantic), retrieve top-k (often + re-rank from Project 03), ground with a strict system prompt, **cite with verifiable pointers** ("citations are guaranteed to contain valid pointers to the provided documents" — source: `sources/official-docs/anthropic-citations.md`), and **monitor faithfulness** offline and online (source: `sources/papers/ragas.md`). Real systems add prompt caching on the document context to cut cost.

---

## Assessment Rubric

See source/rubric.md for the complete grading rubric.

**Summary criteria:**
- [ ] Implementation runs correctly (chunk → index → retrieve → grounded answer → faithfulness)
- [ ] Understanding document completed in learner's own words
- [ ] Failure analysis demonstrates intentional experimentation (off-doc refusal, forced hallucination, chunk-size effect)
- [ ] Evaluation is quantitative (faithfulness `F = |V|/|S|`, retrieval hit/miss), not impressionistic
- [ ] StarcallOS reflection identifies at least one concrete applicable pattern

---

## Sources

See source/resources.md for the full annotated source list.

**Required reading:**
- `sources/papers/rag-paper.md` — what RAG is: parametric + non-parametric memory, provenance, updatable knowledge
- `sources/articles/chunking-strategies.md` — chunk-size tradeoff, overlap, fixed vs recursive vs semantic
- `sources/papers/ragas.md` — faithfulness (the hallucination metric), answer/context relevance

**Recommended reading:**
- `sources/official-docs/anthropic-citations.md` — production citation contract: claim → exact source location
- `sources/official-docs/chromadb.md` — the retrieval index (carried from Project 03)
- `sources/articles/sbert-retrieve-rerank.md` — re-ranking when first-stage retrieval isn't precise enough

---

## Instructor Notes

<!-- Hidden context for the mentor reviewing the learner's work. -->

**Common misconceptions:**
- That putting the document in the prompt *is* RAG. RAG is selective retrieval + grounding; stuffing the whole doc is the thing RAG replaces (scale, cost, noise).
- That a fluent answer is a grounded answer. The hardest RAG failure is a confident answer drawn from the model's memory while ignoring the retrieved context.
- That faithfulness and relevance are the same. Faithful = supported by context; relevant = addresses the question. An answer can be one without the other (source: `sources/papers/ragas.md`).
- That bigger chunks (more context) are better. Larger chunks dilute the embedding and hurt retrieval precision (source: `sources/articles/chunking-strategies.md`).
- That a RAG system should always answer. It should *refuse* when the document doesn't cover the question.

**Diagnostic questions (reveal genuine vs. surface understanding):**
- "Your answer is correct but the retrieved chunks don't contain it. Is that a pass?" (grounding vs. memory — it's a *fail*: ungrounded.)
- "Faithfulness is 1.0 but the answer is useless. How?" (faithful but not relevant.)
- "A fact sits exactly on a chunk boundary and never gets retrieved. What knob fixes it?" (chunk overlap.)
- "Asked about something not in the PDF, the system gave a detailed answer. What's broken?" (no refusal + likely no grounding.)

**Signs of genuine understanding:**
- The learner tests the off-document question and confirms a refusal, unprompted.
- They force a hallucination (inject a false premise / weaken grounding) and *watch the faithfulness score drop*.
- They can say which pipeline stage caused a bad answer (chunking vs retrieval vs generation) rather than "the AI got it wrong."
- They keep stable chunk ids and use them for both citation and faithfulness verification.
