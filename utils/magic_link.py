# utils/magic_link.py
# ============================================
# MAGIC LINK PARA CLIENTES WEB GANCHO - SAMU IA
# ============================================
# Genera y valida tokens unicos para acceso
# al mini-panel del cliente.
#
# V1.0: Version inicial
# ============================================

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
    """
    Genera un token y lo guarda en el pedido.

    Returns:
        tuple: (exito: bool, token: str or None, error: str)
    """
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
    """Fuerza la regeneracion del token."""
    return asignar_token_al_pedido(sb, pedido_id)


# ==========================================
# VALIDACION
# ==========================================
def validar_token(sb, token):
    """
    Valida un token y devuelve el pedido asociado.

    Returns:
        tuple: (exito: bool, pedido: dict or None, error: str)
    """
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

    # Verificar expiracion
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
    Construye la URL del mini-panel con el token.

    Args:
        token (str): Token de acceso
        base_url (str, opcional): Base URL. Default: localhost.

    Returns:
        str: URL completa
    """
    if not base_url:
        base_url = "http://localhost:8501"

    return f"{base_url}/?web=panel&token={token}"


# ==========================================
# TEST MANUAL
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print("TEST MAGIC LINK")
    print("=" * 60)

    token = generar_token()
    print(f"Token generado: {token[:16]}... ({len(token)} chars)")

    expira = generar_expiracion()
    print(f"Expira: {expira.isoformat()}")

    url = construir_url_panel(token)
    print(f"URL panel: {url}")

    print()
    print("Validaciones basicas:")
    print(f"  Token vacio: {validar_token(None, '')[2]}")
    print(f"  Token corto: {validar_token(None, 'abc')[2]}")
    print("=" * 60)