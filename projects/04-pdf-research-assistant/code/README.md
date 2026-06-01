# Project 04: PDF Research Assistant — Code

> Workflow is standardized across all lab projects. `config.py` (swappable provider) and
> `.env.example` are stamped from the canonical template
> (`skills/lesson-generator/templates/`). Lesson-specific starter code and guiding tests are
> added when this lesson is authored — see `../source/project.md`.

## Setup

```bash
# From this directory
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

uv pip install -r requirements.txt

cp .env.example .env       # then put your API key(s) in .env
```

## Run (one command)

```bash
python rag.py
```

## Test (one command)

```bash
python -m pytest
```

Guiding tests live in `tests/` (added with the lesson). They should fail until you
implement the core and run without a network where possible.

## Provider (swappable by key)

`config.py` picks the model from whichever API key is in `.env` — **Groq (free tier)** is
preferred, then Anthropic, then OpenAI. Override with `CHATBOT_MODEL`. No code change is
needed to switch providers (LiteLLM routes by the model string).

## File Roles

Labeled per `OPERATING_RULES.md` §Scaffolding — `provided` (complete) · `partial` (starter
+ `TODO(learner)`) · `learner` (you write the core) · `reference` (docs):

| File | Role | You... |
|------|------|--------|
| `.env.example` | `provided` | copy to `.env`, add a key |
| `config.py` | `provided` | tune `Config`; do not edit the canonical provider block |
| `requirements.txt` | `provided` | install once |
| `rag.py` | `learner` | build the core — full labeled spec in `../source/project.md` |

Search starter files for `TODO(learner)` and `NotImplementedError` to find your work.

## Notes

- Fill in `../UNDERSTANDING.md` before writing any code here.
- Build in milestone order (see the lesson) — don't write everything at once.
- Document your process in `../IMPLEMENTATION.md` as you go.
- Commit working milestones before adding complexity.
