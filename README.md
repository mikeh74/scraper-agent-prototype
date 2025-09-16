# Web Scraper Agent Prototype

A Python web scraper that extracts structured content from web pages using the requests library and BeautifulSoup.

## Features

- Fetches web pages using the `requests` library
- Parses HTML content with `BeautifulSoup`
- Extracts page metadata (title, description, last modified date)
- Extracts and formats content from headings (h1-h6) and paragraphs (p) in markdown format
- Returns structured data as JSON

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

## Output Format

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

## Testing

Run the demo to see the scraper in action:
```bash
python demo_scraper.py
```

## Dependencies

- `requests>=2.25.0` - For making HTTP requests
- `beautifulsoup4>=4.9.0` - For parsing HTML content

## Error Handling

The scraper includes robust error handling for:
- Network connectivity issues
- Invalid URLs
- Missing HTML elements
- Request timeouts

## Features

- **Smart Content Extraction**: Automatically finds and formats headings and paragraphs
- **Metadata Extraction**: Pulls title, description, and last modified information
- **Markdown Formatting**: Converts HTML structure to clean markdown format
- **Flexible Configuration**: Customizable timeout and headers
- **Error Handling**: Comprehensive error handling and informative error messages