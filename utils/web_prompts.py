# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V8.5 (ESTRUCTURA Y COMODINES)
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

## FORMATO DE RESPUESTA (SOLO JSON):
{{
  "reemplazos_texto": [
    {{ "selector": "h2", "texto_actual": "Descubre Colombia", "texto_nuevo": "Los mejores tours" }}
  ],
  "reglas_css": [
    "h2 {{ color: #FFFF00 !important; }}"
  ],
  "secciones_html": [
    "<section class='services-grid' style='padding: 60px 20px;'><div class='card'><h2>Amazonía</h2><img src='{{NUEVA_IMAGEN}}' alt='Selva amazónica'><p>Explora la selva...</p></div></section>"
  ],
  "explicacion": "Agregué la sección de la Amazonía con imagen."
}}

## REGLAS CRÍTICAS PARA SECCIONES NUEVAS (secciones_html)
1. Si el usuario pide AGREGAR UNA SECCIÓN, DEBES usar las clases CSS premium de la página: `<section class="services-grid">` y `<div class="card">`.
2. Si el usuario pide IMÁGENES, **PROHIBIDO INVENTAR URLs**. Escribe EXACTAMENTE el comodín `src="{{NUEVA_IMAGEN}}"` para cada imagen que necesites. El sistema en Python la reemplazará por una foto real.
3. El texto de las imágenes debe ir en el atributo `alt`.
4. **REGLA DE ESTRUCTURA:** La nueva sección se insertará automáticamente ANTES del `<footer>` y de la sección de Contacto. NO incluyas un `<footer>` en tu código HTML generado.
5. Si solo pides colores, deja `reemplazos_texto` y `secciones_html` como `[]`.

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