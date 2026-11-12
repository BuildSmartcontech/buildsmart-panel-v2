# panels/web/panel_cliente.py
# ============================================
# MINI-PANEL DEL CLIENTE - Web Gancho SAMU IA
# ============================================
# V4.1: Ejemplos dinamicos por sector y registro de pagos en eventos_app.
# ============================================

import streamlit as st
import datetime
import streamlit.components.v1 as components
from panels.web import landing_data as D

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

LIMITE_MODIFICACIONES_BASE = 3
TIER_LABELS = {1: "Premium Esencial", 2: "Premium + CRM", 3: "Premium Plus"}
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

def _renderizar_vista_previa(html_content: str):
    if not html_content: return
    components.html(html_content, height=600, scrolling=True)

def _generar_web_inicial(sb, pedido):
    datos_negocio = pedido.get("datos_negocio", {})
    if not datos_negocio:
        return False, "Faltan los datos del negocio.", None

    try:
        from utils.web_generator import generar_web
        from utils.web_storage import guardar_web, generar_uuid
        
        resultado_gen = generar_web(datos_negocio=datos_negocio)
        if not resultado_gen.get("exito"):
            return False, f"Error de IA: {resultado_gen.get('error')}", None
            
        html = resultado_gen["html"]
        web_id = generar_uuid()
        usuario_id = pedido.get("email", "usuario_default")
        
        guardado = guardar_web(usuario_id=usuario_id, web_id=web_id, html=html, datos_extra={"pedido_id": pedido.get("id")})
        if not guardado.get("exito"):
            return False, f"Error guardando web: {guardado.get('error')}", None
            
        sb.update("pedidos_web", {"web_id": web_id, "estado": "pagado", "updated_at": datetime.datetime.now().isoformat()}, "id", pedido.get("id"))
        return True, "¡Web generada! Revisa la vista previa abajo.", html

    except Exception as e:
        return False, f"Error del sistema: {str(e)}", None

def _solicitar_modificacion(sb, pedido, instruccion):
    pedido_id = pedido.get("id")
    web_id = pedido.get("web_id")
    usuario_id = pedido.get("email", "usuario_web") 
    usadas = int(pedido.get("modificaciones_usadas", 0))
    extras = int(pedido.get("modificaciones_extra", 0))
    
    limite_total = LIMITE_MODIFICACIONES_BASE + extras
    restantes = max(0, limite_total - usadas)

    if restantes <= 0:
        return False, "Sin cambios disponibles.", None

    try:
        from utils.web_editor_v2 import editar_y_guardar_v2
        
        contexto = f"Negocio: {pedido.get('datos_negocio', {}).get('nombre_negocio', '')}\n"
        contexto += f"Sector: {pedido.get('datos_negocio', {}).get('sector', '')}"

        resultado = editar_y_guardar_v2(usuario_id, web_id, instruccion, contexto)

        if resultado.get("exito"):
            sb.update(
                "pedidos_web",
                {"modificaciones_usadas": usadas + 1, "updated_at": datetime.datetime.now().isoformat()},
                "id", pedido_id
            )
            return True, "¡Tu web se ha modificado! Revisa la vista previa.", resultado.get("html_nuevo")
        else:
            return False, f"Error de la IA: {resultado.get('error')}", None
            
    except Exception as e:
        return False, f"Error del sistema: {str(e)}", None

