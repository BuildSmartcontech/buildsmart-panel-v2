# utils/web_editor_v2.py
# ============================================
# EDITOR DE WEBS - V6.0 (ENRUTADOR INTELIGENTE Y VISIÓN)
# ============================================

import os
import sys
import re
import json
import time
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.web_prompts import generar_prompt_edicion_estructurada
from utils.html_patcher import aplicar_cambios

try:
    from backend.gateway import gateway, analizar_imagen_gemini
except ImportError:
    try:
        from gateway import gateway, analizar_imagen_gemini
    except ImportError:
        gateway = None
        analizar_imagen_gemini = None

MAX_INTENTOS = 3
TIEMPO_ESPERA = 2

def extraer_mapa_anclas(html):
    if not html: return "HTML vacio"
    soup = BeautifulSoup(html, 'html.parser')
    anclas = []
    
    for sec in soup.find_all('section'):
        sec_id = sec.get('id', '')
        if sec_id:
            texto = sec.get_text(strip=True)[:50]
            anclas.append(f"- Sección [{sec_id}]: \"{texto}...\"")
            
    for img in soup.find_all('img'):
        data_img = img.get('data-img', '')
        if data_img:
            alt = img.get('alt', 'sin alt')
            titulo_tarjeta = ""
            parent = img.find_parent('div')
            if parent:
                h3 = parent.find(['h3', 'h4', 'h2'])
                if h3: titulo_tarjeta = h3.get_text(strip=True)
            
            contexto = f"título_tarjeta=\"{titulo_tarjeta}\"" if titulo_tarjeta else ""
            anclas.append(f"- Imagen [{data_img}]: alt=\"{alt}\", {contexto}, selector=\"img[data-img='{data_img}']\"")
            
    if soup.find('nav'): anclas.append("- Sección [nav]: Menú superior, selector=\"nav\"")
    if soup.find('footer'): anclas.append("- Sección [footer]: Pie de página, selector=\"footer\"")
        
    return "MAPA DE ANCLAS DE LA WEB:\n" + "\n".join(anclas) if anclas else "No se encontraron anclas."

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

def editar_web_v2(usuario_id, web_id, instruccion, contexto_negocio="", html_actual=None, foto_b64=None):
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

    # --- VISIÓN OCR CON GEMINI ---
    texto_extraido = ""
    if foto_b64 and analizar_imagen_gemini:
        print("[VISION] Extrayendo texto de la imagen subida...")
        prompt_ocr = "Extrae TODO el texto visible en esta imagen. Sé muy detallado, conserva títulos y viñetas. Responde SOLO con el texto extraído."
        texto_extraido = analizar_imagen_gemini(foto_b64, prompt_ocr, pedido_id=web_id)
        if texto_extraido:
            instruccion += f"\n\nINFORMACIÓN EXTRAÍDA DE LA IMAGEN:\n{texto_extraido}"

    mapa_anclas = extraer_mapa_anclas(html_actual)

    for intento in range(1, MAX_INTENTOS + 1):
        try:
            prompt = generar_prompt_edicion_estructurada(mapa_anclas, instruccion, contexto_negocio, tiene_foto=bool(foto_b64))
            sistema = "Eres un experto en manipulación de DOM. Devuelves SOLO JSON."
            
            # --- ENRUTADOR INTELIGENTE ---
            # Si hay foto o el prompt parece complejo ("crea", "tarjeta", "nueva"), usar Gemini.
            es_complejo = bool(foto_b64) or any(p in instruccion.lower() for p in ["crea", "tarjeta", "nueva", "html", "sección", "al lado"])
            
            if es_complejo:
                print(f"[IA] Usando Gemini Pro para tarea compleja...")
                respuesta = gateway.chat_con_gemini(prompt, sistema, pedido_id=web_id)
                fuente = "gemini"
            else:
                print(f"[IA] Usando IA rápida (Groq) para tarea simple...")
                respuesta, fuente = gateway.chat_inteligente(prompt, sistema, temperature=0.1, pedido_id=web_id)

            data = parsear_json_cambios(respuesta)
            if not data or "operaciones" not in data:
                time.sleep(TIEMPO_ESPERA)
                continue

            resultado_patcher = aplicar_cambios(html_actual, data["operaciones"], foto_b64)
            
            if not resultado_patcher["exito"]:
                return {"exito": False, "error": resultado_patcher["error"]}

            return {
                "exito": True,
                "html_nuevo": resultado_patcher["html_nuevo"],
                "cambios_aplicados": resultado_patcher.get("cambios_aplicados", 1),
                "error": None
            }
        except Exception as e:
            print(f"Error en intento {intento}: {e}")
            time.sleep(TIEMPO_ESPERA)

    return {"exito": False, "error": "La IA no pudo procesar la orden. Intenta ser más específico."}

def editar_y_guardar_v2(usuario_id, web_id, instruccion, contexto_negocio="", foto_b64=None):
    resultado = editar_web_v2(usuario_id, web_id, instruccion, contexto_negocio, foto_b64=foto_b64)
    if not resultado["exito"]:
        return resultado

    try:
        from utils.web_storage import guardar_en_archivos
        guardar_en_archivos(usuario_id, web_id, resultado["html_nuevo"])
    except Exception as e:
        print(f"[EDITOR] Error guardando en archivos: {e}")

    try:
        from utils.supabase_client import supabase
        if supabase:
            url = supabase.url + f"/rest/v1/paginas_web?id=eq.{web_id}"
            headers = supabase.headers.copy()
            data = {"html_generado": resultado["html_nuevo"]}
            import requests
            requests.patch(url, headers=headers, json=data, timeout=10)
            print(f"[EDITOR] HTML actualizado en Supabase para web_id {web_id}")
    except Exception as e:
        print(f"[EDITOR] Error guardando en Supabase: {e}")

    resultado["guardado"] = True
    return resultado