# Project 03: Semantic Search — Code

> Workflow is standardized across all lab projects. `config.py` (swappable provider) and
> `.env.example` are stamped from the canonical template
> (`skills/lesson-generator/templates/`). The modules and guiding tests below are specified in
> `../source/project.md` and taught in `../source/lesson.agent.md`.

## Setup

```bash
# From this directory
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

uv pip install -r requirements.txt

cp .env.example .env       # then put your API key(s) in .env (or set USE_OLLAMA=1)
```

## Run (build the index once, then query it)

```bash
python indexer.py            # M1: embed the corpus into a persistent Chroma collection
python semantic_search.py    # M2/M3: query by meaning; distance -> similarity, ranked
python baseline.py           # M4: exact brute-force cosine (the validation baseline)
python evaluate.py           # M5: recall@k of the ANN index vs. the exact baseline
python rerank.py             # M6 (optional): cross-encoder re-rank of the top-k
```

The embedding/index/query modules need a provider: set `USE_OLLAMA=1` (with Ollama running) or a
cloud key in `.env`. The cosine math and recall metric (`baseline.py`) run with no network.

## Test (one command)

```bash
python -m pytest
```

Guiding tests live in `tests/`. They **fail until you implement the core** (that's the point). The
docstring input/output examples in each module are taken from these tests, so they stay truthful:
- `test_baseline.py` — cosine, `exact_rank`, `recall_at_k`; fully offline (numpy).
- `test_search.py` — `to_similarity` (offline) + `search` ranking on an in-memory cosine collection.
- `test_indexer.py` / `test_evaluate.py` — index idempotency and recall@k (in-memory Chroma + fake embed).
- `test_rerank.py` — re-rank ordering with a stubbed cross-encoder (offline).
- `test_config_models.py` — pins the current `config.py` models (Ollama `qwen3.5:4b` /
  `nomic-embed-text`, Groq cloud default); **passes today** and guards against model drift.

Tests that need `chromadb` skip automatically if it isn't installed.

## Provider (swappable by key)

`config.py` picks the model from `.env`: local **Ollama** (`USE_OLLAMA=1`, keyless — chat
`qwen3.5:4b`, embeddings `nomic-embed-text` 768-dim) or cloud **Groq → Anthropic → OpenAI** by whichever
key is set. Override embeddings with `EMBEDDING_MODEL`. No code change needed to switch providers.

## File Roles

Labeled per `OPERATING_RULES.md` §Scaffolding — `provided` (complete) · `partial` (starter +
`NotImplementedError`) · `learner` (you write the core) · `reference` (docs):

| File | Role | You... |
|------|------|--------|
| `.env.example` | `provided` | copy to `.env`, add a key or set `USE_OLLAMA=1` |
| `config.py` | `provided` | tune `Config`; do not edit the canonical provider block |
| `requirements.txt` | `provided` | install once |
| `embedding_helpers.py` | `provided` | use `embed_one` / `embed_many` |
| `indexer.py` | `partial` | implement `build_index()` — persistent, cosine, idempotent (M1) |
| `semantic_search.py` | `learner` | implement `to_similarity()` + `search()` (M2/M3) — the core |
| `baseline.py` | `partial` | implement `cosine_similarity` / `exact_rank` / `recall_at_k` (M4/M5) |
| `evaluate.py` | `learner` | implement `evaluate()` — recall@k ANN vs baseline (M5) |
| `rerank.py` | `learner` | implement `rerank()` — cross-encoder re-rank (M6, optional) |
| `tests/` | `provided` | guiding tests — make them pass |

Search starter files for `[learner]` and `NotImplementedError` to find your work. The full labeled
contract for each function (with I/O examples) is in `../source/project.md`.

## Notes

- Fill in `../UNDERSTANDING.md` before writing any code here.
- Build in milestone order (see the lesson) — don't write everything at once.
- Document your process in `../IMPLEMENTATION.md` as you go.
- Commit working milestones before adding complexity.
- The persistent index is written to `code/.chroma/` (gitignored — do not commit it).
