# utils/chat_detector.py
# ============================================
# DETECTOR DE INTENCIONES DEL CHAT - V1.2
# ============================================
# V1.2: Mensajes largos (>200 chars) se tratan como "consultar"
# para permitir prompts de personalidad sin que se confundan con "ayuda"
# ============================================

import os
import sys
import json
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend.gateway import gateway
    GATEWAY_DISPONIBLE = True
except ImportError:
    try:
        from gateway import gateway
        GATEWAY_DISPONIBLE = True
    except ImportError:
        GATEWAY_DISPONIBLE = False
        gateway = None


INTENTS_DISPONIBLES = {
    "crear_web": "El usuario quiere crear/generar/hacer su primera web.",
    "modificar_web": "El usuario quiere cambiar/arreglar/editar algo de su web existente.",
    "vincular_web": "El usuario quiere vincular una URL externa.",
    "ver_modificaciones": "El usuario pregunta cuantas modificaciones le quedan.",
    "ver_web": "El usuario quiere ver su web.",
    "ver_tareas": "El usuario quiere ver sus tareas pendientes o completadas.",
    "crear_tarea": "El usuario quiere agregar una nueva tarea.",
    "enviar_correo": "El usuario quiere enviar un correo electronico.",
    "investigar": "El usuario quiere investigar un tema de mercado o competencia.",
    "estado_negocio": "El usuario pregunta por el estado general de su negocio.",
    "configurar_asistente": "El usuario quiere configurar la personalidad o el rol de su asistente IA. Ejemplos: 'Eres SAMU IA...', 'Actua como un CEO...', 'Tu objetivo es...'.",
    "ayuda": "El usuario pide ayuda, comandos disponibles, o no sabe que hacer. SOLO cuando el mensaje es CORTO y pide comandos.",
    "fuera_de_tema": "El usuario pregunta algo que NO tiene relacion con su negocio (chistes, historia, politica, matematicas, programacion general, etc).",
    "consultar": "Pregunta general, instruccion larga, o prompt personalizado. Intent por defecto.",
}


def construir_system_prompt(contexto):
    intents_str = "\n".join([f"- {k}: {v}" for k, v in INTENTS_DISPONIBLES.items()])

    return f"""Eres un detector de intenciones para SAMU IA, un sistema de gestion de negocios.

Tu trabajo: leer lo que dice el usuario y devolver SOLO un JSON con esta estructura exacta:
{{
  "intent": "<nombre_del_intent>",
  "params": {{...}},
  "confianza": <0.0 a 1.0>
}}

INTENTS DISPONIBLES:
{intents_str}

CONTEXTO ACTUAL DEL USUARIO:
{contexto}

REGLAS CRITICAS:
1. ENTIENDE TYPOS: "geb" = "web", "kiero" = "quiero", "ke" = "que", "pa" = "para"
2. ENTIENDE DIALECTOS LATINOAMERICANOS
3. ENTIENDE SPANGLISH
4. NO REQUIERE PALABRAS EXACTAS. Entiende la INTENCION.

REGLA CRITICA SOBRE MENSAJES LARGOS (IMPORTANTE):
- Si el mensaje del usuario tiene MAS DE 200 CARACTERES, casi siempre es un PROMPT PERSONALIZADO o una instruccion de personalidad. En ese caso:
  * Devuelve "configurar_asistente" (si empieza con "Eres...", "Actua como...", "Tu objetivo...", "Tu mision...", "Debes...")
  * O "consultar" (para cualquier otra instruccion larga)
  * NUNCA lo clasifiques como "ayuda" solo porque mencione las palabras "web", "tareas", "correo"

REGLA SOBRE "AYUDA":
- Solo es "ayuda" cuando el mensaje es CORTO (<50 caracteres) y pide explicitamente comandos.
- Ejemplos: "ayuda", "help", "que puedo hacer", "comandos", "como funciona"

REGLA SOBRE TEMAS FUERA DEL NEGOCIO:
Si el usuario pregunta algo que NO tiene NADA que ver con su negocio (chistes, historia, politica, ciencia, etc.), marca "fuera_de_tema".

SOLO son temas VALIDOS para el negocio:
- El negocio del usuario
- Su web (crear, modificar, ver)
- Sus tareas
- Su correo
- Sus redes sociales
- Investigacion de mercado
- Como usar SAMU IA
- Configurar el asistente

EJEMPLOS:
- "parce arreglame la geb" -> modificar_web
- "che ponele fotos de arepas" -> modificar_web
- "muestrame lo ke tengo pendiente" -> ver_tareas
- "orale mandame un mail a juan@x.com" -> enviar_correo
- "cuantas modificaciones me kedan" -> ver_modificaciones
- "que puedo hacer?" -> ayuda (CORTO, pide comandos)
- "como va mi negocio?" -> estado_negocio
- "quien gano el mundial" -> fuera_de_tema
- "recitame un poema" -> fuera_de_tema
- "Eres SAMU IA, tu objetivo es..." (LARGO) -> configurar_asistente
- "Actua como un CEO experto..." (LARGO) -> configurar_asistente
- "Necesito que me ayudes con un plan de marketing extenso que incluya..." (LARGO) -> consultar

RESPONDE SOLO CON EL JSON. Sin markdown, sin explicaciones."""


