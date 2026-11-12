# utils/html_patcher.py
# ============================================
# APLICADOR DE CAMBIOS AL HTML - V2.6 (REPARADOR MASIVO)
# ============================================

import re
from bs4 import BeautifulSoup
from utils.image_fetcher import obtener_urls_imagenes_negocio

def _reparar_imagenes_rotas(html_completo, categoria="general"):
    """
    Escanea TODO el HTML. Si encuentra imágenes con URLs inventadas (que no sean
    de Unsplash o que estén vacías), las reemplaza por fotos reales.
    """
    soup = BeautifulSoup(html_completo, 'html.parser')
    
    for img in soup.find_all('img'):
        src = img.get('src', '')
        
        # Detectamos si la URL es inventada o vacía
        # (Si no empieza con https://images.unsplash.com o tiene caracteres raros)
        es_invalida = (
            not src or 
            "{{" in src or 
            (src.startswith("http") and "images.unsplash.com" not in src)
        )
        
        # El logo lo dejamos intacto (suele ser base64)
        if "base64" in src:
            continue
            
        if es_invalida:
            alt_texto = img.get('alt', 'negocio')
            # Buscamos una imagen real usando el alt como palabra clave
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
    explicacion = cambios.get("explicacion", "Cambios aplicados")

    if not reglas_css and not secciones_html and not reemplazos_texto:
        return {"exito": False, "html_nuevo": html, "error": "La IA no generó cambios."}

    soup = BeautifulSoup(html, 'html.parser')

    # 1. REEMPLAZAR TEXTOS
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

    # 2. INYECTAR CSS
    if reglas_css:
        bloque_css = "\n/* CAMBIOS DINÁMICOS */\n" + "\n".join(reglas_css) + "\n"
        style_tag = soup.find('style')
        if style_tag:
            style_tag.string = (style_tag.string or "") + bloque_css

    # 3. INYECTAR HTML NUEVO (Ubicación Estructural)
    if secciones_html:
        for html_seccion in secciones_html:
            seccion_soup = BeautifulSoup(html_seccion, 'html.parser')
            
            # Buscamos el punto de anclaje ideal: ID 'contacto' o etiqueta 'footer'
            anclaje = soup.find(id='contacto') or soup.find('footer')
            
            if anclaje:
                anclaje.insert_before(seccion_soup)
            else:
                body = soup.find('body')
                if body: body.append(seccion_soup)
                else: soup.append(seccion_soup)

    html_final = str(soup)
    
    # 4. REPARACIÓN MASIVA DE IMÁGENES (Pase final de seguridad)
    html_final = _reparar_imagenes_rotas(html_final)

    return {
        "exito": True,
        "html_nuevo": html_final,
        "cambios_aplicados": len(reglas_css) + len(secciones_html) + len(reemplazos_texto),
        "cambios_totales": len(reglas_css) + len(secciones_html) + len(reemplazos_texto),
        "aplicados": [{"descripcion": explicacion, "detalle": ""}],
        "fallidos": []
    }