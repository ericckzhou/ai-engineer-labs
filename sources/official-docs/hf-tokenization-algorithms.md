# Hugging Face — Summary of the Tokenizers (BPE, WordPiece, Unigram)

**Type:** official-doc
**Tier:** 1 (Official Doc)
**Author(s):** Hugging Face (Transformers documentation)
**Date:** Accessed 2026-06-01
**URL:** https://huggingface.co/docs/transformers/en/tokenizer_summary
**Accessed:** 2026-06-01

## Why This Source Matters

This is the authoritative, worked-example explanation of *how subword tokenization algorithms actually build their vocabularies*. Where `tiktoken-bpe.md` gives the API, this source gives the **mechanism**: it walks BPE merge-by-merge on a tiny corpus, so the learner can reproduce the algorithm by hand. It also establishes the word-vs-character-vs-subword tradeoff that motivates tokenization in the first place — the conceptual spine of Project 02's tokenization half.

## Key Claims

### The motivating tradeoff (why subword)
- **Word-level**: vocabulary becomes enormous (every inflection — `love`, `loving`, `loved`, `lovingly` — is its own token); huge embedding matrix; new/unseen words map to `<unk>` and are unrepresentable.
- **Character-level**: tiny vocabulary, every word representable, no `<unk>` — but **sequences get very long** and a single char (`"l"`) carries far less meaning than a word (`"love"`), hurting performance.
- **Subword** (the compromise): split between words and characters. Keep common words whole; decompose rare words into known subwords. Compact vocabulary *and* the ability to represent unseen words. Example: `annoyingly` → `["annoying", "ly"]` or `["annoy", "ing", "ly"]`.

### Byte Pair Encoding (BPE), step by step
1. A **pre-tokenizer** splits text into words + frequencies, e.g. `("hug",10), ("pug",5), ("pun",12), ("bun",4), ("hugs",5)`.
2. Build a **base vocabulary** from all characters: `["b","g","h","n","p","s","u"]`.
3. **Iteratively merge the most frequent adjacent pair.** `"u"+"g"` is most frequent → merge into `"ug"`, add to vocab.
4. Next most frequent pair `"u"+"n"` → merge into `"un"`.
5. Continue until the **target vocabulary size** is reached. **Final vocab size = base size + number of merges.** Example: original GPT uses BPE with vocab 40,478 = 478 base + 40,000 merges.
- BPE is **deterministic**: a fixed list of merge rules applied in order.

### Byte-level BPE (what GPT-2 / tiktoken use)
- Using all Unicode chars as the base would be huge. **Byte-level BPE uses the 256 byte values as the base vocabulary**, so *every* string is tokenizable with **no `<unk>` token ever**.
- GPT-2 vocab = 50,257 = 256 byte tokens + 50,000 merges + 1 end-of-text token.

### Contrast algorithms (for accurate mental model)
- **WordPiece** (BERT family): merges the pair that most increases training-data likelihood — `score(u,g) = freq(ug) / (freq(u)·freq(g))` — i.e. how *informative* the merge is, not merely how frequent. BPE merges the most frequent pair; WordPiece merges the most surprising-together pair.
- **Unigram** (T5, Pegasus): starts with a *large* candidate vocab and **removes** the lowest-loss tokens until target size; probabilistic, can produce multiple tokenizations and pick the highest-probability one.
- **SentencePiece**: applies BPE/Unigram to **raw bytes including the space char** (`▁`), so it works for languages without spaces (Chinese, Japanese).

## Relevant To

- concepts: [tokenization, byte-pair-encoding, subword-tokenization, vocabulary, wordpiece, unigram]
- projects: [02-token-embedding-explorer]

## Notes

- The tiny `hug/pug/pun/bun/hugs` corpus is ideal for a learner exercise: have them perform 2–3 BPE merges by hand, then confirm against `tiktoken` behavior on real text.
- Key correction to a common misconception: BPE merges are driven by **frequency in a training corpus**, not by linguistic morphology. Subword boundaries often *look* morphological but are a statistical artifact.
