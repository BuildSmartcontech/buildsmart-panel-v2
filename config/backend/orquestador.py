# backend/orquestador.py - VERSIÓN 8.0 - CON DETECCIÓN DE INTENCIÓN
# ============================================

from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from backend.gateway import gateway
import time
import re
import os

# ========== ESTADO ==========
class Estado(TypedDict):
    mensaje: str
    plan: Optional[str]
    resultado: Optional[str]
    paso_actual: str
    historial: list
    negocio_id: Optional[str]

# ============================================
# FUNCIÓN: LIMPIAR RESPUESTA
# ============================================

def limpiar_respuesta(respuesta: str) -> str:
    """Elimina la cadena de pensamiento (<think>...</think>)"""
    if not respuesta:
        return respuesta
    respuesta = re.sub(r'<think>.*?</think>', '', respuesta, flags=re.DOTALL)
    respuesta = re.sub(r'<piensa>.*?</piensa>', '', respuesta, flags=re.DOTALL)
    respuesta = respuesta.replace('<think>', '').replace('</think>', '')
    respuesta = respuesta.replace('<piensa>', '').replace('</piensa>', '')
    respuesta = respuesta.strip()
    return respuesta

# ============================================
# DETECCIÓN DE INTENCIÓN
# ============================================

def es_mensaje_simple(mensaje: str) -> bool:
    """Detecta saludos o mensajes simples para camino rápido"""
    mensaje_lower = mensaje.lower().strip()
    palabras = mensaje_lower.split()
    
    # Saludos
    saludos = ['hola', 'buenos días', 'buenas tardes', 'buenas noches',
               'hey', 'qué tal', 'cómo estás', 'como estas', 'hi', 'hello',
               'buenas', 'saludos', 'qué hay', 'que hay']
    
    if len(palabras) <= 4:
        for saludo in saludos:
            if saludo in mensaje_lower:
                return True
    
    # Preguntas simples sin tarea
    palabras_tarea = ['plan', 'marketing', 'estrategia', 'buscar', 'investigar',
                      'crear', 'generar', 'analizar', 'desarrollar', 'diseñar',
                      'campaña', 'proyecto', 'negocio', 'empresa', 'video', 'imagen']
    
    if len(palabras) <= 6:
        tiene_tarea = any(p in mensaje_lower for p in palabras_tarea)
        if not tiene_tarea:
            return True
    
    return False

# ============================================
# CAMINO RÁPIDO (SALUDOS)
# ============================================

def ejecutar_camino_rapido(mensaje: str, negocio_id: str = None) -> dict:
    """Camino rápido: 1 llamada a Groq (1-2s)"""
    print("⚡ CAMINO RÁPIDO: Saludo simple detectado")
    print("-" * 60)
    
    try:
        sistema = """Eres un asistente amigable de BuildSmart Holdings.
        Responde de forma breve, cálida y profesional.
        NO generes planes ni listas. Solo responde al saludo.
        Máximo 2 frases."""
        
        respuesta, fuente = gateway.chat_rapido(mensaje, sistema)
        respuesta = limpiar_respuesta(respuesta)
        
        print(f"✅ Respuesta rápida con: {fuente}")
        
        try:
            from utils.supabase_client import supabase
            supabase.guardar_historial(
                mensaje=mensaje, respuesta=respuesta,
                modelo=fuente, negocio_id=negocio_id, fuente=fuente
            )
        except:
            pass
        
        return {
            "mensaje": mensaje, "plan": "", "resultado": respuesta,
            "resumen_ejecutivo": None, "pdf_url": None,
            "paso_actual": "fast_path",
            "historial": [{"nodo": "fast_path", "respuesta": respuesta}]
        }
    except Exception as e:
        print(f"❌ Error en camino rápido: {e}")
        return {
            "mensaje": mensaje, "plan": "", "resultado": f"⚠️ Error: {str(e)}",
            "resumen_ejecutivo": None, "pdf_url": None,
            "paso_actual": "error", "historial": []
        }

# ========== NODOS ==========

def nodo_brainstorm(estado: Estado) -> Estado:
    """Nodo 1: Genera ideas"""
    try:
        print("🧠 Brainstorm - Generando ideas...")
        time.sleep(0.3)
        
        sistema = "Eres un experto en estrategia de negocios. Responde de forma clara y directa."
        prompt = f"Solicitud: {estado['mensaje']}\n\nGenera un plan de acción paso a paso."
        
        respuesta, fuente = gateway.chat_inteligente(prompt, sistema)
        estado["plan"] = limpiar_respuesta(respuesta)
        print(f"✅ Brainstorm completado con: {fuente}")
    except Exception as e:
        estado["plan"] = f"⚠️ Error: {str(e)}"
        print(f"❌ Error en brainstorm: {e}")
    
    estado["paso_actual"] = "plan"
    estado["historial"] = estado.get("historial", []) + [{"nodo": "brainstorm", "respuesta": estado["plan"]}]
    return estado

