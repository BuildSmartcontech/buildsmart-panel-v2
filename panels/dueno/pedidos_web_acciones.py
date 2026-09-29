# panels/dueno/pedidos_web_acciones.py
# ============================================
# ACCIONES DE PEDIDOS WEB - SAMU IA
# ============================================
# V3.1: Inyecta botones WhatsApp/Tel/Email (lee telefono + nombre del pedido)
# V3.0: Inyecta formulario de leads antes de publicar (G11)
# V2.0: Envia email automatico al cliente (G8)
# V1.0: Genera web desde pedido
# ============================================

import datetime
import json as _json
from pathlib import Path


def _log_evento(pedido_id, tipo, detalle=None):
    """Registra accion en eventos_app."""
    try:
        from utils.logger import log_evento as _log
        payload = {"pedido_id": pedido_id, "origen": "pedidos_web_acciones"}
        if detalle:
            payload.update(detalle)
        _log(tipo, detalle=payload)
    except Exception:
        pass


def _actualizar_pedido(sb, pedido_id, campos):
    """Actualiza campos del pedido."""
    try:
        campos["updated_at"] = datetime.datetime.now().isoformat()
        sb.update("pedidos_web", campos, "id", pedido_id)
        return True
    except Exception as e:
        print(f"[pedidos_web_acciones] Error actualizando: {e}")
        return False


def _inyectar_formulario(usuario_id, web_id, pedido_id):
    """
    Inyecta botones WhatsApp/Tel/Email + formulario de leads.
    Lee telefono + nombre_negocio del pedido en Supabase.

    Returns:
        tuple: (exito: bool, mensaje: str)
    """
    try:
        from utils.formulario_leads import inyectar_formulario_leads
    except ImportError as e:
        return False, f"Modulo formulario_leads no disponible: {e}"

    # ==========================================
    # Obtener datos del pedido (telefono + nombre negocio)
    # ==========================================
    telefono = None
    nombre_negocio = None
    try:
        from utils.supabase_rest import supabase_rest
        r = supabase_rest.table("pedidos_web").select("telefono, datos_negocio").eq("id", pedido_id).execute()
        if r.data:
            p = r.data[0]
            telefono = p.get("telefono")
            datos = p.get("datos_negocio") or {}
            if isinstance(datos, str):
                try:
                    datos = _json.loads(datos)
                except Exception:
                    datos = {}
            # Telefono del negocio tiene prioridad sobre el del cliente
            tel_negocio = datos.get("telefono_negocio") or datos.get("whatsapp")
            if tel_negocio:
                telefono = tel_negocio
            nombre_negocio = datos.get("nombre_negocio")
        print(f"[pedidos_web_acciones] Datos: tel={telefono}, negocio={nombre_negocio}")
    except Exception as e:
        print(f"[pedidos_web_acciones] Sin datos del negocio: {e}")

    # Ruta del HTML generado
    ruta = Path("data") / "webs_generadas" / usuario_id / str(web_id) / "index.html"

    if not ruta.exists():
        return False, f"HTML no encontrado en: {ruta}"

    try:
        html_original = ruta.read_text(encoding="utf-8")
        html_nuevo = inyectar_formulario_leads(
            html_original,
            pedido_id,
            telefono_negocio=telefono,
            nombre_negocio=nombre_negocio,
        )

        if html_nuevo == html_original:
            return False, "El formulario no se inyecto (no cambio el HTML)"

        ruta.write_text(html_nuevo, encoding="utf-8")
        print(f"[pedidos_web_acciones] Formulario inyectado en {ruta}")
        return True, f"Formulario inyectado (+{len(html_nuevo) - len(html_original)} chars)"

    except Exception as e:
        return False, f"Error inyectando: {str(e)[:200]}"


