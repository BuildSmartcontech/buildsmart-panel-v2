# panels/dueno/tab_pedidos_web.py
# ============================================
# TAB PEDIDOS WEB - Panel Dueno SAMU IA
# ============================================
# V2.4: Selector de modelo OpenRouter visible en el tab
# ============================================

import streamlit as st
import datetime
from panels.dueno import comun as C
from panels.dueno import pedidos_web_acciones as ACC
from utils.openrouter_manager import MODELOS_GRATUITOS, MODELOS_PREMIUM

E_PEDIDO   = "\U0001F4E6"
E_OK       = "\u2705"
E_AVISO    = "\u26A0\uFE0F"
E_X        = "\u274C"
E_DINERO   = "\U0001F4B0"
E_RELOJ    = "\U0001F550"
E_EMAIL    = "\U0001F4E7"
E_TELEFONO = "\U0001F4F1"
E_CORONA   = "\U0001F451"
E_COHETE   = "\U0001F680"
E_OJO      = "\U0001F441\uFE0F"
E_GLOBO    = "\U0001F310"
E_ROBOT    = "\U0001F916"

ESTADOS = {
    "pendiente_pago_manual": {"label": "Pendiente pago", "icono": E_RELOJ},
    "pagado":                {"label": "Pagado",          "icono": E_OK},
    "generando":             {"label": "Generando",       "icono": E_COHETE},
    "entregado":             {"label": "Entregado",       "icono": E_OK},
    "fallido":               {"label": "Fallido",         "icono": E_X},
}

TIER_LABELS = {1: "Premium Esencial", 2: "Premium + CRM", 3: "Premium Plus"}

def _fmt_fecha(iso_str):
    if not iso_str: return "?"
    dt = C._parse_fecha_segura(iso_str)
    if dt is None: return str(iso_str)[:19].replace("T", " ")
    return dt.strftime("%d/%m/%Y %H:%M")

def _estado_info(estado):
    estado_limpio = str(estado).lower().strip()
    return ESTADOS.get(estado_limpio, {"label": estado, "icono": E_AVISO})

def _cargar_pedidos(sb):
    try:
        return sb.table("pedidos_web").select("*").order("created_at", desc=True).limit(500).execute().data or []
    except Exception as e:
        print(f"[tab_pedidos_web] Error: {e}")
        return []

def _cambiar_estado(sb, pedido_id, nuevo_estado):
    try:
        payload = {"estado": nuevo_estado.lower().strip(), "updated_at": datetime.datetime.now().isoformat()}
        if nuevo_estado == "pagado": payload["pagado_at"] = datetime.datetime.now().isoformat()
        elif nuevo_estado == "entregado": payload["entregado_at"] = datetime.datetime.now().isoformat()
        sb.update("pedidos_web", payload, "id", pedido_id)
        return True, f"Estado cambiado a {nuevo_estado}"
    except Exception as e:
        return False, f"Error: {e}"

def renderizar(sb, inicio=None, fin=None):
    st.markdown(f"### {E_PEDIDO} Pedidos Web Gancho")
    st.caption("Gestiona los pedidos de webs individuales.")

    # --- SELECTOR DE MODELO VISIBLE EN EL TAB ---
    st.markdown(f"#### {E_ROBOT} Motor de IA para generar webs")
    st.caption("Selecciona el modelo de OpenRouter que se usará al hacer clic en 'Generar web'.")
    
    opciones = {**MODELOS_GRATUITOS, **MODELOS_PREMIUM}
    modelo_seleccionado = st.selectbox(
        "Modelo de generación",
        options=list(opciones.keys()),
        format_func=lambda x: f"{x.split('/')[-1]} — {opciones[x]}",
        index=0,
        key="modelo_generacion_web_tab"
    )
    st.divider()

    pedidos = _cargar_pedidos(sb)

    total = len(pedidos)
    pendientes = sum(1 for p in pedidos if str(p.get("estado", "")).lower() == "pendiente_pago_manual")
    pagados = sum(1 for p in pedidos if str(p.get("estado", "")).lower() == "pagado")
    entregados = sum(1 for p in pedidos if str(p.get("estado", "")).lower() == "entregado")

    ingresos = sum(float(p.get("precio_usd", 0) or 0) for p in pedidos if str(p.get("estado", "")).lower() in ("pagado", "entregado", "generando"))

    c1, c2, c3, c4, c5 = st.columns(5)
    C._kpi(c1, f"{E_PEDIDO} Total", total)
    C._kpi(c2, f"{E_RELOJ} Pendientes", pendientes)
    C._kpi(c3, f"{E_OK} Pagados", pagados)
    C._kpi(c4, f"{E_COHETE} Entregados", entregados)
    C._kpi(c5, f"{E_DINERO} Ingresos", f"USD {ingresos:,.0f}")

    st.divider()

    if not pedidos:
        st.info(f"{E_AVISO} Aun no hay pedidos de Web Gancho.")
        return

    col_f1, col_f2 = st.columns([2, 2])
    with col_f1:
        filtro_estado = st.selectbox("Filtrar por estado", ["(todos)"] + list(ESTADOS.keys()), format_func=lambda x: "(todos)" if x == "(todos)" else f"{ESTADOS[x]['label']}", key="pedidos_filtro_estado")
    with col_f2:
        busqueda = st.text_input("Buscar por email o nombre", "", key="pedidos_busqueda")

    filtrados = []
    for p in pedidos:
        estado_limpio = str(p.get("estado", "")).lower().strip()
        if filtro_estado != "(todos)" and estado_limpio != filtro_estado: continue
        if busqueda:
            texto = (str(p.get("email", "")) + " " + str(p.get("nombre_cliente", ""))).lower()
            if busqueda.lower() not in texto: continue
        filtrados.append(p)

    st.caption(f"Mostrando {len(filtrados)} de {total} pedidos")
    st.divider()

    if not filtrados:
        st.info(f"{E_AVISO} Ningun pedido coincide con los filtros.")
        return

    for p in filtrados:
        _renderizar_pedido(sb, p, modelo_seleccionado)

