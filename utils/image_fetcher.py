# utils/image_fetcher.py
# ============================================
# BUSCADOR DE IMÁGENES - V8.0 (HÍBRIDA ADAPTADA A NETLIFY)
# ============================================
# V8.0: Adaptado para usar URLs directas (sin /static/) para compatibilidad con Netlify.
# ============================================

from __future__ import annotations

import os
import sys
import re
import json
import time
import hashlib
import unicodedata
import urllib.parse
import logging
import threading
from collections import deque
from dataclasses import asdict, dataclass, fields
from html import escape as html_escape
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

load_dotenv()

def _truthy(value: Optional[str]) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "si", "on"}

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(os.getenv("IMAGE_LOG_LEVEL", "INFO").upper())

TIMEOUT = int(os.getenv("IMAGE_TIMEOUT", "20"))
RETRIES = int(os.getenv("IMAGE_RETRIES", "2"))
BACKOFF_FACTOR = float(os.getenv("IMAGE_BACKOFF_FACTOR", "1.6"))

UNSPLASH_API_URL = os.getenv("UNSPLASH_API_URL", "https://api.unsplash.com").rstrip("/")
UNSPLASH_ACCESS_KEY = (os.getenv("UNSPLASH_ACCESS_KEY") or "").strip()

POLLINATIONS_URL = os.getenv("POLLINATIONS_URL", "https://image.pollinations.ai/prompt").rstrip("/")
POLLINATIONS_MODEL = os.getenv("POLLINATIONS_MODEL", "flux")
POLLINATIONS_ENABLED = _truthy(os.getenv("POLLINATIONS_ENABLED", "true"))

POLLINATIONS_RATE_PER_MIN = int(os.getenv("POLLINATIONS_RATE_PER_MIN", "4"))
POLLINATIONS_BREAKER_FAILURES = int(os.getenv("POLLINATIONS_BREAKER_FAILURES", "3"))
POLLINATIONS_BREAKER_COOLDOWN = int(os.getenv("POLLINATIONS_BREAKER_COOLDOWN", "600"))

try:
    from utils.sector_detector import detectar_sector_completo, SECTORES_LOCALES
    DETECTOR_DISPONIBLE = True
except ImportError:
    DETECTOR_DISPONIBLE = False
    detectar_sector_completo = None
    SECTORES_LOCALES = {"default": {"keywords_imagenes": ["business", "office", "professional team"]}}

STOPWORDS = {
    "de", "la", "el", "los", "las", "un", "una", "unos", "unas", "y", "o", "u", "para", "con", "por", "en", "a", "al", "del",
    "que", "es", "son", "mi", "tu", "su", "se", "lo", "le", "empresa", "negocio", "servicio", "servicios", "producto", "productos",
    "somos", "hacemos", "ofrecemos", "vendemos", "tenemos", "nuestro", "general", "otros", "otras", "todo", "toda", "todos", "todas",
    "fabricamos", "distribuimos", "hace", "tiene", "tienen", "referencias", "tipo", "tipos", "clase", "clases",
    "the", "of", "and", "or", "for", "with", "by", "in", "to", "a", "an", "is", "are", "was", "were", "be", "been", "being",
}

DEFAULT_KEYWORDS = {
    "hero": ["modern office workspace", "professional business environment"],
    "producto": ["product photography", "premium detail", "clean background"],
    "servicio": ["customer service", "professional team", "consulting meeting"],
}

DIMENSIONES = {"hero": (1200, 675), "producto": (900, 900), "servicio": (900, 700), "default": (1024, 1024)}
VARIANTES_CICLO = ["hero", "producto", "servicio", "producto", "servicio", "hero", "producto", "servicio"]

