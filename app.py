# app.py - SAMU IA Operations Center
# ============================================
# DECIDE QUE PANEL MOSTRAR
# ============================================
# 1. Si URL tiene ?web=landing -> Landing Web Gancho
# 2. Si es dueno (env var) -> Panel Dueno
# 3. Si esta en tabla staff activo -> Panel Dueno (rol)
# 4. Si es usuario normal -> Panel Usuario
# ============================================

import streamlit as st
from config_app import ES_DUENO, MODO, NOMBRE_APP, VERSION, obtener_usuario_actual

# Configuracion de la pagina
st.set_page_config(
    page_title=f"{NOMBRE_APP} - {MODO.upper()}",
    page_icon=":office:",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# DETECTAR RUTA WEB GANCHO (?web=...)
# ==========================================
def detectar_subruta_web():
    """
    Detecta si el usuario esta navegando al modulo Web Gancho.
    Retorna la subruta o None si no aplica.
    Ejemplo: ?web=landing -> "landing"
    """
    try:
        params = st.query_params
        if "web" in params:
            valor = params.get("web", "")
            # Normalizar a string (a veces viene como lista)
            if isinstance(valor, list):
                valor = valor[0] if valor else ""
            return str(valor).strip() or "landing"
    except Exception:
        pass
    return None


# ==========================================
# DETECTAR ROL DEL USUARIO (ERP)
# ==========================================
def detectar_rol():
    """
    Retorna el rol del usuario actual o None si es usuario normal.
    - "dueno" si ES_DUENO es True
    - "admin"/"soporte"/"marketing" si esta en tabla staff
    - None si es usuario normal
    """
    if ES_DUENO:
        return "dueno"

    try:
        from utils.supabase_rest import supabase_rest
        if not supabase_rest.disponible:
            return None

        uid = obtener_usuario_actual()
        if not uid:
            return None

        rows = supabase_rest.table("staff").select("*").eq("usuario_id", uid).execute().data or []
        if not rows:
            return None

        staff_info = rows[0]
        if not staff_info.get("activo"):
            return None

        rol = staff_info.get("rol")
        if rol in ("admin", "soporte", "marketing"):
            st.session_state._staff_info = staff_info
            return rol
        return None

    except Exception as e:
        print(f"[app] Error detectando staff: {e}")
        return None


# ==========================================
# ROUTING
# ==========================================
subruta_web = detectar_subruta_web()

if subruta_web is not None:
    # ==== WEB GANCHO (modulo separado) ====
    print(f"[app] Modulo WEB GANCHO - subruta: {subruta_web}")
    st.session_state["_web_subruta"] = subruta_web

    from panels import web
    web.renderizar()

else:
    # ==== ERP PRINCIPAL ====
    from panels import panel_usuario, panel_dueno

    rol_actual = detectar_rol()
    st.session_state._rol_actual = rol_actual

    if rol_actual:
        print(f"[app] Usuario con rol: {rol_actual}")
    else:
        print("[app] Usuario normal")

    if rol_actual:
        panel_dueno.renderizar()
    else:
        panel_usuario.renderizar()