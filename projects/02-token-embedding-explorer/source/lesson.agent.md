# Lesson 02: Token & Embedding Explorer
<!-- lesson.agent.md — Agent-optimized canonical source. Do not simplify; this is the truth layer. -->

## Metadata

| Field | Value |
|-------|-------|
| Project | 02-token-embedding-explorer |
| Core Concepts | tokenization, byte-pair encoding, embeddings, cosine similarity, vector math |
| Prerequisites | See PROJECT.md (Project 01 complete; vectors at high-school level; Python + numpy) |
| Difficulty | Intermediate |
| Estimated Time | See PROJECT.md (6–10 hours total) |
| Last Updated | 2026-06-01 |

---

## Learning Objectives

By completing this lesson, the learner will be able to:

1. Explain what a **token** is and why LLMs operate on tokens instead of words or characters.
2. Run a real **BPE tokenizer** (`tiktoken`), inspect token boundaries and integer IDs, and predict roughly how many tokens a piece of text will cost before calling an API.
3. Reproduce two or three **BPE merge steps by hand** and explain why merges are driven by corpus frequency, not grammar.
4. Explain what an **embedding vector** is — what the numbers represent and why "meaning becomes geometry."
5. Compute **cosine similarity** by hand once, and explain why it measures *angle*, not distance or magnitude.
6. Explain why **`king − man + woman ≈ queen`** works in embedding space, and demonstrate a case where analogy arithmetic *fails*.
7. Distinguish a **tokenizer** from an **embedding model**, and a **word embedding** from a **sentence embedding** (bi-encoder).
8. Choose an appropriate **embedding model** for a task and reason about why its **dimensionality** (e.g. 768 vs 1536) is model-specific.

---

## Prerequisite Knowledge Check

Before beginning, the learner should be able to answer:

1. From Project 01: when you send text to an LLM, what does `usage.prompt_tokens` count, and why did cost depend on it?
2. What is a vector, and what does it mean to add two vectors or scale one by a number?
3. In Python, what does `len(some_list)` return, and how would you iterate over a list of numbers with `numpy`?

If the learner cannot answer #1, revisit Project 01's token-cost section before continuing.

---

## Core Concepts

| Concept | Definition | Why It Matters |
|---------|-----------|----------------|
| Token | An integer ID for a chunk of text (often a subword), produced by a tokenizer | The model never sees characters; it sees token IDs. Tokens are the unit of cost and context. (source: `sources/official-docs/tiktoken-bpe.md`) |
| Byte-Pair Encoding (BPE) | An algorithm that builds a vocabulary by iteratively merging the most frequent adjacent pair of symbols | The dominant subword tokenizer; explains *why* `encoding` splits into `encod`+`ing`. (source: `sources/official-docs/hf-tokenization-algorithms.md`) |
| Vocabulary | The fixed set of tokens a tokenizer knows (base symbols + learned merges) | Vocab size = base + #merges; different models use different vocabs, so token counts differ. (source: `sources/official-docs/hf-tokenization-algorithms.md`) |
| Embedding | A dense vector that encodes meaning, produced by an embedding model | Turns text into geometry so "similar meaning" becomes "nearby vectors." (source: `sources/papers/word2vec.md`) |
| Embedding space | The high-dimensional space all embeddings live in | Direction and distance carry semantic relationships. (source: `sources/papers/word2vec.md`) |
| Cosine similarity | The cosine of the angle between two vectors: `x·y / (‖x‖‖y‖)` | The standard way to score "how similar" two embeddings are, ignoring magnitude. (source: `sources/official-docs/scikit-learn-cosine-similarity.md`) |
| Sentence embedding | One fixed-size vector for a whole sentence, comparable by cosine | Lets you encode once and compare many — the basis of semantic search. (source: `sources/papers/sentence-bert.md`) |

### Concept Relationships

```
text → [tokenizer: BPE] → token IDs          (what the model reads; unit of cost)
text → [embedding model] → vector            (what carries MEANING)
vector × vector → [cosine similarity] → score (how related two texts are)
```

Critical distinction: **the tokenizer and the embedding model are two different things.** A tokenizer
turns text into integer IDs (reversible, no meaning attached to the *value* of the ID). An embedding
model turns text into a meaning-bearing vector. Project 02 makes both concrete and keeps them separate.

---

## Section 1: Motivation

### Why This Exists
Computers process numbers, not text. Two distinct numeric conversions stand between raw text and a
working AI system: **tokenization** (text → integer IDs the model can read) and **embedding** (text →
a vector that encodes *meaning*). Both existed long before modern LLMs — BPE began as a compression
technique, and dense word vectors were popularized by word2vec in 2013 (source:
`sources/papers/word2vec.md`) — but they are the unglamorous machinery every AI engineer must
understand to debug real systems.

