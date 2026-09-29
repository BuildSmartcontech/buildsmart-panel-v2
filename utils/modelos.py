# utils/modelos.py - Inventario Completo de IA Verificadas
# ==========================================================
# Última actualización: 2026-09-09
# Versión: 2.0 - Arquitectura C

MODELOS_FUNCIONALES = {
    # ============================================
    # 1. GROQ (Rápido - Gratis) ✅
    # ============================================
    "groq_llama3_8b": {
        "nombre": "Llama 3.1 8B",
        "proveedor": "Meta (Groq)",
        "identificador": "groq/llama-3.1-8b-instant",
        "descripcion": "Modelo rápido y gratuito. Ideal para respuestas rápidas.",
        "contexto": "8K tokens",
        "gratuito": True,
        "fuente": "groq",
        "categoria": "texto",
        "rol": "work",
        "probado": True
    },
    "groq_qwen3_27b": {
        "nombre": "Qwen 3.6 27B",
        "proveedor": "Alibaba (Groq)",
        "identificador": "qwen/qwen3.6-27b",
        "descripcion": "Modelo de Qwen en Groq. Buen equilibrio calidad/velocidad.",
        "contexto": "8K tokens",
        "gratuito": True,
        "fuente": "groq",
        "categoria": "texto",
        "rol": "work",
        "probado": True
    },
    
    # ============================================
    # 2. OPENROUTER (Gratis - Contexto largo) ✅
    # ============================================
    "nvidia_nemotron": {
        "nombre": "NVIDIA Nemotron 3 Super 120B",
        "proveedor": "NVIDIA (OpenRouter)",
        "identificador": "nvidia/nemotron-3-super-120b-a12b:free",
        "descripcion": "Modelo gratuito con 1M de contexto. Excelente para planificación.",
        "contexto": "1M tokens",
        "gratuito": True,
        "fuente": "openrouter",
        "categoria": "texto",
        "rol": "brainstorm",
        "probado": True
    },
    "llama3_2_3b_or": {
        "nombre": "Llama 3.2 3B",
        "proveedor": "Meta (OpenRouter)",
        "identificador": "meta-llama/llama-3.2-3b-instruct:free",
        "descripcion": "Modelo gratuito de Meta. Rápido y eficiente.",
        "contexto": "128K tokens",
        "gratuito": True,
        "fuente": "openrouter",
        "categoria": "texto",
        "rol": "general",
        "probado": True
    },
    
    # ============================================
    # 3. GOOGLE GEMINI (Multimodal - Gratis) ✅
    # ============================================
    "gemini_flash_lite": {
        "nombre": "Gemini 3.1 Flash-Lite",
        "proveedor": "Google",
        "identificador": "gemini/gemini-3.1-flash-lite",
        "descripcion": "Modelo multimodal gratuito. Procesa texto, imágenes, audio y video.",
        "contexto": "1M tokens",
        "gratuito": True,
        "fuente": "gemini",
        "categoria": "multimodal",
        "rol": "compound",
        "probado": True
    },
    "gemini_flash_lite_image": {
        "nombre": "Gemini 3.1 Flash-Lite Image",
        "proveedor": "Google",
        "identificador": "gemini/gemini-3.1-flash-lite-image",
        "descripcion": "Generación de imágenes con Gemini (500/día gratis).",
        "contexto": "-",
        "gratuito": True,
        "fuente": "gemini",
        "categoria": "imagen",
        "rol": "imagen",
        "probado": True
    },
    
    # ============================================
    # 4. DEEPSEEK (Con saldo - Razonamiento) ✅
    # ============================================
    "deepseek_chat": {
        "nombre": "DeepSeek Chat",
        "proveedor": "DeepSeek",
        "identificador": "deepseek/deepseek-chat",
        "descripcion": "Modelo de chat general de DeepSeek (requiere saldo).",
        "contexto": "64K tokens",
        "gratuito": False,
        "fuente": "deepseek",
        "categoria": "texto",
        "rol": "plan",
        "probado": True
    },
    "deepseek_reasoner": {
        "nombre": "DeepSeek Reasoner",
        "proveedor": "DeepSeek",
        "identificador": "deepseek/deepseek-reasoner",
        "descripcion": "Especialista en razonamiento profundo y análisis crítico.",
        "contexto": "64K tokens",
        "gratuito": False,
        "fuente": "deepseek",
        "categoria": "texto",
        "rol": "review",
        "probado": True
    },
    "deepseek_v4_flash": {
        "nombre": "DeepSeek V4 Flash",
        "proveedor": "DeepSeek",
        "identificador": "deepseek/deepseek-v4-flash",
        "descripcion": "Versión rápida de DeepSeek. Ideal para respuestas rápidas.",
        "contexto": "64K tokens",
        "gratuito": False,
        "fuente": "deepseek",
        "categoria": "texto",
        "rol": "work",
        "probado": True
    },
    "deepseek_v4_pro": {
        "nombre": "DeepSeek V4 Pro",
        "proveedor": "DeepSeek",
        "identificador": "deepseek/deepseek-v4-pro",
        "descripcion": "Versión premium de DeepSeek. Máxima calidad.",
        "contexto": "64K tokens",
        "gratuito": False,
        "fuente": "deepseek",
        "categoria": "texto",
        "rol": "compound",
        "probado": True
    },
    
    # ============================================
    # 5. HERRAMIENTAS ✅
    # ============================================
    "edge_tts": {
        "nombre": "Edge-TTS",
        "proveedor": "Microsoft",
        "identificador": "edge-tts",
        "descripcion": "Texto a voz gratuito sin límites.",
        "contexto": "-",
        "gratuito": True,
        "fuente": "local",
        "categoria": "voz",
        "rol": "voz",
        "probado": True
    },
    "kling_ai": {
        "nombre": "Kling AI",
        "proveedor": "Kling AI",
        "identificador": "kling-v3",
        "descripcion": "Generación de video desde texto (requiere créditos).",
        "contexto": "-",
        "gratuito": False,
        "fuente": "kling",
        "categoria": "video",
        "rol": "video",
        "probado": False
    },
    "duckduckgo": {
        "nombre": "DuckDuckGo",
        "proveedor": "DuckDuckGo",
        "identificador": "duckduckgo",
        "descripcion": "Búsqueda en tiempo real (gratuita, sin clave).",
        "contexto": "-",
        "gratuito": True,
        "fuente": "local",
        "categoria": "busqueda",
        "rol": "busqueda",
        "probado": True
    }
}

