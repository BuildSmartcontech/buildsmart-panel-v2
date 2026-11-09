# app.py - SAMU IA Operations Center
import streamlit as st
import traceback

if "_session_initialized" not in st.session_state:
    st.session_state._session_initialized = True
    st.session_state._rerun_count = 0
    st.session_state._rol_actual = None

st.session_state._rerun_count += 1
print(f"[RERUN {st.session_state._rerun_count}] Iniciando app...")

from config_app import ES_DUENO, MODO, NOMBRE_APP, VERSION, obtener_usuario_actual

# Sidebar colapsado por defecto
st.set_page_config(
    page_title=f"{NOMBRE_APP} - {MODO.upper()}",
    page_icon=":office:",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

def detectar_subruta_web():
    try:
        params = st.query_params
        if "web" in params:
            valor = params.get("web", "")
            if isinstance(valor, list):
                valor = valor[0] if valor else ""
            return str(valor).strip() or "landing"
    except Exception:
        pass
    return None

def detectar_rol():
    if ES_DUENO:
        return "dueno"
    try:
        from utils.supabase_rest import supabase_rest
        if not supabase_rest.disponible: return None
        uid = obtener_usuario_actual()
        if not uid: return None
        rows = supabase_rest.table("staff").select("*").eq("usuario_id", uid).execute().data or []
        if not rows: return None
        staff_info = rows[0]
        if not staff_info.get("activo"): return None
        rol = staff_info.get("rol")
        if rol in ("admin", "soporte", "marketing"):
            st.session_state._staff_info = staff_info
            return rol
        return None
    except Exception as e:
        print(f"[app] Error detectando staff: {e}")
        return None

subruta_web = detectar_subruta_web()

if subruta_web in ("admin", "app"):
    print(f"[app] Acceso al ERP - Ruta: {subruta_web}")
    try:
        from panels import panel_usuario, panel_dueno
        rol_actual = detectar_rol()
        st.session_state._rol_actual = rol_actual
        if rol_actual:
            print(f"[app] Usuario con rol: {rol_actual}")
            panel_dueno.renderizar()
        else:
            print("[app] Usuario normal (ERP)")
            panel_usuario.renderizar()
    except Exception as e:
        st.error(f"Error crítico cargando el panel: {e}")
        print(traceback.format_exc())
else:
    if subruta_web is None:
        subruta_web = "landing"
        
    print(f"[app] Modulo WEB GANCHO - subruta: {subruta_web}")
    st.session_state["_web_subruta"] = subruta_web
    try:
        from panels import web
        web.renderizar()
    except Exception as e:
        st.error(f"Error cargando Web Gancho: {e}")
        print(traceback.format_exc())