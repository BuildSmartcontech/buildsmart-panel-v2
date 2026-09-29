# utils/web_publisher.py
# ============================================
# PUBLICADOR DE WEBS - V6.0 (PROVIDER MANAGER)
# ============================================
# Orquestador que usa ProviderManager para
# seleccionar el mejor proveedor disponible.
# ============================================

import os
import sys
import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.web_storage import leer_web, CARPETA_WEBS
except ImportError:
    try:
        from web_storage import leer_web, CARPETA_WEBS
    except ImportError:
        leer_web = None
        CARPETA_WEBS = "data/webs_generadas"

# Importar providers
try:
    from utils.vercel_publisher import publicar_web as vercel_publicar
    VERCEL_DISPONIBLE = True
except ImportError:
    try:
        from vercel_publisher import publicar_web as vercel_publicar
        VERCEL_DISPONIBLE = True
    except ImportError:
        VERCEL_DISPONIBLE = False
        vercel_publicar = None

try:
    from utils.cloudflare_publisher import publicar_carpeta as cf_publicar
    CLOUDFLARE_DISPONIBLE = True
except ImportError:
    try:
        from cloudflare_publisher import publicar_carpeta as cf_publicar
        CLOUDFLARE_DISPONIBLE = True
    except ImportError:
        CLOUDFLARE_DISPONIBLE = False
        cf_publicar = None

try:
    from utils.netlify_publisher import publicar_html as netlify_publicar
    NETLIFY_DISPONIBLE = True
except ImportError:
    try:
        from netlify_publisher import publicar_html as netlify_publicar
        NETLIFY_DISPONIBLE = True
    except ImportError:
        NETLIFY_DISPONIBLE = False
        netlify_publicar = None

# Provider Manager
try:
    from utils.provider_manager import (
        seleccionar_provider, registrar_deploy, estado_providers, esta_habilitado,
    )
    PM_DISPONIBLE = True
except ImportError:
    try:
        from provider_manager import (
            seleccionar_provider, registrar_deploy, estado_providers, esta_habilitado,
        )
        PM_DISPONIBLE = True
    except ImportError:
        PM_DISPONIBLE = False
        seleccionar_provider = None
        registrar_deploy = None
        estado_providers = None
        esta_habilitado = None

URL_BASE_LOCAL = "http://localhost:8000"


def _resultado_error(msg, modo=None):
    return {
        "exito": False, "url_publicada": None, "url_local": None,
        "url_publica": None, "subdominio": None,
        "tipo": modo or "desconocido", "fecha": None, "error": msg,
    }


def _resultado_exito(url, tipo, error=None, subdominio=None, url_local=None):
    return {
        "exito": True, "url_publicada": url,
        "url_local": url_local or url, "url_publica": url,
        "subdominio": subdominio, "tipo": tipo,
        "fecha": datetime.datetime.now().isoformat(), "error": error,
    }


def publicar_web(usuario_id, web_id, prefer=None):
    """
    Publica una web seleccionando automaticamente el mejor proveedor.
    """
    print("=" * 60)
    print("PUBLICANDO WEB - V6.0 (PROVIDER MANAGER)")
    print("=" * 60)

    if leer_web is None:
        return _resultado_error("Modulo web_storage no disponible")

    resultado = leer_web(usuario_id, web_id)
    if not resultado.get("exito"):
        return _resultado_error(f"No se pudo leer la web: {resultado.get('error')}")

    html = resultado["html"]
    subdominio = f"web-{str(web_id)[:8]}"
    url_local = f"{URL_BASE_LOCAL}/web/{web_id}"

    # Mostrar estado de providers
    if PM_DISPONIBLE and estado_providers:
        estado = estado_providers()
        print("\nEstado de providers:")
        for p, info in estado.items():
            estado_txt = "OK" if info['disponible'] else "NO"
            hab_txt = "" if info['habilitado'] else " [DESHABILITADO]"
            print(f"  {p}: {estado_txt} ({info['cuota_restante']}/{info['cuota_max']} restantes){hab_txt}")

    # Seleccionar provider
    if PM_DISPONIBLE and seleccionar_provider:
        provider = seleccionar_provider(prefer=prefer)
    else:
        # Fallback simple si no hay ProviderManager
        provider = None
        if VERCEL_DISPONIBLE:
            provider = "vercel"
        elif CLOUDFLARE_DISPONIBLE:
            provider = "cloudflare"

    if not provider:
        return _resultado_error("No hay proveedores disponibles")

    print(f"\n>>> Publicando en: {provider.upper()}")

    error = "?"
    if provider == "vercel" and VERCEL_DISPONIBLE and vercel_publicar:
        resultado_pub = vercel_publicar(usuario_id, web_id)

    elif provider == "cloudflare" and CLOUDFLARE_DISPONIBLE and cf_publicar:
        ruta_carpeta = Path(CARPETA_WEBS) / str(usuario_id) / str(web_id)
        resultado_pub = cf_publicar(usuario_id, web_id, ruta_carpeta)

    elif provider == "netlify" and NETLIFY_DISPONIBLE and netlify_publicar:
        ruta_web = f"{usuario_id}/{web_id}/index.html"
        resultado_pub = netlify_publicar(ruta_web, html)

    else:
        return _resultado_error(f"Provider '{provider}' no disponible")

    # Procesar resultado
    if resultado_pub.get("exito"):
        url = resultado_pub.get("url_publica", "")
        if PM_DISPONIBLE and registrar_deploy:
            registrar_deploy(provider)
        print(f"\n[OK] {provider}: {url}")
        return _resultado_exito(url, provider, subdominio=subdominio, url_local=url_local)
    else:
        error = resultado_pub.get("error", "?")
        print(f"\n[FAIL] {provider}: {error[:150]}")

        # Failover
        otros_providers = [p for p in ["vercel", "cloudflare", "netlify"] if p != provider]
        for otro in otros_providers:
            # No intentar con providers deshabilitados
            if PM_DISPONIBLE and esta_habilitado and not esta_habilitado(otro):
                print(f"   [SKIP] {otro} esta deshabilitado")
                continue

            print(f"\n>>> Failover a: {otro.upper()}")

            if otro == "vercel" and VERCEL_DISPONIBLE and vercel_publicar:
                r2 = vercel_publicar(usuario_id, web_id)
            elif otro == "cloudflare" and CLOUDFLARE_DISPONIBLE and cf_publicar:
                ruta_carpeta = Path(CARPETA_WEBS) / str(usuario_id) / str(web_id)
                r2 = cf_publicar(usuario_id, web_id, ruta_carpeta)
            elif otro == "netlify" and NETLIFY_DISPONIBLE and netlify_publicar:
                ruta_web = f"{usuario_id}/{web_id}/index.html"
                r2 = netlify_publicar(ruta_web, html)
            else:
                continue

            if r2.get("exito"):
                url = r2.get("url_publica", "")
                if PM_DISPONIBLE and registrar_deploy:
                    registrar_deploy(otro)
                print(f"\n[OK] {otro}: {url}")
                return _resultado_exito(url, otro, subdominio=subdominio, url_local=url_local)

    return _resultado_error(f"Todos los providers fallaron: {error}")


def despublicar_web(usuario_id, web_id):
    print(f"Despublicando web: {str(web_id)[:8]}")
    return {"exito": True, "error": None}

# ... (resto de funciones auxiliares)