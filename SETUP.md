# Setup Guide

## Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) — fast Python package manager
- API keys for at least one LLM provider

## 1. Install uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify: `uv --version`

## 2. Clone / Open the Lab

```bash
cd ai-engineering-lab
```

## 3. Create the Base Environment

```bash
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

## 4. Install Base Dependencies

```bash
uv pip install litellm python-dotenv rich
```

Each project's `code/` directory has its own `requirements.txt` or `pyproject.toml` with project-specific dependencies.

## 5. Set Up API Keys

Create a `.env` file in the root (never commit this):

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Primary — Groq (has a FREE TIER; the lab's default provider)
GROQ_API_KEY=...

# Optional alternatives — set any of these and the default model swaps automatically
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
TOGETHER_API_KEY=...

# For vector search (Project 3+)
# PINECONE_API_KEY=...
# QDRANT_URL=...
```

LiteLLM reads these automatically. Each project's `config.py` picks the default model from
whichever key is present (preference order **Groq → Anthropic → OpenAI**); an explicit
`CHATBOT_MODEL` always wins. You can also switch providers by changing the model string — no
other code changes needed. (The provider-resolution block is the canonical template at
`skills/lesson-generator/templates/config.py`.)

## 6. Verify Setup

```bash
python -c "
import litellm
response = litellm.completion(
    model='groq/llama-3.3-70b-versatile',  # free-tier default; or your provider's model string
    messages=[{'role': 'user', 'content': 'Say hello in one word.'}]
)
print(response.choices[0].message.content)
"
```

## Provider Reference (LiteLLM)

| Provider | Model String | Env Var |
|----------|-------------|---------|
| **Groq (default, free tier)** | `groq/llama-3.3-70b-versatile` | `GROQ_API_KEY` |
| Anthropic | `claude-sonnet-4-6` | `ANTHROPIC_API_KEY` |
| OpenAI | `gpt-4o` | `OPENAI_API_KEY` |
| Together | `together_ai/mistralai/Mixtral-8x7B` | `TOGETHER_API_KEY` |
| Ollama (local) | `ollama/llama3` | — |

See [LiteLLM docs](https://docs.litellm.ai/docs/providers) for the full list.

## Per-Project Setup

Each project's `code/` directory has a `README.md` with project-specific setup. Navigate there and follow the instructions.

```bash
cd projects/01-ai-chatbot/code
uv pip install -r requirements.txt
```

## Secrets Hygiene

- Never commit `.env` files
- Never hardcode API keys in source code
- The `.gitignore` at the root covers `.env` and common credential files
- Use `python-dotenv` to load keys: `from dotenv import load_dotenv; load_dotenv()`
