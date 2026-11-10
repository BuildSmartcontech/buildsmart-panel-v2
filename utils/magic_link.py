# utils/magic_link.py
# ============================================
# MAGIC LINK PARA CLIENTES WEB GANCHO - SAMU IA
# ============================================
# V1.1: Detecta la URL base desde variables de entorno o usa samu-ia.com por defecto.
# ============================================

import os
import secrets
import datetime
from datetime import timezone


DIAS_EXPIRACION = 30


# ==========================================
# GENERACION
# ==========================================
def generar_token():
    """Genera un token aleatorio seguro (64 chars hex)."""
    return secrets.token_hex(32)


def generar_expiracion(dias=DIAS_EXPIRACION):
    """Devuelve la fecha de expiracion (UTC)."""
    return (datetime.datetime.now(timezone.utc) +
            datetime.timedelta(days=dias))


# ==========================================
# GUARDADO EN PEDIDO
# ==========================================
def asignar_token_al_pedido(sb, pedido_id):
    token = generar_token()
    expira = generar_expiracion()

    try:
        sb.update(
            "pedidos_web",
            {
                "magic_token": token,
                "magic_token_expira": expira.isoformat(),
                "updated_at": datetime.datetime.now().isoformat(),
            },
            "id",
            pedido_id,
        )
        return True, token, ""
    except Exception as e:
        return False, None, str(e)


def regenerar_token(sb, pedido_id):
    return asignar_token_al_pedido(sb, pedido_id)


# ==========================================
# VALIDACION
# ==========================================
def validar_token(sb, token):
    if not token or not isinstance(token, str):
        return False, None, "Token vacio"

    token = token.strip()
    if len(token) < 32:
        return False, None, "Token invalido"

    try:
        rows = sb.table("pedidos_web").select("*").eq("magic_token", token).execute().data or []
    except Exception as e:
        return False, None, f"Error consultando: {str(e)[:200]}"

    if not rows:
        return False, None, "Token no encontrado"

    pedido = rows[0]

    expira_str = pedido.get("magic_token_expira")
    if expira_str:
        try:
            s = str(expira_str).replace("Z", "")
            if "+" in s and "T" in s:
                base = s.rsplit("+", 1)[0]
                if "." in base:
                    base = base.split(".")[0]
                expira = datetime.datetime.fromisoformat(base)
            else:
                if "." in s:
                    s = s.split(".")[0]
                expira = datetime.datetime.fromisoformat(s)

            ahora = datetime.datetime.now()
            if expira < ahora:
                return False, None, "Token expirado"
        except Exception as e:
            print(f"[magic_link] Error parseando expiracion: {e}")

    return True, pedido, ""


# ==========================================
# URLS
# ==========================================
def construir_url_panel(token, base_url=None):
    """
    Construye la URL del mini-panel.
    Si no se pasa base_url, intenta leer BASE_URL de las variables de entorno.
    Si no existe, usa https://samu-ia.com por defecto.
    """
    if not base_url:
        # Busca en Secrets/Env. Si no está, usa el dominio real.
        base_url = os.getenv("BASE_URL", "https://samu-ia.com")

    # Quitar la barra final si la tiene para evitar dobles barras
    base_url = base_url.rstrip("/")

    return f"{base_url}/?web=panel&token={token}"