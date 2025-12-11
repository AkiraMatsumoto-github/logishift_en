# -*- coding: utf-8 -*-
import os
import base64
from google import genai
from google.genai import types
from dotenv import load_dotenv
import time
import random

load_dotenv()

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
            {context_section}あなたは物流業界の専門家（SEOコンテンツライター）です。
            以下のキーワードについて、読者の検索意図（インサイト）を深く満たす解説記事を執筆してください。
            
            キーワード: {keyword}
            
            ## ターゲット
            - 物流業界の初心者〜中級者
            - 業務効率化やコスト削減に課題を持つ現場リーダー、経営層
            
            ## 構成案
            1. **導入**:
               - 【共感】読者が抱える具体的な悩み（例: 「残業が減らない」「誤出荷が多い」）を提示
               - 【解決】この記事を読むことでどう解決するかを明示
            2. **基礎知識**: {keyword}とは何か？（図解を意識した分かりやすい説明）
            3. **なぜ今重要なのか**: 2024年問題やDXの潮流など、業界背景と絡めて解説
            4. **メリット・効果**: 導入/実施による具体的な変化（定量・定性）
            5. **実践/導入のポイント**: 失敗しないための注意点やステップ
            6. **まとめ**: 次のアクション（社内検討、資料収集など）
            
            ## 執筆ルール（SEO・品質）
            - **共起語・関連語**: {keyword}に関連する専門用語や業界用語を自然に文中に盛り込むこと。
            - **信頼性**: 可能であれば公的なデータ（国交省、業界団体など）や一般的な統計値に言及し、信頼性を高めること（架空のデータは禁止）。
            - **可読性**:
                - 一文は60文字以内を目安に短くする。
                - 3行以上の長文は避け、適宜改行を入れる。
                - 詳細な説明は箇条書きを活用する。
            
            ## フォーマット
            - Markdown形式（適切な階層構造を使用）
            - 3500文字程度
            - **複雑な情報はMarkdownテーブルで整理する（スマホ表示崩れ防止のため、列数は最大3列、セル内は簡潔に）**
            - **【厳守】テーブル内ではHTMLタグ禁止。改行は句読点で対応。**
            
            ## タイトル生成ルール
            - **文字数**: 32文字前後（最大40文字以内）
            - **キーワード配置**: ターゲットキーワード「{keyword}」を可能な限り冒頭に配置
            - **独自性**: 数字、ターゲット層の明示、ベネフィットを含める
            - **具体性**: 「徹底解説」だけでなく、「5つの手順」「3つの選び方」など具体的な数字を入れる。
            - **ターゲット明示**: 「中小企業向け」「担当者必見」など、誰のための記事かをカッコ書きなどで入れる。
            - **パワーワード**: 【徹底解説】【完全版】【図解あり】などを適宜使用
            
            ## タイトルテンプレート（以下のいずれかの形式で生成）
            1. {keyword}とは？[メリット/仕組み]と[導入手順]を[ターゲット]向けに解説
            2. 【徹底解説】{keyword}の基礎知識と導入メリット
            3. {keyword}を[ターゲット]向けに分かりやすく解説
            
            例: WMS（倉庫管理システム）とは？導入メリットと選び方を物流担当者向けに徹底解説
            ## 注意点
            - 信頼感を与えるため自分から物流エバンジェリストですと名乗らないこと
            - **HTMLタグ（<br>, <p>, <div>など）は絶対に使用しないこと** 
            """,
            
            "buy": f"""
            あなたは物流業界のDXコンサルタントです。
            以下のキーワードに関連するソリューションの「失敗しない選び方」と比較記事を執筆してください。
            
            キーワード: {keyword}
            
            ## ターゲット
            - システム導入や機器購入を検討中の決裁者、担当者
            
            ## 構成案
            1. **導入**: 選定の難しさに寄り添い、間違った選び方をした際のリスクを提示
            2. **比較・選定の重要ポイント**: 
               - 「価格」だけでなく「サポート体制」「拡張性」「現場の使いやすさ」など、プロ視点の選定軸を3〜4つ提示
            3. **主要なタイプ分類**: 市場にある製品をタイプ別（例: クラウド型vsオンプレ型、大企業向vs中小向）に分類して解説
            4. **メリット・デメリット比較**: それぞれのタイプの長所と短所を公平に比較
            5. **自社に合った選び方**: 会社の規模や課題別のおすすめパターン
            
            ## 執筆ルール
            - **比較表の質**: 単なる機能の有無だけでなく、「どんな企業に向いているか」が一目で分かるようにする。
            - **中立性**: 特定の製品を過度に持ち上げず、デメリットも正直に伝えることで記事の信頼性を担保する。
            
            ## フォーマット
            - Markdown形式
            - 比較表（Markdownテーブル）必須
            - **各製品の比較やメリット・デメリットは必ずテーブルで整理する**
            - **テーブル作成時の注意: モバイルでの閲覧を考慮し、説明文は極力短く体言止め等を使用する。**
            - **【重要】Markdownテーブル内では<br>タグや他のHTMLタグを一切使用禁止。改行が必要な場合は、セル内で自然な文章として記述する**
            - 3500文字程度
            
            ## タイトル生成ルール
            - **文字数**: 32文字前後（最大40文字以内）
            - **キーワード配置**: ターゲットキーワード「{keyword}」を可能な限り冒頭に配置
            - **独自性**: 数字、比較軸、ターゲット層を含める
            - **具体性**: 「徹底解説」だけでなく、「5つの手順」「3つの選び方」など具体的な数字を入れる。
            - **ターゲット明示**: 「中小企業向け」「担当者必見」など、誰のための記事かをカッコ書きなどで入れる。
            - **パワーワード**: 【最新】【完全版】【徹底比較】などを適宜使用
            
            ## タイトルテンプレート（以下のいずれかの形式で生成）
            1. 【2024年最新】{keyword}おすすめ[数字]選！[比較軸]で徹底比較
            2. {keyword}の選び方完全ガイド｜[ターゲット]必見
            3. 失敗しない{keyword}選び｜[比較軸]を徹底解説
            
            例: 【2024年最新】クラウド型WMSおすすめ10選！価格・機能を徹底比較
            
            ## 注意点
            - 信頼感を与えるため自分から物流エバンジェリストですと名乗らないこと
            - **HTMLタグ（<br>, <p>, <div>など）は絶対に使用しないこと** 
            """,
            
            "do": f"""
            あなたは物流業界のDXエバンジェリストです。以下のキーワードに関連する具体的な事例やノウハウ記事を執筆してください。
            
            キーワード: {keyword}
            
            ## ターゲット
            - 現場改善を目指す倉庫管理者、実務担当者
            
            ## 構成案
            1. **導入**: よくある現場の悩み（Before）
            2. **解決策の提示**: {keyword}を活用した具体的な手法（What）
            3. **実践プロセス**: どのように導入・実践するか（How）
            4. **期待される効果**: 導入後の変化（After、定量・定性）
            5. **まとめ**: 成功の秘訣
            
            ## フォーマット
            - Markdown形式
            - 具体的な数字やステップを含める
            - **手順やBefore/Afterの比較はMarkdownテーブルを使用する**
            - **Markdownテーブル内ではHTMLタグ（<br>など）を絶対に使用せず、シンプルなテキストのみを使用する**
            - 3500文字程度
            
            ## タイトル生成ルール
            - **文字数**: 32文字前後（最大40文字以内）
            - **キーワード配置**: ターゲットキーワード「{keyword}」を可能な限り冒頭に配置
            - **独自性**: 課題、ベネフィット、数字を含める
            - **パワーワード**: 【事例あり】【実践ガイド】などを適宜使用
            
            ## タイトルテンプレート（以下のいずれかの形式で生成）
            1. [悩み]を解決！{keyword}を活用した[解決策]とは？【事例あり】
            2. {keyword}で[ベネフィット]を実現する方法
            3. [課題]を[数字]削減！{keyword}活用事例
            
            例: 倉庫のピッキングミスをゼロに！バーコード管理を活用した誤出荷防止策【事例あり】
            
            ## 注意点   
            - 信頼感を与えるため自分から物流エバンジェリストですと名乗らないこと
            """,
            
            "news": f"""
            {context_section}あなたは物流業界のニュースコメンテーターであり、SEOコンテンツライターです。
            以下のキーワードに関するニュースやトレンドを、読者（物流関係者）の関心に強く訴求するように解説してください。
            
            キーワード: {keyword}
            
            ## ターゲット
            - 業界動向をキャッチアップしたい経営層、現場リーダー
            
            ## 構成案
            1. **導入**: 
               - 【速報・インパクト】「今なぜ話題なのか」「業界にどんな衝撃があるか」を冒頭で端的に伝える（LEAD文）
            2. **ニュースの背景・詳細**: 
               - 事実関係を整理（5W1H）
            3. **業界への具体的な影響**: 
               - 運送、倉庫、メーカーなど、各プレイヤーへの影響
            4. **LogiShiftの視点（独自考察）**: 
               - 単なる事実の羅列ではなく、「今後どうなるか」「企業はどう動くべきか」の予測と提言
            5. **まとめ**: 明日から意識すべきこと
            
            ## 執筆ルール
            - **独自性**: 一般的なニュースサイトと差別化するため、「LogiShiftの視点」セクションでは独自の考察や予測を必ず入れること。
            - **SEO**: トレンドキーワードに関連する複合語を自然に盛り込む。
            - **信頼性**: 公式発表やデータがある場合は積極的に引用する。
            
            ## フォーマット
            - Markdown形式
            - **要点や時系列はMarkdownテーブルを使用して整理する（スマホで見やすいよう列数を絞る）**
            - **【厳守】テーブル内ではHTMLタグ禁止。改行は句読点で対応。**
            - 2500〜3000文字程度
            
            ## タイトル生成ルール
            - **文字数**: 32文字前後（最大40文字以内）
            - **キーワード配置**: ターゲットキーワード「{keyword}」を可能な限り冒頭に配置
            - **速報性・煽り**: 【緊急】【徹底解説】【物流への衝撃】など、クリックしたくなるワードを使用
            - **具体性**: 「3つの影響」「〇〇業界必見」など
            
            ## タイトルテンプレート（以下のいずれかの形式で生成）
            1. {keyword}｜物流業界への影響を徹底解説[企業はどう動く？]
            2. 【徹底解説】{keyword}が物流を変える？最新トレンド分析
            3. 注目の{keyword}｜[業界/属性]が今知るべきことまとめ
            
            例: 物流2024年問題｜運送企業の倒産リスクと生き残り戦略を徹底解説
            ## 注意点
            - 信頼感を与えるため自分から物流エバンジェリストですと名乗らないこと
            """,
            
            "global": f"""
            {context_section}あなたは物流業界の海外トレンドウォッチャー（SEOライター）です。
            以下のキーワードに関連する海外の最新事例やトレンドを、日本の物流企業が参考にできる形で解説してください。
            
            キーワード: {keyword}
            
            ## ターゲット
            - イノベーションを求める経営層、新規事業担当者
            - 海外の先進事例からヒントを得たいDX推進担当者
            
            ## 構成案
            1. **導入**: 
               - 【Why Japan?】なぜ今、日本企業がこの海外トレンドを知る必要があるのかを提示
            2. **海外の最新動向**: 米国・中国・欧州などで何が起きているか（具体的な市場データなど）
            3. **先進事例（ケーススタディ）**: 
               - 特定の企業やプロジェクトを取り上げ、成功要因を深掘り
            4. **日本への示唆**: 
               - 海外の事例を日本国内に適用する場合のポイントや障壁
               - 日本企業が今すぐ真似できること
            5. **まとめ**: 将来の展望
            
            ## 執筆ルール
            - **具体性**: 国名、企業名、具体的な数字（ドル/元など）を出してリアリティを持たせる。
            - **日本ローカライズ**: 単なる翻訳記事にせず、「日本だとどうなるか」という視点を必ず入れる（例: 「日本の商習慣とは異なるが...」）。
            - **SEO**: 「海外物流」「物流DX 事例」などのキーワードで検索されることを意識。
            
            ## フォーマット
            - Markdown形式
            - **国別の比較や事例の一覧はMarkdownテーブルを使用する（スマホ最適化: 列数を絞る）**
            - **【厳守】テーブル内ではHTMLタグ禁止。改行は句読点で対応。**
            - 3500文字程度
            
            ## タイトル生成ルール
            - **文字数**: 32文字前後（最大40文字以内）
            - **キーワード配置**: ターゲットキーワード「{keyword}」を可能な限り冒頭に配置
            - **独自性**: 「日本未上陸」「XXで話題」など、先進性を強調
            - **ベネフィット**: 日本企業にとっての学びがあることを示唆
            
            ## タイトルテンプレート（以下のいずれかの形式で生成）
            1. 【海外事例】{keyword}に学ぶ！[国名]の最新動向と日本への示唆
            2. {keyword}の最前線｜米国・中国の成功事例を徹底分析
            3. 日本未上陸の{keyword}とは？海外トレンドから学ぶ物流の未来
            
            例: 【海外事例】倉庫自動化ロボット｜米国の最新動向と日本への示唆
            ## 注意点
            - 信頼感を与えるため自分から物流エバンジェリストですと名乗らないこと
            """
        }
        
        prompt = prompts.get(article_type, prompts["know"])
        
        if extra_instructions:
            prompt += f"\n\n{extra_instructions}\n"
        
        # Add common formatting instruction
        prompt += """
        
        ## 出力形式
        必ず以下の形式で出力してください：
        
        1行目: # [生成したタイトル]
        2行目: 空行
        3行目以降: 記事本文（導入から始める）
        
        **見出しレベル:**
        - タイトル: # (H1) ← 記事の主題
        - 大見出し: ## (H2) ← 記事の主要な構成要素（章）
        - 中見出し: ### (H3) ← 章を構成する具体的なトピック（節）
        - 小見出し: #### (H4) ← トピックの詳細。情報の粒度を細かくし、可読性を高めるために活用する。
        
        **【重要】Markdown記述ルール:**
        - **リスト（箇条書き）の前には必ず空行を入れること。** 空行がないと正しくリストとして認識されないため厳守する。
        - **ネスト（入れ子）したリストのインデントは必ず半角スペース4つ（4 spaces）を使用すること。** 2スペースでは構造が崩れる場合がある。
        
        **【重要】見出しの禁止事項:**
        - **「具体的な効果」「メリット」「ポイント」といった汎用的な単語だけの見出しを、H3やH4で繰り返し使用することを禁止する。**
        - OK例: `#### 自動見積もりによるコスト削減`
        - NG例: `#### 具体的な効果`
        - 目次を見ただけで内容が伝わる具体的な見出しにすること。
        
        例:
        # WMS（倉庫管理システム）とは？導入メリットと選び方を物流担当者向けに徹底解説
        
        物流倉庫の現場で働く担当者や倉庫管理者の皆様なら...
        
        ## WMSとは何か？
        
        倉庫管理システム（WMS）は...
        
        ### WMSの主な機能
        
        ...
        """
        
        try:
            response = self._retry_request(
                self.client.models.generate_content,
                model='gemini-2.5-pro',
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
                model='gemini-2.5-pro',
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
                model='gemini-2.5-pro',
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

    def generate_static_page(self, page_type):
        """
        Generate static page content (privacy policy, about, contact).
        
        Args:
            page_type: "privacy", "about", or "contact"
        
        Returns:
            Generated markdown content
        """
        prompts = {
            "privacy": """
            あなたは法務に詳しいコンテンツライターです。
            以下の情報を基に、日本の個人情報保護法に準拠したプライバシーポリシーを作成してください。
            
            【サイト情報】
            - サイト名: LogiShift（ロジシフト）
            - 運営者: LogiShift編集部
            - 設立: 2025年11月
            - 目的: 物流業界のDX推進・課題解決に関する情報提供
            - 使用技術: Googleアナリティクス、Cookie
            - お問い合わせ: info@logishift.jp
            
            ## 含めるべき項目
            1. 個人情報の取り扱いについて
            2. 収集する情報の種類（アクセスログ、Cookie等）
            3. 利用目的（サイト改善、統計分析等）
            4. 第三者提供（Googleアナリティクス等）
            5. Cookie・アクセス解析ツールについて
            6. 個人情報の開示・訂正・削除について
            7. お問い合わせ先
            8. 制定日・改定日
            
            ## 出力形式
            - Markdown形式で出力
            - 見出しはH2（##）とH3（###）を使用
            - 箇条書きや表を適宜使用
            - 法的に正確で、かつ読みやすい文章
            - 最後に「制定日: 2025年11月1日」を記載
            
            ## 注意点
            - 専門用語は分かりやすく説明
            - ユーザーの権利を明確に記載
            - 連絡先を明記
            """,
            
            "about": """
            あなたはコーポレートコミュニケーションの専門家です。
            以下の情報を基に、LogiShiftの運営者情報ページを作成してください。
            
            【サイト情報】
            - サイト名: LogiShift（ロジシフト）
            - 運営者: LogiShift編集部
            - 設立: 2025年11月
            - お問い合わせ: info@logishift.jp
            
            【ミッション】
            物流業界の課題解決とDX推進に貢献し、業界No.1のSEOメディアを目指す
            
            【主なコンテンツ】
            - 物流コスト削減のノウハウ
            - 最新テクノロジー（WMS, RFID, マテハンなど）の解説
            - 2024年問題などの業界トレンド解説
            - 物流DXの成功事例紹介
            
            【ターゲット読者】
            企業の物流担当者、倉庫管理者、経営層
            
            ## 含めるべき項目
            1. LogiShiftについて（サイトの目的・ビジョン）
            2. 基本情報（サイト名、運営者、設立年、お問い合わせ先）をテーブル形式で
            3. ミッション・ビジョン
            4. 主なコンテンツカテゴリの紹介
            5. 想定読者
            6. お問い合わせ先
            
            ## 出力形式
            - Markdown形式で出力
            - 見出しはH2（##）とH3（###）を使用
            - 基本情報はMarkdownテーブルで整理
            - 親しみやすく、信頼感のある文章
            - 物流業界への熱意が伝わる内容
            """,
            
            "contact": """
            あなたはカスタマーサポートの専門家です。
            以下の情報を基に、LogiShiftのお問い合わせページを作成してください。
            
            【サイト情報】
            - サイト名: LogiShift（ロジシフト）
            - 運営者: LogiShift編集部
            - お問い合わせ: info@logishift.jp
            - 対応時間: 平日 10:00-18:00（土日祝日を除く）
            
            ## 含めるべき項目
            1. お問い合わせについて（導入文）
            2. お問い合わせ方法（メールアドレス）
            3. 対応時間
            4. お問い合わせ内容の例（記事の内容、広告掲載、取材依頼など）
            5. 返信までの目安時間
            6. 注意事項（個人情報の取り扱い、営業目的の問い合わせなど）
            
            ## 出力形式
            - Markdown形式で出力
            - 見出しはH2（##）とH3（###）を使用
            - 箇条書きを適宜使用
            - 丁寧で分かりやすい文章
            - お問い合わせしやすい雰囲気
            
            ## 注意点
            - メールアドレスは必ず記載
            - 対応時間を明記
            - プライバシーポリシーへのリンクを案内（「詳しくは[プライバシーポリシー](/privacy-policy/)をご覧ください」）
            """
        }
        
        prompt = prompts.get(page_type)
        if not prompt:
            raise ValueError(f"Invalid page_type: {page_type}. Must be 'privacy', 'about', or 'contact'")
        
        try:
            response = self._retry_request(
                self.client.models.generate_content,
                model='gemini-2.5-pro',
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Error generating static page: {e}")
            return None


    def generate_structured_summary(self, content):
        """
        Generate a structured JSON summary of the article for internal linking relevance.
        """
        prompt = f"""
        You are an expert content analyst. Analyze the following article and generate a structured summary in JSON format.
        This summary will be used by an AI system to identify relevant internal links.
        IMPORTANT: The content is Japanese, so the 'summary' and 'key_topics' MUST be written in Japanese.

        Article Content:
        {content[:4000]}... (truncated)

        Output JSON format (Strictly JSON only):
        {{
            "summary": "Detailed summary of the article content (300-500 chars) in Japanese. Mention specific methods, technologies, or case studies discussed.",
            "key_topics": ["list", "of", "specific", "sub-topics", "covered", "(in Japanese)"],
            "entities": ["list", "of", "companies", "products", "or", "tools", "mentioned", "(preserve original names)"]
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
        You are an expert social media manager for a logistics media site "LogiShift".
        Create an engaging X (Twitter) post content based on the following article.
        
        Target Audience: Logistics professionals, warehouse managers, executives.
        Goal: Maximize CTR (Click Through Rate) and engagement. Use "FOMO" (Fear Of Missing Out) or "High Benefit" appeal.

        Article Title: {title}
        Article Type: {article_type}
        Content (excerpt):
        {truncated_content}

        Requirements:
        1. **Hook**: A strong, catchy opening line. Use a question, a shocking fact, or a counter-intuitive statement. 
           - MUST include 1 relevant emoji at the beginning or end.
           - Max 50 chars.
        2. **Summary**: A compelling teaser. Do NOT just summarize("〜について解説"). Explain "Why this matters" or "What they will lose by not reading".
           - Focus on benefits (cost down, efficiency up, risk avoidance).
           - Max 100 chars.
        3. **Hashtags**: 3-5 relevant hashtags. Always include #LogiShift and #物流DX.
        4. Language: Japanese. 
        5. **Tone**: Professional but urgent/exciting. Avoid robotic or purely descriptive tone.

        Output JSON format (Strictly JSON only):
        {{
            "hook": "😱 2024年問題、実はまだ間に合う？",
            "summary": "「もう手遅れ」と諦めるのは早い。現場がすぐ取り組める3つの即効策を公開。知らないと損する物流DXの最前線とは？",
            "hashtags": ["#LogiShift", "#物流DX", "#2024年問題", "#業務改善"]
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
                "hook": f"【新着記事】{title}",
                "summary": "最新の物流トレンドを解説しました。詳細はこちらをチェック！",
                "hashtags": ["#LogiShift", "#物流"]
            }

if __name__ == "__main__":
    # Test generation
    try:
        client = GeminiClient()
        print("GeminiClient initialized successfully.")
    except Exception as e:
        print(f"Initialization failed: {e}")
