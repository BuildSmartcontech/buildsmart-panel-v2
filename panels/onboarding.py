# panels/onboarding.py
# ============================================
# ONBOARDING INLINE - DENTRO DEL PANEL USUARIO
# ============================================

import streamlit as st
import datetime


def hay_negocios():
    return bool(st.session_state.get("negocios"))


def renderizar():
    if hay_negocios():
        return

    paso = st.session_state.get("onboarding_paso", "elegir")

    if paso == "elegir":
        mostrar_elegir_camino()
    elif paso == "desde_cero":
        mostrar_flujo_desde_cero()
    elif paso == "ya_tengo":
        mostrar_flujo_ya_tengo()


def mostrar_elegir_camino():
    st.markdown("## 👋 ¡Bienvenido a SAMU IA!")
    st.markdown("Cuentanos como quieres empezar. Adaptaremos la app a ti.")
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### 🆕 Empezar desde cero")
            st.caption("Perfecto si arrancas un negocio nuevo")
            st.write("")
            st.markdown("**Lo que hara la IA:**")
            st.markdown("✅ Crear la estructura de tu negocio")
            st.markdown("✅ Generar tus primeras tareas")
            st.markdown("✅ Preparar tus agentes IA")
            st.markdown("✅ Dejar lista tu web para generar")
            st.write("")
            if st.button("🚀 EMPEZAR DESDE CERO", use_container_width=True, type="primary", key="btn_desde_cero"):
                st.session_state.onboarding_paso = "desde_cero"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### 🏢 Ya tengo un negocio")
            st.caption("Perfecto si ya tienes clientes/procesos")
            st.write("")
            st.markdown("**Lo que hara la IA:**")
            st.markdown("✅ Importar tu informacion existente")
            st.markdown("✅ Adaptar tareas a tu sector")
            st.markdown("✅ Configurar los modulos que necesites")
            st.markdown("✅ Respetar tu web actual")
            st.write("")
            if st.button("🏢 YA TENGO NEGOCIO", use_container_width=True, type="primary", key="btn_ya_tengo"):
                st.session_state.onboarding_paso = "ya_tengo"
                st.rerun()


