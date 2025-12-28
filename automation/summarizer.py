#!/usr/bin/env python3
"""
Article Summarizer for LogiShift

Summarizes article content and extracts key facts using Gemini API.
Adds LogiShift perspective (DX Evangelist viewpoint).
"""

import os
import sys
import json
from dotenv import load_dotenv
try:
    from automation.gemini_client import GeminiClient
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from automation.gemini_client import GeminiClient

SUMMARIZATION_PROMPT = """You are the "Editor-in-Chief" of LogiShift Global, a logistics DX media.
Summarize the following article and extract key insights for our target audience (Global Logistics Managers & Supply Chain Executives).

【Original Article】
Title: {title}
Content: {content}

【Output Format】
Output ONLY the following JSON format:
{{
  "summary": "Concise summary (approx. 300 chars). Explain 'What happened' and 'Why it matters' clearly.",
  "key_facts": [
    "Key Stat/Fact 1 (e.g., Cost reduction %, Adoption numbers)",
    "Key Entity/Product Name",
    "Main Conclusion or Takeaway"
  ],
  "logishift_angle": "Editor's Comment (approx. 150 chars). As a DX Evangelist, explain the global impact or cross-border implications of this news. Why should a global logistics manager care?"
}}

【Notes】
- Keep key_facts to 3-5 items.
- Be precise with numbers.
- The 'logishift_angle' should be insightful and action-oriented, not just a reaction.
"""


def summarize_article(content: str, title: str, model_name: str = "gemini-3-pro-preview") -> dict:
    """
    Summarize article content and extract key facts.
    
    Args:
        content: Article content
        title: Article title
        model_name: Gemini model to use
    
    Returns:
        Dictionary with keys: summary, key_facts, logishift_angle
    """
    print(f"Summarizing article: {title[:50]}...")
    
    # Removed content truncation to support long articles with Gemini 1.5+
    
    try:
        client = GeminiClient()
    except Exception as e:
        print(f"Error initializing GeminiClient: {e}")
        return {
            "summary": f"要約生成に失敗しました: {str(e)}",
            "key_facts": [],
            "logishift_angle": "分析できませんでした。"
        }
    
    prompt = SUMMARIZATION_PROMPT.format(
        title=title,
        content=content
    )
    
    try:
        # Use GeminiClient's generate_content which has retry logic
        response = client.generate_content(prompt, model=model_name)
        
        if not response:
            raise Exception("No response from Gemini API")
        
        result_text = response.text.strip()
        
        # Extract JSON from markdown code blocks if present
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(result_text)
        
        print(f"Summary: {result['summary'][:100]}...")
        print(f"Key facts: {len(result['key_facts'])} items")
        
        return result
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Response text: {result_text}")
        return {
            "summary": f"要約生成に失敗しました: {str(e)}",
            "key_facts": [],
            "logishift_angle": "分析できませんでした。"
        }
    except Exception as e:
        print(f"Error summarizing article: {e}")
        return {
            "summary": f"要約生成に失敗しました: {str(e)}",
            "key_facts": [],
            "logishift_angle": "分析できませんでした。"
        }


def main():
    """Test summarization"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Summarize article content")
    parser.add_argument("--title", type=str, required=True, help="Article title")
    parser.add_argument("--content", type=str, required=True, help="Article content")
    parser.add_argument("--model", type=str, default="gemini-2.0-flash-exp", help="Gemini model")
    
    args = parser.parse_args()
    
    result = summarize_article(args.content, args.title, args.model)
    
    print("\n=== Summarization Result ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
