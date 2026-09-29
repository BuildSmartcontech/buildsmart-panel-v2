# panels/dueno/tab_ingresos.py
# ============================================
# TAB INGRESOS - MRR, churn, suscripciones
# ============================================

import streamlit as st
from panels.dueno import comun as C


def renderizar(sb, inicio, fin):
    st.markdown(f"### {C.E_DINERO} Ingresos y egresos")

    try:
        suscripciones_todas = sb.table("suscripciones").select("*").execute().data or []
    except Exception:
        suscripciones_todas = []

    suscripciones = [s for s in suscripciones_todas if C._dentro_de_rango(s, "created_at", inicio, fin)]

    if not suscripciones:
        st.info(f"{C.E_RAYO} No hay cobros en el rango seleccionado. Cuando integres Stripe, apareceran aqui.")
        st.markdown("""
        **Planes configurados (provisionales):**
        - WEB Gancho: **$199 pago unico** (+ $10/mes con CRM)
        - PIME: **$99/mes**
        - DESDE CERO: **$99/mes**
        - ENTERPRISE: **$299/mes** (proximamente)
        - Sucursal: **50% del plan**
        """)
        return

    activas = [s for s in suscripciones if s.get("estado") == "activo"]
    mrr = sum(float(s.get("monto", 0) or 0) for s in activas)
    total_historico = sum(float(s.get("monto", 0) or 0) for s in suscripciones)
    canceladas = sum(1 for s in suscripciones if s.get("estado") == "cancelado")
    churn = (canceladas / len(suscripciones) * 100) if suscripciones else 0

    c1, c2, c3, c4 = st.columns(4)
    C._kpi(c1, "MRR", f"${mrr:,.0f}")
    C._kpi(c2, "Total en rango", f"${total_historico:,.0f}")
    C._kpi(c3, f"{C.E_OK} Activas", len(activas))
    C._kpi(c4, "Churn", f"{churn:.1f}%")

    st.divider()
    st.markdown("#### Suscripciones en el rango")
    for s in suscripciones:
        st.text(f"[{s.get('plan','?')}] {s.get('estado','?')} - ${s.get('monto',0)} - {str(s.get('usuario_id','?'))[:12]}")