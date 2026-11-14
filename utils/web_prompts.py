# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V11.2 (JSON ESTRICTO)
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

def generar_prompt_edicion_estructurada(mapa_anclas, instruccion, contexto_negocio="", tiene_foto=False):
    
    regla_foto = ""
    if tiene_foto:
        regla_foto = """
## REGLA DE FOTO ADJUNTA:
El usuario ha subido una foto. Para usarla, usa el valor `{{FOTO_USUARIO}}` en el `src`.
"""

    prompt = f"""Eres un experto en manipulación de DOM con CSS y HTML.
El usuario ha pedido: "{instruccion}"

## MAPA DE ANCLAS DE LA WEB
{mapa_anclas}

{regla_foto}

## TU TAREA
Devuelve un JSON con las operaciones a realizar.

## FORMATO (SOLO JSON):
{{
  "operaciones": [
    {{
      "selector": "#sec-servicios",
      "accion": "crear_tarjeta",
      "titulo": "Generador Yanmar",
      "descripcion": "Generador diésel marino de alta eficiencia.",
      "caracteristicas": ["12 voltios CC", "Apagado automático", "Filtro de combustible", "Bomba de transferencia"]
    }}
  ],
  "explicacion": "Creé la tarjeta con la información extraída."
}}

## REGLAS CRÍTICAS (SI NO LAS CUMPLES, FALLAS):
1. **TU RESPUESTA DEBE SER EXCLUSIVAMENTE EL JSON.** NO uses bloques de código markdown (```json). NO escribas "Aquí tienes el JSON". Solo empieza con {{ y termina con }}.
2. Usa los selectores exactos del MAPA DE ANCLAS.
3. Si el usuario pide crear una tarjeta o te da información de un producto, DEBES usar la acción `crear_tarjeta`.
4. **INVESTIGACIÓN AUTÓNOMA:** Si el texto extraído de la imagen (en la instrucción) es corto, deduce al menos 4 características técnicas del producto basándote en el título y agrégalas al array `caracteristicas`.
5. Si el usuario pide algo que no existe, devuelve una lista vacía `[]` y una explicación.

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