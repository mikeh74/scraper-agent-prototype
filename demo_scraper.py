#!/usr/bin/env python3
"""
Demo script that shows the scraper functionality with a mock HTML example
"""

import json
from bs4 import BeautifulSoup
from scraper import WebScraper


def demo_scraper():
    """Demo the scraper with sample HTML content"""

    # Sample HTML content that matches what we'd expect from a real webpage
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Example Page Title</title>
        <meta name="description" content="This is an example page description for testing purposes">
        <meta property="og:description" content="Open Graph description">
    </head>
    <body>
        <h1>Main Title</h1>
        <p>This is the first paragraph with some content that explains what this page is about.</p>

        <h2>Section Title</h2>
        <p>This is another paragraph under the section. It contains more detailed information.</p>

        <h3>Subsection</h3>
        <p>Here is some content under the subsection.</p>

        <p>This is a standalone paragraph without a heading.</p>

        <h4>Level 4 Heading</h4>
        <p>Content under level 4 heading.</p>

        <h5>Level 5 Heading</h5>
        <p>Content under level 5 heading.</p>

        <h6>Level 6 Heading</h6>
        <p>Content under level 6 heading.</p>

        <p>Final paragraph with some <strong>formatting</strong> and <em>emphasis</em> that should be extracted as plain text.</p>
    </body>
    </html>
    """

    print("Demo: Testing web scraper functionality with sample HTML...")

    try:
        # Create a scraper instance
        scraper = WebScraper()

        # Parse the sample HTML
        soup = BeautifulSoup(sample_html, "html.parser")

        # Extract components manually to simulate the scraper workflow
        title = scraper._extract_title(soup)
        description = scraper._extract_description(soup)
        content = scraper._extract_content(soup)

        # Create result similar to what scrape() would return
        result = {
            "title": title,
            "url": "https://example.com",
            "description": description,
            "last_modified": "Mon, 13 Jan 2025 20:11:20 GMT",  # Example from the issue
            "content": content,
        }

        print("\n✅ Demo completed successfully!")
        print("\nExtracted data structure:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        # Validate the structure
        required_keys = ["title", "url", "description", "last_modified", "content"]
        print("\n📋 Validation:")
        for key in required_keys:
            if key in result and result[key]:
                print(
                    f"✅ {key}: {result[key][:50]}{'...' if len(str(result[key])) > 50 else ''}"
                )
            else:
                print(f"❌ Missing or empty: {key}")

        print("\n🎯 Content preview (first 200 chars):")
        print(f"{result['content'][:200]}...")

        return True

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False


if __name__ == "__main__":
    demo_scraper()
