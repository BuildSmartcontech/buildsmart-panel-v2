# backend/gateway.py - VERSION 8.7 (ENRUTADOR INTELIGENTE)
# ============================================

import os
import requests
import time
import base64
from dotenv import load_dotenv
from typing import Tuple, Optional
from utils.ai_usage_monitor import verificar_limite, registrar_consumo

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
    "gemini-1.5-flash",
    "gemini-2.0-flash-exp",
]

TIMEOUT_API = 300

def chat_openrouter(mensaje: str, sistema: str, temperature: float = 0.7, pedido_id: str = "sin_id") -> Optional[str]:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key: raise Exception("OPENROUTER_API_KEY no configurada")

    for modelo in MODELOS_OPENROUTER:
        try:
            with requests.Session() as session:
                response = session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={"model": modelo, "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": mensaje}], "temperature": temperature, "max_tokens": 8000},
                    timeout=TIMEOUT_API
                )
                if response.status_code == 200:
                    res = response.json()['choices'][0]['message']['content']
                    registrar_consumo(pedido_id, "openrouter", mensaje, res)
                    return res
                elif response.status_code == 429: time.sleep(3); continue
        except Exception: continue
    raise Exception("Ningun modelo de OpenRouter disponible")

def chat_groq_directo(mensaje: str, sistema: str, temperature: float = 0.7, pedido_id: str = "sin_id") -> Optional[str]:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key: raise Exception("GROQ_API_KEY no configurada")

    for modelo in MODELOS_GROQ:
        try:
            with requests.Session() as session:
                response = session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={"model": modelo, "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": mensaje}], "temperature": temperature, "max_tokens": 8000},
                    timeout=TIMEOUT_API
                )
                if response.status_code == 200:
                    res = response.json()['choices'][0]['message']['content']
                    registrar_consumo(pedido_id, "groq", mensaje, res)
                    return res
                elif response.status_code == 429: time.sleep(3); continue
        except Exception: continue
    raise Exception("Ningun modelo de Groq disponible")

def chat_gemini_directo(mensaje: str, sistema: str, temperature: float = 0.7, pedido_id: str = "sin_id") -> Optional[str]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: raise Exception("GEMINI_API_KEY no configurada")

    for modelo in MODELOS_GEMINI:
        try:
            url = f'https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}'
            payload = {'contents': [{'role': 'user', 'parts': [{'text': f"{sistema}\n\nUsuario: {mensaje}"}]}], 'generationConfig': {'temperature': temperature, 'maxOutputTokens': 8000, 'topP': 0.95}}
            response = requests.post(url, json=payload, timeout=TIMEOUT_API)
            if response.status_code == 200:
                res = response.json()['candidates'][0]['content']['parts'][0]['text']
                registrar_consumo(pedido_id, "gemini_text", mensaje, res)
                return res
            elif response.status_code == 503: time.sleep(3); continue
        except Exception: continue
    raise Exception("Ningun modelo de Gemini disponible")

def analizar_imagen_gemini(base64_data: str, prompt_texto: str, pedido_id: str = "sin_id") -> str:
    ok, msg = verificar_limite(pedido_id)
    if not ok:
        print(f"[VISION] BLOQUEADO: {msg}")
        return "Imagen del negocio (Cuota agotada)"

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: return "Imagen subida por el usuario"

    if "," in base64_data: base64_data = base64_data.split(",")[1]

    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}'
    payload = {'contents': [{'role': 'user', 'parts': [{'text': prompt_texto}, {'inline_data': {'mime_type': 'image/jpeg', 'data': base64_data}}]}], 'generationConfig': {'temperature': 0.2, 'maxOutputTokens': 500}}

    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            descripcion = result['candidates'][0]['content']['parts'][0]['text'].strip()
            registrar_consumo(pedido_id, "gemini_vision", prompt_texto, descripcion)
            return descripcion
        return "Imagen del negocio del usuario"
    except Exception as e:
        print(f"[VISION ERROR] {e}")
        return "Imagen del negocio del usuario"

def chat_con_gemini(mensaje: str, sistema: str = "Eres un asistente util.", pedido_id: str = "sin_id") -> str:
    """Fuerza el uso de Gemini para tareas complejas."""
    ok, msg = verificar_limite(pedido_id)
    if not ok: return f"[BLOQUEADO] {msg}"
    try:
        res = chat_gemini_directo(mensaje, sistema, temperature=0.1, pedido_id=pedido_id)
        return res if res else "[ERROR] Gemini no respondió."
    except Exception:
        return "[ERROR] No se pudo conectar con Gemini."

def chat_inteligente(mensaje: str, sistema: str = "Eres un asistente util.", temperature: float = 0.7, pedido_id: str = "sin_id") -> Tuple[str, str]:
    ok, msg = verificar_limite(pedido_id)
    if not ok: return f"[BLOQUEADO] {msg}", "sistema"

    try:
        res = chat_groq_directo(mensaje, sistema, temperature, pedido_id)
        if res: return res, "groq"
    except Exception: pass
    
    try:
        res = chat_openrouter(mensaje, sistema, temperature, pedido_id)
        if res: return res, "openrouter"
    except Exception: pass
    
    try:
        res = chat_gemini_directo(mensaje, sistema, temperature, pedido_id)
        if res: return res, "gemini"
    except Exception: pass
    
    return "[ERROR] No hay modelos disponibles o cuota agotada.", "ninguno"

class Gateway:
    def __init__(self):
        self.chat = chat_inteligente
        self.chat_rapido = chat_inteligente
        self.chat_inteligente = chat_inteligente
        self.chat_con_gemini = chat_con_gemini

gateway = Gateway()