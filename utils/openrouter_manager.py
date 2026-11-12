# utils/openrouter_manager.py
# ============================================
# GESTOR DE OPENROUTER - V1.3 (MONITOREO)
# ============================================

import os
import time
import requests
import streamlit as st
from dotenv import load_dotenv
from utils.ai_usage_monitor import verificar_limite, registrar_consumo

load_dotenv()
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

MODELOS_GRATUITOS = {
    "openrouter/free": "Enrutador automatico de modelos gratis",
    "nvidia/nemotron-3-ultra:free": "Orquestacion y razonamiento (NVIDIA)",
    "nvidia/nemotron-3.5-super-vl:free": "Imagenes y documentos (NVIDIA)",
    "croutonlabs/crouton-alpha:free": "Tareas de agente repetitivas",
    "poolside-ai/poolside-laguna-s-2.1:free": "Codigo (Poolside)",
    "google/gemma-4-26b-it-a4b:free": "Multilingue (Google Gemma 4)",
}
MODELOS_PREMIUM = {
    "anthropic/claude-3.5-sonnet": "Claude 3.5 Sonnet (Excelente para CSS/HTML)",
    "openai/gpt-4o": "GPT-4o (Muy bueno para codigo)",
}

MAX_REQUESTS_POR_MINUTO = 20
MAX_REQUESTS_POR_DIA = 50
_historial_requests = []

def _get_api_key(): return os.getenv("OPENROUTER_API_KEY", "")

def _rate_limit_ok():
    ahora = time.time()
    _historial_requests[:] = [t for t in _historial_requests if ahora - t < 86400]
    if sum(1 for t in _historial_requests if ahora - t < 60) >= MAX_REQUESTS_POR_MINUTO: return False, "Limite minuto"
    if len(_historial_requests) >= MAX_REQUESTS_POR_DIA: return False, "Limite diario"
    return True, "OK"

def _registrar_request(): _historial_requests.append(time.time())

def consultar_openrouter(mensaje: str, sistema: str = "Eres un asistente util.", modelo: str = "openrouter/free", temperature: float = 0.7, pedido_id: str = "sin_id") -> tuple:
    ok_bd, msg_bd = verificar_limite(pedido_id)
    if not ok_bd: return None, modelo, f"BLOQUEADO: {msg_bd}"

    api_key = _get_api_key()
    if not api_key: return None, modelo, "OPENROUTER_API_KEY no configurada."

    ok, msg = _rate_limit_ok()
    if not ok: return None, modelo, msg

    try:
        _registrar_request()
        r = requests.post(OPENROUTER_API_URL, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json={"model": modelo, "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": mensaje}], "temperature": temperature, "max_tokens": 8000}, timeout=300)
        if r.status_code == 200:
            res = r.json()['choices'][0]['message']['content']
            registrar_consumo(pedido_id, "openrouter", mensaje, res)
            return res, modelo, None
        elif r.status_code == 429: return None, modelo, "Rate limit alcanzado (429)."
        else: return None, modelo, f"Error HTTP {r.status_code}"
    except Exception as e: return None, modelo, f"Excepcion: {str(e)}"

def renderizar_selector_modelo():
    st.sidebar.markdown("### 🤖 Motor de IA (OpenRouter)")
    opciones = {**MODELOS_GRATUITOS, **MODELOS_PREMIUM}
    modelo_elegido = st.sidebar.selectbox("Selecciona el modelo", options=list(opciones.keys()), format_func=lambda x: f"{x.split('/')[-1]} — {opciones[x]}", index=0, key="openrouter_modelo_selector")
    ok, msg = _rate_limit_ok()
    if ok: st.sidebar.caption(f"✅ Rate limit OK")
    else: st.sidebar.warning(f"⚠️ {msg}")
    return modelo_elegido