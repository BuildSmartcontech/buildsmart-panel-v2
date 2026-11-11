# utils/web_generator.py
# ============================================
# GENERADOR DE WEBS - V11.0 (INYECCION MAESTRA)
# ============================================
# V11.0: Prompts de imagen abstractos (evita marcas) e inyeccion de logo forzada.
# ============================================

import os
import sys
import re
import time
import json
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.web_prompts_data import DIRECTOR_DE_ARTE_PROMPT, REGLAS_CSS_PREMIUM, REGLAS_FORMULARIO, REGLAS_SALIDA, construir_instrucciones_dinamicas
    from utils.web_validator import validar_completo, limpiar_html
    from utils.image_fetcher import obtener_urls_imagenes_negocio
    from utils.openrouter_manager import consultar_openrouter
except ImportError:
    from web_prompts_data import DIRECTOR_DE_ARTE_PROMPT, REGLAS_CSS_PREMIUM, REGLAS_FORMULARIO, REGLAS_SALIDA, construir_instrucciones_dinamicas
    from web_validator import validar_completo, limpiar_html
    from image_fetcher import obtener_urls_imagenes_negocio
    from openrouter_manager import consultar_openrouter

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
  "keywords_imagenes": ["keyword_visual_1", "keyword_visual_2", "keyword_visual_3"]
}}

