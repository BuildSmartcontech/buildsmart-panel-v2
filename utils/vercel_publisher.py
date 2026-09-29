# utils/vercel_publisher.py
# ============================================
# VERCEL PUBLISHER - SAMU IA
# ============================================
# V1.1: Usa URL de ALIAS (estable) en vez de URL de deployment
#       (la URL del deployment cambia en cada publicacion)
# V1.0: Publicacion inicial via API v13
# ============================================

import os
import base64
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

VERCEL_API = "https://api.vercel.com"
VERCEL_TOKEN = os.getenv("VERCEL_TOKEN", "")

try:
    from utils.web_storage import CARPETA_WEBS
except ImportError:
    try:
        from web_storage import CARPETA_WEBS
    except ImportError:
        CARPETA_WEBS = "data/webs_generadas"


def esta_configurado():
    return bool(VERCEL_TOKEN)


def _recolectar_archivos_de_web(usuario_id, web_id):
    """Recolecta archivos de la web, con paths relativos."""
    raiz_web = Path(CARPETA_WEBS) / str(usuario_id) / str(web_id)
    if not raiz_web.exists():
        return None, []

    archivos = []
    for archivo in raiz_web.rglob("*"):
        if not archivo.is_file():
            continue
        rel = archivo.relative_to(raiz_web).as_posix()
        if rel.endswith(".pyc") or "__pycache__" in rel:
            continue
        try:
            content = archivo.read_bytes()
        except Exception as e:
            print(f"[Vercel] Error leyendo {archivo}: {e}")
            continue
        archivos.append((rel, content))
    return raiz_web, archivos


def _construir_url_estable(result):
    """
    Extrae la URL ESTABLE del deployment.

    Vercel devuelve:
      - url: URL del deployment (con hash, cambia cada vez)
      - alias: lista de URLs estables (sin hash)

    Preferimos el primer alias, que es el mas limpio:
      samu-ia-{id}.vercel.app
    """
    aliases = result.get("alias", [])
    if aliases and isinstance(aliases, list):
        # Preferir el mas corto (sin el sufijo del team)
        candidatos = [a for a in aliases if a.endswith(".vercel.app")]
        if candidatos:
            # El mas corto es el mas limpio (samu-ia-xxx.vercel.app)
            candidatos.sort(key=len)
            url = candidatos[0]
            if not url.startswith("http"):
                url = f"https://{url}"
            return url

    # Fallback: URL del deployment
    url = result.get("url", "")
    if url and not url.startswith("http"):
        url = f"https://{url}"
    return url


def publicar_web(usuario_id, web_id):
    """
    Publica una web en Vercel usando la API v13.

    Devuelve URL ESTABLE (alias de produccion), no la URL del deployment.
    """
    if not esta_configurado():
        return {"exito": False, "url_publica": None, "error": "VERCEL_TOKEN no configurado"}

    ruta_web, archivos = _recolectar_archivos_de_web(usuario_id, web_id)
    if ruta_web is None or not archivos:
        return {"exito": False, "url_publica": None, "error": "No se encontraron archivos"}

    # Vercel espera los archivos en formato base64 y con la ruta como clave.
    files_payload = []
    for rel_path, content in archivos:
        files_payload.append({
            "file": rel_path,
            "data": base64.b64encode(content).decode("utf-8"),
            "encoding": "base64"
        })

    # El nombre del proyecto en Vercel debe ser unico y en minusculas.
    project_name = f"samu-ia-{str(web_id)[:8]}"

    payload = {
        "name": project_name,
        "files": files_payload,
        "target": "production",
        "projectSettings": {
            "framework": None,
        }
    }

    headers = {
        "Authorization": f"Bearer {VERCEL_TOKEN}",
        "Content-Type": "application/json",
    }

    print(f"[Vercel] Publicando: {project_name}")
    print(f"[Vercel] Archivos: {len(files_payload)}")

    try:
        r = requests.post(f"{VERCEL_API}/v13/deployments",
                          headers=headers, json=payload, timeout=120)
        r.raise_for_status()

        result = r.json()
        deploy_url_efimera = result.get("url", "")
        aliases = result.get("alias", [])

        print(f"[Vercel] URL efimera: {deploy_url_efimera}")
        print(f"[Vercel] Aliases: {aliases}")

        url_estable = _construir_url_estable(result)
        if not url_estable:
            return {"exito": False, "url_publica": None,
                    "error": "No se pudo construir URL estable"}

        print(f"[Vercel] URL ESTABLE: {url_estable}")
        return {"exito": True, "url_publica": url_estable,
                "url_efimera": f"https://{deploy_url_efimera}" if deploy_url_efimera else None,
                "aliases": aliases, "error": None}

    except requests.exceptions.HTTPError as e:
        error_text = e.response.text[:300]
        print(f"[Vercel] Error HTTP: {e.response.status_code} - {error_text}")
        return {"exito": False, "url_publica": None,
                "error": f"HTTP {e.response.status_code}: {error_text}"}
    except Exception as e:
        print(f"[Vercel] Excepcion: {e}")
        return {"exito": False, "url_publica": None, "error": str(e)}


if __name__ == "__main__":
    print("=" * 60)
    print("TEST VERCEL PUBLISHER V1.1")
    print("=" * 60)
    print(f"Token configurado: {esta_configurado()}")
    print()

    # Publicar la web de prueba
    r = publicar_web("pedido_c8c1f3c3", "b406912c-e176-4786-85c9-76d225d4a13e")
    import json
    print()
    print(json.dumps(r, indent=2, default=str))