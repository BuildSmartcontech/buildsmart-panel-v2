# utils/ai_usage_monitor.py
# ============================================
# MONITOR DE CONSUMO DE IA - V1.0
# ============================================

import os
import streamlit as st

def _get_supabase():
    try:
        from utils.supabase_rest import supabase_rest
        return supabase_rest if supabase_rest.disponible else None
    except Exception:
        return None

def verificar_limite(pedido_id, max_llamadas_vision=3, max_llamadas_texto=10):
    """
    Verifica si el pedido ya agotó sus llamadas de IA permitidas.
    """
    sb = _get_supabase()
    if not sb:
        return True, "Supabase no disponible. Saltando verificación."

    try:
        # 1. Contar llamadas de Visión
        res_vis = sb.table("consumo_ia").select("id").eq("pedido_id", pedido_id).eq("proveedor", "gemini_vision").execute()
        vision_count = len(res_vis.data) if res_vis.data else 0
        
        if vision_count >= max_llamadas_vision:
            return False, f"Límite de visión alcanzado ({vision_count}/{max_llamadas_vision})."

        # 2. Contar llamadas de Texto (OpenRouter/Groq)
        res_txt = sb.table("consumo_ia").select("id").eq("pedido_id", pedido_id).in_("proveedor", ["groq", "openrouter", "gemini_text"]).execute()
        texto_count = len(res_txt.data) if res_txt.data else 0
        
        if texto_count >= max_llamadas_texto:
            return False, f"Límite de generación de texto alcanzado ({texto_count}/{max_llamadas_texto})."

        return True, "OK"
    except Exception as e:
        print(f"[MONITOR] Error: {e}")
        return True, "Error en verificación. Permitiendo por seguridad."

def registrar_consumo(pedido_id, proveedor, texto_enviado, texto_recibido=""):
    """
    Registra el consumo en Supabase.
    """
    sb = _get_supabase()
    if not sb: return

    # Estimación rápida: 1 token ~ 4 caracteres
    tokens_estimados = (len(texto_enviado) + len(texto_recibido)) // 4
    
    # Costos aproximados (Muy conservadores)
    costo = 0.0
    if proveedor == "gemini_vision":
        costo = 0.0001  # $0.0001 por imagen
    elif proveedor == "groq":
        costo = 0.00005 # Groq es casi gratis
    elif proveedor == "openrouter":
        costo = 0.0002  # Modelos gratuitos, pero estimamos un costo mínimo

    try:
        sb.insert("consumo_ia", {
            "pedido_id": pedido_id,
            "proveedor": proveedor,
            "tokens_estimados": tokens_estimados,
            "costo_estimado_usd": costo
        })
        print(f"[MONITOR] Registrado: {proveedor} para pedido {pedido_id} (~{tokens_estimados} tokens)")
    except Exception as e:
        print(f"[MONITOR] Error al registrar: {e}")