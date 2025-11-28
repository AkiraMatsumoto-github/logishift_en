import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION")
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.use_vertex = False

        if self.api_key:
            print("Initializing Gemini with API Key")
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        elif self.project_id and self.location:
            print(f"Initializing Gemini with Vertex AI (Project: {self.project_id}, Location: {self.location})")
            try:
                import vertexai
                from vertexai.generative_models import GenerativeModel
                vertexai.init(project=self.project_id, location=self.location)
                self.model = GenerativeModel("gemini-1.5-flash-001")
                self.use_vertex = True
            except ImportError:
                print("Error: google-cloud-aiplatform not installed or vertexai import failed.")
                raise
        else:
            raise ValueError("Missing Gemini credentials. Set GEMINI_API_KEY or GOOGLE_CLOUD_PROJECT/LOCATION in .env")

    def generate_article(self, keyword, article_type="know"):
        """
        Generate an article based on the keyword and content type.
        
        Args:
            keyword: Target keyword
            article_type: 'know' (default), 'buy', 'do', 'news', 'global'
        """
        
        prompts = {
            "know": f"""
            あなたは物流業界のDXエバンジェリストです。以下のキーワードについて、基礎から分かりやすく解説する記事を執筆してください。
            
            キーワード: {keyword}
            
            ## ターゲット
            - 物流担当者、倉庫管理者（基礎知識を求めている）
            
            ## 構成案
            1. **導入**: 読者の課題に共感し、なぜこのキーワードが重要なのかを提示
            2. **基礎知識**: {keyword}とは何か？定義や仕組みを解説
            3. **メリット・重要性**: 導入することで何が変わるのか
            4. **注意点・課題**: 導入や運用の際のハードル
            5. **まとめ**: 次のアクション
            
            ## フォーマット
            - Markdown形式（H2, H3を使用）
            - 2000文字程度
            - 専門用語は噛み砕いて解説
            - タイトル: [魅力的な記事タイトル]
            """,
            
            "buy": f"""
            あなたは物流業界のDXエバンジェリストです。以下のキーワードに関連するツールの選び方や比較記事を執筆してください。
            
            キーワード: {keyword}
            
            ## ターゲット
            - ツール導入を検討している経営層、IT担当者
            
            ## 構成案
            1. **導入**: ツール選定の難しさと重要性
            2. **比較のポイント**: 選ぶ際に重視すべき基準（機能、コスト、サポートなど）
            3. **主要なタイプ/製品**: 市場にある主なソリューションの種類と特徴
            4. **メリット・デメリット**: それぞれのタイプの長所と短所
            5. **おすすめの選び方**: 自社に合ったツールの見つけ方
            
            ## フォーマット
            - Markdown形式
            - 比較表を作成すること（Markdownテーブル）
            - 2500文字程度
            - タイトル: [比較・選定ガイドのタイトル]
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
            - 2000文字程度
            - タイトル: [事例・ノウハウ記事タイトル]
            """,
            
            "news": f"""
            あなたは物流業界のニュースコメンテーターです。以下のキーワードに関する最新トレンドやニュース解説記事を執筆してください。
            
            キーワード: {keyword}
            
            ## ターゲット
            - 業界動向をキャッチアップしたい全層
            
            ## 構成案
            1. **ニュース概要**: 今、何が起きているのか（背景）
            2. **業界への影響**: 物流業界にどのようなインパクトがあるか
            3. **LogiShiftの視点**: 独自の考察、今後の予測
            4. **まとめ**: 企業はどう備えるべきか
            
            ## フォーマット
            - Markdown形式
            - 速報性を意識した簡潔な文体
            - 1500文字程度
            - タイトル: [ニュース解説タイトル]
            """,
            
            "global": f"""
            あなたは物流業界の海外トレンドウォッチャーです。以下のキーワードに関連する海外の最新事例やトレンドを紹介する記事を執筆してください。
            
            キーワード: {keyword}
            
            ## ターゲット
            - イノベーションを求める経営層、新規事業担当者
            
            ## 構成案
            1. **海外の動向**: 米国・中国・欧州などで何が起きているか
            2. **先進事例**: 具体的な企業やスタートアップの取り組み
            3. **日本への示唆**: 日本の物流企業はこれをどう捉え、どう活かすべきか
            4. **まとめ**: 将来の展望
            
            ## フォーマット
            - Markdown形式
            - 日本未上陸の概念や技術を分かりやすく
            - 2000文字程度
            - タイトル: [海外トレンド記事タイトル]
            """
        }
        
        prompt = prompts.get(article_type, prompts["know"])
        
        # Add common formatting instruction
        prompt += """
        
        [記事本文]
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            return None

if __name__ == "__main__":
    # Test generation
    try:
        client = GeminiClient()
        print("GeminiClient initialized successfully.")
    except Exception as e:
        print(f"Initialization failed: {e}")
