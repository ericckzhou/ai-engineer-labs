# Model Context Protocol - Security Best Practices

**Type:** official-doc
**Tier:** 1 (Official Doc)
**Author(s):** Model Context Protocol
**Date:** 2025-06-18
**URL:** https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices
**Accessed:** 2026-06-02

## Why This Source Matters

This is the primary source for MCP-specific security risks. It extends the Project 06 path-containment lesson into a distributed trust boundary: a host may launch or connect to external servers that can expose tools, read resources, and touch local or remote systems.

## Key Claims

- Local MCP servers can introduce arbitrary code execution, data exfiltration, data loss, and command-obfuscation risks if launched without consent and sandboxing.
- Clients should show the exact command before launching a local server and require explicit approval.
- Clients should warn about dangerous command patterns, sensitive filesystem access, broad privileges, and network operations.
- Servers should run with minimal filesystem, network, and system privileges.
- Remote servers need authorization, secure session identifiers, request verification, token audience binding, and least-privilege scopes.
- Broad or wildcard scopes increase blast radius and reduce audit clarity.

## Relevant To

- concepts: [mcp-security, trust-boundary, least-privilege, local-server-risk, tool-sandboxing, consent]
- projects: [06-ai-coding-copilot, 08-ai-agent, 09-personal-learning-os, elective-mcp-interface-layer]

## Notes

This source should anchor the failure analysis for an MCP elective: unsafe server launch commands, over-broad filesystem access, missing input validation, and tool-result poisoning are not edge cases.
