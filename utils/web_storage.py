# utils/web_storage.py
# ============================================
# ALMACENAMIENTO DE WEBS (SUPABASE + ARCHIVOS)
# ============================================
# V1.2: leer_web ahora consulta Supabase si el archivo local no existe.
# ============================================

import os
import sys
import json
import uuid
import datetime
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

CARPETA_WEBS = "data/webs_generadas"
DIAS_EXPIRACION = 30

def generar_uuid():
    return str(uuid.uuid4())

def guardar_en_archivos(usuario_id, web_id, html):
    try:
        carpeta = os.path.join(CARPETA_WEBS, str(usuario_id), str(web_id))
        os.makedirs(carpeta, exist_ok=True)
        ruta_html = os.path.join(carpeta, "index.html")
        with open(ruta_html, "w", encoding="utf-8") as f:
            f.write(html)
        print("Guardado en: " + ruta_html)
        return {"exito": True, "ruta": ruta_html, "carpeta": carpeta, "error": None}
    except Exception as e:
        print("Error guardando archivo: " + str(e))
        return {"exito": False, "ruta": None, "carpeta": None, "error": str(e)}

def guardar_en_supabase(usuario_id, web_id, datos):
    if supabase is None:
        return {"exito": False, "error": "Supabase no disponible"}
    try:
        try:
            uuid.UUID(str(usuario_id))
            final_usuario_id = str(usuario_id)
        except ValueError:
            print(f"[STORAGE] usuario_id '{usuario_id}' no es UUID. Generando uno nuevo...")
            final_usuario_id = generar_uuid()

        data = {
            "id": web_id,
            "usuario_id": final_usuario_id,
            "negocio_id": datos.get("negocio_id"),
            "numero_web": datos.get("numero_web", 1),
            "tipo_pagina": datos.get("tipo_pagina"),
            "diseno": datos.get("diseno"),
            "tono": datos.get("tono"),
            "secciones": datos.get("secciones"),
            "logica": datos.get("logica"),
            "funcionalidades": datos.get("funcionalidades"),
            "html_generado": datos.get("html", ""),
            "url_publicada": datos.get("url_publicada"),
            "subdominio": datos.get("subdominio"),
            "es_extra": datos.get("es_extra", False),
            "estado": "activa",
            "fecha_expiracion": datos.get("fecha_expiracion"),
        }
        url = supabase.url + "/rest/v1/paginas_web"
        headers = supabase.headers.copy()
        headers["Prefer"] = "return=representation"
        response = requests.post(url, headers=headers, json=data, timeout=15)
        if response.status_code in [200, 201]:
            print("Guardado en Supabase: " + web_id)
            return {"exito": True, "data": response.json(), "error": None}
        else:
            print("Error Supabase: " + str(response.status_code))
            return {"exito": False, "data": None, "error": "Status " + str(response.status_code) + ": " + response.text[:200]}
    except Exception as e:
        print("Excepcion Supabase: " + str(e))
        return {"exito": False, "data": None, "error": str(e)}

def guardar_usuario(email, nombre, tipo_usuario="solo_pagina"):
    if supabase is None:
        return None
    try:
        user_id = generar_uuid()
        data = {"id": user_id, "email": email, "nombre": nombre, "tipo_usuario": tipo_usuario}
        url = supabase.url + "/rest/v1/usuarios"
        headers = supabase.headers.copy()
        headers["Prefer"] = "return=representation"
        response = requests.post(url, headers=headers, json=data, timeout=15)
        if response.status_code in [200, 201]:
            print("Usuario guardado: " + user_id)
            return user_id
        else:
            print("Error usuario: " + str(response.status_code))
            return None
    except Exception as e:
        print("Excepcion usuario: " + str(e))
        return None