def nodo_plan(estado: Estado) -> Estado:
    """Nodo 2: Convierte ideas en plan"""
    try:
        print("📋 Plan - Estructurando...")
        time.sleep(0.3)
        
        sistema = "Eres un planificador de proyectos experto. Responde de forma clara y directa."
        prompt = f"Ideas: {estado['plan']}\n\nConvierte esto en un plan detallado."
        
        respuesta, fuente = gateway.chat_inteligente(prompt, sistema)
        estado["resultado"] = limpiar_respuesta(respuesta)
        print(f"✅ Plan completado con: {fuente}")
    except Exception as e:
        estado["resultado"] = f"⚠️ Error: {str(e)}"
        print(f"❌ Error en plan: {e}")
    
    estado["paso_actual"] = "work"
    estado["historial"] = estado.get("historial", []) + [{"nodo": "plan", "respuesta": estado["resultado"]}]
    return estado

def nodo_work(estado: Estado) -> Estado:
    """Nodo 3: Ejecuta tareas"""
    try:
        from backend.herramientas import herramientas
        print("⚡ Work - Ejecutando...")
        time.sleep(0.3)
        
        mensaje = estado["mensaje"]
        
        if any(word in mensaje.lower() for word in ['buscar', 'investigar', 'busca', 'noticias']):
            print("   🔍 Búsqueda detectada")
            busqueda = herramientas.buscar(mensaje)
            estado["resultado"] = f"🔍 Resultados:\n\n{limpiar_respuesta(busqueda)}"
        else:
            print("   📝 Procesamiento general")
            sistema = "Eres un ejecutor experto. Responde de forma clara y directa."
            prompt = f"Responde a: {mensaje}"
            respuesta, fuente = gateway.chat_inteligente(prompt, sistema)
            estado["resultado"] = limpiar_respuesta(respuesta)
        
        print("✅ Work completado")
    except Exception as e:
        estado["resultado"] = f"⚠️ Error: {str(e)}"
        print(f"❌ Error en work: {e}")
    
    estado["paso_actual"] = "review"
    estado["historial"] = estado.get("historial", []) + [{"nodo": "work", "respuesta": estado["resultado"]}]
    return estado

def nodo_review(estado: Estado) -> Estado:
    """Nodo 4: Revisa"""
    try:
        print("🔍 Review - Evaluando...")
        time.sleep(0.3)
        
        sistema = "Eres un editor experto. Responde de forma clara y directa."
        prompt = f"Revisa y mejora:\n{estado.get('resultado', '')}"
        
        respuesta, fuente = gateway.chat_inteligente(prompt, sistema)
        estado["resultado"] = limpiar_respuesta(respuesta)
        print(f"✅ Review completado con: {fuente}")
    except Exception as e:
        print(f"⚠️ Review falló: {e}")
    
    estado["paso_actual"] = "compound"
    estado["historial"] = estado.get("historial", []) + [{"nodo": "review", "respuesta": estado["resultado"]}]
    return estado

def nodo_compound(estado: Estado) -> Estado:
    """Nodo 5: Sintetiza"""
    try:
        print("📊 Compound - Sintetizando...")
        time.sleep(0.3)
        
        sistema = "Eres un comunicador experto. Responde de forma clara y concisa."
        prompt = f"Sintetiza:\nPlan: {estado.get('plan', '')}\n\nResultado: {estado.get('resultado', '')}"
        
        respuesta, fuente = gateway.chat_inteligente(prompt, sistema)
        estado["resultado"] = limpiar_respuesta(respuesta)
        print(f"✅ Compound completado con: {fuente}")
    except Exception as e:
        estado["resultado"] = f"⚠️ Error: {str(e)}"
        print(f"❌ Error en compound: {e}")
    
    estado["paso_actual"] = "finish"
    estado["historial"] = estado.get("historial", []) + [{"nodo": "compound", "respuesta": estado["resultado"]}]
    return estado

# ========== CONSTRUIR GRAFICO ==========

