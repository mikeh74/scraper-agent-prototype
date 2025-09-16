#!/usr/bin/env python3
"""
Test script for the MCP server functionality
"""

import asyncio
import json
from mcp_server import app


async def test_mcp_server():
    """Test the MCP server tools."""
    print("Testing MCP Server Tools...")

    # Test listing tools
    print("\n1. Testing list_tools():")
    tools = await app._list_tools_handler()
    for tool in tools:
        print(f"   Tool: {tool.name}")
        print(f"   Description: {tool.description}")
        print(f"   Schema: {json.dumps(tool.inputSchema, indent=4)}")

    # Test calling the search tool
    print("\n2. Testing call_tool() with search_website:")

    test_cases = [
        {"query": "vector search tutorial", "limit": 3},
        {"query": "python", "limit": 2},
        {"query": "machine learning"},
        {"query": "nonexistent query"},
    ]

    for i, args in enumerate(test_cases, 1):
        print(f"\n   Test case {i}: {args}")
        result = await app._call_tool_handler("search_website", args)
        for content in result:
            if hasattr(content, "text"):
                # Show only first few lines of the response
                lines = content.text.split("\n")
                print(f"     Result: {lines[0]}")
                if len(lines) > 1:
                    print(f"     ... (response has {len(lines)} lines)")

    print("\n✅ MCP Server test completed!")


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
