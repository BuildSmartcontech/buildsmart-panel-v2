# auto_sync.py
# ============================================
# AUTO-SYNC INTELIGENTE - Sube solo lo que cambió
# ============================================
# Corre en segundo plano. Cada 30 min verifica si
# algún archivo cambió y lo sube a Supabase.
#
# Uso:
#   python auto_sync.py              # Cada 30 min
#   python auto_sync.py --intervalo 60  # Cada 60 min
#   python auto_sync.py --once       # Una sola vez
# ============================================

import os
import sys
import time
import hashlib
import argparse
import requests
import datetime

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
# CONFIGURACION
# ============================================

INTERVALO_DEFECTO = 30  # minutos

# Mismas exclusiones que subir_todo.py
CARPETAS_EXCLUIDAS = [
    "venv", ".venv", "__pycache__", ".git", ".idea", ".vscode",
    "node_modules", "data/webs_generadas", "data/zips", "imagenes",
    "pdfs", "assets", ".streamlit", ".agents", ".claude",
    "pages", "websites", "RESPALDO",
]

ARCHIVOS_EXCLUIDOS = [
    ".env", ".env.local", "respuesta_ia.txt", "subir_todo.py",
    "bajar_todo.py", "auto_sync.py", "SYNC.md",
]

EXTENSIONES_PERMITIDAS = [".py", ".txt", ".md", ".yaml", ".yml", ".toml", ".json"]


# ============================================
# FUNCIONES
# ============================================

def debe_excluir(ruta):
    """Verifica si un archivo debe excluirse."""
    ruta_norm = ruta.replace("\\", "/").lower()
    nombre = os.path.basename(ruta)
    
    if nombre in ARCHIVOS_EXCLUIDOS:
        return True
    if nombre.endswith(".pyc") or nombre.endswith(".pyo"):
        return True
    if "RESPALDO" in ruta.upper():
        return True
    
    for carpeta in CARPETAS_EXCLUIDAS:
        if carpeta.lower() in ruta_norm:
            return True
    
    return False


def debe_subir(ruta):
    """Verifica si un archivo debe subirse."""
    if os.path.basename(ruta) == "Dockerfile":
        return True
    _, ext = os.path.splitext(ruta)
    return ext.lower() in EXTENSIONES_PERMITIDAS


def hash_contenido(contenido):
    """Genera hash MD5 de un contenido."""
    return hashlib.md5(contenido.encode("utf-8")).hexdigest()


def detectar_fase(ruta):
    """Detecta la fase segun la ruta."""
    ruta_lower = ruta.lower().replace("\\", "/")
    fases = {
        "web_config": 1, "web_prompts": 2, "web_templates": 2,
        "web_validator": 2, "web_generator": 3, "web_storage": 4,
        "web_expiration": 5, "web_downloader": 6, "web_editor": 7,
        "web_publisher": 8, "web_module": 9, "gateway": 10,
    }
    for key, fase in fases.items():
        if key in ruta_lower:
            return fase
    if "backend/main" in ruta_lower:
        return 11
    if ruta_lower == "app.py":
        return 12
    return 0


def subir_si_cambio(ruta):
    """Sube un archivo solo si cambió (compara hash)."""
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
        
        ruta_supabase = ruta.replace("\\", "/")
        hash_local = hash_contenido(contenido)
        
        # Consultar hash actual en Supabase
        url = supabase.url + "/rest/v1/codigo_fuente?ruta=eq." + ruta_supabase + "&select=id,contenido"
        headers = supabase.headers.copy()
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200 and len(response.json()) > 0:
            contenido_remoto = response.json()[0].get("contenido", "")
            hash_remoto = hash_contenido(contenido_remoto)
            
            if hash_local == hash_remoto:
                return "sin_cambios"
        
        # Subir (upsert)
        data = {
            "ruta": ruta_supabase,
            "contenido": contenido,
            "descripcion": "Fase " + str(detectar_fase(ruta)),
            "fase": detectar_fase(ruta),
            "version": 1,
        }
        
        post_url = supabase.url + "/rest/v1/codigo_fuente?on_conflict=ruta"
        post_headers = supabase.headers.copy()
        post_headers["Prefer"] = "resolution=merge-duplicates,return=representation"
        
        response = requests.post(post_url, headers=post_headers, json=data, timeout=15)
        
        if response.status_code in [200, 201, 204]:
            return "subido"
        return "error"
    except Exception as e:
        return "error: " + str(e)[:50]


def escanear_y_subir():
    """Escanea el proyecto y sube solo lo que cambió."""
    print()
    print("=" * 60)
    print("AUTO-SYNC - " + datetime.datetime.now().strftime("%H:%M:%S"))
    print("=" * 60)
    
    archivos = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if not debe_excluir(os.path.join(root, d))]
        for archivo in files:
            ruta = os.path.join(root, archivo)
            ruta_rel = os.path.relpath(ruta, ".")
            if debe_excluir(ruta_rel):
                continue
            if debe_subir(ruta_rel):
                archivos.append(ruta_rel)
    
    print("Archivos encontrados: " + str(len(archivos)))
    print()
    
    subidos = 0
    sin_cambios = 0
    errores = 0
    
    for ruta in sorted(archivos):
        resultado = subir_si_cambio(ruta)
        
        if resultado == "subido":
            subidos += 1
            print("  [↑] " + ruta)
        elif resultado == "sin_cambios":
            sin_cambios += 1
        else:
            errores += 1
            print("  [X] " + ruta + " - " + resultado)
    
    print()
    print("Resumen:")
    print("  Subidos: " + str(subidos))
    print("  Sin cambios: " + str(sin_cambios))
    print("  Errores: " + str(errores))
    print()
    
    if subidos == 0:
        print("Nada nuevo para subir. Todo está sincronizado.")
    else:
        print("Sincronizacion completa. " + str(subidos) + " archivos actualizados.")


def loop_auto_sync(intervalo_min):
    """Ejecuta el auto-sync cada X minutos."""
    print()
    print("=" * 60)
    print("AUTO-SYNC ACTIVADO")
    print("=" * 60)
    print("Intervalo: cada " + str(intervalo_min) + " minutos")
    print("Presiona Ctrl+C para detener")
    print()
    
    # Primera ejecucion inmediata
    escanear_y_subir()
    
    try:
        while True:
            print()
            print("Proxima sincronizacion en " + str(intervalo_min) + " minutos...")
            time.sleep(intervalo_min * 60)
            escanear_y_subir()
    except KeyboardInterrupt:
        print()
        print("=" * 60)
        print("AUTO-SYNC DETENIDO")
        print("=" * 60)


# ============================================
# MAIN
# ============================================

def main():
    parser = argparse.ArgumentParser(description="Auto-sync con Supabase")
    parser.add_argument("--intervalo", type=int, default=INTERVALO_DEFECTO,
                       help="Minutos entre sincronizaciones (default: 30)")
    parser.add_argument("--once", action="store_true",
                       help="Ejecutar solo una vez y salir")
    
    args = parser.parse_args()
    
    if supabase is None:
        print("ERROR: Supabase no disponible")
        return
    
    print()
    print("Conectado a: " + supabase.url)
    
    if args.once:
        escanear_y_subir()
    else:
        loop_auto_sync(args.intervalo)


if __name__ == "__main__":
    main()