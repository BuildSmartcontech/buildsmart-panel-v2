# panels/web/__init__.py
# ============================================
# MODULO WEB GANCHO - SAMU IA
# ============================================
# Router del modulo WEB (producto de pago unico).
#
# Sub-rutas (via query params ?web=xxx):
#   landing  -> Landing con 3 tiers ($149/$299/$499) [V2 DARK]
#   checkout -> Formulario + instrucciones de pago
#   panel    -> Mini-panel del cliente (requiere ?token=xxx)
#
# V3.1: Actualizado para usar landing_v2 (Dark Premium)
# V3.0: Agrega sub-ruta panel (cliente)
# ============================================

from panels.web import landing_v2 as landing
from panels.web import checkout
from panels.web import panel_cliente

__version__ = "3.1"


def renderizar():
    """
    Punto de entrada del modulo WEB.
    Detecta la sub-ruta actual y renderiza la seccion.
    """
    import streamlit as st

    # Sub-ruta via query param ?web=xxx
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

    # Fallback a session_state (compatibilidad)
    if not sub_ruta:
        sub_ruta = st.session_state.get("_web_subruta", "landing")

    # ==========================================
    # ROUTING
    # ==========================================
    # 1. Panel del cliente (prioridad alta: si hay token)
    if sub_ruta == "panel":
        panel_cliente.renderizar()
        return

    # 2. Checkout (si hay tier seleccionado o pedido creado)
    if st.session_state.get("_web_checkout_tier"):
        checkout.renderizar()
        return

    if st.session_state.get("_web_pedido_creado"):
        checkout.renderizar()
        return

    # 3. Sub-ruta explicita
    if sub_ruta == "checkout":
        checkout.renderizar()
    elif sub_ruta == "landing":
        landing.renderizar()
    else:
        # Fallback a landing
        landing.renderizar()


# ============================================
# TEST MANUAL
# ============================================
if __name__ == "__main__":
    print(f"Modulo web v{__version__}")
    print("Sub-rutas soportadas: landing, checkout, panel")