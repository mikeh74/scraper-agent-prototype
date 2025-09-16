#!/usr/bin/env python3
"""
Vector database module with abstraction layer for storing and retrieving
embeddings.

This module provides an abstraction layer that allows switching between
different vector databases. Currently implements Chroma as the default backend.
"""

import logging
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import chromadb

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorDatabaseInterface(ABC):
    """Abstract interface for vector database implementations."""

    @abstractmethod
    def store_document(
        self, document_data: Dict[str, Any], collection_name: str = "default"
    ) -> str:
        """Store a document with embeddings in the vector database."""
        pass

    @abstractmethod
    def query_similar(
        self, query_text: str, collection_name: str = "default", n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """Query for similar documents based on text similarity."""
        pass

    @abstractmethod
    def get_document(
        self, document_id: str, collection_name: str = "default"
    ) -> Optional[Dict[str, Any]]:
        """Retrieve a specific document by ID."""
        pass

    @abstractmethod
    def list_collections(self) -> List[str]:
        """List all available collections."""
        pass

    @abstractmethod
    def delete_document(
        self, document_id: str, collection_name: str = "default"
    ) -> bool:
        """Delete a document from the database."""
        pass


class ChromaVectorDatabase(VectorDatabaseInterface):
    """Chroma vector database implementation."""

    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize Chroma database.

        Args:
            persist_directory (str): Directory to persist the database
        """
        self.persist_directory = persist_directory
        logger.info(f"Initializing Chroma database at {persist_directory}")

        # Initialize Chroma client with persistence
        self.client = chromadb.PersistentClient(path=persist_directory)

        logger.info("Chroma database initialized successfully")

    def store_document(
        self, document_data: Dict[str, Any], collection_name: str = "scraped_content"
    ) -> str:
        """
        Store a document with embeddings in Chroma.

        Args:
            document_data (dict): Document data with embeddings
            collection_name (str): Name of the collection to store in

        Returns:
            str: Document ID
        """
        try:
            # Get or create collection
            collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "Scraped web content with embeddings"},
            )

            # Generate unique ID for the document
            doc_id = str(uuid.uuid4())

            # Extract embeddings - use the first available embedding
            embeddings_data = document_data.get("embeddings", {})
            if not embeddings_data:
                raise ValueError("No embeddings found in document data")

            # Use the first available embedding (prefer content, then description, then title)
            embedding_vector = None
            preferred_order = [
                "content_embedding",
                "description_embedding",
                "title_embedding",
            ]

            for field in preferred_order:
                if field in embeddings_data:
                    embedding_vector = embeddings_data[field]
                    break

            if not embedding_vector:
                # Use the first available embedding
                embedding_vector = list(embeddings_data.values())[0]

            # Prepare metadata (exclude embeddings from metadata to avoid duplication)
            metadata = {k: v for k, v in document_data.items() if k != "embeddings"}

            # Convert metadata values to strings for Chroma compatibility
            for key, value in metadata.items():
                if value is not None:
                    metadata[key] = str(value)
                else:
                    metadata[key] = ""

            # Create document text for search (combine available text fields)
            document_text = self._create_document_text(document_data)

            # Store in Chroma
            collection.add(
                embeddings=[embedding_vector],
                documents=[document_text],
                metadatas=[metadata],
                ids=[doc_id],
            )

            logger.info(
                f"Stored document with ID: {doc_id} in collection: {collection_name}"
            )
            return doc_id

        except Exception as e:
            logger.error(f"Error storing document in Chroma: {e}")
            raise

    def query_similar(
        self,
        query_text: str,
        collection_name: str = "scraped_content",
        n_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Query for similar documents in Chroma.

        Args:
            query_text (str): Text to search for
            collection_name (str): Collection to search in
            n_results (int): Number of results to return

        Returns:
            list: List of similar documents with metadata
        """
        try:
            # Get collection
            collection = self.client.get_collection(name=collection_name)

            # Query for similar documents
            results = collection.query(query_texts=[query_text], n_results=n_results)

            # Format results
            formatted_results = []
            if results["documents"] and results["documents"][0]:
                for i, doc_id in enumerate(results["ids"][0]):
                    result = {
                        "id": doc_id,
                        "document": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "distance": (
                            results["distances"][0][i]
                            if results.get("distances")
                            else None
                        ),
                    }
                    formatted_results.append(result)

            logger.info(f"Found {len(formatted_results)} similar documents for query")
            return formatted_results

        except Exception as e:
            logger.error(f"Error querying Chroma: {e}")
            raise

    def get_document(
        self, document_id: str, collection_name: str = "scraped_content"
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific document by ID from Chroma.

        Args:
            document_id (str): Document ID to retrieve
            collection_name (str): Collection name

        Returns:
            dict or None: Document data if found
        """
        try:
            collection = self.client.get_collection(name=collection_name)

            result = collection.get(ids=[document_id])

            if result["ids"]:
                return {
                    "id": result["ids"][0],
                    "document": result["documents"][0] if result["documents"] else None,
                    "metadata": result["metadatas"][0] if result["metadatas"] else None,
                }

            return None

        except Exception as e:
            logger.error(f"Error retrieving document from Chroma: {e}")
            return None

    def list_collections(self) -> List[str]:
        """List all collections in Chroma."""
        try:
            collections = self.client.list_collections()
            return [col.name for col in collections]
        except Exception as e:
            logger.error(f"Error listing collections: {e}")
            return []

    def delete_document(
        self, document_id: str, collection_name: str = "scraped_content"
    ) -> bool:
        """Delete a document from Chroma."""
        try:
            collection = self.client.get_collection(name=collection_name)
            collection.delete(ids=[document_id])
            logger.info(
                f"Deleted document {document_id} from collection {collection_name}"
            )
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False

    def _create_document_text(self, document_data: Dict[str, Any]) -> str:
        """Create searchable text from document data."""
        text_parts = []

        # Combine text fields for searchability
        for field in ["title", "description", "content"]:
            if field in document_data and document_data[field]:
                text_parts.append(str(document_data[field]))

        return " ".join(text_parts)


class VectorDatabaseManager:
    """Manager class for vector database operations with abstraction layer."""

    def __init__(self, database_type: str = "chroma", **kwargs):
        """
        Initialize the vector database manager.

        Args:
            database_type (str): Type of database to use ("chroma" currently)
            **kwargs: Additional arguments for database initialization
        """
        self.database_type = database_type

        if database_type.lower() == "chroma":
            self.db = ChromaVectorDatabase(**kwargs)
        else:
            raise ValueError(f"Unsupported database type: {database_type}")

        logger.info(f"Vector database manager initialized with {database_type}")

    def store_document_with_embeddings(
        self, document_data: Dict[str, Any], collection_name: str = "scraped_content"
    ) -> str:
        """Store a document with embeddings."""
        return self.db.store_document(document_data, collection_name)

    def search_similar(
        self, query: str, collection_name: str = "scraped_content", limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        return self.db.query_similar(query, collection_name, limit)

    def get_document_by_id(
        self, doc_id: str, collection_name: str = "scraped_content"
    ) -> Optional[Dict[str, Any]]:
        """Get a document by ID."""
        return self.db.get_document(doc_id, collection_name)

    def list_all_collections(self) -> List[str]:
        """List all collections."""
        return self.db.list_collections()

    def remove_document(
        self, doc_id: str, collection_name: str = "scraped_content"
    ) -> bool:
        """Remove a document."""
        return self.db.delete_document(doc_id, collection_name)


if __name__ == "__main__":
    # Example usage
    from .embeddings import add_vector_embeddings

    # Sample data
    sample_data = {
        "title": "Vector Database Example",
        "url": "https://example.com/vector-db",
        "description": "Example showing vector database storage",
        "content": "This is example content for testing vector database functionality.",
    }

    # Add embeddings
    enhanced_data = add_vector_embeddings(sample_data)

    # Initialize database manager
    db_manager = VectorDatabaseManager(database_type="chroma")

    # Store document
    doc_id = db_manager.store_document_with_embeddings(enhanced_data)
    print(f"Stored document with ID: {doc_id}")

    # Search for similar documents
    results = db_manager.search_similar("vector database example")
    print(f"Found {len(results)} similar documents")

    # Retrieve document
    retrieved_doc = db_manager.get_document_by_id(doc_id)
    if retrieved_doc:
        print("Successfully retrieved document")
