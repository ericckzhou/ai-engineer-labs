# Model Context Protocol - Build an MCP Server

**Type:** official-doc
**Tier:** 1 (Official Doc)
**Author(s):** Model Context Protocol
**Date:** 2025-06-18
**URL:** https://modelcontextprotocol.io/docs/develop/build-server
**Accessed:** 2026-06-02

## Why This Source Matters

This is the practical official guide for building an MCP server. It should be treated as implementation scaffolding, while the architecture and specification pages remain the conceptual authority.

## Key Claims

- An MCP server can expose three main capability types: resources, tools, and prompts.
- A simple first server can use the Python MCP SDK and `FastMCP` to register tools from typed functions and docstrings.
- Stdio servers must not write logs to stdout because stdout carries JSON-RPC protocol messages; logs should go to stderr or a file.
- The official guide demonstrates connecting a local server to a host such as Claude Desktop.
- The SDK is a convenience layer over MCP concepts; learners still need to understand handlers, schemas, resources, transports, and host configuration.

## Relevant To

- concepts: [mcp-server, fastmcp, server-scaffolding, stdio-logging, host-configuration]
- projects: [06-ai-coding-copilot, 08-ai-agent, 09-personal-learning-os, elective-mcp-interface-layer]

## Notes

For this curriculum, boilerplate server bootstrapping should be provided. Learners should own handlers, schemas, resources, prompts, and security checks.
