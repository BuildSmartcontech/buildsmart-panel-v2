# utils/html_patcher.py
# ============================================
# APLICADOR DE CAMBIOS AL HTML - V2.8 (LIMPIEZA Y ANCLAJE INTELIGENTE)
# ============================================

import re
from bs4 import BeautifulSoup
from utils.image_fetcher import obtener_urls_imagenes_negocio

def limpiar_html_residual(html_code: str) -> str:
    """Corta cualquier basura que haya quedado después del cierre del footer."""
    if "</footer>" in html_code:
        partes = html_code.split("</footer>")
        # Conservamos hasta el cierre del footer y cerramos bien el body y html
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

    reglas_css = cambios.get("reglas_css", [])
    secciones_html = cambios.get("secciones_html", [])
    reemplazos_texto = cambios.get("reemplazos_texto", [])
    eliminar_secciones = cambios.get("eliminar_secciones", [])
    explicacion = cambios.get("explicacion", "Cambios aplicados")

    if not reglas_css and not secciones_html and not reemplazos_texto and not eliminar_secciones:
        return {"exito": False, "html_nuevo": html, "error": "La IA no generó cambios."}

    # 0. LIMPIEZA PREVIA DE BASURA
    html = limpiar_html_residual(html)
    soup = BeautifulSoup(html, 'html.parser')

    # 1. ELIMINAR SECCIONES VIEJAS
    if eliminar_secciones:
        for elim in eliminar_secciones:
            selector = elim.get("selector", "section")
            texto = elim.get("texto_que_contiene", "")
            if texto:
                for tag in soup.find_all(selector):
                    if texto in tag.get_text():
                        tag.decompose()

    # 2. REEMPLAZAR TEXTOS
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
                        break
                    elif not texto_actual:
                        etiqueta.string = texto_nuevo
                        break

    # 3. INYECTAR CSS
    if reglas_css:
        bloque_css = "\n/* CAMBIOS DINÁMICOS */\n" + "\n".join(reglas_css) + "\n"
        style_tag = soup.find('style')
        if style_tag:
            style_tag.string = (style_tag.string or "") + bloque_css

    # 4. INYECTAR HTML NUEVO (Ubicación Inteligente)
    if secciones_html:
        for html_seccion in secciones_html:
            seccion_soup = BeautifulSoup(html_seccion, 'html.parser')
            
            # Buscamos el ancla correcta: Ubicación, Contacto o Footer
            # Así las tarjetas nuevas quedan antes de Ubicación, no debajo de Horarios
            anclaje = soup.find(id='ubicacion') or soup.find(id='contacto') or soup.find('footer')
            
            if anclaje:
                anclaje.insert_before(seccion_soup)
            else:
                body = soup.find('body')
                if body: body.append(seccion_soup)
                else: soup.append(seccion_soup)

    html_final = str(soup)
    
    # 5. REPARACIÓN MASIVA DE IMÁGENES
    html_final = _reparar_imagenes_rotas(html_final)

    return {
        "exito": True,
        "html_nuevo": html_final,
        "cambios_aplicados": len(reglas_css) + len(secciones_html) + len(reemplazos_texto) + len(eliminar_secciones),
        "cambios_totales": len(reglas_css) + len(secciones_html) + len(reemplazos_texto) + len(eliminar_secciones),
        "aplicados": [{"descripcion": explicacion, "detalle": ""}],
        "fallidos": []
    }