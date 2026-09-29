# utils/image_fetcher.py
# ============================================
# BUSCADOR DE IMAGENES - V4.1
# ============================================
# V4.1: Restaura normalizar_sector (compatibilidad con web_generator)
# ============================================

import os
import sys
import hashlib
import urllib.parse
import requests
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

try:
    from utils.sector_detector import detectar_sector_completo, SECTORES_LOCALES
    DETECTOR_DISPONIBLE = True
except ImportError:
    try:
        from sector_detector import detectar_sector_completo, SECTORES_LOCALES
        DETECTOR_DISPONIBLE = True
    except ImportError:
        DETECTOR_DISPONIBLE = False
        detectar_sector_completo = None
        SECTORES_LOCALES = {"default": {"keywords_imagenes": ["business", "office", "professional team"]}}
        print("ADVERTENCIA: sector_detector no disponible, usando fallback")


UNSPLASH_API_URL = "https://api.unsplash.com"
POLLINATIONS_URL = "https://image.pollinations.ai/prompt"
CARPETA_CACHE = "data/webs_imagenes/cache"
TIMEOUT = 15

STOPWORDS = {
    "de", "la", "el", "los", "las", "un", "una", "unos", "unas",
    "y", "o", "u", "para", "con", "por", "en", "a", "al", "del",
    "que", "es", "son", "mi", "tu", "su", "se", "lo", "le",
    "the", "of", "and", "or", "for", "with", "by", "in", "to", "a",
    "empresa", "negocio", "servicio", "servicios", "producto", "productos",
    "somos", "hacemos", "ofrecemos", "vendemos", "tenemos", "nuestro",
    "general", "otros", "otras", "todo", "toda", "todos", "todas",
    "fabricamos", "distribuimos", "hace", "hacemos", "tiene", "tienen",
    "todas", "referencias", "tipo", "tipos", "clase", "clases",
}


# ============================================
# COMPATIBILIDAD: NORMALIZAR SECTOR
# ============================================

def normalizar_sector(sector):
    """
    Normaliza y verifica si el sector esta reconocido en la lista local.
    Retorna la clave del sector o "default" si no esta.
    Funcion de compatibilidad con web_generator.py
    """
    if not sector:
        return "default"

    sector_norm = sector.lower().strip()
    sector_norm = sector_norm.replace("á", "a").replace("é", "e").replace("í", "i")
    sector_norm = sector_norm.replace("ó", "o").replace("ú", "u").replace("ñ", "n")

    # Match exacto
    if sector_norm in SECTORES_LOCALES:
        return sector_norm

    # Match parcial con claves
    for key in SECTORES_LOCALES:
        if key == "default":
            continue
        key_clean = key.replace("_", " ")
        if key_clean in sector_norm or sector_norm in key_clean:
            return key

    return "default"


# ============================================
# FUNCIONES AUXILIARES
# ============================================

def obtener_api_key():
    return os.getenv("UNSPLASH_ACCESS_KEY")


def limpiar_api_key(key):
    if not key:
        return None
    return key.strip()


def extraer_palabras_clave(texto, max_palabras=4):
    if not texto:
        return []
    texto = texto.lower()
    for ch in [",", ".", ";", ":", "!", "?", "(", ")", "[", "]", "\"", "'", "\n", "\t", "/", "-"]:
        texto = texto.replace(ch, " ")
    palabras = texto.split()
    limpias = []
    for p in palabras:
        if len(p) > 3 and p not in STOPWORDS:
            limpias.append(p)
    return limpias[:max_palabras]


def generar_nombre_cache(query, cantidad):
    texto = query + "_" + str(cantidad)
    hash_md5 = hashlib.md5(texto.encode()).hexdigest()
    return hash_md5 + ".json"


# ============================================
# OBTENER KEYWORDS CON DETECTOR HIBRIDO
# ============================================

