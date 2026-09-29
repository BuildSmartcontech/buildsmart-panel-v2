# panels/dueno/tab_auditoria.py
# ============================================
# TAB AUDITORIA - Historial de cambios en config
# ============================================
# Muestra quien cambio que config y cuando.
# Vista tipo timeline con diff antes/despues.
# ============================================

import streamlit as st
import datetime
import json
from panels.dueno import comun as C


def _fmt_valor(v):
    """Formatea un valor JSONB para mostrar."""
    if v is None:
        return "_vacio_"
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return f'"{v}"' if len(v) < 100 else f'"{v[:100]}..."'
    try:
        s = json.dumps(v, ensure_ascii=False)
        return s if len(s) < 100 else s[:100] + "..."
    except Exception:
        return str(v)


def renderizar(sb, inicio, fin):
    st.markdown(f"### {C.E_LIBRO} Auditoria de cambios")
    st.caption("Historial completo de cambios en la configuracion global.")

    # Cargar auditoria
    try:
        auditorias_todas = sb.table("config_auditoria").select("*").order("created_at", desc=True).limit(500).execute().data or []
    except Exception as e:
        st.warning(f"Tabla 'config_auditoria' no lista: {e}")
        st.info("Ejecuta el SQL de auditoria en Supabase (bloque 1 del modulo M10).")
        return

    # Filtrar por rango
    auditorias = [a for a in auditorias_todas if C._dentro_de_rango(a, "created_at", inicio, fin)]

    # ==========================================
    # KPIs
    # ==========================================
    total = len(auditorias)
    claves_unicas = len(set(a.get("clave") for a in auditorias if a.get("clave")))
    quien_unicos = len(set(a.get("quien") for a in auditorias if a.get("quien")))

    # Cambio mas reciente
    ultima = ""
    if auditorias:
        ultima = str(auditorias[0].get("created_at", ""))[:19].replace("T", " ")

    c1, c2, c3, c4 = st.columns(4)
    C._kpi(c1, f"{C.E_LIBRO} Cambios", total)
    C._kpi(c2, f"{C.E_ENGANCHE} Claves", claves_unicas)
    C._kpi(c3, f"{C.E_USUARIO} Autores", quien_unicos)
    C._kpi(c4, f"{C.E_RELOJ} Ultimo", ultima[:10] if ultima else "-")

    st.divider()

    if not auditorias:
        st.info(f"{C.E_AVISO} Sin cambios registrados en el rango seleccionado.")
        return

    # ==========================================
    # Filtros
    # ==========================================
    col_f1, col_f2 = st.columns([2, 2])
    with col_f1:
        claves = sorted(set(a.get("clave") for a in auditorias if a.get("clave")))
        filtro_clave = st.selectbox("Filtrar por clave", ["(todas)"] + claves, key="aud_clave")
    with col_f2:
        quien_list = sorted(set(a.get("quien") for a in auditorias if a.get("quien")))
        filtro_quien = st.selectbox("Filtrar por autor", ["(todos)"] + quien_list, key="aud_quien")

    # Aplicar filtros
    filtradas = []
    for a in auditorias:
        if filtro_clave != "(todas)" and a.get("clave") != filtro_clave:
            continue
        if filtro_quien != "(todos)" and a.get("quien") != filtro_quien:
            continue
        filtradas.append(a)

    st.caption(f"Mostrando {len(filtradas)} de {total} cambios")
    st.divider()

    # ==========================================
    # Timeline de cambios
    # ==========================================
    if not filtradas:
        st.info(f"{C.E_AVISO} Ningun cambio coincide con los filtros.")
        return

    for a in filtradas:
        fecha = str(a.get("created_at", ""))[:19].replace("T", " ")
        clave = a.get("clave", "?")
        v_ant = a.get("valor_anterior")
        v_new = a.get("valor_nuevo")
        quien = a.get("quien", "?")
        motivo = a.get("motivo", "")

        with st.container(border=True):
            col_info, col_quien = st.columns([4, 2])

            with col_info:
                st.markdown(f"**{C.E_ENGANCHE} `{clave}`**")
                st.caption(f"{C.E_RELOJ} {fecha}")

            with col_quien:
                st.caption(f"{C.E_USUARIO} Por: **{quien}**")
                if motivo:
                    st.caption(f"{C.E_LIBRO} {motivo}")

            # Diff
            st.markdown("**Cambio:**")
            col_ant, col_arrow, col_new = st.columns([4, 1, 4])
            with col_ant:
                st.markdown(f"<div style='background:#3f1f1f;padding:8px;border-radius:6px;color:#fca5a5;font-family:monospace;'>{_fmt_valor(v_ant)}</div>", unsafe_allow_html=True)
            with col_arrow:
                st.markdown("<div style='text-align:center;font-size:24px;padding-top:8px;'>→</div>", unsafe_allow_html=True)
            with col_new:
                st.markdown(f"<div style='background:#1f3f2f;padding:8px;border-radius:6px;color:#86efac;font-family:monospace;'>{_fmt_valor(v_new)}</div>", unsafe_allow_html=True)

    st.divider()
    st.caption("Los cambios se ordenan del mas reciente al mas antiguo.")