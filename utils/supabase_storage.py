# utils/supabase_storage.py
# ============================================
# SUPABASE STORAGE - SUBIR ARCHIVOS
# ============================================
# Sube HTML e imagenes al bucket "webs-publicas"
# ============================================

import os
import sys
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.supabase_client import supabase
except ImportError:
    try:
        from supabase_client import supabase
    except ImportError:
        supabase = None
        print("ADVERTENCIA: Supabase no disponible")


BUCKET_NAME = "webs-publicas"
TIMEOUT = 30


# ============================================
# FUNCION: SUBIR TEXTO (HTML)
# ============================================

def subir_html(usuario_id, web_id, html):
    """
    Sube un HTML al bucket webs-publicas.

    Ruta final: {usuario_id}/{web_id}/index.html
    URL publica: {supabase_url}/storage/v1/object/public/webs-publicas/{usuario_id}/{web_id}/index.html

    Returns:
        {
            "exito": True/False,
            "url_publica": "https://...",
            "ruta": "usuario/web/index.html",
            "error": None
        }
    """

    if supabase is None:
        return {"exito": False, "url_publica": None, "ruta": None, "error": "Supabase no disponible"}

    if not html or not html.strip():
        return {"exito": False, "url_publica": None, "ruta": None, "error": "HTML vacio"}

    # Construir ruta del archivo dentro del bucket
    ruta = str(usuario_id) + "/" + str(web_id) + "/index.html"

    try:
        # Endpoint de Supabase Storage (upload)
        url = supabase.url + "/storage/v1/object/" + BUCKET_NAME + "/" + ruta

        headers = {
            "apikey": supabase.key,
            "Authorization": "Bearer " + supabase.key,
            "Content-Type": "text/html; charset=utf-8",
            "x-upsert": "true",  # Sobrescribir si existe
            "Cache-Control": "public, max-age=3600",
        }

        # Enviar HTML como bytes
        html_bytes = html.encode("utf-8")

        response = requests.post(url, headers=headers, data=html_bytes, timeout=TIMEOUT)

        if response.status_code in [200, 201]:
            # URL publica
            url_publica = (
                supabase.url + "/storage/v1/object/public/" + BUCKET_NAME + "/" + ruta
            )
            print("[STORAGE] Subido: " + ruta)
            print("[STORAGE] URL: " + url_publica)
            return {
                "exito": True,
                "url_publica": url_publica,
                "ruta": ruta,
                "error": None,
            }
        else:
            error_msg = "Status " + str(response.status_code) + ": " + response.text[:200]
            print("[STORAGE] Error: " + error_msg)
            return {
                "exito": False,
                "url_publica": None,
                "ruta": ruta,
                "error": error_msg,
            }

    except Exception as e:
        print("[STORAGE] Excepcion: " + str(e))
        return {"exito": False, "url_publica": None, "ruta": ruta, "error": str(e)}


# ============================================
# FUNCION: SUBIR BYTES (IMAGENES, PDF, etc.)
# ============================================

def subir_bytes(usuario_id, web_id, nombre_archivo, contenido_bytes, content_type="application/octet-stream"):
    """
    Sube cualquier archivo binario al bucket.

    Returns:
        dict con exito, url_publica, ruta, error
    """

    if supabase is None:
        return {"exito": False, "url_publica": None, "error": "Supabase no disponible"}

    ruta = str(usuario_id) + "/" + str(web_id) + "/" + nombre_archivo

    try:
        url = supabase.url + "/storage/v1/object/" + BUCKET_NAME + "/" + ruta

        headers = {
            "apikey": supabase.key,
            "Authorization": "Bearer " + supabase.key,
            "Content-Type": content_type,
            "x-upsert": "true",
            "Cache-Control": "public, max-age=3600",
        }

        response = requests.post(url, headers=headers, data=contenido_bytes, timeout=TIMEOUT)

        if response.status_code in [200, 201]:
            url_publica = (
                supabase.url + "/storage/v1/object/public/" + BUCKET_NAME + "/" + ruta
            )
            print("[STORAGE] Subido: " + ruta)
            return {"exito": True, "url_publica": url_publica, "ruta": ruta, "error": None}
        else:
            return {
                "exito": False,
                "url_publica": None,
                "ruta": ruta,
                "error": "Status " + str(response.status_code) + ": " + response.text[:200],
            }

    except Exception as e:
        return {"exito": False, "url_publica": None, "ruta": ruta, "error": str(e)}


# ============================================
# FUNCION: ELIMINAR DEL STORAGE
# ============================================

def eliminar_web(usuario_id, web_id):
    """Elimina todos los archivos de una web del Storage."""
    if supabase is None:
        return {"exito": False, "error": "Supabase no disponible"}

    try:
        # Listar archivos
        url_list = supabase.url + "/storage/v1/object/list/" + BUCKET_NAME
        headers = {
            "apikey": supabase.key,
            "Authorization": "Bearer " + supabase.key,
            "Content-Type": "application/json",
        }
        prefix = str(usuario_id) + "/" + str(web_id)

        r = requests.post(url_list, headers=headers, json={"prefix": prefix}, timeout=TIMEOUT)

        if r.status_code != 200:
            return {"exito": False, "error": "No se pudo listar: " + r.text[:200]}

        archivos = r.json()
        rutas_borrar = []
        for a in archivos:
            rutas_borrar.append(prefix + "/" + a.get("name", ""))

        # Borrar
        if rutas_borrar:
            url_del = supabase.url + "/storage/v1/object/" + BUCKET_NAME
            r2 = requests.delete(
                url_del, headers=headers, json={"prefixes": rutas_borrar}, timeout=TIMEOUT
            )
            if r2.status_code in [200, 204]:
                return {"exito": True, "eliminados": len(rutas_borrar), "error": None}
            return {"exito": False, "error": "Error borrando: " + r2.text[:200]}

        return {"exito": True, "eliminados": 0, "error": None}

    except Exception as e:
        return {"exito": False, "error": str(e)}


# ============================================
# FUNCION: VERIFICAR CONEXION
# ============================================

def verificar_storage():
    """Verifica que el bucket existe y es accesible."""
    if supabase is None:
        return False, "Supabase no disponible"

    try:
        url = supabase.url + "/storage/v1/bucket/" + BUCKET_NAME
        headers = {
            "apikey": supabase.key,
            "Authorization": "Bearer " + supabase.key,
        }
        r = requests.get(url, headers=headers, timeout=TIMEOUT)
        if r.status_code == 200:
            info = r.json()
            publico = info.get("public", False)
            return True, "Bucket OK. Publico: " + str(publico)
        return False, "Status " + str(r.status_code) + ": " + r.text[:200]
    except Exception as e:
        return False, str(e)


# ============================================
# TEST
# ============================================

def test_storage():
    print("=" * 60)
    print("TEST SUPABASE STORAGE")
    print("=" * 60)

    ok, msg = verificar_storage()
    print("\nVerificacion bucket: " + msg)
    if not ok:
        return

    usuario_test = "test_usuario_001"
    web_test = "test_web_001"
    html_test = """<!DOCTYPE html>
<html>
<head><title>Test Storage</title></head>
<body><h1>Web subida a Supabase Storage</h1></body>
</html>"""

    print("\nSubiendo HTML de prueba...")
    resultado = subir_html(usuario_test, web_test, html_test)

    if resultado["exito"]:
        print("\nEXITO")
        print("URL publica: " + resultado["url_publica"])
        print("\nAbre esa URL en el navegador para verificar.")
    else:
        print("\nFALLO: " + str(resultado["error"]))

    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_storage()