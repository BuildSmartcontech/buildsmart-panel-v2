# utils/logger.py
# ============================================
# LOGGER DE EVENTOS - SAMU IA V2.0
# ============================================
# V2.0: Modo SINCRONO (sin thread).
#       El thread anterior moria con Streamlit y
#       los eventos se perdian.
# V1.0: Fire-and-forget con thread daemon
# ============================================

import traceback
import uuid as uuid_lib
from datetime import datetime


# Cache de usuario_id (evita leer archivo cada vez)
_usuario_cache = {"id": None}


def _get_usuario_id():
    """Obtiene el usuario actual desde session_state o archivo local."""
    if _usuario_cache["id"]:
        return _usuario_cache["id"]

    # 1. Intentar session_state (dentro de Streamlit)
    try:
        import streamlit as st
        if hasattr(st, "session_state") and "usuario_id" in st.session_state:
            uid = st.session_state.usuario_id
            if uid:
                _usuario_cache["id"] = uid
                return uid
    except Exception:
        pass

    # 2. Fallback: archivo local
    try:
        import os
        ruta = os.path.join("data", "usuario_actual.txt")
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                uid = f.read().strip()
                if uid:
                    _usuario_cache["id"] = uid
                    return uid
    except Exception:
        pass

    return None


def _safe_uuid(val):
    """Convierte a UUID valido o None. La columna negocio_id es UUID."""
    if not val:
        return None
    try:
        uuid_lib.UUID(str(val))
        return str(val)
    except (ValueError, AttributeError, TypeError):
        return None


def _sanitize_detalle(detalle):
    """Convierte valores no-JSON a strings."""
    if not isinstance(detalle, dict):
        return {"raw": str(detalle)}
    result = {}
    for k, v in detalle.items():
        try:
            import json
            json.dumps({k: v})
            result[k] = v
        except (TypeError, ValueError):
            result[k] = str(v)
    return result


def _escribir(tipo, usuario_id, negocio_id, detalle):
    """Escribe el evento en Supabase (SINCRONO)."""
    try:
        from utils.supabase_rest import supabase_rest
        if not supabase_rest.disponible:
            print(f"[logger] Supabase no disponible, evento '{tipo}' perdido")
            return

        payload = {
            "tipo": str(tipo)[:64],
            "usuario_id": str(usuario_id)[:64] if usuario_id else None,
            "negocio_id": _safe_uuid(negocio_id),
            "detalle": _sanitize_detalle(detalle),
        }

        r = supabase_rest.insert("eventos_app", payload)

        if r.error:
            print(f"[logger] Error insertando '{tipo}': {r.error}")
        else:
            print(f"[logger] Evento '{tipo}' guardado OK")

    except Exception as e:
        print(f"[logger] Excepcion en '{tipo}': {e}")


def log_evento(tipo, usuario_id=None, negocio_id=None, detalle=None):
    """
    Registra un evento en eventos_app (SINCRONO).

    Args:
        tipo (str): 'login', 'crear_negocio', 'generar_web',
                    'modificar_web', 'publicar_web', 'crear_tarea', etc.
        usuario_id (str, opcional): si None, se auto-detecta.
        negocio_id (str, opcional): debe ser UUID valido o se ignora.
        detalle (dict, opcional): info adicional (JSON-serializable).
    """
    uid = usuario_id or _get_usuario_id()
    payload_detalle = dict(detalle) if detalle else {}
    if "ts" not in payload_detalle:
        payload_detalle["ts"] = datetime.now().isoformat()

    _escribir(tipo, uid, negocio_id, payload_detalle)


def log_error(modulo, error, usuario_id=None, negocio_id=None, detalle=None):
    """
    Registra un error en eventos_app.

    Args:
        modulo (str): 'netlify', 'ia', 'supabase', 'web_generator', etc.
        error: Exception o string.
        detalle (dict, opcional): contexto extra.
    """
    payload = {
        "modulo": str(modulo)[:64],
        "error": str(error)[:500],
        "traceback": traceback.format_exc()[:1000],
    }
    if detalle:
        payload.update(detalle)

    log_evento(
        tipo="error",
        usuario_id=usuario_id,
        negocio_id=negocio_id,
        detalle=payload,
    )


# ==========================================
# TEST RAPIDO
# ==========================================
if __name__ == "__main__":
    print("Test logger V2.0 (sincrono) - enviando evento de prueba...")
    log_evento("test_logger_v2", detalle={"origen": "cli", "modo": "sincrono"})
    print("Listo. Revisa la tabla eventos_app en Supabase.")