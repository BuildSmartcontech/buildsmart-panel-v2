# utils/web_validator.py
# ============================================
# VALIDADOR DE HTML/CSS GENERADO POR LA IA - V2
# ============================================
# V2: Ajustado para soportar imagenes base64 embebidas.
# El conteo de caracteres EXCLUYE las imagenes base64.
# ============================================

import re
import os
import sys
from typing import Dict, List

# Agregar la raiz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.web_prompts import PALABRAS_PROHIBIDAS
except ImportError:
    try:
        from web_prompts import PALABRAS_PROHIBIDAS
    except ImportError:
        PALABRAS_PROHIBIDAS = []


# ============================================
# CONSTANTES
# ============================================

MIN_CARACTERES = 500
MAX_CARACTERES = 500000          # Limite del HTML SIN imagenes base64
MAX_CARACTERES_CON_IMAGENES = 5000000   # Limite absoluto (5 MB)

ETIQUETAS_REQUERIDAS = [
    "<!doctype html>",
    "<html",
    "<head",
    "<body",
    "</html>",
]

ETIQUETAS_SEMANTICAS = [
    "header",
    "main",
    "section",
    "footer",
]

# Patron para detectar imagenes base64
PATRON_BASE64 = r'data:image/[a-z]+;base64,[A-Za-z0-9+/=]+'


# ============================================
# FUNCION AUXILIAR: REMOVER BASE64
# ============================================

def remover_imagenes_base64(html):
    """Remueve las imagenes base64 del HTML para el conteo."""
    return re.sub(PATRON_BASE64, "BASE64_IMAGE", html)


# ============================================
# FUNCION PRINCIPAL: VALIDAR HTML
# ============================================

def validar_html(html):
    """Valida que el HTML cumpla con los estandares."""
    
    errores = []
    advertencias = []
    info = {}
    
    if not html or not html.strip():
        errores.append("HTML vacio")
        return {
            "valido": False,
            "errores": errores,
            "advertencias": advertencias,
            "info": info,
        }
    
    html_lower = html.lower()
    
    # ========== CONTEO INTELIGENTE DE TAMANO ==========
    longitud_total = len(html)
    html_sin_base64 = remover_imagenes_base64(html)
    longitud_contenido = len(html_sin_base64)
    
    # Contar imagenes base64
    imagenes_base64 = re.findall(PATRON_BASE64, html)
    cantidad_imagenes = len(imagenes_base64)
    peso_imagenes = sum(len(img) for img in imagenes_base64)
    
    info["longitud_total"] = longitud_total
    info["longitud_contenido"] = longitud_contenido
    info["cantidad_imagenes_base64"] = cantidad_imagenes
    info["peso_imagenes_base64"] = peso_imagenes
    info["longitud"] = longitud_total  # Compatibilidad
    
    # Validar longitud del CONTENIDO (sin imagenes)
    if longitud_contenido < MIN_CARACTERES:
        errores.append("HTML muy corto (" + str(longitud_contenido) + " caracteres de contenido, minimo " + str(MIN_CARACTERES) + ")")
    
    if longitud_contenido > MAX_CARACTERES:
        errores.append("Contenido HTML muy largo (" + str(longitud_contenido) + " caracteres, maximo " + str(MAX_CARACTERES) + ")")
    
    # Validar longitud TOTAL (con imagenes)
    if longitud_total > MAX_CARACTERES_CON_IMAGENES:
        errores.append("HTML total muy grande (" + str(longitud_total) + " caracteres, maximo " + str(MAX_CARACTERES_CON_IMAGENES) + ")")
    
    # Validar estructura basica
    estructura_ok = 0
    for etiqueta in ETIQUETAS_REQUERIDAS:
        if etiqueta in html_lower:
            estructura_ok += 1
        else:
            errores.append("Falta etiqueta: " + etiqueta)
    
    info["estructura_ok"] = estructura_ok
    info["estructura_total"] = len(ETIQUETAS_REQUERIDAS)
    
    # Validar CSS embebido
    tiene_css = "<style" in html_lower
    info["tiene_css"] = tiene_css
    
    if not tiene_css:
        errores.append("No tiene CSS embebido (falta etiqueta style)")
    
    # Validar responsive
    tiene_viewport = "viewport" in html_lower
    tiene_media = "@media" in html_lower
    info["tiene_viewport"] = tiene_viewport
    info["tiene_media_queries"] = tiene_media
    
    if not tiene_viewport:
        advertencias.append("Falta meta viewport (no es responsive)")
    if not tiene_media:
        advertencias.append("Falta media queries (no es responsive en movil)")
    
    # Validar SEO
    tiene_description = 'name="description"' in html_lower or "name='description'" in html_lower
    tiene_title = "<title>" in html_lower
    info["tiene_description"] = tiene_description
    info["tiene_title"] = tiene_title
    
    if not tiene_description:
        advertencias.append("Falta meta description (SEO)")
    if not tiene_title:
        errores.append("Falta etiqueta title")
    
    # Validar etiquetas semanticas
    semanticas_encontradas = []
    for etiqueta in ETIQUETAS_SEMANTICAS:
        if "<" + etiqueta in html_lower:
            semanticas_encontradas.append(etiqueta)
    info["semanticas_encontradas"] = semanticas_encontradas
    
    if len(semanticas_encontradas) < 2:
        advertencias.append("Pocas etiquetas semanticas (" + str(len(semanticas_encontradas)) + "/" + str(len(ETIQUETAS_SEMANTICAS)) + ")")
    
    # Validar palabras prohibidas (SOLO en contenido, no en base64)
    html_contenido_lower = html_sin_base64.lower()
    palabras_encontradas = []
    for palabra in PALABRAS_PROHIBIDAS:
        if palabra in html_contenido_lower:
            palabras_encontradas.append(palabra)
    
    info["palabras_prohibidas"] = palabras_encontradas
    
    if palabras_encontradas:
        advertencias.append("Palabras prohibidas encontradas: " + ", ".join(palabras_encontradas[:5]))
    
    # Validar imagenes externas
    imagenes_externas = re.findall(r'src=["\']https?://[^"\']+["\']', html_lower)
    info["imagenes_externas"] = len(imagenes_externas)
    
    if imagenes_externas:
        advertencias.append("Tiene " + str(len(imagenes_externas)) + " imagenes externas")
    
    # Validar CDN externos
    cdn_externos = re.findall(r'(?:bootstrap|tailwind|jquery|cdn\.)', html_contenido_lower)
    info["cdn_externos"] = len(cdn_externos)
    
    if cdn_externos:
        advertencias.append("Usa CDN externos (" + str(len(cdn_externos)) + " referencias)")
    
    # Validar dark mode (NUEVO)
    tiene_dark_mode = "prefers-color-scheme" in html_lower
    info["tiene_dark_mode"] = tiene_dark_mode
    
    if tiene_dark_mode:
        errores.append("Tiene dark mode automatico (PROHIBIDO)")
    
    valido = len(errores) == 0
    
    return {
        "valido": valido,
        "errores": errores,
        "advertencias": advertencias,
        "info": info,
    }


