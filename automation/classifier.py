import json
import re
try:
    from automation.gemini_client import GeminiClient
except ImportError:
    from gemini_client import GeminiClient

class ArticleClassifier:
    def __init__(self):
        self.gemini = GeminiClient()
        
    def classify_article(self, title, content_summary):
        """
        Classify an article into Category, Industry Tags, and Theme Tags.
        
        Returns:
            dict: {
                "category": "slug",
                "industry_tags": ["slug1", "slug2"],
                "theme_tags": ["slug1", "slug2"]
            }
        """
        
        prompt = f"""
        You are an Editor for the logistics media "LogiShift Global".
        Analyze the following article title and summary, and select the most appropriate "Category (Select 1)" and "Tags (Multiple allowed)".

        ## Article Info
        Title: {title}
        Summary: {content_summary}

        ## 1. Category (Select EXACTLY ONE)
        - Global Trends (global-trends)
        - Technology & DX (technology-dx)
        - Cost & Efficiency (cost-efficiency)
        - Supply Chain Management (scm)
        - Case Studies (case-studies)
        - Logistics Startups (startups)
        * Note: If the content is about non-domestic trends or case studies, MUST select "Global Trends (global-trends)".

        ## 2. Industry Tags (Select 1 if applicable, else empty)
        - Manufacturing (manufacturing)
        - Retail (retail)
        - eCommerce (ecommerce)
        - 3PL / Warehousing (3pl-warehouse)
        - Food & Beverage (food-beverage)
        - Apparel (apparel)
        - Medical / Pharma (medical)

        ## 3. Theme Tags (Select multiple if applicable, else empty)
        - Cost Reduction (cost-reduction)
        - Labor Shortage (labor-shortage)
        - Kaizen / Quality Improvement (kaizen)
        - Sustainability (sustainability)
        - Warehouse Automation (automation)
        - Last Mile (last-mile)
        - Safety / BCP (safety-bcp)
        - Subsidy (subsidy)

        ## 4. Region Tags (Select 1 (REQUIRED))
        - USA / North America (usa)
        - Europe (europe)
        - Asia-Pacific (asia-pacific)
        - Japan (japan)
        * Note: You MUST select exactly one region. If the news is global, select the most dominant region or origin.

        ## Output Format (Strict JSON)
        {{
            "category": "slug",
            "industry_tags": ["slug1", "slug2"],
            "theme_tags": ["slug1", "slug2"],
            "region_tags": ["slug1"]
        }}
        """
        
        try:
            response = self.gemini.client.models.generate_content(
                model='gemini-3-flash-preview',
                contents=prompt,
                config={
                    'response_mime_type': 'application/json'
                }
            )
            response_text = response.text
            # Clean up JSON markdown if present (though response_mime_type should handle it)
            response_text = re.sub(r'```json\n|\n```', '', response_text).strip()
            result = json.loads(response_text)
            return result
        except Exception as e:
            print(f"Classification failed: {e}")
            # Default fallback
            return {
                "category": "technology-dx",
                "industry_tags": [],
                "theme_tags": [],
                "region_tags": []
            }

            
    def classify_type(self, title, summary, source=""):
        """
        Classify the article type based on title and summary.
        
        Args:
            title: Article title
            summary: Article summary
            source: Source identifier (optional)
            
        Returns:
            str: One of [know, buy, do, news, global]
        """
        
        # 1. Check for Global/News based on source/content first (Low cost)
        # For English Site: 
        # - Asian/Japanese sources are "Global Trends" (foreign context) -> 'global'
        # - Western sources are standard -> Let Gemini decide (likely 'news' or 'know/buy/do')
        if source in ["lnews", "logistics_today", "logi_biz", "36kr_japan", "pandaily", "supply_chain_asia"]:
            return "global"
            
        # 2. Use Gemini for semantic classification (High accuracy)
        prompt = f"""
        You are the Editor-in-Chief of a logistics media.
        Classify the following article plan into one of the 5 article types (formats) that delivers the most value to the reader.

        Article Title: {title}
        Article Summary: {summary}

        ## Options (Choose ONE)
        1. know  (Educational: "What is WMS", "Mechanisms of DX", basics and definitions)
        2. buy   (Comparison/Selection: "Top 10 WMS", "How to choose", comparison guides)
        3. do    (Practical/Case Study: "Success Stories", "How-to guides", "Road to Zero Errors")
        4. news  (Domestic News: Latest administrative trends, press releases, personnel changes - time sensitive)
        5. global (Global News: International supply chain trends, cross-border logistics, and multi-region analysis)

        ## Decision Rules
        - If it covers multiple regions or international trade -> "global"
        - If "Comparison", "Selection", "Recommended" -> "buy"
        - If "Case Study", "Success", "Practical" -> "do"
        - If "What is", "Mechanism", "Benefits" (Fundamentals) -> "know"
        - If specific dates, "breaking news", or highly time-sensitive -> "news"
        
        Output ONLY the type name in lowercase: know, buy, do, news, or global.
        """

        try:
            response = self.gemini.client.models.generate_content(
                model='gemini-3-flash-preview',
                contents=prompt,
                config={
                    'response_mime_type': 'text/plain'
                }
            )
            result = response.text.strip().lower()
            
            # Validation
            valid_types = ["know", "buy", "do", "news", "global"]
            found_type = "news" # default
            
            for t in valid_types:
                if t in result:
                    found_type = t
                    break
            
            print(f"  > Classification result: {found_type} (Raw: {result})")
            return found_type

        except Exception as e:
            print(f"Type classification failed: {e}")
            return "news" # Safe fallback

