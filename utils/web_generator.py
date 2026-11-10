# utils/web_generator.py
# ============================================
# GENERADOR DE WEBS CON IA - V7.0 (AGENTE ESTRATEGA + PROGRAMADOR)
# ============================================
# V7.0: Implementa Chain of Thought. Primero redacta el copy, luego el HTML.
# ============================================

import os
import sys
import re
import time
import json

try:
    import requests as _requests
    REQUESTS_DISPONIBLE = True
except ImportError:
    REQUESTS_DISPONIBLE = False

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.web_prompts_data import DIRECTOR_DE_ARTE_PROMPT, REGLAS_CSS_PREMIUM, REGLAS_FORMULARIO, REGLAS_IMAGENES, REGLAS_SALIDA, REGLAS_SECCION_UBICACION, REGLAS_SECCION_HORARIOS, REGLAS_REDES_SOCIALES, construir_instrucciones_dinamicas
    from utils.web_validator import validar_completo, limpiar_html
except ImportError:
    from web_prompts_data import DIRECTOR_DE_ARTE_PROMPT, REGLAS_CSS_PREMIUM, REGLAS_FORMULARIO, REGLAS_IMAGENES, REGLAS_SALIDA, REGLAS_SECCION_UBICACION, REGLAS_SECCION_HORARIOS, REGLAS_REDES_SOCIALES, construir_instrucciones_dinamicas
    from web_validator import validar_completo, limpiar_html

try:
    from backend.gateway import gateway
except ImportError:
    try:
        from gateway import gateway
    except ImportError:
        gateway = None

try:
    from utils.image_fetcher import obtener_urls_imagenes_negocio
    IMAGENES_DISPONIBLES = True
except ImportError:
    try:
        from image_fetcher import obtener_urls_imagenes_negocio
        IMAGENES_DISPONIBLES = True
    except ImportError:
        IMAGENES_DISPONIBLES = False

try:
    from utils.openrouter_manager import consultar_openrouter
    OPENROUTER_DISPONIBLE = True
except ImportError:
    OPENROUTER_DISPONIBLE = False

MAX_INTENTOS = 3
TIEMPO_ESPERA = 2

# ==========================================
# PASO 1: EL ESTRATEGA (Redacta el Copy)
# ==========================================
def generar_copy_estrategico(datos_negocio, modelo_ia):
    prompt = f"""
Eres un Director de Marketing Digital experto en ventas B2B.
Analiza el siguiente negocio:
- Nombre: {datos_negocio.get('nombre')}
- Sector: {datos_negocio.get('sector')}
- Descripcion: {datos_negocio.get('descripcion')}
- Publico: {datos_negocio.get('publico_objetivo')}
- Diferenciadores: {datos_negocio.get('diferenciadores')}

Tu tarea es redactar el Copy exacto para su pagina web premium.
Debes devolver UNICAMENTE un JSON valido con la siguiente estructura:
{{
  "headline": "Un titulo impactante para el Hero (max 10 palabras)",
  "subheadline": "Un subtitulo persuasivo (max 25 palabras)",
  "servicios": [
    {{"titulo": "Servicio 1", "descripcion": "Texto persuasivo (20 palabras)"}},
    {{"titulo": "Servicio 2", "descripcion": "Texto persuasivo (20 palabras)"}},
    {{"titulo": "Servicio 3", "descripcion": "Texto persuasivo (20 palabras)"}}
  ],
  "sobre_nosotros": "Un parrafo de 40 palabras sobre la historia y vision del negocio.",
  "keywords_imagenes": ["palabra_en_ingles_1", "palabra_en_ingles_2"]
}}
NO incluyas markdown, solo el JSON.
"""
    sistema = "Eres un copywriter experto. Devuelves solo JSON."
    
    if OPENROUTER_DISPONIBLE:
        respuesta, _, error = consultar_openrouter(prompt, sistema, modelo=modelo_ia)
        if not error:
            return respuesta
            
    if gateway:
        respuesta, _ = gateway.chat_inteligente(prompt, sistema)
        return respuesta
        
    return None

