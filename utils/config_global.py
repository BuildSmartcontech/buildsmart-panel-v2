# utils/config_global.py
# ============================================
# LECTOR DE CONFIG GLOBAL - SAMU IA V1.1
# ============================================

import os
import sys
import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

_CACHE = {"data": None, "timestamp": 0}
_CACHE_TTL = 60

def _get_supabase():
    """Obtiene cliente Supabase de forma defensiva. Atrapa el KeyError de Secrets."""
    try:
        from utils.supabase_rest import supabase_rest
        if supabase_rest.disponible:
            return supabase_rest
    except Exception as e:
        print(f"[config_global] Supabase no disponible (posible falta de Secrets): {e}")
        pass
    return None

def cargar_config(forzar=False):
    import time
    ahora = time.time()

    if not forzar and _CACHE["data"] is not None:
        if (ahora - _CACHE["timestamp"]) < _CACHE_TTL:
            return _CACHE["data"]

    sb = _get_supabase()
    if sb is None:
        return _CACHE["data"] or {}

    try:
        rows = sb.table("config_global").select("*").execute().data or []
        config = {}
        for row in rows:
            clave = row.get("clave")
            valor = row.get("valor")
            if clave:
                if isinstance(valor, str):
                    try:
                        config[clave] = json.loads(valor)
                    except Exception:
                        config[clave] = valor
                else:
                    config[clave] = valor

        _CACHE["data"] = config
        _CACHE["timestamp"] = ahora
        return config
    except Exception as e:
        print(f"[config_global] Error cargando tabla: {e}")
        return _CACHE["data"] or {}

def obtener(clave, default=None):
    config = cargar_config()
    return config.get(clave, default)

def invalidar_cache():
    _CACHE["data"] = None
    _CACHE["timestamp"] = 0

def recargar():
    invalidar_cache()
    return cargar_config(forzar=True)