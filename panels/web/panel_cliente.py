# panels/web/panel_cliente.py
# ============================================
# MINI-PANEL DEL CLIENTE - Web Gancho SAMU IA
# ============================================
# El cliente entra con ?web=panel&token=xxx
# y ve:
# - Estado de su pedido
# - URL publica de su web
# - Leads capturados (Tier 2/3)
# - Info de renovacion
#
# V1.0: Version inicial
# ============================================

import streamlit as st
import datetime
from panels.web import landing_data as D


# ==========================================
# EMOJIS ASCII-SAFE
# ==========================================
E_OK        = "\u2705"
E_X         = "\u274C"
E_AVISO     = "\u26A0\uFE0F"
E_CORONA    = "\U0001F451"
E_GLOBO     = "\U0001F310"
E_COHETE    = "\U0001F680"
E_RELOJ     = "\U0001F550"
E_USUARIO   = "\U0001F464"
E_EMAIL     = "\U0001F4E7"
E_TELEFONO  = "\U0001F4F1"
E_DOC       = "\U0001F4C4"
E_LIBRO     = "\U0001F4DC"
E_MALETIN   = "\U0001F4BC"
E_DINERO    = "\U0001F4B0"
E_LLAVE     = "\U0001F511"


TIER_LABELS = {
    1: "Premium Esencial",
    2: "Premium + CRM",
    3: "Premium Plus",
}

ESTADOS = {
    "pendiente_pago_manual": {"label": "Pendiente pago", "icono": E_RELOJ},
    "pagado":                {"label": "Pagado",          "icono": E_OK},
    "generando":             {"label": "Generando web",   "icono": E_COHETE},
    "entregado":             {"label": "Web lista",       "icono": E_OK},
    "fallido":               {"label": "Fallido",         "icono": E_X},
}


# ==========================================
# HELPERS
# ==========================================
def _get_supabase():
    try:
        from utils.supabase_rest import supabase_rest
        return supabase_rest if supabase_rest.disponible else None
    except Exception:
        return None


def _fmt_fecha(iso_str):
    if not iso_str:
        return "?"
    try:
        s = str(iso_str).replace("Z", "")
        if "+" in s and "T" in s:
            base = s.rsplit("+", 1)[0]
            if "." in base:
                base = base.split(".")[0]
            dt = datetime.datetime.fromisoformat(base)
        else:
            if "." in s:
                s = s.split(".")[0]
            dt = datetime.datetime.fromisoformat(s)
        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return str(iso_str)[:19]


def _cargar_leads(sb, pedido_id):
    """Carga los leads capturados por la web del cliente."""
    try:
        rows = sb.table("crm_leads").select("*").eq("pedido_web_id", pedido_id).execute().data or []
        rows.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return rows
    except Exception:
        return []


# ==========================================
# RENDERIZADO
# ==========================================
def _renderizar_login():
    """Pantalla si el token es invalido o falta."""
    st.markdown(f"# {E_LLAVE} Acceso al panel")
    st.markdown(
        "Para acceder a tu panel, usa el link que te enviamos por email."
    )

    st.divider()
    st.markdown("### Ingresá tu email")
    st.caption(
        "Te enviamos un link de acceso al email con el que compraste tu web."
    )

    email = st.text_input("Tu email", placeholder="tu@email.com", key="panel_email")

    if st.button(f"{E_OK} Enviar link de acceso", use_container_width=True, type="primary"):
        if not email or "@" not in email:
            st.error(f"{E_AVISO} Email invalido")
        else:
            st.info(
                f"{E_AVISO} **Funcion: proximamente**\n\n"
                f"Por ahora, si perdiste el email, escribinos y te reenviamos el link.\n"
                f"El sistema de reenvio automatico esta en desarrollo."
            )