# ============================================
# ORDEN DE PRIORIDAD PARA LA ARQUITECTURA C
# ============================================

ORDEN_PRIORIDAD = [
    "groq_llama3_8b",       # #1 Trabajo rápido
    "groq_qwen3_27b",       # #2 Alternativa rápida
    "nvidia_nemotron",      # #3 Razonamiento profundo
    "gemini_flash_lite",    # #4 Multimodal
    "llama3_2_3b_or",       # #5 Generalista
    "deepseek_chat",        # #6 Planificación
    "deepseek_reasoner",    # #7 Razonamiento
    "deepseek_v4_flash",    # #8 Rápido (DeepSeek)
    "deepseek_v4_pro",      # #9 Premium
]

# ============================================
# ROLES EN LA ARQUITECTURA C
# ============================================

ROLES = {
    "brainstorm": ["nvidia_nemotron", "deepseek_reasoner"],
    "plan": ["deepseek_chat", "nvidia_nemotron", "llama3_2_3b_or"],
    "work": ["groq_llama3_8b", "groq_qwen3_27b", "deepseek_v4_flash"],
    "review": ["deepseek_reasoner", "nvidia_nemotron"],
    "compound": ["gemini_flash_lite", "deepseek_v4_pro"],
    "imagen": ["gemini_flash_lite_image"],
    "video": ["kling_ai"],
    "voz": ["edge_tts"],
    "busqueda": ["duckduckgo"]
}

# ============================================
# FUNCIONES
# ============================================

def get_modelo(identificador):
    """Obtener configuración de un modelo por su identificador"""
    for key, modelo in MODELOS_FUNCIONALES.items():
        if modelo["identificador"] == identificador:
            return modelo
    return None

def get_modelo_por_nombre(nombre):
    """Obtener modelo por nombre clave"""
    return MODELOS_FUNCIONALES.get(nombre)

def listar_modelos():
    """Listar todos los modelos disponibles"""
    return MODELOS_FUNCIONALES

def listar_modelos_ordenados():
    """Listar modelos en orden de prioridad"""
    return [MODELOS_FUNCIONALES[key] for key in ORDEN_PRIORIDAD if key in MODELOS_FUNCIONALES]

def get_modelos_por_rol(rol):
    """Obtener modelos por rol en la Arquitectura C"""
    keys = ROLES.get(rol, [])
    return [MODELOS_FUNCIONALES[key] for key in keys if key in MODELOS_FUNCIONALES]

def get_mejor_modelo_por_rol(rol):
    """Obtener el mejor modelo para un rol"""
    modelos = get_modelos_por_rol(rol)
    gratis = [m for m in modelos if m.get("gratuito", False)]
    pago = [m for m in modelos if not m.get("gratuito", False)]
    return (gratis + pago)[0] if gratis or pago else None

def get_modelos_probados():
    """Obtener solo modelos que han sido probados y funcionan"""
    return {k: v for k, v in MODELOS_FUNCIONALES.items() if v.get("probado", False)}

def get_modelos_por_categoria(categoria):
    """Obtener modelos por categoría"""
    return {k: v for k, v in MODELOS_FUNCIONALES.items() if v.get("categoria") == categoria}

# ============================================
# PRUEBA
# ============================================
if __name__ == "__main__":
    print("=" * 60)
    print("📋 INVENTARIO COMPLETO DE IA PARA ARQUITECTURA C")
    print("=" * 60)
    
    print("\n✅ Modelos Funcionales:")
    for modelo in listar_modelos_ordenados():
        gratis = "✅ Gratis" if modelo.get("gratuito", False) else "💰 Pago"
        probado = "✅" if modelo.get("probado", False) else "⏳"
        print(f"  [{probado}] {modelo['nombre']} ({gratis}) - {modelo['fuente']}")
    
    print("\n🎯 Roles en la Arquitectura C:")
    for rol, keys in ROLES.items():
        print(f"  - {rol}: {', '.join(keys)}")
    
    print("\n🏆 Mejor modelo por rol:")
    for rol in ROLES.keys():
        mejor = get_mejor_modelo_por_rol(rol)
        if mejor:
            print(f"  - {rol}: {mejor['nombre']} ({mejor['fuente']})")
    
    print("\n📊 Resumen:")
    total = len(MODELOS_FUNCIONALES)
    probados = len(get_modelos_probados())
    print(f"  Total modelos: {total}")
    print(f"  Modelos probados: {probados}")
    print(f"  Modelos pendientes: {total - probados}")