def _enviar_email_entrega(pedido, url_publica):
    """Envia email de entrega al cliente."""
    try:
        from utils.email_pedidos import enviar_email_entrega
    except ImportError as e:
        return False, f"Modulo email no disponible: {e}"

    pedido_email = dict(pedido)
    pedido_email["web_url"] = url_publica

    try:
        return enviar_email_entrega(pedido_email)
    except Exception as e:
        return False, f"Error enviando email: {str(e)[:200]}"


def generar_web_para_pedido(sb, pedido):
    """
    Genera una web completa para un pedido de Web Gancho.

    Flujo:
    1. Extrae datos del negocio del pedido
    2. Llama a crear_web() con IA
    3. Inyecta formulario + botones WhatsApp/Tel/Email (G11)
    4. Publica via ProviderManager (Vercel/Cloudflare/Local)
    5. Actualiza pedido + envia email automatico al cliente

    Returns:
        dict con exito, mensaje, url_publica, email_enviado, email_mensaje
    """
    pedido_id = pedido.get("id", "?")
    datos = pedido.get("datos_negocio") or {}
    tier = pedido.get("tier", 1)

    if isinstance(datos, str):
        try:
            datos = _json.loads(datos)
        except Exception:
            datos = {}

    if not datos or not datos.get("nombre_negocio"):
        return {
            "exito": False,
            "mensaje": "El pedido no tiene datos de negocio.",
            "url_publica": None,
            "email_enviado": False,
            "email_mensaje": "",
        }

    nombre = datos.get("nombre_negocio", "Mi Negocio")
    sector = datos.get("sector", "General")
    descripcion = datos.get("descripcion", "")

    usuario_id = f"pedido_{pedido_id[:8]}"

    datos_negocio = {
        "nombre": nombre,
        "sector": sector,
        "descripcion": descripcion,
        "publico_objetivo": "Clientes potenciales",
        "diferenciadores": "Calidad y dedicacion",
    }

    opciones = {
        "tipo_pagina": "Landing Page",
        "diseno": "Moderno",
        "tono": "Profesional",
        "sector": sector,
    }

    _log_evento(pedido_id, "web_generacion_iniciada", {
        "nombre": nombre, "sector": sector, "tier": tier,
    })

    # ==========================================
    # PASO 1: Crear web con IA
    # ==========================================
    try:
        from utils.web_module import crear_web
    except ImportError as e:
        return {
            "exito": False,
            "mensaje": f"Modulo web_module no disponible: {e}",
            "url_publica": None,
            "email_enviado": False,
            "email_mensaje": "",
        }

    try:
        print(f"[pedidos_web_acciones] Generando web para pedido {pedido_id}...")
        resultado = crear_web(usuario_id, datos_negocio, opciones)
    except Exception as e:
        _log_evento(pedido_id, "web_generacion_error", {"error": str(e)[:200]})
        return {
            "exito": False,
            "mensaje": f"Error creando web: {str(e)[:200]}",
            "url_publica": None,
            "email_enviado": False,
            "email_mensaje": "",
        }

    if not resultado or not resultado.get("exito"):
        error = (resultado or {}).get("error", "Desconocido")
        _log_evento(pedido_id, "web_generacion_fallida", {"error": str(error)[:200]})
        return {
            "exito": False,
            "mensaje": f"Error en generacion: {error}",
            "url_publica": None,
            "email_enviado": False,
            "email_mensaje": "",
        }

    web_id = resultado.get("web_id")
    print(f"[pedidos_web_acciones] Web generada: {web_id}")

    # ==========================================
    # PASO 1.5: Inyectar formulario + botones contacto (G11)
    # ==========================================
    form_ok, form_msg = _inyectar_formulario(usuario_id, web_id, pedido_id)
    print(f"[pedidos_web_acciones] Formulario: {form_msg}")

    if form_ok:
        _log_evento(pedido_id, "formulario_inyectado", {"web_id": web_id})
    else:
        _log_evento(pedido_id, "formulario_error", {"error": form_msg[:200]})

    # ==========================================
    # PASO 2: Publicar via ProviderManager (Vercel/Cloudflare)
    # ==========================================
    try:
        from utils.web_publisher import publicar_web
    except ImportError as e:
        _log_evento(pedido_id, "web_publicacion_error", {"error": str(e)[:200], "web_id": web_id})
        _actualizar_pedido(sb, pedido_id, {"web_id": web_id})
        return {
            "exito": False,
            "mensaje": f"Web generada pero modulo de publicacion no disponible: {e}",
            "url_publica": None,
            "email_enviado": False,
            "email_mensaje": "",
        }

    try:
        print(f"[pedidos_web_acciones] Publicando {web_id}...")
        resultado_pub = publicar_web(usuario_id, web_id)
    except Exception as e:
        _log_evento(pedido_id, "web_publicacion_error", {"error": str(e)[:200], "web_id": web_id})
        _actualizar_pedido(sb, pedido_id, {"web_id": web_id})
        return {
            "exito": False,
            "mensaje": f"Web generada pero fallo publicacion: {str(e)[:200]}",
            "url_publica": None,
            "email_enviado": False,
            "email_mensaje": "",
        }

    if not resultado_pub or not resultado_pub.get("exito"):
        error = (resultado_pub or {}).get("error", "Desconocido")
        _log_evento(pedido_id, "web_publicacion_fallida", {"error": str(error)[:200], "web_id": web_id})
        _actualizar_pedido(sb, pedido_id, {"web_id": web_id})
        return {
            "exito": False,
            "mensaje": f"Web generada pero fallo publicacion: {error}",
            "url_publica": None,
            "email_enviado": False,
            "email_mensaje": "",
        }

    url_publica = resultado_pub.get("url_publica", "")
    proveedor = resultado_pub.get("tipo", "?")
    print(f"[pedidos_web_acciones] Publicada en {proveedor}: {url_publica}")

    # ==========================================
    # PASO 3: Actualizar pedido
    # ==========================================
    _actualizar_pedido(sb, pedido_id, {
        "web_id": web_id,
        "web_url": url_publica,
        "estado": "entregado",
        "entregado_at": datetime.datetime.now().isoformat(),
    })

    _log_evento(pedido_id, "web_entregada", {
        "web_id": web_id,
        "url": url_publica,
        "proveedor": proveedor,
        "formulario_ok": form_ok,
    })

    # ==========================================
    # PASO 4: Enviar email al cliente
    # ==========================================
    email_enviado = False
    email_msg = ""

    if url_publica:
        try:
            email_enviado, email_msg = _enviar_email_entrega(pedido, url_publica)

            if email_enviado:
                _log_evento(pedido_id, "email_entrega_enviado", {"email": pedido.get("email")})
                print(f"[pedidos_web_acciones] Email enviado a {pedido.get('email')}")
            else:
                _log_evento(pedido_id, "email_entrega_error", {"error": email_msg[:200]})
                print(f"[pedidos_web_acciones] Email fallo: {email_msg}")
        except Exception as e:
            email_msg = f"Excepcion enviando email: {str(e)[:200]}"
            print(f"[pedidos_web_acciones] {email_msg}")
    else:
        email_msg = "No hay URL publica, email omitido"

    msg_final = f"Web generada y publicada en {proveedor}."
    if not form_ok:
        msg_final += f" (aviso: formulario no inyectado: {form_msg[:80]})"

    return {
        "exito": True,
        "mensaje": msg_final,
        "url_publica": url_publica,
        "email_enviado": email_enviado,
        "email_mensaje": email_msg,
    }


# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    print("=" * 60)
    print("TEST PEDIDOS WEB ACCIONES V3.1")
    print("=" * 60)
    print("Cambios V3.1:")
    print("  - Inyecta botones WhatsApp/Tel/Email")
    print("  - Lee telefono + nombre del pedido en Supabase")
    print("  - Publica via ProviderManager (Vercel/Cloudflare)")
    print("=" * 60)