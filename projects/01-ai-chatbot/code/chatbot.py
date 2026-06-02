"""chatbot.py — [learner] The conversation loop. THIS is the project.

Actually talking to the model and managing history so the bot remembers the conversation is the
work. There is no offline test here (it needs a provider) — the [learner] docstrings carry a
behavioral Example showing the expected shape.

PROVIDED: command dispatch (/cost, /reset, /system, /quit) and the wiring to config / cost_tracker
/ context.
LEARNER: stream_completion() and the one-turn block inside run_repl() (both marked [learner]).

Run:  python chatbot.py     (needs a provider — USE_OLLAMA=1 or a cloud key)
"""
from __future__ import annotations

import litellm

from config import Config, load_config
from context import estimate_tokens, trim_to_budget
from cost_tracker import CostTracker


def stream_completion(history: list[dict], cfg: Config) -> tuple[str, dict]:
    """[learner] Call the model with streaming; print tokens as they arrive; return (full_text, usage).

    Steps:
      1. call litellm.completion(model=cfg.model, messages=history, stream=True, ...) — pass
         temperature/max_tokens from cfg.
      2. iterate the stream; for each chunk print the content delta (end="", flush=True) AND
         append it to a running string.
      3. capture the final token usage. Streamed chunks may not carry usage — request it
         (stream_options={"include_usage": True}) or fall back to estimate_tokens(). See lesson
         §3 Implementation Details.
      4. return (full_text, usage).

    Example (behavioral — needs a provider, so there is no offline test; shape, not exact text):
        history = [{"role": "system", "content": "..."}, {"role": "user", "content": "hi"}]
        text, usage = stream_completion(history, cfg)
        # tokens print to stdout as they arrive, then:
        isinstance(text, str)                              # the full assembled reply
        usage["input_tokens"], usage["output_tokens"]      # ints → feed CostTracker.record()
    """
    stream = litellm.completion(
        model=cfg.model,
        messages=history,
        stream=True,
        temperature=cfg.temperature,
        max_tokens=cfg.max_tokens,
        stream_options={"include_usage": True},  # ask the provider to send usage on the final chunk
    )

    parts: list[str] = []
    usage_obj = None
    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            print(delta, end="", flush=True)
            parts.append(delta)
        # The final chunk (after content) carries usage when include_usage is honored.
        if getattr(chunk, "usage", None):
            usage_obj = chunk.usage
    print()  # newline after the streamed reply

    full_text = "".join(parts)

    if usage_obj is not None:
        usage = {
            "input_tokens": usage_obj.prompt_tokens,
            "output_tokens": usage_obj.completion_tokens,
        }
    else:
        # Provider didn't return usage on the stream — fall back to a local estimate so the
        # cost tracker still gets integers to work with.
        usage = {
            "input_tokens": estimate_tokens(history),
            "output_tokens": estimate_tokens([{"role": "assistant", "content": full_text}]),
        }

    return full_text, usage


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

        # --- one conversation turn ([learner]) ---
        # Steps:
        #   1. append the user turn: history.append({"role": "user", "content": user}).
        #   2. guard the budget: history = trim_to_budget(history, cfg.context_budget, ...).
        #   3. text, usage = stream_completion(history, cfg).
        #   4. append the assistant turn: history.append({"role": "assistant", "content": text}).
        #      Appending BOTH roles is what gives the bot memory — forgetting the assistant
        #      append is the #1 bug (the bot acts amnesiac). (lesson §9 Common Mistakes)
        #   5. cost = tracker.record(cfg.model, usage["input_tokens"], usage["output_tokens"]);
        #      print the per-turn cost.
        history.append({"role": "user", "content": user})
        history = trim_to_budget(history, cfg.context_budget, cfg.system_prompt)
        text, usage = stream_completion(history, cfg)
        # Appending the assistant turn is what gives the bot memory (lesson §9).
        history.append({"role": "assistant", "content": text})
        cost = tracker.record(cfg.model, usage["input_tokens"], usage["output_tokens"])
        print(f"  (turn cost: ${cost:.6f})")


def main() -> None:
    run_repl(load_config())


if __name__ == "__main__":
    main()
