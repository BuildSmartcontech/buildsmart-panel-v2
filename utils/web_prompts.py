# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V7.0 (CSS INJECTION)
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
    # (Esta función no cambia, se mantiene igual)
    pass

def generar_prompt_edicion_estructurada(estructura_resumen, instruccion, contexto_negocio=""):
    """
    Nuevo Prompt V7.0: Pide CSS en lugar de acciones específicas.
    Tolera mala ortografía y falta de términos técnicos.
    """
    prompt = f"""Eres un experto en CSS y diseño web. El usuario de tu web no sabe términos técnicos, tiene faltas de ortografía y escribe como habla.

## CONTEXTO DEL NEGOCIO
{contexto_negocio if contexto_negocio else "Negocio generico"}

## ESTRUCTURA ACTUAL DEL HTML
{estructura_resumen}

## INSTRUCCIÓN DEL USUARIO (puede tener errores)
"{instruccion}"

## TU TAREA
Entiende lo que el usuario quiere lograr visualmente y genera las reglas CSS necesarias para hacerlo.
NO importa si el usuario escribe "quita el blanco del contacto" o "pone oscuro los input". Tú debes deducir qué etiquetas o clases afectan esa sección.

## FORMATO DE RESPUESTA (SOLO JSON):
{{
  "reglas_css": [
    "form {{ background-color: #0B0C14 !important; }}",
    "input, textarea {{ background-color: #1a1a1a !important; color: #FFFFFF !important; border: 1px solid #333 !important; }}",
    "h1 {{ color: #FFD700 !important; }}"
  ],
  "explicacion": "Cambié el fondo del formulario y los campos de texto a modo oscuro."
}}

## REGLAS CRÍTICAS
1. Devuelve SOLO JSON válido.
2. Usa `!important` en todas las reglas CSS para asegurar que se apliquen.
3. Si el usuario pide centrar un logo, usa `nav img {{ margin: 0 auto !important; display: block !important; }}`.
4. Si pide cambiar el color del título, usa `h1, h2 {{ color: #... !important; }}`.
5. Si pide quitar el blanco de algún lado, apunta a `form`, `input`, `textarea` o `section` con fondo oscuro.

## RESPUESTA (SOLO JSON):"""
    return prompt

def generar_prompt_resumen(html):
    return "Analiza esta pagina web y genera un resumen ejecutivo de maximo 150 palabras.\n\n## HTML:\n" + html[:3000] + "\n\nResumen ejecutivo:"