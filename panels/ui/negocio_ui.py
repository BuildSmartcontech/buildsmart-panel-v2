# panels/ui/negocio_ui.py
# ============================================
# UI: SELECCION DE NEGOCIOS
# ============================================

import streamlit as st


def renderizar_seleccion_negocio():
    """Renderiza la seleccion de negocios (cards)."""
    st.subheader("📋 Tus Negocios")

    if st.session_state.negocios:
        cols = st.columns(min(len(st.session_state.negocios), 4))
        for idx, (key, negocio) in enumerate(st.session_state.negocios.items()):
            with cols[idx % 4]:
                selected = st.session_state.negocio_seleccionado == key
                border_color = negocio["color"] if selected else "#e0e0e0"
                bg_color = "#f0f4ff" if selected else "white"

                creditos_html = ""
                if hasattr(st.session_state, 'MOSTRAR_CREDITOS') and st.session_state.MOSTRAR_CREDITOS:
                    creditos = negocio.get("creditos", 0)
                    creditos_html = f'<span>💳 {creditos}</span>'

                icono_str = negocio.get("icono", "") or ""
                icono_html = f'<span style="font-size: 2rem;">{icono_str}</span>' if icono_str else ""

                html_card = (
                    f'<div class="business-card" style="border-color: {border_color}; background: {bg_color};">'
                    f'<div style="display: flex; justify-content: space-between; align-items: center;">'
                    f'<div>'
                    f'{icono_html}'
                    f'<h4 style="margin: 0; color: {negocio["color"]};">{negocio["nombre"]}</h4>'
                    f'<small style="color: #888;">{negocio["descripcion"][:40]}...</small>'
                    f'</div>'
                    f'<div><span style="font-size: 0.8rem;">{"✅" if selected else "🔘"}</span></div>'
                    f'</div>'
                    f'<div style="display: flex; gap: 0.5rem; margin-top: 0.5rem; font-size: 0.7rem;">'
                    f'<span>📋 {negocio["metricas"]["Proyectos"]}</span>'
                    f'<span>👥 {negocio["metricas"]["Clientes"]}</span>'
                    f'<span>💰 {negocio["metricas"]["Ingresos"]}</span>'
                    f'{creditos_html}'
                    f'</div>'
                    f'</div>'
                )
                st.markdown(html_card, unsafe_allow_html=True)

                if st.button(f"Seleccionar", key=f"select_{key}", use_container_width=True):
                    st.session_state.negocio_seleccionado = key
                    st.rerun()
    else:
        st.info("👈 Crea tu primer negocio usando el boton '➕ CREAR NEGOCIO' en el panel lateral.")

    st.divider()