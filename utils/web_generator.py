# utils/web_generator.py
# ============================================
# GENERADOR DE WEBS - V10.0 (BEAUTIFULSOUP INJECTION)
# ============================================
# V10.0: Usa BeautifulSoup para forzar la inyeccion de imagenes y logo.
# ============================================

import os
import sys
import re
import time
import json
from bs4 import BeautifulSoup

try:
    import requests as _requests
    REQUESTS_DISPONIBLE = True
except ImportError:
    REQUESTS_DISPONIBLE = False

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.web_prompts_data import DIRECTOR_DE_ARTE_PROMPT, REGLAS_CSS_PREMIUM, REGLAS_FORMULARIO, REGLAS_SALIDA, construir_instrucciones_dinamicas
    from utils.web_validator import validar_completo, limpiar_html
except ImportError:
    from web_prompts_data import DIRECTOR_DE_ARTE_PROMPT, REGLAS_CSS_PREMIUM, REGLAS_FORMULARIO, REGLAS_SALIDA, construir_instrucciones_dinamicas
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

def generar_copy_estrategico(datos_negocio, modelo_ia):
    prompt = f"""
Eres un Director de Marketing Digital experto en ventas B2B.
Analiza el siguiente negocio:
- Nombre: {datos_negocio.get('nombre')}
- Sector: {datos_negocio.get('sector')}
- Descripcion: {datos_negocio.get('descripcion')}
- Publico: {datos_negocio.get('publico_objetivo')}

Redacta el Copy exacto para su pagina web premium.
Devuelve UNICAMENTE un JSON valido:
{{
  "headline": "Titulo impactante (max 10 palabras)",
  "subheadline": "Subtitulo persuasivo (max 25 palabras)",
  "servicios": [
    {{"titulo": "Servicio 1", "descripcion": "Texto persuasivo (20 palabras)"}},
    {{"titulo": "Servicio 2", "descripcion": "Texto persuasivo (20 palabras)"}},
    {{"titulo": "Servicio 3", "descripcion": "Texto persuasivo (20 palabras)"}}
  ],
  "sobre_nosotros": "Parrafo de 40 palabras sobre la vision del negocio.",
  "keywords_imagenes": ["keyword_ingles_1", "keyword_ingles_2"]
}}
"""
    sistema = "Eres un copywriter experto. Devuelves solo JSON."
    
    if OPENROUTER_DISPONIBLE:
        respuesta, _, error = consultar_openrouter(prompt, sistema, modelo=modelo_ia)
        if not error: return respuesta
            
    if gateway:
        respuesta, _ = gateway.chat_inteligente(prompt, sistema)
        return respuesta
    return None

def generar_html_programador(datos_negocio, copy, modelo_ia):
    instrucciones_dinamicas = construir_instrucciones_dinamicas(datos_negocio)
    
    prompt = f"""
{DIRECTOR_DE_ARTE_PROMPT}

=========================================================
GENERA LA PAGINA WEB COMPLETA
=========================================================

## COPY EXACTO (NO INVENTES TEXTO, USA ESTE)
- Headline Hero: {copy.get('headline')}
- Subheadline Hero: {copy.get('subheadline')}
- Servicios:
  1. {copy.get('servicios', [{}])[0].get('titulo')}: {copy.get('servicios', [{}])[0].get('descripcion')}
  2. {copy.get('servicios', [{}, {}])[1].get('titulo')}: {copy.get('servicios', [{}, {}])[1].get('descripcion')}
  3. {copy.get('servicios', [{}, {}, {}])[2].get('titulo')}: {copy.get('servicios', [{}, {}, {}])[2].get('descripcion')}
- Sobre Nosotros: {copy.get('sobre_nosotros')}

## INSTRUCCIONES DINAMICAS
{instrucciones_dinamicas}

## REGLAS DE DISENO
{REGLAS_CSS_PREMIUM}

{REGLAS_FORMULARIO}
{REGLAS_SALIDA}
"""
    sistema = "Eres un programador Frontend Senior. Devuelves solo HTML. Usa el CSS exacto que se te da."
    
    if OPENROUTER_DISPONIBLE:
        respuesta, _, error = consultar_openrouter(prompt, sistema, modelo=modelo_ia)
        if not error: return respuesta
            
    if gateway:
        respuesta, _ = gateway.chat_inteligente(prompt, sistema)
        return respuesta
    return None

