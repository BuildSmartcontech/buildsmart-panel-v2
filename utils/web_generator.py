# utils/web_generator.py
# ============================================
# GENERADOR DE WEBS - V20.4 (PLANTILLA PREMIUM + GALERIA 6 FOTOS)
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
        elif 'galeria' in texto or 'galería' in texto:
            sec['id'] = 'sec-galeria'
        elif 'contacto' in texto or 'formulario' in texto or sec.find('form'):
            sec['id'] = 'sec-contacto'
    
    images = soup.find_all('img')
    for i, img in enumerate(images):
        if not img.get('data-img'):
            img['data-img'] = f"img-{i+1}"
            
    return str(soup)

def _obtener_copy_fallback(nombre_negocio):
    return {
        "headline": f"Excelencia y Calidad en {nombre_negocio}",
        "subheadline": "Ofrecemos soluciones integrales adaptadas a tus necesidades con los más altos estándares del mercado.",
        "servicios": [
            {"titulo": "Servicio Especializado", "descripcion": "Garantía, rapidez y eficiencia en cada proyecto que asumimos.", "alt_imagen": "Imagen de servicio 1"},
            {"titulo": "Atención al Cliente", "descripcion": "Asesoría personalizada para encontrar exactamente lo que buscas.", "alt_imagen": "Imagen de servicio 2"},
            {"titulo": "Proyectos a Medida", "descripcion": "Nos adaptamos a tus requerimientos con resultados excepcionales.", "alt_imagen": "Imagen de servicio 3"}
        ],
        "sobre_nosotros": f"En {nombre_negocio} creemos en el poder de la calidad. Somos líderes en nuestro sector, combinando experiencia y tecnología para superar las expectativas de nuestros clientes.",
        "keywords_imagenes": ["business", "industry", "premium"]
    }

