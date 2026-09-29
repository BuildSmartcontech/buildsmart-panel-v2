# utils/analisis_profundo.py
# ============================================
# MOTOR DE ANALISIS PROFUNDO - SAMU IA
# ============================================
# V1.4: Deteccion de 5 tipos de analisis + prompts especializados
# V1.3: Inyecta contexto de SAMU IA
# V1.2: Fix $ escapado
# V1.1: Fix deteccion keywords
# V1.0: Version inicial
# ============================================

import re
import datetime
from pathlib import Path


# ==========================================
# CONFIGURACION
# ==========================================

KEYWORDS_ANALISIS = [
    "estudio de mercado", "analisis de mercado", "analisis profundo",
    "viabilidad financiera", "proyeccion financiera", "estrategia de precios",
    "analisis de precios", "plan de negocio", "reporte ejecutivo",
    "hoja de ruta", "analisis competitivo", "benchmark",
    "estudio de viabilidad", "proyeccion de ingresos", "analisis financiero",
    "analiza mi", "analizar mi",
]

MIN_PALABRAS_PROMPT_LARGO = 100

PREFIJOS_FORZAR = [
    "[ejecutar", "[analizar", "[reporte",
    "genera inmediatamente", "genera un estudio", "genera un analisis",
]

# Tipos de analisis para usuarios
TIPOS_ANALISIS = {
    "marketing": [
        "marketing", "redes sociales", "contenido", "campanas",
        "publicidad", "instagram", "facebook", "tiktok", "seo",
    ],
    "finanzas": [
        "finanzas", "financiero", "margenes", "rentabilidad",
        "costos", "precios", "ingresos", "gastos",
    ],
    "competencia": [
        "competencia", "competidores", "competitivo", "mercado",
        "sector", "industria",
    ],
    "web": [
        "mi web", "mi pagina", "sitio web", "pagina web",
        "landing", "conversion", "visitas",
    ],
    "operacion": [
        "operacion", "procesos", "equipo", "productividad",
        "tareas", "flujo",
    ],
}

_ROOT = Path(__file__).resolve().parent.parent
RUTA_CONTEXTO = _ROOT / "config" / "contexto_samu_ia.md"

_CONTEXTO_CACHE = {"data": None}


# ==========================================
# DETECCION
# ==========================================
def es_prompt_largo(texto):
    if not texto:
        return False
    return len(texto.split()) >= MIN_PALABRAS_PROMPT_LARGO


def tiene_prefijo_forzado(texto):
    if not texto:
        return False
    texto_lower = texto.lower().strip()
    return any(texto_lower.startswith(p) for p in PREFIJOS_FORZAR)


def tiene_keywords_analisis(texto):
    if not texto:
        return False
    texto_lower = texto.lower()
    return any(kw in texto_lower for kw in KEYWORDS_ANALISIS)


def es_analisis_profundo(texto):
    """
    Determina si un prompt debe procesarse como analisis profundo.
    Reglas:
    1. Prefijo forzado [ejecutar...] -> SI
    2. Tiene keyword de analisis -> SI
    3. Prompt largo (>100 palabras) -> SI
    """
    if not texto:
        return False
    if tiene_prefijo_forzado(texto):
        return True
    if tiene_keywords_analisis(texto):
        return True
    if es_prompt_largo(texto):
        return True
    return False


def detectar_tipo_analisis(texto):
    """
    Detecta el tipo de analisis segun palabras clave.
    Retorna: "marketing", "finanzas", "competencia", "web",
             "operacion" o "general".
    """
    if not texto:
        return "general"

    texto_lower = texto.lower()

    # Buscar el tipo con mas coincidencias
    mejor_tipo = "general"
    mejor_score = 0

    for tipo, palabras in TIPOS_ANALISIS.items():
        score = sum(1 for p in palabras if p in texto_lower)
        if score > mejor_score:
            mejor_score = score
            mejor_tipo = tipo

    return mejor_tipo


def limpiar_prompt(texto):
    if not texto:
        return ""
    t = texto.strip()
    t = re.sub(r"^\[[^\]]+\]\s*", "", t)
    return t.strip()


