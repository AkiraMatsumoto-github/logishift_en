# -*- coding: utf-8 -*-
import os
import base64
from google import genai
from google.genai import types
from dotenv import load_dotenv
import time
import random

load_dotenv(override=True)

class GeminiClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION")
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        self.use_vertex = False

        # Prioritize Vertex AI initialization
        if self.project_id and self.location:
            try:
                print(f"Initializing Gemini with Vertex AI (Project: {self.project_id}, Location: {self.location})")
                self.client = genai.Client(vertexai=True, project=self.project_id, location=self.location)
                self.use_vertex = True
            except Exception as e:
                print(f"Warning: Vertex AI initialization failed: {e}, falling back to API Key.")
                self.use_vertex = False
        
        # Fallback to API Key if Vertex AI is not available
        if not self.use_vertex:
            if self.api_key:
                print("Initializing Gemini with API Key (google-genai)")
                self.client = genai.Client(api_key=self.api_key)
            else:
                raise ValueError("Missing Gemini credentials. Set GOOGLE_CLOUD_PROJECT/LOCATION or GEMINI_API_KEY in .env")

    def _retry_request(self, func, *args, **kwargs):
        """
        Retry a function call with exponential backoff if a quota error occurs.
        """
        max_retries = 5
        base_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_str = str(e).lower()
                # Check for rate limit/quota errors
                if "429" in error_str or "quota" in error_str or "exhausted" in error_str:
                    if attempt == max_retries - 1:
                        print(f"Max retries ({max_retries}) exceeded for quota error.")
                        raise e
                    
                    delay = (base_delay * (2 ** attempt)) + (random.random() * 1)
                    print(f"Quota exceeded (429). Retrying in {delay:.2f}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                else:
                    # Not a quota error, raise immediately
                    raise e

    def generate_content(self, prompt, model='gemini-3-pro-preview', config=None):
        """
        Generic method to generate content with retry logic.
        """
        try:
            response = self._retry_request(
                self.client.models.generate_content,
                model=model,
                contents=prompt,
                config=config
            )
            return response
        except Exception as e:
            # Fallback for Vertex AI Auth errors
            if self.use_vertex and "Reauthentication is needed" in str(e):
                print(f"Vertex AI Auth failed ({e}). Switching to API Key...")
                try:
                    self.use_vertex = False
                    self.client = genai.Client(api_key=self.api_key)
                    # Retry with new client
                    response = self._retry_request(
                        self.client.models.generate_content,
                        model=model,
                        contents=prompt,
                        config=config
                    )
                    return response
                except Exception as fallback_e:
                    print(f"Fallback to API Key failed: {fallback_e}")
                    return None

            print(f"Error generating content: {e}")
            return None

    def generate_article(self, keyword, article_type="know", context=None, extra_instructions=None):
        """
        Generate a full blog article in Markdown format based on the keyword and type.
        """
        print(f"Generating article for keyword: {keyword} (Type: {article_type})")
        
        context_section = ""
        if context:
            context_section = f"""
            ## Context Information
            The following external information is relevant to the topic. Use it to ensure accuracy and freshness.
            Summary: {context.get('summary', '')}
            Key Facts: {', '.join(context.get('key_facts', []))}
            """
            
        prompts = {
            "know": f"""
            {context_section}You are an expert logistics content writer (SEO specialist).
            Write a comprehensive educational article on the following keyword that deeply satisfies the reader's search intent.
            
            Keyword: {keyword}
            
            ## Target Audience
            - Logistics beginners to intermediate professionals
            - Operations leaders and executives facing efficiency/cost challenges
            
            ## Structure
            1. **Introduction**:
               - [Empathy] Address specific pain points (e.g., "Rising costs," "Labor shortage").
               - [Solution] State clearly how this article helps.
            2. **Basics**: What is {keyword}? (Clear, easy-to-understand explanation)
            3. **Why Now?**: Relevance in the current market (Global supply chain trends, Digital Transformation).
            4. **Benefits**: Quantitative and qualitative advantages of adoption.
            5. **Implementation**: Key points for successful introduction/implementation.
            6. **Conclusion**: Recommended next steps.
            
            ## Writing Rules (SEO & Quality)
            - **Keywords**: Naturally include clear industry terminology related to {keyword}.
            - **Authority**: Cite general statistics or well-known industry facts where possible (Do not make up data).
            - **Readability**: Short sentences, frequent paragraph breaks, and bullet points.
            
            ## Format
            - Markdown format
            - Approx. 1500-2000 words
            - **Use Markdown Tables for complex info (Max 3 columns for mobile).**
            - **NO HTML tags in tables.**
            
            ## Title Generation Rules
            - **Goal**: Maximize CTR.
            - **Length**: STRICTLY under 60 characters.
            - **Structure**:
                1. Keyword at the start.
                2. Benefit/Promise (e.g., "Guide", "Cost Reduction").
            
            ## Title Examples
            - {keyword} Guide: Essential Logistics Strategies
            - 5 Benefits of {keyword} for Warehousing
            - Implementing {keyword}: Reduce Costs by 20%
            
            Produce a title based on these principles.
            ## Constraints
            - Do not introduce yourself.
            - **ABSOLUTELY NO HTML TAGS** (<br>, <p>, <div>, etc.).
            """,
            
            "buy": f"""
            You are a Logistics DX Consultant.
            Write a comparison/selection guide for solutions related to the keyword.
            
            Keyword: {keyword}
            
            ## Target
            - Decision makers considering system/equipment purchase.
            
            ## Structure
            1. **Introduction**: Risks of choosing the wrong solution.
            2. **Selection Criteria**: Price, Support, Scalability, Usability.
            3. **Types**: Categorize available solutions (e.g., Cloud vs On-premise).
            4. **Pros & Cons**: Fair comparison.
            5. **Recommendation**: Best choice by company size/need.
            
            ## Rules
            - **Comparison Table**: MUST include a Markdown comparison table.
            - **Neutrality**: Be fair and objective.
            
            ## Format
            - Markdown
            - Comparison Table required (NO HTML tags).
            - Approx. 1500-2000 words.
            
            ## Title Rules
            - **Goal**: Capture "Buy" intent.
            - **Length**: STRICTLY under 60 characters.
            - **Elements**: Keyword, Numbers ("Top 10"), Year ("2025").
            - **Examples**:
                - Top 10 {keyword} Systems 2025: Pricing Compared
                - Best {keyword}: A Buyer's Guide
            """,
            
            "do": f"""
            You are a Logistics DX Evangelist.
            Write a practical "How-to" guide or case study article.
            
            Keyword: {keyword}
            
            ## Target
            - Warehouse managers seeking operational improvements.
            
            ## Structure
            1. **Introduction**: Common operational pain (Before).
            2. **Solution**: Specific method/technique using {keyword} (What).
            3. **Process**: Step-by-step implementation guide (How).
            4. **Results**: Expected improvements (After).
            5. **Summary**: Keys to success.
            
            ## Format
            - Markdown
            - Use specific steps and numbers.
            - **Use Markdown Tables for steps or Before/After comparisons (NO HTML).**
            - Approx. 1500 words.
            
            ## Title Rules
            - **Goal**: Solves "Do" intent (Actionable).
            - **Length**: STRICTLY under 60 characters.
            - **Elements**: Keyword, Benefit ("Zero Errors"), Action ("How to").
            - **Examples**:
                 - Eliminate Picking Errors with {keyword}
                 - 3 Steps to Optimize Inventory using {keyword}
            """,
            
            "news": f"""
            {context_section}You are a Logistics News Commentator.
            Write a news analysis article that explains the impact of this topic on the industry.
            
            Keyword: {keyword}
            
            ## Target
            - Executives and managers wanting to stay ahead of trends.
            
            ## Structure
            1. **Lead**: Why this matters NOW.
            2. **The Facts**: 5W1H of the news/trend.
            3. **Industry Impact**: Effect on carriers, warehouses, shippers.
            4. **LogiShift View**: Unique insight/prediction (The "So What?").
            5. **Takeaway**: What companies should do next.
            
            ## Rules
            - **Insight**: Go beyond reporting. Add analysis.
            - **Professionalism**: Data-driven and objective.
            
            ## Format
            - Markdown
            - **Use Markdown Tables for summaries (NO HTML).**
            - Approx. 1000-1500 words.
            
            ## Title Rules
            - **Goal**: High Impact & CTR.
            - **Length**: STRICTLY under 60 characters.
            - **Elements**: Keyword, Insight/Impact.
            - **Examples**:
                - {keyword}: Impact on Global Supply Chains
                - Why {keyword} is Logistics' Next Big Thing
            """,
            
            "global": f"""
            {context_section}You are a Global Logistics Trend Watcher.
            Write an article introducing a global trend/case study to a global audience (US/EU/Asia focus).
            
            Keyword: {keyword}
            
            ## Target
            - Innovation leaders, Strategy executives.
            
            ## Structure
            1. **Why It Matters**: Global context.
            2. **Global Trend**: What is happening in US/China/Europe?
            3. **Case Study**: Specific company success story.
            4. **Key Takeaways**: Lessons for the logistics industry.
            5. **Future Outlook**.
            
            ## Rules
            - **Specificity**: Use real company names and data.
            - **Global Perspective**: Focus on cross-border, supply chain resilience, or sustainability.
            
            ## Format
            - Markdown
            - **Use Tables for comparisons (NO HTML).**
            - Approx. 1500-2000 words.
            
            ## Title Rules
            - **Goal**: Intrigue and Relevance.
            - **Length**: STRICTLY under 60 characters.
            - **Elements**: Keyword, Global Scale, Innovation.
            - **Examples**:
                - {keyword} Transforming EU Supply Chains
                - Future of {keyword}: Lessons from Amazon
            """,

            "weekly_summary": f"""
            {context_section}You are the Editor-in-Chief of LogiShift Global.
            Create a "Weekly Industry Summary" based on the provided articles. Provide deep insights, not just summaries.
            
            ## Target Period
            - Past 1 week
            
            ## Target Audience
            - C-SUITE, Supply Chain Directors looking for macro trends.
            
            ## Structure
            1. **The Weekly Macro View**:
               - Define the "Theme of the Week" (e.g., "AI moves from pilot to production").
               - Brief macro context.
            
            2. **Key Movements & Insights**:
               - Group news into 2-3 structural themes (H2).
               - **What**: The news event.
               - **Why/So What?**: Deep analysis of what this means for the industry.
               - **Links**: Embed links to source articles: `[Title](URL)`.
            
            3. **Strategic Outlook**:
               - What to watch next week?
               - Specific technologies, companies, or regulations to monitor.
            
            ## Rules
            - **Depth**: Connect the dots.
            - **Links**: Cite at least 10 articles if possible.
            - **Tone**: Sophisticated, Insightful, Professional.
            
            ## Format
            - Markdown.
            - Approx. 2000+ words.
            
            ## Title Rules
            - Format: Weekly LogiShift: [Date Range] | [Abstract Theme]
            - Example: Weekly LogiShift: Dec 13-20 | The Shift to Autonomous Supply Chains
            """
        }
        
        prompt = prompts.get(article_type, prompts["know"])
        
        if extra_instructions:
            prompt += f"\n\n{extra_instructions}\n"
        
        # Add common formatting instruction
        # Add common formatting instruction
        prompt += """
        
        ## Output Format
        Output MUST be in the following format:
        
        Line 1: # [Generated Title]
        Line 2: (Blank Line)
        Line 3+: Article body (Start with Introduction)
        
        **Heading Levels:**
        - Title: # (H1)
        - Main Section: ## (H2)
        - Subsection: ### (H3)
        - Detail: #### (H4)
        
        **Markdown Rules:**
        - **Lists:** MUST have a blank line before the list.
        - **Nested Lists:** MUST use 4 spaces for indentation.
        
        **Heading Rules:**
        - DO NOT use generic headings like "Benefits" or "Key Points" repeatedly in H3/H4.
        - OK: `#### Cost Reduction via Automated Estimation`
        - NG: `#### Specific Benefits`
        - Headings must be descriptive.
        
        Example:
        # What is WMS? The Complete Guide to Warehouse Management Systems
        
        For logistics managers, choosing the right WMS is...
        
        ## What is WMS?
        
        A Warehouse Management System (WMS) is...
        
        ### Key Features of WMS
        
        ...
        """
        
        try:
            response = self._retry_request(
                self.client.models.generate_content,
                model='gemini-3-pro-preview',
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            return None

    def generate_image(self, prompt, output_path, aspect_ratio="16:9"):
        """
        Generate an image using Gemini 2.5 Flash Image (Primary) or Imagen 3.0 (Fallback).
        """
        # 1. Try Gemini 2.5 Flash Image (API Key supported)
        try:
            print(f"Generating image with Gemini 2.5 Flash Image for prompt: {prompt}")
            
            # Use google-genai SDK (v1beta) for API Key support and aspect ratio control
            # We need a dedicated client for v1beta to ensure aspect_ratio works
            client_v1beta = genai.Client(api_key=self.api_key, vertexai=False, http_options={'api_version': 'v1beta'})
            
            response = client_v1beta.models.generate_content(
                model='gemini-2.5-flash-image',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(
                        aspect_ratio=aspect_ratio,
                    )
                )
            )
            
            # Extract image from response (Gemini 2.5 Flash)
            if response.parts:
                for part in response.parts:
                    # Check if part has inline_data (image)
                    if part.inline_data is not None:
                        image_bytes = part.inline_data.data
                        with open(output_path, 'wb') as f:
                            f.write(image_bytes)
                        print(f"Image saved to: {output_path}")
                        return output_path
            
            print("No image found in Gemini 2.5 response, trying fallback...")
            
        except Exception as e:
            print(f"Gemini 2.5 Flash Image failed ({e}), falling back to Imagen 3.0...")

        # 2. Fallback to Imagen 3.0 (Vertex AI only)
        try:
            print(f"Generating image with Imagen 3.0 (Fallback) for prompt: {prompt}")
            
            response = self._retry_request(
                self.client.models.generate_images,
                model='imagen-3.0-generate-001',
                prompt=prompt,
                config={
                    'aspect_ratio': aspect_ratio
                }
            )
            
            # Extract image from response (Imagen 3.0)
            if response.generated_images:
                image_bytes = response.generated_images[0].image.image_bytes
                with open(output_path, 'wb') as f:
                    f.write(image_bytes)
                print(f"Image saved to: {output_path}")
                return output_path
            
            print("No image generated in Imagen 3.0 response.")
            return None
                
        except Exception as e:
            print(f"Failed to generate image with Imagen 3.0: {e}")
            return None


    def generate_image_prompt(self, title, content_summary, article_type="know"):
        """
        Generate an optimized English image prompt based on article title and content.
        
        Args:
            title: Article title
            content_summary: Brief summary or first paragraph of the article
            article_type: Type of article (know, buy, do, news, global)
        
        Returns:
            English image prompt optimized for Imagen 3.0
        """
        prompt = f"""
        You are an expert at creating image generation prompts for Imagen 3.0.
        
        Based on the following article information, create a detailed English image prompt that:
        1. Captures the main theme and context of the article
        2. Is specific and descriptive (not abstract)
        3. Focuses on logistics/warehouse/supply chain context
        4. Is photorealistic and professional
        5. Avoids text, human faces, or complex diagrams
        
        Article Title: {title}
        Article Type: {article_type}
        Content Summary: {content_summary[:500]}
        
        Generate a single, detailed English image prompt (max 100 words) that would create a compelling hero image for this article.
        Output ONLY the prompt text, no explanations.
        """
        
        try:
            response = self._retry_request(
                self.client.models.generate_content,
                model='gemini-3-pro-preview',
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error generating image prompt: {e}")
            # Fallback to simple prompt
            return f"Professional logistics warehouse scene related to {title}, photorealistic, high quality, 4k"

    def classify_content(self, content):
        """
        Classify the article content into categories and tags.
        """
        prompt = f"""
        You are an expert content classifier for a logistics media site.
        Analyze the following article content and classify it.

        Content:
        {content[:3000]}... (truncated)

        Output JSON format:
        {{
            "category": "one of [warehouse-management, logistics-dx, material-handling, 2024-problem, cost-reduction, global-logistics]",
            "industry_tags": ["list", "of", "relevant", "industries", "e.g.", "manufacturing", "retail", "ecommerce", "3pl-warehouse", "transportation"],
            "theme_tags": ["list", "of", "relevant", "themes", "e.g.", "labor-shortage", "automation", "cost-reduction", "quality-improvement", "safety", "environment"]
        }}
        """
        
        try:
            response = self._retry_request(
                self.client.models.generate_content,
                model='gemini-3-pro-preview',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            import json
            return json.loads(response.text)
        except Exception as e:
            print(f"Classification failed: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_static_page(self, page_type, language="en"):
        """
        Generate static page content (privacy policy, about, contact).
        
        Args:
            page_type: "privacy", "about", or "contact"
            language: Deprecated, defaults to "en"
        
        Returns:
            Generated markdown content
        """
        prompts = {
            "privacy": """
            You are a legal content writer specializing in digital media.
            Create a Privacy Policy for "LogiShift Global" compliant with GDPR and international standards.

            【Site Info】
            - Site Name: LogiShift Global
            - Operator: LogiShift Editorial Team
            - Established: Nov 2025
            - Purpose: Global logistics insights, DX trends, and supply chain management.
            - Tech: Google Analytics, Cookies
            - Contact: info@logishift.net

            ## Required Sections
            1. Introduction (Commitment to privacy)
            2. Information We Collect (Cookies, Analytics, etc.)
            3. How We Use Your Information (Service improvement, Analysis)
            4. Third-Party Sharing (Google Analytics, etc.)
            5. Cookies & Tracking Technologies
            6. Your Rights (GDPR/CCPA compliance - Access, Correction, Deletion)
            7. Contact Information
            8. Effective Date

            ## Output Format
            - Markdown format
            - Use H2 (##) and H3 (###) for headings
            - Use bullet points and lists for readability
            - Professional, clear, and reassuring tone
            - End with "Effective Date: November 1, 2025"

            ## Notes
            - Clearly state user rights.
            - Provide contact email for privacy concerns.
            """,

            "about": """
            You are a corporate communications expert.
            Create an "About Us" page for LogiShift Global.

            【Site Info】
            - Site Name: LogiShift Global
            - Operator: LogiShift Editorial Team
            - Established: Nov 2025
            - Contact: info@logishift.net

            【Mission】
            To solve global logistics challenges (Cost, Labor, Efficiency) through digital transformation (DX) insights. We aim to be the #1 global source for logistics innovation.

            【Key Content】
            - Cost Reduction Strategies
            - Technology & DX (WMS, RFID, Robotics)
            - Supply Chain Management (SCM)
            - Global Case Studies

            【Target Audience】
            Logistics managers, Warehouse directors, Supply Chain Executives worldwide.

            ## Required Sections
            1. About LogiShift Global (Vision & Purpose)
            2. Operator Information (Table: Site Name, Operator, Established, Contact)
            3. Our Mission
            4. What We Cover (Content categories)
            5. Who It's For (Target audience)
            6. Contact Us

            ## Output Format
            - Markdown format
            - Use H2 (##) and H3 (###) for headings
            - Use a Markdown table for Operator Information
            - Tone: Professional, authoritative, yet innovative and accessible
            """,

            "contact": """
            You are a customer support specialist.
            Create a "Contact Us" page for LogiShift Global.

            【Site Info】
            - Site Name: LogiShift Global
            - Operator: LogiShift Editorial Team
            - Email: info@logishift.net
            - Hours: Mon-Fri 10:00-18:00 (JST)

            ## Required Sections
            1. Introduction (We'd love to hear from you)
            2. How to reach us (Email)
            3. Response Time (Typical response time)
            4. Guidelines (Inquiries about content, advertising, partnerships)

            ## Output Format
            - Markdown format
            - Use H2 (##) and H3 (###) for headings
            - Professional, friendly, and accessible tone

            ## Notes
            - Clearly display info@logishift.net
            - Link to Privacy Policy for data handling
            """
        }

        prompt = prompts.get(page_type)
        if not prompt:
            return None

        return self.generate_content(prompt, model='gemini-3-pro-preview')

    def generate_structured_summary(self, content):
        """
        Generate a structured JSON summary of the article for internal linking relevance.
        """
        prompt = f"""
        You are an expert content analyst. Analyze the following article and generate a structured summary in JSON format.
        This summary will be used by an AI system to identify relevant internal links.
        
        Article Content:
        {content[:4000]}... (truncated)

        Output JSON format (Strictly JSON only):
        {{
            "summary": "Detailed summary of the article content (300-500 chars). Mention specific methods, technologies, or case studies discussed.",
            "key_topics": ["list", "of", "specific", "sub-topics", "covered"],
            "entities": ["list", "of", "companies", "products", "or", "tools", "mentioned"]
        }}
        """
        
        try:
            response = self._retry_request(
                self.client.models.generate_content,
                model='gemini-3-pro-preview',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            import json
            return json.loads(response.text)
        except Exception as e:
            print(f"Structured summary generation failed: {e}")
            return None

    def generate_sns_content(self, title, content, article_type="know"):
        """
        Generate engaging SNS (Twitter/X) post content.
        Output is JSON: {"hook": "...", "summary": "...", "hashtags": ["#tag1", ...]}
        """
        # Truncate content for efficiency
        truncated_content = content[:3000]
        
        prompt = f"""
        You are an expert social media manager for a logistics media site "LogiShift Global".
        Create an engaging X (Twitter) post content based on the following article.
        
        Target Audience: Global Logistics professionals, warehouse managers, executives.
        Goal: Maximize CTR (Click Through Rate) and engagement. Use "FOMO" (Fear Of Missing Out) or "High Benefit" appeal.

        Article Title: {title}
        Article Type: {article_type}
        Content (excerpt):
        {truncated_content}

        Requirements:
        1. **Hook**: A strong, catchy opening line. Use a question, a shocking fact, or a counter-intuitive statement. 
           - MUST include 1 relevant emoji at the beginning or end.
           - Max 50 chars.
        2. **Summary**: A compelling teaser. Do NOT just summarize. Explain "Why this matters" or "What they will lose by not reading".
           - Focus on benefits.
           - Max 200 chars.
        3. **Hashtags**: 3-5 relevant English hashtags.
           - Use specific tags like #SupplyChain, #Logistics, #WarehouseAutomation, #Amazon.

        4. Language: English. 
        5. **Tone**: Professional but urgent/exciting.

        Output JSON format (Strictly JSON only):
        {{
            "hook": "😱 Is your WMS outdated?",
            "summary": "Don't get left behind. Discover 3 key strategies to modernize your warehouse operations today. #SupplyChain #Logistics",
            "hashtags": ["#LogiShift", "#SupplyChain", "#WMS"]
        }}
        """
        
        try:
            response = self._retry_request(
                self.client.models.generate_content,
                model='gemini-3-pro-preview',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            import json
            return json.loads(response.text)
        except Exception as e:
            print(f"SNS content generation failed: {e}")
            # Fallback
            return {
                "hook": f"【New Post】{title}",
                "summary": "Check out our latest logistics insights here!",
                "hashtags": ["#LogiShift", "#Logistics"]
            }

if __name__ == "__main__":
    # Test generation
    try:
        client = GeminiClient()
        print("GeminiClient initialized successfully.")
    except Exception as e:
        print(f"Initialization failed: {e}")
