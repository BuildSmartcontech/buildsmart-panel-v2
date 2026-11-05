# panels/dueno/tab_arm.py
# ============================================
# TAB ARM - Consumo de Tokens y Mensajes Meta
# ============================================

import streamlit as st
from panels.dueno import comun as C

def renderizar(sb, inicio, fin):
    st.markdown(f"### 🤖 ARM - Automated Relationship Manager")
    st.info("Este panel muestra el consumo del plan **Premium Plus**.")
    
    # FIX: Inicializar logs ANTES del try para evitar UnboundLocalError
    logs = []
    
    try:
        # Consultar logs de arm en Supabase
        logs = sb.table("arm_logs").select("*").gte("created_at", inicio).lte("created_at", fin).execute().data or []
        tokens_totales = sum(l.get("tokens_usados", 0) for l in logs)
        mensajes_meta = len([l for l in logs if l.get("tipo") == "whatsapp"])
        leads_odoo = len([l for l in logs if l.get("tipo") == "odoo"])
    except Exception as e:
        print(f"[ARM TAB ERROR] {e}")
        tokens_totales = 0
        mensajes_meta = 0
        leads_odoo = 0

    c1, c2, c3 = st.columns(3)
    C._kpi(c1, "Tokens IA Consumidos", f"{tokens_totales:,}")
    C._kpi(c2, "Mensajes WhatsApp", mensajes_meta)
    C._kpi(c3, "Leads en Odoo", leads_odoo)
    
    st.divider()
    st.markdown("#### Últimos Leads Capturados por ARM")
    
    if not logs:
        st.caption("No hay actividad en el rango seleccionado.")
    else:
        for log in logs[:5]:
            st.text(f"[{log.get('created_at', '')[:10]}] {log.get('telefono')} - {log.get('resumen', 'Sin resumen')}")