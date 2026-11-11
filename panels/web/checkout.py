# panels/web/checkout.py
# ============================================
# CHECKOUT UI - Web Gancho SAMU IA
# ============================================
# V5.9: Arreglo de loop en file_uploader y warnings de ancho.
# ============================================

import streamlit as st
import base64
from panels.web import landing_data as D

try:
    from panels.web.pagos import obtener_proveedor, proveedor_actual
except ImportError:
    obtener_proveedor = None
    proveedor_actual = None

from utils.paises import PAISES_DEFAULT, obtener_prefijo, obtener_nombres
from utils.security import validar_imagen_subida

from panels.web.checkout_validators import (
    SECTORES, validar_formulario, calcular_faltantes,
)
from panels.web.checkout_data import (
    datos_pago_desde_config, crear_pedido_y_avanzar, limpiar_estado_checkout,
)

E_OK        = "\u2705"
E_AVISO     = "\u26A0\uFE0F"
E_X         = "\u274C"
E_FLECHA    = "\u2B05\uFE0F"
E_DINERO    = "\U0001F4B0"
E_CELULAR   = "\U0001F4F1"
E_DOC       = "\U0001F4C4"
E_COHETE    = "\U0001F680"
E_RELOJ     = "\U0001F550"
E_CORONA    = "\U0001F451"
E_CHAT      = "\U0001F4AC"
E_PIN       = "\U0001F4CD"
E_TIENDA    = "\U0001F3EA"
E_GLOBO     = "\U0001F310"
E_CAMARA    = "\U0001F4F8"

def _procesar_imagen_subida(file):
    if not file:
        return None
    bytes_data = file.read()
    base64_str = base64.b64encode(bytes_data).decode("utf-8")
    mime = file.type
    return f"data:{mime};base64,{base64_str}"

