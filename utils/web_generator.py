# utils/web_generator.py
# ============================================
# GENERADOR DE WEBS - V18.1 (INYECCIÓN FORZADA DE HERO)
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
    # 1. REEMPLAZO DE MARCADORES
    hero_url = imagenes.get("hero")
    servicios_urls = imagenes.get("servicios", [])
    
    if hero_url:
        html = html.replace("{{HERO_IMAGE}}", hero_url)
    if len(servicios_urls) > 0:
        html = html.replace("{{SERVICIO_1}}", servicios_urls[0])
    if len(servicios_urls) > 1:
        html = html.replace("{{SERVICIO_2}}", servicios_urls[1])
    if len(servicios_urls) > 2:
        html = html.replace("{{SERVICIO_3}}", servicios_urls[2])

    soup = BeautifulSoup(html, 'html.parser')

    # 2. LOGO
    if logo_b64:
        print("[INYECTOR] Inyectando logo...")
        primer_enlace = soup.find('a')
        header = soup.find('header') or soup.find('nav')
        
        logo_img = soup.new_tag('img', src=logo_b64, alt="Logo")
        logo_img['style'] = "height:60px; width:auto; object-fit:contain; max-width:220px; margin-right:20px;"
        
        if header:
            header.insert(0, logo_img)
        elif primer_enlace:
            primer_enlace.clear()
            primer_enlace.append(logo_img)
        else:
            body = soup.find('body')
            if body:
                body.insert(0, logo_img)

    # 3. HERO IMAGE (INYECCIÓN FORZADA Y LIMPIEZA DE FANTASMAS)
    if hero_url and "{{HERO_IMAGE}}" not in html:
        print("[INYECTOR] Forzando inyección de imagen Hero...")
        h1 = soup.find('h1')
        container = h1.parent if h1 else soup.find('section')
        
        if container:
            # ELIMINAMOS cualquier imagen invisible o rota que haya puesto la IA
            for img in container.find_all('img'):
                img.decompose()
                
            img_tag = soup.new_tag('img', src=hero_url, alt="Hero Image")
            # Forzamos estilos para que la imagen se vea bien y no se deforme
            img_tag['style'] = "width:100%; max-width:1000px; height:auto; max-height:600px; object-fit:cover; border-radius:24px; margin:40px auto 0; display:block; box-shadow: 0 20px 40px rgba(0,0,0,0.4);"
            container.append(img_tag)

    # 4. IMAGENES EN SERVICIOS
    if servicios_urls and "{{SERVICIO_1}}" not in html:
        print(f"[INYECTOR] Buscando tarjetas para inyectar {len(servicios_urls)} imagenes...")
        tarjetas = []
        for div in soup.find_all('div'):
            if (div.find('h3') or div.find('h4')) and not div.find('img') and len(div.get_text(strip=True)) < 350:
                tarjetas.append(div)

        for i, url in enumerate(servicios_urls):
            if i >= len(tarjetas): break
            tarjeta = tarjetas[i]
            print(f"[INYECTOR] Inyectando imagen en tarjeta {i+1}...")
            
            img_tag = soup.new_tag('img', src=url, alt=f"Servicio {i+1}")
            img_tag['style'] = "width:100%; height:220px; object-fit:cover; border-radius:16px; margin-bottom:24px; display:block;"
            tarjeta.insert(0, img_tag)
            
            tarjeta['style'] = "background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 24px; padding: 30px; display: flex; flex-direction: column; height: 100%;"

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
    print("GENERANDO WEB - V18.1")
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
    
    faltan_servicios = 3 - len(imagenes["servicios"])
    if faltan_servicios > 0 or not imagenes["hero"]:
        print(f"[DIAGNOSTICO] Faltan imágenes. Buscando {faltan_servicios} en la IA...")
        keywords = copy.get("keywords_imagenes", ["business"])
        negocio_info = {"nombre": nombre_negocio, "sector": " ".join(keywords), "descripcion": datos_negocio.get("descripcion")}
        poll = obtener_urls_imagenes_negocio(negocio_info, cantidad=4)
        
        if poll:
            if not imagenes["hero"] and len(poll) > 0:
                imagenes["hero"] = poll[0]["url_regular"]
            
            imagenes_poll = [p["url_regular"] for p in poll[1:4]]
            for img in imagenes_poll:
                if len(imagenes["servicios"]) < 3:
                    imagenes["servicios"].append(img)

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