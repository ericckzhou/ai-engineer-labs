# Project 02: Token & Embedding Explorer — Code

> Workflow is standardized across all lab projects. `config.py` (swappable provider) and
> `.env.example` are stamped from the canonical template
> (`skills/lesson-generator/templates/`). The four learner modules and guiding tests are
> specified in `../source/project.md` and taught in `../source/lesson.agent.md`.

## Setup

```bash
# From this directory
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

uv pip install -r requirements.txt

cp .env.example .env       # then put your API key(s) in .env
```

## Run (one module at a time, in milestone order)

```bash
python tokenizer_explorer.py     # M1: tokens, IDs, count, round-trip (no network)
python embedding_explorer.py     # M3: embed text, read the vector's dimension
python similarity_calculator.py  # M4: cosine from scratch on a paraphrase vs. unrelated pair
python corpus_search.py          # M5: rank a small corpus against a query by cosine
```

The embedding modules need a provider: set `USE_OLLAMA=1` (with Ollama running) or a cloud key in
`.env`. `tokenizer_explorer.py` and the cosine math run with no network.

## Test (one command)

```bash
python -m pytest
```

Guiding tests live in `tests/`. They **fail until you implement the core** (that's the point) and
run without a network where possible:
- `test_similarity.py` — cosine invariants (`cos(v,v)=1`, `cos(v,-v)=-1`, bounds), fully offline.
- `test_corpus_search.py` — ranking logic with a fake `embed`, fully offline.
- `test_tokenizer.py` — lossless round-trip; skips if the `tiktoken` encoding can't load offline.

## Provider (swappable by key)

`config.py` picks the model from whichever API key is in `.env` — **Groq (free tier)** is
preferred, then Anthropic, then OpenAI. Override with `CHATBOT_MODEL`. No code change is
needed to switch providers (LiteLLM routes by the model string).

## File Roles

Labeled per `OPERATING_RULES.md` §Scaffolding — `provided` (complete) · `partial` (starter
+ `TODO(learner)`) · `learner` (you write the core) · `reference` (docs):

| File | Role | You... |
|------|------|--------|
| `.env.example` | `provided` | copy to `.env`, add a key (or set `USE_OLLAMA=1`) |
| `config.py` | `provided` | tune `Config`; do not edit the canonical provider block |
| `requirements.txt` | `provided` | install once |
| `tokenizer_explorer.py` | `partial` | implement `encode/decode/token_pieces/count` (M1); harness is provided |
| `embedding_explorer.py` | `partial` | implement `embed()` (M3); printing harness is provided |
| `similarity_calculator.py` | `learner` | implement `cosine_similarity()` from scratch (M4) — the core |
| `corpus_search.py` | `learner` | implement `search()` ranking (M5) |
| `tests/` | `provided` | guiding tests — make them pass |

Search starter files for `[learner]` and `NotImplementedError` to find your work. The full labeled
contract for each function is in `../source/project.md`.

## Notes

- Fill in `../UNDERSTANDING.md` before writing any code here.
- Build in milestone order (see the lesson) — don't write everything at once.
- Document your process in `../IMPLEMENTATION.md` as you go.
- Commit working milestones before adding complexity.
