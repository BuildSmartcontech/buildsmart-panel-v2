# utils/image_optimizer.py
# ============================================
# OPTIMIZADOR DE IMAGENES
# ============================================
# Descarga imagenes de Unsplash, las optimiza
# (comprime y redimensiona) y las guarda en cache.
# ============================================

import os
import sys
import hashlib
import requests
from io import BytesIO
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ============================================
# CONFIGURACION
# ============================================

CARPETA_CACHE = "data/webs_imagenes/cache"
TIMEOUT = 30

# Tamano maximo en KB para cada tipo
TAMANOS = {
    "hero": {"width": 1600, "height": 900, "calidad": 85},
    "servicio": {"width": 600, "height": 400, "calidad": 80},
    "thumb": {"width": 300, "height": 200, "calidad": 75},
}

# Formatos soportados
EXTENSIONES_PERMITIDAS = [".jpg", ".jpeg", ".png", ".webp"]


# ============================================
# FUNCIONES AUXILIARES
# ============================================

def asegurar_carpeta_cache():
    """Crea la carpeta de cache si no existe."""
    os.makedirs(CARPETA_CACHE, exist_ok=True)


def generar_nombre_archivo(url, tamano):
    """Genera un nombre unico para el archivo cacheado."""
    texto = url + "_" + tamano
    hash_md5 = hashlib.md5(texto.encode()).hexdigest()
    return hash_md5 + ".jpg"


def ruta_cache(url, tamano):
    """Retorna la ruta completa del archivo en cache."""
    nombre = generar_nombre_archivo(url, tamano)
    return os.path.join(CARPETA_CACHE, nombre)


# ============================================
# FUNCION: DESCARGAR IMAGEN
# ============================================

def descargar_imagen(url):
    """
    Descarga una imagen desde una URL.
    Retorna los bytes o None si falla.
    """
    try:
        response = requests.get(url, timeout=TIMEOUT)
        
        if response.status_code != 200:
            print("   Error descargando: Status " + str(response.status_code))
            return None
        
        return response.content
    except Exception as e:
        print("   Error descargando: " + str(e)[:100])
        return None


# ============================================
# FUNCION: OPTIMIZAR IMAGEN
# ============================================

def optimizar_imagen(bytes_imagen, tamano="hero"):
    """
    Optimiza una imagen: la redimensiona y comprime.
    
    Args:
        bytes_imagen: bytes de la imagen original
        tamano: "hero" | "servicio" | "thumb"
    
    Returns:
        dict con bytes optimizados, o None si falla
    """
    try:
        # Abrir imagen
        img = Image.open(BytesIO(bytes_imagen))
        
        # Convertir a RGB si es necesario (para guardar como JPG)
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")
        
        # Obtener configuracion del tamano
        config = TAMANOS.get(tamano, TAMANOS["servicio"])
        ancho_max = config["width"]
        alto_max = config["height"]
        calidad = config["calidad"]
        
        # Redimensionar manteniendo proporcion
        img.thumbnail((ancho_max, alto_max), Image.LANCZOS)
        
        # Guardar en BytesIO
        output = BytesIO()
        img.save(output, format="JPEG", quality=calidad, optimize=True)
        output.seek(0)
        
        bytes_optimizados = output.getvalue()
        
        return {
            "exito": True,
            "bytes": bytes_optimizados,
            "ancho": img.width,
            "alto": img.height,
            "tamano_kb": round(len(bytes_optimizados) / 1024, 2),
            "error": None
        }
    except Exception as e:
        return {
            "exito": False,
            "bytes": None,
            "ancho": 0,
            "alto": 0,
            "tamano_kb": 0,
            "error": str(e)
        }


# ============================================
# FUNCION: DESCARGAR Y OPTIMIZAR
# ============================================

def descargar_y_optimizar(url, tamano="hero", usar_cache=True):
    """
    Descarga una imagen, la optimiza y la guarda en cache.
    
    Args:
        url: URL de Unsplash
        tamano: "hero" | "servicio" | "thumb"
        usar_cache: si True, usa el cache si existe
    
    Returns:
        dict con la ruta local del archivo, o None si falla
    """
    asegurar_carpeta_cache()
    
    ruta = ruta_cache(url, tamano)
    
    # 1. Verificar cache
    if usar_cache and os.path.exists(ruta):
        tamano_kb = round(os.path.getsize(ruta) / 1024, 2)
        return {
            "exito": True,
            "ruta": ruta,
            "desde_cache": True,
            "tamano_kb": tamano_kb,
            "error": None
        }
    
    # 2. Descargar
    bytes_originales = descargar_imagen(url)
    
    if bytes_originales is None:
        return {
            "exito": False,
            "ruta": None,
            "desde_cache": False,
            "tamano_kb": 0,
            "error": "No se pudo descargar la imagen"
        }
    
    # 3. Optimizar
    resultado = optimizar_imagen(bytes_originales, tamano)
    
    if not resultado["exito"]:
        return {
            "exito": False,
            "ruta": None,
            "desde_cache": False,
            "tamano_kb": 0,
            "error": "Error optimizando: " + str(resultado["error"])
        }
    
    # 4. Guardar en cache
    try:
        with open(ruta, "wb") as f:
            f.write(resultado["bytes"])
        
        return {
            "exito": True,
            "ruta": ruta,
            "desde_cache": False,
            "tamano_kb": resultado["tamano_kb"],
            "ancho": resultado["ancho"],
            "alto": resultado["alto"],
            "error": None
        }
    except Exception as e:
        return {
            "exito": False,
            "ruta": None,
            "desde_cache": False,
            "tamano_kb": 0,
            "error": "Error guardando: " + str(e)
        }