def extraer_json(texto):
    if not texto:
        return None
    texto = texto.strip()
    if texto.startswith("```"):
        texto = re.sub(r'^```(?:json)?\s*', '', texto)
        texto = re.sub(r'\s*```$', '', texto)
    inicio = texto.find("{")
    fin = texto.rfind("}")
    if inicio == -1 or fin == -1:
        return None
    json_str = texto[inicio:fin + 1]
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None


def _parece_prompt_personalidad(mensaje):
    """Detecta si un mensaje parece un prompt de personalidad."""
    if not mensaje:
        return False
    # Mensajes cortos no son prompts
    if len(mensaje) < 150:
        return False

    indicadores = [
        "eres ", "actua como", "actúa como", "tu objetivo", "tu misión",
        "tu mision", "debes ", "serás ", "seras ", "asistente virtual",
        "director de", "consultor", "tu rol", "rol de", "comportate",
        "comportate como", "comportate como", "asume el rol"
    ]

    msg_lower = mensaje.lower()
    for ind in indicadores:
        if ind in msg_lower:
            return True

    # Mensajes muy largos (>500) son probablemente prompts
    if len(mensaje) > 500:
        return True

    return False


def detectar_intencion(mensaje, contexto=""):
    resultado_base = {
        "exito": False,
        "intent": "consultar",
        "params": {},
        "confianza": 0.0,
        "error": None,
        "fuente": None,
    }

    if not GATEWAY_DISPONIBLE or gateway is None:
        resultado_base["error"] = "Gateway no disponible"
        return resultado_base

    if not mensaje or not mensaje.strip():
        resultado_base["error"] = "Mensaje vacio"
        return resultado_base

    # PRE-CHECK: detectar prompt de personalidad localmente sin gastar llamada
    if _parece_prompt_personalidad(mensaje):
        return {
            "exito": True,
            "intent": "configurar_asistente",
            "params": {"prompt": mensaje},
            "confianza": 0.9,
            "error": None,
            "fuente": "local"
        }

    try:
        system_prompt = construir_system_prompt(contexto)
        respuesta, fuente = gateway.chat_inteligente(mensaje, system_prompt)

        if not respuesta:
            resultado_base["error"] = "Respuesta vacia"
            return resultado_base

        data = extraer_json(respuesta)

        if not data or "intent" not in data:
            resultado_base["error"] = "JSON invalido: " + str(respuesta[:200])
            return resultado_base

        intent = data.get("intent", "consultar")
        if intent not in INTENTS_DISPONIBLES:
            intent = "consultar"

        return {
            "exito": True,
            "intent": intent,
            "params": data.get("params", {}),
            "confianza": float(data.get("confianza", 0.5)),
            "error": None,
            "fuente": fuente,
        }

    except Exception as e:
        resultado_base["error"] = "Excepcion: " + str(e)
        return resultado_base


if __name__ == "__main__":
    print("=" * 60)
    print("TEST DETECTOR V1.2")
    print("=" * 60)

    contexto = """
- Negocio: Dulceria Los Pinos
- Sector: alimentos
- Tiene web: SI (ID: abc123)
- Modificaciones usadas: 1/7
"""

    pruebas = [
        ("que puedo hacer?", "ayuda (CORTO)"),
        ("Eres SAMU IA, el asistente virtual de SAMU IA. Tu objetivo principal es actuar como Director de Operaciones y Consultor de Crecimiento de Elite para el usuario actual.", "configurar_asistente (LARGO)"),
        ("Actua como un CEO experto en marketing digital y ayudame con mi negocio", "configurar_asistente"),
        ("parce arreglame la geb", "modificar_web"),
        ("como va mi negocio", "estado_negocio"),
        ("quien gano el mundial", "fuera_de_tema"),
    ]

    for msg, esperado in pruebas:
        print("\n" + "-" * 60)
        print("Mensaje (" + str(len(msg)) + " chars): " + msg[:70])
        print("Esperado: " + esperado)
        r = detectar_intencion(msg, contexto)
        if r["exito"]:
            print("  Resultado: " + r["intent"] + " (" + str(r["confianza"]) + ")")

    print("\n" + "=" * 60)