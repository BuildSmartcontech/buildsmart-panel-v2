# panels/dueno/tab_pedidos_web.py
# ============================================
# TAB PEDIDOS WEB - Panel Dueno SAMU IA
# ============================================
# V3.1: Normaliza el estado de la BD para mostrar botones correctamente.
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
E_CORONA   = "\U0001F451"
E_COHETE   = "\U0001F680"
E_GLOBO    = "\U0001F310"
E_OJO      = "\U0001F441\uFE0F"

ESTADOS = {
    "pendiente_pago_manual": {"label": "Pendiente pago", "icono": E_RELOJ},
    "pagado":                {"label": "Pagado",          "icono": E_OK},
    "entregado":             {"label": "Entregado",       "icono": E_OK},
    "fallido":               {"label": "Fallido",         "icono": E_X},
}

TIER_LABELS = {1: "Premium Esencial", 2: "Premium + CRM", 3: "Premium Plus"}

def _normalizar_estado(estado_raw):
    """Convierte cualquier variacion de texto a un ID interno valido."""
    e = str(estado_raw).lower().strip()
    if e in ("pendiente_pago_manual", "pendiente pago", "pendiente", "pending"):
        return "pendiente_pago_manual"
    if e in ("pagado", "paid"):
        return "pagado"
    if e in ("entregado", "delivered"):
        return "entregado"
    if e in ("fallido", "failed"):
        return "fallido"
    return e

def _fmt_fecha(iso_str):
    if not iso_str: return "?"
    dt = C._parse_fecha_segura(iso_str)
    if dt is None: return str(iso_str)[:19].replace("T", " ")
    return dt.strftime("%d/%m/%Y %H:%M")

def _cargar_pedidos(sb):
    try:
        return sb.table("pedidos_web").select("*").order("created_at", desc=True).limit(500).execute().data or []
    except Exception:
        return []

def _cambiar_estado(sb, pedido_id, nuevo_estado):
    try:
        payload = {"estado": nuevo_estado.lower().strip(), "updated_at": datetime.datetime.now().isoformat()}
        sb.update("pedidos_web", payload, "id", pedido_id)
        return True, f"Estado cambiado a {nuevo_estado}"
    except Exception as e:
        return False, f"Error: {e}"

def renderizar(sb, inicio=None, fin=None):
    st.markdown(f"### {E_PEDIDO} Pedidos Web Gancho")
    st.caption("Genera VISTAS PREVIAS sin gastar creditos, y publica cuando estes seguro.")

    pedidos = _cargar_pedidos(sb)

    if not pedidos:
        st.info("Aun no hay pedidos.")
        return

    for p in pedidos:
        _renderizar_pedido(sb, p)

def _renderizar_pedido(sb, p):
    pedido_id = p.get("id", "?")
    fecha = _fmt_fecha(p.get("created_at"))
    
    # Normalizamos el estado aqui para que el titulo y los botones coincidan
    estado = _normalizar_estado(p.get("estado", ""))
    info_estado = ESTADOS.get(estado, {"label": estado, "icono": E_AVISO})
    nombre = p.get("nombre_cliente", "Sin nombre")
    
    titulo = f"{info_estado['icono']} [{fecha}] {nombre} - USD {p.get('precio_usd', 0):.0f}"
    
    with st.expander(titulo):
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown(f"**Estado:** {info_estado['label']}")
            if p.get("web_url"): st.markdown(f"**{E_GLOBO} Web Publica:** [{p.get('web_url')}]({p.get('web_url')})")
        st.divider()

        # --- LOGICA DE BOTONES ---
        if estado == "pendiente_pago_manual":
            st.markdown("#### 1. Confirmar Pago")
            if st.button(f"{E_OK} Marcar como PAGADO", key=f"marcar_pagado_{pedido_id}", use_container_width=True, type="primary"):
                ok, msg = _cambiar_estado(sb, pedido_id, "pagado")
                if ok: st.rerun()
                else: st.error(msg)

        elif estado == "pagado":
            st.markdown("#### 1. Generar y Previsualizar")
            if st.button(f"{E_OJO} Generar Vista Previa (No gasta Netlify)", key=f"preview_{pedido_id}", use_container_width=True):
                with st.spinner("Generando HTML... (esto toma 30-60s)"):
                    res = ACC.generar_web_para_pedido(sb, p, publicar=False)
                if res.get("exito"):
                    st.session_state[f"html_preview_{pedido_id}"] = res.get("html")
                    st.success(res.get("mensaje"))
                else:
                    st.error(res.get("mensaje"))

            if f"html_preview_{pedido_id}" in st.session_state:
                st.markdown("#### 2. Revisar y Publicar")
                html_preview = st.session_state[f"html_preview_{pedido_id}"]
                st.components.v1.html(html_preview, height=600, scrolling=True)
                
                if st.button(f"{E_COHETE} PUBLICAR EN NETLIFY AHORA", key=f"publish_{pedido_id}", type="primary", use_container_width=True):
                    with st.spinner("Subiendo a Netlify..."):
                        res_pub = ACC.generar_web_para_pedido(sb, p, publicar=True)
                    if res_pub.get("exito"):
                        st.success(res_pub.get("mensaje"))
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(res_pub.get("mensaje"))

        elif estado == "entregado":
            st.success(f"{E_OK} Pedido entregado.")
            if st.button(f"{E_OJO} Regenerar Vista Previa", key=f"force_preview_{pedido_id}", use_container_width=True):
                with st.spinner("Generando HTML..."):
                    res = ACC.generar_web_para_pedido(sb, p, publicar=False)
                if res.get("exito"):
                    st.session_state[f"html_preview_{pedido_id}"] = res.get("html")
                    st.success("Vista previa regenerada.")
                else:
                    st.error(res.get("mensaje"))
            
            if f"html_preview_{pedido_id}" in st.session_state:
                st.components.v1.html(st.session_state[f"html_preview_{pedido_id}"], height=600, scrolling=True)
        else:
            st.warning(f"Estado actual en BD: {p.get('estado')}")