# Project 07: AI Evaluation Framework — Code

## Setup

`ash
# From this directory
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

uv pip install litellm python-dotenv rich pandas

cp ../.env .env  # or create fresh with API keys
`

## Run

`ash
python regression_runner.py
`

## Files

See ../PROJECT.md for the expected file structure.

Build each file in order — don't write everything at once.

## Notes

- Fill in ../UNDERSTANDING.md before writing any code here.
- Document your process in ../IMPLEMENTATION.md as you go.
- Commit working milestones before adding complexity.