def mostrar_flujo_desde_cero():
    st.markdown("## 🆕 Empecemos desde cero")
    st.caption("La IA creara la estructura basica de tu negocio. Luego puedes personalizar todo.")
    st.write("")

    paso = st.session_state.get("cero_paso", 1)
    st.progress(paso / 4, text=f"Paso {paso} de 4")
    st.write("")

    if paso == 1:
        st.markdown("### 📝 ¿Como se llamara tu negocio?")
        nombre = st.text_input("Nombre del negocio", value=st.session_state.get("cero_nombre", ""), placeholder="Ej: Mi Panaderia La Espiga", key="inp_cero_nombre")
        st.write("")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(" Cancelar", use_container_width=True, key="cero_cancel"):
                st.session_state.onboarding_paso = "elegir"
                st.rerun()
        with col2:
            if st.button("Siguiente ", use_container_width=True, type="primary", key="cero_next_1"):
                if nombre.strip():
                    st.session_state.cero_nombre = nombre.strip()
                    st.session_state.cero_paso = 2
                    st.rerun()
                else:
                    st.warning(" Escribe un nombre")

    elif paso == 2:
        st.markdown("###  ¿A que se dedica?")
        sector = st.text_input("Sector o rubro", value=st.session_state.get("cero_sector", ""), placeholder="Ej: Panaderia artesanal", key="inp_cero_sector")
        publico = st.text_input("¿Quienes son tus clientes?", value=st.session_state.get("cero_publico", ""), placeholder="Ej: Familias del barrio", key="inp_cero_publico")
        st.write("")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(" Atras", use_container_width=True, key="cero_back_2"):
                st.session_state.cero_paso = 1
                st.rerun()
        with col2:
            if st.button("Siguiente ", use_container_width=True, type="primary", key="cero_next_2"):
                if sector.strip():
                    st.session_state.cero_sector = sector.strip()
                    st.session_state.cero_publico = publico.strip() or "Clientes locales"
                    st.session_state.cero_paso = 3
                    st.rerun()
                else:
                    st.warning(" Escribe el sector")

    elif paso == 3:
        st.markdown("### 🎯 ¿Que modulos necesitas?")
        st.caption("Selecciona los servicios que quieres activar. Puedes cambiarlos luego.")
        st.write("")

        web = st.checkbox("🌐 Web profesional con IA", value=True, key="cero_chk_web")
        kanban = st.checkbox("📋 Kanban de tareas", value=True, key="cero_chk_kanban")
        crm = st.checkbox("👥 CRM (gestion de clientes)", value=False, key="cero_chk_crm")
        social = st.checkbox("🐦 Redes sociales", value=False, key="cero_chk_social")
        contabilidad = st.checkbox("💰 Contabilidad (proximamente Odoo)", value=False, key="cero_chk_contab")
        research = st.checkbox("🔍 Investigacion de mercado", value=False, key="cero_chk_research")

        st.write("")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(" Atras", use_container_width=True, key="cero_back_3"):
                st.session_state.cero_paso = 2
                st.rerun()
        with col2:
            if st.button("Siguiente ", use_container_width=True, type="primary", key="cero_next_3"):
                st.session_state.cero_modulos = {
                    "web": web, "kanban": kanban, "crm": crm,
                    "social": social, "contabilidad": contabilidad, "research": research
                }
                st.session_state.cero_paso = 4
                st.rerun()

    elif paso == 4:
        st.markdown("### 🎉 ¡Todo listo!")
        st.write("Esto es lo que crearemos:")
        st.write("")
        with st.container(border=True):
            st.markdown(f"**📝 Nombre:** {st.session_state.get('cero_nombre', '')}")
            st.markdown(f"** Sector:** {st.session_state.get('cero_sector', '')}")
            st.markdown(f"**👥 Clientes:** {st.session_state.get('cero_publico', '')}")
        st.write("")
        with st.container(border=True):
            modulos_sel = st.session_state.get("cero_modulos", {})
            st.markdown("**🤖 La IA generara:**")
            st.markdown(f"• Tareas iniciales para arrancar")
            st.markdown(f"• Agentes IA configurados")
            activos = [k for k, v in modulos_sel.items() if v]
            st.markdown(f"• Modulos activos: {', '.join(activos) or 'ninguno'}")
        st.write("")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(" Atras", use_container_width=True, key="cero_back_4"):
                st.session_state.cero_paso = 3
                st.rerun()
        with col2:
            if st.button("🚀 CREAR MI NEGOCIO", use_container_width=True, type="primary", key="cero_crear"):
                crear_negocio_desde_cero()
                st.rerun()


