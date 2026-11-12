# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V8.6 (BORRADO Y COMODINES)
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
    prompt = f"""Eres un experto en CSS, HTML y edición de contenido.

## CONTEXTO DEL NEGOCIO
{contexto_negocio if contexto_negocio else "Negocio generico"}

## ESTRUCTURA ACTUAL DE LA WEB
{estructura_resumen}

## INSTRUCCIÓN DEL USUARIO
"{instruccion}"

## TU TAREA
Analiza lo que el usuario quiere y devuelve un JSON con las modificaciones.
Si el usuario pide borrar o eliminar algo, usa `eliminar_secciones`.
Si pide agregar, usa `secciones_html`.
Si pide cambiar texto, usa `reemplazos_texto`.
Si pide colores, usa `reglas_css`.

## FORMATO DE RESPUESTA (SOLO JSON):
{{
  "reemplazos_texto": [],
  "reglas_css": [],
  "secciones_html": [
    "<section class='services-grid' style='padding: 60px 20px;'><div class='card'><h2>Amazonía</h2><img src='{{NUEVA_IMAGEN}}' alt='Selva amazónica'><p>Explora la selva...</p></div></section>"
  ],
  "eliminar_secciones": [
    {{ "selector": "section", "texto_que_contiene": "Amazonía Colombiana" }}
  ],
  "explicacion": "Borré la sección vieja y agregué la nueva con tarjetas."
}}

## REGLAS CRÍTICAS PARA SECCIONES NUEVAS (secciones_html)
1. DEBES usar las clases CSS premium: `<section class="services-grid">` y `<div class="card">`.
2. Si necesitas imágenes, **PROHIBIDO INVENTAR URLs**. Escribe EXACTAMENTE el comodín `src="{{NUEVA_IMAGEN}}"`. El sistema lo reemplazará.
3. El texto de las imágenes debe ir en el atributo `alt` (en español).

## REGLAS PARA ELIMINAR (eliminar_secciones)
1. Si el usuario pide borrar una sección, busca la etiqueta (ej. "section", "div") y el texto que la identifica.
2. Ejemplo: Para borrar la sección de Amazonía vieja, usa `selector: "section"` y `texto_que_contiene: "Amazonía Colombiana"`.

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