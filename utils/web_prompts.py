# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V9.1 (UNA SOLA ACCIÓN)
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
    prompt = f"""Eres un experto en CSS y HTML. El usuario ha pedido: "{instruccion}"

## TU TAREA
Devuelve un JSON con LAS ACCIONES que el usuario pide. 
Si el usuario pide eliminar, usa SOLO la acción "eliminar". Si pide agregar, usa SOLO "agregar". Si pide color, usa SOLO "color".

## FORMATO (SOLO JSON):
{{
  "acciones": [
    {{
      "tipo": "eliminar",
      "texto": "Amazonía Colombiana"
    }}
  ],
  "explicacion": "Eliminé la sección de Amazonía"
}}

## REGLAS:
1. Para eliminar, escribe el texto EXACTO del título que el usuario quiere borrar (ej: "Amazonía Colombiana"). No escribas el selector HTML, solo el texto.
2. Si pide agregar, usa el comodín {{{{NUEVA_IMAGEN}}}} y las clases `card`.
3. Devuelve SOLO JSON válido.

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