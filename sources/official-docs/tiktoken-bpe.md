# tiktoken — Fast BPE Tokenizer for OpenAI Models

**Type:** official-doc
**Tier:** 1 (Official Doc)
**Author(s):** OpenAI
**Date:** Accessed 2026-06-01
**URL:** https://github.com/openai/tiktoken
**Accessed:** 2026-06-01

## Why This Source Matters

`tiktoken` is the lab's hands-on tokenizer for Project 02. It is OpenAI's official, open-source Byte Pair Encoding (BPE) tokenizer — the exact algorithm used to turn text into the integer token IDs that GPT models consume. It grounds the project's first learning objective ("explain what a token is and why LLMs use them") in runnable, authoritative code rather than analogy. It is also the concrete tool the learner uses to *predict token cost before calling an API*, the bridge back to Project 01's cost tracking.

## Key Claims

### What it is
- tiktoken is "a fast BPE tokeniser for use with OpenAI's models." BPE = Byte Pair Encoding.
- It is **3–6× faster** than a comparable open-source tokenizer.

### Why tokens at all
- Language models operate on **sequences of integers, not text**. The tokenizer is the boundary layer: text → token IDs (in), token IDs → text (out). The model never sees characters.

### Properties of BPE tokenization
- **Reversible and lossless** — tokens decode back to the exact original text.
- Works on **arbitrary/unseen text** (no out-of-vocabulary failure).
- **Compresses** text into shorter sequences — on average **each token ≈ 4 bytes** of text.
- Identifies **common subwords**: e.g. `"ing"` is frequent, so `"encoding"` splits into tokens like `"encod"` + `"ing"`.

### API (encode / decode / count)
```python
import tiktoken

enc = tiktoken.get_encoding("o200k_base")
enc.encode("hello world")            # -> list[int] of token IDs
enc.decode(enc.encode("hello world")) # -> "hello world"  (lossless round-trip)

# token count = length of the encoded list
num_tokens = len(enc.encode("hello world"))

# get the encoding a specific model actually uses
enc = tiktoken.encoding_for_model("gpt-4o")
```

### Encodings
- An **encoding** (e.g. `cl100k_base`, `o200k_base`) is a named tokenizer configuration: a fixed vocabulary + merge rules that defines exactly how text maps to tokens. Different model families use different encodings, so token counts differ across models.

## Relevant To

- concepts: [tokenization, byte-pair-encoding, token, vocabulary, token-cost-estimation]
- projects: [02-token-embedding-explorer, 01-ai-chatbot]

## Notes

- tiktoken implements **byte-level BPE** (base vocabulary = 256 byte values), which is why it never needs an `<unk>` token — see `hf-tokenization-algorithms.md` for the algorithm mechanics.
- Caveat for the lab: token counts from `tiktoken` are exact for OpenAI models. Other providers (Groq/Llama, Anthropic) use **different tokenizers**, so tiktoken counts are an *estimate* for them, not ground truth. The learner should observe this discrepancy rather than assume one tokenizer is universal.
- tiktoken is a **tokenizer, not an embedding model** — it produces integer IDs, not meaning-bearing vectors. Keeping that distinction crisp is an explicit Project 02 objective.