@dataclass
class ImageResult:
    url_regular: str = ""
    url_small: str = ""
    url_thumb: str = ""
    autor: str = "Unknown"
    descripcion: str = ""
    fuente: str = "unknown"
    variante: str = ""
    credit_html: str = ""
    download_location: str = ""
    width: int = 0
    height: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class SlidingWindowRateLimiter:
    def __init__(self, max_calls: int, period_seconds: int = 60):
        self.max_calls = max(1, max_calls)
        self.period = max(1, period_seconds)
        self.calls: deque[float] = deque()
        self.lock = threading.Lock()
    def _purge(self, now: float) -> None:
        while self.calls and now - self.calls[0] > self.period:
            self.calls.popleft()
    def available(self) -> bool:
        now = time.monotonic()
        with self.lock:
            self._purge(now)
            return len(self.calls) < self.max_calls
    def allow(self) -> bool:
        now = time.monotonic()
        with self.lock:
            self._purge(now)
            if len(self.calls) < self.max_calls:
                self.calls.append(now)
                return True
            return False

class CircuitBreaker:
    def __init__(self, failure_threshold: int, recovery_timeout: int):
        self.failure_threshold = max(1, failure_threshold)
        self.recovery_timeout = max(1, recovery_timeout)
        self.failures = 0
        self.opened_at = 0.0
        self.half_open = False
        self.lock = threading.Lock()
    def allow(self) -> bool:
        now = time.monotonic()
        with self.lock:
            if self.failures >= self.failure_threshold:
                if now - self.opened_at < self.recovery_timeout:
                    return False
                self.half_open = True
            return True
    def record_success(self) -> None:
        with self.lock:
            self.failures = 0
            self.opened_at = 0.0
            self.half_open = False
    def record_failure(self) -> None:
        with self.lock:
            self.failures += 1
            if self.failures >= self.failure_threshold:
                self.opened_at = time.monotonic()
                self.half_open = False

pollinations_limiter = SlidingWindowRateLimiter(max_calls=POLLINATIONS_RATE_PER_MIN, period_seconds=60)
pollinations_breaker = CircuitBreaker(failure_threshold=POLLINATIONS_BREAKER_FAILURES, recovery_timeout=POLLINATIONS_BREAKER_COOLDOWN)

def _sin_acentos(texto: str) -> str:
    if not texto: return ""
    return "".join(ch for ch in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(ch))

