# utils/config_global.py
# ============================================
# LECTOR DE CONFIG GLOBAL - SAMU IA
# ============================================
# Lee la tabla config_global de Supabase.
# Permite que panel_dueno cambie valores en vivo
# sin tener que tocar codigo.
# ============================================

import os
import sys
import json
from pathlib import Path

# Bootstrap de path (para correr standalone)
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


# Cache global del modulo
_CACHE = {
    "data": None,
    "timestamp": 0,
}

# TTL de cache en segundos (60 = 1 minuto)
_CACHE_TTL = 60


def _get_supabase():
    """Obtiene cliente Supabase de forma defensiva."""
    try:
        from utils.supabase_rest import supabase_rest
        if supabase_rest.disponible:
            return supabase_rest
    except Exception:
        pass
    return None


def cargar_config(forzar=False):
    """
    Carga TODA la config de Supabase.
    Con cache de 60s para no re-consultar en cada rerun.

    Returns:
        dict: {clave: valor}
    """
    import time

    ahora = time.time()

    # Devolver cache si esta fresca y no se fuerza recarga
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
                # El valor viene como JSONB (puede ser dict, list, str, num, bool)
                # Si viene como string JSON, intentar parsear
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
        print(f"[config_global] Error cargando: {e}")
        return _CACHE["data"] or {}


def obtener(clave, default=None):
    """Obtiene UNA clave de la config."""
    config = cargar_config()
    return config.get(clave, default)


def invalidar_cache():
    """Fuerza que la proxima llamada relea de Supabase."""
    _CACHE["data"] = None
    _CACHE["timestamp"] = 0


def recargar():
    """Invalida cache y relee inmediatamente."""
    invalidar_cache()
    return cargar_config(forzar=True)


# ==========================================
# TEST MANUAL
# ==========================================
if __name__ == "__main__":
    print("=" * 70)
    print("TEST CONFIG GLOBAL")
    print("=" * 70)
    config = cargar_config(forzar=True)
    if not config:
        print("No se pudo cargar la config (revisa Supabase)")
    else:
        print(f"Total claves: {len(config)}")
        for k in sorted(config.keys()):
            v = config[k]
            print(f"  {k:35s} = {repr(v)}")
    print("=" * 70)