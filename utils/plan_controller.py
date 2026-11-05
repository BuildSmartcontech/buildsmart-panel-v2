# utils/plan_controller.py
# ============================================
# CONTROLADOR DE PLANES Y LÍMITES (SaaS)
# ============================================

import datetime
import streamlit as st
try:
    from utils.supabase_rest import supabase_rest
except ImportError:
    supabase_rest = None

PLANES_VALIDOS = ["esencial", "premium_crm", "premium_plus", "enterprise"]
LIMITE_CONVERSACIONES_MENSUALES = 1500

def obtener_datos_cliente(cliente_id):
    """Busca el plan, país y estado del cliente en Supabase."""
    if not supabase_rest or not supabase_rest.disponible:
        return {"plan": "premium_plus", "pais": "CO", "conversaciones_mes": 0}

    try:
        res = supabase_rest.table("clientes").select("plan, pais").eq("id", cliente_id).execute()
        if res.data and len(res.data) > 0:
            return res.data[0]
    except Exception as e:
        print(f"[PLAN ERROR] No se pudo obtener cliente: {e}")
    
    return {"plan": "esencial", "pais": "CO"}

def contar_conversaciones_mes(cliente_id):
    """Cuenta cuántos mensajes ha procesado el ARM en el mes actual."""
    if not supabase_rest or not supabase_rest.disponible:
        return 0
        
    try:
        hoy = datetime.date.today()
        primer_dia_mes = hoy.replace(day=1).isoformat()
        
        res = supabase_rest.table("arm_logs").select("id", count="exact").eq("cliente_id", cliente_id).gte("created_at", primer_dia_mes).execute()
        return res.count if res.count else 0
    except Exception as e:
        print(f"[PLAN ERROR] Error contando mensajes: {e}")
        return 0

def recomendar_plan(volumen_mensual):
    """
    Lógica de negocio basada en la investigación de mercado.
    - < 500: CRM (No necesita ARM aún)
    - 500 - 1500: ARM Pro (Premium Plus)
    - > 1500: Enterprise (Requiere customización)
    """
    if volumen_mensual < 500:
        return "Premium + CRM", "Tu volumen es bajo. Te recomendamos el plan CRM. El ARM sería un gasto innecesario por ahora."
    elif 500 <= volumen_mensual <= 1500:
        return "Web Premium Plus", "¡El plan perfecto para ti! Tu volumen encaja exacto con el ARM Pro de $150/mes (incluye 1,500 mensajes)."
    else:
        return "Enterprise", "Tu volumen es muy alto. El plan Premium Plus no soportará tu flujo. Contacta a ventas para un plan Enterprise personalizado."

def verificar_acceso_arm(cliente_id):
    """
    Valida si el cliente puede usar el ARM.
    Retorna (tiene_acceso, mensaje_error)
    """
    datos = obtener_datos_cliente(cliente_id)
    plan = datos.get("plan", "esencial")
    
    if plan not in ["premium_plus", "enterprise"]:
        return False, "🚫 **Requiere Web Premium Plus**\n\nEl módulo ARM solo está disponible en el plan Premium Plus o Enterprise."
    
    if plan == "enterprise":
        return True, "✅ Acceso Enterprise concedido (Sin límites)."
    
    conversaciones_usadas = contar_conversaciones_mes(cliente_id)
    
    if conversaciones_usadas >= LIMITE_CONVERSACIONES_MENSUALES:
        return False, (
            f"⚠️ **Límite Mensual Alcanzado ({LIMITE_CONVERSACIONES_MENSUALES} conversaciones)**\n\n"
            f"Has usado {conversaciones_usadas}/{LIMITE_CONVERSACIONES_MENSUALES} este mes.\n\n"
            "Para seguir usando el ARM, puedes:\n"
            "1. Comprar un Add-on de 500 conversaciones extra.\n"
            "2. Actualizar al plan Enterprise."
        )
    
    return True, f"✅ Acceso concedido. Llevas {conversaciones_usadas}/{LIMITE_CONVERSACIONES_MENSUALES} conversaciones."