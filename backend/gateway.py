# backend/gateway.py - VERSION 8.2
# ============================================
# MEJORAS v8.2:
# - Groq: modelos actualizados (gpt-oss-120b, gpt-oss-20b)
#   * Antes usaba qwen3.6-27b (404) y qwen3.8-27b (rate limited)
# - Gemini: modelos actualizados (gemini-2.0-flash-exp + 1.5-flash)
# - Sin mojibake en comentarios
# ============================================

import os
import requests
import time
from dotenv import load_dotenv
from typing import Tuple, Optional

load_dotenv()


# ============================================
# MODELOS VERIFICADOS
# ============================================

MODELOS_OPENROUTER = [
    "nvidia/nemotron-3-super-120b-a12b:free",     # Verificado funcionando
    "deepseek/deepseek-chat-v3.1:free",           # Potente para codigo
    "meta-llama/llama-3.3-70b-instruct:free",     # Excelente HTML
    "qwen/qwen-2.5-72b-instruct:free",            # Buen respaldo
]

# MODELOS GROQ - ACTUALIZADOS V8.2
# Los GPT-OSS son los mas potentes y estan disponibles
MODELOS_GROQ = [
    "openai/gpt-oss-120b",       # Principal - potente
    "openai/gpt-oss-20b",        # Fallback - rapido
    "qwen/qwen3.8-27b",          # Ultimo recurso
]

# MODELOS GEMINI - ACTUALIZADOS V8.2
MODELOS_GEMINI = [
    "gemini-2.0-flash-exp",      # Multimodal, rapido
    "gemini-1.5-flash",          # Fallback estable
]

# Timeout global para todas las APIs
TIMEOUT_API = 300  # 5 minutos


# ============================================
# 1. OPENROUTER
# ============================================

def chat_openrouter(mensaje: str, sistema: str) -> Optional[str]:
    """Chat con OpenRouter - Contexto largo"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise Exception("OPENROUTER_API_KEY no configurada")

    for modelo in MODELOS_OPENROUTER:
        try:
            print(f"   Intentando OpenRouter: {modelo}")
            with requests.Session() as session:
                response = session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": modelo,
                        "messages": [
                            {"role": "system", "content": sistema},
                            {"role": "user", "content": mensaje}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 8000
                    },
                    timeout=TIMEOUT_API
                )

                if response.status_code == 200:
                    print(f"   [OK] OpenRouter: {modelo}")
                    return response.json()['choices'][0]['message']['content']
                elif response.status_code == 429:
                    print(f"   [WAIT] Rate Limit, esperando 3s...")
                    time.sleep(3)
                    continue
                else:
                    print(f"   [FAIL] OpenRouter error: {response.status_code}")
                    continue
        except Exception as e:
            print(f"   [FAIL] OpenRouter exception: {str(e)[:50]}")
            continue

    raise Exception("Ningun modelo de OpenRouter disponible")


# ============================================
# 2. GROQ
# ============================================

def chat_groq_directo(mensaje: str, sistema: str) -> Optional[str]:
    """Chat con Groq - Rapido"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise Exception("GROQ_API_KEY no configurada")

    for modelo in MODELOS_GROQ:
        try:
            print(f"   Intentando Groq: {modelo}")
            with requests.Session() as session:
                response = session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": modelo,
                        "messages": [
                            {"role": "system", "content": sistema},
                            {"role": "user", "content": mensaje}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 8000
                    },
                    timeout=TIMEOUT_API
                )

                if response.status_code == 200:
                    print(f"   [OK] Groq: {modelo}")
                    return response.json()['choices'][0]['message']['content']
                elif response.status_code == 429:
                    print(f"   [WAIT] Rate Limit (429), esperando 3s...")
                    time.sleep(3)
                    continue
                else:
                    print(f"   [FAIL] Groq error: {response.status_code}")
                    continue
        except Exception as e:
            print(f"   [FAIL] Groq exception: {str(e)[:50]}")
            continue

    raise Exception("Ningun modelo de Groq disponible")


# ============================================
# 3. GEMINI
# ============================================

