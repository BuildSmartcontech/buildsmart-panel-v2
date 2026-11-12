# utils/web_editor_v2.py
# ============================================
# EDITOR DE WEBS ESTRUCTURADO - V3.0 (CSS INJECTION)
# ============================================

import os
import sys
import re
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.web_prompts import generar_prompt_edicion_estructurada
from utils.html_patcher import aplicar_cambios

try:
    from backend.gateway import gateway
except ImportError:
    try:
        from gateway import gateway
    except ImportError:
        gateway = None

MAX_INTENTOS = 3
TIEMPO_ESPERA = 2

def extraer_estructura_html(html):
    if not html: return "HTML vacio"
    partes = []
    
    # Extraemos las clases para que la IA sepa qué hay
    clases = set()
    for match in re.finditer(r'class\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE):
        for c in match.group(1).split():
            clases.add(c)
    if clases:
        partes.append("CLASES CSS EXISTENTES: " + ", ".join(sorted(list(clases))[:30]))
        
    return "\n\n".join(partes)

def parsear_json_cambios(texto):
    if not texto: return None
    texto = texto.strip()
    if texto.startswith("```"):
        texto = re.sub(r'^```(?:json)?\s*', '', texto)
        texto = re.sub(r'\s*```$', '', texto)
    inicio = texto.find("{")
    fin = texto.rfind("}")
    if inicio == -1 or fin == -1: return None
    try:
        return json.loads(texto[inicio:fin + 1])
    except json.JSONDecodeError:
        return None

def editar_web_v2(usuario_id, web_id, instruccion, contexto_negocio="", html_actual=None):
    print("=" * 60)
    print("EDITANDO WEB (CSS INJECTION) - V3.0")
    print("=" * 60)
    
    if gateway is None:
        return {"exito": False, "error": "Gateway no disponible"}

    if html_actual is None:
        try:
            from utils.web_storage import leer_web
        except ImportError:
            from web_storage import leer_web
        resultado_lectura = leer_web(usuario_id, web_id)
        if not resultado_lectura["exito"]:
            return {"exito": False, "error": "No se pudo leer la web."}
        html_actual = resultado_lectura["html"]

    estructura = extraer_estructura_html(html_actual)

    for intento in range(1, MAX_INTENTOS + 1):
        try:
            prompt = generar_prompt_edicion_estructurada(estructura, instruccion, contexto_negocio)
            sistema = "Eres un experto en CSS. Devuelves SOLO JSON."
            respuesta, fuente = gateway.chat_inteligente(prompt, sistema)

            data = parsear_json_cambios(respuesta)
            if not data or "reglas_css" not in data:
                time.sleep(TIEMPO_ESPERA)
                continue

            resultado_patcher = aplicar_cambios(html_actual, data)
            
            if not resultado_patcher["exito"]:
                time.sleep(TIEMPO_ESPERA)
                continue

            return {
                "exito": True,
                "html_nuevo": resultado_patcher["html_nuevo"],
                "cambios_aplicados": resultado_patcher.get("cambios_aplicados", 1),
                "aplicados": resultado_patcher.get("aplicados", []),
                "fallidos": resultado_patcher.get("fallidos", []),
                "error": None
            }
        except Exception as e:
            print(f"Error en intento {intento}: {e}")
            time.sleep(TIEMPO_ESPERA)

    return {"exito": False, "error": "No se pudieron aplicar cambios tras 3 intentos."}

def editar_y_guardar_v2(usuario_id, web_id, instruccion, contexto_negocio=""):
    resultado = editar_web_v2(usuario_id, web_id, instruccion, contexto_negocio)
    if not resultado["exito"]:
        return resultado

    try:
        from utils.web_storage import guardar_en_archivos
    except ImportError:
        from web_storage import guardar_en_archivos

    guardado = guardar_en_archivos(usuario_id, web_id, resultado["html_nuevo"])
    resultado["guardado"] = guardado["exito"]
    return resultado