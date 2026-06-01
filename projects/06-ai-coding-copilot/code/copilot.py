"""copilot.py — [learner] The core of Project 06 (AI Coding Copilot). THIS is what you build.

Setup is provided (config.py with swappable provider, .env). The implementation is yours.
The full labeled spec (provided/partial/learner files) is written when this lesson is
authored — see ../source/project.md. Until then this is a runnable skeleton.

Run:  python copilot.py
"""
from __future__ import annotations

from config import load_config


def main() -> None:
    cfg = load_config()
    print(f"Project 06 (AI Coding Copilot) — model: {cfg.model}")
    # TODO(learner): build this project's core. See ../source/project.md and the lesson.
    raise NotImplementedError(
        "Project 06 core not implemented yet — this is your work to build."
    )


if __name__ == "__main__":
    main()
