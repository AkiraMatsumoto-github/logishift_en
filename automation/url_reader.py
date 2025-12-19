#!/usr/bin/env python3
"""
URL Content Extractor for LogiShift

Extracts article content from URLs using BeautifulSoup.
Supports major logistics news sources with fallback to Gemini URL reading.
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import sys

# Content selectors for each source
CONTENT_SELECTORS = {
    "techcrunch": {
        "content": "div.article-content",
        "title": "h1",
        "author": "a[rel='author']",
    },
    "wsj_logistics": {
        "content": "div.article-content",
        "title": "h1.wsj-article-headline",
        "author": "span.author-name",
    },
    "lnews": {
        "content": "div.entry-content",
        "title": "h1.entry-title",
        "author": "span.author",
    },
    "logistics_today": {
        "content": "div.entry-content",
        "title": "h1.entry-title",
        "author": "span.author",
    },
    "logi_biz": {
        "content": "div.entry-content",
        "title": "h1.entry-title",
        "author": "span.author",
    },
    "supply_chain_dive": {
        "content": "div.article-body",
        "title": "h1.article-title",
        "author": "span.author-name",
    },
    "logistics_mgmt": {
        "content": "div.article-body",
        "title": "h1",
        "author": "span.author",
    },
    "freightwaves": {
        "content": "div.entry-content",
        "title": "h1.entry-title",
        "author": "a.author",
    },
    "robot_report": {
        "content": "div.entry-content",
        "title": "h1",
        "author": ".entry-author",
    },
    "supply_chain_brain": {
        "content": "div.editorial-content__body", # Updated from div.body
        "title": "h1",
        "author": ".author",
    },
    "robotics_automation_news": {
        "content": "div.entry-content",
        "title": "h1",
        "author": ".entry-author",
    },
    "36kr_japan": {
        "content": "div.entry-content",
        "title": "h1",
        "author": ".post-author",
    },
    "pandaily": {
        "content": "div.prose",
        "title": "h1",
        "author": "div.flex.items-center span",
    },
    "the_loadstar": {
        "content": "div.entry-content", # Changed from article-body
        "title": "h1",
        "author": ".author",
    },
    "logistics_manager_uk": {
        "content": "div.entry-content",
        "title": "h1",
        "author": "a[rel='author']",
    },
    "supply_chain_asia": {
        "content": "div.entry-content",
        "title": "h1",
        "author": ".author",
    },
}


def extract_content(url: str, source: str) -> Dict[str, str]:
    """
    Extract article content from URL.
    
    Args:
        url: Article URL
        source: Source name (e.g., 'techcrunch', 'lnews')
    
    Returns:
        Dictionary with keys: title, content, author, url
    """
    print(f"Extracting content from {source}: {url}")
    
    # Get selectors for this source
    selectors = CONTENT_SELECTORS.get(source)
    
    if not selectors:
        print(f"Warning: No selectors defined for source '{source}', using generic extraction")
        selectors = {
            "content": "article, div.content, div.post-content, div.entry-content",
            "title": "h1",
            "author": "span.author, a.author, span.author-name",
        }
    
    try:
        # Fetch URL
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Extract title
        title_elem = soup.select_one(selectors["title"])
        title = title_elem.get_text(strip=True) if title_elem else "No Title"
        
        # Extract content
        content_elem = soup.select_one(selectors["content"])
        if content_elem:
            # Remove script and style tags
            for tag in content_elem.find_all(['script', 'style', 'nav', 'aside']):
                tag.decompose()
            content = content_elem.get_text(separator='\n', strip=True)
        
        # If content selector found nothing or text is empty, try fallback
        if not content_elem or not content:
            print(f"Warning: Content selector '{selectors['content']}' yielded empty result. Using fallback.")
            # Fallback: get all paragraphs
            paragraphs = soup.find_all('p')
            content = '\n'.join([p.get_text(strip=True) for p in paragraphs])
        
        # Extract author
        author_elem = soup.select_one(selectors["author"])
        author = author_elem.get_text(strip=True) if author_elem else "Unknown"
        
        result = {
            "title": title,
            "content": content,
            "author": author,
            "url": url,
        }
        
        print(f"Successfully extracted: {len(content)} chars")
        return result
        
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return {
            "title": "Error",
            "content": f"Failed to fetch content: {str(e)}",
            "author": "Unknown",
            "url": url,
        }
    except Exception as e:
        print(f"Error parsing content: {e}")
        return {
            "title": "Error",
            "content": f"Failed to parse content: {str(e)}",
            "author": "Unknown",
            "url": url,
        }


def main():
    """Test URL extraction"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract content from URL")
    parser.add_argument("--url", type=str, required=True, help="URL to extract")
    parser.add_argument("--source", type=str, required=True, help="Source name")
    
    args = parser.parse_args()
    
    result = extract_content(args.url, args.source)
    
    print("\n=== Extraction Result ===")
    print(f"Title: {result['title']}")
    print(f"Author: {result['author']}")
    print(f"Content Length: {len(result['content'])} chars")
    print(f"\nContent Preview:\n{result['content'][:500]}...")


if __name__ == "__main__":
    main()