### The Problem We're Solving
Most engineers treat embeddings as a black box: "text goes in, magic happens, numbers come out." That
black box produces real, expensive bugs — mismatched embedding models, wrong chunk sizes, failed
similarity searches, surprise token bills. You cannot debug what you cannot see.

### Real-World Stakes
Every semantic search, RAG pipeline, recommendation engine, and deduplication system rests on these
two conversions. If you embed a query with one model and your documents with another, similarity
scores become meaningless and retrieval silently returns garbage — with no error raised. If you
misjudge tokenization, you blow the context window or the budget. (Connects directly to Project 01's
token-cost work and forward to Projects 03–04.)

### Would Users Pay For This?
For the *explorer tool* itself, probably not. But the **judgment** it builds — which embedding model
to use, how to chunk, when embeddings fail — is the foundation of search, matching, and
recommendation products that users pay for every day. The value is in the engineering judgment, not
the visualization.

---

## Section 2: Mental Model

### ELI12 (Explain Like I'm 12)
Imagine you have to mail a long book, but the post office only accepts numbered LEGO bricks. First you
chop the book into common little pieces ("ing", "the", "pre") and give each piece a brick number —
that's **tokenization**. Now imagine a magic map of a city where every word lives at an address, and
words that *mean* similar things live on the same street. "King" and "queen" are neighbors; "banana"
is across town. The address of a word is its **embedding**. To ask "are these two words similar?" you
don't measure how far apart the houses are — you stand at the city center and check whether they're in
the *same direction*. That "same direction?" check is **cosine similarity**.

### ELI-Engineer (Explain to a Software Engineer)
- **Tokenization** is a lossless, reversible `str ⇄ list[int]` codec with a learned dictionary.
  Byte-Pair Encoding builds that dictionary by starting from bytes and greedily merging the most
  frequent adjacent pair until it hits a target vocabulary size (source:
  `sources/official-docs/hf-tokenization-algorithms.md`). `tiktoken` is OpenAI's fast implementation;
  `len(enc.encode(text))` is your token count, and on average one token ≈ 4 bytes of text (source:
  `sources/official-docs/tiktoken-bpe.md`).
- **Embedding** is a function `str → R^d` (d = 768, 1536, …) learned so that semantically related
  inputs map to vectors pointing in similar directions. word2vec established this for words (source:
  `sources/papers/word2vec.md`); SBERT extended it to whole sentences with a fixed-size output vector
  (source: `sources/papers/sentence-bert.md`).
- **Cosine similarity** is the L2-normalized dot product: `x·y / (‖x‖‖y‖)` — the cosine of the angle
  between the two vectors, ranging −1…1 (source: `sources/official-docs/scikit-learn-cosine-similarity.md`).

### Real-World Analogy
A **tokenizer is like syllables**; an **embedding is like a thesaurus coordinate**. Syllables let you
pronounce (process) any word, even one you've never seen, by breaking it into known pieces — but
syllables carry no meaning ("un-be-liev-able" tells you nothing about belief). The thesaurus
coordinate is the opposite: it ignores spelling entirely and places the *meaning* near related
meanings. You need both: one to read, one to understand.

### Intuition Diagram
```
  "unbelievable"
        │ tokenizer (BPE)            │ embedding model
        ▼                            ▼
  [un][bel][iev][able]        [ 0.02, 0.41, -0.13, ... , 0.07 ]   (d numbers)
  4 integer IDs                       a point/direction in R^d

        cosine( vec("unbelievable"), vec("incredible") )  →  ~0.7   (close direction = similar)
        cosine( vec("unbelievable"), vec("granite")     )  →  ~0.1   (near-orthogonal = unrelated)
```

---

## Section 3: Technical Explanation

### Formal Definition
- **BPE tokenization**: given a target vocab size V, learn an ordered list of merge rules over a base
  alphabet; at encode time, apply merges greedily to map a string to a sequence of token IDs. **Final
  vocab size = base size + number of merges** (source: `sources/official-docs/hf-tokenization-algorithms.md`).
- **Embedding**: a learned map `E: text → R^d`. Cosine similarity `cos(x,y) = (x·y)/(‖x‖‖y‖)` measures
  the angle between two embeddings (source: `sources/official-docs/scikit-learn-cosine-similarity.md`).

### How It Works (Mechanically)

