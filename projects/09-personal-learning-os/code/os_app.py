"""os_app.py — [provided] The orchestrator app: run the Personal Learning OS on real requests.

Wires your learner cores into a live system: builds a real LiteLLM-backed `chat`, constructs the
subsystem kernel (make_subsystems), instantiates LearningOS, and runs a REPL. For every request it
prints the chosen ROUTE, the REASON, the ANSWER, and the PROVENANCE (the audit trail).

It calls the learner cores (route_query, LearningOS.handle, the SAVE worker's graph.add), so it raises
NotImplementedError until those are implemented — then it runs end to end (M5).

Run:  python os_app.py                              # interactive REPL
      python os_app.py "remember the demo is June 20"   # one-shot

Try, in order:  "remember that StarcallOS routes requests through a front door"
                "what did I save about StarcallOS?"
                "summarize everything I saved about StarcallOS"
                "what is query routing?"             # -> CHAT (no personal data needed)
"""
from __future__ import annotations

import sys

import litellm

from config import load_config
from knowledge import KnowledgeGraph
from learning_os import LearningOS, Response
from subsystems import MemoryStore, make_subsystems


def make_chat(cfg):
    """Return a `chat(messages) -> str` backed by a real LiteLLM call."""
    def chat(messages: list) -> str:
        resp = litellm.completion(
            model=cfg.model,
            messages=messages,
            temperature=cfg.temperature,
            max_tokens=cfg.max_tokens,
        )
        return resp.choices[0].message.content or ""
    return chat


def _print_response(r: Response) -> None:
    print(f"\n[route: {r.route}]  ({r.reason})")
    print(r.answer)
    if r.provenance:
        print(f"  provenance: {r.provenance}")


def build_os() -> LearningOS:
    cfg = load_config()
    store, graph = MemoryStore(), KnowledgeGraph()
    subsystems = make_subsystems(store, graph, make_chat(cfg))
    print(f"Project 09 (Personal Learning OS) — model: {cfg.model}")
    return LearningOS(subsystems, graph)


def main() -> None:
    os_ = build_os()

    # One-shot mode: everything after the script name is a single request.
    if len(sys.argv) > 1:
        _print_response(os_.handle(" ".join(sys.argv[1:])))
        return

    print("Type a request (or 'quit'). Examples: 'remember …', 'what did I save about …', "
          "'summarize everything I saved about …'.")
    while True:
        try:
            query = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not query:
            continue
        if query.lower() in {"quit", "exit", ":q"}:
            break
        _print_response(os_.handle(query))


if __name__ == "__main__":
    main()
