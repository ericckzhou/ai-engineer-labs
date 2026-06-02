# Project 03 — Reference Solution Notes (solns branch only)

> Exists only on `solns`. **Do not merge to `main`** — leaks answers.

## What was implemented (the learner surface)

| File | Function(s) | Milestone |
|---|---|---|
| `baseline.py` | `cosine_similarity`, `exact_rank`, `recall_at_k` | M4/M5 |
| `indexer.py` | `build_index` (persistent cosine, idempotent upsert) | M1 |
| `semantic_search.py` | `to_similarity`, `search` (distance→similarity, rank desc) | M2/M3 |
| `evaluate.py` | `evaluate` (recall@k, ANN vs exact) | M5 |
| `rerank.py` | `rerank` (cross-encoder re-score) | M6 (extended) |

`config.py` and `embedding_helpers.py` are `[provided]` — not touched.

## Offline verification (the gate) — PASS

```
$ .venv/Scripts/python.exe -m pytest -q
17 passed, 1 warning   (0 skipped — chromadb-backed tests actually ran)
```

## ⚠️ Provided-scaffold defects found via this gate (BELONG ON main, not solns)

Running the solution against the real `chromadb` (1.5.9) surfaced **two provided-test
defects** that a learner on `main` would also hit. These are scaffold bugs, not answers:

1. **`tests/test_indexer.py`** — collection names `"t1"`/`"t2"` are 2 chars; chromadb now
   requires names of 3–512 chars. Renamed to `"idx_count"` / `"idx_idem"`.
2. **`tests/conftest.py`** — `cosine_collection` creates collection `"test"` on a shared
   in-memory `chromadb.Client()`; the second test using the fixture died with
   `Collection [test] already exists`. Added a `delete_collection("test")` guard before
   create so the fixture is re-entrant.

**Action required:** port these two test fixes to `main` scaffold. They were applied here
only so the solution gate could run; without them the *provided* suite is red on a clean
checkout. First concrete evidence that the provided template is **not** sufficient as-is.

## Live smoke run (provider-dependent code) — PENDING

`build_index`/`search`/`evaluate` ran offline via fake embeds + in-memory Chroma. A real
run still needs an embedding provider:

```
$ USE_OLLAMA=1 .venv/Scripts/python.exe indexer.py          # persistent .chroma, count = 6
$ USE_OLLAMA=1 .venv/Scripts/python.exe semantic_search.py  # finance query → finance docs top
$ USE_OLLAMA=1 .venv/Scripts/python.exe evaluate.py         # recall@3 table vs exact baseline
```