def _generar_html_fallback(copy, nombre_negocio, imagenes_extra=None):
    """Plantilla PREMIUM de emergencia. Garantiza una web hermosa incluso si la IA falla."""
    if not imagenes_extra: imagenes_extra = []
    
    galeria_html = ""
    if len(imagenes_extra) > 0:
        galeria_html = f"""
        <section class="galeria" id="sec-galeria">
            <h2>Nuestro Trabajo</h2>
            <div class="galeria-grid">
                {''.join([f'<img src="{img}" alt="Trabajo {i+1}" style="width:100%; border-radius:16px; object-fit:cover; height:250px;">' for i, img in enumerate(imagenes_extra)])}
            </div>
        </section>
        """

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{nombre_negocio}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #14B8A6; --bg: #0B0C14; --card-bg: rgba(255,255,255,0.03); --text: #F8FAFC; --text-muted: #94A3B8; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Outfit', sans-serif; }}
        body {{ background-color: var(--bg); color: var(--text); line-height: 1.6; }}
        
        /* Nav */
        nav {{ display: flex; justify-content: space-between; align-items: center; padding: 20px 5%; background: rgba(11, 12, 20, 0.8); backdrop-filter: blur(10px); position: sticky; top: 0; z-index: 100; border-bottom: 1px solid rgba(255,255,255,0.05); }}
        nav h2 {{ color: var(--text); font-weight: 700; letter-spacing: 1px; }}
        
        /* Hero */
        .hero {{ text-align: center; padding: 120px 20px; background: linear-gradient(180deg, rgba(20,184,166,0.1) 0%, rgba(11,12,20,1) 100%); }}
        .hero h1 {{ font-size: 3.5rem; margin-bottom: 20px; background: linear-gradient(90deg, #fff, var(--primary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .hero p {{ font-size: 1.2rem; color: var(--text-muted); max-width: 700px; margin: 0 auto; }}
        .hero img {{ width: 100%; max-width: 900px; height: 500px; object-fit: cover; border-radius: 24px; margin-top: 40px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }}
        
        /* Servicios */
        .servicios {{ padding: 80px 5%; text-align: center; }}
        .servicios h2 {{ font-size: 2.5rem; margin-bottom: 50px; }}
        .grid-servicios {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }}
        .card {{ background: var(--card-bg); border: 1px solid rgba(255,255,255,0.08); border-radius: 24px; padding: 30px; text-align: left; transition: transform 0.3s ease; }}
        .card:hover {{ transform: translateY(-5px); border-color: var(--primary); }}
        .card img {{ width: 100%; height: 200px; object-fit: cover; border-radius: 16px; margin-bottom: 20px; }}
        .card h3 {{ color: var(--primary); font-size: 1.5rem; margin-bottom: 15px; }}
        
        /* Galería */
        .galeria {{ padding: 80px 5%; text-align: center; background: rgba(0,0,0,0.3); }}
        .galeria h2 {{ font-size: 2.5rem; margin-bottom: 40px; }}
        .galeria-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }}
        
        /* Formulario */
        .contacto {{ padding: 80px 20px; text-align: center; }}
        .contacto form {{ display: flex; flex-direction: column; gap: 15px; max-width: 500px; margin: 40px auto; background: var(--card-bg); padding: 40px; border-radius: 24px; border: 1px solid rgba(255,255,255,0.08); }}
        .contacto input, .contacto textarea {{ padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); background: rgba(0,0,0,0.5); color: white; font-family: inherit; }}
        .contacto input:focus, .contacto textarea:focus {{ outline: none; border-color: var(--primary); }}
        .contacto button {{ padding: 15px; border-radius: 12px; border: none; background: var(--primary); color: #000; font-weight: bold; font-size: 1.1rem; cursor: pointer; transition: opacity 0.3s; }}
        .contacto button:hover {{ opacity: 0.9; }}
        
        footer {{ text-align: center; padding: 40px; border-top: 1px solid rgba(255,255,255,0.05); color: var(--text-muted); }}
    </style>
</head>
<body>
    <nav><h2>{nombre_negocio}</h2></nav>
    <section class="hero" id="sec-hero">
        <h1>{copy.get('headline')}</h1>
        <p>{copy.get('subheadline')}</p>
        <img src="{{HERO_IMAGE}}" alt="Imagen Principal">
    </section>
    <section class="servicios" id="sec-servicios">
        <h2>Nuestros Servicios</h2>
        <div class="grid-servicios">
            <div class="card">
                <img src="{{SERVICIO_1}}" alt="{copy['servicios'][0]['alt_imagen']}">
                <h3>{copy['servicios'][0]['titulo']}</h3>
                <p>{copy['servicios'][0]['descripcion']}</p>
            </div>
            <div class="card">
                <img src="{{SERVICIO_2}}" alt="{copy['servicios'][1]['alt_imagen']}">
                <h3>{copy['servicios'][1]['titulo']}</h3>
                <p>{copy['servicios'][1]['descripcion']}</p>
            </div>
            <div class="card">
                <img src="{{SERVICIO_3}}" alt="{copy['servicios'][2]['alt_imagen']}">
                <h3>{copy['servicios'][2]['titulo']}</h3>
                <p>{copy['servicios'][2]['descripcion']}</p>
            </div>
        </div>
    </section>
    {galeria_html}
    <section class="contacto" id="sec-contacto">
        <h2>Contáctanos</h2>
        <p style="color: var(--text-muted); margin-bottom: 20px;">Estamos listos para atenderte.</p>
        <form action="/submit_lead" method="POST">
            <input type="text" name="nombre" placeholder="Nombre completo" required>
            <input type="email" name="email" placeholder="Correo electrónico" required>
            <textarea name="mensaje" placeholder="¿En qué podemos ayudarte?" required style="min-height: 120px;"></textarea>
            <button type="submit">Enviar Mensaje</button>
        </form>
    </section>
    <footer>
        <p>&copy; 2026 {nombre_negocio}. Todos los derechos reservados.</p>
    </footer>
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
¡CRÍTICO! Usa ESPAÑOL NEUTRO DE LATINOAMÉRICA.

Devuelve UNICAMENTE un JSON valido. NO agregues texto antes ni después. Solo el JSON puro:
{{
  "headline": "Titulo impactante (max 10 palabras)",
  "subheadline": "Subtitulo persuasivo (max 25 palabras)",
  "servicios": [
    {{"titulo": "Servicio 1", "descripcion": "Texto persuasivo (max 25 palabras)", "alt_imagen": "Descripcion de la foto 1"}},
    {{"titulo": "Servicio 2", "descripcion": "Texto persuasivo (max 25 palabras)", "alt_imagen": "Descripcion de la foto 2"}},
    {{"titulo": "Servicio 3", "descripcion": "Texto persuasivo (max 25 palabras)", "alt_imagen": "Descripcion de la foto 3"}}
  ],
  "sobre_nosotros": "Parrafo de 40 palabras.",
  "keywords_imagenes": ["keyword_1_in_english", "keyword_2_in_english", "keyword_3_in_english"]
}}
"""
    sistema = "Eres un redactor publicitario experto."
    
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
        match = re.search(r'<html.*?>.*?</html>', respuesta_final, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(0)
        elif "<body" in respuesta_final.lower():
            return f"<!DOCTYPE html>\n<html>\n<head><meta charset='utf-8'></head>\n{respuesta_final}\n</html>"

    return None

def inyectar_elementos_criticos(html, imagenes, logo_b64, nombre_negocio, datos_negocio, copy):
    hero_url = imagenes.get("hero", "")
    servicios_urls = imagenes.get("servicios", [])
    
    # FIX: Buscamos llaves simples Y dobles para evitar los textos raros en pantalla
    html = html.replace("{{HERO_IMAGE}}", hero_url).replace("{HERO_IMAGE}", hero_url)
    if len(servicios_urls) > 0: html = html.replace("{{SERVICIO_1}}", servicios_urls[0]).replace("{SERVICIO_1}", servicios_urls[0])
    if len(servicios_urls) > 1: html = html.replace("{{SERVICIO_2}}", servicios_urls[1]).replace("{SERVICIO_2}", servicios_urls[1])
    if len(servicios_urls) > 2: html = html.replace("{{SERVICIO_3}}", servicios_urls[2]).replace("{SERVICIO_3}", servicios_urls[2])

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

    if hero_url and "{{HERO_IMAGE}}" not in html and "{HERO_IMAGE}" not in html:
        h1 = soup.find('h1')
        container = h1.parent if h1 else soup.find('section')
        if container:
            for img in container.find_all('img'): img.decompose()
            img_tag = soup.new_tag('img', src=hero_url, alt=f"Imagen de {nombre_negocio}")
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

    form_section = soup.find(id='contacto') or soup.find(class_=re.compile('contact', re.I))
    if form_section and not form_section.find('form'):
        form_html = """
        <form action="/submit_lead" method="POST" style="display:flex; flex-direction:column; gap:15px; max-width:500px; margin:40px auto;">
            <input type="text" name="nombre" placeholder="Nombre completo" required style="padding:15px; border-radius:8px; border:1px solid #333; background:#1a1a1a; color:white;">
            <input type="email" name="email" placeholder="Correo electronico" required style="padding:15px; border-radius:8px; border:1px solid #333; background:#1a1a1a; color:white;">
            <textarea name="mensaje" placeholder="En que podemos ayudarte?" required style="padding:15px; border-radius:8px; border:1px solid #333; background:#1a1a1a; color:white; min-height:120px;"></textarea>
            <button type="submit" class="btn" style="padding:15px; border-radius:8px; border:none; background:#14B8A6; color:black; font-weight:bold; cursor:pointer;">Enviar Mensaje</button>
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

    # Distribución de las 6 imágenes
    imagenes = {"hero": None, "servicios": [], "galeria": []}
    if fotos_b64:
        imagenes["hero"] = fotos_b64[0] if len(fotos_b64) > 0 else None
        imagenes["servicios"] = fotos_b64[1:4] # Fotos 2, 3, 4
        imagenes["galeria"] = fotos_b64[4:7]   # Fotos 5, 6, 7
    
    # Si faltan imágenes de servicio, usamos Unsplash
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

    # PLAN C: Si la IA falló, usamos la plantilla local PREMIUM
    if not html_valido:
        print("[ALERTA] IA falló en generar HTML válido. Usando plantilla local PREMIUM.")
        html_fallback = _generar_html_fallback(copy, nombre_negocio, imagenes_extra=imagenes["galeria"])
        html_final = inyectar_elementos_criticos(html_fallback, imagenes, logo_b64, nombre_negocio, datos_negocio, copy)
        html_final = _inyectar_anclas(html_final)

    return {"exito": True, "html": html_final, "error": None}