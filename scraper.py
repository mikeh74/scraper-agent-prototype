#!/usr/bin/env python3
"""
Web Scraper using Python requests and BeautifulSoup

This script scrapes web pages and extracts:
- Page title
- Page description (from meta tags)
- Last modified header
- Content from h1-h6 and p tags formatted as markdown
"""

import json
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class WebScraper:
    """A web scraper that extracts structured content from web pages."""
    
    def __init__(self, timeout=30, headers=None):
        """
        Initialize the scraper with optional configuration.
        
        Args:
            timeout (int): Request timeout in seconds
            headers (dict): Custom headers to use for requests
        """
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set default headers
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        if headers:
            default_headers.update(headers)
        
        self.session.headers.update(default_headers)
    
    def scrape(self, url):
        """
        Scrape a web page and extract structured content.
        
        Args:
            url (str): The URL to scrape
            
        Returns:
            dict: Scraped data in the specified JSON format
        """
        try:
            # Make the request
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract metadata
            title = self._extract_title(soup)
            description = self._extract_description(soup)
            last_modified = self._extract_last_modified(response)
            
            # Extract and format content
            content = self._extract_content(soup)
            
            return {
                "title": title,
                "url": url,
                "description": description,
                "last_modified": last_modified,
                "content": content
            }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch URL {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error scraping {url}: {str(e)}")
    
    def _extract_title(self, soup):
        """Extract page title."""
        title_tag = soup.find('title')
        if title_tag and title_tag.get_text(strip=True):
            return title_tag.get_text(strip=True)
        
        # Fallback to h1 if no title tag
        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text(strip=True)
        
        return "No title found"
    
    def _extract_description(self, soup):
        """Extract page description from meta tags."""
        # Try meta description first
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc.get('content').strip()
        
        # Try og:description
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        if og_desc and og_desc.get('content'):
            return og_desc.get('content').strip()
        
        # Fallback to first paragraph
        first_p = soup.find('p')
        if first_p:
            text = first_p.get_text(strip=True)
            # Limit to first 160 characters for description
            return text[:160] + "..." if len(text) > 160 else text
        
        return "No description available"
    
    def _extract_last_modified(self, response):
        """Extract last modified date from response headers."""
        last_modified = response.headers.get('Last-Modified')
        if last_modified:
            return last_modified
        
        # Try other common headers
        date_header = response.headers.get('Date')
        if date_header:
            return date_header
        
        return None
    
    def _extract_content(self, soup):
        """Extract and format content from headings and paragraphs."""
        content_parts = []
        
        # Find all headings and paragraphs in order
        elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'])
        
        for element in elements:
            text = element.get_text(strip=True)
            if not text:  # Skip empty elements
                continue
            
            tag_name = element.name.lower()
            
            if tag_name.startswith('h'):
                # Convert headings to markdown
                level = int(tag_name[1])
                markdown_heading = '#' * level + ' ' + text
                content_parts.append(markdown_heading)
            elif tag_name == 'p':
                # Add paragraph text
                content_parts.append(text)
        
        # Join with double newlines for proper markdown formatting
        return '\n\n'.join(content_parts)


def main():
    """Main function for command-line usage."""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python scraper.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    
    try:
        scraper = WebScraper()
        result = scraper.scrape(url)
        
        # Pretty print JSON
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()