**BPE, by hand** (worked example from `sources/official-docs/hf-tokenization-algorithms.md`).
Start from a corpus of word→frequency with each word split into characters:
```
("h" "u" "g", 10) ("p" "u" "g", 5) ("p" "u" "n", 12) ("b" "u" "n", 4) ("h" "u" "g" "s", 5)
```
1. Most frequent adjacent pair is `u·g` (in hug, pug, hugs) → merge to `ug`.
2. Next is `u·n` (in pun, bun) → merge to `un`.
Vocabulary grows `[b,g,h,n,p,s,u] → [...,ug,un]`. Continue until target size. The merges *look*
morphological but are pure frequency statistics.

**Byte-level BPE** (what GPT-2 / `tiktoken` use): the base vocabulary is the **256 byte values**, so
*every possible string* is tokenizable and there is **no `<unk>` token, ever** (source:
`sources/official-docs/hf-tokenization-algorithms.md`, `sources/official-docs/tiktoken-bpe.md`).

**Embedding → similarity flow**: send text to an embedding model → get back a `d`-length vector →
compare two vectors with cosine similarity. Because cosine ignores magnitude, the vectors can be
L2-normalized to the unit sphere and compared by plain dot product (source:
`sources/official-docs/scikit-learn-cosine-similarity.md`).

### The Math (When Necessary)
For vectors `a, b ∈ R^d`:
```
dot(a,b) = Σ aᵢ·bᵢ
‖a‖      = sqrt(Σ aᵢ²)
cos(a,b) = dot(a,b) / (‖a‖ · ‖b‖)      ∈ [−1, 1]
```
- `1` → same direction (maximally similar); `0` → orthogonal (unrelated); `−1` → opposite.
- **Cosine distance** = `1 − cos`. Mixing similarity and distance silently inverts your rankings.

### Implementation Details
- Token counts are **exact for the model whose encoding you use** and only an **estimate** for other
  providers, because each model family has its own tokenizer (source: `sources/official-docs/tiktoken-bpe.md`).
- **Embedding dimensionality is model-specific**: `nomic-embed-text` → 768, OpenAI `text-embedding-3-small`
  → 1536. Never hardcode a dimension; read it from the returned vector. Do **not** compare vectors from
  two different embedding models — the spaces are unrelated.
- word2vec produces **one static vector per word** (so "bank" the riverbank and "bank" the institution
  share a vector); modern sentence embedders are **contextual** and resolve this (source:
  `sources/papers/word2vec.md`, `sources/papers/sentence-bert.md`).

---

## Section 4: Guided Examples

> The lab stack: `tiktoken` (tokenization), `litellm` (embeddings — provider chosen by `config.py`,
> default local `ollama/nomic-embed-text` at 768-dim), and `numpy` (cosine). See `code/`.

### Example 1: Simple Case — see the tokens
```python
import tiktoken

enc = tiktoken.get_encoding("o200k_base")          # GPT-4o-family encoding
ids = enc.encode("Tokenization is not magic.")
print(ids)                                          # e.g. [2350, 2860, ...] integer IDs
print([enc.decode([i]) for i in ids])               # the text chunk each ID maps to
print("token count:", len(ids))                     # what you'd be billed on
print("round-trip:", enc.decode(ids))               # lossless: exact original text
```
**What to observe:** spaces attach to the *front* of words; common words are one token while rare
words split into several; the count is what Project 01's cost formula multiplies.

### Example 2: Real-World Case — meaning by cosine
```python
import numpy as np, litellm
from config import load_config, default_embedding_model

def embed(text: str) -> np.ndarray:
    r = litellm.embedding(model=default_embedding_model(), input=[text])
    return np.array(r["data"][0]["embedding"])

def cosine(a, b) -> float:
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

a, b, c = embed("the cat sat on the mat"), embed("a feline rested on the rug"), embed("quarterly tax filing")
print(round(cosine(a, b), 3))   # high: same meaning, different words
print(round(cosine(a, c), 3))   # low: unrelated topics
print("dims:", a.shape[0])      # 768 for nomic-embed-text — model-specific
```
**What to observe:** paraphrases score high *despite sharing few words* — proof that embeddings encode
meaning, not surface tokens. This is exactly what keyword search cannot do.

### Example 3: Edge Case — analogy arithmetic, and where it breaks
```python
king, man, woman = embed("king"), embed("man"), embed("woman")
queen, banana = embed("queen"), embed("banana")
analogy = king - man + woman
print("→ queen :", round(cosine(analogy, queen), 3))    # expected: relatively high
print("→ banana:", round(cosine(analogy, banana), 3))   # expected: low
# Now try a pair the model has weak signal for and watch the analogy degrade.
```
**What to observe:** the famous regularity (source: `sources/papers/word2vec.md`) holds *approximately*
— it is a demonstrated tendency, not a law. Finding a triple where it fails is a required Failure
Analysis experiment, not a bug.

