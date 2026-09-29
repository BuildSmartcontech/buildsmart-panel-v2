# utils/web_storage.py
# ============================================
# ALMACENAMIENTO DE WEBS (SUPABASE + ARCHIVOS)
# ============================================
# Este archivo guarda las webs en Supabase y en archivos locales.
# ============================================

import os
import sys
import json
import uuid
import datetime
import requests

# Agregar la raiz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar Supabase
try:
    from utils.supabase_client import supabase
except ImportError:
    try:
        from supabase_client import supabase
    except ImportError:
        supabase = None
        print("ADVERTENCIA: Supabase no disponible")


# ============================================
# CONSTANTES
# ============================================

CARPETA_WEBS = "data/webs_generadas"
DIAS_EXPIRACION = 30


# ============================================
# FUNCION: GENERAR UUID VALIDO
# ============================================

def generar_uuid():
    """Genera un UUID valido para Supabase."""
    return str(uuid.uuid4())


# ============================================
# FUNCION: GUARDAR EN ARCHIVOS
# ============================================

def guardar_en_archivos(usuario_id, web_id, html):
    """Guarda el HTML en un archivo local."""
    
    try:
        carpeta = os.path.join(CARPETA_WEBS, str(usuario_id), str(web_id))
        os.makedirs(carpeta, exist_ok=True)
        
        ruta_html = os.path.join(carpeta, "index.html")
        with open(ruta_html, "w", encoding="utf-8") as f:
            f.write(html)
        
        print("Guardado en: " + ruta_html)
        
        return {
            "exito": True,
            "ruta": ruta_html,
            "carpeta": carpeta,
            "error": None
        }
    except Exception as e:
        print("Error guardando archivo: " + str(e))
        return {
            "exito": False,
            "ruta": None,
            "carpeta": None,
            "error": str(e)
        }


# ============================================
# FUNCION: GUARDAR EN SUPABASE
# ============================================