def guardar_web(usuario_id, web_id, html, datos_extra=None):
    print("=" * 60)
    print("GUARDANDO WEB")
    print("=" * 60)
    print("Usuario: " + str(usuario_id))
    print("Web ID: " + str(web_id))
    print("HTML: " + str(len(html)) + " caracteres")
    if datos_extra is None:
        datos_extra = {}
    print("\n1. Guardando en archivos...")
    resultado_archivos = guardar_en_archivos(usuario_id, web_id, html)
    
    print("\n2. Guardando en Supabase...")
    fecha_expiracion = datetime.datetime.now() + datetime.timedelta(days=DIAS_EXPIRACION)
    datos_supabase = datos_extra.copy()
    datos_supabase["html"] = html
    datos_supabase["fecha_expiracion"] = fecha_expiracion.isoformat()
    resultado_supabase = guardar_en_supabase(usuario_id, web_id, datos_supabase)
    
    # Retornamos exito si al menos guardó en Supabase (que es lo importante en la nube)
    exito_total = resultado_archivos["exito"] or resultado_supabase["exito"]
    
    return {
        "exito": exito_total,
        "ruta_archivo": resultado_archivos.get("ruta"),
        "ruta_carpeta": resultado_archivos.get("carpeta"),
        "supabase_ok": resultado_supabase["exito"],
        "supabase_error": resultado_supabase.get("error"),
        "error": None
    }

def leer_web(usuario_id, web_id):
    """Lee el HTML desde el disco local o, si falla, desde Supabase."""
    # 1. INTENTO LOCAL (Funciona en desarrollo)
    try:
        ruta = os.path.join(CARPETA_WEBS, str(usuario_id), str(web_id), "index.html")
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                html = f.read()
            return {"exito": True, "html": html, "error": None}
    except Exception as e:
        print(f"[STORAGE] Error leyendo archivo local: {e}")

    # 2. INTENTO SUPABASE (A prueba de balas en Streamlit Cloud)
    if supabase is None:
        return {"exito": False, "html": None, "error": "No encontrado en disco. Supabase no disponible."}

    try:
        print(f"[STORAGE] Archivo local no encontrado. Buscando web_id {web_id} en Supabase...")
        # Consultamos la tabla paginas_web
        url = supabase.url + f"/rest/v1/paginas_web?id=eq.{web_id}&select=html_generado"
        headers = supabase.headers.copy()
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                html = data[0].get("html_generado")
                if html:
                    print("[STORAGE] HTML recuperado exitosamente de Supabase.")
                    return {"exito": True, "html": html, "error": None}
        
        return {"exito": False, "html": None, "error": f"No se encontró el HTML en Supabase para web_id {web_id}"}
    except Exception as e:
        print(f"[STORAGE] Excepcion buscando en Supabase: {e}")
        return {"exito": False, "html": None, "error": f"Error en Supabase: {str(e)}"}

def listar_webs(usuario_id):
    try:
        carpeta_usuario = os.path.join(CARPETA_WEBS, str(usuario_id))
        if not os.path.exists(carpeta_usuario):
            return {"exito": True, "webs": [], "error": None}
        webs = []
        for web_id in os.listdir(carpeta_usuario):
            ruta_web = os.path.join(carpeta_usuario, web_id)
            if os.path.isdir(ruta_web):
                ruta_html = os.path.join(ruta_web, "index.html")
                if os.path.exists(ruta_html):
                    webs.append({"web_id": web_id, "ruta": ruta_html, "tamano": os.path.getsize(ruta_html)})
        return {"exito": True, "webs": webs, "error": None}
    except Exception as e:
        return {"exito": False, "webs": [], "error": str(e)}

def eliminar_web(usuario_id, web_id):
    try:
        carpeta = os.path.join(CARPETA_WEBS, str(usuario_id), str(web_id))
        if not os.path.exists(carpeta):
            return {"exito": False, "error": "Carpeta no existe"}
        import shutil
        shutil.rmtree(carpeta)
        print("Eliminada: " + carpeta)
        return {"exito": True, "error": None}
    except Exception as e:
        return {"exito": False, "error": str(e)}

def obtener_estadisticas(usuario_id):
    resultado = listar_webs(usuario_id)
    if not resultado["exito"]:
        return {"exito": False, "total": 0, "tamano_total": 0, "error": resultado["error"]}
    webs = resultado["webs"]
    tamano_total = sum(w["tamano"] for w in webs)
    return {"exito": True, "total": len(webs), "tamano_total": tamano_total, "tamano_promedio": tamano_total // len(webs) if webs else 0, "error": None}