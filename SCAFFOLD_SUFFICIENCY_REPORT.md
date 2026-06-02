# Scaffold Sufficiency Report — `solns` vs `main`

> **solns-branch artifact.** Produced by implementing a verified reference solution for every
> project and cross-referencing the result against the `main` scaffold. The question:
> **is the provided template sufficient for a learner to reach a green offline gate by
> filling only the labeled learner stubs?**
>
> **Do not merge to `main`.**

## Method

For each project: fill every `[learner]`/`[partial]` stub, create a fresh venv, `pip install
-r requirements.txt`, run `pytest`. The provided test suite is the gate. "Sufficient" =
the suite goes green with **only** learner-owned files changed (config/provided untouched).

## Result: 9 of 10 sufficient; 1 (P03) had provided-scaffold defects

| Project | Offline gate | Learner-only diff? | Verdict |
|---|---|---|---|
| P01 ai-chatbot | 13 passed | yes | ✅ sufficient |
| P02 token-embedding-explorer | 27 passed | yes | ✅ sufficient |
| **P03 semantic-search** | 17 passed *(after fix)* | **no — 2 provided tests edited** | ⚠️ **insufficient** |
| P04 pdf-research-assistant | 16 passed | yes | ✅ sufficient |
| P05 personal-memory-system | 20 passed | yes | ✅ sufficient |
| P06 ai-coding-copilot | 18 passed | yes | ✅ sufficient |
| P07 ai-evaluation-framework | 20 passed | yes | ✅ sufficient |
| P08 ai-agent | 25 passed | yes | ✅ sufficient |
| P09 personal-learning-os | 28 passed | yes | ✅ sufficient |
| Elective mcp-interface-layer | 26 passed | yes | ✅ sufficient |

**Total: 210 offline tests green across the curriculum.** Each project's `git diff main..solns`
is exactly its learner stubs + a `SOLUTION_NOTES.md`, confirming the difficulty boundary is
solvable and nothing leaked into provided files — **except P03**.

## The one insufficiency — P03 (must be fixed on `main`)

Running the P03 reference solution against the real `chromadb` (1.5.9) surfaced **two
provided-test defects**. They are independent of the learner's work — a learner on `main`
hits the same red suite on a clean checkout:

1. **`tests/test_indexer.py`** — collection names `"t1"`/`"t2"` (2 chars) violate chromadb's
   current 3–512 char rule → `InvalidArgumentError`. Renamed to `"idx_count"`/`"idx_idem"`.
2. **`tests/conftest.py`** — the `cosine_collection` fixture creates collection `"test"` on a
   shared in-memory `chromadb.Client()`; the 2nd test using it dies with
   `Collection [test] already exists`. Added a `delete_collection` guard so the fixture is
   re-entrant.

These two fixes live on `solns` in commit `bcea12b`. **They belong on `main`** (they fix the
provided scaffold, not the answer). Recommended: cherry-pick `bcea12b` onto `main`.

## Secondary observations (not blocking, worth noting)

- **No requirements pinning.** Every `requirements.txt` is unpinned (`chromadb`, `litellm`,
  `mcp`, …). P03's failure was a direct consequence: an unpinned `chromadb` rolled to 1.5.9
  and tightened name validation. Consider pinning or adding lower bounds, especially for
  `chromadb` and `mcp`, so the provided suite can't silently rot.
- **`asyncio_mode` pytest warning** appears in every project (an unknown config option in the
  shared `pyproject.toml`). Harmless, but it's noise on every run — worth removing or wiring
  up `pytest-asyncio` if async tests are intended.
- **Provider-dependent paths are untested by design** (`stream_completion`, `embed`, `answer`,
  `check_faithfulness`, the live agent/judge calls). The offline gate verifies pure logic and
  injected-`complete` loops; each `SOLUTION_NOTES.md` lists the exact live-smoke command that
  still needs a one-time manual run with a provider (Ollama or a key).

## Bottom line

The scaffolding standard holds: setup is solved, the learning target is genuinely incomplete,
and the labeled boundary is solvable end-to-end. The template is **sufficient for 9/10**; P03's
provided test suite needs the `bcea12b` fix ported to `main` to be sufficient on a clean
checkout with current dependencies.
