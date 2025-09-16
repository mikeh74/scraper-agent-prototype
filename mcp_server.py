#!/usr/bin/env python3
"""
MCP Server for Web Scraper Agent

This MCP server exposes a search_website(query) tool that performs vector
similarity search against the scraped and indexed content using the existing
vector database.
"""

import asyncio
import json
from typing import Any, Dict, List

from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from embeddings_processor import search_website_data


# Create the MCP server instance
app = Server("scraper-agent-mcp")


@app.list_tools()
async def list_tools() -> List[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="search_website",
            description="Search for similar content in the scraped website database using semantic vector search",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query text to find similar content",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 5, max: 20)",
                        "minimum": 1,
                        "maximum": 20,
                        "default": 5,
                    },
                    "collection": {
                        "type": "string",
                        "description": "Database collection name (default: 'scraped_content')",
                        "default": "scraped_content",
                    },
                },
                "required": ["query"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls."""
    if name == "search_website":
        query = arguments.get("query")
        limit = arguments.get("limit", 5)
        collection = arguments.get("collection", "scraped_content")

        if not query:
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(
                        {"success": False, "error": "Query parameter is required"},
                        indent=2,
                    ),
                )
            ]

        # Validate limit
        if not isinstance(limit, int) or limit < 1 or limit > 20:
            limit = 5

        # Perform the search
        result = search_website_data(query, collection, limit)

        # Format the response
        if result["success"] and result["count"] > 0:
            # Create a user-friendly response
            response_text = (
                f"Found {result['count']} similar document(s) for query: '{query}'\n\n"
            )

            for i, doc in enumerate(result["results"], 1):
                response_text += f"{i}. {doc['title']}\n"
                response_text += f"   URL: {doc['url']}\n"
                if doc["similarity_score"]:
                    response_text += f"   Similarity: {doc['similarity_score']:.3f}\n"
                if doc["content_snippet"]:
                    response_text += f"   Content: {doc['content_snippet']}\n"
                response_text += "\n"

            # Also include the raw data as JSON
            response_text += "Raw data:\n" + json.dumps(result, indent=2)

        else:
            response_text = json.dumps(result, indent=2)

        return [types.TextContent(type="text", text=response_text)]

    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the MCP server."""
    # Use stdio transport to communicate with the MCP client
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    print("Starting MCP Server for Scraper Agent...", file=__import__("sys").stderr)
    asyncio.run(main())
