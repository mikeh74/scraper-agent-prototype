#!/usr/bin/env python3
"""
Main script that combines web scraping, vector embeddings, and vector database storage.

This script takes a JSON object (or URL to scrape), adds vector embeddings to text fields,
and stores the enhanced data in a Chroma vector database.
"""

import json
import sys
import argparse
from typing import Dict, Any, Union

from scraper import WebScraper
from vector_embeddings import add_vector_embeddings
from vector_database import VectorDatabaseManager


def process_json_with_embeddings(json_data: Union[Dict[str, Any], str], 
                                store_in_db: bool = False,
                                collection_name: str = "scraped_content") -> Dict[str, Any]:
    """
    Process JSON data by adding vector embeddings and optionally storing in vector database.
    
    Args:
        json_data (dict or str): Input JSON data or JSON string
        store_in_db (bool): Whether to store in vector database
        collection_name (str): Collection name for database storage
        
    Returns:
        dict: Enhanced JSON with embeddings and optional database ID
    """
    # Parse JSON string if needed
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    
    print("Adding vector embeddings to text fields...")
    enhanced_data = add_vector_embeddings(json_data)
    
    # Check if embeddings were added
    if "embeddings" in enhanced_data:
        embeddings_count = len(enhanced_data["embeddings"])
        print(f"✅ Added {embeddings_count} embedding(s) to the JSON data")
        
        # Show which fields were embedded
        for field_name in enhanced_data["embeddings"].keys():
            original_field = field_name.replace("_embedding", "")
            vector_length = len(enhanced_data["embeddings"][field_name])
            print(f"   - {original_field}: {vector_length}-dimensional vector")
    else:
        print("⚠️  No text fields found for embedding")
    
    # Store in vector database if requested
    if store_in_db and "embeddings" in enhanced_data:
        print(f"\nStoring in vector database (collection: {collection_name})...")
        try:
            db_manager = VectorDatabaseManager(database_type="chroma")
            doc_id = db_manager.store_document_with_embeddings(enhanced_data, collection_name)
            enhanced_data["database_id"] = doc_id
            print(f"✅ Stored in database with ID: {doc_id}")
        except Exception as e:
            print(f"❌ Failed to store in database: {e}")
    
    return enhanced_data


def scrape_and_process(url: str, store_in_db: bool = False, 
                      collection_name: str = "scraped_content") -> Dict[str, Any]:
    """
    Scrape a URL and process the result with embeddings.
    
    Args:
        url (str): URL to scrape
        store_in_db (bool): Whether to store in vector database
        collection_name (str): Collection name for database storage
        
    Returns:
        dict: Enhanced scraped data with embeddings
    """
    print(f"Scraping URL: {url}")
    
    # Scrape the webpage
    scraper = WebScraper()
    scraped_data = scraper.scrape(url)
    print("✅ Successfully scraped webpage")
    
    # Process with embeddings
    return process_json_with_embeddings(scraped_data, store_in_db, collection_name)


def search_website_data(query_text: str, collection_name: str = "scraped_content", 
                       limit: int = 5) -> Dict[str, Any]:
    """
    Query the vector database for similar content and return results as data.
    This version works offline by searching through stored document text.
    
    Args:
        query_text (str): Text to search for
        collection_name (str): Collection to search in
        limit (int): Maximum number of results
        
    Returns:
        dict: Search results with status and data
    """
    try:
        db_manager = VectorDatabaseManager(database_type="chroma")
        
        # Try to get direct results from the database first
        try:
            # Check if collection exists and has documents
            collections = db_manager.list_all_collections()
            if collection_name not in collections:
                return {
                    "success": True,
                    "query": query_text,
                    "count": 0,
                    "results": [],
                    "message": f"Collection '{collection_name}' does not exist"
                }
            
            # For now, in offline mode, we'll do a simple text matching approach
            # since we can't generate embeddings for the query without internet access
            # This is a fallback implementation
            from vector_database import ChromaVectorDatabase
            chroma_db = ChromaVectorDatabase()
            collection = chroma_db.client.get_collection(name=collection_name)
            
            # Get all documents and do text-based filtering
            all_results = collection.get()
            if not all_results["documents"]:
                return {
                    "success": True,
                    "query": query_text,
                    "count": 0,
                    "results": [],
                    "message": "No documents found in collection"
                }
            
            # Simple text matching for offline mode
            matching_docs = []
            query_lower = query_text.lower()
            
            for i, doc in enumerate(all_results["documents"]):
                # Check if query terms appear in document
                doc_text = doc.lower() if doc else ""
                metadata = all_results["metadatas"][i] if all_results["metadatas"] else {}
                title = metadata.get("title", "").lower() if metadata else ""
                description = metadata.get("description", "").lower() if metadata else ""
                
                # Simple matching score based on term presence
                score = 0
                query_terms = query_lower.split()
                for term in query_terms:
                    if term in doc_text:
                        score += 2
                    if term in title:
                        score += 3
                    if term in description:
                        score += 2
                
                if score > 0:
                    matching_docs.append({
                        "index": i,
                        "score": score,
                        "id": all_results["ids"][i],
                        "document": doc,
                        "metadata": metadata
                    })
            
            # Sort by score and limit results
            matching_docs.sort(key=lambda x: x["score"], reverse=True)
            matching_docs = matching_docs[:limit]
            
            if matching_docs:
                # Format results
                formatted_results = []
                for doc in matching_docs:
                    formatted_result = {
                        "id": doc["id"],
                        "title": doc["metadata"].get("title", "No title"),
                        "url": doc["metadata"].get("url", "No URL"),
                        "content_snippet": doc["document"][:200] + "..." if doc["document"] else "",
                        "similarity_score": round(doc["score"] / 10.0, 3)  # Normalize score
                    }
                    formatted_results.append(formatted_result)
                
                return {
                    "success": True,
                    "query": query_text,
                    "count": len(formatted_results),
                    "results": formatted_results
                }
            else:
                return {
                    "success": True,
                    "query": query_text,
                    "count": 0,
                    "results": [],
                    "message": "No matching documents found"
                }
                
        except Exception as search_error:
            # If the advanced search fails, try the original method
            results = db_manager.search_similar(query_text, collection_name, limit)
            
            if results:
                # Format results for structured output
                formatted_results = []
                for result in results:
                    formatted_result = {
                        "id": result['id'],
                        "title": result.get('metadata', {}).get('title', 'No title'),
                        "url": result.get('metadata', {}).get('url', 'No URL'),
                        "content_snippet": result.get('document', '')[:200] + '...' if result.get('document') else '',
                        "similarity_score": round(1 - result['distance'], 4) if result.get('distance') is not None else None
                    }
                    formatted_results.append(formatted_result)
                
                return {
                    "success": True,
                    "query": query_text,
                    "count": len(formatted_results),
                    "results": formatted_results
                }
            else:
                return {
                    "success": True,
                    "query": query_text,
                    "count": 0,
                    "results": [],
                    "message": "No similar documents found"
                }
            
    except Exception as e:
        return {
            "success": False,
            "query": query_text,
            "error": str(e)
        }


