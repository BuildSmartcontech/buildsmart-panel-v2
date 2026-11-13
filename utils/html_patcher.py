# utils/html_patcher.py
# ============================================
# APLICADOR DE CAMBIOS AL HTML - V4.0 (PARCHER DEFINITIVO)
# ============================================

import re
from bs4 import BeautifulSoup
from utils.image_fetcher import obtener_urls_imagenes_negocio

def _reparar_imagenes_rotas(html_completo):
    soup = BeautifulSoup(html_completo, 'html.parser')
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if "{{" in src or not src or (src.startswith("http") and "images.unsplash.com" not in src):
            if "base64" in src:
                continue
            alt_texto = img.get('alt', 'negocio')
            imagenes = obtener_urls_imagenes_negocio({"sector": alt_texto}, cantidad=1)
            if imagenes:
                img['src'] = imagenes[0]['url_regular']
            else:
                img['src'] = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1200&auto=format&fit=crop"
    return str(soup)

def _limpiar_html_residual(html_code: str) -> str:
    if "</footer>" in html_code:
        partes = html_code.split("</footer>")
        return partes[0] + "</footer>\n</body>\n</html>"
    return html_code

def aplicar_cambios(html, acciones):
    if not html or not acciones:
        return {"exito": False, "html_nuevo": html, "error": "Sin cambios"}

    html = _limpiar_html_residual(html)
    soup = BeautifulSoup(html, 'html.parser')
    cambios_reales = 0
    explicacion = "Cambios aplicados"

    for accion in acciones:
        tipo = accion.get("tipo")
        
        # 1. REEMPLAZAR TEXTO (Seguro, sin borrar la etiqueta)
        if tipo == "reemplazar_texto":
            selector = accion.get("selector", "h1")
            texto_actual = accion.get("texto_actual", "")
            texto_nuevo = accion.get("texto_nuevo", "")
            etiquetas = soup.find_all(selector)
            for etiqueta in etiquetas:
                # Si no hay texto_actual, cambiamos el primero que encontremos
                if not texto_actual or texto_actual in etiqueta.get_text():
                    etiqueta.string = texto_nuevo
                    cambios_reales += 1
                    break

        # 2. REEMPLAZAR IMAGEN (Buscando por Alt)
        elif tipo == "reemplazar_imagen":
            alt_viejo = accion.get("alt_viejo", "")
            busqueda = accion.get("busqueda_nueva", "")
            if alt_viejo and busqueda:
                imagenes = soup.find_all('img')
                for img in imagenes:
                    if alt_viejo.lower() in img.get('alt', '').lower():
                        # Buscamos una nueva imagen real
                        nuevas = obtener_urls_imagenes_negocio({"sector": busqueda}, cantidad=1)
                        if nuevas:
                            img['src'] = nuevas[0]['url_regular']
                            cambios_reales += 1
                        break

        # 3. AGREGAR SECCIÓN
        elif tipo == "agregar_seccion":
            html_seccion = accion.get("html", "")
            if html_seccion:
                seccion_soup = BeautifulSoup(html_seccion, 'html.parser')
                anclaje = soup.find(id='ubicacion') or soup.find(id='horarios') or soup.find(id='contacto') or soup.find('footer')
                if anclaje:
                    anclaje.insert_before(seccion_soup)
                else:
                    body = soup.find('body')
                    if body: body.append(seccion_soup)
                cambios_reales += 1

        # 4. ELIMINAR SECCIÓN
        elif tipo == "eliminar":
            texto = accion.get("texto", "")
            if texto:
                nodos = soup.find_all(string=re.compile(re.escape(texto), re.IGNORECASE))
                for nodo in nodos:
                    padre = nodo.parent
                    top_padre = padre
                    while padre and padre.name not in ['body', 'html']:
                        top_padre = padre
                        padre = padre.parent
                    if top_padre and top_padre.name not in ['body', 'html']:
                        top_padre.decompose()
                        cambios_reales += 1
                        break

        # 5. CAMBIAR COLOR
        elif tipo == "color":
            css = accion.get("css", "")
            if css:
                style_tag = soup.find('style')
                if style_tag:
                    style_tag.string = (style_tag.string or "") + "\n" + css
                    cambios_reales += 1

    html_final = str(soup)

    if cambios_reales == 0:
        return {
            "exito": False, 
            "html_nuevo": html, 
            "error": "La IA no encontró el texto o la imagen que pediste cambiar. Intenta ser más específico."
        }

    # Reparar imágenes si es que se agregó una sección con el comodín
    html_final = _reparar_imagenes_rotas(html_final)

    return {
        "exito": True,
        "html_nuevo": html_final,
        "cambios_aplicados": cambios_reales,
        "cambios_totales": len(acciones),
        "aplicados": [{"descripcion": explicacion, "detalle": ""}],
        "fallidos": []
    }