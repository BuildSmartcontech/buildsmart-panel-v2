# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V8.1 (DOBLE ORDEN BLINDADA)
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
    pass

def generar_prompt_edicion_estructurada(estructura_resumen, instruccion, contexto_negocio=""):
    prompt = f"""Eres un experto en CSS, HTML y diseño web. El usuario escribe con faltas de ortografía y no sabe términos técnicos.

## CONTEXTO DEL NEGOCIO
{contexto_negocio if contexto_negocio else "Negocio generico"}

## ESTRUCTURA ACTUAL DEL HTML
{estructura_resumen}

## INSTRUCCIÓN DEL USUARIO (puede tener errores)
"{instruccion}"

## TU TAREA
Analiza lo que el usuario quiere y devuelve un JSON con las modificaciones.

¡ATENCIÓN! Si el usuario pide AGREGAR INFORMACIÓN o NUEVAS SECCIONES (ej: "incluye info de la Amazonía"), DEBES generar obligatoriamente el código HTML en `secciones_html`. 
Si además pide un cambio de color o diseño, TAMBIÉN debes llenar `reglas_css`. ¡Haz las dos cosas si te las pide!

## FORMATO DE RESPUESTA (SOLO JSON):
{{
  "reglas_css": [
    "h1, h2, a {{ color: #FFFF00 !important; }}"
  ],
  "secciones_html": [
    "<section style='padding: 60px 20px; background-color: #0B0C14; color: white; text-align: center;'><h2>La Amazonía</h2><p>Descubre la selva tropical más grande del mundo, su biodiversidad y sus ríos majestuosos.</p></section>"
  ],
  "explicacion": "Cambié el color del texto a amarillo y agregué la sección de la Amazonía."
}}

## REGLAS CRÍTICAS
1. Devuelve SOLO JSON válido.
2. Usa `!important` en todas las reglas CSS.
3. Si el usuario pide agregar texto/secciones, ES OBLIGATORIO que generes el bloque HTML completo en `secciones_html`. Usa estilos inline para que combine con el diseño.
4. Si SOLO pide cambios visuales (ej: "pon el fondo azul"), deja `secciones_html` como `[]`.
5. Si SOLO pide agregar texto (ej: "agrega un párrafo sobre nosotros"), deja `reglas_css` como `[]`.

## RESPUESTA (SOLO JSON):"""
    return prompt

def generar_prompt_edicion(html_actual, instruccion):
    pass

def generar_prompt_resumen(html):
    pass

def generar_prompt_seo(nombre_negocio, sector, descripcion):
    pass

def validar_html_generado(html):
    pass