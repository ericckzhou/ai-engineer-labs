# Project 9: Personal Learning OS

## What We're Building

A personal AI operating system that orchestrates memory (Project 5), retrieval (Projects 3–4), agents (Project 8), and evaluation (Project 7) into a unified system for personal knowledge management and learning. This is the direct prototype for StarcallOS architectural patterns.

## Why We're Building It

This is the synthesis project. Every previous project taught you a component. Now you design the system that makes them work together. Personal AI operating systems are the emerging category — the AI that knows you, learns from you, and works for you across time.

## Learning Objectives

- [ ] Design a multi-component AI system with clear interfaces between components
- [ ] Integrate memory, retrieval, agents, and evaluation into one product
- [ ] Design for extensibility: how do you add a new component without breaking others?
- [ ] Define the data model for a personal knowledge graph
- [ ] Implement a query router that chooses the right component for each task
- [ ] Evaluate the system holistically (not just individual components)
- [ ] Apply the "Build vs. Buy" lens to a full system architecture

## Key Concepts

System design, orchestration, query routing, knowledge graphs, data models, component interfaces, extensible architecture, AI product thinking

## Core Engineering Problem

**Problem:** You have memory, search, agents, and evaluation working independently. How do you compose them into a coherent system that a user can actually rely on — without the complexity growing unmanageable?

## Time Estimate

**Total:** 15–20 hours

## Startup Lens

This project IS a startup idea. Personal AI OS is the product category that Apple, Google, Microsoft, and dozens of startups are racing to define. What you build here is a working proof-of-concept for a real product.

## Key Files

```
code/
  os_core.py            — Main orchestration layer
  query_router.py       — Route tasks to right component
  knowledge_graph.py    — Personal knowledge data model
  component_registry.py — Register and manage components
  integration/
    memory_adapter.py   — Wraps Project 5 memory system
    search_adapter.py   — Wraps Project 3 semantic search
    agent_adapter.py    — Wraps Project 8 agent
    eval_adapter.py     — Wraps Project 7 evaluation
  cli.py                — User interface
  evaluate_system.py    — Holistic system evaluation
  requirements.txt
  README.md
```
