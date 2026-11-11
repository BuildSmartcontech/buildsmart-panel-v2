# utils/image_fetcher.py
# ============================================
# BUSCADOR DE IMÁGENES - V9.2 (UNIVERSAL)
# ============================================

from __future__ import annotations
import os, sys, re, json, time, hashlib, unicodedata, urllib.parse, logging, threading
from collections import deque
from dataclasses import asdict, dataclass
from html import escape as html_escape
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))
load_dotenv()

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    logger.addHandler(handler)

UNSPLASH_API_URL = "https://api.unsplash.com"
UNSPLASH_ACCESS_KEY = (os.getenv("UNSPLASH_ACCESS_KEY") or "").strip()
POLLINATIONS_URL = "https://image.pollinations.ai/prompt"
POLLINATIONS_MODEL = "flux"

DIMENSIONES = {
    "hero": (1200, 675),
    "servicio": (900, 700),
    "default": (900, 700)
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

def generar_url_pollinations(prompt: str, width=1200, height=675, seed=None):
    if not prompt: prompt = "professional business"
    prompt_mejorado = f"{prompt}, photorealistic, 8k, cinematic lighting, professional photography"
    prompt_encoded = urllib.parse.quote(prompt_mejorado)
    url = f"{POLLINATIONS_URL}/{prompt_encoded}?width={width}&height={height}&model={POLLINATIONS_MODEL}&nologo=true"
    if seed: url += f"&seed={seed}"
    return url

def _svg_placeholder(titulo: str, width: int = 900, height: int = 700) -> str:
    titulo = html_escape(str(titulo or "Imagen")[:80], quote=True)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"><rect width="100%" height="100%" fill="#0B0C14"/><text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle" font-family="Arial" font-size="30" fill="#14B8A6">{titulo}</text></svg>'
    return "data:image/svg+xml;charset=utf-8," + urllib.parse.quote(svg, safe="")

def obtener_urls_imagenes_negocio(negocio_info: Dict[str, Any], cantidad: int = 4) -> List[Dict[str, Any]]:
    # Aqui ya no hay logica de "Tech" o "Panaderia". Usamos lo que mando el Estratega.
    sector_completo = negocio_info.get("sector", "business")
    keywords = sector_completo.split() if sector_completo else ["business"]
    
    resultados = []

    # 1. HERO
    try:
        prompt_hero = f"wide angle shot of {keywords[0] if keywords else 'business'}, authentic professional environment"
        url_hero = generar_url_pollinations(prompt_hero, width=1200, height=675, seed=137)
        resultados.append(ImageResult(url_regular=url_hero, url_small=url_hero, url_thumb=url_hero, autor="Flux", fuente="pollinations", variante="hero").to_dict())
    except Exception:
        resultados.append(ImageResult(**{"url_regular": _svg_placeholder("Hero"), "variante": "hero"}))

    # 2. SERVICIOS
    for i in range(1, cantidad):
        # Tomamos las keywords que genero el Estratega
        kw = keywords[i % len(keywords)] if keywords else "business team"
        
        # Si las keywords tienen sentido, Unsplash devuelve fotos perfectas
        res = buscar_imagenes(kw, cantidad=1, orientacion="landscape")
        
        if res.get("exito") and res.get("imagenes"):
            img = res["imagenes"][0]
            img["variante"] = "servicio"
            resultados.append(img)
        else:
            resultados.append(ImageResult(url_regular=_svg_placeholder(kw), url_small=_svg_placeholder(kw), url_thumb=_svg_placeholder(kw), autor="Fallback", fuente="fallback", variante="servicio").to_dict())

    return resultados