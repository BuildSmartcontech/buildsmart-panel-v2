# utils/web_generator.py
# ============================================
# GENERADOR DE WEBS CON IA - V5.0 (OPENROUTER)
# ============================================
# V5.0: Usa OpenRouter (Claude/GPT-4o) para respetar el diseno premium
#       Fallback automatico a Groq si OpenRouter falla.
# ============================================

import os
import sys
import re
import time
import datetime

try:
    import requests as _requests
    REQUESTS_DISPONIBLE = True
except ImportError:
    REQUESTS_DISPONIBLE = False

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.web_prompts import generar_prompt_web, generar_prompt_resumen, generar_prompt_seo
    from utils.web_templates import renderizar_template
    from utils.web_validator import validar_completo, limpiar_html, resumen_validacion
except ImportError:
    from web_prompts import generar_prompt_web, generar_prompt_resumen, generar_prompt_seo
    from web_templates import renderizar_template
    from web_validator import validar_completo, limpiar_html, resumen_validacion

try:
    from backend.gateway import gateway
except ImportError:
    try:
        from gateway import gateway
    except ImportError:
        gateway = None

try:
    from utils.business_detector import analizar_negocio
    ANALISIS_DISPONIBLE = True
except ImportError:
    try:
        from business_detector import analizar_negocio
        ANALISIS_DISPONIBLE = True
    except ImportError:
        ANALISIS_DISPONIBLE = False

try:
    from utils.image_fetcher import obtener_urls_imagenes_negocio, normalizar_sector, buscar_imagenes_sector
    IMAGENES_DISPONIBLES = True
except ImportError:
    try:
        from image_fetcher import obtener_urls_imagenes_negocio, normalizar_sector, buscar_imagenes_sector
        IMAGENES_DISPONIBLES = True
    except ImportError:
        IMAGENES_DISPONIBLES = False

# Importar OpenRouter
try:
    from utils.openrouter_manager import consultar_openrouter
    OPENROUTER_DISPONIBLE = True
except ImportError:
    OPENROUTER_DISPONIBLE = False

MAX_INTENTOS = 3
TIEMPO_ESPERA = 2
SECTORES_GENERICOS = ["general", "negocio general", "default", "otros", "varios", ""]

def _es_sector_generico(sector):
    if not sector: return True
    return sector.lower().strip() in SECTORES_GENERICOS

def decidir_sector_para_imagenes(sector_original, sector_detectado):
    if not _es_sector_generico(sector_original): return sector_original
    if sector_detectado and not _es_sector_generico(sector_detectado): return sector_detectado
    return "General"

def _precalentar_imagenes(urls, timeout=45):
    if not REQUESTS_DISPONIBLE or not urls: return 0
    ok = 0
    for url in urls:
        try:
            r = _requests.get(url, timeout=timeout, stream=True)
            if r.status_code == 200:
                _ = r.raw.read(1024)
                ok += 1
            r.close()
        except Exception: pass
    return ok

def obtener_imagenes_para_web(sector, cantidad_servicios=4, texto_negocio="", negocio_info=None, precalentar=True):
    if not IMAGENES_DISPONIBLES: return {"hero": None, "servicios": []}
    info = negocio_info or {}
    if not info.get("sector"): info["sector"] = sector
    if not info.get("descripcion"): info["descripcion"] = texto_negocio

    urls_data = obtener_urls_imagenes_negocio(info, cantidad=cantidad_servicios + 1)
    if not urls_data: return {"hero": None, "servicios": []}

    resultado = {"hero": urls_data[0]["url_regular"], "servicios": [u["url_regular"] for u in urls_data[1:cantidad_servicios + 1]], "hero_prompt": urls_data[0]["descripcion"], "fuente": "pollinations"}
    if precalentar:
        todas_urls = [resultado["hero"]] + resultado["servicios"]
        _precalentar_imagenes([u for u in todas_urls if u])
    return resultado

