# backend/gateway.py - VERSION 8.4 (GEMINI VISION)
# ============================================
# MEJORAS v8.4:
# - Nueva funcion analizar_imagen_gemini para ver fotos (Multimodal).
# ============================================

import os
import requests
import time
import base64
from dotenv import load_dotenv
from typing import Tuple, Optional, List

load_dotenv()

MODELOS_OPENROUTER = [
    "nvidia/nemotron-3-super-120b-a12b:free",
    "deepseek/deepseek-chat-v3.1:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "qwen/qwen-2.5-72b-instruct:free",
]

MODELOS_GROQ = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
]

MODELOS_GEMINI = [
    "gemini-1.5-flash",          # Excelente para Vision
    "gemini-2.0-flash-exp",
]

TIMEOUT_API = 300

# ... (Las funciones chat_openrouter, chat_groq_directo, chat_ollama se mantienen igual que en la V8.3)

def chat_gemini_directo(mensaje: str, sistema: str, temperature: float = 0.7) -> Optional[str]:
    # ... (Se mantiene igual)
    pass

def analizar_imagen_gemini(base64_data: str, prompt_texto: str) -> str:
    """
    Analiza una imagen en Base64 usando Gemini Vision.
    Retorna una descripcion de la imagen.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: return "Imagen subida por el usuario"

    # Limpiamos el prefijo si viene como data:image/jpeg;base64,...
    if "," in base64_data:
        base64_data = base64_data.split(",")[1]

    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}'
    
    payload = {
        'contents': [
            {
                'role': 'user',
                'parts': [
                    {'text': prompt_texto},
                    {
                        'inline_data': {
                            'mime_type': 'image/jpeg', # Asumimos JPEG o PNG
                            'data': base64_data
                        }
                    }
                ]
            }
        ],
        'generationConfig': {'temperature': 0.2, 'maxOutputTokens': 100}
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
        return "Imagen del negocio del usuario"
    except Exception as e:
        print(f"[VISION ERROR] {e}")
        return "Imagen del negocio del usuario"

# ... (El resto de funciones y la clase Gateway se mantienen, asegúrate de incluirlas)