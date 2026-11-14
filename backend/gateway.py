# backend/gateway.py - VERSION 9.1 (MODELOS REALES + VISION REPARADA)
# ============================================

import os
import requests
import time
import base64
from dotenv import load_dotenv
from typing import Tuple, Optional
from utils.ai_usage_monitor import verificar_limite, registrar_consumo

load_dotenv()

# MODELOS REALES Y ACTIVOS EN 2026
MODELOS_OPENROUTER = [
    "meta-llama/llama-3.1-70b-instruct:free",
    "deepseek/deepseek-chat:free",
]

MODELOS_GROQ = [
    "llama3-70b-8192",
    "llama3-8b-8192",
]

MODELOS_GEMINI = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]

TIMEOUT_API = 180

def chat_openrouter(mensaje: str, sistema: str, temperature: float = 0.7, pedido_id: str = "sin_id") -> Optional[str]:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key: raise Exception("OPENROUTER_API_KEY no configurada")
    for modelo in MODELOS_OPENROUTER:
        try:
            with requests.Session() as session:
                response = session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={"model": modelo, "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": mensaje}], "temperature": temperature, "max_tokens": 4000},
                    timeout=TIMEOUT_API
                )
                if response.status_code == 200:
                    res = response.json()['choices'][0]['message']['content']
                    registrar_consumo(pedido_id, "openrouter", mensaje, res)
                    return res
                elif response.status_code == 429: time.sleep(3); continue
        except Exception as e: 
            print(f"[OPENROUTER ERROR] {e}")
            continue
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
                    json={"model": modelo, "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": mensaje}], "temperature": temperature, "max_tokens": 4000},
                    timeout=TIMEOUT_API
                )
                if response.status_code == 200:
                    res = response.json()['choices'][0]['message']['content']
                    registrar_consumo(pedido_id, "groq", mensaje, res)
                    return res
                elif response.status_code == 429: time.sleep(3); continue
        except Exception as e: 
            print(f"[GROQ ERROR] {e}")
            continue
    raise Exception("Ningun modelo de Groq disponible")

def chat_gemini_directo(mensaje: str, sistema: str, temperature: float = 0.7, pedido_id: str = "sin_id", foto_b64: str = None) -> Optional[str]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: raise Exception("GEMINI_API_KEY no configurada en Secrets")
    
    ultimo_error = "sin detalle"
    for modelo in MODELOS_GEMINI:
        try:
            url = f'https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}'
            
            partes = [{'text': f"{sistema}\n\nUsuario: {mensaje}"}]
            
            if foto_b64:
                foto_limpia = foto_b64
                if "," in foto_limpia: foto_limpia = foto_limpia.split(",")[1]
                partes.append({'inline_data': {'mime_type': 'image/jpeg', 'data': foto_limpia}})
                
            payload = {
                'contents': [{'role': 'user', 'parts': partes}], 
                'generationConfig': {'temperature': temperature, 'maxOutputTokens': 4000}
            }
            response = requests.post(url, json=payload, timeout=TIMEOUT_API)
            if response.status_code == 200:
                res = response.json()['candidates'][0]['content']['parts'][0]['text']
                registrar_consumo(pedido_id, "gemini_text", mensaje, res)
                return res
            else:
                ultimo_error = f"{modelo} HTTP {response.status_code}: {response.text[:200]}"
                print(f"[GEMINI] {ultimo_error}")
                time.sleep(2)
                continue
        except Exception as e: 
            ultimo_error = f"{modelo}: {e}"
            print(f"[GEMINI ERROR] {ultimo_error}")
            continue
    raise Exception(f"Ningun modelo de Gemini disponible. Ultimo error: {ultimo_error}")

def analizar_imagen_gemini(foto_b64: str, prompt: str, pedido_id: str = "sin_id") -> str:
    """NUEVA FUNCION: Analiza una imagen y devuelve texto descriptivo."""
    try:
        res = chat_gemini_directo(prompt, "Eres un experto en análisis visual.", temperature=0.1, pedido_id=pedido_id, foto_b64=foto_b64)
        return res if res else "Imagen sin descripción."
    except Exception as e:
        print(f"[VISION ERROR] {e}")
        return "Imagen del producto."

def chat_con_gemini(mensaje: str, sistema: str = "Eres un asistente util.", pedido_id: str = "sin_id", foto_b64: str = None) -> str:
    ok, msg = verificar_limite(pedido_id)
    if not ok: return f"[BLOQUEADO] {msg}"
    try:
        res = chat_gemini_directo(mensaje, sistema, temperature=0.1, pedido_id=pedido_id, foto_b64=foto_b64)
        return res if res else "[ERROR] Gemini no respondió."
    except Exception as e:
        return f"[ERROR] {e}"

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
    return "[ERROR] No hay modelos disponibles.", "ninguno"

class Gateway:
    def __init__(self):
        self.chat = chat_inteligente
        self.chat_rapido = chat_inteligente
        self.chat_inteligente = chat_inteligente
        self.chat_con_gemini = chat_con_gemini
        self.analizar_imagen = analizar_imagen_gemini

gateway = Gateway()