# ============================================
# FUNCION: VALIDAR CSS
# ============================================

def validar_css(css):
    """Valida que el CSS sea correcto"""
    
    errores = []
    advertencias = []
    
    if not css or not css.strip():
        return {
            "valido": True,
            "errores": [],
            "advertencias": ["CSS vacio"],
        }
    
    abiertas = css.count("{")
    cerradas = css.count("}")
    
    if abiertas != cerradas:
        errores.append("Llaves desbalanceadas (" + str(abiertas) + " abiertas, " + str(cerradas) + " cerradas)")
    
    parentesis_abiertos = css.count("(")
    parentesis_cerrados = css.count(")")
    
    if parentesis_abiertos != parentesis_cerrados:
        advertencias.append("Parentesis desbalanceados")
    
    return {
        "valido": len(errores) == 0,
        "errores": errores,
        "advertencias": advertencias,
    }


# ============================================
# FUNCION: VALIDAR COMPLETO
# ============================================

def validar_completo(html):
    """Valida HTML completo (incluye CSS embebido)."""
    
    resultado_html = validar_html(html)
    
    css_match = re.search(r'<style[^>]*>(.*?)</style>', html, re.DOTALL | re.IGNORECASE)
    
    if css_match:
        css = css_match.group(1)
        resultado_css = validar_css(css)
        
        resultado_html["errores"].extend(resultado_css["errores"])
        resultado_html["advertencias"].extend(resultado_css["advertencias"])
        resultado_html["valido"] = len(resultado_html["errores"]) == 0
        resultado_html["info"]["css_extraido"] = True
    else:
        resultado_html["info"]["css_extraido"] = False
    
    return resultado_html


# ============================================
# FUNCION: LIMPIAR HTML
# ============================================

def limpiar_html(html):
    """Limpia el HTML generado por la IA."""
    
    if not html:
        return ""
    
    # Eliminar bloques markdown
    html = re.sub(r'```html\s*', '', html)
    html = re.sub(r'```\s*$', '', html)
    html = re.sub(r'```', '', html)
    
    # Eliminar espacios al inicio y final
    html = html.strip()
    
    # Eliminar comentarios de IA
    html = re.sub(
        r'<!--\s*(?:generado por|creado por|producido por|ia|ai|asistente|chatgpt|claude)\s*.*?-->',
        '',
        html,
        flags=re.IGNORECASE | re.DOTALL
    )
    
    # Limpiar espacios multiples
    html = re.sub(r'\n\s*\n\s*\n', '\n\n', html)
    
    return html


# ============================================
# FUNCION: RESUMEN DE VALIDACION
# ============================================

