# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V8.3 (CONTEXTO DE TÍTULOS)
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
    prompt = f"""Eres un experto en CSS, HTML y edición de contenido.

## CONTEXTO DEL NEGOCIO
{contexto_negocio if contexto_negocio else "Negocio generico"}

## ESTRUCTURA ACTUAL DE LA WEB
{estructura_resumen}

## INSTRUCCIÓN DEL USUARIO
"{instruccion}"

## TU TAREA
Analiza lo que el usuario quiere y devuelve un JSON con las modificaciones.

¡ATENCIÓN AL CONTEXTO! Revisa los "TITULOS ACTUALES" para saber qué texto hay en la página.
Si el usuario dice "Cambia el título principal", mira cuál es el más grande (usualmente el del Hero, ej. h1 o h2) y usa el texto_actual para que el sistema sepa cuál borrar.

## FORMATO DE RESPUESTA (SOLO JSON):
{{
  "reemplazos_texto": [
    {{ "selector": "h2", "texto_actual": "Descubre Colombia", "texto_nuevo": "Los mejores tours de Colombia" }}
  ],
  "reglas_css": [
    "h2 {{ color: #FFFF00 !important; }}"
  ],
  "secciones_html": [],
  "explicacion": "Cambié el título principal del Hero."
}}

## REGLAS CRÍTICAS
1. Devuelve SOLO JSON válido.
2. Para reemplazar texto, usa `reemplazos_texto`. Incluye `texto_actual` (una parte del texto viejo) y `texto_nuevo`. Esto es CRUCIAL para no modificar el título equivocado.
3. Si agregas una sección nueva, usa `secciones_html`.
4. Si solo pides colores, deja `reemplazos_texto` y `secciones_html` como `[]`.

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