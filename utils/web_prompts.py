# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V7.1 (CSS INJECTION + FIX IMPORT)
# ============================================

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from utils.web_prompts_data import (
    PALABRAS_PROHIBIDAS, DIRECTOR_DE_ARTE_PROMPT, REGLAS_CSS_PREMIUM,
    REGLAS_CODIGO, REGLAS_IMAGENES, REGLAS_SALIDA,
    construir_reglas_contenido, construir_instrucciones_dinamicas,
)

def generar_prompt_web(
    nombre_negocio, sector, descripcion, publico_objetivo="",
    diferenciadores="", tono="Profesional", colores="#0f3460, #f39c12",
    tipo_pagina="Landing Page", diseno="Moderno", secciones=None,
    logica="Estatica", funcionalidades=None, opciones_usuario=None,
    direccion="", ciudad="", pais="", horarios="",
    instagram="", facebook="", tiktok="",
    anio_fundacion="", email_contacto="", whatsapp_negocio="",
):
    if secciones is None:
        secciones = ["Hero", "Servicios", "Sobre Nosotros", "Contacto"]
    if funcionalidades is None:
        funcionalidades = ["SEO optimizado", "Animaciones"]

    secciones_texto = "\n".join(["   - " + s for s in secciones])
    funcionalidades_texto = "\n".join(["   - " + f for f in funcionalidades])
    lista_negra = ", ".join(PALABRAS_PROHIBIDAS[:20])

    reglas_contenido = construir_reglas_contenido(sector, lista_negra)

    datos_negocio_completos = {
        "direccion": direccion, "ciudad": ciudad, "pais": pais,
        "horarios": horarios, "instagram": instagram, "facebook": facebook,
        "tiktok": tiktok, "anio_fundacion": anio_fundacion,
        "email_contacto": email_contacto, "whatsapp_negocio": whatsapp_negocio,
    }
    instrucciones_dinamicas = construir_instrucciones_dinamicas(datos_negocio_completos)

    info_negocio = [
        "- Nombre: " + nombre_negocio,
        "- Sector: " + sector,
        "- Descripcion: " + descripcion,
    ]
    if publico_objetivo: info_negocio.append("- Publico objetivo: " + publico_objetivo)
    if diferenciadores: info_negocio.append("- Diferenciadores: " + diferenciadores)
    if ciudad: info_negocio.append("- Ubicacion: " + ciudad + (", " + pais if pais else ""))
    if direccion: info_negocio.append("- Direccion: " + direccion)
    if anio_fundacion: info_negocio.append("- Ano de fundacion: " + anio_fundacion)
    if email_contacto: info_negocio.append("- Email de contacto: " + email_contacto)
    if whatsapp_negocio: info_negocio.append("- WhatsApp: " + whatsapp_negocio)
    if horarios: info_negocio.append("- Horarios: " + horarios)
    if instagram: info_negocio.append("- Instagram: @" + instagram.lstrip("@"))
    if facebook: info_negocio.append("- Facebook: " + facebook)
    if tiktok: info_negocio.append("- TikTok: @" + tiktok.lstrip("@"))

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

def generar_prompt_edicion_estructurada(estructura_resumen, instruccion, contexto_negocio=""):
    """
    Genera el prompt para que la IA devuelva reglas CSS en lugar de JSON de acciones.
    """
    prompt = f"""Eres un experto en CSS y diseño web. El usuario de tu web no sabe términos técnicos, tiene faltas de ortografía y escribe como habla.

## CONTEXTO DEL NEGOCIO
{contexto_negocio if contexto_negocio else "Negocio generico"}

## ESTRUCTURA ACTUAL DEL HTML
{estructura_resumen}

## INSTRUCCIÓN DEL USUARIO (puede tener errores)
"{instruccion}"

## TU TAREA
Entiende lo que el usuario quiere lograr visualmente y genera las reglas CSS necesarias para hacerlo.
NO importa si el usuario escribe "quita el blanco del contacto" o "pone oscuro los input". Tú debes deducir qué etiquetas o clases afectan esa sección.

## FORMATO DE RESPUESTA (SOLO JSON):
{{
  "reglas_css": [
    "form {{ background-color: #0B0C14 !important; }}",
    "input, textarea {{ background-color: #1a1a1a !important; color: #FFFFFF !important; border: 1px solid #333 !important; }}",
    "h1 {{ color: #FFD700 !important; }}"
  ],
  "explicacion": "Cambié el fondo del formulario y los campos de texto a modo oscuro."
}}

## REGLAS CRÍTICAS
1. Devuelve SOLO JSON válido.
2. Usa `!important` en todas las reglas CSS para asegurar que se apliquen.
3. Si el usuario pide centrar un logo, usa `nav img {{ margin: 0 auto !important; display: block !important; }}`.
4. Si pide cambiar el color del título, usa `h1, h2 {{ color: #... !important; }}`.
5. Si pide quitar el blanco de algún lado, apunta a `form`, `input`, `textarea` o `section` con fondo oscuro.

## RESPUESTA (SOLO JSON):"""
    return prompt

def generar_prompt_edicion(html_actual, instruccion):
    prompt = (
        "Eres un disenador web profesional. El usuario quiere hacer un cambio en su pagina web.\n\n"
        "## INSTRUCCION DEL USUARIO:\n" + instruccion + "\n\n"
        "## CODIGO HTML ACTUAL (COMPLETO):\n" + html_actual + "\n\n"
        "## REGLAS ESTRICTAS:\n"
        "1. Devuelve el CODIGO HTML COMPLETO, no solo la parte modificada.\n"
        "2. DEBES incluir: <!DOCTYPE html>, <html>, <head>, <body>, </html>.\n"
        "3. Modifica SOLO lo que el usuario pide, manten el resto igual.\n\n"
        "Codigo HTML completo actualizado:"
    )
    return prompt

def generar_prompt_resumen(html):
    return (
        "Analiza esta pagina web y genera un resumen ejecutivo de maximo 150 palabras.\n\n"
        "## HTML:\n" + html[:3000] + "\n\n"
        "## REGLAS:\n1. Maximo 150 palabras.\n2. Enfocate en propuesta de valor.\n\nResumen ejecutivo:"
    )

def generar_prompt_seo(nombre_negocio, sector, descripcion):
    return (
        "Genera meta tags SEO.\n\n"
        "## INFO:\n- Nombre: " + nombre_negocio + "\n- Sector: " + sector + "\n- Descripcion: " + descripcion + "\n\n"
        "## FORMATO (JSON):\n{\n    \"title\": \"max 60 chars\",\n    \"description\": \"max 160 chars\",\n    \"keywords\": [\"p1\", \"p2\"]\n}\n\nDevuelve SOLO el JSON."
    )

def validar_html_generado(html):
    errores = []
    advertencias = []
    if not html: return {"errores": ["HTML vacio"], "advertencias": [], "valido": False}
    if len(html) < 500: errores.append("HTML muy corto")
    html_lower = html.lower()
    if "<!doctype html>" not in html_lower: advertencias.append("Falta DOCTYPE")
    if "<html" not in html_lower: errores.append("Falta etiqueta html")
    if "<body>" not in html_lower: errores.append("Falta body")
    if "</html>" not in html_lower: errores.append("Falta cierre html")
    return {"errores": errores, "advertencias": advertencias, "valido": len(errores) == 0}