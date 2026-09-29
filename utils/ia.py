# utils/ia.py - Conexión con IA usando modelos chinos gratuitos en OpenRouter

import os
import requests
from dotenv import load_dotenv
from utils.modelos import MODELOS_CHINOS

load_dotenv()

class IA:
    def __init__(self, modelo_key="ox_alpha"):
        """
        Inicializa la IA con un modelo chino gratuito.
        Por defecto usa Ox Alpha (el mejor).
        """
        # 🔑 La clave se lee desde variables de entorno
        self.api_key = os.getenv('OPENROUTER_API_KEY', '')
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # 📌 Seleccionar modelo de la lista de modelos chinos
        self.modelo_key = modelo_key
        self.modelo_config = MODELOS_CHINOS.get(modelo_key)
        
        if self.modelo_config:
            self.modelo = self.modelo_config["identificador"]
            self.modelo_nombre = self.modelo_config["nombre"]
        else:
            # Fallback: usar Ox Alpha por defecto
            self.modelo = "stealth/ox-alpha"
            self.modelo_nombre = "Ox Alpha (GLM-5.3-Flash)"
        
    def cambiar_modelo(self, modelo_key):
        """Cambiar el modelo usado por la IA"""
        if modelo_key in MODELOS_CHINOS:
            self.modelo_key = modelo_key
            self.modelo_config = MODELOS_CHINOS[modelo_key]
            self.modelo = self.modelo_config["identificador"]
            self.modelo_nombre = self.modelo_config["nombre"]
            return f"✅ Modelo cambiado a: {self.modelo_nombre}"
        else:
            return f"❌ Modelo '{modelo_key}' no encontrado"
    
    def chat(self, mensaje, sistema="Eres un asistente útil y profesional."):
        """Envía un mensaje y obtiene respuesta usando OpenRouter."""
        
        if not self.api_key:
            return "⚠️ No hay API Key configurada en las variables de entorno."
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.modelo,
                "messages": [
                    {"role": "system", "content": sistema},
                    {"role": "user", "content": mensaje}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            response = requests.post(self.api_url, headers=headers, json=data, timeout=120)
            
            if response.status_code == 200:
                resultado = response.json()
                return resultado['choices'][0]['message']['content']
            else:
                return f"⚠️ Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"⚠️ Error de conexión: {str(e)}"

# Instancia global
ia = IA()