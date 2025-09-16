#!/usr/bin/env python3
"""
Vector embeddings module that adds embeddings to JSON objects with text fields.

This module uses sentence-transformers for generating embeddings from text content.
"""

import json
import logging
from typing import Dict, Any, List, Union
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorEmbeddingsGenerator:
    """Generates vector embeddings for text content in JSON objects."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embeddings generator with a specified model.

        Args:
            model_name (str):
                Name of the sentence-transformers model to use.
                Default is 'all-MiniLM-L6-v2' which is lightweight and free.
        """
        self.model_name = model_name
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        logger.info("Embedding model loaded successfully")

    def add_embeddings(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add vector embeddings to text fields in a JSON object.

        Args:
            json_data (dict): Input JSON object containing text fields

        Returns:
            dict: Enhanced JSON object with embeddings added
        """
        # Create a copy to avoid modifying the original
        enhanced_data = json_data.copy()

        # Text fields to embed - looking for common text field names
        text_fields = self._identify_text_fields(json_data)

        if not text_fields:
            logger.warning("No text fields found for embedding")
            return enhanced_data

        # Generate embeddings for each text field
        embeddings = {}
        for field_name in text_fields:
            text_content = json_data[field_name]
            if text_content and isinstance(text_content, str):
                logger.info(f"Generating embedding for field: {field_name}")
                embedding = self.model.encode(text_content).tolist()
                embeddings[f"{field_name}_embedding"] = embedding
                logger.info(
                    f"Generated embedding for '{field_name}' with {len(embedding)} dimensions"
                )

        # Add embeddings to the enhanced data
        enhanced_data["embeddings"] = embeddings

        return enhanced_data

    def _identify_text_fields(self, json_data: Dict[str, Any]) -> List[str]:
        """
        Identify text fields in the JSON data that should be embedded.

        Args:
            json_data (dict): Input JSON data

        Returns:
            list: List of field names containing text to embed
        """
        text_fields = []

        # Common text field names to look for
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

        return text_fields


def add_vector_embeddings(json_data: Union[Dict[str, Any], str]) -> Dict[str, Any]:
    """
    Convenience function to add vector embeddings to a JSON object.

    Args:
        json_data (dict or str): JSON data as dictionary or JSON string

    Returns:
        dict: JSON object with embeddings added
    """
    # Parse JSON string if needed
    if isinstance(json_data, str):
        json_data = json.loads(json_data)

    # Initialize embeddings generator
    generator = VectorEmbeddingsGenerator()

    # Generate and add embeddings
    return generator.add_embeddings(json_data)


if __name__ == "__main__":
    # Example usage
    sample_data = {
        "title": "Example Web Page",
        "url": "https://example.com",
        "description": "This is a sample description for testing vector embeddings",
        "last_modified": "Mon, 13 Jan 2025 20:11:20 GMT",
        "content": "# Sample Content\n\nThis is sample content with some text that will be embedded.",
    }

    print("Original data:")
    print(json.dumps(sample_data, indent=2))

    enhanced_data = add_vector_embeddings(sample_data)

    print("\nEnhanced data with embeddings:")
    # Print without embeddings for readability, just show structure
    display_data = enhanced_data.copy()
    if "embeddings" in display_data:
        embeddings_info = {}
        for key, embedding in display_data["embeddings"].items():
            embeddings_info[key] = f"<{len(embedding)} dimensional vector>"
        display_data["embeddings"] = embeddings_info

    print(json.dumps(display_data, indent=2))
