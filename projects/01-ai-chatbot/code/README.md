# Project 01: AI Chatbot — Code

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
python chatbot.py
```

## Test (one command)

```bash
python -m pytest
```

The provided tests in `tests/` **fail until you implement the core**. Making them pass is
your first checkpoint — and they need no network or API key.

## Provider (swappable by key)

`config.py` picks the model from whichever API key is in `.env` — **Groq (free tier)** is
preferred, then Anthropic, then OpenAI. Override with `CHATBOT_MODEL`. No code change is
needed to switch providers (LiteLLM routes by the model string).

## File Roles

Every file is labeled with its role (see `OPERATING_RULES.md` §Scaffolding Rules):

| File | Role | You... |
|------|------|--------|
| `.env.example` | `provided` | copy to `.env`, add keys |
| `config.py` | `provided` | may tune values; need not edit |
| `tests/test_cost_tracker.py` | `provided` | make these pass |
| `cost_tracker.py` | `partial` | implement `cost_of()` + `record()` |
| `context.py` | `partial` | implement the 3 functions |
| `chatbot.py` | `learner` | build the conversation loop — the heart of the project |

Search the starter files for `TODO(learner)` and `NotImplementedError` to find your work.

## Notes

- Fill in `../UNDERSTANDING.md` before writing any code here.
- Build in milestone order (lesson §7) — don't write everything at once.
- Document your process in `../IMPLEMENTATION.md` as you go.
- Commit working milestones before adding complexity.
