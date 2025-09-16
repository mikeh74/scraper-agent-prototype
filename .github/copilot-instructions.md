# Web Scraper Agent Prototype - GitHub Copilot Instructions

**ALWAYS follow these instructions first and only fallback to search or bash commands when you encounter unexpected information that does not match the info here.**

## Project Overview
Web Scraper Agent Prototype is a Python-based modular web scraping system with vector embeddings and semantic search capabilities. It includes:
- Core web scraper extracting structured content from HTML
- Vector embeddings using sentence-transformers (all-MiniLM-L6-v2 model)
- Chroma vector database integration
- MCP (Model Context Protocol) server for AI assistant integration
- FastAPI REST server with interactive documentation
- Command-line interface for all operations

## Working Effectively

### Environment Setup
```bash
# Install dependencies - NEVER CANCEL: Takes 5+ minutes for ML libraries
pip install -r requirements.txt
```
**Timeout: Set 10+ minutes. The install downloads PyTorch (~2GB) and other ML dependencies.**

### Testing and Validation
```bash
# Run all demo tests - each completes in under 60 seconds
python demo_scraper.py          # Basic web scraper demo
python demo_embeddings.py       # Vector embeddings demo (mock mode)
python test_integration.py      # Complete integration test
python test_mcp_simple.py       # MCP server functions test

# Test MCP server functionality with database creation
python demo_mcp.py              # Complete MCP demo with sample data
```

### Running the Applications
```bash
# Start FastAPI server - NEVER CANCEL: Starts in ~10 seconds
python fastapi_server.py
# Server runs on http://localhost:8000
# Visit http://localhost:8000/docs for interactive API documentation

# Start MCP server (stdio transport)
python mcp_server.py

# Use CLI for embeddings processing
python embeddings_processor.py --help
python embeddings_processor.py process '{"title": "Test", "content": "Sample"}' --store
python embeddings_processor.py query "search term" --limit 5
python embeddings_processor.py list

# Use basic web scraper
python scraper.py https://example.com
```

## CRITICAL Timing and Timeout Information

- **pip install**: 5-10 minutes (downloads PyTorch, transformers, ChromaDB) - **NEVER CANCEL**
- **FastAPI server startup**: ~10 seconds - **NEVER CANCEL**
- **MCP server startup**: ~5 seconds
- **Demo scripts**: 30-60 seconds each
- **Integration tests**: 30-60 seconds each
- **Real embedding model download**: 2-5 minutes (~90MB) - **NEVER CANCEL** - Only happens on first use with internet

### Network Dependency Notes
- **With Internet**: Full functionality including real sentence-transformer embeddings
- **Without Internet**: All functionality works using mock embeddings
- **First Run**: Requires internet to download all-MiniLM-L6-v2 model (~90MB)
- **Subsequent Runs**: Works offline using cached models

## Manual Validation Scenarios

### Essential End-to-End Testing (ALWAYS perform after changes)

1. **Basic Web Scraper Validation**:
   ```bash
   python demo_scraper.py
   # Verify: JSON output with title, description, content, URL
   # Verify: Content is properly formatted as markdown
   ```

2. **Vector Embeddings Integration**:
   ```bash
   python demo_embeddings.py
   # Verify: Mock embeddings generated (384 dimensions)
   # Verify: Multiple document processing works
   # Verify: Similarity search returns ranked results
   ```

3. **Complete Pipeline Test**:
   ```bash
   python test_integration.py
   # Verify: HTML->JSON->Embeddings->Database pipeline
   # Verify: CLI interface simulation works
   # Verify: All integration points function correctly
   ```

4. **MCP Server Validation**:
   ```bash
   # Terminal 1: Create test data and validate search
   python demo_mcp.py
   # Verify: Sample documents created in database
   # Verify: Search queries return relevant results
   # Verify: MCP tools respond correctly
   ```

5. **FastAPI Server Validation**:
   ```bash
   # Terminal 1:
   python fastapi_server.py
   # Terminal 2:
   curl "http://localhost:8000/health"
   curl "http://localhost:8000/search_query?query=test&limit=2"
   # Verify: Health endpoint returns healthy status
   # Verify: Search endpoint returns valid JSON response
   # Verify: Interactive docs at http://localhost:8000/docs
   ```

6. **CLI Interface Testing**:
   ```bash
   # Test help and basic functionality
   python embeddings_processor.py --help
   python embeddings_processor.py list
   # With internet: Test real embedding generation
   python embeddings_processor.py process '{"title":"Test","content":"Sample text"}' --store
   ```

## Code Quality and Validation

### Syntax Validation
```bash
# Basic Python syntax check - always run before committing
python -m py_compile *.py
```

**NO ADDITIONAL LINTERS OR FORMATTERS** - The project uses basic Python validation only.

## Common Issues and Troubleshooting

### Internet Connectivity Issues
- **Error**: "We couldn't connect to 'https://huggingface.co'"
- **Solution**: Use demo scripts which work with mock embeddings offline
- **Workaround**: All functionality except real ML embeddings works offline

### Database Initialization
- **ChromaDB**: Automatically creates `./chroma_db/` directory
- **Clean Reset**: Delete `chroma_db/` directory to reset database
- **Persistent Storage**: Database persists between runs

### Server Port Conflicts
- **FastAPI**: Uses port 8000 by default
- **Check**: `curl http://localhost:8000/health` to test if running
- **Stop**: Use Ctrl+C to terminate servers

## Repository Structure (Key Directories)

```
/home/runner/work/scraper-agent-prototype/scraper-agent-prototype/
├── scraper.py              # Core web scraping functionality
├── vector_embeddings.py    # Vector embedding generation
├── vector_database.py      # Chroma database abstraction
├── embeddings_processor.py # Main CLI interface
├── mcp_server.py          # MCP server implementation
├── fastapi_server.py      # REST API server
├── demo_*.py              # Demonstration scripts
├── test_*.py              # Test scripts
├── requirements.txt       # Python dependencies
├── README.md              # Main documentation
├── MCP_README.md          # MCP server documentation
└── chroma_db/            # Vector database storage (created at runtime)
```

## Frequently Accessed Files

### Core Modules
- `scraper.py` - Modify for web scraping logic changes
- `vector_embeddings.py` - Modify for embedding model configuration  
- `vector_database.py` - Modify for database operations
- `embeddings_processor.py` - Modify for CLI interface changes

### Server Implementations
- `mcp_server.py` - Modify for MCP tool functionality
- `fastapi_server.py` - Modify for REST API endpoints

### Testing and Validation
- Always run `demo_*.py` scripts after changes to core modules
- Always run `test_integration.py` after architectural changes
- Always test both online and offline functionality

## Development Workflow

1. **Before Making Changes**: Run all demo and test scripts to establish baseline
2. **During Development**: Test changes with relevant demo script
3. **Before Committing**: Run complete validation scenario
4. **Integration Testing**: Always test both MCP and FastAPI servers
5. **Network Testing**: Validate both online and offline modes

## Architecture Notes

- **Modular Design**: Each component can be used independently
- **Database Abstraction**: Designed for easy switching between vector databases
- **Offline Capability**: Full functionality without internet (except model downloads)
- **No Build Step**: Pure Python application, no compilation required
- **Mock vs Real**: System seamlessly switches between mock and real embeddings based on model availability

Always refer to README.md and MCP_README.md for detailed usage examples and API documentation.