def crear_orquestador():
    graph = StateGraph(Estado)
    graph.add_node("brainstorm", nodo_brainstorm)
    graph.add_node("plan", nodo_plan)
    graph.add_node("work", nodo_work)
    graph.add_node("review", nodo_review)
    graph.add_node("compound", nodo_compound)
    
    graph.set_entry_point("brainstorm")
    graph.add_edge("brainstorm", "plan")
    graph.add_edge("plan", "work")
    graph.add_edge("work", "review")
    graph.add_edge("review", "compound")
    graph.add_edge("compound", END)
    return graph.compile()

# ========== FUNCIONES AUXILIARES ==========

def guardar_en_supabase(mensaje: str, respuesta: str, modelo: str = None,
                        negocio_id: str = None, fuente: str = None, usuario: str = 'anonimo'):
    try:
        from utils.supabase_client import supabase
        return supabase.guardar_historial(
            mensaje=mensaje, respuesta=respuesta, modelo=modelo,
            negocio_id=negocio_id, fuente=fuente, usuario=usuario
        )
    except:
        return False

def generar_resumen_ejecutivo(plan_completo: str) -> str:
    try:
        sistema = "Eres un ejecutivo experto en marketing. Genera un resumen conciso."
        prompt = f"Genera un resumen ejecutivo (máximo 200 palabras):\n{plan_completo}"
        respuesta, fuente = gateway.chat_rapido(prompt, sistema)
        return limpiar_respuesta(respuesta)
    except Exception as e:
        return f"Error: {str(e)}"

def generar_pdf_del_plan(contenido: str, titulo: str = "Plan de Marketing") -> str:
    try:
        from utils.pdf_generator import generar_pdf_plan
        return generar_pdf_plan(contenido, titulo)
    except:
        return None

# ========== EJECUTAR ==========

def ejecutar_orquestador(mensaje: str, negocio_id: Optional[str] = None) -> dict:
    try:
        print("=" * 60)
        print("🚀 INICIANDO ORQUESTADOR - VERSIÓN 8.0")
        print("=" * 60)
        print(f"📝 Mensaje: {mensaje[:100]}...")
        print("-" * 60)
        
        # Detección de intención
        if es_mensaje_simple(mensaje):
            return ejecutar_camino_rapido(mensaje, negocio_id)
        
        # Camino completo
        print("🔄 CAMINO COMPLETO: Tarea compleja")
        
        orquestador = crear_orquestador()
        estado_inicial = {
            "mensaje": mensaje, "plan": None, "resultado": None,
            "paso_actual": "inicio", "historial": [], "negocio_id": negocio_id
        }
        
        resultado = orquestador.invoke(estado_inicial)
        
        print("-" * 60)
        print("✅ ORQUESTADOR COMPLETADO")
        print("=" * 60)
        
        guardar_en_supabase(
            mensaje=mensaje, respuesta=resultado.get("resultado", ""),
            modelo="openrouter", negocio_id=negocio_id, fuente="nube"
        )
        
        plan_completo = resultado.get("resultado", "")
        pdf_url = None
        resumen = None
        
        if plan_completo and len(plan_completo) > 500:
            print("📄 Generando resumen ejecutivo...")
            resumen = generar_resumen_ejecutivo(plan_completo)
            print("📄 Generando PDF...")
            pdf_url = generar_pdf_del_plan(plan_completo, "Plan de Marketing BuildSmart")
            if pdf_url:
                print(f"✅ PDF guardado en: {pdf_url}")
        
        return {
            "mensaje": resultado["mensaje"], "plan": resultado.get("plan", ""),
            "resultado": resultado.get("resultado", ""),
            "resumen_ejecutivo": resumen, "pdf_url": pdf_url,
            "paso_actual": resultado.get("paso_actual", "finish"),
            "historial": resultado.get("historial", [])
        }
    except Exception as e:
        print(f"❌ Error en orquestador: {e}")
        return {
            "mensaje": mensaje, "plan": "", "resultado": f"⚠️ Error: {str(e)}",
            "resumen_ejecutivo": None, "pdf_url": None,
            "paso_actual": "error", "historial": []
        }

if __name__ == "__main__":
    print("\n🧪 PRUEBA 1: Saludo")
    resultado = ejecutar_orquestador("Hola")
    print(f"📌 Respuesta: {resultado['resultado'][:200]}")
    
    print("\n" + "=" * 60)
    print("\n🧪 PRUEBA 2: Tarea compleja")
    resultado = ejecutar_orquestador("Necesito un plan de marketing")
    print(f"📌 Respuesta: {resultado['resultado'][:300]}...")