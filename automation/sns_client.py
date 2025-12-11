import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

class SNSClient:
    def __init__(self):
        # X (Twitter) Credentials
        self.x_api_key = os.getenv("X_API_KEY")
        self.x_api_secret = os.getenv("X_API_SECRET")
        self.x_access_token = os.getenv("X_ACCESS_TOKEN")
        self.x_access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
        
        self.x_client = None
        self._authenticate_x()

    def _authenticate_x(self):
        """Authenticate with X API v2"""
        if self.x_api_key and self.x_api_secret and self.x_access_token and self.x_access_token_secret:
            try:
                self.x_client = tweepy.Client(
                    consumer_key=self.x_api_key,
                    consumer_secret=self.x_api_secret,
                    access_token=self.x_access_token,
                    access_token_secret=self.x_access_token_secret
                )
                print("Authenticated with X (Twitter) successfully.")
            except Exception as e:
                print(f"Failed to authenticate with X: {e}")
                self.x_client = None
        else:
            print("X credentials missing in .env. Skipping X authentication.")

    def post_to_x(self, content):
        """
        Post text content to X.
        
        Args:
            content (str): The text to post.
            
        Returns:
            dict: Response data or None if failed.
        """
        if not self.x_client:
            print("X client not initialized.")
            return None
            
        try:
            response = self.x_client.create_tweet(text=content)
            print(f"Posted to X successfully. ID: {response.data['id']}")
            return response.data
        except Exception as e:
            print(f"Failed to post to X: {e}")
            return None

if __name__ == "__main__":
    # Test
    client = SNSClient()
    if client.x_client:
        print("Ready to post (dry run test passed).")
