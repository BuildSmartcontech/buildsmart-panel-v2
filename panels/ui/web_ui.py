# panels/ui/web_ui.py
# ============================================
# UI: GESTION DE WEB Y CONFIG ASISTENTE
# ============================================

import streamlit as st


def renderizar_gestion_web(negocio):
    """Renderiza la gestion de web (generar, modificar, vincular)."""
    negocio_id = negocio["id"]
    tiene_web_generada = bool(negocio['sitio_web'].get('archivo_generado'))
    web_vinculada = negocio['sitio_web'].get('vinculada', False)
    es_ya_tengo = negocio.get('tipo') == 'ya_tengo'
    mods_usadas = negocio.get("modificaciones_usadas", 0)
    
    # Obtener MODIFICACIONES_GRATIS de session_state o default
    MODIFICACIONES_GRATIS = getattr(st.session_state, 'MODIFICACIONES_GRATIS', 7)
    COSTO_MODIFICACION_EXTRA = getattr(st.session_state, 'COSTO_MODIFICACION_EXTRA', 5)
    WEB_DISPONIBLE = getattr(st.session_state, 'WEB_DISPONIBLE', False)
    
    mods_restantes = max(0, MODIFICACIONES_GRATIS - mods_usadas)

    if not tiene_web_generada and not web_vinculada:
        st.info("🌐 Aun no tienes web. Genera una con IA o vincula la tuya existente.")

        col_a, col_b = st.columns(2)

        with col_a:
            if WEB_DISPONIBLE:
                if st.button("🚀 GENERAR MI WEB CON IA", use_container_width=True, type="primary", key=f"gen_{negocio_id}"):
                    with st.spinner("🧠 Generando web con IA... (30-60s)"):
                        # Llamar a la funcion de web_service
                        from panels.services.web_service import generar_sitio_web_con_ia
                        resultado, msg = generar_sitio_web_con_ia(negocio_id)
                        if resultado:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
            else:
                st.warning("⚠️ Modulo web no disponible")

        with col_b:
            if es_ya_tengo:
                with st.expander("🔗 Vincular mi web existente", expanded=False):
                    url_input = st.text_input("URL de tu web", placeholder="https://tu-web.com", key=f"url_{negocio_id}")
                    if st.button("Vincular", use_container_width=True, key=f"vinc_{negocio_id}"):
                        if url_input:
                            from panels.services.web_service import vincular_web_existente
                            ok, msg = vincular_web_existente(negocio_id, url_input)
                            if ok:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                        else:
                            st.warning("⚠️ Ingresa una URL")

    elif web_vinculada and not tiene_web_generada:
        st.success(f"🔗 Web vinculada: {negocio['sitio_web']['url']}")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"[🌐 Abrir mi web]({negocio['sitio_web']['url']})")
        with col_b:
            if st.button("🔄 Cambiar URL", use_container_width=True, key=f"cambiar_url_{negocio_id}"):
                st.session_state[f"editando_url_{negocio_id}"] = True

        if st.session_state.get(f"editando_url_{negocio_id}", False):
            with st.form(f"form_url_{negocio_id}"):
                nueva_url = st.text_input("Nueva URL", value=negocio['sitio_web']['url'], key=f"nueva_url_{negocio_id}")
                col_ok, col_cancel = st.columns(2)
                with col_ok:
                    if st.form_submit_button("Actualizar", use_container_width=True):
                        from panels.services.web_service import vincular_web_existente
                        ok, msg = vincular_web_existente(negocio_id, nueva_url)
                        if ok:
                            st.session_state[f"editando_url_{negocio_id}"] = False
                            st.success(msg)
                            st.rerun()
                with col_cancel:
                    if st.form_submit_button("Cancelar", use_container_width=True):
                        st.session_state[f"editando_url_{negocio_id}"] = False
                        st.rerun()

    else:
        web_id = negocio['sitio_web'].get('archivo_generado')
        url_publica = negocio['sitio_web'].get('url_publica', '')

        st.success(f"✅ Web generada")

        if url_publica:
            st.markdown(f"**🌎 URL publica:** [{url_publica}]({url_publica})")
            st.caption("Comparte esta URL con tus clientes. Funciona desde cualquier dispositivo.")

        if mods_restantes > 0:
            st.info(f"✏️ **Modificaciones gratis disponibles:** {mods_restantes}/{MODIFICACIONES_GRATIS}")
        else:
            st.warning(
                f"⚠️ **Has agotado las {MODIFICACIONES_GRATIS} modificaciones gratis.**\n\n"
                f"Cada modificacion adicional tendra un costo de **${COSTO_MODIFICACION_EXTRA} USD**.\n\n"
                f"_(En modo prueba no se cobra, pero se registra)_"
            )

        if st.button("✏️ MODIFICAR MI WEB", use_container_width=True, type="primary", key=f"mod_{negocio_id}"):
            st.session_state.modal_modificar_web = True

        if st.session_state.get("modal_modificar_web", False):
            with st.form(f"form_mod_{negocio_id}"):
                st.markdown("#### ✏️ ¿Que quieres cambiar?")
                st.caption("Los cambios se publican automaticamente en tu URL publica.")
                instruccion = st.text_area(
                    "Describe tu cambio (en tus palabras, cualquier dialecto)",
                    placeholder="Ej: Ponle fotos de dulces a los cuadros vacios y cambia el titulo a rojo",
                    height=100,
                    key=f"instruc_{negocio_id}"
                )

                aviso = ""
                if mods_restantes > 0:
                    aviso = f"Te quedan {mods_restantes} modificaciones gratis."
                else:
                    aviso = f"⚠️ Esta modificacion tendra un costo de ${COSTO_MODIFICACION_EXTRA} USD."

                st.caption(aviso)

                col_ok, col_cancel = st.columns(2)
                with col_ok:
                    if st.form_submit_button("🚀 Aplicar cambio", use_container_width=True):
                        if instruccion.strip():
                            with st.spinner("✏️ Modificando y republicando tu web..."):
                                from panels.services.web_service import modificar_web_con_ia
                                ok, msg = modificar_web_con_ia(negocio_id, instruccion.strip())
                                if ok:
                                    st.session_state.modal_modificar_web = False
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)
                        else:
                            st.warning("⚠️ Escribe que quieres cambiar")
                with col_cancel:
                    if st.form_submit_button("❌ Cancelar", use_container_width=True):
                        st.session_state.modal_modificar_web = False
                        st.rerun()


