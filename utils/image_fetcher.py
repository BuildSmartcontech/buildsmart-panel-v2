
# utils/image_fetcher.py
# ============================================
# BUSCADOR DE IMAGENES - V5.0 (REALISMO CON FLUX)
# ============================================
# V5.0: Usa el modelo 'flux' y prompts fotorrealistas para Pollinations.
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

UNSPLASH_API_URL = "https://api.unsplash.com"
POLLINATIONS_URL = "https://image.pollinations.ai/prompt"
CARPETA_CACHE = "data/webs_imagenes/cache"
TIMEOUT = 30

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

def normalizar_sector(sector):
    if not sector: return "default"
    sector_norm = sector.lower().strip()
    sector_norm = sector_norm.replace("Ã¡", "a").replace("Ã©", "e").replace("Ã­", "i")
    sector_norm = sector_norm.replace("Ã³", "o").replace("Ãº", "u").replace("Ã±", "n")
    if sector_norm in SECTORES_LOCALES: return sector_norm
    for key in SECTORES_LOCALES:
        if key == "default": continue
        key_clean = key.replace("_", " ")
        if key_clean in sector_norm or sector_norm in key_clean: return key
    return "default"

def obtener_api_key():
    return os.getenv("UNSPLASH_ACCESS_KEY")

def limpiar_api_key(key):
    if not key: return None
    return key.strip()

def extraer_palabras_clave(texto, max_palabras=4):
    if not texto: return []
    texto = texto.lower()
    for ch in [",", ".", ";", ":", "!", "?", "(", ")", "[", "]", "\"", "'", "\n", "\t", "/", "-"]:
        texto = texto.replace(ch, " ")
    palabras = texto.split()
    limpias = []
    for p in palabras:
        if len(p) > 3 and p not in STOPWORDS: limpias.append(p)
    return limpias[:max_palabras]

def generar_nombre_cache(query, cantidad):
    texto = query + "_" + str(cantidad)
    hash_md5 = hashlib.md5(texto.encode()).hexdigest()
    return hash_md5 + ".json"

def obtener_keywords_inteligentes(nombre, descripcion, sector):
    if DETECTOR_DISPONIBLE and detectar_sector_completo:
        try:
            resultado = detectar_sector_completo(nombre, descripcion, sector)
            return resultado.get("keywords_imagenes", ["professional business"])
        except Exception: pass
    return ["professional business", "modern office", "business team"]

def generar_url_pollinations(prompt, width=1024, height=1024, seed=None):
    """
    Genera una URL de Pollinations usando el modelo 'flux' para maximo realismo.
    """
    if not prompt: prompt = "professional business product"
    
    # Añadimos palabras clave de calidad al prompt para forzar realismo
    prompt_mejorado = f"{prompt}, photorealistic, 8k resolution, highly detailed, cinematic lighting, professional photography, shot on 35mm lens, depth of field"
    prompt_encoded = urllib.parse.quote(prompt_mejorado)

    # Usamos model=flux y nologo=true
    url = (
        f"{POLLINATIONS_URL}/{prompt_encoded}"
        f"?width={width}&height={height}&model=flux&nologo=true&enhance=true"
    )
    if seed is not None: url += f"&seed={seed}"
    return url

def construir_prompt_imagen(negocio_info, variante="hero"):
    nombre = negocio_info.get("nombre", "")
    sector = negocio_info.get("sector", "")
    descripcion = negocio_info.get("descripcion", "")
    keywords = obtener_keywords_inteligentes(nombre, descripcion, sector)
    if not keywords: keywords = ["professional business"]

    if variante == "hero":
        tema = keywords[0]
        return f"wide angle shot of {tema}, dramatic lighting, high end commercial photography"
    elif variante == "producto":
        tema = keywords[1] if len(keywords) > 1 else keywords[0]
        return f"close up product photography of {tema}, studio lighting, macro detail"
    elif variante == "servicio":
        tema = keywords[2] if len(keywords) > 2 else keywords[0]
        return f"professional working environment of {tema}, natural light, candid shot"
    else:
        tema = keywords[0]
        return f"professional photo of {tema}, high quality"

