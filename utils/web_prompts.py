# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V8.0 (CSS + HTML HÍBRIDO)
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

def generar_prompt_web(*args, **kwargs):
    # (Se mantiene igual que en la versión anterior)
    pass

def generar_prompt_edicion_estructurada(estructura_resumen, instruccion, contexto_negocio=""):
    """
    Nuevo Prompt V8.0: Permite CSS para estilos y HTML para agregar texto/secciones.
    """
    prompt = f"""Eres un experto en CSS, HTML y diseño web. El usuario escribe con faltas de ortografía y no sabe términos técnicos.

## CONTEXTO DEL NEGOCIO
{contexto_negocio if contexto_negocio else "Negocio generico"}

## ESTRUCTURA ACTUAL DEL HTML
{estructura_resumen}

## INSTRUCCIÓN DEL USUARIO (puede tener errores)
"{instruccion}"

## TU TAREA
Analiza lo que el usuario quiere y devuelve un JSON con las modificaciones.

Si el usuario pide cambiar colores, centrar cosas o arreglar el diseño visual, usa la lista `reglas_css`.
Si el usuario pide agregar nueva información, textos, o secciones nuevas, usa la lista `secciones_html`.

## FORMATO DE RESPUESTA (SOLO JSON):
{{
  "reglas_css": [
    "form {{ background-color: #0B0C14 !important; }}",
    "h1 {{ color: #FFD700 !important; }}"
  ],
  "secciones_html": [
    "<section id='nueva-seccion' style='padding: 60px 20px; background-color: #111; color: white;'><h2>Nueva Sección</h2><p>Texto nuevo aquí...</p></section>"
  ],
  "explicacion": "Cambié el fondo y agregué la sección de la Amazonía."
}}

## REGLAS CRÍTICAS
1. Devuelve SOLO JSON válido.
2. Usa `!important` en todas las reglas CSS.
3. Si el usuario pide agregar texto/secciones, genera el bloque HTML completo en `secciones_html`. Usa estilos inline o clases oscuras para que combine con el diseño premium.
4. Si solo pide cambios visuales, deja `secciones_html` como una lista vacía `[]`.
5. Si solo pide agregar texto, deja `reglas_css` como una lista vacía `[]`.

## RESPUESTA (SOLO JSON):"""
    return prompt

def generar_prompt_edicion(html_actual, instruccion):
    # (Se mantiene igual)
    pass

def generar_prompt_resumen(html):
    # (Se mantiene igual)
    pass

def generar_prompt_seo(nombre_negocio, sector, descripcion):
    # (Se mantiene igual)
    pass

def validar_html_generado(html):
    # (Se mantiene igual)
    pass