def _renderizar_formulario(tier):
    st.markdown(f"# {E_CORONA} Checkout - {tier['nombre']}")
    st.markdown(f"**Plan:** {tier['precio_label']} ({tier['pago_label']})")
    st.caption("Los campos marcados con * son obligatorios. El resto es opcional.")
    st.divider()

    # TUS DATOS
    st.markdown(f"### {E_CELULAR} Tus datos (contacto)")
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Tu nombre completo *", placeholder="Ej: Antonio Porras", key="ck_nombre")
        telefono = st.text_input("Tu telefono personal", placeholder="Ej: 300 123 4567", help="Solo lo usamos para contactarte si hay alguna duda con tu pedido.", key="ck_telefono")
    with col2:
        email = st.text_input("Tu email *", placeholder="Ej: tu@email.com", key="ck_email")
        st.write("")
        st.caption("Aca te enviaremos tu web cuando este lista.")

    # DATOS DEL NEGOCIO
    st.divider()
    st.markdown(f"### {E_TIENDA} Datos de tu negocio")
    col3, col4 = st.columns(2)
    with col3:
        nombre_negocio = st.text_input("Nombre del negocio *", placeholder="Ej: Panaderia Los Tres Amigos", key="ck_nombre_negocio")
    with col4:
        sector_sel = st.selectbox("Sector *", SECTORES, index=0, key="ck_sector")

    sector_otro = ""
    if sector_sel == "Otro (especificar abajo)":
        sector_otro = st.text_input("Especifica tu sector *", placeholder="Ej: Venta de velas artesanales", key="ck_sector_otro")

    descripcion = st.text_area("Descripcion breve (2-3 lineas) *", placeholder="Conta que hace tu negocio, que vendes, a quien.", height=100, key="ck_descripcion")
    publico_objetivo = st.text_input("Publico objetivo", placeholder="Ej: familias, jovenes, oficinas, turistas...", help="Opcional. Ayuda a la IA a personalizar el tono de tu web.", key="ck_publico")

    # UBICACION
    st.divider()
    st.markdown(f"### {E_PIN} Ubicacion")
    col5, col6 = st.columns(2)
    with col5:
        ciudad = st.text_input("Ciudad *", placeholder="Ej: Bogota", key="ck_ciudad")
    with col6:
        nombres_paises = obtener_nombres()
        idx_default = nombres_paises.index(PAISES_DEFAULT) if PAISES_DEFAULT in nombres_paises else 0
        pais_sel = st.selectbox(f"{E_GLOBO} Pais *", nombres_paises, index=idx_default, help="El prefijo del WhatsApp se ajusta automaticamente.", key="ck_pais")

    prefijo_pais = obtener_prefijo(pais_sel)
    direccion = st.text_input("Direccion fisica", placeholder="Ej: Calle 123 #45-67, Barrio Centro", help="Opcional. Si tenes local fisico, aparece un mapa en tu web.", key="ck_direccion")

    # CONTACTO DEL NEGOCIO
    st.divider()
    st.markdown(f"### {E_CHAT} Contacto del negocio")
    st.info(f"{E_GLOBO} **Prefijo automatico:** `{prefijo_pais}` (pais seleccionado: {pais_sel})")

    col7, col8 = st.columns(2)
    with col7:
        whatsapp_negocio = st.text_input(f"WhatsApp del negocio (prefijo {prefijo_pais})", placeholder="Ej: 300 123 4567", help=f"Se agregara el prefijo {prefijo_pais} automaticamente.", key="ck_whatsapp")
    with col8:
        email_contacto = st.text_input("Email del negocio", placeholder="Ej: contacto@minegocio.com", key="ck_email_contacto")

    horarios = st.text_input("Horarios de atencion", placeholder="Ej: Lun-Vie 8am-6pm, Sab 9am-1pm", key="ck_horarios")

    # REDES SOCIALES
    st.divider()
    st.markdown("### Redes sociales")
    col9, col10, col11 = st.columns(3)
    with col9:
        instagram = st.text_input("Instagram", placeholder="@minegocio", key="ck_instagram")
    with col10:
        facebook = st.text_input("Facebook", placeholder="minegocio", key="ck_facebook")
    with col11:
        tiktok = st.text_input("TikTok", placeholder="@minegocio", key="ck_tiktok")

    anio_fundacion = st.text_input("Año de fundación", placeholder="Ej: 2018", key="ck_anio")

    # FOTOS Y LOGO (ARREGLADO PARA EVITAR EL LOOP)
    st.divider()
    st.markdown(f"### {E_CAMARA} Fotos de tu negocio (Opcional)")
    st.caption("Sube tu logo y hasta 3 fotos de tus productos. Máximo 5MB por archivo.")
    
    logo_b64 = None
    fotos_b64 = []

    col_img1, col_img2 = st.columns(2)
    with col_img1:
        logo_file = st.file_uploader("Sube tu Logo (PNG o JPG)", type=["png", "jpg", "jpeg"], key="ck_logo")
        if logo_file:
            es_valido, msg = validar_imagen_subida(logo_file)
            if not es_valido:
                st.error(msg)
                # NO seteamos logo_file = None para no causar el loop.
            else:
                logo_b64 = _procesar_imagen_subida(logo_file)

    with col_img2:
        fotos_files = st.file_uploader("Sube hasta 3 fotos (PNG o JPG)", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="ck_fotos")
        if fotos_files:
            for f in fotos_files:
                es_valido, msg = validar_imagen_subida(f)
                if not es_valido:
                    st.error(f"{f.name}: {msg}")
                else:
                    fotos_b64.append(_procesar_imagen_subida(f))

    # BLOQUE LEGAL
    st.divider()
    st.markdown("### ⚖️ Términos y Privacidad")
    st.caption("Para continuar, debes aceptar nuestras políticas de tratamiento de datos.")
    
    leyes_por_pais = {
        "Colombia": "Ley 1581 de 2012",
        "México": "LFPDPPP (Ley Federal de Protección de Datos Personales)",
        "Perú": "Ley 29733 de Protección de Datos Personales",
        "Chile": "Ley 19.628 sobre Protección de la Vida Privada",
    }
    ley_local = leyes_por_pais.get(pais_sel, "las normativas locales vigentes de Protección de Datos Personales")
    
    acepta_terminos = st.checkbox(f"Acepto los Términos y Condiciones y autorizo el Tratamiento de mis Datos Personales según la {ley_local} y la política completa de SAMU IA.", key="ck_acepta_legal")
    
    with st.expander("Ver resumen de la Política de Privacidad"):
        st.markdown(f"""
        *   **SAMU IA** usará tus datos personales solo para crear tu sitio web, gestionar tu cuenta, prestar el servicio ARM y enviar soporte relacionado con el servicio contratado.
        *   **Cuando contrates Web Premium Plus y actives el ARM:** las conversaciones recibidas por WhatsApp serán transferidas internacionalmente y procesadas por los modelos de IA (Groq, OpenRouter, Gemini).
        *   **SAMU IA NO es responsable del consentimiento** que tú debes obtener de tus propios clientes.
        *   Tienes derecho a acceder, rectificar, cancelar u oponerte (Derechos ARCO) escribiendo a soporte@samu-ia.com.
        """)

    # BOTON CONFIRMAR
    st.divider()
    st.caption("* Campos obligatorios")

    if st.button(f"{E_OK} Confirmar compra - {tier['precio_label']}", width="stretch", type="primary", key="ck_btn_confirmar", disabled=not acepta_terminos):
        if sector_sel == "Otro (especificar abajo)":
            sector_final = sector_otro.strip()
        else:
            sector_final = sector_sel

        datos_form = {
            "nombre": nombre, "email": email, "telefono": telefono,
            "nombre_negocio": nombre_negocio, "sector": sector_final,
            "descripcion": descripcion, "publico_objetivo": publico_objetivo,
            "ciudad": ciudad, "pais": pais_sel, "direccion": direccion,
            "whatsapp_negocio": whatsapp_negocio, "email_contacto": email_contacto,
            "horarios": horarios, "instagram": instagram,
            "facebook": facebook, "tiktok": tiktok,
            "anio_fundacion": anio_fundacion,
            "logo_b64": logo_b64,
            "fotos_b64": fotos_b64,
            "ley_aceptada": ley_local
        }

        errores = validar_formulario(datos_form, sector_sel, sector_otro)

        if errores:
            st.error(f"{E_AVISO} Revisa: " + " . ".join(errores))
        else:
            faltantes = calcular_faltantes(datos_form)
            if faltantes:
                st.session_state["_checkout_datos_pendientes"] = datos_form
                st.session_state["_checkout_tier_actual"] = tier
                st.session_state["_checkout_faltantes"] = faltantes
                st.session_state["_checkout_confirmando"] = True
                st.rerun()
            else:
                crear_pedido_y_avanzar(datos_form, tier)

    # DIALOGO DE CONFIRMACION
    if st.session_state.get("_checkout_confirmando", False):
        faltantes = st.session_state.get("_checkout_faltantes", [])
        st.divider()
        st.warning(f"{E_AVISO} **Faltan estos campos opcionales:**\n\n" + "\n".join([f"- {f}" for f in faltantes]))
        st.info("Podes continuar sin estos datos o volver a completarlos. La IA completara lo que falte con contenido generico.")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            if st.button(f"{E_OK} Continuar sin estos campos", type="primary", width="stretch", key="btn_continuar_sin_opc"):
                datos = st.session_state.get("_checkout_datos_pendientes", {})
                tier_actual = st.session_state.get("_checkout_tier_actual", tier)
                crear_pedido_y_avanzar(datos, tier_actual)
        with col_c2:
            if st.button(f"{E_FLECHA} Volver y completar", width="stretch", key="btn_volver_completar"):
                st.session_state.pop("_checkout_confirmando", None)
                st.session_state.pop("_checkout_faltantes", None)
                st.rerun()

    st.divider()
    if st.button(f"{E_FLECHA} Volver al inicio", key="volver_form"):
        limpiar_estado_checkout()


