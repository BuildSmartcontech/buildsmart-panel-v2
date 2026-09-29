# utils/config.py - Configuración centralizada para la nube

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración centralizada de la aplicación"""
    
    # ========== BASE DE DATOS ==========
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'postgres')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'mi_password')
    
    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # ========== IA ==========
    OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.1:8b')
    
    # ========== EMAIL ==========
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    EMAIL_USER = os.getenv('EMAIL_USER', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    
    # ========== REDES SOCIALES ==========
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY', '')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET', '')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', '')
    TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET', '')
    
    # ========== MODO ==========
    MODO_AUTOMATICO = os.getenv('MODO_AUTOMATICO', 'True').lower() == 'true'
    MODO_DIOS = os.getenv('MODO_DIOS', 'True').lower() == 'true'
    
    # ========== ENTORNO ==========
    ENTORNO = os.getenv('ENTORNO', 'desarrollo')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    @property
    def is_production(self):
        return self.ENTORNO == 'produccion'

config = Config()