def _renderizar_panel(pedido, sb):
    """Panel principal del cliente."""

    # Datos
    pedido_id = pedido.get("id", "?")
    nombre = pedido.get("nombre_cliente", "Cliente")
    email = pedido.get("email", "?")
    tier_num = pedido.get("tier", 1)
    tier_label = TIER_LABELS.get(tier_num, f"Tier {tier_num}")
    precio = pedido.get("precio_usd", 0)
    estado = pedido.get("estado", "?")
    info_estado = ESTADOS.get(estado, {"label": estado, "icono": E_AVISO})
    datos_negocio = pedido.get("datos_negocio") or {}
    web_url = pedido.get("web_url", "")
    web_id = pedido.get("web_id", "")

    # Header
    st.markdown(f"# {E_CORONA} Tu panel - SAMU IA")

    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.markdown(f"**Cliente:** {nombre}")
        st.caption(f"{email}")
    with col_h2:
        st.markdown(f"**Plan:** {tier_label}")
        st.caption(f"USD {precio:.0f} - pago unico")

    st.divider()

    # KPIs
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Estado", f"{info_estado['icono']} {info_estado['label']}")
    with c2:
        st.metric("Web", "Activa" if web_url else "Sin crear")
    with c3:
        st.metric("Leads", len(_cargar_leads(sb, pedido_id)) if tier_num >= 2 else "-")

    st.divider()

    # Web
    st.markdown(f"### {E_GLOBO} Tu web")
    if web_url:
        st.success(f"{E_OK} Tu web esta publicada y activa")
        st.markdown(f"**URL publica:** [{web_url}]({web_url})")
        st.caption(
            "Compartila con tus clientes. Funciona en cualquier dispositivo. "
            "El hosting es gratis por 1 año."
        )
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.markdown(f"[{E_GLOBO} Abrir mi web]({web_url})")
        with col_b2:
            if st.button(f"{E_DOC} Solicitar cambio", use_container_width=True, key="btn_cambio_web"):
                st.info(
                    f"{E_AVISO} Para modificar tu web, escribinos a "
                    f"**hola@samu-ia.com** indicando:\n\n"
                    f"1. Tu ID de pedido: `{pedido_id}`\n"
                    f"2. Que cambio queres hacer\n\n"
                    f"El sistema de modificacion automatica esta en desarrollo."
                )
    else:
        st.warning(f"{E_RELOJ} Tu web aun no esta lista.")
        if estado == "pendiente_pago_manual":
            st.markdown(
                "**Que sigue:**\n"
                "1. Realiza el pago con los datos que te enviamos\n"
                "2. Envia el comprobante\n"
                "3. Confirmaremos el pago y generaremos tu web\n"
                "4. Recibiras otro email cuando este lista"
            )
        elif estado == "pagado":
            st.markdown(
                "**Que sigue:**\n"
                "Estamos generando tu web. En breve recibiras otro email con la URL."
            )

    st.divider()

    # Leads (solo Tier 2/3)
    if tier_num >= 2:
        _renderizar_leads(sb, pedido_id, tier_num)
    else:
        st.info(
            f"{E_AVISO} **No tenes CRM incluido en tu plan.**\n\n"
            f"Con el plan {tier_label} solo incluye la web. "
            f"Si queres capturar leads, podes actualizar a Premium + CRM."
        )

    st.divider()

    # Info del pedido
    with st.expander(f"{E_DOC} Detalles del pedido"):
        st.text(f"ID: {pedido_id}")
        st.text(f"Plan: {tier_label} - USD {precio:.0f}")
        st.text(f"Fecha de compra: {_fmt_fecha(pedido.get('created_at'))}")
        if web_id:
            st.text(f"Web ID: {web_id}")

        st.markdown("**Tu negocio:**")
        st.text(f"Nombre: {datos_negocio.get('nombre_negocio', '?')}")
        st.text(f"Sector: {datos_negocio.get('sector', '?')}")

    # Renovacion
    st.divider()
    st.markdown(f"### {E_MALETIN} Renovacion")
    st.info(
        f"**Tu hosting es gratis por 1 año.**\n\n"
        f"Despues del primer año, podes:\n"
        f"- **Renovar** por USD 59/año (o USD 79 con dominio propio)\n"
        f"- **Descargar** tu web como HTML y llevartela\n"
        f"- **Actualizar** al plan PIME (USD 99/mes) y obtener el ERP completo\n\n"
        f"Te enviaremos un aviso 30 dias antes del vencimiento."
    )

    # Footer
    st.divider()
    st.caption(f"SAMU IA - Tu web profesional · ¿Consultas? hola@samu-ia.com")


