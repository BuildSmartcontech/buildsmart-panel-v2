# panels/dueno/__init__.py
# ============================================
# ROUTER INTERNO - Panel Dueno SAMU IA V6.1
# ============================================
# V6.1: Agrega tab ARM (13 tabs)
# ============================================

import streamlit as st
from config_app import MODO, ES_DUENO, VERSION

from panels.dueno import comun as C
from panels.dueno import (
    tab_panel,
    tab_clientes,
    tab_ingresos,
    tab_webs,
    tab_uso_ia,
    tab_moderacion,
    tab_auditoria,
    tab_registros,
    tab_pedidos_web,
    tab_staff,
    tab_config,
    tab_salud,
    tab_arm, # <-- NUEVO
    detalle_cliente,
)


# ==========================================
# DEFINICION DE TABS POR ROL
# ==========================================

TABS_DEF = [
    # (clave, label, funcion, permiso, args)
    ("panel",        f"{C.E_PANEL} Panel",           tab_panel,          "panel.ver",         "con_filtro"),
    ("clientes",     f"{C.E_CLIENTES} Clientes",     tab_clientes,       "clientes.ver",      "con_filtro"),
    ("pedidos",      f"\U0001F4E6 Pedidos Web",      tab_pedidos_web,    "pedidos_web.ver",   "con_filtro"),
    ("ingresos",     f"{C.E_DINERO} Ingresos",       tab_ingresos,       "ingresos.ver",      "con_filtro"),
    ("webs",         f"{C.E_GLOBO} Webs",            tab_webs,           "webs.ver",          "con_filtro"),
    ("arm",          f"🤖 ARM",                      tab_arm,            "arm.ver",           "con_filtro"), # <-- NUEVO
    ("uso_ia",       f"{C.E_RAYO} Uso IA",           tab_uso_ia,         "uso_ia.ver",        "con_filtro"),
    ("moderacion",   f"{C.E_ENGANCHE} Moderacion",   tab_moderacion,     "moderacion.usar",   "con_filtro"),
    ("auditoria",    f"{C.E_LIBRO} Auditoria",       tab_auditoria,      "auditoria.ver",     "con_filtro"),
    ("registros",    f"{C.E_LIBRO} Registros",       tab_registros,      "registros.ver",     "con_filtro"),
    ("staff",        f"{C.E_USUARIO} Staff",         tab_staff,          "staff.ver",         "solo_sb"),
    ("config",       f"{C.E_ENGANCHE} Configuracion",tab_config,         "config.usar",       "solo_sb"),
    ("salud",        f"{C.E_SALUD} Salud",           tab_salud,          "salud.ver",         "solo_sb"),
]


def _tiene_permiso(rol, permiso):
    if rol == "dueno":
        return True
    try:
        from utils import staff as S
        return S.tiene_permiso(rol, permiso)
    except Exception:
        return False


def _tabs_para_rol(rol):
    return [t for t in TABS_DEF if _tiene_permiso(rol, t[3])]


def renderizar_control_total():
    """Punto de entrada del bloque CONTROL TOTAL del dueno."""

    cliente_sel = st.session_state.get("cliente_detalle_id")
    if cliente_sel:
        detalle_cliente.renderizar(cliente_sel)
        return

    rol_actual = st.session_state.get("_rol_actual", "dueno")

    if rol_actual == "dueno":
        st.markdown(f"# {C.E_CORONA} CONTROL TOTAL - SAMU IA")
        st.caption(f"Modo: **{MODO}** | Version: **{VERSION}** | Dueno: **Antonio**")
    else:
        try:
            from utils import staff as S
            info_rol = S.info_rol(rol_actual)
            nombre_rol = info_rol.get("nombre", rol_actual)
        except Exception:
            nombre_rol = rol_actual.capitalize()

        st.markdown(f"# {C.E_USUARIO} PANEL {nombre_rol.upper()} - SAMU IA")
        st.caption(f"Modo: **{MODO}** | Version: **{VERSION}** | Rol: **{nombre_rol}**")

    sb = C._get_supabase()
    if sb is None:
        st.error(f"{C.E_AVISO} Supabase no disponible. Revisa utils/supabase_rest.py y .env.")
        return

    st.markdown(f"#### {C.E_CALENDAR} Filtro de fechas")
    inicio, fin, etiqueta = C._selector_rango()
    st.caption(f"{C.E_LUPA} Mostrando: {etiqueta}")
    st.divider()

    tabs_permitidos = _tabs_para_rol(rol_actual)

    if not tabs_permitidos:
        st.warning(f"{C.E_AVISO} Tu rol ({rol_actual}) no tiene acceso a ninguna seccion.")
        return

    tab_labels = [t[1] for t in tabs_permitidos]
    tabs_ui = st.tabs(tab_labels)

    for i, tab_def in enumerate(tabs_permitidos):
        clave, label, funcion, permiso, tipo_args = tab_def

        with tabs_ui[i]:
            try:
                if tipo_args == "con_filtro":
                    funcion.renderizar(sb, inicio, fin)
                elif tipo_args == "solo_sb":
                    funcion.renderizar(sb)
            except Exception as e:
                st.error(f"{C.E_AVISO} Error en tab {clave}: {e}")
                print(f"[panel_dueno] Error renderizando {clave}: {e}")