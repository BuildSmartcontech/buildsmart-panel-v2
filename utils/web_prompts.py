# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V10.4 (SOPORTE DE FOTO Y MENSAJES CLAROS)
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
El usuario ha subido una foto. Para usarla, usa el valor `{{FOTO_USUARIO}}` en el `src` de la imagen que quieras reemplazar.
Ejemplo: {"selector": "img[data-img='servicio-1']", "accion": "cambiar_atributo", "atributo": "src", "valor": "{{FOTO_USUARIO}}"}
"""

    prompt = f"""Eres un experto en manipulación de DOM con CSS y HTML.
El usuario ha pedido: "{instruccion}"

## MAPA DE ANCLAS DE LA WEB
{mapa_anclas}

{regla_foto}

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
      "valor": "{{NUEVA_IMAGEN}}"  // O usa {{FOTO_USUARIO}} si el usuario subió una foto.
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
3. Si el usuario pide cambiar una foto y NO subió una, usa `{{NUEVA_IMAGEN}}`.
4. Si el usuario pide cambiar una foto y SÍ subió una, usa `{{FOTO_USUARIO}}`.
5. Si el usuario pide un cambio que no puedes hacer (ej: una sección que no existe), devuelve `{{"operaciones": [], "explicacion": "Explicación de por qué no se puede hacer"}}`.

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