#!/usr/bin/env python3
"""
Demo script for MCP Server functionality

This script demonstrates how to:
1. Add sample data to the vector database
2. Use the MCP server to search the data
3. Use the FastAPI server to search the data
"""

import asyncio
import requests
from demo_embeddings import add_mock_embeddings
from vector.database import VectorDatabaseManager
from embeddings_processor import search_website_data


def create_sample_data():
    """Create some sample documents for testing."""
    print("Creating sample data for testing...")

    sample_docs = [
        {
            "title": "Python Vector Search Tutorial",
            "url": "https://example.com/python-vector-search",
            "description": "Learn how to implement vector search using embeddings and similarity matching in Python",
            "content": "Vector search is a powerful technique for finding similar documents using machine learning embeddings. This tutorial covers the basics of vector databases, semantic search, and similarity scoring using Python libraries like sentence-transformers and chromadb.",
        },
        {
            "title": "Machine Learning with FastAPI",
            "url": "https://example.com/ml-fastapi",
            "description": "Building machine learning APIs using FastAPI framework",
            "content": "FastAPI is an excellent framework for building machine learning APIs. It provides automatic API documentation, request validation, and high performance. This guide shows how to deploy ML models as REST APIs using FastAPI and uvicorn.",
        },
        {
            "title": "Web Scraping Best Practices",
            "url": "https://example.com/scraping-guide",
            "description": "Comprehensive guide to ethical and effective web scraping",
            "content": "Web scraping is the process of extracting data from websites. This guide covers ethical scraping practices, handling different content types, rate limiting, and using tools like BeautifulSoup and requests for robust web scraping.",
        },
    ]

    db_manager = VectorDatabaseManager(database_type="chroma")
    stored_ids = []

    for i, doc in enumerate(sample_docs, 1):
        print(f"  Adding document {i}: {doc['title']}")

        # Add mock embeddings
        enhanced_doc = add_mock_embeddings(doc)

        # Store in database
        doc_id = db_manager.store_document_with_embeddings(enhanced_doc)
        stored_ids.append(doc_id)

    print(f"✅ Created {len(stored_ids)} sample documents")
    return stored_ids


def test_search_function():
    """Test the search function directly."""
    print("\nTesting search function...")

    test_queries = [
        "python tutorial",
        "machine learning API",
        "web scraping",
        "vector embeddings",
        "nonexistent topic",
    ]

    for query in test_queries:
        print(f"\n  Query: '{query}'")
        result = search_website_data(query, limit=2)

        if result["success"] and result["count"] > 0:
            print(f"    Found {result['count']} results:")
            for r in result["results"]:
                print(f"      - {r['title']} (score: {r['similarity_score']})")
        else:
            print("    No results found")


async def test_mcp_server():
    """Test MCP server functionality."""
    print("\nTesting MCP Server...")

    from mcp_server import call_tool

    test_args = {"query": "python machine learning", "limit": 2}
    result = await call_tool("search_website", test_args)

    if result:
        print("  MCP server response:")
        lines = result[0].text.split("\n")
        print(f"    {lines[0]}")  # First line summary
        print(f"    (Full response has {len(lines)} lines)")

    print("✅ MCP Server test completed")


def test_fastapi_server():
    """Test FastAPI server (requires server to be running)."""
    print("\nTesting FastAPI Server...")

    try:
        # Test basic endpoint
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("  FastAPI server is running ✅")

            # Test search endpoint
            search_response = requests.get(
                "http://localhost:8000/search_query",
                params={"query": "python tutorial", "limit": 2},
                timeout=5,
            )

            if search_response.status_code == 200:
                data = search_response.json()
                print(f"  Search returned {data['count']} results ✅")
            else:
                print(f"  Search failed: {search_response.status_code}")
        else:
            print(f"  Health check failed: {response.status_code}")

    except requests.exceptions.RequestException:
        print("  FastAPI server not running (start with: python fastapi_server.py)")


def main():
    """Run the complete demo."""
    print("🚀 MCP Server Demo")
    print("=" * 50)

    # Create sample data
    create_sample_data()

    # Test search function
    test_search_function()

    # Test MCP server
    asyncio.run(test_mcp_server())

    # Test FastAPI server
    test_fastapi_server()

    print("\n" + "=" * 50)
    print("Demo completed! 🎉")
    print("\nNext steps:")
    print("  1. Start FastAPI server: python fastapi_server.py")
    print("  2. Visit http://localhost:8000/docs for interactive API docs")
    print("  3. Start MCP server: python mcp_server.py")
    print("  4. Use the search_website(query) tool in your MCP client")


if __name__ == "__main__":
    main()