# ==========================================
# PASO 2: EL PROGRAMADOR (Genera el HTML)
# ==========================================
def generar_html_programador(datos_negocio, copy, imagenes, modelo_ia):
    instrucciones_dinamicas = construir_instrucciones_dinamicas(datos_negocio)
    
    prompt = f"""
{DIRECTOR_DE_ARTE_PROMPT}

=========================================================
GENERA LA PAGINA WEB COMPLETA
=========================================================

## INFORMACION DEL NEGOCIO
- Nombre: {datos_negocio.get('nombre')}
- Sector: {datos_negocio.get('sector')}

## COPY EXACTO A UTILIZAR (NO INVENTES TEXTO, USA ESTE)
- Headline Hero: {copy.get('headline')}
- Subheadline Hero: {copy.get('subheadline')}
- Servicios:
  1. {copy.get('servicios', [{}])[0].get('titulo')}: {copy.get('servicios', [{}])[0].get('descripcion')}
  2. {copy.get('servicios', [{}, {}])[1].get('titulo')}: {copy.get('servicios', [{}, {}])[1].get('descripcion')}
  3. {copy.get('servicios', [{}, {}, {}])[2].get('titulo')}: {copy.get('servicios', [{}, {}, {}])[2].get('descripcion')}
- Sobre Nosotros: {copy.get('sobre_nosotros')}

## INSTRUCCIONES DINAMICAS (Ubicacion/Horarios/Redes)
{instrucciones_dinamicas}

## REGLAS DE DISENO (OBLIGATORIO)
{REGLAS_CSS_PREMIUM}

{REGLAS_IMAGENES}
{REGLAS_FORMULARIO}
{REGLAS_SALIDA}
"""
    sistema = "Eres un programador Frontend Senior. Devuelves solo HTML."
    
    if OPENROUTER_DISPONIBLE:
        respuesta, _, error = consultar_openrouter(prompt, sistema, modelo=modelo_ia)
        if not error:
            return respuesta
            
    if gateway:
        respuesta, _ = gateway.chat_inteligente(prompt, sistema)
        return respuesta
        
    return None

# ==========================================
# FUNCION PRINCIPAL
# ==========================================
def generar_web(datos_negocio, opciones=None, usar_template=True, con_imagenes=True, modelo_ia="openrouter/free"):
    print("=" * 60)
    print("GENERANDO WEB - V7.0 (Agente Estratega + Programador)")
    print("=" * 60)

    if not gateway and not OPENROUTER_DISPONIBLE:
        return {"exito": False, "html": None, "error": "Gateway no disponible"}

    # 1. Generar Copy Estrategico
    print("[PASO 1] Generando copy persuasivo...")
    copy_raw = generar_copy_estrategico(datos_negocio, modelo_ia)
    if not copy_raw:
        return {"exito": False, "html": None, "error": "Fallo el paso 1 (Copy)"}
        
    try:
        # Limpiar el JSON por si la IA agrega markdown
        copy_str = copy_raw.replace("```json", "").replace("```", "").strip()
        copy = json.loads(copy_str)
        print(f"[PASO 1] Exito. Headline: {copy.get('headline')}")
    except Exception as e:
        print(f"[PASO 1] Error parseando JSON: {e}")
        return {"exito": False, "html": None, "error": "La IA no devolvio un JSON valido en el copy."}

    # 2. Preparar Imagenes (Usuario o Pollinations)
    imagenes = {"hero": None, "servicios": []}
    logo_b64 = datos_negocio.get("logo_b64")
    fotos_b64 = datos_negocio.get("fotos_b64", [])
    
    if fotos_b64:
        imagenes["hero"] = fotos_b64[0] if len(fotos_b64) > 0 else None
        imagenes["servicios"] = fotos_b64[1:4]
    elif con_imagenes and IMAGENES_DISPONIBLES:
        keywords = copy.get("keywords_imagenes", ["business"])
        negocio_info = {"nombre": datos_negocio.get("nombre"), "sector": " ".join(keywords), "descripcion": datos_negocio.get("descripcion")}
        poll = obtener_urls_imagenes_negocio(negocio_info, cantidad=4)
        if poll:
            imagenes["hero"] = poll[0]["url_regular"]
            imagenes["servicios"] = [p["url_regular"] for p in poll[1:4]]

    # 3. Generar HTML Programador
    print("[PASO 2] Generando HTML con el copy inyectado...")
    for intento in range(1, MAX_INTENTOS + 1):
        html_raw = generar_html_programador(datos_negocio, copy, imagenes, modelo_ia)
        
        if not html_raw:
            time.sleep(TIEMPO_ESPERA)
            continue

        html = limpiar_html(html_raw)
        
        # Inyectar Logo
        if logo_b64:
            html = html.replace("{{LOGO_IMAGE}}", logo_b64)
            
        # Inyectar Hero y Servicios
        if imagenes.get("hero"):
            html = html.replace("{{HERO_IMAGE}}", imagenes["hero"])
        for i, img in enumerate(imagenes.get("servicios", []), 1):
            html = html.replace(f"{{{{SERVICIO_{i}}}}}", img)

        # Validar
        validacion = validar_completo(html)
        if validacion["valido"]:
            print(f"[PASO 2] Exito. HTML valido en intento {intento}.")
            return {"exito": True, "html": html, "error": None}

        print(f"[PASO 2] HTML invalido en intento {intento}. Reintentando...")
        time.sleep(TIEMPO_ESPERA)

    return {"exito": False, "html": None, "error": "No se pudo generar HTML valido."}