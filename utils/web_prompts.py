# utils/web_prompts.py
# ============================================
# PROMPTS DE CALIDAD V8.7 (LIMPIEZA Y ORDEN)
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

## REGLAS ESTRICTAS DE EDICIÓN Y LIMPIEZA:
1. Si el usuario pide ELIMINAR o BORRAR una sección, texto o bloque, bórralo por completo del código HTML sin dejar rastros ni etiquetas vacías. Usa `eliminar_secciones`.
2. Mantén siempre este orden lógico en la página: 
   - Barra de navegación (<nav>)
   - Portada principal (Hero)
   - Servicios / Destinos / Productos (Tarjetas)
   - Quiénes somos
   - Ubicación y Horarios
   - Formulario de Contacto y WhatsApp
   - Pie de página (<footer>)
3. Nunca dejes texto ni etiquetas HTML fuera de la etiqueta </body>.
4. Si el usuario pide AGREGAR una nueva sección (ej: "agrega Amazonía"), usa las clases `<section class="services-grid">` y `<div class="card">`.
5. Si necesitas imágenes, **PROHIBIDO INVENTAR URLs**. Usa EXACTAMENTE el comodín `src="{{NUEVA_IMAGEN}}"`. El sistema la reemplazará.

## TU TAREA
Devuelve un JSON con las modificaciones.

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