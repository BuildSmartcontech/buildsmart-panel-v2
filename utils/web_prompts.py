# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V10.2 (SWAP CLARO)
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

def generar_prompt_edicion_estructurada(mapa_anclas, instruccion, contexto_negocio=""):
    prompt = f"""Eres un experto en manipulación de DOM con CSS y HTML.
El usuario ha pedido: "{instruccion}"

## MAPA DE ANCLAS DE LA WEB
{mapa_anclas}

## TU TAREA
Devuelve un JSON con las operaciones a realizar sobre las anclas de la web.

## FORMATO (SOLO JSON):
{{
  "operaciones": [
    {{
      "selector": "#sec-hero h1",
      "accion": "cambiar_texto",
      "valor": "Nuevo texto"
    }},
    {{
      "selector": "img[data-img='servicio-1']",
      "accion": "cambiar_atributo",
      "atributo": "src",
      "valor": "{{NUEVA_IMAGEN}}"
    }},
    {{
      "selector": "img[data-img='servicio-1']",
      "selector_2": "img[data-img='servicio-3']",
      "accion": "intercambiar_imagenes"
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
2. Usa los selectores exactos del MAPA DE ANCLAS. NUNCA inventes IDs.
3. Para cambiar texto, usa `cambiar_texto`.
4. Para cambiar una imagen, usa `cambiar_atributo` con atributo `src` y valor `{{NUEVA_IMAGEN}}`.
5. Para INTERCAMBIAR dos imágenes de lugar, usa `accion: "intercambiar_imagenes"` y define `selector` y `selector_2` con los valores exactos del mapa de anclas.
6. Para insertar contenido, usa `insertar_html`.
7. Para mover una sección, usa `mover` con `destino`.
8. Para cambiar estilos, usa `cambiar_css` con el selector del ancla.

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