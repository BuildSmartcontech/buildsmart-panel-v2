# utils/web_generator.py
# ============================================
# GENERADOR DE WEBS - V20.3 (EXTRACTOR HTML + FALLBACK)
# ============================================

import os
import sys
import re
import time
import json
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.web_prompts_data import DIRECTOR_DE_ARTE_PROMPT, REGLAS_CSS_PREMIUM, REGLAS_FORMULARIO, REGLAS_SALIDA, REGLAS_ORTOGRAFIA, REGLAS_FOOTER_LEGAL, construir_instrucciones_dinamicas
from utils.web_validator import validar_completo, limpiar_html
from utils.image_fetcher import obtener_urls_imagenes_negocio
from utils.openrouter_manager import consultar_openrouter

try:
    from backend.gateway import analizar_imagen_gemini, gateway
except ImportError:
    analizar_imagen_gemini = None
    gateway = None

MAX_INTENTOS = 3
TIEMPO_ESPERA = 2

def _inyectar_anclas(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    sections = soup.find_all('section')
    for sec in sections:
        texto = sec.get_text(strip=True).lower()
        if 'hero' in texto or (sec.find('h1') and 'bienvenido' in sec.find('h1').get_text().lower()):
            sec['id'] = 'sec-hero'
        elif 'servicio' in texto or 'producto' in texto or sec.find(class_=re.compile('card', re.I)):
            sec['id'] = 'sec-servicios'
        elif 'sobre' in texto or 'quiénes' in texto or 'quienes' in texto:
            sec['id'] = 'sec-quienes-somos'
        elif 'ubicación' in texto or 'donde' in texto or 'dónde' in texto:
            sec['id'] = 'sec-ubicacion'
        elif 'contacto' in texto or 'formulario' in texto or sec.find('form'):
            sec['id'] = 'sec-contacto'
        elif 'horario' in texto:
            sec['id'] = 'sec-horarios'
    
    images = soup.find_all('img')
    for i, img in enumerate(images):
        if not img.get('data-img'):
            img['data-img'] = f"img-{i+1}"
            
    return str(soup)

def _obtener_copy_fallback(nombre_negocio):
    return {
        "headline": f"Bienvenido a {nombre_negocio}",
        "subheadline": "Ofrecemos los mejores servicios de alta calidad para satisfacer todas tus necesidades.",
        "servicios": [
            {"titulo": "Servicio Principal", "descripcion": "Calidad y compromiso garantizado en cada detalle.", "alt_imagen": "Imagen de servicio 1"},
            {"titulo": "Atención Personalizada", "descripcion": "Nos adaptamos a lo que necesitas de manera rápida.", "alt_imagen": "Imagen de servicio 2"},
            {"titulo": "Garantía de Satisfacción", "descripcion": "Trabajamos para superar tus expectativas.", "alt_imagen": "Imagen de servicio 3"}
        ],
        "sobre_nosotros": f"En {nombre_negocio} nos dedicamos a brindar la mejor experiencia a nuestros clientes, con años de experiencia en el sector.",
        "keywords_imagenes": ["business", "office", "success"]
    }

def _generar_html_fallback(copy, nombre_negocio):
    """Plantilla de emergencia si la IA falla 3 veces. Garantiza que el cliente vea su web."""
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{nombre_negocio}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0B0C14; color: #FFFFFF; margin: 0; padding: 0; }}
        nav {{ display: flex; justify-content: space-between; padding: 20px 40px; background: rgba(255,255,255,0.05); }}
        .hero {{ text-align: center; padding: 100px 20px; }}
        .hero h1 {{ font-size: 3rem; margin-bottom: 20px; color: #14B8A6; }}
        .hero p {{ font-size: 1.2rem; color: #94A3B8; max-width: 600px; margin: 0 auto; }}
        .servicios {{ display: flex; justify-content: center; gap: 30px; padding: 60px 20px; flex-wrap: wrap; }}
        .card {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 24px; padding: 30px; width: 300px; text-align: center; }}
        .card h3 {{ color: #14B8A6; }}
        .contacto {{ text-align: center; padding: 60px 20px; }}
        form {{ display: flex; flex-direction: column; gap: 15px; max-width: 400px; margin: 0 auto; }}
        input, textarea {{ padding: 15px; border-radius: 8px; border: 1px solid #333; background: #1a1a1a; color: white; }}
        button {{ padding: 15px; border-radius: 8px; border: none; background: #14B8A6; color: black; font-weight: bold; cursor: pointer; }}
    </style>
</head>
<body>
    <nav><h2>{nombre_negocio}</h2></nav>
    <section class="hero" id="sec-hero">
        <h1>{copy.get('headline')}</h1>
        <p>{copy.get('subheadline')}</p>
        {{HERO_IMAGE}}
    </section>
    <section class="servicios" id="sec-servicios">
        <div class="card"><h3>{copy['servicios'][0]['titulo']}</h3><p>{copy['servicios'][0]['descripcion']}</p>{{SERVICIO_1}}</div>
        <div class="card"><h3>{copy['servicios'][1]['titulo']}</h3><p>{copy['servicios'][1]['descripcion']}</p>{{SERVICIO_2}}</div>
        <div class="card"><h3>{copy['servicios'][2]['titulo']}</h3><p>{copy['servicios'][2]['descripcion']}</p>{{SERVICIO_3}}</div>
    </section>
    <section class="contacto" id="sec-contacto">
        <h2>Contáctanos</h2>
        <form action="/submit_lead" method="POST">
            <input type="text" name="nombre" placeholder="Nombre completo" required>
            <input type="email" name="email" placeholder="Correo electronico" required>
            <textarea name="mensaje" placeholder="En que podemos ayudarte?" required></textarea>
            <button type="submit">Enviar Mensaje</button>
        </form>
    </section>
</body>
</html>"""
    return html

def generar_copy_estrategico(datos_negocio, descripcion_fotos, modelo_ia, pedido_id="sin_id"):
    sector = datos_negocio.get('sector', 'General')
    desc = datos_negocio.get('descripcion', '')
    
    contexto_fotos = ""
    if descripcion_fotos:
        contexto_fotos = f"\n¡ATENCIÓN! El usuario subió fotos reales y la IA de visión las describió así:\n{descripcion_fotos}\nPor favor, integra estas imágenes reales en el copy."

    prompt = f"""
Analiza el siguiente negocio:
- Nombre: {datos_negocio.get('nombre')}
- Sector: {sector}
- Descripcion: {desc}
{contexto_fotos}

Redacta el Copy exacto para su pagina web premium. 
¡ATENCIÓN! Los servicios DEBEN estar directamente relacionados con el sector '{sector}' y la descripción.
¡CRÍTICO! Usa ESPAÑOL NEUTRO DE LATINOAMÉRICA. NO uses modismos de España.

Devuelve UNICAMENTE un JSON valido. NO agregues texto antes ni después. Solo el JSON puro:
{{
  "headline": "Titulo impactante (max 10 palabras)",
  "subheadline": "Subtitulo persuasivo (max 25 palabras)",
  "servicios": [
    {{"titulo": "Servicio 1", "descripcion": "Texto persuasivo (max 25 palabras, idea completa)", "alt_imagen": "Descripcion en español de la foto del servicio 1"}},
    {{"titulo": "Servicio 2", "descripcion": "Texto persuasivo (max 25 palabras, idea completa)", "alt_imagen": "Descripcion en español de la foto del servicio 2"}},
    {{"titulo": "Servicio 3", "descripcion": "Texto persuasivo (max 25 palabras, idea completa)", "alt_imagen": "Descripcion en español de la foto del servicio 3"}}
  ],
  "sobre_nosotros": "Parrafo de 40 palabras.",
  "keywords_imagenes": ["keyword_1_in_english", "keyword_2_in_english", "keyword_3_in_english"]
}}
"""
    sistema = "Eres un redactor publicitario experto. No hables de diseño web ni marketing digital a menos que el cliente sea una agencia."
    
    try:
        respuesta, _, error = consultar_openrouter(prompt, sistema, modelo=modelo_ia, temperature=0.7, pedido_id=pedido_id)
        if not error and respuesta and len(respuesta) > 20: return respuesta
    except Exception: pass
    
    try:
        if gateway:
            respuesta, fuente = gateway.chat_inteligente(prompt, sistema, temperature=0.7, pedido_id=pedido_id)
            if respuesta and "[ERROR]" not in respuesta and len(respuesta) > 20:
                return respuesta
    except Exception: pass
    
    return None

def generar_html_programador(datos_negocio, copy, modelo_ia, pedido_id="sin_id"):
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

## REGLAS OBLIGATORIAS
{REGLAS_CSS_PREMIUM}
{REGLAS_FORMULARIO}
{REGLAS_ORTOGRAFIA}
{REGLAS_FOOTER_LEGAL}
{REGLAS_SALIDA}
"""
    sistema = "Eres un programador Frontend Senior. Devuelves solo el codigo HTML puro, sin markdown."
    
    respuesta_final = None
    try:
        respuesta, _, error = consultar_openrouter(prompt, sistema, modelo=modelo_ia, pedido_id=pedido_id)
        if not error and respuesta and len(respuesta) > 100: respuesta_final = respuesta
    except Exception: pass
    
    if not respuesta_final:
        try:
            if gateway:
                respuesta, _ = gateway.chat_inteligente(prompt, sistema, pedido_id=pedido_id)
                if respuesta and "[ERROR]" not in respuesta and len(respuesta) > 100:
                    respuesta_final = respuesta
        except Exception: pass

    if respuesta_final:
        # EXTRACTOR QUIRURGICO: Si la IA manda markdown o texto extra, sacamos solo el HTML
        match = re.search(r'<html.*?>.*?</html>', respuesta_final, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(0)
        elif "<body" in respuesta_final.lower():
            # Si le faltó el <html> pero tiene <body>, lo envolvemos
            return f"<!DOCTYPE html>\n<html>\n<head><meta charset='utf-8'></head>\n{respuesta_final}\n</html>"

    return None

def inyectar_elementos_criticos(html, imagenes, logo_b64, nombre_negocio, datos_negocio, copy):
    hero_url = imagenes.get("hero")
    servicios_urls = imagenes.get("servicios", [])
    
    if hero_url: html = html.replace("{{HERO_IMAGE}}", hero_url)
    if len(servicios_urls) > 0: html = html.replace("{{SERVICIO_1}}", servicios_urls[0])
    if len(servicios_urls) > 1: html = html.replace("{{SERVICIO_2}}", servicios_urls[1])
    if len(servicios_urls) > 2: html = html.replace("{{SERVICIO_3}}", servicios_urls[2])

    soup = BeautifulSoup(html, 'html.parser')

    if logo_b64:
        primer_enlace = soup.find('a')
        header = soup.find('header') or soup.find('nav')
        logo_img = soup.new_tag('img', src=logo_b64, alt=f"Logo de {nombre_negocio}")
        logo_img['style'] = "height:60px; width:auto; object-fit:contain; max-width:220px; margin-right:20px;"
        logo_img['data-img'] = "logo"
        
        if header: header.insert(0, logo_img)
        elif primer_enlace:
            primer_enlace.clear()
            primer_enlace.append(logo_img)
        else:
            body = soup.find('body')
            if body: body.insert(0, logo_img)

    if hero_url and "{{HERO_IMAGE}}" not in html:
        h1 = soup.find('h1')
        container = h1.parent if h1 else soup.find('section')
        
        if container:
            for img in container.find_all('img'): img.decompose()
            sector = datos_negocio.get('sector', 'Negocio')
            img_tag = soup.new_tag('img', src=hero_url, alt=f"Imagen representativa de {sector} para {nombre_negocio}")
            img_tag['style'] = "width:100%; max-width:1000px; height:auto; max-height:600px; object-fit:cover; border-radius:24px; margin:40px auto 0; display:block; box-shadow: 0 20px 40px rgba(0,0,0,0.4);"
            img_tag['data-img'] = "hero"
            container.append(img_tag)

    if servicios_urls:
        tarjetas = []
        for div in soup.find_all('div'):
            if (div.find('h3') or div.find('h4')) and len(div.get_text(strip=True)) < 350:
                tarjetas.append(div)

        servicios_copy = copy.get('servicios', [])
        for i, url in enumerate(servicios_urls):
            if i >= len(tarjetas): break
            tarjeta = tarjetas[i]
            
            for img in tarjeta.find_all('img'): img.decompose()
                
            alt_serv = servicios_copy[i].get('alt_imagen', f"Servicio {i+1}") if i < len(servicios_copy) else f"Servicio {i+1}"
            img_tag = soup.new_tag('img', src=url, alt=alt_serv)
            img_tag['style'] = "width:100%; height:220px; object-fit:cover; border-radius:16px; margin-bottom:24px; display:block;"
            img_tag['data-img'] = f"servicio-{i+1}"
            tarjeta.insert(0, img_tag)
            
            tarjeta['style'] = "background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 24px; padding: 30px; display: flex; flex-direction: column; height: 100%;"

    form_section = soup.find(id='contacto') or soup.find(class_=re.compile('contact', re.I))
    if form_section and not form_section.find('form'):
        form_html = """
        <form action="/submit_lead" method="POST" style="display:flex; flex-direction:column; gap:15px; max-width:500px; margin:40px auto; position: relative; z-index: 10;">
            <input type="text" name="nombre" placeholder="Nombre completo" required style="padding:15px; border-radius:8px; border:1px solid #333; background:#1a1a1a; color:white; width:100%;">
            <input type="email" name="email" placeholder="Correo electronico" required style="padding:15px; border-radius:8px; border:1px solid #333; background:#1a1a1a; color:white; width:100%;">
            <textarea name="mensaje" placeholder="En que podemos ayudarte?" required style="padding:15px; border-radius:8px; border:1px solid #333; background:#1a1a1a; color:white; min-height:120px; width:100%;"></textarea>
            <button type="submit" class="btn" style="padding:15px; border-radius:8px; border:none; background:#14B8A6; color:black; font-weight:bold; cursor:pointer; width:100%;">Enviar Mensaje</button>
        </form>
        """
        form_soup = BeautifulSoup(form_html, 'html.parser')
        form_section.append(form_soup)

    return str(soup)

def generar_web(datos_negocio, opciones=None, modelo_ia="nvidia/nemotron-3-super-120b"):
    logo_b64 = datos_negocio.get("logo_b64")
    fotos_b64 = datos_negocio.get("fotos_b64", [])
    pedido_id = datos_negocio.get("pedido_id", "sin_id")
    nombre_negocio = datos_negocio.get("nombre", "Mi Negocio")
    
    descripcion_fotos = ""
    if fotos_b64 and analizar_imagen_gemini:
        try:
            prompt_vision = "Describe esta imagen en 10 palabras. ¿Qué producto o servicio muestra?"
            desc_individual = analizar_imagen_gemini(fotos_b64[0], prompt_vision, pedido_id=pedido_id)
            if desc_individual and "Imagen del producto" not in desc_individual:
                descripcion_fotos = f"Foto Principal: {desc_individual}"
        except Exception: pass

    copy_raw = generar_copy_estrategico(datos_negocio, descripcion_fotos, modelo_ia, pedido_id=pedido_id)
    copy = None
    if copy_raw and not copy_raw.startswith("[ERROR]"):
        try:
            match = re.search(r'\{.*\}', copy_raw, re.DOTALL)
            if match: copy = json.loads(match.group(0))
        except Exception: pass
    
    if not copy:
        copy = _obtener_copy_fallback(nombre_negocio)

    imagenes = {"hero": None, "servicios": []}
    if fotos_b64:
        imagenes["hero"] = fotos_b64[0] if len(fotos_b64) > 0 else None
        imagenes["servicios"] = fotos_b64[1:4]
    
    faltan_servicios = 3 - len(imagenes["servicios"])
    if faltan_servicios > 0 or not imagenes["hero"]:
        keywords = copy.get("keywords_imagenes", ["business"])
        negocio_info = {"nombre": nombre_negocio, "sector": " ".join(keywords), "descripcion": datos_negocio.get("descripcion")}
        poll = obtener_urls_imagenes_negocio(negocio_info, cantidad=4)
        if poll:
            if not imagenes["hero"] and len(poll) > 0: imagenes["hero"] = poll[0]["url_regular"]
            imagenes_poll = [p["url_regular"] for p in poll[1:4]]
            for img in imagenes_poll:
                if len(imagenes["servicios"]) < 3: imagenes["servicios"].append(img)

    html_valido = False
    html_final = ""
    for intento in range(1, MAX_INTENTOS + 1):
        html_raw = generar_html_programador(datos_negocio, copy, modelo_ia, pedido_id=pedido_id)
        if not html_raw: continue

        html = limpiar_html(html_raw)
        html = inyectar_elementos_criticos(html, imagenes, logo_b64, nombre_negocio, datos_negocio, copy)
        html = _inyectar_anclas(html)

        if validar_completo(html)["valido"]:
            html_valido = True
            html_final = html
            break

    # PLAN C: Si la IA falló 3 veces, usamos la plantilla local para que el usuario SI VEA SU WEB
    if not html_valido:
        print("[ALERTA] IA falló en generar HTML válido. Usando plantilla local de respaldo.")
        html_fallback = _generar_html_fallback(copy, nombre_negocio)
        html_final = inyectar_elementos_criticos(html_fallback, imagenes, logo_b64, nombre_negocio, datos_negocio, copy)
        html_final = _inyectar_anclas(html_final)

    return {"exito": True, "html": html_final, "error": None}