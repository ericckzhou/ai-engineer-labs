"""server.py — [provided] MCP transport + bootstrapping. NOT the learning target.

This is the boilerplate that turns your SDK-agnostic learner modules into a live MCP server
over stdio. It is the ADAPTER: it reads the plain dicts you defined (TOOL_DEFINITIONS,
PROMPT_DEFINITIONS, list_resources(...)) and carries them across the protocol as MCP types.
You should not need to edit it — and note there is NO agent loop here. The loop lives in the
HOST (Claude Desktop, the smoke-test client, etc.). The server only exposes a surface.

It runs even before you implement the cores: list_tools returns your (initially empty)
TOOL_DEFINITIONS, and a tool call surfaces NotImplementedError as an error result — that is
your feedback. Implement the learner modules and the same wiring lights up.

CRITICAL (stdio): never write to STDOUT. On stdio the protocol *is* stdin/stdout, so a stray
print() corrupts the JSON-RPC stream and breaks the server. Log to STDERR only.

Run:   python server.py            (starts the server; a host launches it the same way)
       (or configure a host — see README "Two consumers")
"""
from __future__ import annotations

import logging
import sys

import anyio
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from config import load_config
from memory_backend import MemoryBackend
from memory_resources import list_resources, read_resource
from memory_tools import TOOL_DEFINITIONS, dispatch
from prompts import PROMPT_DEFINITIONS, get_prompt

logging.basicConfig(level=logging.INFO, stream=sys.stderr)  # stderr, never stdout
log = logging.getLogger("personal-memory")

cfg = load_config()
backend = MemoryBackend()
server: Server = Server(cfg.server_name)


@server.list_tools()
async def _list_tools() -> list[types.Tool]:
    return [
        types.Tool(name=d["name"], description=d["description"], inputSchema=d["inputSchema"])
        for d in TOOL_DEFINITIONS
    ]


@server.call_tool()
async def _call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        result = dispatch(name, arguments or {}, backend)
        return [types.TextContent(type="text", text=result["text"])]
    except Exception as exc:  # SecurityError, NotImplementedError, KeyError → error result
        log.warning("tool %s failed: %s", name, exc)
        return [types.TextContent(type="text", text=f"Error: {exc}")]


@server.list_resources()
async def _list_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri=d["uri"],
            name=d["name"],
            description=d.get("description"),
            mimeType=d.get("mimeType", "text/plain"),
        )
        for d in list_resources(backend)
    ]


@server.read_resource()
async def _read_resource(uri) -> str:
    return read_resource(str(uri), backend)["text"]


@server.list_prompts()
async def _list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name=d["name"],
            description=d.get("description"),
            arguments=[types.PromptArgument(**a) for a in d.get("arguments", [])],
        )
        for d in PROMPT_DEFINITIONS
    ]


@server.get_prompt()
async def _get_prompt(name: str, arguments: dict | None) -> types.GetPromptResult:
    result = get_prompt(name, arguments or {}, backend)
    return types.GetPromptResult(
        description=result.get("description"),
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=result["text"]),
            )
        ],
    )


async def _main() -> None:
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    print(f"{cfg.server_name} v{cfg.server_version} starting on stdio", file=sys.stderr)
    anyio.run(_main)
