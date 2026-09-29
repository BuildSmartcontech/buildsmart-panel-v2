# utils/html_patcher.py
# ============================================
# APLICADOR DE CAMBIOS AL HTML - V1.2
# ============================================
# V1.2: Retorna informacion detallada por cambio
# (aplicados con descripcion + fallidos con razon)
# ============================================

import re
import sys
import os
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

POLLINATIONS_URL = "https://image.pollinations.ai/prompt"


# ============================================
# UTILIDADES
# ============================================

def generar_url_pollinations(prompt, width=1200, height=800, seed=None):
    if not prompt:
        prompt = "professional business photo"
    prompt_encoded = urllib.parse.quote(prompt.strip())
    url = POLLINATIONS_URL + "/" + prompt_encoded + "?width=" + str(width) + "&height=" + str(height) + "&nologo=true&enhance=true"
    if seed is not None:
        url += "&seed=" + str(seed)
    return url


def _descripcion_cambio(cambio):
    """Genera una descripcion legible del cambio."""
    tipo = cambio.get("tipo", "desconocido")
    if tipo == "reemplazar_imagen":
        return "Cambiar imagen '" + str(cambio.get('target_alt', '?')) + "'"
    elif tipo == "cambiar_todas_las_imagenes":
        return "Cambiar TODAS las imagenes por: " + str(cambio.get('prompt_general', '?'))[:50]
    elif tipo == "cambiar_color_fondo":
        return "Cambiar fondo (" + str(cambio.get('selector_class') or cambio.get('selector_tag') or cambio.get('selector', '?')) + ") a " + str(cambio.get('color', '?'))
    elif tipo == "cambiar_color_texto":
        return "Cambiar color de <" + str(cambio.get('selector_tag', '?')) + "> a " + str(cambio.get('color', '?'))
    elif tipo == "cambiar_texto":
        return "Cambiar texto de <" + str(cambio.get('selector_tag', '?')) + ">"
    return "Cambio tipo: " + tipo


# ============================================
# REEMPLAZAR IMAGENES
# ============================================

def _reemplazar_imagen_por_alt(html, target_alt, nuevo_prompt):
    if not target_alt or not nuevo_prompt:
        return html, False

    alt_escaped = re.escape(target_alt)
    patron = r'<img\s+([^>]*?)alt\s*=\s*["\']' + alt_escaped + r'["\']([^>]*?)>'
    match = re.search(patron, html, re.IGNORECASE | re.DOTALL)

    if not match:
        patron2 = r'<img\s+([^>]*?)alt\s*=\s*["\'][^"\']*' + alt_escaped[:15] + r'[^"\']*["\']([^>]*?)>'
        match = re.search(patron2, html, re.IGNORECASE | re.DOTALL)

    if not match:
        return html, False

    nueva_url = generar_url_pollinations(nuevo_prompt)
    tag_completo = match.group(0)

    if 'src=' in tag_completo.lower():
        tag_nuevo = re.sub(r'src\s*=\s*["\'][^"\']*["\']', 'src="' + nueva_url + '"', tag_completo, flags=re.IGNORECASE)
    else:
        tag_nuevo = tag_completo.replace('<img', '<img src="' + nueva_url + '"', 1)

    html_nuevo = html.replace(tag_completo, tag_nuevo, 1)
    return html_nuevo, True


def _reemplazar_imagen_placeholder(html, nuevo_prompt):
    patrones = [
        r'<img\s+[^>]*src\s*=\s*["\']\s*["\'][^>]*>',
        r'<img\s+[^>]*src\s*=\s*["\']#["\'][^>]*>',
        r'<img\s+[^>]*src\s*=\s*["\']data:image[^"\']{0,50}["\'][^>]*>',
    ]
    nueva_url = generar_url_pollinations(nuevo_prompt)
    for patron in patrones:
        match = re.search(patron, html, re.IGNORECASE)
        if match:
            tag_completo = match.group(0)
            tag_nuevo = re.sub(r'src\s*=\s*["\'][^"\']*["\']', 'src="' + nueva_url + '"', tag_completo, flags=re.IGNORECASE)
            html = html.replace(tag_completo, tag_nuevo, 1)
            return html, True
    return html, False


# ============================================
# COLORES
# ============================================

def _cambiar_color_texto(html, selector_tag, color):
    if not selector_tag or not color:
        return html, False
    if not color.startswith("#"):
        color = "#" + color
    patron_style = r'(<style[^>]*>)(.*?)(</style>)'
    match = re.search(patron_style, html, re.DOTALL | re.IGNORECASE)
    if not match:
        return html, False
    style_completo = match.group(0)
    selector = selector_tag.strip()
    regla = "\n" + selector + " { color: " + color + " !important; }\n"
    style_nuevo = style_completo.replace("</style>", regla + "</style>", 1)
    html_nuevo = html.replace(style_completo, style_nuevo, 1)
    return html_nuevo, True


