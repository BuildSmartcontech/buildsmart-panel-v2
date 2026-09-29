# panels/dueno/tab_panel.py
# ============================================
# TAB PANEL - Metricas globales y graficos
# ============================================

import streamlit as st
import datetime
from panels.dueno import comun as C
from config_app import VERSION


def renderizar(sb, inicio, fin):
    st.markdown(f"### {C.E_PANEL} Metricas globales")

    try:
        data_neg = sb.table("negocios").select("*").execute().data or []
    except Exception as e:
        st.warning(f"No se pudo leer 'negocios': {e}")
        data_neg = []

    try:
        eventos_todos = sb.table("eventos_app").select("*").execute().data or []
    except Exception:
        eventos_todos = []

    try:
        suscripciones_todas = sb.table("suscripciones").select("*").execute().data or []
    except Exception:
        suscripciones_todas = []

    negocios_todos = [C._plano(n) for n in data_neg]
    negocios = [n for n in negocios_todos if C._dentro_de_rango(n, "created_at", inicio, fin)]
    eventos = [e for e in eventos_todos if C._dentro_de_rango(e, "created_at", inicio, fin)]
    suscripciones = [s for s in suscripciones_todas if C._dentro_de_rango(s, "created_at", inicio, fin)]

    total_negocios = len(negocios)
    usuarios_unicos = len(set(n.get("usuario_id") for n in negocios if n.get("usuario_id")))
    total_webs = sum(1 for n in negocios if (n.get("sitio_web") or {}).get("archivo_generado") or n.get("web_url"))
    total_eventos = len(eventos)
    activos_hoy = len(set(
        e.get("usuario_id") for e in eventos
        if str(e.get("created_at", "")).startswith(str(datetime.date.today()))
    ))
    suscripciones_activas = sum(1 for s in suscripciones if s.get("estado") == "activo")

    estados = C._obtener_estados_usuarios(sb)
    suspendidos = sum(1 for uid, info in estados.items() if info.get("estado") == "suspendido")

    c1, c2, c3, c4 = st.columns(4)
    C._kpi(c1, f"{C.E_CLIENTES} Usuarios", usuarios_unicos)
    C._kpi(c2, f"{C.E_CORONA} Negocios", total_negocios)
    C._kpi(c3, f"{C.E_GLOBO} Webs", total_webs)
    C._kpi(c4, f"{C.E_LIBRO} Eventos", total_eventos)

    c5, c6, c7, c8 = st.columns(4)
    C._kpi(c5, f"{C.E_RAYO} Activos hoy", activos_hoy)
    C._kpi(c6, f"{C.E_TARJETA} Suscripciones", suscripciones_activas)
    C._kpi(c7, f"{C.E_PROHIBIDO} Suspendidos", suspendidos)
    C._kpi(c8, f"{C.E_PIN} Version", VERSION)

    st.divider()
    st.markdown(f"#### {C.E_GRAFICO} Graficos")

    try:
        from utils import graficos as g
    except Exception as e:
        st.warning(f"No se pudieron cargar los graficos: {e}")
        return

    col_a, col_b = st.columns(2)
    with col_a:
        try:
            g.render_plotly(st, g.eventos_por_dia(eventos, dias=30))
        except Exception as e:
            st.caption(f"Sin datos de eventos: {e}")
    with col_b:
        try:
            g.render_plotly(st, g.usuarios_nuevos_por_dia(negocios, dias=30))
        except Exception as e:
            st.caption(f"Sin datos de usuarios: {e}")

    col_c, col_d = st.columns(2)
    with col_c:
        try:
            fig = g.negocios_por_sector(negocios)
            if fig:
                g.render_plotly(st, fig)
            else:
                st.info("Aun no hay negocios para mostrar por sector.")
        except Exception as e:
            st.caption(f"Sin datos de sectores: {e}")
    with col_d:
        try:
            g.render_plotly(st, g.webs_por_semana(negocios, semanas=8))
        except Exception as e:
            st.caption(f"Sin datos de webs: {e}")

    st.divider()
    st.markdown(f"#### {C.E_RELOJ} Ultimos eventos")
    if eventos:
        ultimos = sorted(eventos, key=lambda x: x.get("created_at", ""), reverse=True)[:10]
        for e in ultimos:
            fecha = str(e.get("created_at", ""))[:19].replace("T", " ")
            st.text(f"[{fecha}] {e.get('tipo', '?')} - {str(e.get('usuario_id', '?'))[:8]}")
    else:
        st.info(f"{C.E_AVISO} No hay eventos en el rango seleccionado.")