# utils/salud.py
# ============================================
# CHEQUEO DE SALUD DE APIS - SAMU IA V3.0
# ============================================
# V3.0: Config-driven. Lee config/servicios_monitoreados.json
#       Agregar IA nueva = editar JSON, no tocar codigo.
# V2.0: Bootstrap de path para standalone
# ============================================

import os
import sys
import json
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

# Bootstrap de path (para cuando se corre standalone)
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

TIMEOUT_HTTP = 8
TIMEOUT_BACKEND = 3

RUTA_CONFIG = _ROOT / "config" / "servicios_monitoreados.json"


# ==========================================
# UTILIDADES
# ==========================================
def _get_env(*nombres):
    """Devuelve el primer valor de las env vars que exista."""
    for n in nombres:
        v = os.getenv(n)
        if v:
            return v
    return None


def _cargar_config():
    """Carga el JSON de servicios. Si falla, devuelve dict vacio."""
    try:
        with open(RUTA_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[salud] Error cargando config: {e}")
        return {"servicios": {}}


def _fmt(msg, **kwargs):
    """Aplica formato a un mensaje con placeholders."""
    if not msg:
        return ""
    try:
        return msg.format(**kwargs)
    except Exception:
        return msg


# ==========================================
# CHECKS POR TIPO
# ==========================================
def _check_supabase(cfg, nombre):
    """Check custom para Supabase (usa supabase_rest)."""
    t0 = time.time()
    try:
        from utils.supabase_rest import supabase_rest
        if not supabase_rest.disponible:
            return {
                "ok": False,
                "configurado": False,
                "msg": cfg.get("msg_sin_config", "Faltan credenciales"),
                "ms": 0,
            }
        r = supabase_rest.table("config_global").select("*").limit(1).execute()
        ms = int((time.time() - t0) * 1000)
        if r.error:
            return {"ok": False, "configurado": True, "msg": str(r.error)[:100], "ms": ms}
        count = len(r.data)
        return {
            "ok": True,
            "configurado": True,
            "msg": _fmt(cfg.get("msg_ok", "{count} filas"), count=count),
            "ms": ms,
        }
    except Exception as e:
        return {"ok": False, "configurado": True, "msg": str(e)[:100], "ms": 0}


def _check_http(cfg, nombre):
    """Check generico HTTP. Soporta auth bearer, query_key, header, none."""
    t0 = time.time()

    # Obtener token (si requiere auth)
    auth = cfg.get("auth", "none")
    env_keys = cfg.get("env_keys", [])
    token = None

    if auth != "none":
        token = _get_env(*env_keys) if env_keys else None
        if not token:
            return {
                "ok": False,
                "configurado": False,
                "msg": cfg.get("msg_sin_config", "Faltan credenciales"),
                "ms": 0,
            }

    # Construir URL y headers
    endpoint = cfg.get("endpoint", "")
    headers = {}
    params = {}

    if auth == "bearer":
        headers["Authorization"] = f"Bearer {token}"
    elif auth == "query_key":
        params["key"] = token
    elif auth == "header":
        header_key = cfg.get("header_key", "x-api-key")
        headers[header_key] = token

    # Headers extra
    extra = cfg.get("extra_headers", {})
    if isinstance(extra, dict):
        headers.update(extra)

    # Ejecutar
    try:
        r = requests.get(endpoint, headers=headers, params=params, timeout=TIMEOUT_HTTP)
        ms = int((time.time() - t0) * 1000)

        ok_statuses = cfg.get("ok_statuses", [200])

        if r.status_code in ok_statuses:
            # Extraer valores
            fmt_kwargs = {}

            # Contar items
            contar_en = cfg.get("contar_en")
            if contar_en:
                try:
                    data = r.json()
                    items = data.get(contar_en, [])
                    fmt_kwargs["count"] = len(items) if isinstance(items, list) else 0
                except Exception:
                    fmt_kwargs["count"] = 0

            # Extraer campo especifico
            extraer = cfg.get("extraer")
            if extraer:
                try:
                    data = r.json() or {}
                    fmt_kwargs[extraer] = data.get(extraer, "?")
                except Exception:
                    fmt_kwargs[extraer] = "?"

            msg = _fmt(cfg.get("msg_ok", "OK"), **fmt_kwargs)
            return {"ok": True, "configurado": True, "msg": msg, "ms": ms}

        # Errores comunes
        if r.status_code == 401:
            return {"ok": False, "configurado": True, "msg": "Token invalido o vencido", "ms": ms}
        if r.status_code == 403:
            return {"ok": False, "configurado": True, "msg": "API key invalida o sin permisos", "ms": ms}
        if r.status_code == 429:
            return {"ok": False, "configurado": True, "msg": "Limite alcanzado (rate limit)", "ms": ms}

        return {"ok": False, "configurado": True, "msg": f"HTTP {r.status_code}", "ms": ms}

    except Exception as e:
        return {"ok": False, "configurado": True, "msg": str(e)[:100], "ms": 0}


def _check_local(cfg, nombre):
    """Check para servicios locales (backend, etc.)."""
    t0 = time.time()

    endpoint_env = cfg.get("endpoint_env")
    endpoint_default = cfg.get("endpoint_default", "http://localhost:8000")
    endpoint = os.getenv(endpoint_env, endpoint_default) if endpoint_env else endpoint_default

    try:
        r = requests.get(endpoint, timeout=TIMEOUT_BACKEND)
        ms = int((time.time() - t0) * 1000)
        ok_statuses = cfg.get("ok_statuses", [200])

        if r.status_code in ok_statuses:
            return {
                "ok": True,
                "configurado": True,
                "msg": _fmt(cfg.get("msg_ok", "OK"), endpoint=endpoint),
                "ms": ms,
            }
        return {"ok": False, "configurado": True, "msg": f"HTTP {r.status_code}", "ms": ms}
    except Exception:
        return {
            "ok": False,
            "configurado": True,
            "msg": cfg.get("msg_sin_config", "No responde"),
            "ms": 0,
        }


# ==========================================
# DISPATCHER
# ==========================================
def _check_servicio(nombre, cfg):
    """Ejecuta el check del servicio segun su tipo."""
    tipo = cfg.get("tipo", "http")

    if tipo == "supabase":
        return _check_supabase(cfg, nombre)
    elif tipo == "local":
        return _check_local(cfg, nombre)
    else:  # "http" por defecto
        return _check_http(cfg, nombre)


# ==========================================
# API PUBLICA
# ==========================================
def check_todos():
    """
    Ejecuta todos los checks de servicios ACTIVOS.
    Retorna dict {nombre_servicio: {ok, configurado, msg, ms}}
    Solo incluye servicios con 'activo': true.
    """
    config = _cargar_config()
    servicios = config.get("servicios", {})

    # Ordenar por campo 'orden'
    items_ordenados = sorted(
        servicios.items(),
        key=lambda kv: kv[1].get("orden", 999),
    )

    resultados = {}
    for nombre, cfg in items_ordenados:
        if not cfg.get("activo", False):
            continue
        try:
            resultados[nombre] = _check_servicio(nombre, cfg)
        except Exception as e:
            resultados[nombre] = {
                "ok": False,
                "configurado": True,
                "msg": f"Error interno: {str(e)[:80]}",
                "ms": 0,
            }
    return resultados


def check_servicio(nombre):
    """Ejecuta el check de un servicio especifico por nombre."""
    config = _cargar_config()
    servicios = config.get("servicios", {})
    cfg = servicios.get(nombre)
    if not cfg:
        return {"ok": False, "configurado": False, "msg": "Servicio no encontrado", "ms": 0}
    return _check_servicio(nombre, cfg)


def nombres_bonitos():
    """Devuelve dict {clave: nombre_bonito} para usar en la UI."""
    config = _cargar_config()
    servicios = config.get("servicios", {})
    return {nombre: cfg.get("nombre", nombre) for nombre, cfg in servicios.items()}


def listar_activos():
    """Devuelve la lista de nombres de servicios activos."""
    config = _cargar_config()
    servicios = config.get("servicios", {})
    return [nombre for nombre, cfg in servicios.items() if cfg.get("activo", False)]


def listar_inactivos():
    """Devuelve la lista de servicios inactivos (pendientes de API key)."""
    config = _cargar_config()
    servicios = config.get("servicios", {})
    return [nombre for nombre, cfg in servicios.items() if not cfg.get("activo", False)]


# ==========================================
# TEST MANUAL
# ==========================================
if __name__ == "__main__":
    print("=" * 70)
    print("TEST DE SALUD V3.0 (config-driven)")
    print("=" * 70)
    print(f"Config: {RUTA_CONFIG}")
    print()

    activos = listar_activos()
    inactivos = listar_inactivos()
    print(f"Servicios activos: {len(activos)}")
    print(f"Servicios inactivos (pendientes): {len(inactivos)}")
    print()

    resultados = check_todos()
    for nombre, r in resultados.items():
        estado = "OK" if r["ok"] else ("SIN CONFIG" if not r["configurado"] else "ERROR")
        print(f"  [{estado:9s}] {nombre:12s} ({r['ms']:4d}ms) - {r['msg']}")

    print()
    print(f"Inactivos (listos para cuando tengas API key): {', '.join(inactivos) if inactivos else 'ninguno'}")
    print("=" * 70)