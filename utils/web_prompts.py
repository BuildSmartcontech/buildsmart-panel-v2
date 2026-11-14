# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V11.1 (INVESTIGACIÓN AUTÓNOMA)
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
      "selector": "#sec-hero h1",
      "accion": "cambiar_texto",
      "valor": "Nuevo texto"
    }},
    {{
      "selector": "#sec-servicios",
      "accion": "crear_tarjeta",
      "titulo": "Título del producto",
      "descripcion": "Descripción persuasiva",
      "caracteristicas": ["Característica 1", "Característica 2"]
    }},
    {{
      "selector": "body",
      "accion": "cambiar_css",
      "valor": "background-color: #FF5722;"
    }}
  ],
  "explicacion": "Explicación breve"
}}

## REGLAS CRÍTICAS:
1. Devuelve SOLO JSON válido.
2. Usa los selectores exactos del MAPA DE ANCLAS.
3. Si el usuario pide "crear una nueva tarjeta" o "agregar un producto" o te da información de un producto, DEBES usar la acción `crear_tarjeta`.
4. **INVESTIGACIÓN AUTÓNOMA:** Si la información extraída de la imagen (OCR) es muy corta (solo el título), investiga y deduce al menos 4 características técnicas estándar del producto basándote en el título y el nicho de la web, y agrégalas al array `caracteristicas`.
5. Si el usuario dice "el montacargas" o "la segunda tarjeta", BUSCA en el MAPA la imagen cuyo `alt` o `título_tarjeta` coincida y usa su selector.
6. Si el usuario pide algo que no existe, devuelve una lista vacía `[]` y una explicación.

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