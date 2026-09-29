# panels/panel_usuario.py
# ============================================
# V2.0: Agrega seccion "Mis Reportes" (analisis profundo)
# V1.0: Panel usuario inicial
# ============================================

import streamlit as st
from config_app import MODO, MOSTRAR_CREDITOS
from panels import panel_base, onboarding
from modules import css, sidebar, header_footer


def renderizar():
    """Renderiza el panel del usuario."""

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
            panel_base.crear_negocio(
                accion["nombre"], accion["icono"], accion["descripcion"]
            )
            st.rerun()
        elif accion.get("accion") == "seleccionar_negocio":
            st.session_state.negocio_seleccionado = accion["negocio_id"]
            st.rerun()

    # ==========================================
    # ONBOARDING INLINE (solo si NO hay negocios)
    # ==========================================
    if not onboarding.hay_negocios():
        onboarding.renderizar()
    else:
        # Panel normal
        panel_base.renderizar_seleccion_negocio()
        panel_base.renderizar_dashboard_negocio()

        # ==========================================
        # MIS REPORTES (analisis profundo)
        # ==========================================
        try:
            from panels import reportes_usuario
            reportes_usuario.renderizar()
        except Exception as e:
            print(f"[panel_usuario] Error cargando reportes: {e}")

    # Chat (siempre visible)
    panel_base.renderizar_chat(BACKEND_ACTIVO)

    header_footer.renderizar_footer(BACKEND_ACTIVO, modulos)