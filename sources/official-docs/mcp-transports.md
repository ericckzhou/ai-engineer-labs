# Model Context Protocol - Transports

**Type:** official-doc
**Tier:** 1 (Official Doc)
**Author(s):** Model Context Protocol
**Date:** 2025-06-18
**URL:** https://modelcontextprotocol.io/specification/2025-06-18/basic/transports
**Accessed:** 2026-06-02

## Why This Source Matters

This is the primary source for MCP transports. It gives the future MCP lab a precise way to teach local-process versus remote-server integration without confusing transport with the protocol itself.

## Key Claims

- MCP separates the data layer from the transport layer: the JSON-RPC protocol remains the same while transport changes how messages move.
- Stdio transport uses standard input/output streams for local process communication.
- Streamable HTTP transport supports remote servers using HTTP POST with optional server-sent events for streaming.
- Transport choice changes operational constraints, including logging, authentication, lifecycle, and who can connect.
- Local stdio servers are simple and fast but run as local processes; remote HTTP servers need stronger authorization and network security.

## Relevant To

- concepts: [mcp-transport, stdio-transport, streamable-http, json-rpc, local-server, remote-server]
- projects: [06-ai-coding-copilot, 08-ai-agent, 09-personal-learning-os, elective-mcp-interface-layer]

## Notes

For a first MCP lab, stdio should be the provided default. Streamable HTTP belongs in explanation and optional extension unless the learner needs remote access.
