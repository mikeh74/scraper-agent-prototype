#!/usr/bin/env python3
"""
Demo script for testing vector embeddings and database functionality.

This script simulates the embedding process and demonstrates the complete pipeline
without requiring internet access to download models.
"""

import json
import numpy as np
from typing import Dict, Any, List


def create_mock_embedding(text: str, dimensions: int = 384) -> List[float]:
    """
    Create a mock embedding vector based on text content.

    This simulates what a real embedding model would do, creating a consistent
    vector for the same input text.

    Args:
        text (str): Text to create embedding for
        dimensions (int): Number of dimensions for the embedding vector

    Returns:
        list: Mock embedding vector
    """
    # Use hash of text as seed for reproducible results
    np.random.seed(hash(text) % (2**31))

    # Generate normalized random vector
    vector = np.random.randn(dimensions)
    vector = vector / np.linalg.norm(vector)  # Normalize to unit vector

    return vector.tolist()


def add_mock_embeddings(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add mock embeddings to JSON data (simulates vector_embeddings.py functionality).

    Args:
        json_data (dict): Input JSON data

    Returns:
        dict: Enhanced JSON with mock embeddings
    """
    enhanced_data = json_data.copy()

    # Identify text fields
    text_fields = []
    potential_text_fields = [
        "title",
        "description",
        "content",
        "text",
        "body",
        "summary",
    ]

    for field in potential_text_fields:
        if (
            field in json_data
            and isinstance(json_data[field], str)
            and json_data[field].strip()
        ):
            text_fields.append(field)

    if not text_fields:
        print("⚠️  No text fields found for embedding")
        return enhanced_data

    # Generate mock embeddings for each text field
    embeddings = {}
    for field_name in text_fields:
        text_content = json_data[field_name]
        embedding = create_mock_embedding(text_content)
        embeddings[f"{field_name}_embedding"] = embedding
        print(
            f"✅ Generated mock embedding for '{field_name}' with {len(embedding)} dimensions"
        )

    enhanced_data["embeddings"] = embeddings
    return enhanced_data


def demo_embeddings_pipeline():
    """Demonstrate the complete embeddings and database pipeline."""
    print("🚀 Demo: Vector Embeddings and Database Pipeline")
    print("=" * 60)

    # Sample scraped data (simulates output from scraper.py)
    sample_data = {
        "title": "Introduction to Machine Learning",
        "url": "https://example.com/ml-intro",
        "description": "A comprehensive guide to machine learning concepts and algorithms",
        "last_modified": "Mon, 13 Jan 2025 20:11:20 GMT",
        "content": "# Machine Learning Basics\n\nMachine learning is a subset of artificial intelligence that focuses on algorithms and statistical models. These systems can automatically improve their performance on a specific task through experience.\n\n## Types of Machine Learning\n\n### Supervised Learning\nSupervised learning uses labeled training data to learn a mapping function.\n\n### Unsupervised Learning\nUnsupervised learning finds hidden patterns in data without labeled examples.",
    }

    print("\n1. Original scraped data:")
    print("-" * 30)
    print(json.dumps(sample_data, indent=2))

    print("\n2. Adding vector embeddings...")
    print("-" * 30)
    enhanced_data = add_mock_embeddings(sample_data)

    print(f"\n✅ Added {len(enhanced_data.get('embeddings', {}))} embedding(s)")

    print("\n3. Enhanced data structure (embeddings shown as vector info):")
    print("-" * 30)
    display_data = enhanced_data.copy()
    if "embeddings" in display_data:
        embeddings_info = {}
        for key, embedding in display_data["embeddings"].items():
            embeddings_info[key] = f"<{len(embedding)}-dimensional vector>"
        display_data["embeddings"] = embeddings_info

    print(json.dumps(display_data, indent=2))

    print("\n4. Simulating vector database storage...")
    print("-" * 30)

    # Simulate what the database would do
    doc_id = f"doc_{hash(enhanced_data['title']) % 10000}"
    print(f"✅ Would store document with ID: {doc_id}")
    print("✅ Would index embeddings in collection: 'scraped_content'")

    print("\n5. Simulating similarity search...")
    print("-" * 30)

    # Simulate a search query
    query = "machine learning algorithms"
    print(f"Search query: '{query}'")

    # Create mock search results
    query_embedding = create_mock_embedding(query)

    # Calculate similarity with our stored document (cosine similarity)
    content_embedding = enhanced_data["embeddings"]["content_embedding"]

    # Cosine similarity calculation
    dot_product = np.dot(query_embedding, content_embedding)
    similarity = dot_product  # Already normalized vectors

    print("✅ Found similar document:")
    print(f"   - Document ID: {doc_id}")
    print(f"   - Title: {enhanced_data['title']}")
    print(f"   - Similarity score: {similarity:.4f}")
    print(f"   - URL: {enhanced_data['url']}")

    print("\n🎉 Demo completed successfully!")
    print("=" * 60)

    return enhanced_data


def demo_multiple_documents():
    """Demo with multiple documents to show database-like functionality."""
    print("\n\n🚀 Demo: Multiple Documents Database Simulation")
    print("=" * 60)

    documents = [
        {
            "title": "Python Programming Basics",
            "url": "https://example.com/python-basics",
            "description": "Learn Python programming from scratch",
            "content": "Python is a high-level programming language known for its simplicity and readability.",
        },
        {
            "title": "Web Development with Flask",
            "url": "https://example.com/flask-web",
            "description": "Build web applications using Flask framework",
            "content": "Flask is a lightweight WSGI web application framework in Python.",
        },
        {
            "title": "Data Science with Pandas",
            "url": "https://example.com/pandas-data",
            "description": "Data analysis and manipulation with Pandas library",
            "content": "Pandas is a powerful data manipulation and analysis library for Python.",
        },
    ]

    # Process each document
    processed_docs = []
    for i, doc in enumerate(documents, 1):
        print(f"\nProcessing document {i}: {doc['title']}")
        enhanced_doc = add_mock_embeddings(doc)
        doc_id = f"doc_{hash(doc['title']) % 10000}"
        enhanced_doc["database_id"] = doc_id
        processed_docs.append(enhanced_doc)

    print(f"\n✅ Processed {len(processed_docs)} documents")

    # Simulate search across all documents
    print("\nSimulating search across all documents...")
    query = "Python programming"
    query_embedding = create_mock_embedding(query)

    search_results = []
    for doc in processed_docs:
        # Calculate similarity with title embedding
        title_embedding = doc["embeddings"]["title_embedding"]
        similarity = np.dot(query_embedding, title_embedding)

        search_results.append({"document": doc, "similarity": similarity})

    # Sort by similarity
    search_results.sort(key=lambda x: x["similarity"], reverse=True)

    print(f"\nSearch results for '{query}':")
    for i, result in enumerate(search_results, 1):
        doc = result["document"]
        similarity = result["similarity"]
        print(f"{i}. {doc['title']} (similarity: {similarity:.4f})")
        print(f"   URL: {doc['url']}")

    print("\n🎉 Multi-document demo completed!")
    return processed_docs


if __name__ == "__main__":
    # Run the main demo
    enhanced_data = demo_embeddings_pipeline()

    # Run multi-document demo
    processed_docs = demo_multiple_documents()

    print("\n📊 Summary:")
    print("- Demonstrated vector embedding generation")
    print("- Simulated vector database storage and retrieval")
    print("- Showed similarity search functionality")
    print(f"- Processed {1 + len(processed_docs)} total documents")
    print("\nThis demonstrates the complete pipeline that would work with:")
    print("- Real embedding models (sentence-transformers)")
    print("- Chroma vector database")
    print("- Web scraping integration")
