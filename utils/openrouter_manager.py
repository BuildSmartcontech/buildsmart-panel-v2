# utils/openrouter_manager.py
# ============================================
# GESTOR DE OPENROUTER - Modelos Gratuitos y Premium
# ============================================
# V1.0: Integra modelos gratuitos con selector y manejo de rate limits.
# ============================================

import os
import time
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Modelos gratuitos solicitados
MODELOS_GRATUITOS = {
    "openrouter/free": "Enrutador automatico de modelos gratis",
    "nvidia/nemotron-3-ultra:free": "Orquestacion y razonamiento (NVIDIA)",
    "nvidia/nemotron-3.5-super-vl:free": "Imagenes y documentos (NVIDIA)",
    "croutonlabs/crouton-alpha:free": "Tareas de agente repetitivas",
    "poolside-ai/poolside-laguna-s-2.1:free": "Codigo (Poolside)",
    "google/gemma-4-26b-it-a4b:free": "Multilingue (Google Gemma 4)",
}

# Modelos premium (si el usuario tiene creditos)
MODELOS_PREMIUM = {
    "anthropic/claude-3.5-sonnet": "Claude 3.5 Sonnet (Excelente para CSS/HTML)",
    "openai/gpt-4o": "GPT-4o (Muy bueno para codigo)",
}

MAX_REQUESTS_POR_MINUTO = 20
MAX_REQUESTS_POR_DIA = 50  # Sube a 1000 si compras $10 en creditos
_historial_requests = []

def _get_api_key():
    return os.getenv("OPENROUTER_API_KEY", "")

def _rate_limit_ok():
    """Verifica si estamos dentro del limite (20 req/min y 50 req/dia)."""
    ahora = time.time()
    _historial_requests[:] = [t for t in _historial_requests if ahora - t < 86400]
    
    requests_ultimo_minuto = sum(1 for t in _historial_requests if ahora - t < 60)
    if requests_ultimo_minuto >= MAX_REQUESTS_POR_MINUTO:
        return False, f"Limite de {MAX_REQUESTS_POR_MINUTO} req/min alcanzado. Espera un momento."
    
    if len(_historial_requests) >= MAX_REQUESTS_POR_DIA:
        return False, f"Limite de {MAX_REQUESTS_POR_DIA} req/dia alcanzado. Compra $10 en creditos para subir a 1000."
    
    return True, "OK"

def _registrar_request():
    _historial_requests.append(time.time())

def consultar_openrouter(mensaje: str, sistema: str = "Eres un asistente util.", modelo: str = "openrouter/free") -> tuple:
    """
    Consulta a OpenRouter con el modelo seleccionado.
    Retorna (respuesta, modelo_usado, error).
    """
    api_key = _get_api_key()
    if not api_key:
        return None, modelo, "OPENROUTER_API_KEY no configurada en .env o Secrets."

    ok, msg = _rate_limit_ok()
    if not ok:
        return None, modelo, msg

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": modelo,
        "messages": [
            {"role": "system", "content": sistema},
            {"role": "user", "content": mensaje}
        ],
        "temperature": 0.7,
        "max_tokens": 8000,
    }

    try:
        _registrar_request()
        r = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=300)
        
        if r.status_code == 200:
            data = r.json()
            respuesta = data['choices'][0]['message']['content']
            return respuesta, modelo, None
        elif r.status_code == 429:
            return None, modelo, "Rate limit alcanzado (429). Espera o usa otro modelo."
        else:
            return None, modelo, f"Error HTTP {r.status_code}: {r.text[:200]}"
    except Exception as e:
        return None, modelo, f"Excepcion: {str(e)}"

def renderizar_selector_modelo():
    """Renderiza un selector de modelo en el sidebar y devuelve el elegido."""
    st.sidebar.markdown("### 🤖 Motor de IA (OpenRouter)")
    
    opciones = {**MODELOS_GRATUITOS, **MODELOS_PREMIUM}
    
    modelo_elegido = st.sidebar.selectbox(
        "Selecciona el modelo para generar webs",
        options=list(opciones.keys()),
        format_func=lambda x: f"{x.split('/')[-1]} — {opciones[x]}",
        index=0,
        key="openrouter_modelo_selector"
    )
    
    ok, msg = _rate_limit_ok()
    if ok:
        st.sidebar.caption(f"✅ Rate limit OK ({len(_historial_requests)}/{MAX_REQUESTS_POR_DIA} req hoy)")
    else:
        st.sidebar.warning(f"⚠️ {msg}")
    
    return modelo_elegido