# ==========================================
# CARGA DEL CONTEXTO
# ==========================================
def cargar_contexto_samu():
    """Lee config/contexto_samu_ia.md (con cache)."""
    if _CONTEXTO_CACHE["data"] is not None:
        return _CONTEXTO_CACHE["data"]

    try:
        if RUTA_CONTEXTO.exists():
            contenido = RUTA_CONTEXTO.read_text(encoding="utf-8")
            _CONTEXTO_CACHE["data"] = contenido
            print(f"[analisis_profundo] Contexto SAMU IA cargado ({len(contenido)} chars)")
            return contenido
    except Exception as e:
        print(f"[analisis_profundo] Error leyendo contexto: {e}")

    _CONTEXTO_CACHE["data"] = ""
    return ""


# ==========================================
# ESCAPADO MARKDOWN
# ==========================================
def _escapar_markdown(texto):
    if not texto:
        return ""
    return texto.replace("$", "\\$")


# ==========================================
# PROMPTS DEL DUENO
# ==========================================
PROMPT_BASE_DUENO = """Eres un analista de negocios senior del proyecto SAMU IA.

CONTEXTO REAL DEL PROYECTO:
{contexto}

=========================================================
INSTRUCCIONES PARA EL ANALISIS
=========================================================

Consulta del dueno:
{consulta}

REGLAS ESTRICTAS:
1. USA SOLO la informacion del CONTEXTO de arriba
2. NO inventes features que SAMU IA no tiene
3. SI reconoces que algo esta pendiente, decirlo como "pendiente"
4. SI comparas con competidores, usar los del contexto (Polsia, Odoo, etc)
5. SI hablas de precios, usar los del contexto (USD 199, USD 99/mes, etc)
6. SI usas montos, escribir "USD 100" o "100 dolares" (NO uses $)
7. SIEMPRE usar encabezados Markdown (##, ###)
8. SIEMPRE incluir tablas cuando compares opciones
9. NO inventar fuentes, empresas o estadisticas especificas
10. Responder en espanol claro, sin relleno
11. Maximo 2500 palabras

ESTRUCTURA SUGERIDA:
- ## Resumen ejecutivo (3-5 lineas)
- ## Analisis principal (con tablas)
- ## Recomendaciones
- ## Proximos pasos
"""


# ==========================================
# PROMPTS DE USUARIOS POR TIPO
# ==========================================
_HEADER_USUARIO = """Eres un consultor de negocios para PYMES.

NEGOCIO DEL USUARIO:
- Nombre: {nombre}
- Sector: {sector}
- Descripcion: {descripcion}
- Tareas pendientes: {tareas_pendientes}
- Tiene web publicada: {tiene_web}

El usuario te hace esta consulta:
{consulta}

"""

_REGLAS_BASE_USUARIO = """REGLAS ESTRICTAS:
1. USA SOLO los datos reales del negocio del usuario
2. NO inventes metricas, ventas ni clientes
3. Si no hay datos suficientes, decirlo explicitamente
4. Dar recomendaciones CONCRETAS y ACCIONABLES
5. Usar tablas cuando compares opciones
6. Responder en espanol claro, directo, sin relleno
7. Maximo 800 palabras
8. Para montos usa "USD 100", NO uses el simbolo $
"""

PROMPT_USUARIO_MARKETING = _HEADER_USUARIO + _REGLAS_BASE_USUARIO + """
ESTRUCTURA:
- ## Diagnostico de marketing
- ## Canales recomendados (con tabla comparativa)
- ## Plan de contenido (3 acciones concretas)
- ## Proximos 3 pasos
"""

PROMPT_USUARIO_FINANZAS = _HEADER_USUARIO + _REGLAS_BASE_USUARIO + """
ESTRUCTURA:
- ## Diagnostico financiero
- ## Analisis de precios y margenes
- ## Oportunidades de mejora
- ## Proximos 3 pasos
"""

PROMPT_USUARIO_COMPETENCIA = _HEADER_USUARIO + _REGLAS_BASE_USUARIO + """
ESTRUCTURA:
- ## Tu sector en contexto
- ## Tipos de competidores (con tabla)
- ## Tu diferenciacion
- ## Proximos 3 pasos
"""