def _cambiar_color_fondo(html, selector, color):
    if not selector or not color:
        return html, False
    if not color.startswith("#"):
        color = "#" + color
    patron_style = r'(<style[^>]*>)(.*?)(</style>)'
    match = re.search(patron_style, html, re.DOTALL | re.IGNORECASE)
    if not match:
        return html, False
    style_completo = match.group(0)
    selector = selector.strip().lower()
    etiquetas_html = ["body", "html", "main", "header", "footer", "section", "div"]
    if selector in etiquetas_html:
        selector_css = selector
    elif selector.startswith((".", "#")):
        selector_css = selector
    elif selector.startswith("class_") or selector.startswith("clase_"):
        nombre = selector.replace("class_", "").replace("clase_", "")
        selector_css = "." + nombre
    else:
        selector_css = "." + selector
    regla = "\n" + selector_css + " { background-color: " + color + " !important; }\n"
    style_nuevo = style_completo.replace("</style>", regla + "</style>", 1)
    html_nuevo = html.replace(style_completo, style_nuevo, 1)
    return html_nuevo, True


# ============================================
# TEXTO
# ============================================

def _cambiar_texto(html, selector_tag, texto_actual, texto_nuevo):
    if not texto_actual or not texto_nuevo:
        return html, False
    patron = r'(<' + re.escape(selector_tag) + r'[^>]*>)\s*' + re.escape(texto_actual) + r'\s*(</' + re.escape(selector_tag) + r'>)'
    match = re.search(patron, html, re.DOTALL | re.IGNORECASE)
    if not match:
        return html, False
    reemplazo = match.group(1) + texto_nuevo + match.group(2)
    html_nuevo = html.replace(match.group(0), reemplazo, 1)
    return html_nuevo, True


# ============================================
# TODAS LAS IMAGENES
# ============================================

def _cambiar_todas_las_imagenes(html, prompt_general):
    if not prompt_general:
        return html, False, 0

    patron_img = r'<img\s+([^>]*?)>'
    matches = list(re.finditer(patron_img, html, re.IGNORECASE))
    if not matches:
        return html, False, 0

    html_nuevo = html
    contador = 0

    sufijos = [
        ", presentacion profesional",
        ", close-up",
        ", sobre mesa",
        ", en plato blanco",
        ", fotografia de producto",
    ]

    for i, match in enumerate(matches):
        tag_completo = match.group(0)
        alt_match = re.search(r'alt\s*=\s*["\']([^"\']*)["\']', tag_completo, re.IGNORECASE)
        alt = alt_match.group(1) if alt_match else ""

        if alt and len(alt) > 3:
            prompt_especifico = prompt_general + ", " + alt + sufijos[i % len(sufijos)]
        else:
            prompt_especifico = prompt_general + sufijos[i % len(sufijos)]

        nueva_url = generar_url_pollinations(prompt_especifico, seed=i * 137)

        if 'src=' in tag_completo.lower():
            tag_nuevo = re.sub(r'src\s*=\s*["\'][^"\']*["\']', 'src="' + nueva_url + '"', tag_completo, flags=re.IGNORECASE)
        else:
            tag_nuevo = tag_completo.replace('<img', '<img src="' + nueva_url + '"', 1)

        html_nuevo = html_nuevo.replace(tag_completo, tag_nuevo, 1)
        contador += 1

    return html_nuevo, contador > 0, contador


# ============================================
# FUNCION PRINCIPAL
# ============================================

