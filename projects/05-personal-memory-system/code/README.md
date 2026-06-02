# Project 05: Personal Memory System — Code

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

## Run (the chat loop, and each module on its own)

```bash
python chat_with_memory.py            # interactive: remembers across turns (needs a provider)
python chat_with_memory.py --seed     # preload a few memories, ask one question, exit

python scoring.py            # M1–M3: the four scoring functions (offline once implemented)
python retriever.py          # M4: score all memories, take top-k, touch last_accessed (offline)
python memory_store.py       # the provided memory stream (offline)
python embedding_helpers.py  # prints the active embedding model + vector dim (needs a provider)
```

`chat_with_memory.py` and `embedding_helpers.py` need a provider: set `USE_OLLAMA=1` (with Ollama
running) or a cloud key in `.env`. The scoring and retrieval logic runs with **no network**.

## Test (one command)

```bash
python -m pytest
```

Guiding tests live in `tests/`. They **fail until you implement the core** (that's the point). The
docstring input/output examples in each module are taken from these tests, so they stay truthful:
- `test_scoring.py` — recency decay (`0.995 ** hours`), importance normalize, cosine relevance, the
  three-signal weighted sum; fully offline.
- `test_retriever.py` — `retrieve` ranks important+fresh over trivial+old on tied relevance, returns
  top-k, and **touches** `last_accessed`; fully offline (hand-built vectors + timestamps).
- `test_config_models.py` — pins the current `config.py` models (Ollama `qwen3.5:4b` /
  `nomic-embed-text`, Groq cloud default); **passes today** and guards against model drift.

`answer_with_memory()` needs a provider and is exercised by running `chat_with_memory.py`, not in
the offline suite.

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
| `config.py` | `provided` | tune `Config` (decay rate, top_k, weights); do not edit the canonical provider block |
| `requirements.txt` | `provided` | install once |
| `embedding_helpers.py` | `provided` | use `embed_one` / `embed_many` (same model both sides) |
| `memory_store.py` | `provided` | use the `Memory` dataclass + `MemoryStore` (`remember` / `all`) |
| `scoring.py` | `learner` | implement `recency_score`, `importance_score`, `relevance_score`, `retrieval_score` (M1–M3) — **the core** |
| `retriever.py` | `learner` | implement `retrieve()` — score all, sort, take top-k, touch `last_accessed` (M4) |
| `chat_with_memory.py` | `provided` | run it — the end-to-end loop that calls your modules (M5) |
| `tests/` | `provided` | guiding tests — make them pass |

Search starter files for `[learner]` and `NotImplementedError` to find your work. The full labeled
contract for each function (with I/O examples) is in `../source/project.md`.

## Notes

- Fill in `../UNDERSTANDING.md` before writing any code here.
- Build in milestone order (see the lesson) — `scoring.py` first (M1–M3), then `retriever.py` (M4),
  then run `chat_with_memory.py` (M5).
- Document your process in `../IMPLEMENTATION.md` as you go.
- Commit working milestones before adding complexity.
