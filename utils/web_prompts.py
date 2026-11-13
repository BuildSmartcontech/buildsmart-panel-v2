# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V9.3 (ANTI-BORRADO ACCIDENTAL)
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
Devuelve un JSON con las ACCIONES que el usuario pide. 
¡ATENCIÓN! Si el usuario dice "cambia", "modifica" o "reemplaza" el texto, usa SOLO `reemplazar_texto`. Si el usuario dice "elimina", "borra" o "quita", usa SOLO `eliminar`. NO confundas cambiar con eliminar.

## FORMATO (SOLO JSON):
{{
  "acciones": [
    {{
      "tipo": "reemplazar_texto",
      "selector": "h1",
      "texto_actual": "texto viejo (opcional)",
      "texto_nuevo": "texto nuevo"
    }},
    {{
      "tipo": "reemplazar_imagen",
      "alt_viejo": "texto del alt de la imagen a cambiar",
      "busqueda_nueva": "palabra clave en ingles para buscar la nueva foto"
    }},
    {{
      "tipo": "agregar_seccion",
      "html": "<section class='services-grid'><div class='card'><h2>Nuevo</h2><img src='{{{{NUEVA_IMAGEN}}}}' alt='foto'></div></section>"
    }},
    {{
      "tipo": "eliminar",
      "texto": "Texto exacto de la sección a borrar"
    }},
    {{
      "tipo": "color",
      "css": "h1 {{ color: #FFD700 !important; }}"
    }}
  ],
  "explicacion": "Explicación de lo que se hizo"
}}

## REGLAS CRÍTICAS:
1. Devuelve SOLO JSON válido.
2. Para reemplazar texto, usa `tipo: "reemplazar_texto"`. Si el usuario no especifica el texto viejo, usa `selector: "h1"` o `"h2"` y deja `texto_actual` vacío. NUNCA borres la etiqueta completa.
3. Para cambiar una imagen, usa `tipo: "reemplazar_imagen"`. Busca la imagen por su texto `alt`. La `busqueda_nueva` DEBE estar en INGLÉS.
4. Si pide agregar, usa `tipo: "agregar_seccion"`.
5. Si pide borrar, usa `tipo: "eliminar"`.
6. Si pide colores, usa `tipo: "color"`.

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