
import os
import sys
# Add current directory to path so we can import automation.gemini_client
sys.path.append(os.getcwd())

from automation.gemini_client import GeminiClient

def test_sns_generation():
    client = GeminiClient()
    
    title = "自動倉庫システム(AS/RS)の最新トレンドとDaifukuの戦略"
    content = """
    物流業界では自動化が進んでおり、特に自動倉庫システム(AS/RS)の導入が加速しています。
    市場を牽引するのは日本のDaifuku（ダイフク）です。彼らの最新モデルは、従来比で20%の省エネを実現しました。
    また、AutoStore（オートストア）も高密度保管ソリューションとして注目を集めています。
    一方で、トヨタL&Fも自律搬送ロボットとの連携を強化しています。
    これらの技術は、2024年問題の解決策として期待されています。
    """
    
    print("Testing SNS generation...")
    result = client.generate_sns_content(title, content, article_type="know")
    
    print("\nResult:")
    print(result)
    
    if result and "hashtags" in result:
        print("\nHashtags:", result["hashtags"])
        
        # Check if proper nouns are included
        proper_nouns = ["Daifuku", "ダイフク", "AutoStore", "オートストア", "Toyota", "トヨタ"]
        found = any(any(noun.lower() in tag.lower() for noun in proper_nouns) for tag in result["hashtags"])
        
        if found:
             print("\nSUCCESS: Proper nouns found in hashtags.")
        else:
             print("\nWARNING: No expected proper nouns found in hashtags. Check prompt behavior.")

if __name__ == "__main__":
    test_sns_generation()
