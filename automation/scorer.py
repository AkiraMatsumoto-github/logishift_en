#!/usr/bin/env python3
"""
Article Relevance Scorer for LogiShift

Evaluates articles using Gemini API based on LogiShift's editorial persona:
- DX Evangelist perspective
- Focus on cost reduction and feasibility
- Future potential evaluation
"""

import argparse
import json
import os
import sys
from dotenv import load_dotenv
try:
    from automation.gemini_client import GeminiClient
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from automation.gemini_client import GeminiClient

# Editorial Persona and Scoring Criteria
SCORING_PROMPT = """You are the "Editor-in-Chief" of LogiShift Global, a logistics DX media.
Evaluate whether the following article is beneficial for our target audience: "Logistics Warehouse Managers" and "Supply Chain Executives (Global)".

【Target Persona】
- Role: Logistics Operations Manager or C-level Executive.
- Challenges: Labor shortages, Cost reduction, Legacy system modernization.
- Interests: Global Industry Trends, Efficiency Methods, Case Studies, Latest Tech (Automation/Robotics).

【Scoring Criteria】 (Total 100 points)

1. **Relevance to Global Logistics & Strategy** (0-40 points)
   - Is it highly relevant to logistics, SCM, or warehouse operations?
   - Does it address accurate global market trends or supply chain challenges?
   - Is it critical information for a C-level executive or Manager?

2. **Innovation & Modernization** (0-20 points)
   - Does it cover Technology (DX), Automation, OR Process Innovation (Kaizen)?
   - *Note: Pure strategic moves or regulatory changes are also "Innovation" if they modernize the industry.*

3. **Managerial Utility** (0-30 points)
   - Is this helpful for decision making (strategy, purchasing, hiring)?
   - Does it provide actionable insights or essential knowledge?
   - Is it "Must Read" vs "Nice to know"?

4. **Freshness** (0-10 points)
   - Is it timely news?
   - Does it feature major players or significant shifts?

【Article Info】
Title: {title}
Summary: {summary}
Source: {source}

【Output Format】
Output ONLY the following JSON format:
{{
  "score": <Integer 0-100>,
  "reasoning": "<Concise reasoning in English from the Editor's perspective (2-3 sentences)>",
  "relevance": "<high/medium/low>"
}}
"""

def score_article(article, model_name="gemini-3-pro-preview"):
    """Score a single article using Gemini API."""
    
    try:
        client = GeminiClient()
    except Exception as e:
        print(f"Error initializing GeminiClient: {e}", file=sys.stderr)
        return {
            "title": article.get("title"),
            "url": article.get("url"),
            "source": article.get("source"),
            "summary": article.get("summary", ""),
            "score": 0,
            "reasoning": f"Initialization Error: {str(e)}",
            "relevance": "error"
        }
    
    prompt = SCORING_PROMPT.format(
        title=article.get("title", ""),
        summary=article.get("summary", ""),
        source=article.get("source", "")
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
        
        return {
            "title": article.get("title"),
            "url": article.get("url"),
            "source": article.get("source"),
            "summary": article.get("summary", ""),
            "score": result.get("score", 0),
            "reasoning": result.get("reasoning", ""),
            "relevance": result.get("relevance", "low")
        }
        
    except Exception as e:
        print(f"Error scoring article '{article.get('title', 'Unknown')}': {e}", file=sys.stderr)
        return {
            "title": article.get("title"),
            "url": article.get("url"),
            "source": article.get("source"),
            "summary": article.get("summary", ""),
            "score": 0,
            "reasoning": f"Error: {str(e)}",
            "relevance": "error"
        }

def main():
    parser = argparse.ArgumentParser(description="Score articles for relevance to LogiShift.")
    parser.add_argument("--input", type=str, help="Path to JSON file with articles (from collector.py)", required=True)
    parser.add_argument("--threshold", type=int, default=80, help="Minimum score to pass (default: 80)")
    parser.add_argument("--output", type=str, help="Output file for scored articles (optional)")
    parser.add_argument("--model", type=str, default="gemini-3-pro-preview", help="Gemini model to use")
    
    args = parser.parse_args()
    
    # Load articles
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except Exception as e:
        print(f"Error loading input file: {e}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Scoring {len(articles)} articles using {args.model}...")
    
    scored_articles = []
    for i, article in enumerate(articles, 1):
        print(f"[{i}/{len(articles)}] Scoring: {article.get('title', 'Unknown')[:60]}...")
        scored = score_article(article, args.model)
        scored_articles.append(scored)
    
    # Filter by threshold
    high_score_articles = [a for a in scored_articles if a["score"] >= args.threshold]
    
    print(f"\n{'='*60}")
    print(f"Scoring complete!")
    print(f"Total articles: {len(articles)}")
    print(f"High-score articles (>={args.threshold}): {len(high_score_articles)}")
    print(f"{'='*60}\n")
    
    # Display high-score articles
    if high_score_articles:
        print("High-score articles:")
        for article in sorted(high_score_articles, key=lambda x: x["score"], reverse=True):
            print(f"\n[{article['score']}点] {article['title']}")
            print(f"  URL: {article['url']}")
            print(f"  理由: {article['reasoning']}")
    
    # Save output if specified
    if args.output:
        output_data = {
            "threshold": args.threshold,
            "total": len(articles),
            "high_score_count": len(high_score_articles),
            "articles": scored_articles,
            "high_score_articles": high_score_articles
        }
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {args.output}")

if __name__ == "__main__":
    main()
