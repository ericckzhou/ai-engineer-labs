# Model Context Protocol - Prompts

**Type:** official-doc
**Tier:** 1 (Official Doc)
**Author(s):** Model Context Protocol
**Date:** 2025-06-18
**URL:** https://modelcontextprotocol.io/specification/2025-06-18/server/prompts
**Accessed:** 2026-06-02

## Why This Source Matters

This is the primary source for MCP prompts. It grounds prompts as reusable protocol-exposed templates, not private strings buried inside one application.

## Key Claims

- MCP prompts let servers expose reusable interaction templates to clients.
- Prompts are user-controlled rather than automatically model-invoked: clients usually present prompts for users or hosts to select.
- Prompts can declare arguments so clients know what inputs are needed.
- Prompts can return structured message content that a host can place into an LLM interaction.
- A prompt surface can encode task workflows, examples, or role instructions without coupling them to one host application.

## Relevant To

- concepts: [mcp-prompts, reusable-prompts, prompt-templates, protocol-interface]
- projects: [01-ai-chatbot, 06-ai-coding-copilot, 09-personal-learning-os, elective-mcp-interface-layer]

## Notes

This source is useful when separating "prompt design" from "application implementation." A future MCP server can expose a `memory-grounded-assistant` prompt alongside tools and resources.
