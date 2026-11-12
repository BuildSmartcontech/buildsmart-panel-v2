# utils/html_patcher.py
# ============================================
# APLICADOR DE CAMBIOS AL HTML - V2.4 (REEMPLAZO QUIRÚRGICO)
# ============================================

import re
from bs4 import BeautifulSoup

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

    # 1. REEMPLAZAR TEXTOS (Quirúrgico)
    if reemplazos_texto:
        for rep in reemplazos_texto:
            selector = rep.get("selector", "")
            texto_actual = rep.get("texto_actual", "")
            texto_nuevo = rep.get("texto_nuevo", "")
            
            if selector and texto_nuevo:
                etiquetas = soup.find_all(selector)
                for etiqueta in etiquetas:
                    # Si la IA nos dio el texto_actual, verificamos que sea la etiqueta correcta
                    if texto_actual:
                        if texto_actual in etiqueta.get_text():
                            etiqueta.string = texto_nuevo
                            break
                    else:
                        # Si no hay texto_actual, cambiamos la primera que encontremos
                        etiqueta.string = texto_nuevo
                        break

    # 2. INYECTAR CSS
    if reglas_css:
        bloque_css = "\n/* CAMBIOS DINÁMICOS */\n" + "\n".join(reglas_css) + "\n"
        style_tag = soup.find('style')
        if style_tag:
            style_tag.string = (style_tag.string or "") + bloque_css

    # 3. INYECTAR HTML NUEVO
    if secciones_html:
        for html_seccion in secciones_html:
            seccion_soup = BeautifulSoup(html_seccion, 'html.parser')
            footer = soup.find('footer')
            if footer:
                footer.insert_before(seccion_soup)
            else:
                body = soup.find('body')
                if body: body.append(seccion_soup)
                else: soup.append(seccion_soup)

    return {
        "exito": True,
        "html_nuevo": str(soup),
        "cambios_aplicados": len(reglas_css) + len(secciones_html) + len(reemplazos_texto),
        "cambios_totales": len(reglas_css) + len(secciones_html) + len(reemplazos_texto),
        "aplicados": [{"descripcion": explicacion, "detalle": ""}],
        "fallidos": []
    }