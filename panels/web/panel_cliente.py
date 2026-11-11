# panels/web/panel_cliente.py
# ============================================
# MINI-PANEL DEL CLIENTE - Web Gancho SAMU IA
# ============================================
# V1.2: Integracion de cobro por ePayco en 4to cambio.
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
E_RAYO      = "\u26A1"

LIMITE_MODIFICACIONES = 3

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

def _get_supabase():
    try:
        from utils.supabase_rest import supabase_rest
        return supabase_rest if supabase_rest.disponible else None
    except Exception:
        return None

def _fmt_fecha(iso_str):
    if not iso_str: return "?"
    try:
        s = str(iso_str).replace("Z", "")
        if "+" in s and "T" in s:
            base = s.rsplit("+", 1)[0]
            if "." in base: base = base.split(".")[0]
            dt = datetime.datetime.fromisoformat(base)
        else:
            if "." in s: s = s.split(".")[0]
            dt = datetime.datetime.fromisoformat(s)
        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return str(iso_str)[:19]

def _cargar_leads(sb, pedido_id):
    try:
        rows = sb.table("crm_leads").select("*").eq("pedido_web_id", pedido_id).execute().data or []
        rows.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return rows
    except Exception:
        return []

def _solicitar_modificacion(sb, pedido, instruccion):
    pedido_id = pedido.get("id")
    web_id = pedido.get("web_id")
    usuario_id = pedido.get("email", "usuario_web") 
    usadas = int(pedido.get("modificaciones_usadas", 0))

    try:
        from utils.web_editor_v2 import editar_y_guardar_v2
        from utils.web_publisher import publicar_web
        
        contexto = f"Negocio: {pedido.get('datos_negocio', {}).get('nombre_negocio', '')}\n"
        contexto += f"Sector: {pedido.get('datos_negocio', {}).get('sector', '')}"

        resultado = editar_y_guardar_v2(usuario_id, web_id, instruccion, contexto)

        if resultado.get("exito"):
            sb.update(
                "pedidos_web",
                {"modificaciones_usadas": usadas + 1, "updated_at": datetime.datetime.now().isoformat()},
                "id", pedido_id
            )
            publicar_web(usuario_id, web_id)
            return True, "¡Tu web se ha modificado y republicado con exito!"
        else:
            return False, f"Error de la IA: {resultado.get('error')}"
            
    except Exception as e:
        return False, f"Error del sistema: {str(e)}"

def _renderizar_login():
    st.markdown(f"# {E_LLAVE} Acceso al panel")
    st.markdown("Para acceder a tu panel, usa el link que te enviamos por email.")
    st.divider()
    st.markdown("### Ingresá tu email")
    email = st.text_input("Tu email", placeholder="tu@email.com", key="panel_email")
    if st.button(f"{E_OK} Enviar link de acceso", use_container_width=True, type="primary"):
        if not email or "@" not in email:
            st.error(f"{E_AVISO} Email invalido")
        else:
            st.info(f"{E_AVISO} Funcion proximamente. Escribinos a hola@samu-ia.com")

