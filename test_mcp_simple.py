#!/usr/bin/env python3
"""
Simple test to verify MCP server functions work
"""

import json
import asyncio
from mcp import types
from mcp_server import list_tools, call_tool

async def test_mcp_functions():
    """Test MCP functions directly"""
    print("Testing MCP Server Functions...")
    
    # Test list_tools
    print("\n1. Testing list_tools:")
    tools = await list_tools()
    for tool in tools:
        print(f"   Tool: {tool.name}")
        print(f"   Description: {tool.description[:80]}...")
    
    # Test call_tool
    print("\n2. Testing call_tool:")
    test_args = {"query": "vector search tutorial", "limit": 2}
    result = await call_tool("search_website", test_args)
    
    print(f"   Result type: {type(result)}")
    print(f"   Number of content blocks: {len(result)}")
    if result:
        content = result[0].text
        lines = content.split('\n')
        print(f"   First line: {lines[0]}")
        print(f"   Total lines: {len(lines)}")
    
    print("\n✅ MCP functions test completed!")

if __name__ == "__main__":
    asyncio.run(test_mcp_functions())