# panels/web/panel_cliente.py
# ============================================
# MINI-PANEL DEL CLIENTE - Web Gancho SAMU IA
# ============================================
# V3.8: Recuperacion persistente de vista previa desde Supabase.
# ============================================

import streamlit as st
import datetime
import streamlit.components.v1 as components
from panels.web import landing_data as D

# ... (definición de constantes y EMOJIS se mantienen igual) ...

def _recuperar_html_desde_bd(sb, pedido):
    """
    Función centralizada para recuperar el HTML desde Supabase.
    """
    web_id = pedido.get("web_id")
    email = pedido.get("email", "usuario_web")
    
    if not web_id:
        return None, "No hay web_id en este pedido."

    try:
        from utils.web_storage import leer_web
        # Forzamos la lectura desde la fuente persistente (Supabase/Storage)
        resultado = leer_web(email, web_id)
        if resultado.get("exito"):
            return resultado.get("html"), None
        else:
            return None, f"Error en storage: {resultado.get('error')}"
    except Exception as e:
        return None, f"Excepción al leer: {str(e)}"

def _renderizar_panel(pedido, sb):
    # ... (código de cabecera y métricas se mantienen igual) ...

    st.markdown(f"### {E_GLOBO} Tu web")

    # --- CASO 1: LA WEB AÚN NO SE HA CREADO ---
    if not pedido.get("web_id") and not pedido.get("web_url"):
        # ... (lógica de generación inicial se mantiene igual) ...
        pass

    # --- CASO 2: LA WEB YA EXISTE ---
    else:
        # 1. Intentar recuperar de la memoria de sesión
        if "preview_html" not in st.session_state or not st.session_state["preview_html"]:
            # 2. Si la memoria está vacía, recuperar de la Base de Datos (Supabase)
            with st.spinner("Recuperando vista previa desde la base de datos..."):
                html_recuperado, error = _recuperar_html_desde_bd(sb, pedido)
                if html_recuperado:
                    st.session_state["preview_html"] = html_recuperado
                else:
                    st.warning(f"No se pudo recuperar automáticamente. {error}")

        # 3. Mostrar la vista previa (ya sea de memoria o de la BD)
        if "preview_html" in st.session_state and st.session_state["preview_html"]:
            st.divider()
            st.markdown("**Revisa cómo quedó tu web:**")
            _renderizar_vista_previa(st.session_state["preview_html"])

            st.write("")
            st.markdown("**Si todo está bien, publícala:**")
            if st.button(f"{E_COHETE} Publicar en Vivo", type="primary", use_container_width=True):
                # ... (lógica de publicación se mantiene igual) ...
                pass
        else:
            st.error("No se pudo cargar la vista previa. Es posible que el borrador se haya perdido y necesites generar una nueva web. El botón de abajo intentará recuperarla desde el último guardado en la base de datos.")
            if st.button("🔄 Reintentar Recuperación desde Base de Datos"):
                html_recuperado, error = _recuperar_html_desde_bd(sb, pedido)
                if html_recuperado:
                    st.session_state["preview_html"] = html_recuperado
                    st.rerun()
                else:
                    st.error(f"Error persistente: {error}")

    # ... (el resto del código: formulario de cambios, leads, detalles se mantienen igual) ...