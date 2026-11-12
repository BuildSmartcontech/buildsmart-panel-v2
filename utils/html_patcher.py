# utils/html_patcher.py
# ============================================
# APLICADOR DE CAMBIOS AL HTML - V2.2 (HTML BLINDADO)
# ============================================

import re

def aplicar_cambios(html, cambios):
    if not html or not cambios:
        return {"exito": False, "html_nuevo": html, "error": "Sin cambios"}

    reglas_css = cambios.get("reglas_css", [])
    secciones_html = cambios.get("secciones_html", [])
    explicacion = cambios.get("explicacion", "Cambios aplicados")

    if not reglas_css and not secciones_html:
        return {"exito": False, "html_nuevo": html, "error": "La IA no generó cambios."}

    html_nuevo = html

    # 1. INYECTAR CSS (Si hay)
    if reglas_css:
        bloque_css = "\n/* CAMBIOS DINÁMICOS */\n" + "\n".join(reglas_css) + "\n"
        patron_style = r'(<style[^>]*>)(.*?)(</style>)'
        match = re.search(patron_style, html_nuevo, re.DOTALL | re.IGNORECASE)
        if match:
            style_completo = match.group(0)
            style_nuevo = style_completo.replace("</style>", bloque_css + "</style>", 1)
            html_nuevo = html_nuevo.replace(style_completo, style_nuevo, 1)

    # 2. INYECTAR HTML NUEVO (Si hay)
    if secciones_html:
        bloque_html = "\n<!-- SECCIONES AGREGADAS -->\n" + "\n".join(secciones_html) + "\n"
        
        # Buscamos el footer para inyectar justo antes
        if "<footer" in html_nuevo.lower():
            html_nuevo = re.sub(r'(<footer)', bloque_html + r'\1', html_nuevo, count=1, flags=re.IGNORECASE)
        # Si no hay footer, insertar antes de cerrar el body
        elif "</body>" in html_nuevo.lower():
            html_nuevo = html_nuevo.replace("</body>", bloque_html + "</body>")
        # Si no hay body (caso extremo), al final del string
        else:
            html_nuevo += bloque_html

    return {
        "exito": True,
        "html_nuevo": html_nuevo,
        "cambios_aplicados": len(reglas_css) + len(secciones_html),
        "cambios_totales": len(reglas_css) + len(secciones_html),
        "aplicados": [{"descripcion": explicacion, "detalle": ""}],
        "fallidos": []
    }