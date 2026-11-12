# utils/image_fetcher.py
# ============================================
# BUSCADOR DE IMÁGENES - V9.6 (FALLBACK GARANTIZADO)
# ============================================

from __future__ import annotations
import os, sys, re, json, time, hashlib, unicodedata, urllib.parse, logging
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

# IMÁGENES DE RESPALDO GARANTIZADAS (Por si la API falla o se bloquea)
FALLBACK_IMAGES = [
    "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?q=80&w=1000&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1506744626753-143d4e0ce6b2?q=80&w=1000&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1504280506221-7344a3b3c1a1?q=80&w=1000&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=1000&auto=format&fit=crop"
]

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

def buscar_imagenes(query: str, cantidad: int = 1, orientacion: str = "landscape") -> Dict[str, Any]:
    if not UNSPLASH_ACCESS_KEY:
        return {"exito": False, "imagenes": []}
    
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}", "Accept-Version": "v1"}
    params = {"query": query, "per_page": cantidad, "orientation": orientacion}
    
    try:
        r = requests.get(f"{UNSPLASH_API_URL}/search/photos", headers=headers, params=params, timeout=15)
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
    except Exception:
        pass
    return {"exito": False, "imagenes": []}

def _svg_placeholder(titulo: str, width: int = 900, height: int = 700) -> str:
    titulo = html_escape(str(titulo or "Imagen")[:80], quote=True)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"><rect width="100%" height="100%" fill="#0B0C14"/><text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle" font-family="Arial" font-size="30" fill="#14B8A6">{titulo}</text></svg>'
    return "data:image/svg+xml;charset=utf-8," + urllib.parse.quote(svg, safe="")

def obtener_urls_imagenes_negocio(negocio_info: Dict[str, Any], cantidad: int = 4) -> List[Dict[str, Any]]:
    sector_completo = negocio_info.get("sector", "business")
    keywords = sector_completo.split() if sector_completo else ["business"]
    
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
            url_hero = FALLBACK_IMAGES[0]
            resultados.append(ImageResult(url_regular=url_hero, url_small=url_hero, url_thumb=url_hero, autor="Fallback", fuente="fallback", variante="hero").to_dict())
    except Exception:
        resultados.append(ImageResult(**{"url_regular": _svg_placeholder("Hero"), "variante": "hero"}))

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
            url_serv = FALLBACK_IMAGES[i % len(FALLBACK_IMAGES)]
            resultados.append(ImageResult(url_regular=url_serv, url_small=url_serv, url_thumb=url_serv, autor="Fallback", fuente="fallback", variante="servicio").to_dict())

    return resultados