# ============================================
# FUNCION: PROCESAR VARIAS IMAGENES
# ============================================

def procesar_imagenes(lista_imagenes, tamano="servicio"):
    """
    Procesa varias imagenes a la vez.
    
    Args:
        lista_imagenes: lista de dicts con "url_regular"
        tamano: "hero" | "servicio" | "thumb"
    
    Returns:
        lista de dicts con rutas locales
    """
    resultados = []
    
    for img in lista_imagenes:
        url = img.get("url_regular", "")
        
        if not url:
            continue
        
        resultado = descargar_y_optimizar(url, tamano)
        
        if resultado["exito"]:
            resultado["autor"] = img.get("autor", "Unsplash")
            resultado["descripcion"] = img.get("descripcion", "")
            resultados.append(resultado)
    
    return resultados


# ============================================
# FUNCION: LIMPIAR CACHE ANTIGUO
# ============================================

def limpiar_cache(dias=30):
    """
    Elimina archivos de cache mas antiguos que X dias.
    """
    import time
    
    asegurar_carpeta_cache()
    
    ahora = time.time()
    segundos = dias * 86400
    eliminados = 0
    
    for archivo in os.listdir(CARPETA_CACHE):
        ruta = os.path.join(CARPETA_CACHE, archivo)
        
        if not os.path.isfile(ruta):
            continue
        
        if ahora - os.path.getmtime(ruta) > segundos:
            try:
                os.remove(ruta)
                eliminados += 1
            except:
                pass
    
    return eliminados


# ============================================
# FUNCION: ESTADISTICAS DEL CACHE
# ============================================

def estadisticas_cache():
    """Retorna estadisticas del cache."""
    asegurar_carpeta_cache()
    
    total_archivos = 0
    total_bytes = 0
    
    for archivo in os.listdir(CARPETA_CACHE):
        ruta = os.path.join(CARPETA_CACHE, archivo)
        
        if os.path.isfile(ruta):
            total_archivos += 1
            total_bytes += os.path.getsize(ruta)
    
    return {
        "archivos": total_archivos,
        "tamano_kb": round(total_bytes / 1024, 2),
        "tamano_mb": round(total_bytes / 1024 / 1024, 2)
    }


# ============================================
# TEST
# ============================================

def test_optimizer():
    """Prueba el optimizador de imagenes."""
    
    print("=" * 60)
    print("PROBANDO OPTIMIZADOR DE IMAGENES")
    print("=" * 60)
    print()
    
    # 1. Importar fetcher
    try:
        from utils.image_fetcher import buscar_imagenes_sector
    except ImportError:
        try:
            from image_fetcher import buscar_imagenes_sector
        except ImportError:
            print("ERROR: No se pudo importar image_fetcher")
            return
    
    # 2. Buscar imagenes
    print("1. Buscando imagenes de construccion...")
    resultado = buscar_imagenes_sector("construccion", cantidad=3)
    
    if not resultado["exito"]:
        print("   ERROR: " + str(resultado["error"]))
        return
    
    print("   Encontradas: " + str(len(resultado["imagenes"])))
    print()
    
    # 3. Procesar cada imagen en 3 tamanos
    print("2. Procesando imagenes...")
    print()
    
    for i, img in enumerate(resultado["imagenes"][:2], 1):
        print("-" * 60)
        print("Imagen " + str(i) + " - Autor: " + img["autor"])
        print("-" * 60)
        
        for tamano in ["hero", "servicio", "thumb"]:
            print("  Procesando como [" + tamano + "]...")
            
            resultado_opt = descargar_y_optimizar(img["url_regular"], tamano)
            
            if resultado_opt["exito"]:
                desde = "cache" if resultado_opt.get("desde_cache") else "descarga"
                print("    OK: " + str(resultado_opt["tamano_kb"]) + " KB (" + desde + ")")
                print("    Ruta: " + resultado_opt["ruta"])
            else:
                print("    ERROR: " + str(resultado_opt["error"]))
        
        print()
    
    # 4. Estadisticas del cache
    print("=" * 60)
    print("ESTADISTICAS DEL CACHE")
    print("=" * 60)
    
    stats = estadisticas_cache()
    print("  Archivos: " + str(stats["archivos"]))
    print("  Tamano: " + str(stats["tamano_kb"]) + " KB (" + str(stats["tamano_mb"]) + " MB)")
    
    print()
    print("=" * 60)
    print("PRUEBA COMPLETADA")
    print("=" * 60)


if __name__ == "__main__":
    test_optimizer()