---

## Section 5: Reflection Before Building

> The learner should fill UNDERSTANDING.md before proceeding to implementation.

**Questions to answer in UNDERSTANDING.md:**

1. Explain a token in your own words (ELI12 then ELI-Engineer). Why not just feed the model characters?
2. Draw the data flow from raw text to a cosine-similarity score. Where does the tokenizer sit? Where does the embedding model sit? Are they the same component?
3. Predict: if you embed your documents with model A and your queries with model B, what happens — and will you get an error?
4. Predict: what is `cosine(v, v)` for any vector `v`? What about `cosine(v, -v)`? Why?
5. Where have you seen "represent meaning as coordinates" before, inside or outside AI?
6. What is the one thing about embeddings you still don't fully understand?

---

## Section 6: Project Assignment

See PROJECT.md for the full project specification.

### Core Requirement
Build the explorer in `code/`:
- **`tokenizer_explorer.py`** — given text, show each token's boundary, its integer ID, and the total
  count; demonstrate the lossless round-trip.
- **`embedding_explorer.py`** — embed text via `litellm` and report the vector's dimensionality and a
  few components.
- **`similarity_calculator.py`** — implement cosine similarity **by hand with numpy** (no library
  shortcut for the core function) and score pairs of texts.
- **`corpus_search.py`** — embed a small corpus, then return the nearest neighbors of a query by cosine.

### Extended Requirements
- Reproduce `king − man + woman` and find one analogy that *fails*.
- Compare token counts of the same text under two encodings and explain the difference.
- (Optional) Swap the embedding model (local ↔ OpenAI) and observe the dimensionality change; confirm
  you cannot compare vectors across models.

### Start Building

**Open [`code/README.md`](../code/README.md)** for setup, the milestone build order, and the file roles (which files are *provided* vs. *learner-owned*). Run `python -m pytest` to see the failing guiding tests, then implement the learner-owned functions in milestone order until they pass.

---

## Section 7: Project Milestones

| Milestone | What You Build | Validation |
|-----------|---------------|------------|
| M1: Tokenize | `tokenizer_explorer.py` prints IDs + per-token text + count | Round-trip `decode(encode(s)) == s` for several strings |
| M2: BPE by hand | Written: 2–3 merges on the hug/pug corpus | Your merges match BPE's frequency rule |
| M3: Embed | `embedding_explorer.py` returns a vector; you print its length | Same text → same vector; length matches the model (e.g. 768) |
| M4: Cosine | `similarity_calculator.py` implements cosine from scratch | `cos(v,v)=1`, `cos(v,-v)=−1`; paraphrases score higher than unrelated text |
| M5: Search | `corpus_search.py` ranks a corpus by similarity to a query | Top result is semantically (not lexically) the closest |
| M6: Break it | Analogy failure + cross-model dimension mismatch documented | At least one surprising/failed result recorded in FAILURE_ANALYSIS.md |

---

## Section 8: Self-Evaluation

After completing the project, compare your implementation against:

| Criterion | Does your implementation... | Pass? |
|-----------|---------------------------|-------|
| Tokenizer truth | show real `tiktoken` IDs and a lossless round-trip? | |
| Count accuracy | report a token count equal to `len(enc.encode(text))`? | |
| Cosine from scratch | compute `x·y/(‖x‖‖y‖)` yourself, not via a library helper? | |
| Semantic win | rank a paraphrase above a keyword-overlapping but unrelated text? | |
| Dimensionality | read the vector length from the model rather than hardcoding it? | |
| Separation | keep tokenizer and embedding model as distinct components? | |

**Red flags (your implementation may have problems if):**
- Your cosine values fall outside [−1, 1] (you forgot to divide by the norms).
- You compare embeddings produced by two different models and trust the score.
- You hardcoded `1536` (or any dimension) instead of reading `len(vector)`.
- You assume `tiktoken` counts are exact for a non-OpenAI provider.

---

## Section 9: Common Mistakes

