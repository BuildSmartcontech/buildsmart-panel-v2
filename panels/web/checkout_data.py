# panels/web/checkout_data.py
# ============================================
# DATOS Y PERSISTENCIA DEL CHECKOUT
# ============================================
# V1.0: Extraido de checkout.py (split 400 lineas)
# ============================================

import datetime
import streamlit as st
from utils.paises import PAISES_DEFAULT, obtener_prefijo
from panels.web.checkout_validators import (
    normalizar_whatsapp,
    normalizar_instagram,
)


TIER_NUM = {"tier1": 1, "tier2": 2, "tier3": 3}


def _get_supabase():
    try:
        from utils.supabase_rest import supabase_rest
        return supabase_rest if supabase_rest.disponible else None
    except Exception:
        return None


def datos_pago_desde_config():
    """Lee los datos de pago desde config_global."""
    try:
        from utils.config_global import obtener
        return {
            "nequi": obtener("pago_nequi", ""),
            "daviplata": obtener("pago_daviplata", ""),
            "bancolombia_ahorros": obtener("pago_bancolombia_ahorros", ""),
            "titular": obtener("pago_titular", ""),
            "email_comprobante": obtener("pago_email_comprobante", ""),
        }
    except Exception as e:
        print(f"[checkout_data] Error leyendo config: {e}")
        return {}


def guardar_pedido(datos_form, tier):
    """Crea el pedido en pedidos_web + genera magic token."""
    sb = _get_supabase()
    if not sb:
        return None, "Supabase no disponible"

    try:
        pais = datos_form.get("pais", PAISES_DEFAULT)
        prefijo = obtener_prefijo(pais)

        datos_negocio = {
            "nombre_negocio": datos_form["nombre_negocio"].strip()[:200],
            "sector":         datos_form["sector"].strip()[:100],
            "descripcion":    datos_form["descripcion"].strip()[:1500],
            "ciudad":         datos_form["ciudad"].strip()[:100],
            "pais":           pais,
        }

        if datos_form.get("whatsapp_negocio", "").strip():
            wa_norm = normalizar_whatsapp(datos_form["whatsapp_negocio"], prefijo)
            datos_negocio["whatsapp_negocio"] = wa_norm
            datos_negocio["telefono_negocio"] = wa_norm

        opcionales = {
            "email_contacto":   datos_form.get("email_contacto", ""),
            "direccion":        datos_form.get("direccion", ""),
            "horarios":         datos_form.get("horarios", ""),
            "instagram":        datos_form.get("instagram", ""),
            "facebook":         datos_form.get("facebook", ""),
            "tiktok":           datos_form.get("tiktok", ""),
            "anio_fundacion":   datos_form.get("anio_fundacion", ""),
            "publico_objetivo": datos_form.get("publico_objetivo", ""),
        }

        for k, v in opcionales.items():
            if v and str(v).strip():
                if k == "instagram":
                    datos_negocio[k] = normalizar_instagram(v)
                else:
                    datos_negocio[k] = str(v).strip()[:200]

        payload = {
            "email":          datos_form["email"].strip()[:200],
            "nombre_cliente": datos_form["nombre"].strip()[:200],
            "telefono":       (datos_form.get("telefono") or "").strip()[:50] or None,
            "tier":           TIER_NUM.get(tier["id"], 1),
            "precio_usd":     float(tier["precio"]),
            "estado":         "pendiente_pago_manual",
            "datos_negocio":  datos_negocio,
            "created_at":     datetime.datetime.now().isoformat(),
            "updated_at":     datetime.datetime.now().isoformat(),
        }

        r = sb.insert("pedidos_web", payload)
        if r.error:
            return None, str(r.error)

        pedido = r.data[0] if r.data else None
        if not pedido:
            return None, "No se pudo crear el pedido"

        try:
            from utils.magic_link import asignar_token_al_pedido
            ok_token, token, err = asignar_token_al_pedido(sb, pedido.get("id"))
            if ok_token:
                pedido["magic_token"] = token
                print(f"[checkout_data] Token generado: {pedido.get('id')}")
        except Exception as e:
            print(f"[checkout_data] Error magic_link: {e}")

        return pedido, None
    except Exception as e:
        return None, str(e)


def enviar_email_confirmacion(pedido, tier):
    """Envia email al cliente con link al panel."""
    try:
        from utils.email_sender import email_sender
    except ImportError:
        return False, "email_sender no disponible"

    if not email_sender.disponible:
        return False, "Email no configurado"

    email = pedido.get("email", "")
    nombre = pedido.get("nombre_cliente", "Cliente")
    token = pedido.get("magic_token", "")
    pedido_id = pedido.get("id", "?")

    panel_url = ""
    if token:
        try:
            from utils.magic_link import construir_url_panel
            panel_url = construir_url_panel(token)
        except Exception:
            pass

    asunto = f"Confirmamos tu pedido - {tier['nombre']}"

    contenido = f"""Hola {nombre},

Recibimos tu pedido de web. Gracias por confiar en SAMU IA.

Resumen del pedido:
- Plan: {tier['nombre']} - {tier['precio_label']}
- ID del pedido: {pedido_id}

PROXIMOS PASOS:
1. Realiza el pago con los datos que se muestran en la pantalla
2. Envia el comprobante por email
3. Confirmaremos el pago en menos de 24 horas
4. Recibiras otro email cuando tu web este lista

TU PANEL DE CLIENTE:
{panel_url if panel_url else "(El link estara disponible en proximo email)"}

Cualquier consulta, responde a este email.

Saludos,
El equipo de SAMU IA
"""

    try:
        resultado = email_sender.enviar_correo(email, asunto, contenido)
        print(f"[checkout_data] Email confirmacion: {resultado}")
        return "OK" in resultado, resultado
    except Exception as e:
        return False, str(e)[:200]


def crear_pedido_y_avanzar(datos_form, tier):
    """Crea el pedido + envia email + actualiza session_state."""
    with st.spinner("Creando tu pedido..."):
        pedido, error = guardar_pedido(datos_form, tier)

    if error:
        st.error(f"Error creando pedido: {error}")
        return

    with st.spinner("Enviando email de confirmacion..."):
        enviar_email_confirmacion(pedido, tier)

    for k in ["_checkout_confirmando", "_checkout_faltantes",
              "_checkout_datos_pendientes", "_checkout_tier_actual"]:
        st.session_state.pop(k, None)

    st.session_state["_web_pedido_creado"] = {"pedido": pedido, "tier": tier}
    st.rerun()


def limpiar_estado_checkout():
    """Limpia todos los estados del checkout."""
    for k in ["_web_checkout_tier", "_web_pedido_creado",
              "_checkout_confirmando", "_checkout_faltantes",
              "_checkout_datos_pendientes", "_checkout_tier_actual"]:
        st.session_state.pop(k, None)
    for k in list(st.session_state.keys()):
        if k.startswith("ck_"):
            st.session_state.pop(k, None)
    st.rerun()