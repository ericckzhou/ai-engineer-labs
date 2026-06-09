# Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection

**Type:** paper
**Authors:** Greshake, Abdelnabi, Mishra, Endres, Holz, Fritz
**Year:** 2023 (submitted Feb 2023; rev. May 2023)
**arXiv:** 2302.12173 — https://arxiv.org/abs/2302.12173

> Primary source for **Elective 02 — Guardrails & Safety Layer** (the indirect-injection threat
> model that ties guarding to retrieval / Project 04). Faithful summary; arXiv PDF is canonical.

---

## Core thesis

LLM-integrated applications blur the boundary between **data** and **instructions**: any text
that reaches the prompt — including text the application *retrieved on the user's behalf* — can
be interpreted as a command. The user no longer has to be the attacker.

## Threat model — indirect prompt injection

Instead of interacting with the LLM directly, an adversary **plants malicious instructions in
content that the application is likely to retrieve** (a web page, a PDF, an email, a calendar
entry). When the app fetches that content and places it in the model's context, the hidden
instructions become live commands. The injection is *indirect*: it arrives through the data
channel, not the user's prompt.

## Demonstrated attack categories

- **Data theft / exfiltration** of conversation or system data.
- **Worming** — self-propagating injections that spread to other content/users.
- **Information ecosystem contamination** — poisoning sources future retrievals will trust.
- **Remote control of functionality** — manipulating the app's tool/API calls.

## Defenses

The authors are explicit that **robust mitigations are currently lacking** — the paper raises and
characterizes the threat rather than solving it. This is itself a key lesson: there is no single
fix; defense is layered and incomplete.

## Why it anchors the elective

This is the reason scanning *only the user's prompt* is insufficient. In a RAG system (Project
04), the dangerous text is in the **retrieved document**. The elective therefore must guard the
retrieved context, not just the user input — and must frame guarding as risk reduction over an
unsolved problem, not a fix.

## Known issues / cautions

- Treating retrieved content as trusted is the core mistake; in a guarded system, retrieved text
  is *untrusted input* exactly like user input (cf. Project 06: "tool arguments are untrusted
  model input").