def guardar_en_supabase(usuario_id, web_id, datos):
    """Guarda los metadatos de la web en Supabase."""
    
    if supabase is None:
        return {
            "exito": False,
            "error": "Supabase no disponible"
        }
    
    try:
        # Preparar datos
        data = {
            "id": web_id,
            "usuario_id": usuario_id,
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
        
        # Insertar en Supabase
        url = supabase.url + "/rest/v1/paginas_web"
        headers = supabase.headers.copy()
        headers["Prefer"] = "return=representation"
        
        response = requests.post(url, headers=headers, json=data, timeout=15)
        
        if response.status_code in [200, 201]:
            print("Guardado en Supabase: " + web_id)
            return {
                "exito": True,
                "data": response.json(),
                "error": None
            }
        else:
            print("Error Supabase: " + str(response.status_code))
            return {
                "exito": False,
                "data": None,
                "error": "Status " + str(response.status_code) + ": " + response.text[:200]
            }
    except Exception as e:
        print("Excepcion Supabase: " + str(e))
        return {
            "exito": False,
            "data": None,
            "error": str(e)
        }


# ============================================
# FUNCION: GUARDAR USUARIO (para pruebas)
# ============================================

def guardar_usuario(email, nombre, tipo_usuario="solo_pagina"):
    """Guarda un usuario en Supabase y retorna su UUID."""
    
    if supabase is None:
        return None
    
    try:
        user_id = generar_uuid()
        
        data = {
            "id": user_id,
            "email": email,
            "nombre": nombre,
            "tipo_usuario": tipo_usuario,
        }
        
        url = supabase.url + "/rest/v1/usuarios"
        headers = supabase.headers.copy()
        headers["Prefer"] = "return=representation"
        
        response = requests.post(url, headers=headers, json=data, timeout=15)
        
        if response.status_code in [200, 201]:
            print("Usuario guardado: " + user_id)
            return user_id
        else:
            print("Error usuario: " + str(response.status_code))
            print(response.text[:200])
            return None
    except Exception as e:
        print("Excepcion usuario: " + str(e))
        return None


# ============================================
# FUNCION: GUARDAR WEB COMPLETA
# ============================================

def guardar_web(usuario_id, web_id, html, datos_extra=None):
    """Guarda una web completa (archivos + Supabase)."""
    
    print("=" * 60)
    print("GUARDANDO WEB")
    print("=" * 60)
    print("Usuario: " + str(usuario_id))
    print("Web ID: " + str(web_id))
    print("HTML: " + str(len(html)) + " caracteres")
    
    if datos_extra is None:
        datos_extra = {}
    
    # 1. Guardar en archivos
    print("\n1. Guardando en archivos...")
    resultado_archivos = guardar_en_archivos(usuario_id, web_id, html)
    
    if not resultado_archivos["exito"]:
        return {
            "exito": False,
            "ruta_archivo": None,
            "ruta_carpeta": None,
            "supabase_ok": False,
            "error": "Error guardando archivo: " + str(resultado_archivos["error"])
        }
    
    # 2. Guardar en Supabase
    print("\n2. Guardando en Supabase...")
    
    fecha_expiracion = datetime.datetime.now() + datetime.timedelta(days=DIAS_EXPIRACION)
    
    datos_supabase = datos_extra.copy()
    datos_supabase["html"] = html
    datos_supabase["fecha_expiracion"] = fecha_expiracion.isoformat()
    
    resultado_supabase = guardar_en_supabase(usuario_id, web_id, datos_supabase)
    
    # 3. Retornar
    return {
        "exito": resultado_archivos["exito"],
        "ruta_archivo": resultado_archivos["ruta"],
        "ruta_carpeta": resultado_archivos["carpeta"],
        "supabase_ok": resultado_supabase["exito"],
        "supabase_error": resultado_supabase.get("error"),
        "error": None
    }


# ============================================
# FUNCION: LEER WEB
# ============================================

def leer_web(usuario_id, web_id):
    """Lee una web de los archivos."""
    
    try:
        ruta = os.path.join(CARPETA_WEBS, str(usuario_id), str(web_id), "index.html")
        
        if not os.path.exists(ruta):
            return {
                "exito": False,
                "html": None,
                "error": "Archivo no encontrado: " + ruta
            }
        
        with open(ruta, "r", encoding="utf-8") as f:
            html = f.read()
        
        return {
            "exito": True,
            "html": html,
            "error": None
        }
    except Exception as e:
        return {
            "exito": False,
            "html": None,
            "error": str(e)
        }


# ============================================
# FUNCION: LISTAR WEBS
# ============================================

def listar_webs(usuario_id):
    """Lista todas las webs de un usuario."""
    
    try:
        carpeta_usuario = os.path.join(CARPETA_WEBS, str(usuario_id))
        
        if not os.path.exists(carpeta_usuario):
            return {
                "exito": True,
                "webs": [],
                "error": None
            }
        
        webs = []
        for web_id in os.listdir(carpeta_usuario):
            ruta_web = os.path.join(carpeta_usuario, web_id)
            if os.path.isdir(ruta_web):
                ruta_html = os.path.join(ruta_web, "index.html")
                if os.path.exists(ruta_html):
                    webs.append({
                        "web_id": web_id,
                        "ruta": ruta_html,
                        "tamano": os.path.getsize(ruta_html)
                    })
        
        return {
            "exito": True,
            "webs": webs,
            "error": None
        }
    except Exception as e:
        return {
            "exito": False,
            "webs": [],
            "error": str(e)
        }


# ============================================
# FUNCION: ELIMINAR WEB
# ============================================

def eliminar_web(usuario_id, web_id):
    """Elimina una web de los archivos."""
    
    try:
        carpeta = os.path.join(CARPETA_WEBS, str(usuario_id), str(web_id))
        
        if not os.path.exists(carpeta):
            return {
                "exito": False,
                "error": "Carpeta no existe"
            }
        
        import shutil
        shutil.rmtree(carpeta)
        
        print("Eliminada: " + carpeta)
        
        return {
            "exito": True,
            "error": None
        }
    except Exception as e:
        return {
            "exito": False,
            "error": str(e)
        }


# ============================================
# FUNCION: OBTENER ESTADISTICAS
# ============================================

def obtener_estadisticas(usuario_id):
    """Obtiene estadisticas de las webs de un usuario."""
    
    resultado = listar_webs(usuario_id)
    
    if not resultado["exito"]:
        return {
            "exito": False,
            "total": 0,
            "tamano_total": 0,
            "error": resultado["error"]
        }
    
    webs = resultado["webs"]
    tamano_total = sum(w["tamano"] for w in webs)
    
    return {
        "exito": True,
        "total": len(webs),
        "tamano_total": tamano_total,
        "tamano_promedio": tamano_total // len(webs) if webs else 0,
        "error": None
    }


# ============================================
# PRUEBA
# ============================================

def test_storage():
    """Prueba el almacenamiento con UUIDs validos."""
    
    print("=" * 60)
    print("PROBANDO ALMACENAMIENTO")
    print("=" * 60)
    
    # 1. Crear usuario de prueba en Supabase
    print("\n1. Creando usuario de prueba...")
    usuario_test = guardar_usuario(
        email="test_" + generar_uuid()[:8] + "@test.com",
        nombre="Usuario Test"
    )
    
    if usuario_test is None:
        print("No se pudo crear usuario en Supabase.")
        print("Continuando solo con archivos...")
        usuario_test = generar_uuid()
    
    # 2. Crear web de prueba
    web_test = generar_uuid()
    html_test = "<!DOCTYPE html>\n<html>\n<head><title>Test</title></head>\n<body><h1>Test</h1></body>\n</html>"
    
    print("\n2. Guardando web de prueba...")
    resultado = guardar_web(
        usuario_id=usuario_test,
        web_id=web_test,
        html=html_test,
        datos_extra={
            "tipo_pagina": "Landing Page",
            "diseno": "Moderno",
            "tono": "Profesional",
            "secciones": ["Hero", "Contacto"],
        }
    )
    
    print("\nResultado:")
    print("   Exito: " + str(resultado["exito"]))
    if resultado["ruta_archivo"]:
        print("   Archivo: " + resultado["ruta_archivo"])
    print("   Supabase: " + str(resultado.get("supabase_ok")))
    if resultado.get("supabase_error"):
        print("   Supabase error: " + str(resultado["supabase_error"])[:200])
    
    # 3. Leer web
    print("\n3. Leyendo web...")
    resultado = leer_web(usuario_test, web_test)
    if resultado["exito"]:
        print("   Leido: " + str(len(resultado["html"])) + " caracteres")
    else:
        print("   Error: " + str(resultado["error"]))
    
    # 4. Listar webs
    print("\n4. Listando webs...")
    resultado = listar_webs(usuario_test)
    print("   Total: " + str(len(resultado["webs"])))
    
    # 5. Estadisticas
    print("\n5. Estadisticas...")
    stats = obtener_estadisticas(usuario_test)
    print("   Total: " + str(stats["total"]))
    print("   Tamano total: " + str(stats["tamano_total"]) + " bytes")
    
    # 6. Eliminar web
    print("\n6. Eliminando web de prueba...")
    resultado = eliminar_web(usuario_test, web_test)
    print("   Resultado: " + str(resultado["exito"]))
    
    print("\n" + "=" * 60)
    print("PRUEBA COMPLETADA")
    print("=" * 60)


# ============================================
# EJECUTAR PRUEBA
# ============================================

if __name__ == "__main__":
    test_storage()