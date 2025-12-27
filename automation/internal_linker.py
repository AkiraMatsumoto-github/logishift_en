import json
from typing import List, Dict, Optional

class InternalLinkSuggester:
    """
    Suggests relevant internal links for a new article based on existing content.
    Phase 1: One-way linking (New Article -> Existing Articles).
    """

    def __init__(self, wp_client, gemini_client):
        self.wp = wp_client
        self.gemini = gemini_client

    def fetch_candidates(self) -> List[Dict]:
        """
        Fetch existing posts from WordPress to serve as link candidates.
        Prioritizes:
        1. Popular Posts (Top 20 by PV in last 7 days)
        2. Recent Posts (100)
        """
        print("Fetching internal linking candidates...")

        # 1. Fetch Popular Posts
        print("Fetching popular posts (Top 20, 7 days)...")
        popular_posts = self.wp.get_popular_posts(days=7, limit=20)
        if not popular_posts:
            popular_posts = []
        print(f"Fetched {len(popular_posts)} popular posts.")

        # 2. Fetch Recent Posts
        print("Fetching recent posts (Limit 100)...")
        recent_posts = self.wp.get_posts(limit=100, status="publish")
        if not recent_posts:
            recent_posts = []
        print(f"Fetched {len(recent_posts)} recent posts.")

        # 3. Merge and Deduplicate
        all_posts = []
        seen_ids = set()

        # Helper to process and add post
        def add_post(post):
            pid = post['id']
            if pid in seen_ids:
                return
            
            seen_ids.add(pid)
            
            ai_summary_json = None
            if 'meta' in post and 'ai_structured_summary' in post['meta']:
                 try:
                     # Check if it's already a dict or needs parsing
                     meta_val = post['meta']['ai_structured_summary']
                     if isinstance(meta_val, str):
                        ai_summary_json = json.loads(meta_val)
                     elif isinstance(meta_val, dict):
                        ai_summary_json = meta_val
                 except:
                     pass
            
            summary_text = ""
            if ai_summary_json:
                summary_text = f"Title: {post['title']['rendered']}\nSummary: {ai_summary_json.get('summary', '')}\nTopics: {', '.join(ai_summary_json.get('key_topics', []))}\nEntities: {', '.join(ai_summary_json.get('entities', []))}"
            else:
                excerpt_raw = post['excerpt']['rendered'] if 'excerpt' in post else ""
                summary_text = f"Title: {post['title']['rendered']}\nExcerpt: {self._clean_excerpt(excerpt_raw)}"

            # Add marker for popular posts
            is_popular = hasattr(post, 'views') or 'views' in post
            if is_popular:
                summary_text = "[POPULAR] " + summary_text

            all_posts.append({
                "id": pid,
                "title": post['title']['rendered'],
                "url": post['link'],
                "summary_context": summary_text, # Store combined context for prompting
                "excerpt": self._clean_excerpt(post['excerpt']['rendered'] if 'excerpt' in post else ""),
                "is_popular": is_popular
            })

        # Process Popular first (Higher Priority)
        for p in popular_posts:
            add_post(p)
            
        # Process Recent second
        for p in recent_posts:
            add_post(p)
        
        print(f"Total unique candidates loaded: {len(all_posts)}")
        return all_posts

    def score_relevance(self, new_article_keyword: str, new_article_context: str, candidates: List[Dict]) -> List[Dict]:
        """
        Score the relevance of candidate articles against the new article's topic.
        Returns a list of highly relevant articles (score >= 80).
        """
        if not candidates:
            return []

        print(f"Scoring candidate relevance with Gemini (Candidates: {len(candidates)})...")
        
        # Prepare candidates for the prompt
        candidates_text = ""
        for c in candidates:
            # Use the rich summary context if available
            candidates_text += f"- ID: {c['id']} | {c['summary_context']}\n"

        prompt = f"""
        You are an SEO expert. We are writing a new article about "{new_article_keyword}".
        Context/Outline of new article: {new_article_context[:500]}...

        Evaluate the following existing articles and determine which ones are HIGHLY RELEVANT to the new article.
        Relevance means the existing article provides valuable supplementary information, detailed explanation of a sub-topic, or a related case study.
        
        Note: Articles marked [POPULAR] have high traffic. If they are relevant, prioritize checks for them as they are good for SEO.

        Existing Articles:
        {candidates_text}

        Task:
        1. Rate each article's relevance from 0 to 100.
        2. Select only articles with valid relevance >= 80.
        3. Return the result in JSON format:
        [
            {{"id": 123, "title": "Title", "score": 95, "reason": "Explains the specific tech mentioned in new article"}},
            ...
        ]
        
        Output JSON only. If no articles are relevant, output [].
        """

        try:
            response = self.gemini.generate_content(prompt)
            if not response or not response.text:
                print("No response from Gemini for relevance scoring.")
                return []
                
            response_text = response.text
            # basic cleanup for code blocks if gemini adds them
            clean_text = response_text.replace('```json', '').replace('```', '').strip()
            results = json.loads(clean_text)
            
            # Map back to full candidate objects
            relevant_posts = []
            for res in results:
                if res['score'] >= 80:
                    # Find original candidate data
                    original = next((c for c in candidates if c['id'] == res['id']), None)
                    if original:
                        original['relevance_score'] = res['score']
                        original['relevance_reason'] = res.get('reason', '')
                        relevant_posts.append(original)
            
            # Sort by score desc
            relevant_posts.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            print(f"Found {len(relevant_posts)} highly relevant articles.")
            return relevant_posts[:5] # Return top 5 max

        except Exception as e:
            print(f"Error during relevance scoring: {e}")
            return []

    def _clean_excerpt(self, html_excerpt: str) -> str:
        """Remove HTML tags from excerpt for cleaner prompt usage."""
        # Simple tag removal
        import re
        clean = re.sub('<[^<]+?>', '', html_excerpt)
        return clean.strip()
