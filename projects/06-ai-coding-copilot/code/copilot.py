"""copilot.py — [provided] The orchestrator. Wires context injection + the tool loop together.

This is the runnable copilot: it injects the top-k relevant files as starting context (provided
retrieval), then runs YOUR agent loop (agent_loop.run_agent) with a REAL LiteLLM completion so the
model can read more of the repo via tools. PROVIDED — your work is safe_resolve, dispatch_tool,
parse_tool_calls, and run_agent. Once those four are implemented, this answers questions about a
repository end to end.

Run:  python copilot.py "where is the default model configured?" --repo .
"""
from __future__ import annotations

import argparse

import litellm

from agent_loop import run_agent
from config import load_config
from context_selector import select_context
from tools import TOOL_SCHEMAS

SYSTEM = (
    "You are a coding copilot answering questions about a specific repository. "
    "Use the tools to read and search the repo before answering — do NOT guess about code you have "
    "not read. Cite the files (and line numbers when you can) that you used. If the answer is not "
    "in the repo, say so plainly."
)


def make_complete(cfg):
    """Return a `complete(messages, tools)` that calls the model and returns its message."""
    def complete(messages, tools):
        resp = litellm.completion(
            model=cfg.model, messages=messages, tools=tools, tool_choice="auto",
            temperature=cfg.temperature, max_tokens=cfg.max_tokens,
        )
        return resp.choices[0].message
    return complete


def answer(question: str, repo_root: str) -> str:
    cfg = load_config()
    messages: list = [{"role": "system", "content": SYSTEM}]

    # Context injection (provided): seed the prompt with the most relevant files. If the embeddings
    # provider is unavailable, skip it — the tool loop alone can still find the files.
    try:
        ctx = select_context(repo_root, question, k=cfg.top_k_files)
        if ctx:
            blob = "\n\n".join(f"# {path}\n{text[:2000]}" for path, text in ctx)
            messages.append({"role": "user",
                             "content": f"Possibly relevant files (you may read more via tools):\n\n{blob}"})
    except Exception as e:  # noqa: BLE001 — context is best-effort; tools are the real grounding
        messages.append({"role": "system", "content": f"(context injection skipped: {e})"})

    messages.append({"role": "user", "content": question})
    return run_agent(messages, repo_root, make_complete(cfg),
                     tools=TOOL_SCHEMAS, max_steps=cfg.max_agent_steps)


def main() -> None:
    ap = argparse.ArgumentParser(description="Ask the copilot a question about a repository.")
    ap.add_argument("question", help="The question to answer about the repo.")
    ap.add_argument("--repo", default=load_config().repo_root,
                    help="Path to the repository to operate in (default: COPILOT_REPO_ROOT or '.').")
    args = ap.parse_args()
    print(answer(args.question, args.repo))


if __name__ == "__main__":
    main()