def resumen_validacion(resultado):
    """Genera un resumen legible del resultado."""
    
    lineas = []
    lineas.append("=" * 50)
    lineas.append("RESUMEN DE VALIDACION")
    lineas.append("=" * 50)
    
    if resultado["valido"]:
        lineas.append("ESTADO: VALIDO")
    else:
        lineas.append("ESTADO: INVALIDO")
    
    info = resultado.get("info", {})
    lineas.append("")
    lineas.append("INFORMACION:")
    lineas.append("   Longitud total: " + str(info.get("longitud_total", 0)) + " caracteres")
    lineas.append("   Longitud contenido: " + str(info.get("longitud_contenido", 0)) + " caracteres")
    lineas.append("   Imagenes base64: " + str(info.get("cantidad_imagenes_base64", 0)))
    lineas.append("   Peso imagenes: " + str(info.get("peso_imagenes_base64", 0)) + " caracteres")
    lineas.append("   Estructura: " + str(info.get("estructura_ok", 0)) + "/" + str(info.get("estructura_total", 0)))
    lineas.append("   Tiene CSS: " + str(info.get("tiene_css", False)))
    lineas.append("   Tiene dark mode: " + str(info.get("tiene_dark_mode", False)))
    lineas.append("   Etiquetas semanticas: " + str(len(info.get("semanticas_encontradas", []))))
    lineas.append("   Palabras prohibidas: " + str(len(info.get("palabras_prohibidas", []))))
    
    if resultado["errores"]:
        lineas.append("")
        lineas.append("ERRORES (" + str(len(resultado["errores"])) + "):")
        for error in resultado["errores"]:
            lineas.append("   - " + error)
    
    if resultado["advertencias"]:
        lineas.append("")
        lineas.append("ADVERTENCIAS (" + str(len(resultado["advertencias"])) + "):")
        for adv in resultado["advertencias"]:
            lineas.append("   - " + adv)
    
    lineas.append("=" * 50)
    
    return "\n".join(lineas)


# ============================================
# FUNCION: TEST RAPIDO
# ============================================

def test_rapido():
    """Prueba rapida del validador."""
    
    print("=" * 60)
    print("PROBANDO VALIDADOR DE HTML/CSS V2")
    print("=" * 60)
    
    # --- Prueba 1: HTML valido ---
    print("\n" + "=" * 60)
    print("PRUEBA 1: HTML valido (template)")
    print("=" * 60)
    
    try:
        from utils.web_templates import renderizar_template
    except ImportError:
        from web_templates import renderizar_template
    
    datos = {
        "nombre_negocio": "Construcciones ABC",
        "titulo": "Construcciones ABC",
        "descripcion_seo": "30 anos de experiencia",
        "titulo_hero": "Construimos tu hogar",
        "subtitulo_hero": "30 anos en Bogota",
        "servicios": ["Obra Civil", "Reformas"],
    }
    
    html_valido = renderizar_template("Landing Page", datos)
    resultado = validar_completo(html_valido)
    print(resumen_validacion(resultado))
    
    # --- Prueba 2: HTML con imagen base64 ---
    print("\n" + "=" * 60)
    print("PRUEBA 2: HTML con imagen base64 simulada")
    print("=" * 60)
    
    # Simular un HTML con una imagen base64 grande
    imagen_fake = "data:image/jpeg;base64," + ("A" * 200000)  # 200 KB
    
    html_con_imagen = '<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width">\n<meta name="description" content="Test">\n<title>Test</title>\n<style>\nbody { font-family: sans-serif; }\n@media (max-width: 768px) { body { font-size: 14px; } }\n</style>\n</head>\n<body>\n<header><h1>Test</h1><img src="' + imagen_fake + '" alt="Hero"></header>\n<main>\n<section>\n<p>Contenido de prueba real.</p>\n</section>\n</main>\n<footer><p>Footer</p></footer>\n</body>\n</html>'
    
    print("Tamano total: " + str(len(html_con_imagen)))
    
    resultado = validar_completo(html_con_imagen)
    print(resumen_validacion(resultado))
    
    # --- Prueba 3: HTML con dark mode (debe fallar) ---
    print("\n" + "=" * 60)
    print("PRUEBA 3: HTML con dark mode (debe FALLAR)")
    print("=" * 60)
    
    html_dark = '<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width">\n<meta name="description" content="Test">\n<title>Test</title>\n<style>\nbody { background: white; color: black; }\n@media (prefers-color-scheme: dark) { body { background: black; color: white; } }\n@media (max-width: 768px) { body { font-size: 14px; } }\n</style>\n</head>\n<body>\n<header><h1>Test</h1></header>\n<main>\n<section>\n<p>Contenido de prueba con dark mode.</p>\n</section>\n</main>\n<footer><p>Footer</p></footer>\n</body>\n</html>'
    
    resultado = validar_completo(html_dark)
    print(resumen_validacion(resultado))


# ============================================
# EJECUTAR PRUEBA
# ============================================

if __name__ == "__main__":
    test_rapido()