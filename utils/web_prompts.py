# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V11.4 (TODAS LAS ACCIONES)
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
## REGLA DE FOTO ADJUNTA (CRÍTICO):
El usuario ha subido una imagen. DEBES analizarla. 
1. Extrae el título real del producto (NO pongas "Nuevo Producto").
2. Extrae todas las características técnicas, especificaciones o viñetas que veas en la imagen.
3. Si la imagen tiene mucho texto, resume las 4 características más importantes.
4. Usa el valor `{{FOTO_USUARIO}}` en el `src` de la imagen.
"""

    prompt = f"""Eres un experto en manipulación de DOM con CSS y HTML.
El usuario ha pedido: "{instruccion}"

## MAPA DE ANCLAS DE LA WEB
{mapa_anclas}

{regla_foto}

## TU TAREA
Devuelve un JSON con las operaciones a realizar.

## ACCIONES PERMITIDAS (USA EXACTAMENTE ESTOS NOMBRES):
1. "cambiar_texto": Modifica el texto de un elemento. (Necesita: selector, accion, valor).
2. "cambiar_css": Modifica los estilos visuales de un elemento. (Necesita: selector, accion, valor). 
   * EJEMPLO FONDO: Si el usuario pide cambiar el fondo, usa selector "body" y valor "background-color: #0a192f !important; color: #ffffff !important;".
3. "cambiar_atributo": Modifica un atributo (ej. src, href). (Necesita: selector, accion, atributo, valor).
4. "insertar_html": Inserta código HTML dentro de un elemento. (Necesita: selector, accion, valor).
5. "crear_tarjeta": Crea una nueva tarjeta de servicio/producto. (Necesita: selector, accion, titulo, descripcion, caracteristicas).
6. "mover": Mueve un elemento a otra posición. (Necesita: selector, accion, destino).
7. "eliminar": Borra un elemento. (Necesita: selector, accion).

## FORMATO DE RESPUESTA (SOLO JSON):
{{
  "operaciones": [
    {{
      "selector": "#sec-hero",
      "accion": "cambiar_texto",
      "valor": "Nuevo título de la web"
    }},
    {{
      "selector": "body",
      "accion": "cambiar_css",
      "valor": "background-color: #0a192f !important; color: #ffffff !important;"
    }}
  ],
  "explicacion": "Cambié el título y el fondo a azul oscuro."
}}

## REGLAS CRÍTICAS (SI NO LAS CUMPLES, FALLAS):
1. **TU RESPUESTA DEBE SER EXCLUSIVAMENTE EL JSON.** NO uses bloques de código markdown (```json). NO escribas "Aquí tienes el JSON". Solo empieza con {{ y termina con }}.
2. Usa los selectores exactos del MAPA DE ANCLAS. Si el usuario pide cambiar el fondo general, usa el selector "body".
3. Si el usuario pide crear una tarjeta o te da información de un producto, DEBES usar la acción `crear_tarjeta`.
4. **EXTRACCIÓN PROFUNDA:** Si hay una imagen adjunta, analízala. NO uses textos genéricos como "Alta calidad". Lee la imagen y escribe las especificaciones reales.
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