PROMPT_USUARIO_WEB = _HEADER_USUARIO + _REGLAS_BASE_USUARIO + """
ESTRUCTURA:
- ## Estado actual de tu web
- ## Oportunidades de mejora
- ## Acciones concretas de SEO/conversion
- ## Proximos 3 pasos
"""

PROMPT_USUARIO_OPERACION = _HEADER_USUARIO + _REGLAS_BASE_USUARIO + """
ESTRUCTURA:
- ## Diagnostico operativo
- ## Procesos a optimizar
- ## Delegacion y equipo
- ## Proximos 3 pasos
"""

PROMPT_USUARIO_GENERAL = _HEADER_USUARIO + _REGLAS_BASE_USUARIO + """
ESTRUCTURA:
- ## Diagnostico (que veo en tu negocio)
- ## Analisis
- ## Recomendaciones concretas
- ## Proximos 3 pasos
"""

PROMPTS_USUARIO = {
    "marketing": PROMPT_USUARIO_MARKETING,
    "finanzas": PROMPT_USUARIO_FINANZAS,
    "competencia": PROMPT_USUARIO_COMPETENCIA,
    "web": PROMPT_USUARIO_WEB,
    "operacion": PROMPT_USUARIO_OPERACION,
    "general": PROMPT_USUARIO_GENERAL,
}


# ==========================================
# GENERACION
# ==========================================
def _cargar_gateway():
    try:
        from backend.gateway import gateway
        return gateway
    except ImportError:
        try:
            from gateway import gateway
            return gateway
        except ImportError:
            return None


def _construir_prompt(consulta, contexto_usuario=None):
    if contexto_usuario:
        # Usuario: detectar tipo y usar prompt especializado
        tipo = detectar_tipo_analisis(consulta)
        plantilla = PROMPTS_USUARIO.get(tipo, PROMPT_USUARIO_GENERAL)
        return plantilla.format(
            nombre=contexto_usuario.get("nombre", "Sin nombre"),
            sector=contexto_usuario.get("sector", "General"),
            descripcion=(contexto_usuario.get("descripcion", "") or "")[:300],
            tareas_pendientes=contexto_usuario.get("tareas_pendientes", 0),
            tiene_web="Si" if contexto_usuario.get("tiene_web") else "No",
            consulta=consulta,
        )
    else:
        # Dueno: inyecta contexto de SAMU IA
        contexto = cargar_contexto_samu()
        if not contexto:
            contexto = "(Contexto de SAMU IA no disponible. Se conservador en las respuestas.)"

        return PROMPT_BASE_DUENO.format(
            contexto=contexto,
            consulta=consulta,
        )


def generar_analisis(texto, contexto_usuario=None):
    t0 = datetime.datetime.now()

    if not texto or not texto.strip():
        return {
            "exito": False, "reporte": "", "error": "Prompt vacio",
            "tipo": "dueno" if not contexto_usuario else "usuario",
            "subtipo": "general", "tiempo_ms": 0,
        }

    consulta = limpiar_prompt(texto)
    prompt_final = _construir_prompt(consulta, contexto_usuario)

    # Detectar subtipo si es usuario
    subtipo = "general"
    if contexto_usuario:
        subtipo = detectar_tipo_analisis(consulta)

    gateway = _cargar_gateway()
    if gateway is None:
        return {
            "exito": False, "reporte": "",
            "error": "Gateway de IA no disponible",
            "tipo": "dueno" if not contexto_usuario else "usuario",
            "subtipo": subtipo, "tiempo_ms": 0,
        }

    try:
        respuesta, fuente = gateway.chat_inteligente(consulta, prompt_final)
        ms = int((datetime.datetime.now() - t0).total_seconds() * 1000)

        if not respuesta:
            return {
                "exito": False, "reporte": "",
                "error": "La IA no devolvio respuesta",
                "tipo": "dueno" if not contexto_usuario else "usuario",
                "subtipo": subtipo, "tiempo_ms": ms,
            }

        tipo = "dueno" if not contexto_usuario else "usuario"
        encabezado = _construir_encabezado(tipo, consulta, subtipo)
        pie = f"\n\n---\n_Generado con {fuente} en {ms/1000:.1f}s_"

        reporte_raw = encabezado + respuesta + pie
        reporte_limpio = _escapar_markdown(reporte_raw)

        return {
            "exito": True,
            "reporte": reporte_limpio,
            "error": None,
            "tipo": tipo,
            "subtipo": subtipo,
            "fuente": fuente,
            "tiempo_ms": ms,
        }

    except Exception as e:
        ms = int((datetime.datetime.now() - t0).total_seconds() * 1000)
        return {
            "exito": False, "reporte": "",
            "error": f"Error generando analisis: {str(e)[:200]}",
            "tipo": "dueno" if not contexto_usuario else "usuario",
            "subtipo": subtipo, "tiempo_ms": ms,
        }


