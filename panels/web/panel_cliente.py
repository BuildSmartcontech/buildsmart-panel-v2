# panels/web/panel_cliente.py
# ============================================
# MINI-PANEL DEL CLIENTE - Web Gancho SAMU IA
# ============================================
# V4.2: clear_on_submit para limpiar la caja de texto después de enviar.
# ============================================

import streamlit as st
import datetime
import streamlit.components.v1 as components
from panels.web import landing_data as D

# ... (constantes E_OK, etc. y otras funciones se mantienen igual) ...

def _renderizar_panel(pedido, sb):
    # ... (código de cabecera se mantiene igual) ...

    # --- SECCION DE MODIFICACION ---
    if restantes > 0:
        st.info(f"Tienes **{restantes}** modificaciones disponibles.")
        
        # AQUI ESTA EL FIX DE LA CAJA DE TEXTO
        with st.form("form_modificacion", clear_on_submit=True):
            instruccion = st.text_area("Escribe lo que quieres cambiar aquí:", placeholder="Ej: Cambia el título principal a 'Prueba'.", height=100)
            btn_mod = st.form_submit_button(f"{E_COHETE} Generar Vista Previa", type="primary", use_container_width=True)
            
            if btn_mod:
                if not instruccion.strip():
                    st.warning("Escribe lo que quieres cambiar antes de generar la vista previa.")
                else:
                    with st.spinner("La IA esta aplicando los cambios..."):
                        exito, msg, html_nuevo = _solicitar_modificacion(sb, pedido, instruccion)
                    if exito:
                        st.session_state["preview_html"] = html_nuevo
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
    else:
        # ... (lógica de compra de cambios se mantiene igual) ...

    # ... (el resto del código se mantiene igual) ...