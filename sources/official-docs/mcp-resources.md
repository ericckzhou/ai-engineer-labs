# Model Context Protocol - Resources

**Type:** official-doc
**Tier:** 1 (Official Doc)
**Author(s):** Model Context Protocol
**Date:** 2025-06-18
**URL:** https://modelcontextprotocol.io/specification/2025-06-18/server/resources
**Accessed:** 2026-06-02

## Why This Source Matters

This is the primary source for MCP resources. Resources are the context counterpart to tools: instead of asking a model to invoke an action, a server exposes data that a host can read and place into model context.

## Key Claims

- MCP resources expose data that clients can read, such as files, schemas, API responses, memory entries, or application-specific objects.
- Each resource is identified by a URI and can include metadata such as name, description, MIME type, and annotations.
- Resources are application-controlled: hosts decide how to present, select, and include resources in model context.
- Servers may support listing resources, reading resources, templates, and change notifications.
- Resource design should make the data boundary explicit: what can be read, how it is identified, and what metadata helps the host decide how to use it.

## Relevant To

- concepts: [mcp-resources, context-data, resource-uri, provider-consumer-split, provenance]
- projects: [04-pdf-research-assistant, 05-personal-memory-system, 09-personal-learning-os, elective-mcp-interface-layer]

## Notes

For a future MCP elective, Project 05 memory entries are a natural resource surface: `memory://entries` and `memory://entry/{id}` can be read by multiple hosts without importing the memory implementation.