def chat_gemini_directo(mensaje: str, sistema: str) -> Optional[str]:
    """Chat con Gemini - Multimodal"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise Exception("GEMINI_API_KEY no configurada")

    for modelo in MODELOS_GEMINI:
        try:
            print(f"   Intentando Gemini: {modelo}")
            url = f'https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}'
            prompt_completo = f"{sistema}\n\nUsuario: {mensaje}"

            payload = {
                'contents': [
                    {
                        'role': 'user',
                        'parts': [{'text': prompt_completo}]
                    }
                ],
                'generationConfig': {
                    'temperature': 0.7,
                    'maxOutputTokens': 8000,
                    'topP': 0.95,
                    'topK': 40
                }
            }

            response = requests.post(url, json=payload, timeout=TIMEOUT_API)

            if response.status_code == 200:
                result = response.json()
                text = result['candidates'][0]['content']['parts'][0]['text']
                print(f"   [OK] Gemini: {modelo}")
                return text
            elif response.status_code == 503:
                print(f"   [WAIT] Servicio ocupado (503), esperando 3s...")
                time.sleep(3)
                continue
            else:
                print(f"   [FAIL] Gemini error: {response.status_code}")
                continue

        except Exception as e:
            print(f"   [FAIL] Gemini exception: {str(e)[:50]}")
            continue

    raise Exception("Ningun modelo de Gemini disponible")


# ============================================
# 4. OLLAMA (RESPALDO)
# ============================================

def chat_ollama(mensaje: str, sistema: str) -> Optional[str]:
    """Chat con Ollama - Local (ultimo recurso)"""
    try:
        print("   Intentando Ollama (local)...")
        with requests.Session() as session:
            response = session.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5:3b",
                    "prompt": f"{sistema}\n\nUsuario: {mensaje}\n\nAsistente:",
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=300
            )

            if response.status_code == 200:
                print("   [OK] Ollama")
                return response.json().get('response', '')
            else:
                raise Exception(f"Ollama error: {response.status_code}")
    except Exception as e:
        raise Exception(f"Ollama exception: {str(e)}")


# ============================================
# 5. CHAT RAPIDO (SALUDOS)
# ============================================

def chat_rapido(mensaje: str, sistema: str = "Eres un asistente amigable.") -> Tuple[str, str]:
    """Chat rapido para saludos y mensajes simples."""
    # 1. Groq (mas rapido)
    try:
        print("[FAST] Chat rapido: Intentando Groq...")
        respuesta = chat_groq_directo(mensaje, sistema)
        return respuesta, "groq"
    except Exception as e:
        print(f"[WARN] Groq fallo: {str(e)[:50]}")

    # 2. OpenRouter
    try:
        print("[FAST] Chat rapido: Intentando OpenRouter...")
        respuesta = chat_openrouter(mensaje, sistema)
        return respuesta, "openrouter"
    except Exception as e:
        print(f"[WARN] OpenRouter fallo: {str(e)[:50]}")

    # 3. Gemini
    try:
        print("[FAST] Chat rapido: Intentando Gemini...")
        respuesta = chat_gemini_directo(mensaje, sistema)
        return respuesta, "gemini"
    except Exception as e:
        print(f"[WARN] Gemini fallo: {str(e)[:50]}")

    return "Hola! En que puedo ayudarte?", "ninguno"


# ============================================
# 6. CHAT INTELIGENTE (TAREAS) - V8.2
# ============================================

def chat_inteligente(mensaje: str, sistema: str = "Eres un asistente util.") -> Tuple[str, str]:
    """
    Chat para tareas complejas.
    Prioriza Groq (mas rapido) -> OpenRouter -> Gemini -> Ollama.
    """
    # 1. Groq (mas rapido, 5-15 seg)
    try:
        print("[IA] Chat inteligente: Intentando Groq...")
        respuesta = chat_groq_directo(mensaje, sistema)
        return respuesta, "groq"
    except Exception as e:
        print(f"[WARN] Groq fallo: {str(e)[:50]}")

    # 2. OpenRouter (contexto largo, 60-120 seg)
    try:
        print("[IA] Chat inteligente: Intentando OpenRouter...")
        respuesta = chat_openrouter(mensaje, sistema)
        return respuesta, "openrouter"
    except Exception as e:
        print(f"[WARN] OpenRouter fallo: {str(e)[:50]}")

    # 3. Gemini
    try:
        print("[IA] Chat inteligente: Intentando Gemini...")
        respuesta = chat_gemini_directo(mensaje, sistema)
        return respuesta, "gemini"
    except Exception as e:
        print(f"[WARN] Gemini fallo: {str(e)[:50]}")

    # 4. Ollama (local)
    try:
        print("[IA] Chat inteligente: Intentando Ollama...")
        respuesta = chat_ollama(mensaje, sistema)
        return respuesta, "ollama"
    except Exception as e:
        print(f"[WARN] Ollama fallo: {str(e)[:50]}")

    return "[ERROR] No hay modelos disponibles.", "ninguno"


# ============================================
# 7. CHAT GATEWAY (GENERAL)
# ============================================

def chat_gateway(mensaje: str, sistema: str = "Eres un asistente util.") -> Tuple[str, str]:
    """Enrutamiento general."""
    try:
        print("[TRY] Probando: Groq")
        respuesta = chat_groq_directo(mensaje, sistema)
        return respuesta, "groq"
    except Exception as e:
        print(f"[WARN] Groq: {str(e)[:50]}")

    try:
        print("[TRY] Probando: OpenRouter")
        respuesta = chat_openrouter(mensaje, sistema)
        return respuesta, "openrouter"
    except Exception as e:
        print(f"[WARN] OpenRouter: {str(e)[:50]}")

    try:
        print("[TRY] Probando: Gemini")
        respuesta = chat_gemini_directo(mensaje, sistema)
        return respuesta, "gemini"
    except Exception as e:
        print(f"[WARN] Gemini: {str(e)[:50]}")

    try:
        print("[TRY] Probando: Ollama (local)")
        respuesta = chat_ollama(mensaje, sistema)
        return respuesta, "ollama"
    except Exception as e:
        print(f"[WARN] Ollama: {str(e)[:50]}")

    return "[ERROR] No hay modelos disponibles.", "ninguno"


# ============================================
# FUNCIONES ADICIONALES
# ============================================

def generar_imagen_gemini(prompt: str) -> str:
    """Genera una imagen usando Gemini"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "[ERROR] GEMINI_API_KEY no configurada"

    # Modelos de imagen de Gemini
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "temperature": 1.0,
            "candidateCount": 1
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=180)
        if response.status_code == 200:
            data = response.json()
            parts = data['candidates'][0]['content']['parts']
            for part in parts:
                if 'inlineData' in part:
                    import base64
                    image_data = part['inlineData']['data']
                    ruta = f"imagenes/gemini_{int(time.time())}.png"
                    os.makedirs("imagenes", exist_ok=True)
                    with open(ruta, 'wb') as f:
                        f.write(base64.b64decode(image_data))
                    return ruta
        return f"[ERROR] {response.status_code}"
    except Exception as e:
        return f"[ERROR] {str(e)}"


