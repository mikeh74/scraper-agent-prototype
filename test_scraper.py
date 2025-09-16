#!/usr/bin/env python3
"""
Test script for the web scraper
"""

import json
import sys
from scraper import WebScraper


def test_scraper():
    """Test the scraper with example.com"""
    print("Testing web scraper with example.com...")
    
    try:
        scraper = WebScraper()
        result = scraper.scrape("https://example.com")
        
        print("\nScraper test completed successfully!")
        print("\nResult:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Validate the structure
        required_keys = ["title", "url", "description", "last_modified", "content"]
        for key in required_keys:
            if key not in result:
                print(f"❌ Missing required key: {key}")
                return False
            else:
                print(f"✅ Found required key: {key}")
        
        print(f"\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_scraper()
    sys.exit(0 if success else 1)