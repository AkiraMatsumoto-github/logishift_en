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

# Editorial Persona and Scoring Criteria (Shared Context)
SCORING_CONTEXT = """You are the "Editor-in-Chief" of LogiShift Global, a logistics DX media.
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
"""

BATCH_SCORING_PROMPT = SCORING_CONTEXT + """
【Instructions】
You will be provided with a list of articles.
For EACH article, provide a score (0-100), reasoning, and relevance assessment.

【Input Articles】
{articles_text}

【Output Format】
Output ONLY a JSON Array containing an object for each article in the same order as the input.
[
    {{
        "id": <Article ID>,
        "score": <Integer 0-100>,
        "reasoning": "<Concise reasoning>",
        "relevance": "<high/medium/low>"
    }},
    ...
]
"""

SINGLE_SCORING_PROMPT = SCORING_CONTEXT + """
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

def score_articles_batch(client, articles, start_id, model_name="gemini-3-flash-preview"):
    """
    Score a batch of articles using a single Gemini API call.
    """
    if not articles:
        return []

    # Format articles for the prompt
    articles_text = ""
    for i, article in enumerate(articles):
        # Use simple ID relative to this batch (or global if we want, but passing start_id helps debugging)
        article_id = start_id + i
        articles_text += f"Article ID: {article_id}\n"
        articles_text += f"Title: {article.get('title', 'Unknown')}\n"
        articles_text += f"Source: {article.get('source', 'Unknown')}\n"
        articles_text += f"Summary: {article.get('summary', '')}\n\n"

    prompt = BATCH_SCORING_PROMPT.format(articles_text=articles_text)

    try:
        response = client.generate_content(prompt, model=model_name)
        
        if not response:
            raise Exception("No response from Gemini API")

        result_text = response.text.strip()
        
        # Extract JSON
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        try:
            results_list = json.loads(result_text)
        except json.JSONDecodeError:
            # Fallback: sometimes Gemini returns just the object if only 1 item, or separate objects
            print(f"JSON Decode Error in batch. Raw text: {result_text[:100]}...", file=sys.stderr)
            raise

        scored_batch = []
        
        # Create a map of ID -> Result for safer mapping
        result_map = {str(r.get("id")): r for r in results_list if "id" in r}
        
        # If mapping fails (e.g. Gemini didn't output IDs), assume order if lengths match
        if len(result_map) != len(articles) and len(results_list) == len(articles):
             # print("Warning: ID mismatch or missing IDs. Assuming sequential order.", file=sys.stderr)
             result_map = {str(start_id + i): res for i, res in enumerate(results_list)}

        for i, article in enumerate(articles):
            a_id = start_id + i
            res = result_map.get(str(a_id))
            
            if res:
                scored_batch.append({
                    "title": article.get("title"),
                    "url": article.get("url"),
                    "source": article.get("source"),
                    "summary": article.get("summary", ""),
                    "score": res.get("score", 0),
                    "reasoning": res.get("reasoning", ""),
                    "relevance": res.get("relevance", "low")
                })
            else:
                 # Fallback if specific article missing from batch response
                 print(f"Warning: Article {a_id} missing from batch response. Scoring individually...", file=sys.stderr)
                 scored_batch.append(score_single_article(client, article, model_name))

        return scored_batch

    except Exception as e:
        print(f"Batch scoring failed: {e}. Falling back to individual scoring.", file=sys.stderr)
        # Fallback to individual scoring upon batch failure
        fallback_results = []
        for article in articles:
            fallback_results.append(score_single_article(client, article, model_name))
        return fallback_results

def score_single_article(client, article, model_name="gemini-3-flash-preview"):
    """Score a single article (fallback or legacy usage)."""
    prompt = SINGLE_SCORING_PROMPT.format(
        title=article.get("title", ""),
        summary=article.get("summary", ""),
        source=article.get("source", "")
    )
    
    try:
        response = client.generate_content(prompt, model=model_name)
        if not response:
            raise Exception("No response")
            
        result_text = response.text.strip()
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
        print(f"Error scoring individual article: {e}", file=sys.stderr)
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
    parser.add_argument("--model", type=str, default="gemini-3-flash-preview", help="Gemini model to use")
    
    args = parser.parse_args()
    
    # Load articles
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except Exception as e:
        print(f"Error loading input file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Initialize Client ONCE
    try:
        client = GeminiClient()
    except Exception as e:
        print(f"Fatal Error: Failed to initialize GeminiClient: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Scoring {len(articles)} articles using {args.model} (Batch Size: 10)...")
    
    scored_articles = []
    batch_size = 10
    
    for i in range(0, len(articles), batch_size):
        batch = articles[i:i + batch_size]
        print(f"[{i+1}-{min(i+batch_size, len(articles))}/{len(articles)}] Processing batch...")
        
        batch_results = score_articles_batch(client, batch, start_id=i, model_name=args.model)
        scored_articles.extend(batch_results)
        
        # Simple progress indication
        for res in batch_results:
             print(f"  - Scored: {res.get('title', 'Unknown')[:40]}... -> {res.get('score')} pts")

    
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
            print(f"\n[{article['score']}pts] {article['title']}")
            print(f"  URL: {article['url']}")
            print(f"  Reasoning: {article['reasoning']}")
    
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
