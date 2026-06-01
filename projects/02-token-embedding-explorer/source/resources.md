# Resources & Sources

> All sources used for this lesson, organized by tier.
> Every claim in lesson.agent.md traces back to one of these.
> Truth lives in `sources/`; this file is the per-project annotated index.

---

## Tier 1: Official Documentation

> Primary sources. Check these first.

- [x] **tiktoken — OpenAI's BPE tokenizer** → `sources/official-docs/tiktoken-bpe.md`
  - URL: https://github.com/openai/tiktoken
  - What to read: README — encode/decode API, token counting, "~4 bytes per token"
  - Key sections: encode/decode round-trip, `encoding_for_model`, byte-level BPE properties

- [x] **Hugging Face — Summary of the Tokenizers** → `sources/official-docs/hf-tokenization-algorithms.md`
  - URL: https://huggingface.co/docs/transformers/en/tokenizer_summary
  - What to read: BPE worked example (hug/pug/pun/bun/hugs), word vs char vs subword tradeoff
  - Key sections: Byte-Pair Encoding, Byte-level BPE, Word-level vs Character-level

- [x] **scikit-learn — Cosine Similarity** → `sources/official-docs/scikit-learn-cosine-similarity.md`
  - URL: https://scikit-learn.org/stable/modules/metrics.html#cosine-similarity
  - What to read: formula, "cosine of the angle", magnitude-invariance, range [−1, 1]
  - Key sections: cosine_similarity definition and L2 normalization note

---

## Tier 2: Foundational Papers

> Academic papers that established the concepts in this lesson.

- [x] **Efficient Estimation of Word Representations in Vector Space (word2vec)** → `sources/papers/word2vec.md`
  - Title: Efficient Estimation of Word Representations in Vector Space
  - Authors: Mikolov, Chen, Corrado, Dean (Google)
  - Year: 2013
  - URL: https://arxiv.org/abs/1301.3781
  - Why it matters: foundational "meaning as geometry" paper; CBOW/Skip-gram; `king − man + woman ≈ queen` vector arithmetic

- [x] **Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks (SBERT)** → `sources/papers/sentence-bert.md`
  - Title: Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks
  - Authors: Reimers & Gurevych (UKP Lab, TU Darmstadt)
  - Year: 2019 (EMNLP)
  - URL: https://arxiv.org/abs/1908.10084
  - Why it matters: how to embed whole sentences for cosine comparison; encode-once/compare-many; bi- vs cross-encoder; 65h → 5s speedup

---

## Tier 3: Engineering Blogs

> Practical engineering perspectives from teams who've shipped this in production.

- [ ] *(none gathered yet — add when the lesson is authored, e.g. an embedding-model-selection or chunking-cost post)*

---

## Tier 4: Educational Sources

> Tutorials, courses, and explanatory content useful for learning.

- [ ] *(none gathered yet — HF LLM Course ch.6 "Build a tokenizer" is the natural addition: https://huggingface.co/learn/llm-course/chapter6/1)*

---

## Recommended Reading Order

For a learner new to this topic:

1. Start with: `hf-tokenization-algorithms.md` — what a token is and how BPE builds a vocabulary (do the hug/pug merge by hand)
2. Then read: `tiktoken-bpe.md` — run a real tokenizer; count tokens; connect back to Project 01 cost
3. Then read: `word2vec.md` — meaning becomes geometry; analogy arithmetic
4. For depth: `sentence-bert.md` (sentence-level embeddings) then `scikit-learn-cosine-similarity.md` (how to measure it)

---

## Further Reading

Topics adjacent to this lesson worth exploring later:

- Contextual vs. static embeddings (why "bank" needs context) — bridges word2vec → modern embedding APIs
- Bi-encoder retrieve + cross-encoder re-rank — the production pattern hinted at in `sentence-bert.md`, expanded in Project 03
- Tokenizer differences across providers (tiktoken vs. Llama/Anthropic) — why token counts are provider-specific
