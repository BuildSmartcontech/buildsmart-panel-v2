# panels/web/__init__.py
# ============================================
# MODULO WEB GANCHO - SAMU IA
# ============================================

from panels.web import landing_v2 as landing
from panels.web import checkout
from panels.web import panel_cliente

__version__ = "3.1"

def renderizar():
    """Punto de entrada del modulo WEB."""
    import streamlit as st

    sub_ruta = None
    try:
        params = st.query_params
        if "web" in params:
            valor = params.get("web", "")
            if isinstance(valor, list):
                valor = valor[0] if valor else ""
            sub_ruta = str(valor).strip() or "landing"
    except Exception:
        pass

    if not sub_ruta:
        sub_ruta = st.session_state.get("_web_subruta", "landing")

    # 1. Panel del cliente
    if sub_ruta == "panel":
        panel_cliente.renderizar()
        return

    # 2. Checkout (si hay tier seleccionado o pedido creado)
    if st.session_state.get("_web_checkout_tier") or st.session_state.get("_web_pedido_creado"):
        checkout.renderizar()
        return

    # 3. Sub-ruta explicita
    if sub_ruta == "checkout":
        checkout.renderizar()
    elif sub_ruta == "landing":
        landing.renderizar()
    else:
        landing.renderizar()