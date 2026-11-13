# utils/html_patcher.py
# ============================================
# APLICADOR DE CAMBIOS AL HTML - V3.2 (LIMPIEZA NUCLEAR)
# ============================================

import re
from bs4 import BeautifulSoup
from utils.image_fetcher import obtener_urls_imagenes_negocio

def limpiar_html_residual(html_code: str) -> str:
    """Corta cualquier basura que haya quedado después del cierre del footer."""
    if "</footer>" in html_code:
        partes = html_code.split("</footer>")
        html_limpio = partes[0] + "</footer>\n</body>\n</html>"
        return html_limpio
    return html_code

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

def aplicar_cambios(html, cambios):
    if not html or not cambios:
        return {"exito": False, "html_nuevo": html, "error": "Sin cambios"}

    # 1. LIMPIEZA PREVIA (Corta basura después del footer)
    html = limpiar_html_residual(html)

    reglas_css = cambios.get("reglas_css", [])
    secciones_html = cambios.get("secciones_html", [])
    reemplazos_texto = cambios.get("reemplazos_texto", [])
    eliminar_secciones = cambios.get("eliminar_secciones", [])
    explicacion = cambios.get("explicacion", "Cambios aplicados")

    soup = BeautifulSoup(html, 'html.parser')
    cambios_reales = 0

    # 2. ELIMINAR SECCIONES VIEJAS (BORRADO BRUTAL POR TEXTO)
    if eliminar_secciones:
        for elim in eliminar_secciones:
            texto = elim.get("texto_que_contiene", "").strip()
            if texto:
                nodos = soup.find_all(string=re.compile(re.escape(texto), re.IGNORECASE))
                for nodo in nodos:
                    # Buscamos el "padre" más alto que no sea el body
                    padre = nodo.parent
                    top_padre = padre
                    while padre and padre.name not in ['body', 'html']:
                        top_padre = padre
                        padre = padre.parent
                    
                    if top_padre and top_padre.name not in ['body', 'html']:
                        top_padre.decompose()
                        cambios_reales += 1
                        break
                    elif nodo.parent:
                        nodo.parent.decompose()
                        cambios_reales += 1
                        break

    # 3. REEMPLAZAR TEXTOS
    if reemplazos_texto:
        for rep in reemplazos_texto:
            selector = rep.get("selector", "")
            texto_actual = rep.get("texto_actual", "")
            texto_nuevo = rep.get("texto_nuevo", "")
            if selector and texto_nuevo:
                etiquetas = soup.find_all(selector)
                for etiqueta in etiquetas:
                    if texto_actual and texto_actual in etiqueta.get_text():
                        etiqueta.string = texto_nuevo
                        cambios_reales += 1
                        break
                    elif not texto_actual:
                        etiqueta.string = texto_nuevo
                        cambios_reales += 1
                        break

    # 4. INYECTAR CSS
    if reglas_css:
        bloque_css = "\n/* CAMBIOS DINÁMICOS */\n" + "\n".join(reglas_css) + "\n"
        style_tag = soup.find('style')
        if style_tag:
            style_tag.string = (style_tag.string or "") + bloque_css
            cambios_reales += 1

    # 5. INYECTAR HTML NUEVO
    if secciones_html:
        for html_seccion in secciones_html:
            seccion_soup = BeautifulSoup(html_seccion, 'html.parser')
            anclaje = soup.find(id='ubicacion') or soup.find(id='horarios') or soup.find(id='contacto') or soup.find('footer')
            if anclaje:
                anclaje.insert_before(seccion_soup)
                cambios_reales += 1
            else:
                body = soup.find('body')
                if body: body.append(seccion_soup); cambios_reales += 1
                else: soup.append(seccion_soup); cambios_reales += 1

    html_final = str(soup)
    
    if secciones_html:
        html_final = _reparar_imagenes_rotas(html_final)

    if cambios_reales == 0:
        return {
            "exito": False, 
            "html_nuevo": html, 
            "error": "No se encontró la sección o el texto que pediste eliminar. Intenta ser más específico."
        }

    return {
        "exito": True,
        "html_nuevo": html_final,
        "cambios_aplicados": cambios_reales,
        "cambios_totales": cambios_reales,
        "aplicados": [{"descripcion": explicacion, "detalle": ""}],
        "fallidos": []
    }