# panels/dueno/tab_uso_ia.py
# ============================================
# TAB USO IA - Consumo por usuario
# ============================================
# Agrupa eventos_app por usuario para mostrar:
# - Llamadas al chat IA
# - Webs generadas
# - Modificaciones IA
# - Fuente IA mas usada
# ============================================

import streamlit as st
import datetime
from collections import Counter, defaultdict
from panels.dueno import comun as C


def _contar_por_usuario(eventos):
    """Agrupa eventos por usuario. Retorna dict {uid: {tipo: count, ...}}."""
    por_usuario = defaultdict(lambda: {
        "chat_ia": 0,
        "generar_web": 0,
        "modificar_web": 0,
        "crear_negocio": 0,
        "chat_intent": 0,
        "total": 0,
        "ultima_actividad": "",
        "fuentes": Counter(),
    })

    for e in eventos:
        uid = e.get("usuario_id")
        if not uid:
            continue
        tipo = e.get("tipo", "?")
        por_usuario[uid][tipo] = por_usuario[uid].get(tipo, 0) + 1
        por_usuario[uid]["total"] += 1

        fecha = str(e.get("created_at", ""))
        if fecha > por_usuario[uid]["ultima_actividad"]:
            por_usuario[uid]["ultima_actividad"] = fecha

        if tipo == "chat_ia":
            detalle = e.get("detalle") or {}
            fuente = detalle.get("fuente", "?")
            if fuente and fuente != "?":
                por_usuario[uid]["fuentes"][fuente] += 1

    return dict(por_usuario)


def _fuente_top(fuentes):
    """Devuelve la fuente IA mas usada."""
    if not fuentes:
        return "-"
    try:
        return fuentes.most_common(1)[0][0]
    except Exception:
        return "-"


