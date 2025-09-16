# MCP Server for Web Scraper Agent

This directory contains a Model Context Protocol (MCP) server that exposes the web scraper's vector search functionality.

## Files

- `mcp_server.py` - Main MCP server implementing the `search_website(query)` tool
- `fastapi_server.py` - FastAPI REST API server exposing the same functionality
- `test_mcp_simple.py` - Simple test for MCP server functions
- `test_mcp_server.py` - More comprehensive test (requires server setup)

## MCP Server

The MCP server exposes a single tool:

### `search_website(query)`

Searches for similar content in the scraped website database using semantic vector search.

**Parameters:**
- `query` (required): Search query text
- `limit` (optional): Maximum number of results (default: 5, max: 20)  
- `collection` (optional): Database collection name (default: "scraped_content")

**Returns:** Formatted results with page snippets, URLs, and similarity scores.

### Running the MCP Server

```bash
python mcp_server.py
```

The server uses stdio transport to communicate with MCP clients.

## FastAPI Server

The FastAPI server provides a REST API interface to the same search functionality.

### Running the FastAPI Server

```bash
python fastapi_server.py
```

The server runs on http://localhost:8000

### Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /search_query` - Search with query parameters
- `POST /search` - Search with JSON body
- `GET /collections` - List available database collections
- `GET /docs` - Interactive API documentation

### Examples

```bash
# Search using GET with query parameters
curl "http://localhost:8000/search_query?query=python+tutorial&limit=3"

# Search using POST with JSON
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "machine learning", "limit": 5}'

# List collections
curl "http://localhost:8000/collections"
```

## Testing

Both servers can be tested with the provided test scripts:

```bash
# Test MCP server functions
python test_mcp_simple.py

# Test FastAPI endpoints (requires server to be running)
curl "http://localhost:8000/search_query?query=test"
```

## Requirements

See `requirements.txt` for dependencies. Key packages:
- `mcp` - Model Context Protocol implementation
- `fastapi` - REST API framework  
- `uvicorn` - ASGI server for FastAPI
- Plus existing scraper dependencies