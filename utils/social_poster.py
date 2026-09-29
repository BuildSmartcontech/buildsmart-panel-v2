# utils/social_poster.py - Publicación en redes sociales

import requests
import os
from dotenv import load_dotenv

load_dotenv()

class SocialPoster:
    def __init__(self):
        self.twitter_api_key = os.getenv('TWITTER_API_KEY', '')
        self.twitter_api_secret = os.getenv('TWITTER_API_SECRET', '')
        self.twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN', '')
        self.twitter_access_secret = os.getenv('TWITTER_ACCESS_SECRET', '')
    
    def publicar_twitter(self, mensaje):
        """Publicar en Twitter"""
        if not all([self.twitter_api_key, self.twitter_api_secret, 
                   self.twitter_access_token, self.twitter_access_secret]):
            return "❌ Configura las credenciales de Twitter en .env"
        
        try:
            # Twitter API v2
            url = "https://api.twitter.com/2/tweets"
            headers = {
                "Authorization": f"Bearer {self.twitter_access_token}",
                "Content-Type": "application/json"
            }
            data = {"text": mensaje[:280]}  # Límite de Twitter
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 201:
                return "✅ Publicado en Twitter"
            else:
                return f"❌ Error: {response.status_code}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def publicar_linkedin(self, mensaje):
        """Publicar en LinkedIn"""
        # LinkedIn API (requiere configuración adicional)
        return "📝 LinkedIn: Pendiente de configuración"

social_poster = SocialPoster()