def _procesar_retorno_pago(sb, pedido_id, paquete):
    try:
        res = sb.table("pedidos_web").select("modificaciones_extra").eq("id", pedido_id).execute()
        if not res.data: return False
        extras_actuales = int(res.data[0].get("modificaciones_extra", 0))
        nuevos_extras = extras_actuales + int(paquete)
        sb.update("pedidos_web", {"modificaciones_extra": nuevos_extras}, "id", pedido_id)
        
        # --- REGISTRO DE PAGO EN EVENTOS_APP ---
        try:
            monto = 5 if int(paquete) == 1 else 12
            evento = {
                "tipo": "pago_modificacion",
                "usuario_id": pedido_id,
                "detalle": {"paquete": paquete, "monto_usd": monto},
                "created_at": datetime.datetime.now().isoformat()
            }
            sb.insert("eventos_app", evento)
        except Exception as e:
            print(f"[PANEL] Error registrando evento de pago: {e}")
            
        return True
    except Exception as e:
        return False

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
    sector = datos_negocio.get("sector", "general").lower()
    web_url = pedido.get("web_url", "")
    web_id = pedido.get("web_id", "")
    token = pedido.get("magic_token", "")
    
    usadas = int(pedido.get("modificaciones_usadas", 0))
    extras = int(pedido.get("modificaciones_extra", 0))
    limite_total = LIMITE_MODIFICACIONES_BASE + extras
    restantes = max(0, limite_total - usadas)

    try:
        params = st.query_params
        if params.get("pago") == "exitoso":
            paquete = int(params.get("paquete", 1))
            if _procesar_retorno_pago(sb, pedido_id, paquete):
                st.success(f"{E_OK} ¡Pago recibido! Se han añadido {paquete} cambios extra a tu cuenta.")
                st.query_params.clear()
                st.query_params.update({"web": "panel", "token": token})
                st.rerun()
    except Exception:
        pass

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
    with c2: st.metric("Web", "Publicada" if web_url else ("Creada" if web_id else "Sin crear"))
    with c3: st.metric("Leads", len(_cargar_leads(sb, pedido_id)) if tier_num >= 2 else "-")

    st.divider()

    st.markdown(f"### {E_GLOBO} Tu web")

    if not web_id and not web_url:
        st.warning(f"{E_RELOJ} Tu web aun no esta creada.")
        if estado == "pagado":
            st.markdown("Haz clic en el botón de abajo para que nuestra IA construya tu página web.")
            if st.button(f"{E_COHETE} Generar mi web ahora", type="primary", use_container_width=True):
                with st.spinner("La IA está construyendo tu página..."):
                    exito, msg, html_generado = _generar_web_inicial(sb, pedido)
                if exito:
                    st.session_state["preview_html"] = html_generado
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        else:
            st.markdown("**Que sigue:**\nEsperando confirmación de pago.")
    else:
        if "preview_html" not in st.session_state or not st.session_state["preview_html"]:
            try:
                from utils.web_storage import leer_web
                res_leer = leer_web(email, web_id)
                if res_leer.get("exito"):
                    st.session_state["preview_html"] = res_leer.get("html")
            except Exception:
                pass

        if web_url:
            st.success(f"{E_OK} Tu web esta publicada y activa")
            st.markdown(f"**URL publica:** [{web_url}]({web_url})")

        st.write("")
        st.markdown(f"#### {E_RAYO} Hacer un cambio en tu web")
        
        # --- EJEMPLOS DINÁMICOS SEGÚN EL SECTOR ---
        ejemplos_por_sector = {
            "turismo": "Cambia el título y ponle 'Los mejores tours de Colombia'.\nAgrega una sección sobre la Amazonía.",
            "inmobiliaria": "Cambia el título a 'Encuentra tu hogar ideal'.\nPon el fondo de la página en blanco y negro.",
            "restaurante": "Cambia el título a 'El mejor sabor de la ciudad'.\nAgrega una sección con el menú del día.",
            "general": "Cambia el título principal de tu web.\nPon el fondo de la página en color oscuro.\nAgrega una nueva sección con información de tu negocio."
        }
        ejemplos = ejemplos_por_sector.get(sector, ejemplos_por_sector["general"])

        with st.expander("💡 ¿No sabes qué escribir? Haz clic aquí para ver ejemplos", expanded=False):
            st.info(f"""
            Para que la IA te entienda perfectamente, pídele las cosas de forma sencilla. Aquí tienes algunos ejemplos:
            
            {ejemplos}
            
            *Truco: Puedes pedir una cosa a la vez para obtener resultados más rápidos.*
            """)
        # ------------------------------------------
        
        if restantes > 0:
            st.info(f"Tienes **{restantes}** modificaciones disponibles.")
            with st.form("form_modificacion"):
                instruccion = st.text_area("Escribe lo que quieres cambiar aquí:", placeholder="Ej: Cambia el título principal y pon el fondo azul oscuro.", height=100)
                btn_mod = st.form_submit_button(f"{E_COHETE} Generar Vista Previa", type="primary", use_container_width=True)
                
                if btn_mod:
                    if not instruccion.strip():
                        st.warning("Escribe lo que quieres cambiar antes de generar la vista previa.")
                    else:
                        with st.spinner("La IA esta aplicando los cambios..."):
                            exito, msg, html_nuevo = _solicitar_modificacion(sb, pedido, instruccion)
                        if exito:
                            st.session_state["preview_html"] = html_nuevo
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
        else:
            st.warning(f"Has agotado tus {limite_total} modificaciones disponibles.")
            st.markdown("Puedes comprar más cambios para seguir editando.")
            from panels.web.pagos import obtener_proveedor, proveedor_actual
            prov_nombre = proveedor_actual()
            proveedor = obtener_proveedor(prov_nombre, {})
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                if st.button(f"{E_DINERO} Comprar 1 cambio ($5)", use_container_width=True):
                    id_pago = f"mod_1_{pedido_id}_{int(datetime.datetime.now().timestamp())}"
                    res_pago = proveedor.crear_pago(id_pago, 5.0, f"1 Cambio extra - {nombre}", metadata={"token": token})
                    if res_pago.get("exito") and res_pago.get("url_pago"):
                        st.markdown(f'<meta http-equiv="refresh" content="0; url={res_pago["url_pago"]}">', unsafe_allow_html=True)
            with col_p2:
                if st.button(f"{E_DINERO} Comprar 3 cambios ($12)", use_container_width=True):
                    id_pago = f"mod_3_{pedido_id}_{int(datetime.datetime.now().timestamp())}"
                    res_pago = proveedor.crear_pago(id_pago, 12.0, f"3 Cambios extra - {nombre}", metadata={"token": token})
                    if res_pago.get("exito") and res_pago.get("url_pago"):
                        st.markdown(f'<meta http-equiv="refresh" content="0; url={res_pago["url_pago"]}">', unsafe_allow_html=True)

        if "preview_html" in st.session_state and st.session_state["preview_html"]:
            st.divider()
            st.markdown("**Revisa cómo quedó tu web:**")
            _renderizar_vista_previa(st.session_state["preview_html"])
            
            st.write("")
            st.markdown("**Si todo está bien, publícala:**")
            if st.button(f"{E_COHETE} Publicar en Vivo", type="primary", use_container_width=True):
                with st.spinner("Publicando..."):
                    from utils.web_publisher import publicar_web
                    res_pub = publicar_web(email, web_id)
                    if res_pub.get("exito"):
                        url_publica = res_pub.get("url_publica", "")
                        sb.update("pedidos_web", {"web_url": url_publica, "estado": "entregado"}, "id", pedido_id)
                        st.success("¡Tu web está en vivo!")
                        st.rerun()
                    else:
                        st.error(f"Error publicando: {res_pub.get('error')}")
        else:
            st.info("💡 La sesión se ha reiniciado. Si tu web ya estaba publicada, haz clic abajo para recuperarla.")
            if st.button("🔄 Recuperar Vista Previa"):
                try:
                    from utils.web_storage import leer_web
                    res_leer = leer_web(email, web_id)
                    if res_leer.get("exito"):
                        st.session_state["preview_html"] = res_leer.get("html")
                        st.rerun()
                    else:
                        st.error(f"No se pudo recuperar: {res_leer.get('error')}")
                except Exception as e:
                    st.error(f"Error de conexión: {e}")

    st.divider()

    if tier_num >= 2:
        _renderizar_leads(sb, pedido_id, tier_num)

    with st.expander(f"{E_DOC} Detalles del pedido"):
        st.text(f"ID: {pedido_id}")
        st.text(f"Plan: {tier_label} - USD {precio:.0f}")
        st.text(f"Fecha: {_fmt_fecha(pedido.get('created_at'))}")
        st.text(f"Nombre: {datos_negocio.get('nombre_negocio', '?')}")
        st.text(f"Sector: {datos_negocio.get('sector', '?')}")

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
    fecha = _fmt_fecha(lead.get("created_at"))

    with st.expander(f"{E_USUARIO} [{fecha}] {nombre} - {email}"):
        if lead.get("telefono"): st.markdown(f"{E_TELEFONO} {lead.get('telefono')}")
        if lead.get("mensaje"): st.text(lead.get("mensaje")[:200])
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
        st.markdown(f"# {E_LLAVE} Acceso al panel")
        st.info("Para acceder, usa el link que enviamos a tu correo.")
        return

    from utils.magic_link import validar_token
    exito, pedido, error = validar_token(sb, token)
    if not exito:
        st.markdown(f"# {E_X} Acceso denegado")
        st.error(f"{E_AVISO} {error}")
        return

    _renderizar_panel(pedido, sb)