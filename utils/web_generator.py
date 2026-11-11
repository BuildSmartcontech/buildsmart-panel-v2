# utils/web_generator.py
# ============================================
# GENERADOR DE WEBS - V16.0 (INYECCION ESTRUCTURAL)
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
  "sobre_nosotros": "Parrafo de 40 palabras.",
  "keywords_imagenes": ["keyword_1", "keyword_2", "keyword_3"]
}}
"""
    sistema = "Eres un copywriter experto. Devuelves solo JSON."
    
    try:
        respuesta, _, error = consultar_openrouter(prompt, sistema, modelo=modelo_ia)
        if not error and respuesta: return respuesta
    except Exception: pass
    
    try:
        from backend.gateway import gateway
        if gateway:
            respuesta, _ = gateway.chat_inteligente(prompt, sistema)
            return respuesta
    except Exception: pass
    return None

def generar_html_programador(datos_negocio, copy, modelo_ia):
    instrucciones_dinamicas = construir_instrucciones_dinamicas(datos_negocio)
    
    prompt = f"""
{DIRECTOR_DE_ARTE_PROMPT}

## COPY EXACTO
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
    sistema = "Eres un programador Frontend Senior. Devuelves solo HTML."
    
    try:
        respuesta, _, error = consultar_openrouter(prompt, sistema, modelo=modelo_ia)
        if not error and respuesta: return respuesta
    except Exception: pass
    
    try:
        from backend.gateway import gateway
        if gateway:
            respuesta, _ = gateway.chat_inteligente(prompt, sistema)
            return respuesta
    except Exception: pass
    return None

def inyectar_elementos_criticos(html, imagenes, logo_b64, nombre_negocio):
    soup = BeautifulSoup(html, 'html.parser')

    # 1. LOGO
    if logo_b64:
        print("[INYECTOR] Inyectando logo...")
        nav = soup.find('nav') or soup.find('header')
        if nav:
            logo_el = nav.find('a') or nav.find('div', class_=re.compile('logo|brand', re.I))
            if logo_el:
                logo_el.clear()
                logo_img = soup.new_tag('img', src=logo_b64, alt="Logo")
                logo_img['style'] = "height:45px; width:auto; object-fit:contain;"
                logo_el.append(logo_img)
            else:
                logo_img = soup.new_tag('img', src=logo_b64, alt="Logo")
                logo_img['style'] = "height:45px; width:auto; object-fit:contain; margin-right:20px;"
                nav.insert(0, logo_img)

    # 2. HERO IMAGE
    hero_url = imagenes.get("hero")
    if hero_url:
        print("[INYECTOR] Inyectando imagen Hero...")
        h1 = soup.find('h1')
        if h1:
            parent = h1.parent
            if not parent.find('img'):
                img_tag = soup.new_tag('img', src=hero_url, alt="Hero Image")
                img_tag['style'] = "width:100%; max-height:500px; object-fit:cover; border-radius:20px; margin-top:30px; display:block;"
                parent.append(img_tag)

    # 3. IMAGENES EN SERVICIOS (Búsqueda Estructural)
    servicios_urls = imagenes.get("servicios", [])
    if servicios_urls:
        print(f"[INYECTOR] Buscando tarjetas para inyectar {len(servicios_urls)} imagenes...")
        tarjetas = soup.find_all('div', recursive=True)
        tarjetas_validas = []
        
        for div in tarjetas:
            if (div.find('h3') or div.find('h4')) and not div.find('img'):
                if len(div.get_text(strip=True)) < 300:
                    tarjetas_validas.append(div)

        for i, url in enumerate(servicios_urls):
            if i >= len(tarjetas_validas): break
            tarjeta = tarjetas_validas[i]
            print(f"[INYECTOR] Inyectando imagen en tarjeta {i+1}...")
            
            img_tag = soup.new_tag('img', src=url, alt=f"Servicio {i+1}")
            img_tag['style'] = "width:100%; height:220px; object-fit:cover; border-radius:12px; margin-bottom:20px; display:block;"
            tarjeta.insert(0, img_tag)
            
            tarjeta['style'] = "background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 30px; display: flex; flex-direction: column; height: 100%;"

    # 4. BOTONES
    for a_tag in soup.find_all('a'):
        texto = a_tag.text.lower()
        if "comienza" in texto or "saber" in texto or "contacto" in texto or "servicio" in texto:
            a_tag['class'] = a_tag.get('class', []) + ['btn']
            a_tag['style'] = "display:inline-block; padding:16px 36px; background:#14B8A6; color:#0B0C14; font-weight:700; border-radius:999px; text-decoration:none;"

    # 5. FORMULARIO
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
    print("GENERANDO WEB - V16.0 (Inyeccion Estructural)")
    print("=" * 60)

    logo_b64 = datos_negocio.get("logo_b64")
    print(f"[DIAGNOSTICO] Logo en datos_negocio: {'SI' if logo_b64 else 'NO'}")

    copy_raw = generar_copy_estrategico(datos_negocio, modelo_ia)
    if not copy_raw: return {"exito": False, "html": None, "error": "Fallo el copy."}
    try:
        copy_str = copy_raw.replace("```json", "").replace("```", "").strip()
        start = copy_str.find('{'); end = copy_str.rfind('}') + 1
        copy = json.loads(copy_str[start:end])
    except Exception:
        return {"exito": False, "html": None, "error": "JSON invalido."}

    imagenes = {"hero": None, "servicios": []}
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

        if validar_completo(html)["valido"]:
            return {"exito": True, "html": html, "error": None}

        time.sleep(TIEMPO_ESPERA)

    return {"exito": False, "html": None, "error": "No se pudo generar HTML valido."}