def _renderizar_instrucciones():
    datos = st.session_state.get("_web_pedido_creado", {})
    pedido = datos.get("pedido") or {}
    tier = datos.get("tier") or {}
    if not pedido or not tier:
        st.error("Datos del pedido no encontrados.")
        if st.button("Volver al inicio"): limpiar_estado_checkout()
        return
    st.markdown(f"# {E_OK} Pedido registrado")
    st.markdown(f"**Pedido ID:** `{pedido.get('id', '?')}`")
    st.markdown(f"**Plan:** {tier['nombre']} - {tier['precio_label']}")
    st.divider()
    if obtener_proveedor and proveedor_actual:
        datos_pago = datos_pago_desde_config()
        proveedor = obtener_proveedor(proveedor_actual(), datos_pago)
        resultado = proveedor.crear_pago(pedido_id=pedido.get("id", "?"), monto=tier.get("precio", 0), descripcion=f"Web Gancho - {tier['nombre']}")
        st.markdown(f"## {E_DINERO} Como pagar")
        st.info(resultado.get("instrucciones", "Contactanos para mas informacion."))
    else:
        st.info("El proveedor de pagos no esta configurado.")
    st.divider()
    st.markdown(f"## {E_RELOJ} Que sigue?")
    st.markdown("1. Realiza la transferencia.\n2. Envia el comprobante.\n3. Confirmaremos en 24h.\n4. **Recibiras tu web y tu panel.**")
    token = pedido.get("magic_token", "")
    if token:
        st.divider()
        st.markdown(f"## {E_COHETE} Acceso a tu panel")
        try:
            from utils.magic_link import construir_url_panel
            url_panel = construir_url_panel(token)
            st.markdown(f"**Link:** [Abrir mi panel]({url_panel})")
            st.code(url_panel, language=None)
        except Exception: pass
    st.divider()
    st.success(f"{E_CORONA} Recibimos tu pedido. Guarda este ID: `{pedido.get('id', '?')}`")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"{E_DOC} Hacer otro pedido", width="stretch"): limpiar_estado_checkout()
    with col2:
        if st.button(f"{E_FLECHA} Volver al inicio", width="stretch"): limpiar_estado_checkout()

def renderizar():
    if st.session_state.get("_web_pedido_creado"):
        _renderizar_instrucciones()
        return
    tier_id = st.session_state.get("_web_checkout_tier")
    if not tier_id:
        st.warning(f"{E_AVISO} No hay plan seleccionado.")
        if st.button(f"{E_FLECHA} Volver a la landing"):
            st.session_state["_web_subruta"] = "landing"
            st.rerun()
        return
    tier = next((t for t in D.TIERS if t["id"] == tier_id), None)
    if not tier:
        st.error(f"{E_X} Plan no encontrado: {tier_id}")
        if st.button(f"{E_FLECHA} Volver a la landing"):
            st.session_state["_web_subruta"] = "landing"
            st.rerun()
        return
    _renderizar_formulario(tier)