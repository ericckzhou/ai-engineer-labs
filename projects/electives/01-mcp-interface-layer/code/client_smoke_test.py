"""client_smoke_test.py — [provided] CONSUMER #1: a programmatic MCP client over stdio.

This is the first of the TWO consumers your Definition of Done requires. It launches server.py
as a subprocess, runs the MCP lifecycle (initialize → capability negotiation), DISCOVERS the
surface (list_tools / list_resources / list_prompts), then EXERCISES it (call_tool, read a
resource, get the prompt). It imports nothing from your code — it only speaks the protocol.
That is the whole point: a consumer fully decoupled from the provider.

The second consumer is a different HOST (Claude Desktop or the MCP Inspector) — see README
"Two consumers". Run a save here, then read it there (or vice-versa) to prove one server,
many hosts.

Run:   python client_smoke_test.py
       (requires the learner cores implemented; otherwise tool calls return "Error: ...")
"""
from __future__ import annotations

import sys

import anyio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = StdioServerParameters(command=sys.executable, args=["server.py"])


async def _main() -> None:
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()  # capability negotiation handshake
            print(f"connected to: {init.serverInfo.name} v{init.serverInfo.version}")

            tools = await session.list_tools()
            print("tools:", [t.name for t in tools.tools])

            print("save:", await session.call_tool(
                "memory_save", {"text": "the StarcallOS demo is on June 20", "kind": "episodic"}))
            print("save:", await session.call_tool(
                "memory_save", {"text": "I prefer dark mode", "kind": "semantic"}))
            print("search:", await session.call_tool("memory_search", {"query": "demo"}))

            resources = await session.list_resources()
            uris = [str(r.uri) for r in resources.resources]
            print("resources:", uris)
            if uris:
                print("read:", await session.read_resource(uris[0]))

            prompts = await session.list_prompts()
            print("prompts:", [p.name for p in prompts.prompts])
            if any(p.name == "reflect_on" for p in prompts.prompts):
                print("prompt:", await session.get_prompt("reflect_on", {"topic": "StarcallOS"}))


if __name__ == "__main__":
    anyio.run(_main)
