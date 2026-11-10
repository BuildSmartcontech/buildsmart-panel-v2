# panels/dueno/tab_pedidos_web.py
# ============================================
# TAB PEDIDOS WEB - Panel Dueno SAMU IA
# ============================================
# V2.5: Interfaz limpia, sin selector de modelo (usa default del sistema)
# ============================================

import streamlit as st
import datetime
from panels.dueno import comun as C
from panels.dueno import pedidos_web_acciones as ACC

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
E_GLOBO    = "\U0001F310"

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
    except Exception:
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
        st.info(f"{E_AVISO} Aun no hay pedidos.")
        return

    for p in pedidos:
        _renderizar_pedido(sb, p)

def _renderizar_pedido(sb, p):
    pedido_id = p.get("id", "?")
    fecha = _fmt_fecha(p.get("created_at"))
    tier_num = p.get("tier", 1)
    tier_label = TIER_LABELS.get(tier_num, f"Tier {tier_num}")
    precio = p.get("precio_usd", 0)
    estado = str(p.get("estado", "?")).lower().strip()
    info_estado = _estado_info(estado)

    nombre = p.get("nombre_cliente", "Sin nombre")
    email = p.get("email", "?")
    titulo = f"{info_estado['icono']} [{fecha}] {nombre} - {tier_label} (USD {precio:.0f})"

    with st.expander(titulo):
        col_a, col_b = st.columns([3, 2])
        with col_a:
            st.markdown(f"**{E_CORONA} {nombre}**")
            st.markdown(f"{E_EMAIL} {email}")
            st.markdown(f"**Plan:** {tier_label} - USD {precio:.0f}")
            st.markdown(f"**Estado:** {info_estado['icono']} {info_estado['label']}")
            st.caption(f"ID: `{pedido_id}`")
            if p.get("web_url"): st.markdown(f"**{E_GLOBO} Web:** [{p.get('web_url')}]({p.get('web_url')})")
        
        with col_b:
            datos = p.get("datos_negocio") or {}
            if isinstance(datos, dict):
                st.markdown(f"**{E_CORONA} {datos.get('nombre_negocio', '?')}**")
                st.caption(f"Sector: {datos.get('sector', '?')}")

        st.divider()
        _renderizar_acciones(sb, p)

def _generar_web_accion(sb, p):
    # Usamos el modelo por defecto definido en generar_web (nvidia/nemotron-3-super-120b)
    with st.spinner("Generando web premium... (esto puede tardar 1-2 mins)"):
        resultado = ACC.generar_web_para_pedido(sb, p)

    if resultado.get("exito"):
        st.success(f"{E_OK} {resultado.get('mensaje')}")
        url = resultado.get("url_publica", "")
        if url: st.markdown(f"{E_GLOBO} **URL publica:** [{url}]({url})")
        st.balloons()
        st.rerun()
    else:
        st.error(f"{E_X} {resultado.get('mensaje')}")

def _renderizar_acciones(sb, p):
    pedido_id = p.get("id", "?")
    estado = str(p.get("estado", "?")).lower().strip()

    if estado == "pendiente_pago_manual":
        if st.button(f"{E_OK} Marcar como PAGADO", key=f"marcar_pagado_{pedido_id}", use_container_width=True, type="primary"):
            ok, msg = _cambiar_estado(sb, pedido_id, "pagado")
            if ok: st.rerun()
    elif estado == "pagado":
        if st.button(f"{E_COHETE} Generar web ahora", key=f"generar_{pedido_id}", use_container_width=True, type="primary"):
            _generar_web_accion(sb, p)
    elif estado == "entregado":
        st.success(f"{E_OK} Pedido entregado.")
        if p.get("web_url"): st.markdown(f"**{E_GLOBO} URL:** [{p.get('web_url')}]({p.get('web_url')})")
        if st.button(f"{E_COHETE} Forzar Regeneracion", key=f"force_regen_{pedido_id}", use_container_width=True):
            _generar_web_accion(sb, p)
    else:
        st.info(f"Estado actual: {estado}")