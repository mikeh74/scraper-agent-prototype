# Web Scraper Agent Prototype

A Python web scraper that extracts structured content from web pages and enhances it with vector embeddings for semantic search and storage in vector databases.

## Features

### Web Scraping
- Fetches web pages using the `requests` library
- Parses HTML content with `BeautifulSoup`
- Extracts page metadata (title, description, last modified date)
- Extracts and formats content from headings (h1-h6) and paragraphs (p) in markdown format
- Returns structured data as JSON

### Vector Embeddings
- **Text Field Embedding**: Automatically generates embeddings for text fields (title, description, content)
- **Free Open Source Models**: Uses sentence-transformers library with models like all-MiniLM-L6-v2
- **Semantic Understanding**: Creates high-dimensional vectors that capture semantic meaning

### Vector Database Integration
- **Chroma Database Support**: Stores embeddings in Chroma vector database
- **Abstraction Layer**: Designed for easy switching between different vector databases
- **Semantic Search**: Query similar documents using natural language
- **Document Management**: Store, retrieve, and delete documents with embeddings

### Command Line Interface
- **Process JSON**: Add embeddings to existing JSON data
- **Scrape and Process**: Scrape URLs and add embeddings in one step  
- **Query Database**: Search for similar content using semantic queries
- **Database Management**: List collections and manage stored documents

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line
```bash
python scraper.py <URL>
```

Example:
```bash
python scraper.py https://example.com
```

### As a Python Module
```python
from scraper import WebScraper

scraper = WebScraper()
result = scraper.scrape("https://example.com")
print(result)
```

### Vector Embeddings and Database

#### Process JSON with Embeddings
```bash
# Add embeddings to existing JSON data
python embeddings_processor.py process '{"title": "Example", "content": "Sample text"}'

# Add embeddings and store in database
python embeddings_processor.py process '{"title": "Example", "content": "Sample text"}' --store
```

#### Scrape URL and Process with Embeddings
```bash
# Scrape URL and add embeddings
python embeddings_processor.py scrape https://example.com

# Scrape URL, add embeddings, and store in database
python embeddings_processor.py scrape https://example.com --store
```

#### Query Vector Database
```bash
# Search for similar content
python embeddings_processor.py query "machine learning algorithms"

# Limit number of results
python embeddings_processor.py query "web scraping" --limit 10
```

#### Database Management
```bash
# List all collections
python embeddings_processor.py list
```

#### Python API for Embeddings
```python
from vector_embeddings import add_vector_embeddings
from vector_database import VectorDatabaseManager

# Add embeddings to JSON data
data = {"title": "Example", "content": "Sample text"}
enhanced_data = add_vector_embeddings(data)

# Store in vector database
db_manager = VectorDatabaseManager(database_type="chroma")
doc_id = db_manager.store_document_with_embeddings(enhanced_data)

# Search similar documents
results = db_manager.search_similar("sample text", limit=5)
```

## Output Format

### Basic Scraper Output
The scraper returns a JSON object with the following structure:

```json
{
  "title": "Page Title",
  "url": "https://example.com",
  "description": "Page description from meta tags",
  "last_modified": "Mon, 13 Jan 2025 20:11:20 GMT",
  "content": "# Heading 1\n\nParagraph content...\n\n## Heading 2\n\nMore content..."
}
```

### Enhanced Output with Vector Embeddings
When using the vector embeddings functionality, the output is enhanced with embeddings:

```json
{
  "title": "Page Title",
  "url": "https://example.com", 
  "description": "Page description from meta tags",
  "last_modified": "Mon, 13 Jan 2025 20:11:20 GMT",
  "content": "# Heading 1\n\nParagraph content...",
  "embeddings": {
    "title_embedding": [384-dimensional vector array],
    "description_embedding": [384-dimensional vector array], 
    "content_embedding": [384-dimensional vector array]
  },
  "database_id": "doc_12345"
}
```

## Testing

Run the demos to see the functionality:

### Basic Web Scraper Demo
```bash
python demo_scraper.py
```

### Vector Embeddings Demo
```bash
python demo_embeddings.py
```

### Complete Integration Test
```bash
python test_integration.py
```

## Dependencies

- `requests>=2.25.0` - For making HTTP requests
- `beautifulsoup4>=4.9.0` - For parsing HTML content
- `sentence-transformers>=2.2.0` - For generating vector embeddings
- `chromadb>=0.4.0` - For vector database storage

## Error Handling

The system includes robust error handling for:
- Network connectivity issues
- Invalid URLs
- Missing HTML elements
- Request timeouts
- Vector embedding generation failures
- Vector database connection issues

## Architecture

### Modular Design
The system is designed with modularity in mind:

- **`scraper.py`** - Core web scraping functionality
- **`vector_embeddings.py`** - Vector embedding generation using sentence-transformers
- **`vector_database.py`** - Vector database abstraction layer with Chroma implementation
- **`embeddings_processor.py`** - Main script combining all functionality with CLI interface

### Vector Database Abstraction
The vector database layer is designed for easy switching:

```python
# Current implementation uses Chroma
db_manager = VectorDatabaseManager(database_type="chroma")

# Future implementations could support other databases
# db_manager = VectorDatabaseManager(database_type="pinecone")
# db_manager = VectorDatabaseManager(database_type="weaviate")
```

### Embedding Models
Currently uses sentence-transformers with the lightweight `all-MiniLM-L6-v2` model:
- **Size**: ~90MB download
- **Dimensions**: 384
- **Performance**: Good balance of speed and quality
- **Free**: Completely open source

Other models can be easily configured by changing the model name in `VectorEmbeddingsGenerator`.

## Future Enhancements

- Support for additional vector databases (Pinecone, Weaviate, etc.)
- Batch processing for multiple URLs
- Custom embedding model fine-tuning
- Web interface for document management
- Advanced search filters and faceting
- Automatic content updates and re-embedding