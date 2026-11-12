# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V8.8 (BORRADO POR TEXTO)
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

## REGLAS ESTRICTAS:
1. Si el usuario pide ELIMINAR o BORRAR una sección, usa `eliminar_secciones`. Escribe el título EXACTO de la sección que quieres borrar (ej: "Amazonía Colombiana") en `texto_que_contiene`. El sistema en Python se encargará de buscar y destruir ese bloque.
2. Si el usuario pide AGREGAR, usa las clases `<section class="services-grid">` y `<div class="card">`. Usa el comodín `src="{{NUEVA_IMAGEN}}"` para fotos.
3. Si pide cambiar colores, usa `reglas_css`.

## FORMATO DE RESPUESTA (SOLO JSON):
{{
  "reemplazos_texto": [],
  "reglas_css": [],
  "secciones_html": [
    "<section class='services-grid' style='padding: 60px 20px;'><div class='card'><h2>Amazonía</h2><img src='{{NUEVA_IMAGEN}}' alt='Selva amazónica'><p>Explora la selva...</p></div></section>"
  ],
  "eliminar_secciones": [
    {{ "texto_que_contiene": "Amazonía Colombiana" }}
  ],
  "explicacion": "Borré la sección vieja y agregué la nueva con tarjetas."
}}

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