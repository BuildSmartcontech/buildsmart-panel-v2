# utils/provider_manager.py
# ============================================
# PROVIDER MANAGER - Seleccion automatica
# ============================================
# V1.2: Agrega Vercel como tercer proveedor.
#       Netlify permanece deshabilitado (cuenta suspendida).
# V1.1: Lista de providers deshabilitados.
# ============================================

import os
import json
import datetime

try:
    from utils.web_storage import CARPETA_WEBS
except ImportError:
    try:
        from web_storage import CARPETA_WEBS
    except ImportError:
        CARPETA_WEBS = "data/webs_generadas"

USAGE_FILE = "data/provider_usage.json"

CUOTAS = {
    "vercel": 100,      # Free: 100 deploys por dia (mucho mas generoso)
    "cloudflare": 500,
    "netlify": 300,
}

# Netlify deshabilitado (cuenta suspendida)
PROVIDERS_DESHABILITADOS = ["netlify"]


def _leer_uso():
    if not os.path.exists(USAGE_FILE):
        return {}
    try:
        with open(USAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _guardar_uso(data):
    os.makedirs(os.path.dirname(USAGE_FILE), exist_ok=True)
    with open(USAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _mes_actual():
    return datetime.datetime.now().strftime("%Y-%m")


def esta_habilitado(provider):
    return provider not in PROVIDERS_DESHABILITADOS


def registrar_deploy(provider):
    data = _leer_uso()
    mes = _mes_actual()
    if mes not in data:
        data[mes] = {}
    if provider not in data[mes]:
        data[mes][provider] = {"deploys": 0, "ultimo": None}
    data[mes][provider]["deploys"] += 1
    data[mes][provider]["ultimo"] = datetime.datetime.now().isoformat()
    _guardar_uso(data)
    return data[mes][provider]["deploys"]


def get_uso(provider):
    data = _leer_uso()
    mes = _mes_actual()
    return data.get(mes, {}).get(provider, {}).get("deploys", 0)


def get_cuota_restante(provider):
    usado = get_uso(provider)
    cuota = CUOTAS.get(provider, 0)
    return max(0, cuota - usado)


def health_check(provider):
    try:
        if provider == "netlify":
            from utils.netlify_publisher import esta_configurado
            return esta_configurado()
        elif provider == "cloudflare":
            from utils.cloudflare_publisher import BLAKE3_DISPONIBLE
            token = os.getenv("CLOUDFLARE_TOKEN", "")
            account = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
            return BLAKE3_DISPONIBLE and token.startswith("cfut_") and bool(account)
        elif provider == "vercel":
            from utils.vercel_publisher import esta_configurado
            return esta_configurado()
    except Exception as e:
        print(f"[PM] Health check {provider}: {e}")
        return False
    return False


def seleccionar_provider(prefer=None):
    if prefer:
        if not esta_habilitado(prefer):
            print(f"[PM] Preferido '{prefer}' esta DESHABILITADO...")
        elif health_check(prefer) and get_cuota_restante(prefer) > 0:
            return prefer
        else:
            print(f"[PM] Preferido '{prefer}' no viable...")

    candidatos = []
    # Orden de prioridad: Vercel, Cloudflare, Netlify
    for p in ["vercel", "cloudflare", "netlify"]:
        if not esta_habilitado(p):
            continue
        if health_check(p):
            restante = get_cuota_restante(p)
            if restante > 0:
                candidatos.append((p, restante))

    if not candidatos:
        print("[PM] No hay providers disponibles")
        return None

    # Vercel tiene prioridad si esta disponible (mas cuota diaria)
    for p, r in candidatos:
        if p == "vercel":
            print(f"[PM] Provider seleccionado: vercel (cuota: {r})")
            return "vercel"

    # Si no, el de mayor cuota
    candidatos.sort(key=lambda x: x[1], reverse=True)
    elegido = candidatos[0][0]
    print(f"[PM] Provider seleccionado: {elegido} (cuota: {candidatos[0][1]})")
    return elegido


def estado_providers():
    resultado = {}
    for p in ["vercel", "cloudflare", "netlify"]:
        resultado[p] = {
            "disponible": health_check(p),
            "habilitado": esta_habilitado(p),
            "deploys_usados": get_uso(p),
            "cuota_max": CUOTAS.get(p, 0),
            "cuota_restante": get_cuota_restante(p),
        }
    return resultado


if __name__ == "__main__":
    print("=" * 60)
    print("TEST PROVIDER MANAGER V1.2")
    print("=" * 60)
    print(f"Providers DESHABILITADOS: {PROVIDERS_DESHABILITADOS}")
    estado = estado_providers()
    for p, info in estado.items():
        print(f"\n{p.upper()}:")
        print(f"  Disponible:      {info['disponible']}")
        print(f"  Habilitado:      {info['habilitado']}")
        print(f"  Cuota restante:  {info['cuota_restante']}/{info['cuota_max']}")
    print("\n" + "-" * 40)
    print(f"Seleccion automatica: {seleccionar_provider()}")
    print("=" * 60)