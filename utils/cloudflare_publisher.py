
# utils/cloudflare_publisher.py
# ============================================
# CLOUDFLARE PAGES PUBLISHER - SAMU IA
# ============================================
# V5.2: FIX definitivo error 8000006/8000096
#       - manifest como CAMPO en data (no archivo)
#       - files SIN filename y SIN mime: (hash, (None, content))
# V5.1: Intento fallido - manifest como archivo
# V5.0: Manifest en data + files con (hash, content, mime)
# ============================================

import os
import json
import base64
import requests
from pathlib import Path
from dotenv import load_dotenv

try:
    import blake3 as _blake3
    BLAKE3_DISPONIBLE = True
except ImportError:
    BLAKE3_DISPONIBLE = False

load_dotenv()

API_BASE = "https://api.cloudflare.com/client/v4"

try:
    from utils.web_storage import CARPETA_WEBS
except ImportError:
    try:
        from web_storage import CARPETA_WEBS
    except ImportError:
        CARPETA_WEBS = "data/webs_generadas"


def _get_creds():
    return {
        "token": os.getenv("CLOUDFLARE_TOKEN", ""),
        "account_id": os.getenv("CLOUDFLARE_ACCOUNT_ID", ""),
        "project": os.getenv("CLOUDFLARE_PROJECT_NAME", "buildsmart-webs"),
    }


def _hash_file(content_bytes, rel_path):
    """Hash BLAKE3: blake3(base64(contenido) + extension).hex()[:32]"""
    if not BLAKE3_DISPONIBLE:
        import hashlib
        return hashlib.sha256(content_bytes).hexdigest()[:32]

    ext = os.path.splitext(rel_path)[1][1:]
    b64_str = base64.b64encode(content_bytes).decode("ascii")
    hasher = _blake3.blake3((b64_str + ext).encode("ascii"))
    return hasher.hexdigest()[:32]


def _recolectar_archivos_de_web(usuario_id, web_id):
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
            print(f"[CF] Error leyendo {archivo}: {e}")
            continue
        archivos.append((rel, content))
    return raiz_web, archivos


def _crear_proyecto_si_no_existe(project, account_id, token):
    url = f"{API_BASE}/accounts/{account_id}/pages/projects/{project}"
    r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=15)
    if r.status_code == 200:
        return True, "Proyecto ya existe"

    payload = {"name": project, "production_branch": "main"}
    r = requests.post(
        f"{API_BASE}/accounts/{account_id}/pages/projects",
        headers={"Authorization": f"Bearer {token}"},
        json=payload, timeout=20,
    )
    if r.status_code in (200, 201):
        return True, "Proyecto creado"
    if r.status_code == 409:
        return True, "Proyecto ya existe"
    return False, f"HTTP {r.status_code}: {r.text[:200]}"


