# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V9.0 (JSON SIMPLIFICADO)
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
Devuelve un JSON con las acciones a realizar. 

Si el usuario pide BORRAR o ELIMINAR una sección, DEBES usar la acción "eliminar". 
Si pide AGREGAR, usa "agregar".
Si pide CAMBIAR COLOR, usa "color".

## FORMATO (SOLO JSON):
{{
  "acciones": [
    {{
      "tipo": "eliminar",
      "texto": "Amazonía Colombiana"
    }},
    {{
      "tipo": "agregar",
      "html": "<section class='services-grid'><div class='card'><h2>Nuevo</h2><img src='{{{{NUEVA_IMAGEN}}}}' alt='foto'></div></section>"
    }},
    {{
      "tipo": "color",
      "css": "h1 {{ color: red !important; }}"
    }}
  ],
  "explicacion": "Eliminé la sección y cambié el color"
}}

## REGLAS:
1. Devuelve SOLO JSON.
2. Para eliminar, escribe el texto exacto del título de la sección.
3. Para agregar, usa las clases `card` y el comodín `{{{{NUEVA_IMAGEN}}}}`.

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