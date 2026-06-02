# OpenTelemetry - Generative AI Semantic Conventions

**Type:** official-doc
**Tier:** 1 (Official Doc)
**Author(s):** OpenTelemetry
**Date:** 2026
**URL:** https://opentelemetry.io/docs/specs/semconv/gen-ai/
**Accessed:** 2026-06-02

## Why This Source Matters

This is the primary source for standard observability vocabulary around generative AI systems. It strengthens Project 07 and Project 09 by turning evaluation traces into structured telemetry concepts rather than ad hoc logs.

## Key Claims

- OpenTelemetry semantic conventions define common attribute names for operations and telemetry so different tools can interpret traces consistently.
- The GenAI conventions cover LLM operations and agent/framework spans.
- GenAI telemetry can describe model requests, responses, finish reasons, usage, errors, and framework-level operations.
- Standardized trace attributes make it easier to compare runs across models, prompts, tools, and deployments.
- Observability is separate from evaluation but supports evaluation by preserving run context, costs, errors, and model behavior over time.

## Relevant To

- concepts: [agent-observability, genai-telemetry, tracing, evaluation-traces, regression-testing]
- projects: [07-ai-evaluation-framework, 08-ai-agent, 09-personal-learning-os]

## Notes

Use this as a production vocabulary source, not as a requirement to instrument every project. Project 07 can stay lightweight while teaching why traces and eval records should share stable fields.
