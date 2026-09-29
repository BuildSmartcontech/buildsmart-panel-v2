# bajar_todo.py
# ============================================
# BAJA TODO EL PROYECTO DESDE SUPABASE
# ============================================
# Descarga todos los archivos de la tabla codigo_fuente
# y los guarda en el disco local (sobrescribiendo).
#
# Uso:
#   python bajar_todo.py           # Baja todos
#   python bajar_todo.py --lista   # Solo lista los archivos
#   python bajar_todo.py --diff    # Muestra diferencias sin bajar
# ============================================

import os
import sys
import argparse
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.supabase_client import supabase
except ImportError:
    try:
        from supabase_client import supabase
    except ImportError:
        print("ERROR: No se pudo importar supabase_client")
        sys.exit(1)


# ============================================
# FUNCIONES
# ============================================

def obtener_archivos_de_supabase():
    """Obtiene todos los archivos de la tabla codigo_fuente."""
    url = supabase.url + "/rest/v1/codigo_fuente?select=ruta,contenido,version,fase,actualizado_en&order=ruta"
    headers = supabase.headers.copy()
    
    response = requests.get(url, headers=headers, timeout=30)
    
    if response.status_code != 200:
        print("ERROR consultando Supabase: " + str(response.status_code))
        print(response.text[:200])
        return []
    
    return response.json()


def leer_archivo_local(ruta):
    """Lee un archivo local, retorna None si no existe."""
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return None


def guardar_archivo_local(ruta, contenido):
    """Guarda un archivo local."""
    try:
        # Crear carpeta si no existe
        carpeta = os.path.dirname(ruta)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta, exist_ok=True)
        
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        return True
    except Exception as e:
        print("   ERROR guardando: " + str(e))
        return False


def mostrar_lista(archivos):
    """Muestra la lista de archivos en Supabase."""
    print("=" * 70)
    print("ARCHIVOS EN SUPABASE (" + str(len(archivos)) + ")")
    print("=" * 70)
    print()
    print(f"{'Fase':<6} {'Ruta':<50} {'Version':<8} {'Chars':<10}")
    print("-" * 70)
    for a in archivos:
        fase = a.get("fase", 0)
        ruta = a.get("ruta", "?")[:48]
        version = a.get("version", 1)
        chars = len(a.get("contenido", ""))
        print(f"{fase:<6} {ruta:<50} {version:<8} {chars:<10}")
    print()


def mostrar_diff(archivos):
    """Muestra diferencias entre Supabase y local."""
    print("=" * 70)
    print("DIFERENCIAS (Supabase vs Local)")
    print("=" * 70)
    print()
    
    iguales = 0
    diferentes = 0
    solo_supabase = 0
    
    for a in archivos:
        ruta = a.get("ruta", "")
        contenido_remoto = a.get("contenido", "")
        contenido_local = leer_archivo_local(ruta)
        
        if contenido_local is None:
            print("  [SOLO EN SUPABASE] " + ruta)
            solo_supabase += 1
        elif contenido_local == contenido_remoto:
            iguales += 1
        else:
            print("  [DIFERENTE] " + ruta + f" (remoto: {len(contenido_remoto)}, local: {len(contenido_local)})")
            diferentes += 1
    
    print()
    print("Resumen:")
    print("  Iguales: " + str(iguales))
    print("  Diferentes: " + str(diferentes))
    print("  Solo en Supabase: " + str(solo_supabase))
    print()


def bajar_todos(archivos):
    """Baja todos los archivos de Supabase al disco."""
    print("=" * 70)
    print("BAJANDO ARCHIVOS DE SUPABASE")
    print("=" * 70)
    print()
    
    exitos = 0
    errores = 0
    sin_cambios = 0
    
    for a in archivos:
        ruta = a.get("ruta", "")
        contenido_remoto = a.get("contenido", "")
        
        # Verificar si cambio
        contenido_local = leer_archivo_local(ruta)
        
        if contenido_local == contenido_remoto:
            sin_cambios += 1
            print("  [=] " + ruta + " (sin cambios)")
            continue
        
        # Guardar
        if guardar_archivo_local(ruta, contenido_remoto):
            exitos += 1
            print("  [OK] " + ruta + " (" + str(len(contenido_remoto)) + " chars)")
        else:
            errores += 1
            print("  [ERROR] " + ruta)
    
    print()
    print("=" * 70)
    print("RESUMEN")
    print("=" * 70)
    print("Descargados: " + str(exitos))
    print("Sin cambios: " + str(sin_cambios))
    print("Errores: " + str(errores))
    print("Total: " + str(len(archivos)))
    print()


# ============================================
# MAIN
# ============================================

def main():
    parser = argparse.ArgumentParser(description="Baja el proyecto desde Supabase")
    parser.add_argument("--lista", action="store_true", help="Solo lista archivos")
    parser.add_argument("--diff", action="store_true", help="Muestra diferencias sin bajar")
    
    args = parser.parse_args()
    
    if supabase is None:
        print("ERROR: Supabase no disponible")
        return
    
    print()
    print("Conectado a: " + supabase.url)
    print()
    
    archivos = obtener_archivos_de_supabase()
    
    if not archivos:
        print("No hay archivos en Supabase.")
        return
    
    if args.lista:
        mostrar_lista(archivos)
    elif args.diff:
        mostrar_diff(archivos)
    else:
        bajar_todos(archivos)


if __name__ == "__main__":
    main()