| Mistake | Why It Happens | Consequence | Fix |
|---------|---------------|-------------|-----|
| Confusing tokenizer with embedding model | Both "turn text into numbers" | Treats meaningless IDs as if they carried meaning | IDs index a vocabulary; embeddings encode meaning — keep them separate (source: `sources/official-docs/tiktoken-bpe.md`) |
| Hardcoding embedding dimension | Tutorials say "1536" | Breaks the moment you switch models | Read `len(vector)`; dims are model-specific (768 vs 1536) |
| Mixing embedding models | Query and corpus embedded separately over time | Silent garbage retrieval, no error | Pin one model for both sides |
| Cosine vs. Euclidean confusion | "Similar = close" intuition | Wrong rankings when magnitudes differ | Cosine measures *angle*; normalize or use cosine consistently (source: `sources/official-docs/scikit-learn-cosine-similarity.md`) |
| Similarity vs. distance mixup | Libraries return different ones | Rankings inverted (`1 − cos`) | Check whether your tool returns similarity or distance |
| Assuming tokenizer counts are universal | One tokenizer in Project 01 | Wrong cost/context estimates for other providers | tiktoken is exact for OpenAI; an estimate elsewhere (source: `sources/official-docs/tiktoken-bpe.md`) |
| Expecting analogy arithmetic to always work | The king/queen demo | Frustration when it fails | It's an approximate regularity, not a law (source: `sources/papers/word2vec.md`) |

---

## Section 10: Connections

### How This Connects to Previous Projects
Project 01 billed you per **token** — this lesson opens that black box (`tiktoken`) so token count and
cost stop being mysterious. The provider-abstraction layer (LiteLLM/`config.py`) you met in Project 01
is reused here for embeddings.

### How This Connects to Future Projects
Embeddings + cosine are the literal engine of **Project 03 (semantic search)** and **Project 04 (RAG /
PDF assistant)** — both retrieve by embedding a query and ranking documents by cosine. SBERT's
"encode once, compare many" property (source: `sources/papers/sentence-bert.md`) is what makes that
scalable. **Project 05 (memory)** stores and recalls by embedding similarity.

### How This Connects to StarcallOS
Any StarcallOS feature that "finds related things" — recalling a past note, surfacing a relevant
command, matching a request to a capability — is an embedding + cosine lookup underneath. The judgment
built here (which model, what dimension, when similarity lies) governs whether that retrieval feels
intelligent or random.

### Production Patterns
Real systems separate a **bi-encoder** (embed each item independently → fast retrieval) from a
**cross-encoder** (re-encode a pair → highest accuracy, too slow at scale), and combine them:
**retrieve with the bi-encoder, re-rank the top-k with a cross-encoder** (source:
`sources/papers/sentence-bert.md`). Vectors are stored in a vector database (Project 03).

---

## Assessment Rubric

See source/rubric.md for the complete grading rubric.

**Summary criteria:**
- [ ] Implementation runs correctly (tokenizer, embedder, cosine-from-scratch, corpus search)
- [ ] Understanding document completed in learner's own words
- [ ] Failure analysis demonstrates intentional experimentation (analogy failure, model mismatch)
- [ ] Evaluation is quantitative, not impressionistic (real cosine numbers, token counts)
- [ ] StarcallOS reflection identifies at least one concrete applicable pattern

---

## Sources

See source/resources.md for the full annotated source list.

**Required reading:**
- `sources/official-docs/hf-tokenization-algorithms.md` — how BPE builds a vocabulary (do the merge by hand)
- `sources/official-docs/tiktoken-bpe.md` — run a real tokenizer; token counting
- `sources/official-docs/scikit-learn-cosine-similarity.md` — the cosine formula and what it measures

**Recommended reading:**
- `sources/papers/word2vec.md` — meaning as geometry; vector arithmetic
- `sources/papers/sentence-bert.md` — sentence embeddings; bi- vs cross-encoder; encode-once/compare-many

---

## Instructor Notes

<!-- Hidden context for the mentor reviewing the learner's work. -->

**Common misconceptions:**
- That the tokenizer and the embedding model are the same thing (they are not — different outputs, different purpose).
- That a token's integer ID has numeric meaning (it's just a vocabulary index; ID 500 isn't "more" than ID 5).
- That higher embedding dimensionality is strictly "better" (it's a model property/tradeoff, not a quality score).
- That cosine similarity is a distance (it's an angle; distance = 1 − similarity).

**Diagnostic questions (reveal genuine vs. surface understanding):**
- "If I add 1000 to every token ID, what breaks?" (reveals whether they understand IDs index a fixed vocabulary).
- "Two sentences share no words but score 0.9 cosine — how?" (reveals embedding-vs-tokens understanding).
- "Why can't you compare a 768-dim and a 1536-dim vector?" (reveals model-space understanding, not just shape).

**Signs of genuine understanding:**
- The learner can predict, before running code, whether two texts will score high or low and explain why.
- They reach for `len(vector)` instead of a hardcoded dimension unprompted.
- Their Failure Analysis includes an analogy that *failed* and a coherent explanation of why.
- They can articulate why embedding query and corpus with different models is a silent (not loud) bug.
