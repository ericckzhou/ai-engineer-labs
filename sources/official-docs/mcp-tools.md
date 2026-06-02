# Model Context Protocol - Tools

**Type:** official-doc
**Tier:** 1 (Official Doc)
**Author(s):** Model Context Protocol
**Date:** 2025-06-18
**URL:** https://modelcontextprotocol.io/specification/2025-06-18/server/tools
**Accessed:** 2026-06-02

## Why This Source Matters

This is the primary source for MCP tools. It connects directly to Projects 06 and 08: the learner already knows tool definitions inside one app loop; MCP tools show how those definitions become discoverable and callable across a protocol boundary.

## Key Claims

- MCP tools are model-controlled capabilities that servers expose for language models to invoke.
- A tool definition includes a unique `name`, optional `title`, human-readable `description`, `inputSchema`, optional `outputSchema`, and optional annotations.
- Clients discover tools with `tools/list` and invoke tools with `tools/call`.
- Tool results can include unstructured `content`, `structuredContent`, resource links, or embedded resources.
- Tool errors are separated into protocol errors and tool execution errors; execution errors can be returned with `isError: true`.
- Servers must validate tool inputs, implement access controls, rate limit invocations, and sanitize outputs.
- Clients should show tool inputs, request confirmation for sensitive operations, validate results, set timeouts, and log usage.

## Relevant To

- concepts: [mcp-tools, tool-schema, structured-output, tool-result, tool-security, provider-consumer-split]
- projects: [06-ai-coding-copilot, 08-ai-agent, 09-personal-learning-os, elective-mcp-interface-layer]

## Notes

MCP tools should not be taught as "more function calling." The useful distinction is that the tool provider is now decoupled from the host that consumes it.
