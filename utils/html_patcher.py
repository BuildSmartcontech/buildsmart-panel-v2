# utils/html_patcher.py
# ============================================
# APLICADOR DE CAMBIOS AL HTML - V2.0 (CSS INJECTION)
# ============================================

import re

def aplicar_cambios(html, cambios):
    if not html or not cambios:
        return {"exito": False, "html_nuevo": html, "error": "Sin cambios"}

    # Extraemos las reglas CSS que generó la IA
    reglas_css = cambios.get("reglas_css", [])
    explicacion = cambios.get("explicacion", "Cambios aplicados")

    if not reglas_css:
        return {"exito": False, "html_nuevo": html, "error": "La IA no generó reglas CSS."}

    # Unimos todas las reglas en un solo bloque de CSS
    bloque_css = "\n/* CAMBIOS DINÁMICOS */\n" + "\n".join(reglas_css) + "\n"

    # Buscamos la etiqueta <style> para inyectar al final
    patron_style = r'(<style[^>]*>)(.*?)(</style>)'
    match = re.search(patron_style, html, re.DOTALL | re.IGNORECASE)
    
    if not match:
        return {"exito": False, "html_nuevo": html, "error": "No hay etiqueta <style> en el HTML para inyectar CSS."}

    # Inyectamos el CSS antes de cerrar </style>
    style_completo = match.group(0)
    style_nuevo = style_completo.replace("</style>", bloque_css + "</style>", 1)
    html_nuevo = html.replace(style_completo, style_nuevo, 1)

    return {
        "exito": True,
        "html_nuevo": html_nuevo,
        "cambios_aplicados": len(reglas_css),
        "cambios_totales": len(reglas_css),
        "aplicados": [{"descripcion": explicacion, "detalle": ""}],
        "fallidos": []
    }