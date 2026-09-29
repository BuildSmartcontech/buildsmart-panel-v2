# subir_codigo.py
# ============================================
# SUBE TODO EL CODIGO FUENTE A SUPABASE
# ============================================
# Este script sube todos los archivos del sistema
# de webs a la tabla codigo_fuente en Supabase,
# para que no se pierda el trabajo entre sesiones.
# ============================================

import os
import sys
import requests

# Agregar la raiz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar Supabase
try:
    from utils.supabase_client import supabase
except ImportError:
    try:
        from supabase_client import supabase
    except ImportError:
        print("ERROR: No se pudo importar supabase_client")
        print("Verifica que existe utils/supabase_client.py")
        sys.exit(1)


# ============================================
# LISTA DE ARCHIVOS A SUBIR
# ============================================

ARCHIVOS = [
    # (ruta_local, descripcion, fase)
    ("config/web_config.py", "Configuracion del sistema de webs", 1),
    ("utils/web_prompts.py", "Prompts de calidad para IA", 2),
    ("utils/web_templates.py", "Templates base de HTML/CSS", 2),
    ("utils/web_validator.py", "Validador de HTML/CSS", 2),
    ("utils/web_generator.py", "Generador de webs con IA", 3),
    ("utils/web_storage.py", "Almacenamiento en Supabase y archivos", 4),
    ("utils/web_expiration.py", "Sistema de expiracion (candado 30 dias)", 5),
    ("utils/web_downloader.py", "Descargador de webs en .zip", 6),
    ("utils/web_editor.py", "Editor de webs con IA", 7),
    ("utils/web_publisher.py", "Publicador de webs (local/Netlify)", 8),
]


# ============================================
# FUNCION: SUBIR UN ARCHIVO A SUPABASE
# ============================================

def subir_archivo(ruta, descripcion, fase):
    """Sube un archivo a la tabla codigo_fuente."""
    
    if not os.path.exists(ruta):
        print("   [SKIP] No existe: " + ruta)
        return False
    
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
        
        # Preparar datos
        data = {
            "ruta": ruta,
            "contenido": contenido,
            "descripcion": descripcion,
            "fase": fase,
            "version": 1,
        }
        
        # Upsert (insertar o actualizar)
        url = supabase.url + "/rest/v1/codigo_fuente"
        headers = supabase.headers.copy()
        headers["Prefer"] = "resolution=merge-duplicates,return=representation"
        
        # Primero verificar si ya existe
        check_url = url + "?ruta=eq." + ruta
        check_response = requests.get(check_url, headers=headers, timeout=10)
        
        if check_response.status_code == 200 and len(check_response.json()) > 0:
            # Ya existe: actualizar
            update_url = url + "?ruta=eq." + ruta
            response = requests.patch(update_url, headers=headers, json=data, timeout=15)
        else:
            # No existe: insertar
            response = requests.post(url, headers=headers, json=data, timeout=15)
        
        if response.status_code in [200, 201, 204]:
            print("   [OK] " + ruta + " (" + str(len(contenido)) + " caracteres)")
            return True
        else:
            print("   [ERROR] " + ruta + " - Status " + str(response.status_code))
            print("      " + response.text[:200])
            return False
    
    except Exception as e:
        print("   [EXCEPTION] " + ruta + ": " + str(e))
        return False


# ============================================
# FUNCION PRINCIPAL
# ============================================

def main():
    print("=" * 60)
    print("SUBIENDO CODIGO FUENTE A SUPABASE")
    print("=" * 60)
    print()
    
    if supabase is None:
        print("ERROR: Supabase no disponible")
        return
    
    print("Conectado a Supabase: " + supabase.url)
    print()
    
    exitos = 0
    errores = 0
    
    for ruta, descripcion, fase in ARCHIVOS:
        print("Subiendo [" + ruta + "]...")
        if subir_archivo(ruta, descripcion, fase):
            exitos += 1
        else:
            errores += 1
        print()
    
    print("=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print("Archivos subidos: " + str(exitos))
    print("Errores: " + str(errores))
    print("Total: " + str(len(ARCHIVOS)))
    print()
    
    if errores == 0:
        print("TODO SUBIDO CORRECTAMENTE")
        print()
        print("Ahora puedes consultar el codigo en Supabase:")
        print("   Tabla: codigo_fuente")
        print("   Columnas: ruta, contenido, descripcion, fase, version")
    else:
        print("Hay " + str(errores) + " errores. Revisa los mensajes arriba.")


# ============================================
# EJECUTAR
# ============================================

if __name__ == "__main__":
    main()