def mostrar_flujo_ya_tengo():
    st.markdown("## 🏢 Adaptemos tu negocio")
    st.caption("Cuentanos que tienes y adaptaremos la app a tu operacion actual.")
    st.write("")

    paso = st.session_state.get("ya_paso", 1)
    st.progress(paso / 3, text=f"Paso {paso} de 3")
    st.write("")

    if paso == 1:
        st.markdown("### 📝 Datos de tu negocio")
        nombre = st.text_input("Nombre del negocio", value=st.session_state.get("ya_nombre", ""), placeholder="Ej: Constructora XYZ", key="inp_ya_nombre")
        sector = st.text_input("Sector", value=st.session_state.get("ya_sector", ""), placeholder="Ej: Construccion y reformas", key="inp_ya_sector")
        st.write("")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(" Cancelar", use_container_width=True, key="ya_cancel"):
                st.session_state.onboarding_paso = "elegir"
                st.rerun()
        with col2:
            if st.button("Siguiente ", use_container_width=True, type="primary", key="ya_next_1"):
                if nombre.strip() and sector.strip():
                    st.session_state.ya_nombre = nombre.strip()
                    st.session_state.ya_sector = sector.strip()
                    st.session_state.ya_paso = 2
                    st.rerun()
                else:
                    st.warning(" Completa nombre y sector")

    elif paso == 2:
        st.markdown("### 📄 Cuentanos mas de tu negocio")
        descripcion = st.text_area(
            "Descripcion (opcional pero recomendado)",
            value=st.session_state.get("ya_descripcion", ""),
            placeholder="Ej: Somos una constructora con 15 anos de experiencia en reformas...",
            height=120,
            key="inp_ya_desc"
        )
        url_web = st.text_input(
            "¿Tienes web actual? (opcional)",
            value=st.session_state.get("ya_url_web", ""),
            placeholder="https://tu-web.com",
            key="inp_ya_url"
        )
        st.write("")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(" Atras", use_container_width=True, key="ya_back_2"):
                st.session_state.ya_paso = 1
                st.rerun()
        with col2:
            if st.button("Siguiente ", use_container_width=True, type="primary", key="ya_next_2"):
                st.session_state.ya_descripcion = descripcion.strip()
                st.session_state.ya_url_web = url_web.strip()
                st.session_state.ya_paso = 3
                st.rerun()

    elif paso == 3:
        st.markdown("### 🎯 ¿Que necesitas?")
        st.caption("Selecciona los modulos que quieres activar.")
        st.write("")

        web = st.checkbox("🌐 Gestionar web actual o crear nueva", value=bool(st.session_state.get("ya_url_web")), key="ya_chk_web")
        kanban = st.checkbox("📋 Kanban de tareas y proyectos", value=True, key="ya_chk_kanban")
        crm = st.checkbox("👥 CRM (gestion de clientes)", value=False, key="ya_chk_crm")
        social = st.checkbox("🐦 Redes sociales", value=False, key="ya_chk_social")
        contabilidad = st.checkbox("💰 Contabilidad (proximamente Odoo)", value=False, key="ya_chk_contab")
        research = st.checkbox("🔍 Investigacion de mercado", value=False, key="ya_chk_research")

        st.write("")
        with st.container(border=True):
            st.markdown("**🤖 La IA generara:**")
            n_tareas = 3 + sum([web, crm, social, contabilidad, research])
            st.markdown(f"• {n_tareas} tareas adaptadas a tu sector")
            n_agentes = 2 + sum([web, crm, social, contabilidad])
            st.markdown(f"• {n_agentes} agentes IA segun tus modulos")
            if st.session_state.get("ya_url_web"):
                st.markdown(f"• Enlace a tu web: `{st.session_state.get('ya_url_web')}`")

        st.write("")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(" Atras", use_container_width=True, key="ya_back_3"):
                st.session_state.ya_paso = 2
                st.rerun()
        with col2:
            if st.button("🚀 ADAPTAR MI NEGOCIO", use_container_width=True, type="primary", key="ya_crear"):
                st.session_state.ya_modulos = {
                    "web": web, "kanban": kanban, "crm": crm,
                    "social": social, "contabilidad": contabilidad, "research": research
                }
                crear_negocio_ya_tengo()
                st.rerun()


def crear_negocio_desde_cero():
    from panels import panel_base

    panel_base.inicializar_session_state()

    nombre = st.session_state.get("cero_nombre", "Mi Negocio")
    sector = st.session_state.get("cero_sector", "General")
    publico = st.session_state.get("cero_publico", "Clientes")
    modulos = st.session_state.get("cero_modulos", {})

    descripcion = f"{sector} para {publico}."

    datos_extra = {
        "sector": sector,
        "modulos": modulos,
    }

    # Icono VACIO (no forzar emoji)
    panel_base.crear_negocio(nombre, "", descripcion, tipo="desde_cero", datos_extra=datos_extra)

    st.session_state.onboarding_completado = True
    st.session_state.onboarding_paso = "elegir"

    for key in ["cero_nombre", "cero_sector", "cero_publico", "cero_paso",
                "cero_chk_web", "cero_chk_kanban", "cero_chk_crm",
                "cero_chk_social", "cero_chk_contab", "cero_chk_research", "cero_modulos"]:
        if key in st.session_state:
            del st.session_state[key]

    st.balloons()


def crear_negocio_ya_tengo():
    from panels import panel_base

    panel_base.inicializar_session_state()

    nombre = st.session_state.get("ya_nombre", "Mi Negocio")
    sector = st.session_state.get("ya_sector", "General")
    descripcion = st.session_state.get("ya_descripcion", "") or f"{sector}"
    url_web = st.session_state.get("ya_url_web", "")
    modulos = st.session_state.get("ya_modulos", {})

    datos_extra = {
        "sector": sector,
        "url_web": url_web,
        "modulos": modulos,
    }

    # Icono VACIO
    panel_base.crear_negocio(nombre, "", descripcion, tipo="ya_tengo", datos_extra=datos_extra)

    st.session_state.onboarding_completado = True
    st.session_state.onboarding_paso = "elegir"

    for key in ["ya_nombre", "ya_sector", "ya_descripcion", "ya_url_web", "ya_paso",
                "ya_chk_web", "ya_chk_kanban", "ya_chk_crm",
                "ya_chk_social", "ya_chk_contab", "ya_chk_research", "ya_modulos"]:
        if key in st.session_state:
            del st.session_state[key]

    st.balloons()