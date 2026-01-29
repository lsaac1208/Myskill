#!/usr/bin/env python3
"""
本地搜索 MCP 服务器 - 简化版
"""

import asyncio
import json
from typing import Any
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
)
from ddgs import DDGS

server = Server("local-search")

@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    return []

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="search",
            description="使用 DuckDuckGo 进行本地网络搜索，不消耗 GLM MCP 额度",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search":
        query = arguments.get("query")

        try:
            ddgs = DDGS()
            results = list(ddgs.text(query, max_results=10))

            if not results:
                return [TextContent(type="text", text=f"未找到关于 '{query}' 的搜索结果")]

            output = f"🔍 搜索: {query}\n📊 找到 {len(results)} 条结果\n\n"

            for i, result in enumerate(results[:10], 1):
                title = result.get('title', '无标题')
                url = result.get('href', '')
                body = result.get('body', '')

                output += f"{i}. {title}\n"
                output += f"   🔗 {url}\n"
                if body:
                    preview = body[:100] + "..." if len(body) > 100 else body
                    output += f"   📝 {preview}\n"
                output += "\n"

            return [TextContent(type="text", text=output)]

        except Exception as e:
            return [TextContent(type="text", text=f"搜索失败: {str(e)}")]

    else:
        raise ValueError(f"未知工具: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="local-search",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