def publicar_carpeta(usuario_id, web_id, ruta_local=None):
    """
    Publica web en Cloudflare Pages.

    V5.2: manifest como CAMPO en data + files SIN filename/mime.
    """
    creds = _get_creds()

    if not BLAKE3_DISPONIBLE:
        return {"exito": False, "url_publica": None, "url_produccion": None,
                "tipo": "cloudflare",
                "error": "blake3 no instalado. Ejecutar: pip install blake3"}

    if not creds["token"] or not creds["token"].startswith("cfut_"):
        return {"exito": False, "url_publica": None, "url_produccion": None,
                "tipo": "cloudflare", "error": "CLOUDFLARE_TOKEN no configurado"}

    if not creds["account_id"]:
        return {"exito": False, "url_publica": None, "url_produccion": None,
                "tipo": "cloudflare", "error": "CLOUDFLARE_ACCOUNT_ID no configurado"}

    ok, msg = _crear_proyecto_si_no_existe(creds["project"], creds["account_id"], creds["token"])
    if not ok:
        return {"exito": False, "url_publica": None, "url_produccion": None,
                "tipo": "cloudflare", "error": f"Proyecto: {msg}"}

    ruta_web, archivos = _recolectar_archivos_de_web(usuario_id, web_id)

    if ruta_web is None:
        return {"exito": False, "url_publica": None, "url_produccion": None,
                "tipo": "cloudflare",
                "error": f"No existe carpeta para web {web_id}"}

    if not archivos:
        return {"exito": False, "url_publica": None, "url_produccion": None,
                "tipo": "cloudflare", "error": f"No hay archivos en {ruta_web}"}

    files_data = []
    manifest = {}
    hashes_list = []

    for rel_path, content in archivos:
        file_hash = _hash_file(content, rel_path)
        manifest["/" + rel_path] = file_hash
        files_data.append((rel_path, content, file_hash))
        hashes_list.append(file_hash)

    print(f"[CF] Publicando: {usuario_id}/{web_id}")
    print(f"[CF] Archivos: {len(files_data)}")

    # ==========================================
    # PASO 1: Obtener JWT
    # ==========================================
    print("[CF] Paso 1: Obteniendo JWT...")
    url_jwt = (f"{API_BASE}/accounts/{creds['account_id']}"
               f"/pages/projects/{creds['project']}/upload-token")
    r = requests.get(url_jwt, headers={"Authorization": f"Bearer {creds['token']}"}, timeout=15)

    if r.status_code != 200:
        return {"exito": False, "url_publica": None, "url_produccion": None,
                "tipo": "cloudflare",
                "error": f"Upload-token HTTP {r.status_code}: {r.text[:200]}"}

    jwt = r.json().get("result", {}).get("jwt", "")
    if not jwt:
        return {"exito": False, "url_publica": None, "url_produccion": None,
                "tipo": "cloudflare", "error": "JWT vacio"}

    print(f"[CF] JWT OK: {jwt[:30]}...")

    # ==========================================
    # PASO 2: Verificar hashes faltantes
    # ==========================================
    print("[CF] Paso 2: Verificando hashes faltantes...")
    url_check = f"{API_BASE}/pages/assets/check-missing"
    headers_jwt = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }

    r = requests.post(url_check, headers=headers_jwt,
                      json={"hashes": hashes_list}, timeout=30)

    if r.status_code != 200:
        return {"exito": False, "url_publica": None, "url_produccion": None,
                "tipo": "cloudflare",
                "error": f"Check-missing HTTP {r.status_code}: {r.text[:200]}"}

    faltantes = r.json().get("result", [])
    print(f"[CF] Hashes faltantes: {len(faltantes)} de {len(hashes_list)}")

    # ==========================================
    # PASO 3: Subir assets (SIN prefijo de cuenta)
    # ==========================================
    if faltantes:
        print("[CF] Paso 3: Subiendo assets...")
        url_upload = f"{API_BASE}/pages/assets/upload"

        upload_payload = []
        for rel_path, content, file_hash in files_data:
            if file_hash in faltantes:
                upload_payload.append({
                    "key": file_hash,
                    "value": base64.b64encode(content).decode("ascii"),
                    "metadata": {"contentType": _mime_type(rel_path)},
                    "base64": True,
                })

        if upload_payload:
            r = requests.post(url_upload, headers=headers_jwt,
                              json=upload_payload, timeout=60)

            if r.status_code not in (200, 201):
                return {"exito": False, "url_publica": None, "url_produccion": None,
                        "tipo": "cloudflare",
                        "error": f"Upload HTTP {r.status_code}: {r.text[:300]}"}

            print(f"[CF] Assets subidos: {len(upload_payload)}")

        # ==========================================
        # PASO 4: Upsert hashes
        # ==========================================
        print("[CF] Paso 4: Upsert hashes...")
        url_upsert = f"{API_BASE}/pages/assets/upsert-hashes"

        r = requests.post(url_upsert, headers=headers_jwt,
                          json={"hashes": faltantes}, timeout=30)

        if r.status_code not in (200, 201):
            print(f"[CF] Upsert warning: HTTP {r.status_code}")

    # ==========================================
    # PASO 5: Crear deployment
    # V5.2 FIX: manifest en DATA + files SIN filename/mime
    # ==========================================
    print("[CF] Paso 5: Creando deployment...")

    # manifest como CAMPO JSON en data
    data = {
        "branch": "main",
        "manifest": json.dumps(manifest),
    }

    # files con formato (hash, (None, content)) - SIN filename, SIN mime
    files = []
    for rel_path, content, file_hash in files_data:
        files.append((file_hash, (None, content)))

    url_deploy = (f"{API_BASE}/accounts/{creds['account_id']}"
                  f"/pages/projects/{creds['project']}/deployments")

    r = requests.post(
        url_deploy,
        headers={"Authorization": f"Bearer {creds['token']}"},
        data=data,
        files=files,
        timeout=60,
    )

    if r.status_code not in (200, 201):
        return {"exito": False, "url_publica": None, "url_produccion": None,
                "tipo": "cloudflare",
                "error": f"Deploy HTTP {r.status_code}: {r.text[:300]}"}

    result = r.json()
    if not result.get("success"):
        return {"exito": False, "url_publica": None, "url_produccion": None,
                "tipo": "cloudflare",
                "error": f"API error: {result.get('errors', [])}"}

    deployment = result.get("result", {})
    deploy_url = deployment.get("url", "")
    deploy_id = deployment.get("id", "")

    if not deploy_url:
        deploy_url = f"https://{deploy_id[:8]}.{creds['project']}.pages.dev"

    print(f"[CF] Deploy OK: {deploy_url}")

    return {"exito": True, "url_publica": deploy_url, "url_produccion": deploy_url,
            "tipo": "cloudflare", "error": None, "deployment_id": deploy_id}


def _mime_type(rel_path):
    ext = os.path.splitext(rel_path)[1].lower()
    mimes = {
        ".html": "text/html", ".htm": "text/html",
        ".css": "text/css", ".js": "application/javascript",
        ".json": "application/json", ".png": "image/png",
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".svg": "image/svg+xml", ".gif": "image/gif",
        ".webp": "image/webp", ".ico": "image/x-icon",
    }
    return mimes.get(ext, "application/octet-stream")


if __name__ == "__main__":
    print("=" * 60)
    print("TEST CLOUDFLARE PUBLISHER V5.2")
    print("=" * 60)

    creds = _get_creds()
    print(f"Token: {'OK' if creds['token'].startswith('cfut_') else 'FALTA'}")
    print(f"Account ID: {'OK' if creds['account_id'] else 'FALTA'}")
    print(f"Project: {creds['project']}")
    print(f"BLAKE3 disponible: {BLAKE3_DISPONIBLE}")

    usuario_test = "pedido_c8c1f3c3"
    web_test = "b406912c-e176-4786-85c9-76d225d4a13e"

    ruta_web, archivos = _recolectar_archivos_de_web(usuario_test, web_test)
    if ruta_web:
        print(f"\nWeb test: {ruta_web}")
        print(f"Archivos: {len(archivos)}")
    else:
        print(f"\nNo existe: {usuario_test}/{web_test}")
    print("=" * 60)