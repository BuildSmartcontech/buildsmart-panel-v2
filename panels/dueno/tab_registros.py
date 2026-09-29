# panels/dueno/tab_registros.py
# ============================================
# TAB REGISTROS - Visor de eventos_app
# ============================================
# V1.1: Timestamps en hora local (antes UTC)
# V1.0: Version inicial
# ============================================

import streamlit as st
import json
from panels.dueno import comun as C


def _fmt_fecha_local(iso_str):
    """Convierte timestamp ISO de Supabase (UTC) a hora local legible."""
    if not iso_str:
        return "?"
    dt = C._parse_fecha_segura(iso_str)
    if dt is None:
        return str(iso_str)[:19].replace("T", " ")
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def renderizar(sb, inicio, fin):
    st.markdown(f"### {C.E_LIBRO} Registros del sistema")
    st.caption(f"{C.E_RELOJ} Horarios en hora local.")

    try:
        eventos_todos = sb.table("eventos_app").select("*").order("created_at", desc=True).limit(500).execute().data or []
    except Exception as e:
        st.warning(f"Tabla 'eventos_app' no lista: {e}")
        return

    eventos = [e for e in eventos_todos if C._dentro_de_rango(e, "created_at", inicio, fin)]

    if not eventos:
        st.info(f"{C.E_AVISO} No hay eventos en el rango seleccionado.")
        return

    tipos = sorted(set(e.get("tipo", "?") for e in eventos))
    filtro = st.selectbox("Filtrar por tipo", ["(todos)"] + tipos)

    st.caption(f"Mostrando {len(eventos)} eventos en el rango")
    st.divider()

    for e in eventos:
        if filtro != "(todos)" and e.get("tipo") != filtro:
            continue
        fecha = _fmt_fecha_local(e.get("created_at"))
        uid = str(e.get("usuario_id", "?"))[:12]
        detalle = e.get("detalle")
        det_txt = f" - {json.dumps(detalle, ensure_ascii=False)[:80]}" if detalle else ""
        st.text(f"[{fecha}] {e.get('tipo','?'):20s} - {uid}{det_txt}")