#!/usr/bin/env python3
"""
Vector package for vector embeddings and database functionality.

This package contains modules for:
- database.py: Vector database abstraction layer with Chroma implementation
- embeddings.py: Vector embedding generation using sentence-transformers
"""

# Import key classes and functions for easier access
from .database import VectorDatabaseManager, ChromaVectorDatabase, VectorDatabaseInterface
from .embeddings import VectorEmbeddingsGenerator, add_vector_embeddings

__all__ = [
    'VectorDatabaseManager', 
    'ChromaVectorDatabase', 
    'VectorDatabaseInterface',
    'VectorEmbeddingsGenerator',
    'add_vector_embeddings'
]