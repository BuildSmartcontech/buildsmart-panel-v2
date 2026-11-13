# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V10.0 (JSON QUIRÚRGICO)
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
      "valor": "Nuevo texto del título"
    }},
    {{
      "selector": "#sec-servicios img[data-img='servicio-1']",
      "accion": "cambiar_atributo",
      "atributo": "src",
      "valor": "{{NUEVA_IMAGEN}}"
    }},
    {{
      "selector": "#sec-ubicacion",
      "accion": "insertar_html",
      "valor": "<p>Visítanos en nuestra oficina principal</p><a href='https://maps.google.com' class='btn'>Abrir en Google Maps</a>"
    }},
    {{
      "selector": "#sec-ubicacion",
      "accion": "mover",
      "destino": "despues_de_#sec-hero"
    }},
    {{
      "selector": "nav",
      "accion": "cambiar_css",
      "valor": "justify-content: center;"
    }}
  ],
  "explicacion": "Explicación breve"
}}

## REGLAS CRÍTICAS:
1. Devuelve SOLO JSON válido.
2. Usa las anclas del MAPA DE ANCLAS para referenciar elementos. NUNCA inventes IDs.
3. Para cambiar texto, usa `cambiar_texto`.
4. Para cambiar una imagen, usa `cambiar_atributo` con atributo `src` y valor `{{NUEVA_IMAGEN}}`.
5. Para insertar contenido, usa `insertar_html` con el selector del ancla y el HTML nuevo.
6. Para mover una sección, usa `mover` con `destino` indicando después de qué ancla.
7. Para cambiar estilos, usa `cambiar_css` con el selector del ancla.
8. Si el usuario pide "eliminar", usa `accion: "eliminar"`.

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