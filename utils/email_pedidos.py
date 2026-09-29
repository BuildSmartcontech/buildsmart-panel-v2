# utils/email_pedidos.py
# ============================================
# EMAILS DE PEDIDOS WEB - SAMU IA
# ============================================
# V2.0: Incluye link al panel del cliente en email de entrega
# V1.0: Templates base
# ============================================

import datetime


# ==========================================
# CONSTANTES
# ==========================================
TIER_LABELS = {
    1: "Premium Esencial",
    2: "Premium + CRM",
    3: "Premium Plus",
}


# ==========================================
# HELPERS
# ==========================================
def _construir_link_panel(pedido):
    """Construye el link al panel del cliente si hay token."""
    token = pedido.get("magic_token", "")
    if not token:
        return ""

    try:
        from utils.magic_link import construir_url_panel
        return construir_url_panel(token)
    except Exception as e:
        print(f"[email_pedidos] Error construyendo link: {e}")
        return ""


def _seccion_panel(pedido):
    """Seccion de acceso al panel (si hay token)."""
    url_panel = _construir_link_panel(pedido)
    if not url_panel:
        return ""

    return f"""
TU PANEL DE CLIENTE
{url_panel}

Desde tu panel vas a poder:
- Ver el estado de tu web
- Compartir la URL con tus clientes
- Ver los leads capturados (si tenes CRM)
- Ver informacion de renovacion
"""


# ==========================================
# TEMPLATES
# ==========================================
def _template_entrega(pedido, url_web):
    """Genera el cuerpo del email de entrega."""
    datos = pedido.get("datos_negocio") or {}
    nombre = pedido.get("nombre_cliente") or "Cliente"
    nombre_negocio = datos.get("nombre_negocio", "tu negocio")
    tier_num = pedido.get("tier", 1)
    tier_label = TIER_LABELS.get(tier_num, "Premium")
    panel = _seccion_panel(pedido)

    return f"""Hola {nombre},

Tu web esta lista y publicada!

URL publica:
{url_web}

Resumen de tu pedido:
- Plan: {tier_label}
- Negocio: {nombre_negocio}
- ID del pedido: {pedido.get('id', '?')}
- Fecha de entrega: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}

Que podes hacer ahora:
1. Abri la URL para ver tu web
2. Comparti el link con tus clientes
3. Si contrataste CRM, en breve te enviamos acceso al panel
{panel}
RENOVACION:
Tu web incluye hosting gratis por 1 año. En 12 meses vas a poder:
- Renovar por USD 59/año (o USD 79 con dominio propio)
- Descargar el HTML y llevartela
- Actualizar al plan PIME (USD 99/mes) para gestion completa

Cualquier consulta, responde a este email.

Saludos,
El equipo de SAMU IA
"""


def _template_rechazo(pedido, motivo=""):
    """Genera el cuerpo del email de rechazo."""
    nombre = pedido.get("nombre_cliente") or "Cliente"
    return f"""Hola {nombre},

Lamentablemente no pudimos procesar tu pedido.

Motivo: {motivo or "El pago no pudo ser confirmado"}

Que podes hacer:
1. Verificar los datos de pago
2. Realizar una nueva compra desde nuestra landing
3. Contactarnos respondiendo a este email

Disculpas por las molestias.

Saludos,
El equipo de SAMU IA
"""


# ==========================================
# ENVIO DE EMAILS
# ==========================================
def _cargar_email_sender():
    """Carga el modulo de email de forma defensiva."""
    try:
        from utils.email_sender import email_sender
        return email_sender
    except ImportError:
        print("[email_pedidos] email_sender no disponible")
        return None


def enviar_email_entrega(pedido):
    """
    Envia email de entrega al cliente.

    Args:
        pedido (dict): Debe tener 'email', 'web_url', 'datos_negocio'.
            Opcionalmente 'magic_token' para incluir link al panel.

    Returns:
        tuple: (exito: bool, mensaje: str)
    """
    email = pedido.get("email")
    if not email:
        return False, "El pedido no tiene email"

    url = pedido.get("web_url")
    if not url:
        return False, "El pedido no tiene web_url"

    sender = _cargar_email_sender()
    if sender is None:
        return False, "Modulo email_sender no disponible"

    asunto = "Tu web esta lista - SAMU IA"
    contenido = _template_entrega(pedido, url)

    try:
        resultado = sender.enviar_correo(email, asunto, contenido)
        print(f"[email_pedidos] Email de entrega: {resultado[:100]}")
        return "OK" in resultado, resultado
    except Exception as e:
        print(f"[email_pedidos] Error enviando email: {e}")
        return False, f"Error enviando email: {str(e)[:200]}"


def enviar_email_rechazo(pedido, motivo=""):
    """Envia email de rechazo al cliente."""
    email = pedido.get("email")
    if not email:
        return False, "El pedido no tiene email"

    sender = _cargar_email_sender()
    if sender is None:
        return False, "Modulo email_sender no disponible"

    asunto = "Pedido no procesado - SAMU IA"
    contenido = _template_rechazo(pedido, motivo)

    try:
        resultado = sender.enviar_correo(email, asunto, contenido)
        return "OK" in resultado, resultado
    except Exception as e:
        return False, f"Error enviando email: {str(e)[:200]}"


# ==========================================
# TEST MANUAL
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print("TEST EMAIL PEDIDOS V2.0")
    print("=" * 60)

    pedido_test = {
        "id": "test_pedido_123",
        "email": "test@ejemplo.com",
        "nombre_cliente": "Juan Test",
        "tier": 2,
        "web_url": "https://buildsmart-webs.netlify.app/test/demo/",
        "magic_token": "abc123def456",
        "datos_negocio": {
            "nombre_negocio": "Panaderia Test",
            "sector": "alimentos",
            "descripcion": "Panaderia artesanal",
        },
    }

    print("\nTemplate de entrega (primeros 600 chars):")
    print("-" * 60)
    t = _template_entrega(pedido_test, pedido_test["web_url"])
    print(t[:600])
    print("-" * 60)
    print(f"\nLongitud total: {len(t)} chars")
    print(f"Tiene link al panel: {'SI' if 'TU PANEL DE CLIENTE' in t else 'NO'}")
    print("=" * 60)