def query_database(query_text: str, collection_name: str = "scraped_content", 
                  limit: int = 5) -> None:
    """
    Query the vector database for similar content (CLI version that prints results).
    
    Args:
        query_text (str): Text to search for
        collection_name (str): Collection to search in
        limit (int): Maximum number of results
    """
    print(f"Searching for: '{query_text}'")
    
    # Use the new data function and print results
    result = search_website_data(query_text, collection_name, limit)
    
    if result["success"]:
        if result["count"] > 0:
            print(f"\n✅ Found {result['count']} similar document(s):")
            for i, doc in enumerate(result["results"], 1):
                print(f"\n{i}. Document ID: {doc['id']}")
                print(f"   Title: {doc['title']}")
                print(f"   URL: {doc['url']}")
                if doc['similarity_score'] is not None:
                    print(f"   Similarity score: {doc['similarity_score']}")
        else:
            print("No similar documents found")
    else:
        print(f"❌ Error querying database: {result['error']}")


def list_collections() -> None:
    """List all collections in the vector database."""
    try:
        db_manager = VectorDatabaseManager(database_type="chroma")
        collections = db_manager.list_all_collections()
        
        if collections:
            print("Available collections:")
            for collection in collections:
                print(f"  - {collection}")
        else:
            print("No collections found in database")
            
    except Exception as e:
        print(f"❌ Error listing collections: {e}")


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description="Process JSON data with vector embeddings and store in vector database"
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Process JSON command
    process_parser = subparsers.add_parser('process', help='Process JSON data with embeddings')
    process_parser.add_argument('json_input', help='JSON data as string or file path')
    process_parser.add_argument('--store', action='store_true', help='Store in vector database')
    process_parser.add_argument('--collection', default='scraped_content', help='Database collection name')
    
    # Scrape URL command
    scrape_parser = subparsers.add_parser('scrape', help='Scrape URL and process with embeddings')
    scrape_parser.add_argument('url', help='URL to scrape')
    scrape_parser.add_argument('--store', action='store_true', help='Store in vector database')
    scrape_parser.add_argument('--collection', default='scraped_content', help='Database collection name')
    
    # Query database command
    query_parser = subparsers.add_parser('query', help='Query vector database for similar content')
    query_parser.add_argument('query_text', help='Text to search for')
    query_parser.add_argument('--collection', default='scraped_content', help='Database collection name')
    query_parser.add_argument('--limit', type=int, default=5, help='Maximum number of results')
    
    # List collections command
    subparsers.add_parser('list', help='List all database collections')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'process':
            # Process JSON data
            json_input = args.json_input
            
            # Check if it's a file path or JSON string
            try:
                with open(json_input, 'r') as f:
                    json_data = json.load(f)
                print(f"Loaded JSON from file: {json_input}")
            except (FileNotFoundError, json.JSONDecodeError):
                # Assume it's a JSON string
                json_data = json.loads(json_input)
                print("Processing JSON string input")
            
            result = process_json_with_embeddings(json_data, args.store, args.collection)
            
            print("\nFinal result:")
            # Don't print full embeddings for readability
            display_result = result.copy()
            if "embeddings" in display_result:
                embeddings_info = {}
                for key, embedding in display_result["embeddings"].items():
                    embeddings_info[key] = f"<{len(embedding)}-dimensional vector>"
                display_result["embeddings"] = embeddings_info
            
            print(json.dumps(display_result, indent=2, ensure_ascii=False))
        
        elif args.command == 'scrape':
            # Scrape URL and process
            result = scrape_and_process(args.url, args.store, args.collection)
            
            print("\nFinal result:")
            # Don't print full embeddings for readability
            display_result = result.copy()
            if "embeddings" in display_result:
                embeddings_info = {}
                for key, embedding in display_result["embeddings"].items():
                    embeddings_info[key] = f"<{len(embedding)}-dimensional vector>"
                display_result["embeddings"] = embeddings_info
            
            print(json.dumps(display_result, indent=2, ensure_ascii=False))
        
        elif args.command == 'query':
            # Query database
            query_database(args.query_text, args.collection, args.limit)
        
        elif args.command == 'list':
            # List collections
            list_collections()
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()