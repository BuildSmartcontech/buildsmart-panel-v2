# panels/panel_dueno.py
# ============================================
# PANEL DUENO V4.0 - ROUTER PRINCIPAL
# ============================================
# V4.0: Modularizado en panels/dueno/ (7 tabs)
# V3.1: Tab Salud del sistema
# V3.0: Republicar web forzado
# V2.9: Suspender/reactivar cuentas
# V2.8: Helper _plano()
# V2.7: Detalle cliente
# V2.6: Filtros de fecha globales
# ============================================
# Este archivo ahora es solo un router liviano.
# Toda la logica vive en panels/dueno/.
# ============================================

import streamlit as st
from config_app import ES_DUENO
from panels import panel_base
from panels.dueno import renderizar_control_total
from modules import css, sidebar, header_footer


def renderizar():
    """Punto de entrada del panel del dueno."""

    css.renderizar_css()
    panel_base.inicializar_session_state()
    BACKEND_ACTIVO = panel_base.verificar_backend()

    modulos = {
        "web": panel_base.WEB_DISPONIBLE,
        "email": panel_base.EMAIL_DISPONIBLE,
        "social": panel_base.SOCIAL_DISPONIBLE,
        "automation": panel_base.AUTOMATION_DISPONIBLE,
        "research": panel_base.RESEARCH_DISPONIBLE,
    }

    header_footer.renderizar_header(BACKEND_ACTIVO, modulos)

    accion = sidebar.renderizar_sidebar(BACKEND_ACTIVO, modulos, st.session_state.negocios)

    if accion:
        if accion.get("accion") == "crear_negocio":
            panel_base.crear_negocio(accion["nombre"], accion["icono"], accion["descripcion"])
            st.rerun()
        elif accion.get("accion") == "seleccionar_negocio":
            st.session_state.negocio_seleccionado = accion["negocio_id"]
            st.rerun()

    # Bloque CONTROL TOTAL (solo si es dueno)
    if ES_DUENO:
        renderizar_control_total()
        st.divider()

    # Contenido base (igual que un usuario normal)
    panel_base.renderizar_seleccion_negocio()
    panel_base.renderizar_dashboard_negocio()
    panel_base.renderizar_chat(BACKEND_ACTIVO)

    header_footer.renderizar_footer(BACKEND_ACTIVO, modulos)