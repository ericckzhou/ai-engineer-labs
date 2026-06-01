"""chatbot.py — [learner] The conversation loop. THIS is the project.

Provided for you: command dispatch (/cost, /reset, /system, /quit), and the wiring to
config / cost_tracker / context. Left for you: actually talking to the model and managing
history so the bot remembers the conversation. Search for `TODO(learner)`.

Run:  python chatbot.py
"""
from __future__ import annotations

import litellm

from config import Config, load_config
from context import trim_to_budget
from cost_tracker import CostTracker


def stream_completion(history: list[dict], cfg: Config) -> tuple[str, dict]:
    """Call the model with streaming; print tokens as they arrive; return (full_text, usage).

    LEARNER TODO:
      - call litellm.completion(model=..., messages=history, ..., stream=True)
      - print each content delta as it arrives (end="", flush=True)
      - accumulate the full text AND capture final token usage
        (streamed chunks may not carry usage — see lesson §3 Implementation Details)
    """
    raise NotImplementedError("Implement stream_completion() — see lesson §4 Example 3")


def run_repl(cfg: Config) -> None:
    history: list[dict] = [{"role": "system", "content": cfg.system_prompt}]
    tracker = CostTracker()
    print(f"chatbot [{cfg.model}] — commands: /cost  /reset  /system <text>  /quit")

    while True:
        try:
            user = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user:
            continue

        # --- command dispatch (provided) ---
        if user == "/quit":
            break
        if user == "/cost":
            print(tracker.summary())
            continue
        if user == "/reset":
            history = [{"role": "system", "content": cfg.system_prompt}]
            print("(history reset)")
            continue
        if user.startswith("/system "):
            history[0] = {"role": "system", "content": user[len("/system "):]}
            print("(system prompt updated)")
            continue

        # --- one conversation turn (LEARNER TODO) ---
        # TODO(learner): append the user turn; guard the budget with trim_to_budget();
        # call stream_completion(); append the assistant turn (BOTH roles!); then
        # record + print the cost for the turn. Forgetting the assistant append is the
        # #1 bug — the bot will act amnesiac. (lesson §9 Common Mistakes)
        raise NotImplementedError("Implement the conversation turn in run_repl()")


def main() -> None:
    run_repl(load_config())


if __name__ == "__main__":
    main()
