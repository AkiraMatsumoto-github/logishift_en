#!/usr/bin/env python3
"""
LogiShift Automation Pipeline

Orchestrates the flow:
1. Collection (collector.py)
2. Scoring (scorer.py)
3. Selection (Filter high scores)
4. Generation (generate_article.py)
"""

import argparse
import json
import os
import sys
import subprocess
from datetime import datetime

def run_command(command):
    """Run a shell command and return output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
        return None
    return result.stdout

def main():
    parser = argparse.ArgumentParser(description="LogiShift Automation Pipeline")
    parser.add_argument("--days", type=int, help="Days to look back for collection")
    parser.add_argument("--hours", type=int, default=3, help="Hours to look back for collection (overrides --days)")
    parser.add_argument("--threshold", type=int, default=70, help="Score threshold for generation")
    parser.add_argument("--limit", type=int, default=2, help="Max articles to generate per run")
    parser.add_argument("--score-limit", type=int, default=0, help="Max articles to score (0 for all)")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode (no posting)")
    
    args = parser.parse_args()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    articles_file = os.path.join(base_dir, "collected_articles.json")
    scored_file = os.path.join(base_dir, "scored_articles.json")
    
    # 1. Collection
    print("\n=== Step 1: Collection ===")
    
    # Import modules directly
    sys.path.append(os.path.dirname(base_dir))
    from automation.collector import fetch_rss, DEFAULT_SOURCES
    from automation.scorer import score_articles_batch
    from automation.url_reader import extract_content
    from automation.summarizer import summarize_article
    from automation.classifier import ArticleClassifier
    from automation.gemini_client import GeminiClient
    from automation.wp_client import WordPressClient
    
    collected_articles = []
    if args.hours:
        print(f"Collecting articles from last {args.hours} hours...")
    else:
        print(f"Collecting articles from last {args.days} days...")
    for name, url in DEFAULT_SOURCES.items():
        fetched = fetch_rss(url, name, days=args.days, hours=args.hours)
        collected_articles.extend(fetched)
        
    print(f"Collected {len(collected_articles)} articles.")
    
    # 2. Scoring
    print("\n=== Step 2: Scoring ===")
    scored_articles = []
    
    articles_to_score = collected_articles
    if args.score_limit > 0:
        print(f"Limiting scoring to first {args.score_limit} articles.")
        articles_to_score = collected_articles[:args.score_limit]
    
    # Initialize GeminiClient once
    try:
        gemini_client = GeminiClient()
        print("GeminiClient initialized.")
    except Exception as e:
        print(f"Error initializing Gemini: {e}")
        gemini_client = None

    if gemini_client and articles_to_score:
        batch_size = 10
        print(f"Scoring {len(articles_to_score)} articles in batches of {batch_size}...")
        
        for i in range(0, len(articles_to_score), batch_size):
            batch = articles_to_score[i:i + batch_size]
            print(f"[{i+1}-{min(i+batch_size, len(articles_to_score))}/{len(articles_to_score)}] Processing batch...")
            
            try:
                batch_results = score_articles_batch(gemini_client, batch, start_id=i)
                scored_articles.extend(batch_results)
                 # Simple progress indication
                for res in batch_results:
                     print(f"  - Scored: {res.get('title', 'Unknown')[:40]}... -> {res.get('score', 0)} pts")
            except Exception as e:
                print(f"Error processing batch {i}: {e}")
    elif not gemini_client:
        print("Skipping scoring due to Client initialization failure.")
    else:
        print("No articles to score.")
            
    # Filter
    high_score_articles = [a for a in scored_articles if a["score"] >= args.threshold]
    high_score_articles.sort(key=lambda x: x["score"], reverse=True)
    
    print(f"\nFound {len(high_score_articles)} articles above threshold {args.threshold}.")
    
    # 3. Generation
    print("\n=== Step 3: Generation ===")
    count = 0
    
    # Initialize Classifier
    classifier = ArticleClassifier()
    
    # Initialize WP Client
    wp_client = WordPressClient()
    
    # Fetch recent posts for deduplication context
    print("Fetching recent WordPress posts for deduplication check...")
    existing_posts = wp_client.get_posts(limit=30) # Check last 30 posts (~1-2 weeks)
    existing_titles = []
    if existing_posts:
        existing_titles = [p['title']['rendered'] for p in existing_posts]
        print(f"Loaded {len(existing_titles)} existing post titles.")
    else:
        print("Warning: Could not fetch existing posts (or none exist). Deduplication will only check within current batch.")

    generated_titles_this_run = []

    for article in high_score_articles:
        if count >= args.limit:
            break
            
        print(f"Generating article for: {article['title']}")
        print(f"Score: {article['score']}")
        print(f"Reason: {article['reasoning']}")
        
        # Determine Type
        source = article.get("source", "")
        # Use dynamic classification
        article_type = classifier.classify_type(article['title'], article['summary'], source)
        print(f"Type: {article_type}")
        
        # Generate keyword
        keyword = article['title']
        
        # Base command
        cmd = [
            sys.executable, os.path.join(base_dir, "generate_article.py"),
            "--keyword", keyword,
            "--type", article_type
        ]
        
        # News/Global articles: Context-based generation (URL reading + summarization)
        if article_type in ["news", "global"]:
            print("\n--- Context-based generation (URL reading + summarization) ---")
            
            try:
                # Step 2.5-A: URL reading and summarization
                article_content = extract_content(article['url'], article['source'])
                
                if article_content['content'] and "Error" not in article_content['title']:
                    summary_data = summarize_article(article_content['content'], article['title'])

                    # --- Deduplication Check ---
                    # Check against existing WP posts and currently generated articles
                    candidate_summary = summary_data.get('summary', '')[:500] # Use the generated summary for better context
                    
                    check_against_titles = existing_titles + generated_titles_this_run
                    
                    print(f"Checking for duplicates against {len(check_against_titles)} existing items...")
                    if gemini_client:
                        is_duplicate = gemini_client.check_duplication(article['title'], candidate_summary, check_against_titles)
                    else:
                        is_duplicate = False # fallback
                    
                    if is_duplicate:
                        print(f"⚠️ SKIPPING DUPLICATE: {article['title']}")
                        print("Reason: Gemini detected this topic covers the same event as an existing or just-generated article.")
                        continue # Skip to next article
                    else:
                        print("✅ Duplication check passed. Proceeding.")
                        # Add to list for subsequent checks in this run
                        generated_titles_this_run.append(article['title'])
                    # ---------------------------
                    
                    # Pass context as JSON string
                    context_json = json.dumps(summary_data, ensure_ascii=False)
                    cmd.extend(["--context", context_json])
                    print(f"Context created: {len(summary_data['summary'])} chars summary, {len(summary_data['key_facts'])} key facts")
                else:
                    print("Warning: Failed to extract content, falling back to keyword-based generation")
            except Exception as e:
                print(f"Error during context creation: {e}")
                print("Falling back to keyword-based generation")
        else:
            print("\n--- Keyword-based generation (traditional) ---")
            pass
        
        if args.dry_run:
            cmd.append("--dry-run")
        
        subprocess.run(cmd)
        count += 1
        print("-" * 40)

if __name__ == "__main__":
    main()