def inyectar_imagenes_en_html(html, imagenes):
    if not imagenes: return html
    hero = imagenes.get("hero")
    servicios = imagenes.get("servicios", [])
    if not hero and not servicios: return html

    html_modificado = html
    contador = 0

    if hero:
        marcadores_hero = ["{{HERO_IMAGE}}", "{{IMAGEN_HERO}}", "{{HERO}}", "{{IMAGEN_PRINCIPAL}}", "{{BANNER}}"]
        for marcador in marcadores_hero:
            if marcador in html_modificado:
                html_modificado = html_modificado.replace(marcador, hero)
                contador += 1
        if contador == 0:
            html_modificado = inyectar_hero_automatico(html_modificado, hero)

    if servicios:
        variantes = ["SERVICIO", "SERVICIOS", "PRODUCTO", "PRODUCTOS", "ARTICULO", "ARTICULOS", "ITEM", "ITEMS", "IMAGEN", "IMAGENES", "PROYECTO", "PROYECTOS", "GALERIA", "FOTO", "FOTOS", "CARD", "CARDS"]
        for i, url in enumerate(servicios, 1):
            for variante in variantes:
                marcadores = ["{{" + variante + "_" + str(i) + "}}", "{{IMAGEN_" + variante + "_" + str(i) + "}}"]
                for marcador in marcadores:
                    if marcador in html_modificado:
                        html_modificado = html_modificado.replace(marcador, url)
                        contador += 1

        patron_generico = r'(<img[^>]*src=")\{\{[A-Z_0-9]+\}\}(")'
        matches = list(re.finditer(patron_generico, html_modificado))
        for i, match in enumerate(matches):
            if i < len(servicios):
                reemplazo = match.group(1) + servicios[i] + match.group(2)
                html_modificado = html_modificado.replace(match.group(0), reemplazo, 1)
                contador += 1

    return html_modificado

def inyectar_hero_automatico(html, hero_url):
    patron_hero = r'<section[^>]*class="[^"]*hero[^"]*"[^>]*>'
    match = re.search(patron_hero, html, re.IGNORECASE)
    if match:
        estilo = ' style="background-image: url(\'' + hero_url + '\'); background-size: cover; background-position: center; position: relative;"'
        nuevo_tag = match.group(0).replace(">", estilo + ">")
        return html.replace(match.group(0), nuevo_tag, 1)
    return html

