# panels/web/checkout.py (Fragmento de la función _renderizar_instrucciones)
# REEMPLAZA SOLO ESTA FUNCION EN TU ARCHIVO ACTUAL

def _renderizar_instrucciones():
    datos = st.session_state.get("_web_pedido_creado", {})
    pedido = datos.get("pedido") or {}
    tier = datos.get("tier") or {}
    if not pedido or not tier:
        st.error("Datos del pedido no encontrados.")
        if st.button("Volver al inicio"): limpiar_estado_checkout()
        return
    st.markdown(f"# {E_OK} Pedido registrado")
    st.markdown(f"**Pedido ID:** `{pedido.get('id', '?')}`")
    st.markdown(f"**Plan:** {tier['nombre']} - {tier['precio_label']}")
    st.divider()
    
    # --- NUEVA LOGICA DE PAGO ---
    url_pago = pedido.get("url_pago")
    instrucciones = pedido.get("instrucciones_pago")

    if url_pago:
        st.markdown(f"## {E_DINERO} Como pagar")
        st.success("Tu pedido está listo. Haz clic en el botón de abajo para ir a la pasarela de pago segura.")
        st.markdown(f'<a href="{url_pago}" target="_blank"><button style="background-color:#14B8A6; color:black; padding:15px 30px; border:none; border-radius:5px; font-weight:bold; font-size:18px; cursor:pointer; width:100%;">Pagar ahora con ePayco</button></a>', unsafe_allow_html=True)
        st.divider()
    elif instrucciones:
        st.markdown(f"## {E_DINERO} Como pagar")
        st.info(instrucciones)
        st.divider()
    else:
        st.info("El proveedor de pagos no esta configurado correctamente. Contacta a soporte.")
        
    st.markdown(f"## {E_RELOJ} Que sigue?")
    st.markdown("1. Realiza la transferencia o pago.\n2. Envia el comprobante.\n3. Confirmaremos en 24h.\n4. **Recibiras tu web y tu panel.**")
    token = pedido.get("magic_token", "")
    if token:
        st.divider()
        st.markdown(f"## {E_COHETE} Acceso a tu panel")
        try:
            from utils.magic_link import construir_url_panel
            url_panel = construir_url_panel(token)
            st.markdown(f"**Link:** [Abrir mi panel]({url_panel})")
            st.code(url_panel, language=None)
        except Exception: pass
    st.divider()
    st.success(f"{E_CORONA} Recibimos tu pedido. Guarda este ID: `{pedido.get('id', '?')}`")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"{E_DOC} Hacer otro pedido", width="stretch"): limpiar_estado_checkout()
    with col2:
        if st.button(f"{E_FLECHA} Volver al inicio", width="stretch"): limpiar_estado_checkout()