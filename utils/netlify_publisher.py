# utils/netlify_publisher.py
# ============================================
# NETLIFY PUBLISHER - V1.2
# ============================================
# V1.2: Usa NETLIFY_TOKEN (token bueno samupor527)
#       Auto-detecta site_id si no esta en .env
# V1.1: Fix error 422 - solo sube si es requerido
# V1.0: Version inicial
# ============================================

import os
import sys
import hashlib
import requests
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

# ============================================
# CONFIGURACION
# ============================================

NETLIFY_API = "https://api.netlify.com/api/v1"
TIMEOUT = 30


def _get_token():
    """Lee el token bueno (NETLIFY_TOKEN tiene prioridad)."""
    return os.getenv("NETLIFY_TOKEN", "") or os.getenv("NETLIFY_API_KEY", "")


def _get_site_id():
    """Lee el site_id del .env o lo auto-detecta."""
    site_id = os.getenv("NETLIFY_SITE_ID", "")
    if site_id:
        return site_id

    # Auto-detectar: listar sitios y usar el primero
    token = _get_token()
    if not token:
        return ""

    try:
        r = requests.get(
            f"{NETLIFY_API}/sites",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )
        if r.status_code == 200:
            sites = r.json()
            if sites:
                return sites[0].get("id", "")
    except Exception:
        pass
    return ""


def esta_configurado():
    """Verifica si Netlify esta configurado."""
    return bool(_get_token() and _get_site_id())


def _headers():
    return {
        "Authorization": "Bearer " + _get_token(),
        "Content-Type": "application/json",
    }


# ============================================
# FUNCION PRINCIPAL: PUBLICAR HTML
# ============================================

def publicar_html(ruta_web, html):
    """
    Publica un HTML en Netlify.

    Args:
        ruta_web: ruta dentro del sitio (ej: "abc123/index.html")
        html: contenido HTML completo

    Returns:
        {
            "exito": True/False,
            "url_publica": "...",
            "deploy_id": "...",
            "cacheado": True/False,
            "error": None
        }
    """

    token = _get_token()
    site_id = _get_site_id()

    if not token:
        return {"exito": False, "url_publica": None, "deploy_id": None,
                "cacheado": False, "error": "NETLIFY_TOKEN no configurado"}

    if not site_id:
        return {"exito": False, "url_publica": None, "deploy_id": None,
                "cacheado": False, "error": "No hay sitios en la cuenta Netlify"}

    if not html or not html.strip():
        return {"exito": False, "url_publica": None, "deploy_id": None,
                "cacheado": False, "error": "HTML vacio"}

    # Normalizar ruta
    ruta_limpia = "/" + ruta_web.lstrip("/")

    # Hash SHA1 del contenido (Netlify usa SHA1)
    html_bytes = html.encode("utf-8")
    sha1 = hashlib.sha1(html_bytes).hexdigest()

    try:
        # 1. Crear el deploy con el hash del archivo
        payload_deploy = {"files": {ruta_limpia: sha1}}

        url_deploy = f"{NETLIFY_API}/sites/{site_id}/deploys"
        r = requests.post(url_deploy, headers=_headers(), json=payload_deploy, timeout=TIMEOUT)

        if r.status_code not in [200, 201]:
            return {"exito": False, "url_publica": None, "deploy_id": None,
                    "cacheado": False,
                    "error": f"Deploy error {r.status_code}: {r.text[:200]}"}

        deploy_data = r.json()
        deploy_id = deploy_data.get("id")
        required = deploy_data.get("required", [])

        print(f"[NETLIFY] Deploy creado: {deploy_id}")
        print(f"[NETLIFY] Archivos requeridos: {required}")

        # 2. Subir el archivo SOLO si es requerido
        cacheado = False

        if sha1 in required:
            url_file = f"{NETLIFY_API}/deploys/{deploy_id}/files{ruta_limpia}"
            headers_upload = {
                "Authorization": "Bearer " + token,
                "Content-Type": "application/octet-stream",
            }
            r2 = requests.put(url_file, headers=headers_upload, data=html_bytes, timeout=TIMEOUT)

            if r2.status_code not in [200, 201]:
                return {"exito": False, "url_publica": None, "deploy_id": deploy_id,
                        "cacheado": False,
                        "error": f"Upload error {r2.status_code}: {r2.text[:200]}"}

            print(f"[NETLIFY] Archivo subido: {ruta_limpia}")
        else:
            cacheado = True
            print("[NETLIFY] Archivo ya cacheado (sin cambios)")

        # 3. Construir URL publica
        site_url = f"https://{site_id}.netlify.app"
        try:
            r3 = requests.get(f"{NETLIFY_API}/sites/{site_id}", headers=_headers(), timeout=10)
            if r3.status_code == 200:
                data_site = r3.json()
                site_url = data_site.get("ssl_url") or data_site.get("url") or site_url
        except Exception:
            pass

        url_publica = site_url.rstrip("/") + ruta_limpia
        if url_publica.endswith("/index.html"):
            url_publica = url_publica[:-len("index.html")]

        print(f"[NETLIFY] URL publica: {url_publica}")

        return {"exito": True, "url_publica": url_publica, "deploy_id": deploy_id,
                "cacheado": cacheado, "error": None}

    except Exception as e:
        return {"exito": False, "url_publica": None, "deploy_id": None,
                "cacheado": False, "error": f"Excepcion: {e}"}


# ============================================
# FUNCION: VERIFICAR CONEXION
# ============================================

def verificar_conexion():
    """Verifica que la API de Netlify responda."""
    token = _get_token()
    if not token:
        return False, "NETLIFY_TOKEN no configurado"

    try:
        r = requests.get(
            f"{NETLIFY_API}/user",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )
        if r.status_code == 200:
            data = r.json()
            email = data.get("email", "?")
            rs = requests.get(
                f"{NETLIFY_API}/sites",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10,
            )
            sites_count = len(rs.json()) if rs.status_code == 200 else 0
            return True, f"Conectado: {email} | Sitios: {sites_count}"
        return False, f"Status {r.status_code}: {r.text[:200]}"
    except Exception as e:
        return False, str(e)


# ============================================
# TEST
# ============================================

def test_netlify():
    print("=" * 60)
    print("TEST NETLIFY PUBLISHER V1.2")
    print("=" * 60)

    token = _get_token()
    site_id = _get_site_id()

    print(f"\nToken: {'OK (' + token[:15] + '...)' if token else 'FALTA'}")
    print(f"Site ID: {site_id if site_id else 'FALTA'}")

    if not esta_configurado():
        print("\nFalta configuracion en .env")
        return

    print("\nVerificando conexion...")
    ok, msg = verificar_conexion()
    print(f"Resultado: {msg}")


if __name__ == "__main__":
    test_netlify()