def generar_web(datos_negocio, opciones=None, usar_template=True, con_imagenes=True, modelo_ia="openrouter/free"):
    print("=" * 60)
    print("GENERANDO WEB CON IA - V5.0 (OPENROUTER)")
    print("=" * 60)

    if gateway is None and not OPENROUTER_DISPONIBLE:
        return {"exito": False, "html": None, "intentos": 0, "validacion": None, "sector_detectado": None, "imagenes_usadas": None, "error": "Gateway no disponible"}

    sector_detectado = None
    recomendaciones = None

    if ANALISIS_DISPONIBLE:
        texto_analisis = datos_negocio.get("descripcion", "") + " " + datos_negocio.get("sector", "") + " " + datos_negocio.get("nombre", "")
        analisis = analizar_negocio(texto_analisis)
        sector_detectado = analisis.get("sector")
        if analisis.get("confianza", 0) >= 0.5: recomendaciones = analisis

    nombre = datos_negocio.get("nombre", "Mi Negocio")
    sector_original = datos_negocio.get("sector", "")
    descripcion = datos_negocio.get("descripcion", "Descripcion del negocio")
    publico = datos_negocio.get("publico_objetivo", "")
    diferenciadores = datos_negocio.get("diferenciadores", "")
    colores = datos_negocio.get("colores", "#0B0C14, #14B8A6")

    direccion = datos_negocio.get("direccion", "")
    ciudad = datos_negocio.get("ciudad", "")
    pais = datos_negocio.get("pais", "")
    horarios = datos_negocio.get("horarios", "")
    instagram = datos_negocio.get("instagram", "")
    facebook = datos_negocio.get("facebook", "")
    tiktok = datos_negocio.get("tiktok", "")
    anio_fundacion = datos_negocio.get("anio_fundacion", "")
    email_contacto = datos_negocio.get("email_contacto", "")
    whatsapp_negocio = datos_negocio.get("whatsapp_negocio", "")

    sector_para_imagenes = decidir_sector_para_imagenes(sector_original, sector_detectado)
    texto_negocio = (nombre + " " + descripcion + " " + diferenciadores).strip()

    if opciones is None:
        if recomendaciones:
            opciones = {"tipo_pagina": recomendaciones.get("tipo_pagina", "Landing Page"), "diseno": recomendaciones.get("diseno", "Moderno"), "tono": recomendaciones.get("tono", "Profesional"), "secciones": recomendaciones.get("secciones"), "logica": "Formulario de contacto", "funcionalidades": ["SEO optimizado", "Animaciones"]}
        else:
            opciones = {"tipo_pagina": "Landing Page", "diseno": "Moderno", "tono": "Profesional", "secciones": ["Hero", "Servicios", "Sobre Nosotros", "Contacto"], "logica": "Formulario de contacto", "funcionalidades": ["SEO optimizado", "Animaciones"]}

    imagenes = None
    if con_imagenes and IMAGENES_DISPONIBLES:
        negocio_info = {"nombre": nombre, "sector": sector_para_imagenes, "descripcion": descripcion}
        imagenes = obtener_imagenes_para_web(sector_para_imagenes, texto_negocio=texto_negocio, negocio_info=negocio_info, precalentar=True)

    for intento in range(1, MAX_INTENTOS + 1):
        try:
            prompt = generar_prompt_web(
                nombre_negocio=nombre, sector=sector_original or sector_detectado or "general", descripcion=descripcion, publico_objetivo=publico, diferenciadores=diferenciadores, tono=opciones.get("tono", "Profesional"), colores=colores, tipo_pagina=opciones.get("tipo_pagina", "Landing Page"), diseno=opciones.get("diseno", "Moderno"), secciones=opciones.get("secciones"), logica=opciones.get("logica", "Estatica"), funcionalidades=opciones.get("funcionalidades"), direccion=direccion, ciudad=ciudad, pais=pais, horarios=horarios, instagram=instagram, facebook=facebook, tiktok=tiktok, anio_fundacion=anio_fundacion, email_contacto=email_contacto, whatsapp_negocio=whatsapp_negocio,
            )

            sistema = "Eres un disenador web profesional. Genera codigo HTML/CSS limpio y moderno."
            
            # INTENTAR CON OPENROUTER PRIMERO
            respuesta = None
            if OPENROUTER_DISPONIBLE:
                print(f"[OPENROUTER] Intentando con modelo: {modelo_ia}")
                respuesta_ia, modelo_usado, error_or = consultar_openrouter(prompt, sistema, modelo=modelo_ia)
                if error_or:
                    print(f"[OPENROUTER] Error: {error_or}")
                else:
                    respuesta = respuesta_ia
                    print(f"[OPENROUTER] Exito con: {modelo_usado}")

            # FALLBACK A GROQ SI OPENROUTER FALLA
            if not respuesta and gateway:
                print("[FALLBACK] Usando Groq/Gateway...")
                respuesta, fuente = gateway.chat_inteligente(prompt, sistema)
                print(f"[FALLBACK] Exito con: {fuente}")

            if not respuesta:
                print("No se pudo obtener respuesta de ninguna IA.")
                time.sleep(TIEMPO_ESPERA)
                continue

            html = limpiar_html(respuesta)

            if imagenes and (imagenes.get("hero") or imagenes.get("servicios")):
                html = inyectar_imagenes_en_html(html, imagenes)

            validacion = validar_completo(html)

            if validacion["valido"]:
                return {"exito": True, "html": html, "intentos": intento, "validacion": validacion, "fuente": modelo_ia, "sector_detectado": sector_detectado, "sector_usado_imagenes": sector_para_imagenes, "imagenes_usadas": imagenes, "error": None}

            print("HTML invalido. Reintentando en " + str(TIEMPO_ESPERA) + "s...")
            time.sleep(TIEMPO_ESPERA)
        except Exception as e:
            print("Error en intento " + str(intento) + ": " + str(e))
            time.sleep(TIEMPO_ESPERA)

    return {"exito": False, "html": None, "intentos": MAX_INTENTOS, "validacion": None, "fuente": None, "sector_detectado": sector_detectado, "imagenes_usadas": imagenes, "error": "No se pudo generar HTML valido"}

def generar_resumen(html):
    if gateway is None: return "Gateway no disponible"
    try:
        prompt = generar_prompt_resumen(html)
        sistema = "Eres un experto en marketing digital."
        respuesta, fuente = gateway.chat_rapido(prompt, sistema)
        return limpiar_html(respuesta)
    except Exception as e: return "Error: " + str(e)

def generar_seo(nombre_negocio, sector, descripcion):
    if gateway is None: return {}
    try:
        prompt = generar_prompt_seo(nombre_negocio, sector, descripcion)
        sistema = "Eres un experto en SEO."
        respuesta, fuente = gateway.chat_rapido(prompt, sistema)
        import json
        try: return json.loads(respuesta)
        except Exception: return {}
    except Exception as e: return {}