def _cache_key(*parts: Any) -> str:
    raw = "|".join(str(p) for p in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def _stable_seed(*parts: Any) -> int:
    raw = "|".join(str(p) for p in parts).encode("utf-8")
    return int.from_bytes(hashlib.sha256(raw).digest()[:4], "big") % 2_000_000_000

def normalizar_sector(sector: Optional[str]) -> str:
    if not sector: return "default"
    s = _sin_acentos(str(sector)).lower().strip()
    s = re.sub(r"[^a-z0-9\s_-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    if s in SECTORES_LOCALES: return s
    for key in SECTORES_LOCALES:
        if key == "default": continue
        k = _sin_acentos(key).lower().replace("_", " ").strip()
        if k and (k in s or s in k): return key
    return "default"

def extraer_palabras_clave(texto: Optional[str], max_palabras: int = 4) -> List[str]:
    if not texto: return []
    texto = _sin_acentos(str(texto)).lower()
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    words = [w for w in texto.split() if len(w) > 3 and w not in STOPWORDS]
    seen = set()
    out: List[str] = []
    for w in words:
        if w not in seen:
            seen.add(w)
            out.append(w)
    return out[:max_palabras]

def _svg_placeholder(titulo: str, width: int = 1200, height: int = 675) -> str:
    titulo = html_escape(str(titulo or "Imagen no disponible")[:80], quote=True)
    font_size = max(16, min(int(width), int(height)) // 18)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="#0B0C14"/>'
        f'<stop offset="100%" stop-color="#14B8A6"/>'
        f'</linearGradient></defs>'
        f'<rect width="100%" height="100%" fill="url(#bg)"/>'
        f'<text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle" '
        f'font-family="Arial, Helvetica, sans-serif" font-size="{font_size}" '
        f'fill="#F8FAFC">{titulo}</text></svg>'
    )
    return "data:image/svg+xml;charset=utf-8," + urllib.parse.quote(svg, safe="")

def obtener_keywords_inteligentes(nombre: Optional[str], descripcion: Optional[str], sector: Optional[str]) -> List[str]:
    keywords: List[str] = []
    if DETECTOR_DISPONIBLE and detectar_sector_completo:
        try:
            resultado = detectar_sector_completo(nombre or "", descripcion or "", sector or "")
            if isinstance(resultado, dict):
                kw = resultado.get("keywords_imagenes") or []
                if isinstance(kw, list):
                    keywords.extend([str(x).strip() for x in kw if str(x).strip()])
        except Exception: pass
    if not keywords:
        norm = normalizar_sector(sector)
        sector_data = SECTORES_LOCALES.get(norm, {})
        kw = sector_data.get("keywords_imagenes", []) if isinstance(sector_data, dict) else []
        if isinstance(kw, list): keywords.extend([str(x).strip() for x in kw if str(x).strip()])
    if not keywords: keywords = extraer_palabras_clave(f"{nombre or ''} {descripcion or ''}", max_palabras=3)
    if not keywords: keywords = ["professional business", "modern office"]
    seen = set()
    clean: List[str] = []
    for k in keywords:
        k = k.strip()
        if k and k.lower() not in seen:
            seen.add(k.lower())
            clean.append(k)
    return clean[:8]

def construir_prompt_imagen(negocio_info: Dict[str, Any], variante: str = "hero", keywords: Optional[List[str]] = None) -> str:
    if keywords is None:
        keywords = obtener_keywords_inteligentes(negocio_info.get("nombre", ""), negocio_info.get("descripcion", ""), negocio_info.get("sector", ""))
    if not keywords: keywords = ["professional business"]
    if variante == "hero":
        return f"wide angle shot of {keywords[0]}, authentic professional environment, realistic people if appropriate, natural light, no text, no logo"
    if variante == "producto":
        tema = keywords[1] if len(keywords) > 1 else keywords[0]
        return f"close-up product photography of {tema}, clean neutral background, premium realistic detail, studio light, no text, no logo"
    if variante == "servicio":
        tema = keywords[2] if len(keywords) > 2 else keywords[0]
        return f"candid documentary shot of {tema} in service context, natural light, realistic workplace, no text, no logo"
    return f"professional realistic photo of {keywords[0]}, no text, no logo"

def _construir_url_pollinations(prompt: str, width: int, height: int, seed: Optional[int]) -> str:
    estilo = "photorealistic, professional commercial photography, natural lighting, realistic textures, sharp focus, 35mm lens, shallow depth of field, high detail, authentic"
    negativo = "blurry, low quality, watermark, text, logo, signature, distorted anatomy, extra fingers, cartoon, anime, painting, illustration, oversaturated, fake, cgi"
    full_prompt = f"{prompt}, {estilo}" if prompt else estilo
    params = {"width": width, "height": height, "model": POLLINATIONS_MODEL, "nologo": "true", "enhance": "true", "safe": "true", "negative_prompt": negativo}
    if seed is not None: params["seed"] = seed
    encoded_prompt = urllib.parse.quote(full_prompt, safe="")
    query = urllib.parse.urlencode(params)
    return f"{POLLINATIONS_URL}/{encoded_prompt}?{query}"

def _pollinations_generate(prompt: str, width: int, height: int, seed: Optional[int] = None, contexto: str = "") -> str:
    if not POLLINATIONS_ENABLED: raise RuntimeError("Pollinations deshabilitado")
    if not pollinations_breaker.allow(): raise RuntimeError("Pollinations en cooldown")
    if not pollinations_limiter.allow(): raise RuntimeError("Rate limit de Pollinations")
    try:
        url = _construir_url_pollinations(prompt, width, height, seed)
        pollinations_breaker.record_success()
        return url
    except Exception:
        pollinations_breaker.record_failure()
        raise

def buscar_imagenes(query: str, cantidad: int = 4, orientacion: str = "landscape") -> Dict[str, Any]:
    if not UNSPLASH_ACCESS_KEY:
        return {"exito": False, "imagenes": [], "error": "UNSPLASH_ACCESS_KEY no configurada"}
    query = (query or "").strip()
    if not query: return {"exito": False, "imagenes": [], "error": "Query vacio"}
    cantidad = max(1, min(int(cantidad), 30))
    if orientacion not in {"landscape", "portrait", "squarish"}: orientacion = "landscape"
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}", "Accept-Version": "v1"}
    params = {"query": query, "per_page": cantidad, "orientation": orientacion}
    for intento in range(RETRIES + 1):
        try:
            r = requests.get(f"{UNSPLASH_API_URL}/search/photos", headers=headers, params=params, timeout=TIMEOUT)
            if r.status_code == 429:
                time.sleep(min(int(r.headers.get("Retry-After", 5)), 30))
                continue
            if r.status_code >= 400:
                time.sleep(BACKOFF_FACTOR ** intento)
                continue
            data = r.json()
            imagenes: List[Dict[str, Any]] = []
            for item in data.get("results", [])[:cantidad]:
                urls = item.get("urls", {})
                user = item.get("user", {})
                imagenes.append(ImageResult(
                    url_regular=urls.get("regular", ""), url_small=urls.get("small", ""),
                    url_thumb=urls.get("thumb", ""), autor=user.get("name", "Unsplash"),
                    descripcion=item.get("alt_description", query), fuente="unsplash",
                    width=int(item.get("width", 0)), height=int(item.get("height", 0))
                ).to_dict())
            if not imagenes: return {"exito": False, "imagenes": [], "error": "Sin resultados"}
            return {"exito": True, "imagenes": imagenes, "error": None}
        except Exception:
            time.sleep(BACKOFF_FACTOR ** intento)
    return {"exito": False, "imagenes": [], "error": "Error de red"}

def _fallback_image_dict(variante: str, width: int, height: int, titulo: str = "") -> Dict[str, Any]:
    url = _svg_placeholder(titulo or variante.capitalize(), width, height)
    return ImageResult(url_regular=url, url_small=url, url_thumb=url, autor="Fallback", fuente="fallback", variante=variante).to_dict()

def obtener_urls_imagenes_negocio(negocio_info: Dict[str, Any], cantidad: int = 4, orientacion: str = "landscape") -> List[Dict[str, Any]]:
    cantidad = max(1, min(int(cantidad), 12))
    nombre = negocio_info.get("nombre", "negocio")
    keywords = obtener_keywords_inteligentes(nombre, negocio_info.get("descripcion", ""), negocio_info.get("sector", ""))
    resultados: List[Dict[str, Any]] = []
    for i in range(cantidad):
        variante = VARIANTES_CICLO[i % len(VARIANTES_CICLO)]
        width, height = DIMENSIONES.get(variante, DIMENSIONES["default"])
        item: Optional[ImageResult] = None

        # 1) Pollinations (Solo si es hero o no hay Unsplash)
        if (variante == "hero" or not UNSPLASH_ACCESS_KEY) and POLLINATIONS_ENABLED:
            try:
                prompt = construir_prompt_imagen(negocio_info, variante, keywords)
                seed = _stable_seed(nombre, variante, i)
                url = _pollinations_generate(prompt, width, height, seed, nombre)
                item = ImageResult(url_regular=url, url_small=url, url_thumb=url, autor="Flux", fuente="pollinations", variante=variante)
            except Exception: pass

        # 2) Unsplash
        if item is None and UNSPLASH_ACCESS_KEY:
            query = f"{keywords[i % len(keywords)]} {variante}"
            bus = buscar_imagenes(query, cantidad=1, orientacion=orientacion)
            if bus.get("exito") and bus.get("imagenes"):
                d = dict(bus["imagenes"][0]); d["variante"] = variante
                item = ImageResult(**d)

        # 3) Fallback SVG
        if item is None:
            item = ImageResult(**_fallback_image_dict(variante, width, height, keywords[0]))

        resultados.append(item.to_dict())
    return resultados