def obtener_keywords_inteligentes(nombre, descripcion, sector):
    if DETECTOR_DISPONIBLE and detectar_sector_completo:
        try:
            resultado = detectar_sector_completo(nombre, descripcion, sector)
            return resultado.get("keywords_imagenes", ["professional business"])
        except Exception as e:
            print("[FETCHER] Error detector: " + str(e))

    return ["professional business", "modern office", "business team"]


# ============================================
# POLLINATIONS - GENERAR URLS
# ============================================

def generar_url_pollinations(prompt, width=1200, height=800, seed=None):
    if not prompt:
        prompt = "professional business product"

    prompt_limpio = prompt.strip()
    prompt_encoded = urllib.parse.quote(prompt_limpio)

    url = (
        POLLINATIONS_URL + "/" + prompt_encoded +
        "?width=" + str(width) +
        "&height=" + str(height) +
        "&nologo=true" +
        "&enhance=true"
    )

    if seed is not None:
        url += "&seed=" + str(seed)

    return url


def construir_prompt_imagen(negocio_info, variante="hero"):
    nombre = negocio_info.get("nombre", "")
    sector = negocio_info.get("sector", "")
    descripcion = negocio_info.get("descripcion", "")

    keywords = obtener_keywords_inteligentes(nombre, descripcion, sector)

    if not keywords:
        keywords = ["professional business"]

    if variante == "hero":
        tema = keywords[0]
        prompt = f"professional photograph of {tema}, high quality, cinematic lighting, marketing photo"
    elif variante == "producto":
        tema = keywords[1] if len(keywords) > 1 else keywords[0]
        prompt = f"closeup product photo of {tema}, professional studio lighting, high detail"
    elif variante == "servicio":
        tema = keywords[2] if len(keywords) > 2 else keywords[0]
        prompt = f"work process of {tema}, professional photo, natural lighting"
    elif variante == "equipo":
        tema = keywords[0]
        prompt = f"team working on {tema}, professional photo, warm lighting"
    else:
        tema = keywords[0]
        prompt = f"professional photo of {tema}, high quality"

    return prompt


def obtener_urls_imagenes_negocio(negocio_info, cantidad=5):
    urls = []
    variantes = ["hero", "producto", "servicio", "producto", "servicio"]

    for i in range(cantidad):
        variante = variantes[i % len(variantes)]
        prompt = construir_prompt_imagen(negocio_info, variante=variante)
        url = generar_url_pollinations(prompt, seed=i * 137)
        urls.append({
            "url_regular": url,
            "url_small": url,
            "url_thumb": url,
            "autor": "AI Generated",
            "descripcion": prompt,
            "fuente": "pollinations",
            "variante": variante,
        })

    return urls


# ============================================
# UNSPLASH - FALLBACK
# ============================================

def buscar_imagenes(query, cantidad=4, orientacion="landscape"):
    api_key = limpiar_api_key(obtener_api_key())
    if not api_key:
        return {"exito": False, "imagenes": [], "error": "UNSPLASH_ACCESS_KEY no configurada"}
    if not query or not query.strip():
        return {"exito": False, "imagenes": [], "error": "Query vacio"}

    try:
        response = requests.get(
            UNSPLASH_API_URL + "/search/photos",
            headers={"Authorization": "Client-ID " + api_key},
            params={
                "query": query,
                "per_page": min(cantidad, 30),
                "orientation": orientacion,
            },
            timeout=TIMEOUT
        )
        if response.status_code != 200:
            return {"exito": False, "imagenes": [], "error": "Status " + str(response.status_code)}
        data = response.json()
        resultados = data.get("results", [])
        imagenes = []
        for r in resultados:
            imagenes.append({
                "url_regular": r["urls"].get("regular", ""),
                "url_small": r["urls"].get("small", ""),
                "url_thumb": r["urls"].get("thumb", ""),
                "autor": r.get("user", {}).get("name", "Unsplash"),
                "descripcion": r.get("description") or r.get("alt_description") or query,
                "fuente": "unsplash",
            })
        return {"exito": True, "imagenes": imagenes, "error": None}
    except Exception as e:
        return {"exito": False, "imagenes": [], "error": str(e)}


