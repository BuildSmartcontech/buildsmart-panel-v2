# utils/security.py
# ============================================
# MÓDULO DE SEGURIDAD (SANITIZACIÓN)
# ============================================

import re
from PIL import Image
import io

def sanitizar_input_ia(texto: str) -> str:
    """Limpia el texto del usuario para evitar Prompt Injection."""
    if not texto:
        return ""
    # Eliminar etiquetas HTML y scripts
    texto_limpio = re.sub(r'<[^>]*>', '', texto)
    # Eliminar palabras clave maliciosas comunes
    palabras_prohibidas = ["ignore previous instructions", "system prompt", "api_key", "openai_api_key", "groq_api_key"]
    for palabra in palabras_prohibidas:
        texto_limpio = re.sub(palabra, "***", texto_limpio, flags=re.IGNORECASE)
    # Limitar longitud
    return texto_limpio[:1000]

def validar_imagen_subida(file, max_mb=5) -> tuple[bool, str]:
    """Valida que el archivo sea una imagen y no supere el peso máximo."""
    if not file:
        return True, "Sin archivo"
        
    # Validar tamaño
    file_size_mb = len(file.getvalue()) / (1024 * 1024)
    if file_size_mb > max_mb:
        return False, f"La imagen supera el límite de {max_mb}MB."
        
    # Validar que sea una imagen real (no un .exe renombrado)
    try:
        img = Image.open(io.BytesIO(file.getvalue()))
        img.verify() # Verifica que el archivo sea una imagen válida
    except Exception:
        return False, "El archivo no es una imagen válida."
        
    return True, "OK"