def generar_video_kling(prompt: str, duracion: int = 5, resolucion: str = "720p") -> dict:
    """Genera un video usando Kling AI"""
    api_key = os.getenv("KLING_API_KEY")
    if not api_key:
        return {"error": "KLING_API_KEY no configurada"}

    url = "https://api.klingai.com/v1/videos/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "kling-v3",
        "prompt": prompt,
        "duration": duracion,
        "resolution": resolucion
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "task_id": data.get("data", {}).get("task_id"),
                "status": data.get("data", {}).get("status"),
                "video_url": data.get("data", {}).get("video_url")
            }
        return {"error": f"Error {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}


def consultar_video_kling(task_id: str) -> dict:
    """Consulta el estado de un video en Kling AI"""
    api_key = os.getenv("KLING_API_KEY")
    if not api_key:
        return {"error": "KLING_API_KEY no configurada"}

    url = f"https://api.klingai.com/v1/videos/generations/{task_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        response = requests.get(url, headers=headers, timeout=60)
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "status": data.get("data", {}).get("status"),
                "video_url": data.get("data", {}).get("video_url")
            }
        return {"error": f"Error {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


# ============================================
# INSTANCIA GLOBAL
# ============================================

class Gateway:
    def __init__(self):
        self.chat = chat_gateway
        self.chat_rapido = chat_rapido
        self.chat_inteligente = chat_inteligente
        self.generar_imagen = generar_imagen_gemini
        self.generar_video = generar_video_kling
        self.consultar_video = consultar_video_kling


gateway = Gateway()


# ============================================
# PRUEBA
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("PROBANDO GATEWAY - VERSION 8.2")
    print("=" * 60)

    print("\n[TEST 1] Chat rapido (Groq)")
    respuesta, fuente = chat_rapido("Hola, como estas?")
    print(f"Fuente: {fuente}")
    print(f"Respuesta: {respuesta[:150]}...")

    print("\n" + "=" * 60)
    print("\n[TEST 2] Chat inteligente (Groq primero)")
    respuesta, fuente = chat_inteligente("Necesito un plan de marketing")
    print(f"Fuente: {fuente}")
    print(f"Respuesta: {respuesta[:150]}...")