def renderizar(sb, inicio, fin):
    st.markdown(f"### {C.E_RAYO} Uso IA por usuario")

    # Cargar eventos
    try:
        eventos_todos = sb.table("eventos_app").select("*").order("created_at", desc=True).limit(5000).execute().data or []
    except Exception as e:
        st.error(f"Error leyendo eventos: {e}")
        return

    # Filtrar por rango
    eventos = [e for e in eventos_todos if C._dentro_de_rango(e, "created_at", inicio, fin)]

    if not eventos:
        st.info(f"{C.E_AVISO} No hay actividad en el rango seleccionado.")
        return

    # Agrupar
    por_usuario = _contar_por_usuario(eventos)

    # Totales globales
    total_chat = sum(1 for e in eventos if e.get("tipo") == "chat_ia")
    total_webs = sum(1 for e in eventos if e.get("tipo") == "generar_web")
    total_mods = sum(1 for e in eventos if e.get("tipo") == "modificar_web")
    usuarios_activos = len([uid for uid, d in por_usuario.items() if d.get("chat_ia", 0) > 0])

    c1, c2, c3, c4 = st.columns(4)
    C._kpi(c1, f"{C.E_USUARIO} Usuarios activos IA", usuarios_activos)
    C._kpi(c2, f"{C.E_RAYO} Llamadas chat", total_chat)
    C._kpi(c3, f"{C.E_GLOBO} Webs generadas", total_webs)
    C._kpi(c4, f"{C.E_ENGANCHE} Modificaciones", total_mods)

    st.divider()

    # ==========================================
    # GRAFICO - Actividad IA por dia
    # ==========================================
    st.markdown(f"#### {C.E_GRAFICO} Actividad IA por dia")

    dias_data = defaultdict(lambda: {"chat_ia": 0, "generar_web": 0, "modificar_web": 0})
    for e in eventos:
        tipo = e.get("tipo", "?")
        if tipo not in ("chat_ia", "generar_web", "modificar_web"):
            continue
        f = C._parse_fecha_segura(e.get("created_at"))
        if not f:
            continue
        fecha = f.date()
        dias_data[fecha][tipo] += 1

    if dias_data:
        try:
            import plotly.graph_objects as go
            fechas = sorted(dias_data.keys())
            chat_vals = [dias_data[d]["chat_ia"] for d in fechas]
            web_vals = [dias_data[d]["generar_web"] for d in fechas]
            mod_vals = [dias_data[d]["modificar_web"] for d in fechas]

            fig = go.Figure()
            fig.add_trace(go.Bar(name="Chat IA", x=fechas, y=chat_vals, marker_color="#3b82f6"))
            fig.add_trace(go.Bar(name="Generar web", x=fechas, y=web_vals, marker_color="#10b981"))
            fig.add_trace(go.Bar(name="Modificar web", x=fechas, y=mod_vals, marker_color="#f59e0b"))

            fig.update_layout(
                barmode="stack",
                paper_bgcolor="#1e293b",
                plot_bgcolor="#1e293b",
                font=dict(family="Inter, sans-serif", size=12, color="#cbd5e1"),
                margin=dict(l=50, r=20, t=40, b=50),
                height=340,
                xaxis=dict(title="Fecha", gridcolor="rgba(255,255,255,0.06)", linecolor="#334155"),
                yaxis=dict(title="Llamadas", gridcolor="rgba(255,255,255,0.06)", linecolor="#334155"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                hoverlabel=dict(bgcolor="#1e293b", bordercolor="#334155",
                                font=dict(color="#f1f5f9", size=12)),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        except Exception as e:
            st.caption(f"No se pudo renderizar el grafico: {e}")
    else:
        st.info("Sin actividad IA en el rango.")

    st.divider()

    # ==========================================
    # TABLA POR USUARIO
    # ==========================================
    st.markdown(f"#### {C.E_CLIENTES} Consumo por usuario")

    if not por_usuario:
        st.info("Sin usuarios con actividad.")
        return

    # Ordenar por total descendente
    ordenados = sorted(por_usuario.items(), key=lambda kv: kv[1].get("total", 0), reverse=True)

    for uid, datos in ordenados:
        chat = datos.get("chat_ia", 0)
        webs = datos.get("generar_web", 0)
        mods = datos.get("modificar_web", 0)
        total = datos.get("total", 0)
        fuente_top = _fuente_top(datos.get("fuentes", {}))
        ultima = datos.get("ultima_actividad", "")[:19].replace("T", " ")

        with st.container(border=True):
            col_a, col_b, col_c = st.columns([3, 4, 2])
            with col_a:
                st.markdown(f"**{C.E_USUARIO} `{str(uid)[:12]}...`**")
                st.caption(f"Ultima actividad: {ultima or '-'}")
            with col_b:
                m1, m2, m3, m4 = st.columns(4)
                with m1: st.metric("Chat IA", chat)
                with m2: st.metric("Webs", webs)
                with m3: st.metric("Mods", mods)
                with m4: st.metric("Total", total)
            with col_c:
                st.caption(f"Fuente top: **{fuente_top}**")
                if st.button(f"{C.E_OJO} Ver cliente", key=f"uso_ver_{uid}", use_container_width=True):
                    st.session_state.cliente_detalle_id = uid
                    st.rerun()

    st.divider()

    # ==========================================
    # DISTRIBUCION POR FUENTE IA
    # ==========================================
    st.markdown(f"#### {C.E_TUBO} Distribucion por fuente IA")

    todas_fuentes = Counter()
    for uid, datos in por_usuario.items():
        for fuente, cnt in datos.get("fuentes", {}).items():
            todas_fuentes[fuente] += cnt

    if not todas_fuentes:
        st.info("Sin datos de fuentes IA.")
        return

    cols = st.columns(min(len(todas_fuentes), 5))
    for i, (fuente, cnt) in enumerate(todas_fuentes.most_common()):
        with cols[i % len(cols)]:
            C._kpi(cols[i % len(cols)], f"{fuente}", cnt)