def _renderizar_pedido(sb, p, modelo_seleccionado):
    pedido_id = p.get("id", "?")
    fecha = _fmt_fecha(p.get("created_at"))
    tier_num = p.get("tier", 1)
    tier_label = TIER_LABELS.get(tier_num, f"Tier {tier_num}")
    precio = p.get("precio_usd", 0)
    estado = str(p.get("estado", "?")).lower().strip()
    info_estado = _estado_info(estado)

    email = p.get("email", "?")
    nombre = p.get("nombre_cliente", "Sin nombre")

    titulo = f"{info_estado['icono']} [{fecha}] {nombre} - {tier_label} (USD {precio:.0f})"

    with st.expander(titulo):
        col_a, col_b = st.columns([3, 2])

        with col_a:
            st.markdown(f"**{E_CORONA} {nombre}**")
            st.markdown(f"{E_EMAIL} {email}")
            if p.get("telefono"): st.markdown(f"{E_TELEFONO} {p.get('telefono')}")
            st.markdown(f"**Plan:** {tier_label} - USD {precio:.0f}")
            st.markdown(f"**Estado:** {info_estado['icono']} {info_estado['label']}")
            st.caption(f"ID: `{pedido_id}`")
            if p.get("web_url"): st.markdown(f"**{E_GLOBO} Web:** [{p.get('web_url')}]({p.get('web_url')})")

        with col_b:
            st.markdown("**Datos del negocio:**")
            datos = p.get("datos_negocio") or {}
            if isinstance(datos, dict):
                st.markdown(f"**{E_CORONA} {datos.get('nombre_negocio', '?')}**")
                st.caption(f"Sector: {datos.get('sector', '?')}")
                if datos.get("descripcion"): st.caption(f"_{datos.get('descripcion', '')[:120]}_")
            else: st.caption("(Sin datos del negocio)")

        st.divider()
        _renderizar_acciones(sb, p, modelo_seleccionado)

def _generar_web_accion(sb, p, modelo):
    with st.spinner(f"Generando web con {modelo}... (esto puede tardar 60s)"):
        resultado = ACC.generar_web_para_pedido(sb, p, modelo_ia=modelo)

    exito = resultado.get("exito", False)
    msg = resultado.get("mensaje", "")
    url = resultado.get("url_publica", "")

    if exito:
        st.success(f"{E_OK} {msg}")
        if url: st.markdown(f"{E_GLOBO} **URL publica:** [{url}]({url})")
        st.balloons()
        st.rerun()
    else:
        st.error(f"{E_X} {msg}")

def _renderizar_acciones(sb, p, modelo_seleccionado):
    pedido_id = p.get("id", "?")
    estado = str(p.get("estado", "?")).lower().strip()

    if estado == "pendiente_pago_manual":
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"{E_OK} Marcar como PAGADO", key=f"marcar_pagado_{pedido_id}", use_container_width=True, type="primary"):
                ok, msg = _cambiar_estado(sb, pedido_id, "pagado")
                if ok: st.success(msg); st.rerun()
                else: st.error(msg)
        with col2:
            if st.button(f"{E_X} Rechazar pedido", key=f"rechazar_{pedido_id}", use_container_width=True):
                ok, msg = _cambiar_estado(sb, pedido_id, "fallido")
                if ok: st.warning(f"{E_AVISO} Pedido marcado como fallido"); st.rerun()
                else: st.error(msg)

    elif estado == "pagado":
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"{E_COHETE} Generar web ahora", key=f"generar_{pedido_id}", use_container_width=True, type="primary"):
                _generar_web_accion(sb, p, modelo_seleccionado)
        with col2:
            if st.button(f"{E_OK} Marcar como ENTREGADO", key=f"entregar_{pedido_id}", use_container_width=True):
                ok, msg = _cambiar_estado(sb, pedido_id, "entregado")
                if ok: st.success(msg); st.rerun()
                else: st.error(msg)

    elif estado == "entregado":
        st.success(f"{E_OK} Pedido completado y entregado al cliente.")
        if p.get("web_url"): st.markdown(f"**{E_GLOBO} URL de la web:** [{p.get('web_url')}]({p.get('web_url')})")
        if p.get("web_id"): st.caption(f"Web ID: `{p.get('web_id')}`")
        st.write("")
        st.caption("¿Quieres cambiar el diseño? Puedes regenerar la web.")
        if st.button(f"{E_COHETE} Forzar Regeneracion de Web", key=f"force_regen_{pedido_id}", use_container_width=True, type="secondary"):
            _generar_web_accion(sb, p, modelo_seleccionado)

    elif estado == "fallido":
        st.error(f"{E_X} Pedido rechazado o fallido.")
    else:
        st.info(f"Estado actual: {estado}")