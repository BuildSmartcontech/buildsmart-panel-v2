# utils/image_fetcher.py
# ============================================
# BUSCADOR DE IMÁGENES - V10.0 (FALLBACK ESTÁTICO REAL)
# ============================================

from __future__ import annotations
import os, sys, re, json, time, hashlib, unicodedata, urllib.parse, logging, random
from dataclasses import asdict, dataclass
from html import escape as html_escape
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))
load_dotenv()

UNSPLASH_API_URL = "https://api.unsplash.com"
UNSPLASH_ACCESS_KEY = (os.getenv("UNSPLASH_ACCESS_KEY") or "").strip()

# IMÁGENES ESTÁTICAS GARANTIZADAS (URLs directas al CDN de Unsplash)
FALLBACK_IMAGES = {
    "viajes": [
        "https://images.unsplash.com/photo-1506744626753-143d4e0ce6b2?q=80&w=1200&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?q=80&w=1200&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1504280506221-7344a3b3c1a1?q=80&w=1200&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=1200&auto=format&fit=crop"
    ],
    "inmobiliaria": [
        "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=1200&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?q=80&w=1200&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1200&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?q=80&w=1200&auto=format&fit=crop"
    ],
    "negocios": [
        "https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=1200&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1497215728101-856f4ea42174?q=80&w=1200&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?q=80&w=1200&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1522071820081-009f0129c71c?q=80&w=1200&auto=format&fit=crop"
    ],
    "general": [
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1200&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=1200&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=1200&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1554147090-e1221a04a025?q=80&w=1200&auto=format&fit=crop"
    ]
}

@dataclass
class ImageResult:
    url_regular: str = ""
    url_small: str = ""
    url_thumb: str = ""
    autor: str = "Unknown"
    descripcion: str = ""
    fuente: str = "unknown"
    variante: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

def _obtener_fallback(categoria: str) -> str:
    """Devuelve una URL estática de Unsplash garantizada."""
    cat_limpia = categoria.lower().strip()
    if cat_limpia not in FALLBACK_IMAGES:
        cat_limpia = "general"
    return random.choice(FALLBACK_IMAGES[cat_limpia])

def buscar_imagenes(query: str, cantidad: int = 1, orientacion: str = "landscape") -> Dict[str, Any]:
    if not UNSPLASH_ACCESS_KEY:
        return {"exito": False, "imagenes": []}
    
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}", "Accept-Version": "v1"}
    params = {"query": query, "per_page": cantidad, "orientation": orientacion}
    
    try:
        r = requests.get(f"{UNSPLASH_API_URL}/search/photos", headers=headers, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            imagenes = []
            for item in data.get("results", [])[:cantidad]:
                urls = item.get("urls", {})
                imagenes.append(ImageResult(
                    url_regular=urls.get("regular", ""),
                    url_small=urls.get("small", ""),
                    url_thumb=urls.get("thumb", ""),
                    autor=item.get("user", {}).get("name", "Unsplash"),
                    descripcion=item.get("alt_description", query),
                    fuente="unsplash"
                ).to_dict())
            return {"exito": True, "imagenes": imagenes}
    except Exception as e:
        print(f"[IMAGE FETCHER] Error API Unsplash: {e}")
    
    return {"exito": False, "imagenes": []}

def obtener_urls_imagenes_negocio(negocio_info: Dict[str, Any], cantidad: int = 4) -> List[Dict[str, Any]]:
    # Determinamos la categoría basándonos en el sector
    sector_completo = negocio_info.get("sector", "").lower()
    categoria = "general"
    if "viaje" in sector_completo or "turismo" in sector_completo:
        categoria = "viajes"
    elif "inmobiliaria" in sector_completo or "propiedad" in sector_completo or "casa" in sector_completo:
        categoria = "inmobiliaria"
    elif "negocio" in sector_completo or "empresa" in sector_completo or "agencia" in sector_completo:
        categoria = "negocios"

    keywords = negocio_info.get("sector", "business").split() if negocio_info.get("sector") else ["business"]
    resultados = []

    # 1. HERO
    try:
        kw_hero = keywords[0] if keywords else "business"
        res_hero = buscar_imagenes(kw_hero + " wide shot", cantidad=1, orientacion="landscape")
        
        if res_hero.get("exito") and res_hero.get("imagenes"):
            img_hero = res_hero["imagenes"][0]
            img_hero["variante"] = "hero"
            resultados.append(img_hero)
        else:
            # FALLBACK GARANTIZADO
            url_hero = _obtener_fallback(categoria)
            resultados.append(ImageResult(url_regular=url_hero, url_small=url_hero, url_thumb=url_hero, autor="Fallback", fuente="fallback", variante="hero").to_dict())
    except Exception:
        url_hero = _obtener_fallback(categoria)
        resultados.append(ImageResult(url_regular=url_hero, url_small=url_hero, url_thumb=url_hero, autor="Fallback", fuente="fallback", variante="hero").to_dict())

    # 2. SERVICIOS
    for i in range(1, cantidad):
        kw = keywords[i % len(keywords)] if keywords else "business"
        res = buscar_imagenes(kw, cantidad=1, orientacion="landscape")
        
        if res.get("exito") and res.get("imagenes"):
            img = res["imagenes"][0]
            img["variante"] = "servicio"
            resultados.append(img)
        else:
            # FALLBACK GARANTIZADO
            url_serv = _obtener_fallback(categoria)
            resultados.append(ImageResult(url_regular=url_serv, url_small=url_serv, url_thumb=url_serv, autor="Fallback", fuente="fallback", variante="servicio").to_dict())

    return resultados