def _construir_encabezado(tipo, consulta, subtipo="general"):
    if tipo == "dueno":
        cabecera = "# Reporte ejecutivo - SAMU IA\n\n"
    else:
        # Nombre bonito segun subtipo
        nombres = {
            "marketing": "Analisis de marketing",
            "finanzas": "Analisis financiero",
            "competencia": "Analisis competitivo",
            "web": "Analisis de tu web",
            "operacion": "Analisis operativo",
            "general": "Analisis para tu negocio",
        }
        titulo = nombres.get(subtipo, "Analisis para tu negocio")
        cabecera = f"# {titulo}\n\n"

    cabecera += f"**Consulta:** {consulta[:200]}\n\n"
    cabecera += f"**Fecha:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    cabecera += "---\n\n"
    return cabecera


def extraer_contexto_negocio(negocio):
    if not negocio:
        return None
    tareas = negocio.get("tareas", [])
    tareas_pendientes = len([t for t in tareas if t.get("estado") != "HECHO"])
    sitio_web = negocio.get("sitio_web", {}) or {}
    tiene_web = bool(sitio_web.get("archivo_generado"))
    return {
        "nombre": negocio.get("nombre", ""),
        "sector": negocio.get("sector_contexto") or negocio.get("sector", "General"),
        "descripcion": negocio.get("descripcion", ""),
        "tareas_pendientes": tareas_pendientes,
        "tiene_web": tiene_web,
    }


# ==========================================
# TEST MANUAL
# ==========================================
if __name__ == "__main__":
    print("=" * 70)
    print("TEST ANALISIS PROFUNDO V1.4")
    print("=" * 70)

    # Test deteccion de tipo
    pruebas_tipo = [
        ("Analiza mi marketing digital", "marketing"),
        ("Analiza mis finanzas del mes", "finanzas"),
        ("Analiza mi competencia", "competencia"),
        ("Analiza mi web", "web"),
        ("Analiza mi operacion", "operacion"),
        ("Hola, como estas?", "general"),
    ]

    ok_tipo = 0
    for texto, esperado in pruebas_tipo:
        resultado = detectar_tipo_analisis(texto)
        icono = "OK" if resultado == esperado else "FALLO"
        if resultado == esperado:
            ok_tipo += 1
        print(f"[{icono}] '{texto[:40]}' -> {resultado} (esp: {esperado})")

    # Test deteccion general
    print("\nTest deteccion analisis:")
    pruebas_det = [
        ("Hola, como estas?", False),
        ("Necesito un analisis profundo del mercado", True),
        ("[EJECUTAR] dame el estudio", True),
        ("Analiza mi marketing", True),
    ]
    ok_det = 0
    for texto, esperado in pruebas_det:
        resultado = es_analisis_profundo(texto)
        icono = "OK" if resultado == esperado else "FALLO"
        if resultado == esperado:
            ok_det += 1
        print(f"[{icono}] '{texto[:50]}' -> {resultado}")

    print(f"\nTipo: {ok_tipo}/{len(pruebas_tipo)}")
    print(f"Deteccion: {ok_det}/{len(pruebas_det)}")
    print("=" * 70)