def renderizar_config_asistente(negocio):
    """Renderiza la configuracion del asistente (personalidad IA)."""
    import datetime
    
    negocio_id = negocio["id"]
    personalidad_actual = negocio.get("custom_personality", "")

    with st.expander("⚙️ **CONFIGURAR MI ASISTENTE** (Personalidad IA)", expanded=False):
        st.markdown("### 🎭 Personalidad del Asistente")

        if personalidad_actual:
            st.success("✅ Tienes una personalidad personalizada activa")
        else:
            st.info("ℹ️ Usando personalidad por defecto. Puedes personalizarla aqui.")

        st.markdown("""
**¿Que puedes hacer aqui?**

Puedes definir como quieres que tu asistente IA se comporte. Por ejemplo:
- *"Eres SAMU IA, actua como Director de Operaciones..."*
- *"Eres un consultor experto en marketing digital..."*
- *"Habla en tono formal y profesional..."*

El asistente usara estas instrucciones en **todas las consultas** que le hagas.
        """)

        with st.form(f"form_personalidad_{negocio_id}"):
            nuevo_prompt = st.text_area(
                "Personalidad del asistente",
                value=personalidad_actual,
                placeholder="Ejemplo: Eres SAMU IA, el asistente virtual nativo de BuildSmart. Tu objetivo es actuar como Director de Operaciones y Consultor de Crecimiento...",
                height=400,
                key=f"personalidad_{negocio_id}"
            )

            st.caption(f"📏 Longitud: {len(nuevo_prompt)} caracteres")

            col_ok, col_clear, col_cancel = st.columns(3)

            with col_ok:
                if st.form_submit_button("💾 Guardar", use_container_width=True, type="primary"):
                    if nuevo_prompt.strip():
                        from panels.services.web_service import configurar_asistente
                        ok, msg = configurar_asistente(negocio_id, nuevo_prompt.strip())
                        if ok:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.warning("⚠️ El prompt no puede estar vacio")

            with col_clear:
                if st.form_submit_button("🗑️ Restablecer", use_container_width=True):
                    negocio["custom_personality"] = ""
                    negocio['timeline'].append({
                        "accion": "⚙️ Personalidad restablecida al default",
                        "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "tipo": "info"
                    })
                    st.success("✅ Personalidad restablecida")
                    st.rerun()

            with col_cancel:
                if st.form_submit_button("❌ Cancelar", use_container_width=True):
                    st.session_state.modal_config_asistente = False
                    st.rerun()

        if personalidad_actual:
            st.divider()
            st.markdown("**Vista previa actual:**")
            st.code(personalidad_actual[:500] + ("..." if len(personalidad_actual) > 500 else ""), language="text")