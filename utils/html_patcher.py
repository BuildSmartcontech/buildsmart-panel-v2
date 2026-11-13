# utils/html_patcher.py
# ============================================
# APLICADOR DE CAMBIOS AL HTML - V9.0 (MODO DIOS SUPREMO)
# ============================================

import re
from bs4 import BeautifulSoup
from utils.image_fetcher import obtener_urls_imagenes_negocio

def _limpiar_html_residual(html_code: str) -> str:
    if "</footer>" in html_code:
        partes = html_code.split("</footer>")
        return partes[0] + "</footer>\n</body>\n</html>"
    return html_code

def _es_color_claro(hex_color):
    try:
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3: hex_color = ''.join([c*2 for c in hex_color])
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return (r * 0.299 + g * 0.587 + b * 0.114) > 186
    except: return False

def _reparar_imagenes_rotas(html_completo):
    soup = BeautifulSoup(html_completo, 'html.parser')
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if not src or "{{" in src or (src.startswith("http") and "images.unsplash.com" not in src):
            if "base64" in src: continue
            alt_texto = img.get('alt', 'negocio')
            # Buscamos una imagen real
            imagenes = obtener_urls_imagenes_negocio({"sector": alt_texto}, cantidad=1)
            if imagenes:
                img['src'] = imagenes[0]['url_regular']
            else:
                # Fallback directo a Unsplash
                img['src'] = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1200&auto=format&fit=crop"
    return str(soup)

def _buscar_elemento_tolerante(soup, selector):
    elementos = soup.select(selector)
    if elementos: return elementos
    texto_limpio = selector.replace("#", "").replace(".", "").replace("sec-", "").replace("-", " ").strip().lower()
    if not texto_limpio: return []
    sinonimos = {
        "hero": ["hero", "inicio", "bienvenido", "descubre"],
        "contacto": ["contacto", "contactanos", "formulario", "email"],
        "servicios": ["servicio", "propiedad", "producto", "oferta"],
        "quienes": ["quienes", "sobre", "nosotros", "historia"],
        "ubicacion": ["ubicacion", "donde", "estamos", "mapa", "direccion"],
        "horarios": ["horario", "atencion", "lunes"],
        "nav": ["inicio", "menu", "navegacion"],
        "footer": ["derechos", "reservados", "privacidad"]
    }
    for key, palabras in sinonimos.items():
        if key in texto_limpio or any(p in texto_limpio for p in palabras):
            for tag in soup.find_all(['section', 'div', 'nav', 'footer']):
                contenido = tag.get_text(strip=True).lower()
                if any(p in contenido for p in palabras): return [tag]
    for tag in soup.find_all(['section', 'div']):
        if texto_limpio in tag.get_text(strip=True).lower(): return [tag]
    return []

def aplicar_cambios(html, operaciones):
    if not html or not operaciones:
        return {"exito": False, "html_nuevo": html, "error": "Sin cambios"}

    html = _limpiar_html_residual(html)
    soup = BeautifulSoup(html, 'html.parser')
    cambios_reales = 0
    
    cambio_fondo_body = False
    color_fondo_body = "#000"

    for op in operaciones:
        selector = op.get("selector", "")
        accion = op.get("accion", "")
        valor = op.get("valor", "")
        
        if not selector or not accion: continue
            
        # Protección SVG
        if "svg" in selector.lower() or "map" in selector.lower() or "icon" in selector.lower():
            continue

        elementos = _buscar_elemento_tolerante(soup, selector)
        if not elementos: continue

        if accion == "cambiar_texto":
            for el in elementos:
                el.string = valor
                cambios_reales += 1
                break
                
        elif accion == "cambiar_atributo":
            atributo = op.get("atributo", "")
            if atributo and atributo.lower() != "style":
                for el in elementos:
                    el[atributo] = valor
                    cambios_reales += 1
                    break
                    
        elif accion == "insertar_html":
            for el in elementos:
                fragmento = BeautifulSoup(valor, 'html.parser')
                el.append(fragmento)
                cambios_reales += 1
                break
                
        elif accion == "mover":
            destino = op.get("destino", "")
            destino_limpio = destino.lower().replace("despues de", "despues_de").replace("antes de", "antes_de").replace(" ", "_")
            ancla_destino = None
            if destino_limpio.startswith("despues_de_"):
                ancla_destino = _buscar_elemento_tolerante(soup, destino_limpio.replace("despues_de_", ""))
            elif destino_limpio.startswith("antes_de_"):
                ancla_destino = _buscar_elemento_tolerante(soup, destino_limpio.replace("antes_de_", ""))
            
            if ancla_destino:
                ancla_destino = ancla_destino[0]
                for el in elementos:
                    if destino_limpio.startswith("despues_de_"): ancla_destino.insert_after(el.extract())
                    else: ancla_destino.insert_before(el.extract())
                    cambios_reales += 1
                    break
                        
        elif accion == "cambiar_css":
            for el in elementos:
                if el.name in ['svg', 'path', 'img']: continue
                estilo_actual = el.get('style', '')
                el['style'] = estilo_actual + "; " + valor
                cambios_reales += 1
                
                if el.name in ['body', 'html'] and 'background' in valor:
                    cambio_fondo_body = True
                    match = re.search(r'#([0-9a-fA-F]{3,6})', valor)
                    if match: color_fondo_body = "#" + match.group(1)
                break
                
        elif accion == "eliminar":
            for el in elementos:
                if el.name in ['svg', 'img']: continue
                el.decompose()
                cambios_reales += 1
                break

    # --- REGLAS DE MODO DIOS SUPREMO ---
    style_tag = soup.find('style')
    if style_tag:
        css_extra = ""
        if cambio_fondo_body:
            # 1. Limpiar TODOS los fondos y gradientes hardcodeados
            css_extra += "\nbody, nav, footer, section, .hero, .card { background: none !important; box-shadow: none !important; }\n"
            
            if _es_color_claro(color_fondo_body):
                # 2. Fondo claro: forzar TODO a blanco y textos a negro
                css_extra += "body, nav, footer, section, .card { background-color: #FFFFFF !important; }\n"
                css_extra += "body, h1, h2, h3, p, span, li, a, nav a, footer a { color: #111111 !important; }\n"
                # 3. Fusilar el gradiente del título
                css_extra += "h1, h2 { -webkit-text-fill-color: #111111 !important; -webkit-background-clip: initial !important; background: none !important; }\n"
            else:
                # Fondo oscuro: forzar TODO a negro
                css_extra += "body, nav, footer, section, .card { background-color: #0B0C14 !important; }\n"
                css_extra += "body, h1, h2, h3, p, span, li, a, nav a, footer a { color: #FFFFFF !important; }\n"
        
        # Proteger SVGs de tamaño
        css_extra += "\nsvg { max-width: 100px !important; max-height: 100px !important; }\n"
        
        style_tag.string = (style_tag.string or "") + css_extra

    html_final = str(soup)

    if cambios_reales == 0:
        return {"exito": False, "html_nuevo": html, "error": "La IA no encontró el elemento exacto para aplicar el cambio."}

    # Reparar imágenes rotas SIEMPRE al final
    html_final = _reparar_imagenes_rotas(html_final)

    return {
        "exito": True,
        "html_nuevo": html_final,
        "cambios_aplicados": cambios_reales,
        "cambios_totales": len(operaciones),
        "aplicados": [{"descripcion": "Cambios aplicados", "detalle": ""}],
        "fallidos": []
    }