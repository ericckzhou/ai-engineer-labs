# Model Context Protocol - Architecture

**Type:** official-doc
**Tier:** 1 (Official Doc)
**Author(s):** Model Context Protocol
**Date:** 2025-06-18
**URL:** https://modelcontextprotocol.io/specification/2025-06-18/architecture
**Accessed:** 2026-06-02

## Why This Source Matters

This is the primary source for MCP's architecture. It establishes the provider/consumer split that the curriculum does not teach through hand-wired tools alone: a host coordinates clients, each client connects to one server, and servers expose focused capabilities without owning the whole application loop.

## Key Claims

- MCP follows a client-host-server architecture: the host manages multiple client instances, each client maintains an isolated session with a server, and each server provides specialized context or capabilities.
- MCP is built on JSON-RPC and uses stateful sessions with capability negotiation.
- Servers expose resources, tools, and prompts as MCP primitives.
- Hosts enforce security policies, consent requirements, lifecycle, and context aggregation.
- Servers should be focused and composable; a server should not see the whole conversation or see into other servers.
- Capability negotiation declares which features are available during a session, such as tools, resources, prompts, subscriptions, or sampling.

## Relevant To

- concepts: [mcp, provider-consumer-split, client-host-server, capability-negotiation, protocol-interface]
- projects: [06-ai-coding-copilot, 08-ai-agent, 09-personal-learning-os, elective-mcp-interface-layer]

## Notes

This source grounds MCP as an interface protocol, not an agent framework. It should be used to distinguish a hand-wired Python tool loop from a reusable protocol surface that multiple hosts can consume.
