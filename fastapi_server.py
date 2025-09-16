#!/usr/bin/env python3
"""
FastAPI endpoint for the Web Scraper Agent MCP Server

This provides a REST API interface to the vector search functionality,
complementing the MCP server interface.
"""

from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
import uvicorn

from embeddings_processor import search_website_data


# Create FastAPI app
app = FastAPI(
    title="Web Scraper Agent API",
    description="REST API for searching scraped website content using vector similarity search",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


class SearchRequest(BaseModel):
    """Request model for search endpoint."""
    query: str = Field(..., description="Search query text", min_length=1)
    limit: int = Field(5, description="Maximum number of results", ge=1, le=20)
    collection: str = Field("scraped_content", description="Database collection name")


class SearchResponse(BaseModel):
    """Response model for search results."""
    success: bool
    query: str
    count: int
    results: list = []
    message: Optional[str] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Web Scraper Agent API",
        "description": "Search scraped website content using vector similarity",
        "version": "1.0.0",
        "endpoints": {
            "/search": "POST - Search with JSON body",
            "/search_query": "GET - Search with query parameters", 
            "/health": "GET - Health check",
            "/docs": "GET - Interactive API documentation"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "scraper-agent-api"}


@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    """
    Search for similar content using vector similarity search.
    
    Args:
        request: Search request with query, limit, and collection
        
    Returns:
        Search results with metadata and content snippets
    """
    try:
        result = search_website_data(request.query, request.collection, request.limit)
        return SearchResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.get("/search_query", response_model=SearchResponse)
async def search_with_query_params(
    query: str = Query(..., description="Search query text", min_length=1),
    limit: int = Query(5, description="Maximum number of results", ge=1, le=20),
    collection: str = Query("scraped_content", description="Database collection name")
) -> SearchResponse:
    """
    Search for similar content using query parameters.
    
    Args:
        query: Search query text
        limit: Maximum number of results (1-20)
        collection: Database collection name
        
    Returns:
        Search results with metadata and content snippets
    """
    try:
        result = search_website_data(query, collection, limit)
        return SearchResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.get("/collections")
async def list_collections():
    """List available database collections."""
    try:
        from vector.database import VectorDatabaseManager
        
        db_manager = VectorDatabaseManager(database_type="chroma")
        collections = db_manager.list_all_collections()
        
        return {
            "success": True,
            "collections": collections,
            "count": len(collections)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list collections: {str(e)}")


if __name__ == "__main__":
    print("Starting FastAPI server for Scraper Agent...")
    uvicorn.run(
        "fastapi_server:app",
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )