# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V6.0
# ============================================
# V6.0: Recibe campos extendidos (direccion, horarios, redes,
#       anio, whatsapp, email_contacto) + instrucciones dinamicas
# V5.0: Director de Arte + datos en web_prompts_data
# V4.3: Diseno premium + compatibilidad editor viejo
# ============================================

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


from utils.web_prompts_data import (
    PALABRAS_PROHIBIDAS,
    DIRECTOR_DE_ARTE_PROMPT,
    REGLAS_CSS_PREMIUM,
    REGLAS_CODIGO,
    REGLAS_IMAGENES,
    REGLAS_SALIDA,
    construir_reglas_contenido,
    construir_instrucciones_dinamicas,
)


# ============================================
# PROMPT DE GENERACION (V6.0)
# ============================================

def generar_prompt_web(
    nombre_negocio, sector, descripcion, publico_objetivo="",
    diferenciadores="", tono="Profesional", colores="#0f3460, #f39c12",
    tipo_pagina="Landing Page", diseno="Moderno", secciones=None,
    logica="Estatica", funcionalidades=None, opciones_usuario=None,
    # Campos extendidos V6.0
    direccion="", ciudad="", pais="", horarios="",
    instagram="", facebook="", tiktok="",
    anio_fundacion="", email_contacto="", whatsapp_negocio="",
):
    """Prompt V6.0 con instrucciones dinamicas segun datos disponibles."""

    if secciones is None:
        secciones = ["Hero", "Servicios", "Sobre Nosotros", "Contacto"]
    if funcionalidades is None:
        funcionalidades = ["SEO optimizado", "Animaciones"]

    secciones_texto = "\n".join(["   - " + s for s in secciones])
    funcionalidades_texto = "\n".join(["   - " + f for f in funcionalidades])
    lista_negra = ", ".join(PALABRAS_PROHIBIDAS[:20])

    reglas_contenido = construir_reglas_contenido(sector, lista_negra)

    # Instrucciones dinamicas segun datos disponibles
    datos_negocio_completos = {
        "direccion": direccion,
        "ciudad": ciudad,
        "pais": pais,
        "horarios": horarios,
        "instagram": instagram,
        "facebook": facebook,
        "tiktok": tiktok,
        "anio_fundacion": anio_fundacion,
        "email_contacto": email_contacto,
        "whatsapp_negocio": whatsapp_negocio,
    }
    instrucciones_dinamicas = construir_instrucciones_dinamicas(datos_negocio_completos)

    # Construir seccion de INFO DEL NEGOCIO (solo campos con valor)
    info_negocio = [
        "- Nombre: " + nombre_negocio,
        "- Sector: " + sector,
        "- Descripcion: " + descripcion,
    ]
    if publico_objetivo:
        info_negocio.append("- Publico objetivo: " + publico_objetivo)
    if diferenciadores:
        info_negocio.append("- Diferenciadores: " + diferenciadores)
    if ciudad:
        ciudad_full = ciudad + (", " + pais if pais else "")
        info_negocio.append("- Ubicacion: " + ciudad_full)
    if direccion:
        info_negocio.append("- Direccion: " + direccion)
    if anio_fundacion:
        info_negocio.append("- Ano de fundacion: " + anio_fundacion)
    if email_contacto:
        info_negocio.append("- Email de contacto: " + email_contacto)
    if whatsapp_negocio:
        info_negocio.append("- WhatsApp: " + whatsapp_negocio)
    if horarios:
        info_negocio.append("- Horarios: " + horarios)
    if instagram:
        info_negocio.append("- Instagram: @" + instagram.lstrip("@"))
    if facebook:
        info_negocio.append("- Facebook: " + facebook)
    if tiktok:
        info_negocio.append("- TikTok: @" + tiktok.lstrip("@"))

    info_negocio_texto = "\n".join(info_negocio)

    prompt = (
        DIRECTOR_DE_ARTE_PROMPT +
        "\n\n=========================================================\n"
        "GENERA LA PAGINA WEB COMPLETA\n"
        "=========================================================\n\n"
        "## INFORMACION DEL NEGOCIO\n" + info_negocio_texto + "\n\n"
        "## ESTILO\n"
        "- Tipo de pagina: " + tipo_pagina + "\n"
        "- Diseno visual: " + diseno + "\n"
        "- Tono de comunicacion: " + tono + "\n"
        "- Colores principales: " + colores + "\n"
        "- Tipografia: Moderna, legible, responsive (usa Google Fonts)\n\n"
        "## SECCIONES REQUERIDAS (en este orden)\n" + secciones_texto + "\n\n"
        "## LOGICA\n" + logica + "\n\n"
        "## FUNCIONALIDADES ESPECIALES\n" + funcionalidades_texto + "\n\n"
        + instrucciones_dinamicas +
        "\n\n" + REGLAS_CSS_PREMIUM +
        reglas_contenido +
        REGLAS_CODIGO +
        REGLAS_IMAGENES +
        REGLAS_SALIDA
    )

    return prompt


# ============================================
# PROMPT DE EDICION (VIEJO - COMPATIBILIDAD)
# ============================================

def generar_prompt_edicion(html_actual, instruccion):
    """Prompt para editar una web existente (editor V1)."""

    prompt = (
        "Eres un disenador web profesional. El usuario quiere hacer un cambio en su pagina web.\n\n"
        "## INSTRUCCION DEL USUARIO:\n"
        + instruccion + "\n\n"
        "## CODIGO HTML ACTUAL (COMPLETO):\n"
        + html_actual + "\n\n"
        "## REGLAS ESTRICTAS:\n"
        "1. Devuelve el CODIGO HTML COMPLETO, no solo la parte modificada.\n"
        "2. DEBES incluir: <!DOCTYPE html>, <html>, <head>, <body>, </html>.\n"
        "3. Modifica SOLO lo que el usuario pide, manten el resto igual.\n"
        "4. Manten el CSS embebido en <style>.\n"
        "5. NO uses palabras prohibidas de IA.\n"
        "6. NO incluyas explicaciones ni comentarios fuera del HTML.\n"
        "7. NO uses bloques markdown.\n"
        "8. NO agregues @media (prefers-color-scheme: dark).\n"
        "9. NO inviertas los colores.\n"
        "10. Manten el fondo claro y texto oscuro.\n\n"
        "## FORMATO DE SALIDA:\n"
        "Devuelve SOLO el codigo HTML completo, empezando con <!DOCTYPE html> y terminando con </html>.\n\n"
        "Codigo HTML completo actualizado:"
    )

    return prompt


# ============================================
# PROMPT DE EDICION ESTRUCTURADA (JSON) - V2
# ============================================

def generar_prompt_edicion_estructurada(estructura_resumen, instruccion, contexto_negocio=""):
    """Prompt para edicion estructurada con JSON."""

    prompt = f"""Eres un editor web estructurado. El usuario quiere hacer cambios en su web.

## CONTEXTO DEL NEGOCIO
{contexto_negocio if contexto_negocio else "Negocio generico"}

## ESTRUCTURA ACTUAL DEL HTML
{estructura_resumen}

## INSTRUCCION DEL USUARIO
{instruccion}

## TU TAREA
Analizar la instruccion y devolver un JSON con la lista de cambios EXACTOS.

FORMATO DE RESPUESTA (SOLO JSON, sin explicaciones):
{{
  "cambios": [
    {{
      "tipo": "reemplazar_imagen",
      "target_alt": "Cupcakes",
      "nuevo_prompt_imagen": "colorful cupcakes with frosting, professional food photography"
    }},
    {{
      "tipo": "cambiar_color_fondo",
      "selector_class": "body",
      "color": "#FFD700"
    }}
  ],
  "explicacion": "Cambie las imagenes y el fondo"
}}

## TIPOS DE CAMBIOS DISPONIBLES

1. **reemplazar_imagen**: Cambiar UNA imagen especifica
   - target_alt: el alt EXACTO de la imagen
   - nuevo_prompt_imagen: descripcion EN INGLES de la imagen

2. **cambiar_todas_las_imagenes**: Cambiar TODAS las imagenes
   - prompt_general: tema general EN INGLES

3. **cambiar_color_fondo**: Cambiar color de fondo
   - selector_class: "body" | "html" | "main" | "header" | "footer" | "section" | ".nombre-clase"
   - IMPORTANTE: "body" es la etiqueta completa, NO es ".body"
   - color: codigo hex

4. **cambiar_color_texto**: Cambiar color de texto
   - selector_tag: "h1" | "h2" | "h3" | "p" | "a"
   - color: codigo hex

5. **cambiar_texto**: Reemplazar texto
   - selector_tag, texto_actual, texto_nuevo

## REGLAS CRITICAS

1. **NO INVENTES datos** (telefonos, direcciones, emails, anos).
2. **SI EL USUARIO DICE "TODAS LAS IMAGENES"** usa `cambiar_todas_las_imagenes`.
3. **Los prompts de imagen DEBEN estar en INGLES** y describir el PRODUCTO, no el local.
4. **Devuelve SOLO JSON**.
5. Si dice "fondo de color X" usa `cambiar_color_fondo` con selector_class="body"
6. Si dice "titulos de color X" usa varios `cambiar_color_texto` para h1, h2, h3

## RESPUESTA (SOLO JSON):"""

    return prompt


# ============================================
# PROMPTS AUXILIARES
# ============================================