## REGLA CRITICA PARA LAS KEYWORDS:
Debes generar 3 palabras clave en INGLES para buscar imagenes fotograficas.
PROHIBIDO usar nombres de marcas (ej. WhatsApp, Facebook, Google).
PROHIBIDO usar jerga tecnica (ej. CRM, HTML, SaaS).
USA conceptos visuales profesionales (ej. "modern office team", "business meeting", "customer service handshake", "technology dashboard").
"""
    sistema = "Eres un copywriter experto. Devuelves solo JSON."
    
    if OPENROUTER_DISPONIBLE := True:
        try:
            respuesta, _, error = consultar_openrouter(prompt, sistema, modelo=modelo_ia)
            if not error: return respuesta
        except Exception: pass
    
    from backend.gateway import gateway
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
    
    if OPENROUTER_DISPONIBLE := True:
        try:
            respuesta, _, error = consultar_openrouter(prompt, sistema, modelo=modelo_ia)
            if not error: return respuesta
        except Exception: pass
    
    from backend.gateway import gateway
    if gateway:
        respuesta, _ = gateway.chat_inteligente(prompt, sistema)
        return respuesta
    return None

def inyectar_elementos_criticos(html, imagenes, logo_b64, nombre_negocio):
    soup = BeautifulSoup(html, 'html.parser')

    # 1. LOGO EN EL NAV (A PRUEBA DE BALAS)
    if logo_b64:
        nav = soup.find('nav') or soup.find('header')
        if nav:
            # Buscamos cualquier elemento que parezca el logo (una 'a', un 'div' o un 'h1' con el nombre)
            logo_element = nav.find('a', string=re.compile(nombre_negocio, re.I))
            if not logo_element:
                logo_element = nav.find('div', class_=re.compile('logo|brand', re.I))
            if not logo_element:
                logo_element = nav.find('h1') or nav.find('span')
                
            logo_img = soup.new_tag('img', src=logo_b64, alt="Logo")
            logo_img['style'] = "height:45px; width:auto; object-fit:contain;"
            
            if logo_element:
                logo_element.clear()
                logo_element.append(logo_img)
            else:
                nav.insert(0, logo_img)

    # 2. IMAGEN HERO
    hero_url = imagenes.get("hero")
    if hero_url:
        hero_section = soup.find(class_=re.compile('hero', re.I)) or soup.find('h1')
        if hero_section:
            parent = hero_section if hero_section.name != 'h1' else hero_section.parent
            if parent and not parent.find('img'):
                img_tag = soup.new_tag('img', src=hero_url, alt="Hero Image")
                img_tag['style'] = "width:100%; max-height:400px; object-fit:cover; border-radius:20px; margin-top:30px;"
                parent.append(img_tag)

    # 3. IMAGENES EN SERVICIOS (Forzamos que las 3 tarjetas tengan imagen)
    servicios_urls = imagenes.get("servicios", [])
    if servicios_urls:
        cards = soup.find_all(class_=re.compile('card|service|grid-item', re.I))
        for i, card in enumerate(cards[:len(servicios_urls)]):
            if not card.find('img'):
                img_tag = soup.new_tag('img', src=servicios_urls[i], alt=f"Servicio {i+1}")
                img_tag['style'] = "width:100%; height:220px; object-fit:cover; border-radius:12px; margin-bottom:20px;"
                card.insert(0, img_tag)

    # 4. FORMULARIO
    form_section = soup.find(id='contacto') or soup.find(class_=re.compile('contact', re.I))
    if form_section:
        if "{{FORMULARIO}}" in html or not form_section.find('form'):
            form_html = """
            <form action="/submit_lead" method="POST" style="display:flex; flex-direction:column; gap:15px; max-width:500px; margin:0 auto;">
                <input type="text" name="nombre" placeholder="Nombre completo" required style="padding:15px; border-radius:8px; border:1px solid #333; background:#1a1a1a; color:white;">
                <input type="email" name="email" placeholder="Correo electronico" required style="padding:15px; border-radius:8px; border:1px solid #333; background:#1a1a1a; color:white;">
                <textarea name="mensaje" placeholder="En que podemos ayudarte?" required style="padding:15px; border-radius:8px; border:1px solid #333; background:#1a1a1a; color:white; min-height:120px;"></textarea>
                <button type="submit" class="btn" style="padding:15px; border-radius:8px; border:none; background:#14B8A6; color:black; font-weight:bold; cursor:pointer;">Enviar Mensaje</button>
            </form>
            """
            form_soup = BeautifulSoup(form_html, 'html.parser')
            if "{{FORMULARIO}}" in html:
                html = html.replace("{{FORMULARIO}}", str(form_soup))
                soup = BeautifulSoup(html, 'html.parser')
            else:
                form_section.append(form_soup)

    return str(soup)

def generar_web(datos_negocio, opciones=None, modelo_ia="nvidia/nemotron-3-super-120b"):
    print("=" * 60)
    print("GENERANDO WEB - V11.0 (Inyeccion Maestra)")
    print("=" * 60)

    copy_raw = generar_copy_estrategico(datos_negocio, modelo_ia)
    if not copy_raw: return {"exito": False, "html": None, "error": "Fallo el copy."}
    try:
        copy_str = copy_raw.replace("```json", "").replace("```", "").strip()
        start = copy_str.find('{'); end = copy_str.rfind('}') + 1
        copy = json.loads(copy_str[start:end])
    except Exception:
        return {"exito": False, "html": None, "error": "JSON invalido."}

    imagenes = {"hero": None, "servicios": []}
    logo_b64 = datos_negocio.get("logo_b64")
    fotos_b64 = datos_negocio.get("fotos_b64", [])
    nombre_negocio = datos_negocio.get("nombre", "Mi Negocio")
    
    if fotos_b64:
        imagenes["hero"] = fotos_b64[0] if len(fotos_b64) > 0 else None
        imagenes["servicios"] = fotos_b64[1:4]
    else:
        keywords = copy.get("keywords_imagenes", ["business"])
        negocio_info = {"nombre": nombre_negocio, "sector": " ".join(keywords), "descripcion": datos_negocio.get("descripcion")}
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
        html = inyectar_elementos_criticos(html, imagenes, logo_b64, nombre_negocio)

        validacion = validar_completo(html)
        if validacion["valido"]:
            return {"exito": True, "html": html, "error": None}

        time.sleep(TIEMPO_ESPERA)

    return {"exito": False, "html": None, "error": "No se pudo generar HTML valido."}