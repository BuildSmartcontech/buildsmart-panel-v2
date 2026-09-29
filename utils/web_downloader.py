# utils/web_downloader.py
# ============================================
# DESCARGADOR DE WEBS (GENERA .ZIP CON HTML/CSS)
# ============================================
# Este archivo empaqueta el HTML/CSS en un archivo .zip
# para que el usuario lo descargue.
# ============================================

import os
import sys
import zipfile
import datetime

# Agregar la raiz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar storage para leer las webs
try:
    from utils.web_storage import leer_web, CARPETA_WEBS
except ImportError:
    try:
        from web_storage import leer_web, CARPETA_WEBS
    except ImportError:
        leer_web = None
        CARPETA_WEBS = "data/webs_generadas"


# ============================================
# CONSTANTES
# ============================================

CARPETA_ZIPS = "data/zips"


# ============================================
# FUNCION: CREAR CARPETA DE ZIPS
# ============================================

def asegurar_carpeta_zips():
    """Crea la carpeta de zips si no existe."""
    os.makedirs(CARPETA_ZIPS, exist_ok=True)


# ============================================
# FUNCION: GENERAR NOMBRE DE ZIP
# ============================================

def generar_nombre_zip(usuario_id, web_id):
    """Genera un nombre unico para el zip."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre = "web_" + str(usuario_id)[:8] + "_" + str(web_id)[:8] + "_" + timestamp + ".zip"
    return nombre


# ============================================
# FUNCION: EMPAQUETAR WEB EN ZIP
# ============================================

def empaquetar_web(usuario_id, web_id, incluir_leeme=True):
    """
    Empaqueta una web en un archivo .zip.
    
    Args:
        usuario_id: ID del usuario
        web_id: ID de la web
        incluir_leeme: si True, incluye un archivo LEEME.txt
    
    Returns:
        dict con:
        {
            "exito": True/False,
            "ruta_zip": "...",
            "tamano": 12345,
            "archivos": ["index.html", "LEEME.txt"],
            "error": "..."
        }
    """
    
    print("=" * 60)
    print("EMPAQUETANDO WEB EN ZIP")
    print("=" * 60)
    print("Usuario: " + str(usuario_id)[:8])
    print("Web: " + str(web_id)[:8])
    
    # 1. Leer HTML
    if leer_web is None:
        return {
            "exito": False,
            "ruta_zip": None,
            "tamano": 0,
            "archivos": [],
            "error": "Modulo web_storage no disponible"
        }
    
    resultado = leer_web(usuario_id, web_id)
    
    if not resultado["exito"]:
        return {
            "exito": False,
            "ruta_zip": None,
            "tamano": 0,
            "archivos": [],
            "error": "No se pudo leer la web: " + str(resultado["error"])
        }
    
    html = resultado["html"]
    print("HTML leido: " + str(len(html)) + " caracteres")
    
    # 2. Crear carpeta de zips
    asegurar_carpeta_zips()
    
    # 3. Generar nombre del zip
    nombre_zip = generar_nombre_zip(usuario_id, web_id)
    ruta_zip = os.path.join(CARPETA_ZIPS, nombre_zip)
    
    # 4. Crear zip
    try:
        archivos_incluidos = []
        
        with zipfile.ZipFile(ruta_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            # Agregar index.html
            zf.writestr("index.html", html)
            archivos_incluidos.append("index.html")
            print("Agregado: index.html")
            
            # Agregar LEEME.txt
            if incluir_leeme:
                leeme = generar_leeme(usuario_id, web_id)
                zf.writestr("LEEME.txt", leeme)
                archivos_incluidos.append("LEEME.txt")
                print("Agregado: LEEME.txt")
        
        # 5. Verificar
        tamano = os.path.getsize(ruta_zip)
        print("Zip creado: " + ruta_zip)
        print("Tamano: " + str(tamano) + " bytes")
        
        return {
            "exito": True,
            "ruta_zip": ruta_zip,
            "tamano": tamano,
            "archivos": archivos_incluidos,
            "error": None
        }
    except Exception as e:
        print("Error creando zip: " + str(e))
        return {
            "exito": False,
            "ruta_zip": None,
            "tamano": 0,
            "archivos": [],
            "error": str(e)
        }


# ============================================
# FUNCION: GENERAR ARCHIVO LEEME.TXT
# ============================================

def generar_leeme(usuario_id, web_id):
    """Genera un archivo LEEME.txt con instrucciones."""
    
    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    leeme = (
        "============================================\n"
        "  BUILD SMART HOLDINGS - TU PAGINA WEB\n"
        "============================================\n"
        "\n"
        "Gracias por descargar tu pagina web generada con IA.\n"
        "\n"
        "INFORMACION DE TU WEB\n"
        "---------------------\n"
        "ID de Web: " + str(web_id) + "\n"
        "ID de Usuario: " + str(usuario_id) + "\n"
        "Fecha de descarga: " + fecha + "\n"
        "\n"
        "ARCHIVOS INCLUIDOS\n"
        "------------------\n"
        "1. index.html - Tu pagina web completa (HTML + CSS embebido)\n"
        "2. LEEME.txt - Este archivo de instrucciones\n"
        "\n"
        "COMO USAR TU PAGINA WEB\n"
        "-----------------------\n"
        "\n"
        "OPCION 1: Subir a tu propio hosting\n"
        "1. Descomprime el archivo .zip\n"
        "2. Sube el archivo index.html a tu hosting (cPanel, FTP, etc.)\n"
        "3. Listo, tu web estara en linea en tu dominio\n"
        "\n"
        "OPCION 2: Subir a Netlify (GRATIS)\n"
        "1. Ve a https://app.netlify.com/drop\n"
        "2. Arrastra el archivo index.html a la pagina\n"
        "3. Netlify te dara una URL gratis (ej: tu-web.netlify.app)\n"
        "4. Si quieres, conecta tu dominio propio\n"
        "\n"
        "OPCION 3: Subir a Vercel (GRATIS)\n"
        "1. Ve a https://vercel.com/new\n"
        "2. Sigue las instrucciones\n"
        "3. Vercel te dara una URL gratis\n"
        "\n"
        "OPCION 4: Subir a GitHub Pages (GRATIS)\n"
        "1. Crea un repositorio en GitHub\n"
        "2. Sube el archivo index.html\n"
        "3. Activa GitHub Pages en la configuracion\n"
        "4. GitHub te dara una URL gratis\n"
        "\n"
        "PERSONALIZACION\n"
        "---------------\n"
        "El archivo index.html tiene CSS embebido en la etiqueta style.\n"
        "Para cambiar colores, fuentes o estilos:\n"
        "1. Abre index.html con un editor de texto (Notepad++, VSCode)\n"
        "2. Busca la seccion style en el head\n"
        "3. Modifica los estilos que quieras\n"
        "4. Guarda y sube de nuevo\n"
        "\n"
        "SOPORTE\n"
        "-------\n"
        "Si tienes problemas, contactanos:\n"
        "- Web: https://buildsmart.app\n"
        "- Email: soporte@buildsmart.app\n"
        "\n"
        "============================================\n"
        "  Generado por SAMU IA\n"
        "  https://buildsmart.app\n"
        "============================================\n"
    )
    
    return leeme


# ============================================
# FUNCION: DESCARGAR WEB (FACHADA)
# ============================================

def descargar_web(usuario_id, web_id):
    """
    Funcion principal para descargar una web.
    Verifica permisos y genera el zip.
    
    Returns:
        dict con:
        {
            "exito": True/False,
            "ruta_zip": "...",
            "nombre_zip": "...",
            "tamano": 12345,
            "es_gratis": True/False,
            "error": "..."
        }
    """
    
    print("=" * 60)
    print("DESCARGANDO WEB")
    print("=" * 60)
    print("Usuario: " + str(usuario_id)[:8])
    print("Web: " + str(web_id)[:8])
    
    # Generar zip
    resultado = empaquetar_web(usuario_id, web_id)
    
    if not resultado["exito"]:
        return {
            "exito": False,
            "ruta_zip": None,
            "nombre_zip": None,
            "tamano": 0,
            "es_gratis": False,
            "error": resultado["error"]
        }
    
    # Extraer nombre del zip
    nombre_zip = os.path.basename(resultado["ruta_zip"])
    
    return {
        "exito": True,
        "ruta_zip": resultado["ruta_zip"],
        "nombre_zip": nombre_zip,
        "tamano": resultado["tamano"],
        "es_gratis": False,  # Se define en web_module segun tipo de usuario
        "error": None
    }


# ============================================
# FUNCION: LISTAR ZIPS GENERADOS
# ============================================

def listar_zips():
    """Lista todos los zips generados."""
    
    try:
        asegurar_carpeta_zips()
        
        if not os.path.exists(CARPETA_ZIPS):
            return {
                "exito": True,
                "zips": [],
                "error": None
            }
        
        zips = []
        for archivo in os.listdir(CARPETA_ZIPS):
            if archivo.endswith(".zip"):
                ruta = os.path.join(CARPETA_ZIPS, archivo)
                zips.append({
                    "nombre": archivo,
                    "ruta": ruta,
                    "tamano": os.path.getsize(ruta),
                    "fecha": datetime.datetime.fromtimestamp(
                        os.path.getmtime(ruta)
                    ).isoformat()
                })
        
        return {
            "exito": True,
            "zips": zips,
            "error": None
        }
    except Exception as e:
        return {
            "exito": False,
            "zips": [],
            "error": str(e)
        }


# ============================================
# FUNCION: ELIMINAR ZIP
# ============================================

def eliminar_zip(nombre_zip):
    """Elimina un zip generado."""
    
    try:
        ruta = os.path.join(CARPETA_ZIPS, nombre_zip)
        
        if not os.path.exists(ruta):
            return {
                "exito": False,
                "error": "Zip no encontrado"
            }
        
        os.remove(ruta)
        print("Zip eliminado: " + nombre_zip)
        
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
# PRUEBA
# ============================================

def test_downloader():
    """Prueba el descargador."""
    
    print("=" * 60)
    print("PROBANDO DESCARGADOR DE WEBS")
    print("=" * 60)
    
    try:
        from utils.web_storage import guardar_usuario, guardar_web, generar_uuid
    except ImportError:
        from web_storage import guardar_usuario, guardar_web, generar_uuid
    
    # 1. Crear usuario y web
    print("\n1. Creando usuario y web de prueba...")
    
    usuario_test = guardar_usuario(
        email="test_dl_" + generar_uuid()[:8] + "@test.com",
        nombre="Test Downloader"
    )
    
    if usuario_test is None:
        print("No se pudo crear usuario")
        return
    
    web_test = generar_uuid()
    html_test = (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head><title>Test Web</title></head>\n"
        "<body><h1>Hola Mundo</h1><p>Esta es una web de prueba.</p></body>\n"
        "</html>"
    )
    
    resultado = guardar_web(
        usuario_id=usuario_test,
        web_id=web_test,
        html=html_test,
        datos_extra={"tipo_pagina": "Landing Page"}
    )
    
    print("Web creada: " + web_test[:8])
    
    # 2. Descargar web
    print("\n2. Descargando web...")
    resultado = descargar_web(usuario_test, web_test)
    
    if resultado["exito"]:
        print("\nDescarga EXITOSA")
        print("   Ruta: " + resultado["ruta_zip"])
        print("   Nombre: " + resultado["nombre_zip"])
        print("   Tamano: " + str(resultado["tamano"]) + " bytes")
        print("   Es gratis: " + str(resultado["es_gratis"]))
    else:
        print("\nDescarga FALLIDA")
        print("   Error: " + str(resultado["error"]))
    
    # 3. Listar zips
    print("\n3. Listando zips generados...")
    resultado = listar_zips()
    
    if resultado["exito"]:
        print("   Total: " + str(len(resultado["zips"])))
        for z in resultado["zips"]:
            print("   - " + z["nombre"] + " (" + str(z["tamano"]) + " bytes)")
    
    # 4. Eliminar zip
    if resultado["exito"] and len(resultado["zips"]) > 0:
        print("\n4. Eliminando zip de prueba...")
        nombre = resultado["zips"][-1]["nombre"]
        resultado = eliminar_zip(nombre)
        print("   Resultado: " + str(resultado["exito"]))
    
    print("\n" + "=" * 60)
    print("PRUEBA COMPLETADA")
    print("=" * 60)


# ============================================
# EJECUTAR PRUEBA
# ============================================

if __name__ == "__main__":
    test_downloader()