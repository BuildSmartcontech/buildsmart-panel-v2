# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V10.6 (VISIÓN Y CREACIÓN DE TARJETAS)
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
El usuario ha subido una foto. Para usarla en una imagen existente o en una tarjeta nueva, usa el valor `{{FOTO_USUARIO}}` en el `src`.
Ejemplo: <img src="{{FOTO_USUARIO}}" alt="Foto del producto">
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
      "selector": "#sec-servicios",
      "accion": "insertar_html",
      "valor": "<div class='card'><img src='{{{{FOTO_USUARIO}}}}' alt='Nuevo'><h3>Nuevo Titulo</h3><p>Nueva descripcion</p></div>"
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
3. Si el usuario pide "crear una nueva tarjeta" o "agregar un producto", usa la acción `insertar_html` con el selector `#sec-servicios`.
4. El HTML de la nueva tarjeta DEBE tener esta estructura: `<div class="card"> [imagen] <h3>Título</h3> <p>Texto</p> </div>`.
5. Si el usuario subió una foto, usa `{{FOTO_USUARIO}}` como valor del `src` de la imagen. Si no subió foto, usa una URL real de Unsplash.
6. Si el usuario dice "el montacargas" o "la segunda tarjeta", BUSCA en el MAPA la imagen cuyo `alt` o `título_tarjeta` coincida y usa su selector.
7. Si el usuario pide algo que no existe, devuelve una lista vacía `[]` y una explicación.

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