def inyectar_elementos_criticos(html, imagenes, logo_b64):
    """
    Usa BeautifulSoup para forzar la inyeccion del logo, imagenes y formulario.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # 1. LOGO EN EL NAV
    if logo_b64:
        nav = soup.find('nav')
        if nav:
            # Buscamos si ya hay un <a> para meter la imagen dentro
            primer_a = nav.find('a')
            logo_img = soup.new_tag('img', src=logo_b64, alt="Logo")
            logo_img['style'] = "height:40px; width:auto; margin-right:10px;"
            
            if primer_a:
                # Si el <a> ya tiene texto (ej. "SAMU IA"), lo reemplazamos por la imagen
                primer_a.clear()
                primer_a.append(logo_img)
            else:
                # Si no hay <a>, lo insertamos al inicio del nav
                nav.insert(0, logo_img)

    # 2. IMAGEN HERO (Buscamos la seccion con clase hero o el primer h1)
    hero_url = imagenes.get("hero")
    if hero_url:
        hero_section = soup.find(class_=re.compile('hero', re.I))
        if not hero_section:
            # Si la IA no puso clase "hero", buscamos el h1 principal y subimos a su padre
            h1 = soup.find('h1')
            if h1:
                hero_section = h1.parent

        if hero_section:
            # Si no hay una imagen en el hero, la insertamos
            if not hero_section.find('img'):
                img_tag = soup.new_tag('img', src=hero_url, alt="Hero Image")
                img_tag['style'] = "width:100%; max-height:400px; object-fit:cover; border-radius:20px; margin-top:20px;"
                hero_section.append(img_tag)

    # 3. IMAGENES EN SERVICIOS (Buscamos tarjetas)
    servicios_urls = imagenes.get("servicios", [])
    if servicios_urls:
        # La IA suele usar "card", "service", "grid-item" para las tarjetas
        cards = soup.find_all(class_=re.compile('card|service|grid-item', re.I))
        for i, card in enumerate(cards[:len(servicios_urls)]):
            if not card.find('img'):
                img_tag = soup.new_tag('img', src=servicios_urls[i], alt=f"Servicio {i+1}")
                img_tag['style'] = "width:100%; height:200px; object-fit:cover; border-radius:12px; margin-bottom:15px;"
                card.insert(0, img_tag)

    # 4. FORMULARIO DE CONTACTO
    form_section = soup.find(id='contacto') or soup.find(class_=re.compile('contact', re.I))
    if form_section:
        # Si el marcador {{FORMULARIO}} sigue ahí, o no hay un <form> real
        if "{{FORMULARIO}}" in html or not form_section.find('form'):
            form_html = """
            <form action="/submit_lead" method="POST" style="display:flex; flex-direction:column; gap:15px; max-width:500px; margin:0 auto;">
                <input type="text" name="nombre" placeholder="Nombre completo" required style="padding:15px; border-radius:8px; border:1px solid #333; background:#1a1a1a; color:white;">
                <input type="email" name="email" placeholder="Correo electronico" required style="padding:15px; border-radius:8px; border:1px solid #333; background:#1a1a1a; color:white;">
                <textarea name="mensaje" placeholder="En que podemos ayudarte?" required style="padding:15px; border-radius:8px; border:1px solid #333; background:#1a1a1a; color:white; min-height:120px;"></textarea>
                <button type="submit" class="btn" style="padding:15px; border-radius:8px; border:none; background:#00d4ff; color:black; font-weight:bold; cursor:pointer;">Enviar Mensaje</button>
            </form>
            """
            form_soup = BeautifulSoup(form_html, 'html.parser')
            # Reemplazamos el texto {{FORMULARIO}} o inyectamos al final
            if "{{FORMULARIO}}" in html:
                html = html.replace("{{FORMULARIO}}", str(form_soup))
                soup = BeautifulSoup(html, 'html.parser')
            else:
                form_section.append(form_soup)

    return str(soup)

def generar_web(datos_negocio, opciones=None, modelo_ia="nvidia/nemotron-3-super-120b"):
    print("=" * 60)
    print("GENERANDO WEB - V10.0 (BeautifulSoup)")
    print("=" * 60)

    if not gateway and not OPENROUTER_DISPONIBLE:
        return {"exito": False, "html": None, "error": "Gateway no disponible"}

    copy_raw = generar_copy_estrategico(datos_negocio, modelo_ia)
    if not copy_raw:
        return {"exito": False, "html": None, "error": "Fallo el copy."}
    try:
        copy_str = copy_raw.replace("```json", "").replace("```", "").strip()
        start = copy_str.find('{')
        end = copy_str.rfind('}') + 1
        copy = json.loads(copy_str[start:end])
    except Exception:
        return {"exito": False, "html": None, "error": "JSON invalido."}

    imagenes = {"hero": None, "servicios": []}
    logo_b64 = datos_negocio.get("logo_b64")
    fotos_b64 = datos_negocio.get("fotos_b64", [])
    
    if fotos_b64:
        imagenes["hero"] = fotos_b64[0] if len(fotos_b64) > 0 else None
        imagenes["servicios"] = fotos_b64[1:4]
    elif IMAGENES_DISPONIBLES:
        keywords = copy.get("keywords_imagenes", ["business"])
        negocio_info = {"nombre": datos_negocio.get("nombre"), "sector": " ".join(keywords), "descripcion": datos_negocio.get("descripcion")}
        poll = obtener_urls_imagenes_negocio(negocio_info, cantidad=4)
        if poll:
            imagenes["hero"] = poll[0]["url_regular"]
            imagenes["servicios"] = [p["url_regular"] for p in poll[1:4]]

    for intento in range(1, MAX_INTENTOS + 1):
        html_raw = generar_html_programador(datos_negocio, copy, modelo_ia)
        if not html_raw:
            time.sleep(TIEMPO_ESPERA)
            continue

        html = limpiar_html(html_raw)
        html = inyectar_elementos_criticos(html, imagenes, logo_b64)

        validacion = validar_completo(html)
        if validacion["valido"]:
            return {"exito": True, "html": html, "error": None}

        time.sleep(TIEMPO_ESPERA)

    return {"exito": False, "html": None, "error": "No se pudo generar HTML valido."}
