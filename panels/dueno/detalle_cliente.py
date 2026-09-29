# panels/dueno/detalle_cliente.py
# ============================================
# VISTA DETALLE DE CLIENTE - Panel Dueno
# ============================================

import streamlit as st
from panels.dueno import comun as C


def renderizar(uid):
    """Renderiza la vista detalle del cliente."""
    sb = C._get_supabase()
    if sb is None:
        st.error(f"{C.E_AVISO} Supabase no disponible.")
        return

    col_volver, _ = st.columns([1, 4])
    with col_volver:
        if st.button(f"{C.E_FLECHA} Volver a la lista", use_container_width=True):
            st.session_state.cliente_detalle_id = None
            st.rerun()

    st.markdown(f"# {C.E_USUARIO} Detalle del cliente")
    st.caption(f"ID de usuario: `{uid}`")

    estados = C._obtener_estados_usuarios(sb)
    estado = C._estado_de(uid, estados)
    if estado == "suspendido":
        info = estados.get(uid, {})
        st.error(
            f"{C.E_PROHIBIDO} **CUENTA SUSPENDIDA**\n\n"
            f"Motivo: {info.get('motivo', 'Sin motivo especificado')}\n\n"
            f"Fecha: {str(info.get('fecha_accion', '?'))[:19].replace('T', ' ')}"
        )
    else:
        st.success(f"{C.E_OK} **Cuenta activa**")

    st.divider()

    try:
        data_neg = sb.table("negocios").select("*").execute().data or []
    except Exception as e:
        st.error(f"Error leyendo negocios: {e}")
        return

    try:
        eventos_todos = sb.table("eventos_app").select("*").order("created_at", desc=True).limit(2000).execute().data or []
    except Exception:
        eventos_todos = []

    negocios_todos = [C._plano(n) for n in data_neg]
    mis_negocios = [n for n in negocios_todos if n.get("usuario_id") == uid]
    mis_eventos = [e for e in eventos_todos if e.get("usuario_id") == uid]

    if not mis_negocios and not mis_eventos:
        st.warning(f"{C.E_AVISO} No se encontro informacion de este cliente.")
        return

    total_negocios = len(mis_negocios)
    total_webs = sum(1 for n in mis_negocios if (n.get("sitio_web") or {}).get("archivo_generado") or n.get("web_url"))
    total_eventos = len(mis_eventos)
    total_modificaciones = sum(1 for e in mis_eventos if e.get("tipo") == "modificar_web")
    total_webs_generadas = sum(1 for e in mis_eventos if e.get("tipo") == "generar_web")

    c1, c2, c3, c4, c5 = st.columns(5)
    C._kpi(c1, "Negocios", total_negocios)
    C._kpi(c2, "Webs activas", total_webs)
    C._kpi(c3, "Webs generadas", total_webs_generadas)
    C._kpi(c4, "Modificaciones IA", total_modificaciones)
    C._kpi(c5, "Eventos", total_eventos)

    st.divider()

    if mis_eventos:
        ultimo = max(mis_eventos, key=lambda e: e.get("created_at", "") or "")
        fecha_ultimo = str(ultimo.get("created_at", ""))[:19].replace("T", " ")
        st.info(f"{C.E_RELOJ} **Ultima actividad:** {fecha_ultimo} ({ultimo.get('tipo', '?')})")
    else:
        st.warning(f"{C.E_AVISO} Sin actividad registrada.")

    st.divider()

    st.markdown(f"### {C.E_CORONA} Sus negocios ({total_negocios})")
    if not mis_negocios:
        st.info("Este cliente aun no tiene negocios.")
    else:
        for n in mis_negocios:
            C._renderizar_negocio_con_acciones(sb, n)

    st.divider()

    st.markdown(f"### {C.E_HISTORIAL} Ultimas acciones ({min(len(mis_eventos), 30)})")
    if not mis_eventos:
        st.info("Sin acciones registradas.")
    else:
        for e in mis_eventos[:30]:
            C._renderizar_evento_linea(e)