def generar_prompt_resumen(html):
    return (
        "Analiza esta pagina web y genera un resumen ejecutivo de maximo 150 palabras.\n\n"
        "## HTML:\n" + html[:3000] + "\n\n"
        "## REGLAS:\n"
        "1. Maximo 150 palabras.\n"
        "2. Enfocate en propuesta de valor.\n"
        "3. NO frases genericas.\n\n"
        "Resumen ejecutivo:"
    )


def generar_prompt_seo(nombre_negocio, sector, descripcion):
    return (
        "Genera meta tags SEO.\n\n"
        "## INFO:\n"
        "- Nombre: " + nombre_negocio + "\n"
        "- Sector: " + sector + "\n"
        "- Descripcion: " + descripcion + "\n\n"
        "## FORMATO (JSON):\n"
        '{\n    "title": "max 60 chars",\n    "description": "max 160 chars",\n    "keywords": ["p1", "p2", "p3"]\n}\n\n'
        "Devuelve SOLO el JSON."
    )


def validar_html_generado(html):
    errores = []
    advertencias = []

    if not html:
        return {"errores": ["HTML vacio"], "advertencias": [], "valido": False}

    if len(html) < 500:
        errores.append("HTML muy corto (" + str(len(html)) + " chars)")
    if len(html) > 500000:
        errores.append("HTML muy largo (" + str(len(html)) + " chars)")

    html_lower = html.lower()

    if "<!doctype html>" not in html_lower:
        advertencias.append("Falta DOCTYPE")
    if "<html" not in html_lower:
        errores.append("Falta etiqueta html")
    if "<head>" not in html_lower:
        errores.append("Falta head")
    if "<body>" not in html_lower:
        errores.append("Falta body")
    if "</html>" not in html_lower:
        errores.append("Falta cierre html")

    for palabra in PALABRAS_PROHIBIDAS:
        if palabra in html_lower:
            advertencias.append("Palabra prohibida: " + palabra)
            break

    if "prefers-color-scheme: dark" in html_lower or "prefers-color-scheme:dark" in html_lower:
        errores.append("Tiene dark mode - PROHIBIDO")

    return {"errores": errores, "advertencias": advertencias, "valido": len(errores) == 0}


# ============================================
# TEST
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("TEST PROMPTS V6.0 (con campos extendidos)")
    print("=" * 60)

    # Test 1: negocio basico (sin campos extra)
    p1 = generar_prompt_web(
        nombre_negocio="Test Basico", sector="alimentos",
        descripcion="Test desc", publico_objetivo="Test pub",
        diferenciadores="Test dif",
    )
    print(f"\n1. Prompt basico: {len(p1)} chars")
    print(f"   Director de Arte: {'SI' if 'Director de Arte' in p1 else 'NO'}")
    print(f"   Sin Ubicacion:   {'OK' if 'SECCION UBICACION' not in p1 else 'FALLO'}")
    print(f"   Sin Horarios:    {'OK' if 'SECCION HORARIOS' not in p1 else 'FALLO'}")

    # Test 2: negocio completo con campos nuevos
    p2 = generar_prompt_web(
        nombre_negocio="Panaderia Premium", sector="alimentos",
        descripcion="Panaderia artesanal", publico_objetivo="familias",
        diferenciadores="masa madre",
        direccion="Calle 123 #45-67",
        ciudad="Bogota", pais="Colombia",
        horarios="Lun-Vie 8am-6pm",
        instagram="panaderia", facebook="panaderia", tiktok="panaderia",
        anio_fundacion="2018",
        email_contacto="info@panaderia.com",
        whatsapp_negocio="+573001234567",
    )
    print(f"\n2. Prompt completo: {len(p2)} chars")
    print(f"   Ubicacion: {'SI' if 'SECCION UBICACION' in p2 else 'NO'}")
    print(f"   Horarios:  {'SI' if 'SECCION HORARIOS' in p2 else 'NO'}")
    print(f"   Redes:     {'SI' if 'REDES SOCIALES' in p2 else 'NO'}")
    print(f"   Google Maps: {'SI' if 'google.com/maps' in p2 else 'NO'}")
    print(f"   WhatsApp:  {'SI' if 'wa.me' in p2 else 'NO'}")
    print(f"   Anio:      {'SI' if '2018' in p2 else 'NO'}")

    # Compatibilidad
    p3 = generar_prompt_edicion("<html>test</html>", "cambiar titulo")
    print(f"\n3. Compatibilidad edicion V1: {len(p3)} chars OK")

    p4 = generar_prompt_edicion_estructurada("estructura test", "cambiar algo")
    print(f"4. Compatibilidad edicion V2: {len(p4)} chars OK")

    print("\n" + "=" * 60)