def buscar_imagenes_por_texto(texto_negocio, cantidad=4):
    if not texto_negocio:
        return {"exito": False, "imagenes": [], "error": "Texto vacio"}
    palabras = extraer_palabras_clave(texto_negocio, max_palabras=3)
    if not palabras:
        return {"exito": False, "imagenes": [], "error": "Sin palabras clave"}
    query = " ".join(palabras)
    print("   Query Unsplash: '" + query + "'")
    return buscar_imagenes(query, cantidad=cantidad)


def buscar_imagenes_sector(sector, cantidad=4, texto_negocio=""):
    print("   [FETCHER] Sector: " + str(sector))

    if DETECTOR_DISPONIBLE and detectar_sector_completo:
        try:
            nombre_negocio = texto_negocio[:50] if texto_negocio else ""
            descripcion = texto_negocio

            resultado = detectar_sector_completo(nombre_negocio, descripcion, sector)
            keywords = resultado.get("keywords_imagenes", [])

            print("   [FETCHER] Detectado: " + resultado.get("contexto", "?") + " (fuente: " + resultado.get("fuente", "?") + ")")

            api_key = limpiar_api_key(obtener_api_key())
            if api_key:
                for kw in keywords:
                    resultado_busqueda = buscar_imagenes(kw, cantidad=cantidad)
                    if resultado_busqueda["exito"] and len(resultado_busqueda["imagenes"]) > 0:
                        resultado_busqueda["keyword_usada"] = kw
                        return resultado_busqueda
        except Exception as e:
            print("   [FETCHER] Error: " + str(e))

    print("   [FETCHER] Fallback a busqueda por texto")
    if texto_negocio:
        resultado = buscar_imagenes_por_texto(texto_negocio, cantidad=cantidad)
        if resultado["exito"] and len(resultado["imagenes"]) > 0:
            resultado["keyword_usada"] = "texto_negocio"
            return resultado

    resultado = buscar_imagenes("business", cantidad=cantidad)
    resultado["keyword_usada"] = "business"
    return resultado


def buscar_hero(sector, texto_negocio=""):
    resultado = buscar_imagenes_sector(sector, cantidad=1, texto_negocio=texto_negocio)
    if resultado["exito"] and len(resultado["imagenes"]) > 0:
        return resultado["imagenes"][0]
    return None


def buscar_servicios(sector, cantidad=6, texto_negocio=""):
    resultado = buscar_imagenes_sector(sector, cantidad=cantidad, texto_negocio=texto_negocio)
    if resultado["exito"]:
        return resultado["imagenes"]
    return []


def verificar_conexion():
    resultado = buscar_imagenes("test", cantidad=1)
    return resultado["exito"]


# ============================================
# TEST
# ============================================

def test_fetcher():
    print("=" * 60)
    print("TEST IMAGE FETCHER V4.1")
    print("=" * 60)

    print("\nDETECTOR DISPONIBLE: " + str(DETECTOR_DISPONIBLE))

    # Test normalizar_sector (compatibilidad)
    print("\n--- TEST normalizar_sector ---")
    tests = ["panaderia", "manualidades", "construccion", "xyz123", ""]
    for t in tests:
        print(f"  normalizar_sector('{t}') = {normalizar_sector(t)}")

    # Test URLs
    print("\n--- TEST generacion URLs ---")
    negocios = [
        {"nombre": "Panaderia La Espiga", "sector": "panaderia", "descripcion": "Pan artesanal"},
        {"nombre": "Fabricante Velas", "sector": "manualidades", "descripcion": "Velas aromaticas"},
    ]

    for n in negocios:
        print("\n  Negocio: " + n["nombre"])
        urls = obtener_urls_imagenes_negocio(n, cantidad=2)
        for u in urls:
            print("    " + u["variante"] + ": " + u["descripcion"][:80])

    print("\n" + "=" * 60)
    print("TEST COMPLETADO")
    print("=" * 60)


if __name__ == "__main__":
    test_fetcher()