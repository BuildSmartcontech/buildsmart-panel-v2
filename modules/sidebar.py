# modules/sidebar.py
# ============================================

import streamlit as st
import datetime
from config_app import MODO, ES_DUENO, SISTEMA_CREDITOS_ACTIVO, MOSTRAR_CREDITOS, VERSION


def renderizar_sidebar(BACKEND_ACTIVO, modulos, negocios):
    """Renderiza el sidebar compartido."""

    with st.sidebar:
        if ES_DUENO:
            st.markdown("### 👑 SAMU IA - DUEÑO")
        else:
            st.markdown("###  SAMU IA")

        st.divider()

        # Info del modo
        if MODO == "prueba":
            st.warning(f"🧪 MODO PRUEBA")
            st.caption("Sin limites. Para pruebas.")
        else:
            st.success(f"✅ MODO PRODUCCION")

        st.caption(f"🔄 {datetime.datetime.now().strftime('%H:%M:%S')}")

        # Backend
        if BACKEND_ACTIVO:
            st.info("🧠 Backend: Activo")
        else:
            st.warning(" Backend: Inactivo")

        st.divider()

        # Modulos
        st.markdown("**🧩 Modulos:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"🧠 Backend: {'✅' if BACKEND_ACTIVO else '❌'}")
            st.markdown(f"🌐 Web: {'✅' if modulos.get('web') else '❌'}")
            st.markdown(f"📧 Email: {'✅' if modulos.get('email') else '❌'}")
        with col2:
            st.markdown(f"🐦 Social: {'✅' if modulos.get('social') else '❌'}")
            st.markdown(f"⚡ Auto: {'✅' if modulos.get('automation') else '❌'}")
            st.markdown(f"🔍 Research: {'✅' if modulos.get('research') else '❌'}")

        st.divider()

        # Modos (solo para dueno)
        if ES_DUENO:
            st.markdown("** Modos (Dueno)**")
            col1, col2 = st.columns(2)
            with col1:
                st.toggle("🤖 Auto", value=True, key="modo_auto")
            with col2:
                st.toggle("🧠 Dios", value=True, key="modo_dios")
            st.divider()

        # Creditos (solo si esta activo)
        if MOSTRAR_CREDITOS:
            st.markdown("**💳 Creditos Globales**")
            total_creditos = sum(n.get("creditos", 0) for n in negocios.values())
            col1, col2 = st.columns(2)
            col1.metric("Total", total_creditos)
            col2.metric("Negocios", len(negocios))
            st.divider()

        # Negocios
        st.markdown("**🏢 Negocios**")

        # CREAR NEGOCIO: solo si NO hay negocios, o si es el dueno
        if not negocios or ES_DUENO:
            with st.expander("➕ CREAR NUEVO NEGOCIO", expanded=False):
                nuevo_nombre = st.text_input("Nombre", placeholder="Ej: Mi Empresa", key="nuevo_nombre")
                nuevo_icono = st.text_input("Icono (emoji)", placeholder="🏢", max_chars=2, key="nuevo_icono")
                nueva_descripcion = st.text_area("Descripcion", placeholder="Breve descripcion", key="nueva_descripcion")

                if st.button("🚀 CREAR NEGOCIO", use_container_width=True, key="crear_negocio_btn"):
                    if nuevo_nombre and nuevo_icono and nueva_descripcion:
                        return {
                            "accion": "crear_negocio",
                            "nombre": nuevo_nombre,
                            "icono": nuevo_icono,
                            "descripcion": nueva_descripcion
                        }
                    else:
                        st.warning(" Completa todos los campos.")

        st.divider()

        # Lista de negocios
        for key, negocio in negocios.items():
            if MOSTRAR_CREDITOS:
                creditos = negocio.get("creditos", 0)
                label = f"{negocio['icono']} {negocio['nombre']} ({creditos}💳)"
            else:
                label = f"{negocio['icono']} {negocio['nombre']}"

            if st.button(label, key=f"nav_{key}", use_container_width=True):
                return {"accion": "seleccionar_negocio", "negocio_id": key}

        st.divider()

        # Info del dueno
        if ES_DUENO:
            st.caption("👑 Panel Dueño")
            st.caption("Tienes acceso total")
        else:
            st.caption(f"v{VERSION} · Usuario")

    return None