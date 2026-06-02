# Project 04: PDF Research Assistant — Code

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

## Run (the full RAG pipeline, and each module on its own)

```bash
python rag.py "What was Q3 revenue?"        # end-to-end: chunk -> retrieve -> answer -> faithfulness
python rag.py "..." path/to/file.pdf        # ...over your own PDF instead of the built-in sample doc

python chunker.py            # M1: split text into overlapping, id-tagged chunks
python retriever.py          # M2: build a Chroma index of chunks, retrieve top-k (Project 03 reuse)
python generator.py          # M3/M4: grounded answer with citations
python faithfulness.py       # M5: faithfulness score (the pure metric runs offline)
```

`rag.py` and the network modules need a provider: set `USE_OLLAMA=1` (with Ollama running) or a
cloud key in `.env`. The pure logic — chunking and the faithfulness *score* — runs with no network.

## Test (one command)

```bash
python -m pytest
```

Guiding tests live in `tests/`. They **fail until you implement the core** (that's the point). The
docstring input/output examples in each module are taken from these tests, so they stay truthful:
- `test_chunker.py` — `chunk_text` overlap + stable ids; fully offline.
- `test_generator.py` — `build_prompt` grounds, includes chunk ids/text, allows refusal; offline.
- `test_faithfulness.py` — `faithfulness_score` = |supported|/|total|; offline.
- `test_config_models.py` — pins the current `config.py` models (Ollama `qwen3.5:4b` /
  `nomic-embed-text`, Groq cloud default); **passes today** and guards against model drift.

`answer()` and `check_faithfulness()` need a provider and are exercised by running `rag.py`, not in
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
| `config.py` | `provided` | tune `Config` (chunk size, top_k); do not edit the canonical provider block |
| `requirements.txt` | `provided` | install once |
| `pdf_loader.py` | `provided` | use `load_pdf()` / `SAMPLE_DOC` |
| `embedding_helpers.py` | `provided` | use `embed_one` / `embed_many` |
| `retriever.py` | `provided` | reuse — `build_index()` / `retrieve()` (your Project 03 retriever) |
| `chunker.py` | `learner` | implement `chunk_text()` — overlapping, id-tagged chunks (M1) |
| `generator.py` | `learner` | implement `build_prompt()` + `answer()` — grounded + cited (M3/M4) — the core |
| `faithfulness.py` | `learner` | implement `faithfulness_score()` + `check_faithfulness()` (M5) |
| `rag.py` | `provided` | run it — the end-to-end pipeline that calls your modules |
| `tests/` | `provided` | guiding tests — make them pass |

Search starter files for `[learner]` and `NotImplementedError` to find your work. The full labeled
contract for each function (with I/O examples) is in `../source/project.md`.

## Notes

- Fill in `../UNDERSTANDING.md` before writing any code here.
- Build in milestone order (see the lesson) — don't write everything at once.
- Document your process in `../IMPLEMENTATION.md` as you go.
- Commit working milestones before adding complexity.