def obtener_urls_imagenes_negocio(negocio_info, cantidad=5):
    urls = []
    variantes = ["hero", "producto", "servicio", "producto", "servicio"]
    for i in range(cantidad):
        variante = variantes[i % len(variantes)]
        prompt = construir_prompt_imagen(negocio_info, variante=variante)
        url = generar_url_pollinations(prompt, seed=i * 137)
        urls.append({
            "url_regular": url, "url_small": url, "url_thumb": url,
            "autor": "AI Generated", "descripcion": prompt,
            "fuente": "pollinations", "variante": variante,
        })
    return urls

def buscar_imagenes(query, cantidad=4, orientacion="landscape"):
    api_key = limpiar_api_key(obtener_api_key())
    if not api_key: return {"exito": False, "imagenes": [], "error": "UNSPLASH_ACCESS_KEY no configurada"}
    if not query or not query.strip(): return {"exito": False, "imagenes": [], "error": "Query vacio"}
    try:
        response = requests.get(
            UNSPLASH_API_URL + "/search/photos",
            headers={"Authorization": "Client-ID " + api_key},
            params={"query": query, "per_page": min(cantidad, 30), "orientation": orientacion},
            timeout=TIMEOUT
        )
        if response.status_code != 200: return {"exito": False, "imagenes": [], "error": "Status " + str(response.status_code)}
        data = response.json()
        resultados = data.get("results", [])
        imagenes = []
        for r in resultados:
            imagenes.append({
                "url_regular": r["urls"].get("regular", ""), "url_small": r["urls"].get("small", ""),
                "url_thumb": r["urls"].get("thumb", ""), "autor": r.get("user", {}).get("name", "Unsplash"),
                "descripcion": r.get("description") or r.get("alt_description") or query, "fuente": "unsplash",
            })
        return {"exito": True, "imagenes": imagenes, "error": None}
    except Exception as e: return {"exito": False, "imagenes": [], "error": str(e)}

def buscar_imagenes_por_texto(texto_negocio, cantidad=4):
    if not texto_negocio: return {"exito": False, "imagenes": [], "error": "Texto vacio"}
    palabras = extraer_palabras_clave(texto_negocio, max_palabras=3)
    if not palabras: return {"exito": False, "imagenes": [], "error": "Sin palabras clave"}
    query = " ".join(palabras)
    return buscar_imagenes(query, cantidad=cantidad)

def buscar_imagenes_sector(sector, cantidad=4, texto_negocio=""):
    if DETECTOR_DISPONIBLE and detectar_sector_completo:
        try:
            resultado = detectar_sector_completo(texto_negocio[:50] if texto_negocio else "", texto_negocio, sector)
            keywords = resultado.get("keywords_imagenes", [])
            api_key = limpiar_api_key(obtener_api_key())
            if api_key:
                for kw in keywords:
                    resultado_busqueda = buscar_imagenes(kw, cantidad=cantidad)
                    if resultado_busqueda["exito"] and len(resultado_busqueda["imagenes"]) > 0:
                        resultado_busqueda["keyword_usada"] = kw
                        return resultado_busqueda
        except Exception: pass
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
    if resultado["exito"] and len(resultado["imagenes"]) > 0: return resultado["imagenes"][0]
    return None

def buscar_servicios(sector, cantidad=6, texto_negocio=""):
    resultado = buscar_imagenes_sector(sector, cantidad=cantidad, texto_negocio=texto_negocio)
    if resultado["exito"]: return resultado["imagenes"]
    return []

def verificar_conexion():
    resultado = buscar_imagenes("test", cantidad=1)
    return resultado["exito"]

if __name__ == "__main__":
    print("Test Image Fetcher V5.0 (Flux Realism)")
    print("Modelo: flux | Calidad: photorealistic")