def _renderizar_panel(pedido, sb):
    pedido_id = pedido.get("id", "?")
    nombre = pedido.get("nombre_cliente", "Cliente")
    email = pedido.get("email", "?")
    tier_num = pedido.get("tier", 1)
    tier_label = TIER_LABELS.get(tier_num, f"Tier {tier_num}")
    precio = pedido.get("precio_usd", 0)
    estado = str(pedido.get("estado", "")).lower()
    info_estado = ESTADOS.get(estado, {"label": estado, "icono": E_AVISO})
    datos_negocio = pedido.get("datos_negocio") or {}
    web_url = pedido.get("web_url", "")
    web_id = pedido.get("web_id", "")
    
    modificaciones_usadas = int(pedido.get("modificaciones_usadas", 0))
    modificaciones_restantes = max(0, LIMITE_MODIFICACIONES - modificaciones_usadas)

    st.markdown(f"# {E_CORONA} Tu panel - SAMU IA")
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.markdown(f"**Cliente:** {nombre}")
        st.caption(f"{email}")
    with col_h2:
        st.markdown(f"**Plan:** {tier_label}")
        st.caption(f"USD {precio:.0f} - pago unico")

    st.divider()

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Estado", f"{info_estado['icono']} {info_estado['label']}")
    with c2: st.metric("Web", "Activa" if web_url else "Sin crear")
    with c3: st.metric("Leads", len(_cargar_leads(sb, pedido_id)) if tier_num >= 2 else "-")

    st.divider()

    st.markdown(f"### {E_GLOBO} Tu web")
    if web_url:
        st.success(f"{E_OK} Tu web esta publicada y activa")
        st.markdown(f"**URL publica:** [{web_url}]({web_url})")
        
        st.write("")
        st.markdown(f"#### {E_RAYO} Modificar mi web")
        
        if modificaciones_restantes > 0:
            st.info(f"Tienes **{modificaciones_restantes}** modificaciones gratis restantes (de {LIMITE_MODIFICACIONES}).")
            
            with st.form("form_modificacion"):
                instruccion = st.text_area("¿Que quieres cambiar?", placeholder="Ej: Cambia el titulo a 'Bienvenidos' y pon el fondo de color gris oscuro.", height=100)
                btn_mod = st.form_submit_button(f"{E_COHETE} Aplicar cambio", type="primary", use_container_width=True)
                
                if btn_mod and instruccion.strip():
                    with st.spinner("La IA esta aplicando los cambios... (esto puede tardar 1 minuto)"):
                        exito, msg = _solicitar_modificacion(sb, pedido, instruccion)
                    if exito:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                elif btn_mod:
                    st.warning("Escribe lo que quieres cambiar.")
        else:
            st.warning(f"Has agotado tus {LIMITE_MODIFICACIONES} modificaciones gratis.")
            st.markdown("Cada modificacion adicional cuesta **USD 5**.")
            
            # --- NUEVA LOGICA DE COBRO EPAYCO ---
            from panels.web.pagos import obtener_proveedor, proveedor_actual
            prov_nombre = proveedor_actual()
            proveedor = obtener_proveedor(prov_nombre, {})
            pedido_pago_id = f"mod_extra_{pedido_id}_{int(datetime.datetime.now().timestamp())}"
            
            res_pago = proveedor.crear_pago(
                pedido_id=pedido_pago_id,
                monto=5.0,
                descripcion=f"Modificacion extra Web Gancho - {nombre}",
                metadata={"email": email}
            )
            
            if res_pago.get("exito") and res_pago.get("url_pago"):
                st.markdown(f'<a href="{res_pago["url_pago"]}" target="_blank"><button style="background-color:#14B8A6; color:black; padding:10px 20px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">Pagar $5 USD con ePayco</button></a>', unsafe_allow_html=True)
            else:
                st.info("Contacta a soporte para adquirir mas modificaciones.")

    else:
        st.warning(f"{E_RELOJ} Tu web aun no esta lista.")
        if estado == "pendiente_pago_manual":
            st.markdown("**Que sigue:**\n1. Realiza el pago\n2. Envia el comprobante\n3. Generaremos tu web\n4. Recibiras un email")
        elif estado == "pagado":
            st.markdown("**Que sigue:**\nEstamos generando tu web. En breve recibiras un email.")

    st.divider()

    if tier_num >= 2:
        _renderizar_leads(sb, pedido_id, tier_num)
    else:
        st.info(f"{E_AVISO} **No tenes CRM incluido en tu plan.**")

    with st.expander(f"{E_DOC} Detalles del pedido"):
        st.text(f"ID: {pedido_id}")
        st.text(f"Plan: {tier_label} - USD {precio:.0f}")
        st.text(f"Fecha: {_fmt_fecha(pedido.get('created_at'))}")
        st.text(f"Nombre: {datos_negocio.get('nombre_negocio', '?')}")
        st.text(f"Sector: {datos_negocio.get('sector', '?')}")

    st.divider()
    st.markdown(f"### {E_MALETIN} Renovacion")
    st.info(f"**Tu hosting es gratis por 1 año.**\nDespues de eso: USD 59/año. Te avisaremos 30 dias antes.")

def _renderizar_leads(sb, pedido_id, tier_num):
    st.markdown(f"### {E_USUARIO} Tus leads (CRM)")
    leads = _cargar_leads(sb, pedido_id)
    if not leads:
        st.info(f"{E_LIBRO} Aun no hay leads. Cuando alguien llene tu formulario, apareceran aqui.")
        return

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Total", len(leads))
    with c2: st.metric("Nuevos", sum(1 for l in leads if l.get("estado") == "nuevo"))
    with c3: st.metric("Contactados", sum(1 for l in leads if l.get("estado") == "contactado"))
    
    st.divider()
    for lead in leads[:20]:
        _renderizar_lead(sb, lead)

def _renderizar_lead(sb, lead):
    lead_id = lead.get("id", "?")
    nombre = lead.get("nombre", "Sin nombre")
    email = lead.get("email", "-")
    telefono = lead.get("telefono", "")
    mensaje = lead.get("mensaje", "")
    estado = lead.get("estado", "nuevo")
    fecha = _fmt_fecha(lead.get("created_at"))

    with st.expander(f"{E_USUARIO} [{fecha}] {nombre} - {email}"):
        col_a, col_b = st.columns([2, 1])
        with col_a:
            if email and email != "-": st.markdown(f"{E_EMAIL} {email}")
            if telefono: st.markdown(f"{E_TELEFONO} {telefono}")
            if mensaje: st.text(mensaje[:200])
        with col_b:
            st.markdown(f"**Estado:** {estado}")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Contactado", key=f"cont_{lead_id}", use_container_width=True):
                sb.update("crm_leads", {"estado": "contactado"}, "id", lead_id)
                st.rerun()
        with col2:
            if st.button("Cerrado", key=f"cerr_{lead_id}", use_container_width=True):
                sb.update("crm_leads", {"estado": "cerrado"}, "id", lead_id)
                st.rerun()
        with col3:
            if st.button("Perdido", key=f"perd_{lead_id}", use_container_width=True):
                sb.update("crm_leads", {"estado": "perdido"}, "id", lead_id)
                st.rerun()

def renderizar():
    sb = _get_supabase()
    if not sb:
        st.error(f"{E_X} Error: Supabase no disponible")
        return
    try:
        params = st.query_params
        token = params.get("token", "")
        if isinstance(token, list): token = token[0] if token else ""
    except Exception:
        token = ""

    if not token:
        _renderizar_login()
        return

    from utils.magic_link import validar_token
    exito, pedido, error = validar_token(sb, token)
    if not exito:
        st.markdown(f"# {E_X} Acceso denegado")
        st.error(f"{E_AVISO} {error}")
        return

    _renderizar_panel(pedido, sb)