def _renderizar_leads(sb, pedido_id, tier_num):
    """Muestra los leads capturados por la web."""
    st.markdown(f"### {E_USUARIO} Tus leads")

    leads = _cargar_leads(sb, pedido_id)

    if not leads:
        st.info(
            f"{E_LIBRO} **Aun no hay leads.**\n\n"
            f"Cuando alguien complete el formulario de tu web, "
            f"va a aparecer aca automaticamente.\n\n"
            f"(El formulario de tu web esta conectado a este panel.)"
        )
        return

    # KPIs
    total = len(leads)
    nuevos = sum(1 for l in leads if l.get("estado") == "nuevo")
    contactados = sum(1 for l in leads if l.get("estado") == "contactado")
    cerrados = sum(1 for l in leads if l.get("estado") == "cerrado")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total", total)
    with c2:
        st.metric("Nuevos", nuevos)
    with c3:
        st.metric("Contactados", contactados)
    with c4:
        st.metric("Cerrados", cerrados)

    st.divider()

    # Lista
    for lead in leads[:20]:
        _renderizar_lead(sb, lead)


def _renderizar_lead(sb, lead):
    """Renderiza un lead individual."""
    lead_id = lead.get("id", "?")
    nombre = lead.get("nombre", "Sin nombre")
    email = lead.get("email", "-")
    telefono = lead.get("telefono", "")
    mensaje = lead.get("mensaje", "")
    estado = lead.get("estado", "nuevo")
    fecha = _fmt_fecha(lead.get("created_at"))

    icono = {
        "nuevo": "\U0001F195",
        "contactado": "\U0001F4DE",
        "cerrado": E_OK,
        "perdido": E_X,
    }.get(estado, E_AVISO)

    with st.expander(f"{icono} [{fecha}] {nombre} - {email}"):
        col_a, col_b = st.columns([2, 1])
        with col_a:
            if email and email != "-":
                st.markdown(f"{E_EMAIL} {email}")
            if telefono:
                st.markdown(f"{E_TELEFONO} {telefono}")
            if mensaje:
                st.markdown(f"**Mensaje:**")
                st.text(mensaje[:500])

        with col_b:
            st.markdown(f"**Estado:** {estado}")
            st.caption("Cambialo con los botones:")

        # Botones de estado
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"{E_OK} Contactado", key=f"contactar_{lead_id}", use_container_width=True):
                _cambiar_estado_lead(sb, lead_id, "contactado")
                st.rerun()
        with col2:
            if st.button(f"{E_OK} Cerrado", key=f"cerrar_{lead_id}", use_container_width=True):
                _cambiar_estado_lead(sb, lead_id, "cerrado")
                st.rerun()
        with col3:
            if st.button(f"{E_X} Perdido", key=f"perder_{lead_id}", use_container_width=True):
                _cambiar_estado_lead(sb, lead_id, "perdido")
                st.rerun()


def _cambiar_estado_lead(sb, lead_id, nuevo_estado):
    """Cambia el estado de un lead."""
    try:
        sb.update(
            "crm_leads",
            {
                "estado": nuevo_estado,
                "updated_at": datetime.datetime.now().isoformat(),
            },
            "id",
            lead_id,
        )
    except Exception as e:
        print(f"[panel_cliente] Error cambiando estado: {e}")


# ==========================================
# ENTRY POINT
# ==========================================
def renderizar():
    """Punto de entrada del panel del cliente."""
    sb = _get_supabase()
    if not sb:
        st.error(f"{E_X} Error: Supabase no disponible")
        return

    # Obtener token
    try:
        params = st.query_params
        token = params.get("token", "")
        if isinstance(token, list):
            token = token[0] if token else ""
    except Exception:
        token = ""

    if not token:
        _renderizar_login()
        return

    # Validar token
    from utils.magic_link import validar_token
    exito, pedido, error = validar_token(sb, token)

    if not exito:
        st.markdown(f"# {E_X} Acceso denegado")
        st.error(f"{E_AVISO} {error}")
        st.caption(
            "Si crees que es un error, escribinos a hola@samu-ia.com "
            "indicando tu email de compra."
        )
        return

    _renderizar_panel(pedido, sb)


# ==========================================
# TEST
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print("TEST PANEL CLIENTE")
    print("=" * 60)
    print("Este modulo se usa desde Streamlit con URL:")
    print("  ?web=panel&token=xxx")
    print("=" * 60)