def aplicar_cambios(html, cambios):
    """
    Aplica una lista de cambios al HTML.

    Returns:
        {
            "exito": bool,
            "html_nuevo": str,
            "cambios_aplicados": int,
            "cambios_totales": int,
            "aplicados": [{"descripcion": "...", "detalle": "..."}],
            "fallidos": [{"descripcion": "...", "razon": "...", "sugerencia": "..."}]
        }
    """
    if not html or not cambios:
        return {
            "exito": False,
            "html_nuevo": html,
            "cambios_aplicados": 0,
            "cambios_totales": 0,
            "aplicados": [],
            "fallidos": [{"descripcion": "Sin cambios", "razon": "Lista vacia", "sugerencia": ""}]
        }

    html_actual = html
    aplicados = []
    fallidos = []

    for i, cambio in enumerate(cambios, 1):
        tipo = cambio.get("tipo", "")
        descripcion = _descripcion_cambio(cambio)
        aplicado = False
        detalle = ""
        razon_fallo = ""
        sugerencia = ""

        try:
            if tipo == "reemplazar_imagen":
                target_alt = cambio.get("target_alt", "")
                nuevo_prompt = cambio.get("nuevo_prompt_imagen", "")
                if target_alt and nuevo_prompt:
                    html_actual, aplicado = _reemplazar_imagen_por_alt(html_actual, target_alt, nuevo_prompt)
                    if not aplicado:
                        html_actual, aplicado = _reemplazar_imagen_placeholder(html_actual, nuevo_prompt)
                        if aplicado:
                            detalle = "placeholder reemplazado"
                    if not aplicado:
                        razon_fallo = "No encontre imagen con alt='" + target_alt + "'"
                        sugerencia = "Verifica el nombre exacto o prueba 'cambia todas las imagenes'"

            elif tipo == "cambiar_todas_las_imagenes":
                prompt = cambio.get("prompt_general", "")
                if prompt:
                    html_actual, aplicado, n_imgs = _cambiar_todas_las_imagenes(html_actual, prompt)
                    if aplicado:
                        detalle = str(n_imgs) + " imagenes cambiadas"
                    else:
                        razon_fallo = "No hay imagenes <img> en el HTML"
                        sugerencia = "El HTML no tiene imagenes para cambiar"

            elif tipo == "cambiar_color_texto":
                selector = cambio.get("selector_tag", "")
                color = cambio.get("color", "")
                html_actual, aplicado = _cambiar_color_texto(html_actual, selector, color)
                if aplicado:
                    detalle = "Color " + color + " aplicado a <" + selector + ">"
                else:
                    razon_fallo = "No hay <style> en el HTML"
                    sugerencia = "El HTML no tiene seccion <style>"

            elif tipo == "cambiar_color_fondo":
                selector = cambio.get("selector_class") or cambio.get("selector_tag") or cambio.get("selector") or ""
                color = cambio.get("color", "")
                html_actual, aplicado = _cambiar_color_fondo(html_actual, selector, color)
                if aplicado:
                    detalle = "Fondo " + color + " aplicado a " + selector
                else:
                    razon_fallo = "No hay <style> en el HTML"

            elif tipo == "cambiar_texto":
                html_actual, aplicado = _cambiar_texto(
                    html_actual,
                    cambio.get("selector_tag", ""),
                    cambio.get("texto_actual", ""),
                    cambio.get("texto_nuevo", "")
                )
                if not aplicado:
                    razon_fallo = "No encontre el texto exacto '" + str(cambio.get('texto_actual', ''))[:30] + "'"
                    sugerencia = "Copia el texto exacto como aparece en la web"

            else:
                razon_fallo = "Tipo de cambio desconocido: " + tipo

            if aplicado:
                aplicados.append({"descripcion": descripcion, "detalle": detalle})
            else:
                fallidos.append({
                    "descripcion": descripcion,
                    "razon": razon_fallo or "No se pudo aplicar",
                    "sugerencia": sugerencia or ""
                })

        except Exception as e:
            fallidos.append({
                "descripcion": descripcion,
                "razon": "Error tecnico: " + str(e)[:80],
                "sugerencia": "Intenta reformular la instruccion"
            })

    if html_actual.strip() == html.strip():
        return {
            "exito": False,
            "html_nuevo": html,
            "cambios_aplicados": 0,
            "cambios_totales": len(cambios),
            "aplicados": [],
            "fallidos": fallidos if fallidos else [{"descripcion": "HTML sin cambios", "razon": "Ningun cambio produjo modificacion real", "sugerencia": ""}]
        }

    return {
        "exito": len(aplicados) > 0,
        "html_nuevo": html_actual,
        "cambios_aplicados": len(aplicados),
        "cambios_totales": len(cambios),
        "aplicados": aplicados,
        "fallidos": fallidos
    }


# ============================================
# TEST
# ============================================

def test_patcher():
    print("=" * 60)
    print("TEST HTML PATCHER V1.2")
    print("=" * 60)

    html = """<!DOCTYPE html>
<html><head>
<style>
body { background: #fff; }
h1 { color: #333; }
</style>
</head><body>
<h1>Titulo</h1>
<img src="{{HERO_IMAGE}}" alt="Hero">
<img src="" alt="Cupcakes">
<img src="" alt="Bombones">
</body></html>"""

    cambios = [
        {"tipo": "reemplazar_imagen", "target_alt": "Cupcakes", "nuevo_prompt_imagen": "colorful cupcakes"},
        {"tipo": "reemplazar_imagen", "target_alt": "NO_EXISTE", "nuevo_prompt_imagen": "algo"},
        {"tipo": "cambiar_color_fondo", "selector_class": "body", "color": "#FFD700"},
    ]

    resultado = aplicar_cambios(html, cambios)
    print("\nExito: " + str(resultado["exito"]))
    print("Aplicados: " + str(resultado["cambios_aplicados"]) + "/" + str(resultado["cambios_totales"]))

    print("\n--- APLICADOS ---")
    for a in resultado["aplicados"]:
        print("  OK: " + a["descripcion"] + " | " + a.get("detalle", ""))

    print("\n--- FALLIDOS ---")
    for f in resultado["fallidos"]:
        print("  FALLO: " + f["descripcion"])
        print("    Razon: " + f["razon"])
        if f.get("sugerencia"):
            print("    Sugerencia: " + f["sugerencia"])

    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_patcher()