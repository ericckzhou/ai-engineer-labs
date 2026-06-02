# Project 02 — Reference Solution Notes (solns branch only)

> Exists only on `solns`. Records how the reference implementation was verified.
> **Do not merge to `main`** — it would leak answers to learners.

## What was implemented (the learner surface)

| File | Function(s) | Milestone |
|---|---|---|
| `tokenizer_explorer.py` | `encode`, `decode`, `token_pieces`, `count` | M1 |
| `embedding_explorer.py` | `embed` (litellm, dimension read from vector) | M3 |
| `similarity_calculator.py` | `cosine_similarity` (by hand, numpy) | M4 |
| `corpus_search.py` | `search` (embed corpus, rank by cosine, top-k) | M5 |

`config.py` is `[provided]` and was **not** touched. `git diff main..solns` for this project
equals exactly the four files above.

## Offline verification (the gate) — PASS

```
$ cd projects/02-token-embedding-explorer/code
$ python -m venv .venv && .venv/Scripts/python.exe -m pip install -r requirements.txt
$ .venv/Scripts/python.exe -m pytest -q
27 passed, 1 warning in 1.89s
```

Covers `test_tokenizer.py` (real tiktoken, lossless round-trip), `test_similarity.py`
(cosine invariants on hand-built vectors), `test_corpus_search.py` (ranking with a fake
embed monkeypatched in — no network), `test_config_models.py`. The `embed()` function
itself needs a provider and has no offline test (the corpus-search test fakes it).

## Live smoke run (provider-dependent code) — PENDING

`embed()` and the `main()` harnesses need an embedding provider. With one configured:

```
$ USE_OLLAMA=1 .venv/Scripts/python.exe embedding_explorer.py   # 768-dim nomic vector, stable
$ USE_OLLAMA=1 .venv/Scripts/python.exe similarity_calculator.py # paraphrase HIGH, unrelated LOW
$ USE_OLLAMA=1 .venv/Scripts/python.exe corpus_search.py         # monetary-policy query ranks finance sentences top
```

Expected: dimensionality read from the vector (never hardcoded); paraphrase pair scores
high while unrelated scores low — proof embeddings encode meaning, not surface words.
