"""[provided] Guiding test for Milestone M3 — generator.build_prompt(). Fully OFFLINE (no provider).

build_prompt is pure message construction, so grounding/citation discipline is testable without a
network. answer() needs a provider and is exercised by running the pipeline, not here. The docstring
example in generator.py mirrors test_build_prompt_grounds_and_cites.
Run: python -m pytest tests/test_generator.py
"""
import generator
from chunker import Chunk


CHUNKS = [
    Chunk("c0", "Q3 revenue was 4.2M, up 8% YoY."),
    Chunk("c1", "Opened a Berlin office in July."),
]


def test_build_prompt_grounds_and_cites():
    msgs = generator.build_prompt("What was Q3 revenue?", CHUNKS)
    # system message first, user message last
    assert msgs[0]["role"] == "system"
    assert msgs[-1]["role"] == "user"
    system = msgs[0]["content"].lower()
    # grounding: answer only from context
    assert "context" in system
    # refusal path is present (the model is allowed/instructed to say it doesn't know)
    assert "don't know" in system or "do not know" in system or "not in the context" in system


def test_build_prompt_includes_chunk_ids_and_text():
    msgs = generator.build_prompt("What was Q3 revenue?", CHUNKS)
    blob = msgs[-1]["content"]
    # ids must be present so the model can cite them
    assert "[c0]" in blob and "[c1]" in blob
    # the actual chunk text must be in the prompt (the model answers FROM it)
    assert "Q3 revenue was 4.2M" in blob


def test_build_prompt_contains_the_question():
    msgs = generator.build_prompt("What was Q3 revenue?", CHUNKS)
    assert "Q3 revenue" in msgs[-1]["content"]
