# backend/gateway.py - VERSION 8.3
# ============================================
# MEJORAS v8.3:
# - Parametro "temperature" agregado a todos los modelos.
# - Permite alternar entre modo Creativo (0.7) y Estricto (0.1).
# ============================================

import os
import requests
import time
from dotenv import load_dotenv
from typing import Tuple, Optional

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
    "gemini-2.0-flash-exp",
    "gemini-1.5-flash",
]

TIMEOUT_API = 300

def chat_openrouter(mensaje: str, sistema: str, temperature: float = 0.7) -> Optional[str]:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key: raise Exception("OPENROUTER_API_KEY no configurada")

    for modelo in MODELOS_OPENROUTER:
        try:
            print(f"   Intentando OpenRouter: {modelo} (Temp: {temperature})")
            with requests.Session() as session:
                response = session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={
                        "model": modelo,
                        "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": mensaje}],
                        "temperature": temperature,
                        "max_tokens": 8000
                    },
                    timeout=TIMEOUT_API
                )
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
                elif response.status_code == 429:
                    time.sleep(3)
                    continue
        except Exception:
            continue
    raise Exception("Ningun modelo de OpenRouter disponible")

def chat_groq_directo(mensaje: str, sistema: str, temperature: float = 0.7) -> Optional[str]:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key: raise Exception("GROQ_API_KEY no configurada")

    for modelo in MODELOS_GROQ:
        try:
            print(f"   Intentando Groq: {modelo} (Temp: {temperature})")
            with requests.Session() as session:
                response = session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={
                        "model": modelo,
                        "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": mensaje}],
                        "temperature": temperature,
                        "max_tokens": 8000
                    },
                    timeout=TIMEOUT_API
                )
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
                elif response.status_code == 429:
                    time.sleep(3)
                    continue
        except Exception:
            continue
    raise Exception("Ningun modelo de Groq disponible")

def chat_gemini_directo(mensaje: str, sistema: str, temperature: float = 0.7) -> Optional[str]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: raise Exception("GEMINI_API_KEY no configurada")

    for modelo in MODELOS_GEMINI:
        try:
            print(f"   Intentando Gemini: {modelo} (Temp: {temperature})")
            url = f'https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}'
            payload = {
                'contents': [{'role': 'user', 'parts': [{'text': f"{sistema}\n\nUsuario: {mensaje}"}]}],
                'generationConfig': {'temperature': temperature, 'maxOutputTokens': 8000, 'topP': 0.95}
            }
            response = requests.post(url, json=payload, timeout=TIMEOUT_API)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            elif response.status_code == 503:
                time.sleep(3)
                continue
        except Exception:
            continue
    raise Exception("Ningun modelo de Gemini disponible")

def chat_ollama(mensaje: str, sistema: str, temperature: float = 0.7) -> Optional[str]:
    try:
        with requests.Session() as session:
            response = session.post(
                "http://localhost:11434/api/generate",
                json={"model": "qwen2.5:3b", "prompt": f"{sistema}\n\nUsuario: {mensaje}\n\nAsistente:", "stream": False, "temperature": temperature},
                timeout=300
            )
            if response.status_code == 200: return response.json().get('response', '')
    except Exception:
        pass
    raise Exception("Ollama no disponible")

def chat_inteligente(mensaje: str, sistema: str = "Eres un asistente util.", temperature: float = 0.7) -> Tuple[str, str]:
    try:
        print("[IA] Chat inteligente: Intentando Groq...")
        return chat_groq_directo(mensaje, sistema, temperature), "groq"
    except Exception: pass
    try:
        print("[IA] Chat inteligente: Intentando OpenRouter...")
        return chat_openrouter(mensaje, sistema, temperature), "openrouter"
    except Exception: pass
    try:
        print("[IA] Chat inteligente: Intentando Gemini...")
        return chat_gemini_directo(mensaje, sistema, temperature), "gemini"
    except Exception: pass
    try:
        return chat_ollama(mensaje, sistema, temperature), "ollama"
    except Exception: pass
    return "[ERROR] No hay modelos disponibles.", "ninguno"

# (Las demás funciones como chat_rapido, chat_gateway se mantienen igual, 
# pero llaman a chat_inteligente con temperature por defecto 0.7)

class Gateway:
    def __init__(self):
        self.chat = chat_inteligente
        self.chat_rapido = chat_inteligente
        self.chat_inteligente = chat_inteligente

gateway = Gateway()