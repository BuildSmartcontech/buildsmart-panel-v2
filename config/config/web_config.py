# config/web_config.py
# ============================================
# CONFIGURACIÓN DEL MÓDULO DE PÁGINAS WEB
# ============================================
# Este archivo es la ÚNICA configuración que necesitas tocar.
# Cuando definas tu modelo de negocio, solo llenas la sección PRECIOS.
# ============================================

import os

# ============================================
# CONFIGURACIÓN GENERAL
# ============================================

CONFIG = {
    # --- Expiración de webs ---
    "dias_gratis": 30,
    "dias_gracia": 30,
    "alertas_dias": [15, 25, 29],
    
    # --- Tipos de usuario ---
    "tipos_usuario": ["solo_pagina", "negocio", "empresa"],
    "tipo_por_defecto": "solo_pagina",
    
    # --- Descarga de código ---
    "descarga_gratis_para": ["solo_pagina"],
    "descarga_pago_para": ["negocio", "empresa"],
    
    # --- IA (usa el gateway existente) ---
    "modelo_generacion": "chat_inteligente",
    "modelo_edicion": "chat_inteligente",
    "max_tokens_generacion": 8000,
    "max_tokens_edicion": 4000,
    "temperatura": 0.7,
    
    # --- Validación ---
    "validar_html": True,
    "validar_css": True,
    "min_caracteres_html": 500,
    "max_caracteres_html": 500000,
    
    # --- Publicación ---
    "publisher": "netlify",
    "subdominio_base": "buildsmart.app",
    "subdominio_prefijo": "web",
    
    # --- Rutas (cloud-ready) ---
    "carpeta_webs": "data/webs_generadas",
    "carpeta_zips": "data/zips",
    "carpeta_temporal": "/tmp/webs",
    
    # --- Límites ---
    "max_webs_por_usuario": 100,
    "max_intentos_generacion": 3,
    
    # --- Cache ---
    "usar_cache": True,
    "ttl_cache_segundos": 3600,
}

# ============================================
# PRECIOS (VACÍOS HASTA QUE DEFINAS TU MODELO DE NEGOCIO)
# ============================================

PRECIOS = {
    "web_extra": 0,
    "descarga_html": 0,
    "plan_premium_mensual": 0,
    "recuperacion": 0,
    "hosting_propio": 0,
}

# ============================================
# OPCIONES DE DISEÑO WEB (56 OPCIONES EN 6 CATEGORÍAS)
# ============================================

OPCIONES_DISENO = {
    # --- 1. TIPO DE PÁGINA (7 opciones) ---
    "tipo_pagina": [
        "Landing Page",
        "Sitio Corporativo",
        "Portafolio",
        "Blog",
        "E-commerce",
        "Catálogo",
        "One Page"
    ],
    
    # --- 2. DISEÑO VISUAL (8 opciones) ---
    "diseno_visual": [
        "Moderno",
        "Corporativo",
        "Creativo",
        "Elegante",
        "Tecnológico",
        "Natural",
        "Retro",
        "Brutalista"
    ],
    
    # --- 3. TONO DE COMUNICACIÓN (8 opciones) ---
    "tono": [
        "Profesional",
        "Cercano",
        "Técnico",
        "Inspirador",
        "Directo",
        "Divertido",
        "Formal",
        "Casual"
    ],
    
    # --- 4. SECCIONES A INCLUIR (13 opciones) ---
    "secciones": [
        "Hero",
        "Sobre Nosotros",
        "Servicios",
        "Proyectos",
        "Testimonios",
        "Equipo",
        "Precios",
        "Blog",
        "FAQ",
        "Contacto",
        "Galería",
        "Mapa",
        "Redes Sociales"
    ],
    
    # --- 5. LÓGICA DE LA PÁGINA (8 opciones) ---
    "logica": [
        "Estática",
        "Formulario de contacto",
        "WhatsApp directo",
        "Calendario de citas",
        "Catálogo con filtros",
        "Multi-idioma",
        "Blog dinámico",
        "Login de usuarios"
    ],
    
    # --- 6. FUNCIONALIDADES ESPECIALES (12 opciones) ---
    "funcionalidades": [
        "Blog integrado",
        "Galería de imágenes",
        "Video de fondo",
        "Animaciones",
        "Chat en vivo",
        "SEO optimizado",
        "Google Analytics",
        "Modo oscuro",
        "Multi-página",
        "Formulario avanzado",
        "Integración con redes",
        "PWA"
    ],
}

# ============================================
# ESTADOS DE LAS WEBS
# ============================================

ESTADOS_WEB = {
    "activa": "Web activa y visible",
    "por_expirar": "Web próxima a expirar",
    "expirada": "Web expirada (período de gracia)",
    "borrada": "Web eliminada",
}

# ============================================
# MENSAJES DEL SISTEMA
# ============================================

MENSAJES = {
    "web_creada": "Web creada exitosamente",
    "web_editada": "Web actualizada",
    "web_publicada": "Web en linea",
    "web_descargada": "Web descargada",
    "web_expirada": "Web expirada",
    "alerta_15": "Tu web expira en 15 dias. Descargala o pasa a Premium!",
    "alerta_25": "Tu web expira en 5 dias. Ultima oportunidad!",
    "alerta_29": "ULTIMO DIA! Tu web expira manana",
    "web_borrada": "Web eliminada",
}

# ============================================
# VALIDACIÓN DE CONFIGURACIÓN
# ============================================

def validar_config():
    """Valida que la configuración sea coherente"""
    errores = []
    
    if CONFIG["dias_gratis"] <= 0:
        errores.append("dias_gratis debe ser > 0")
    if CONFIG["dias_gracia"] < 0:
        errores.append("dias_gracia no puede ser negativo")
    
    for dia in CONFIG["alertas_dias"]:
        if dia >= CONFIG["dias_gratis"]:
            errores.append(f"alerta del dia {dia} debe ser < {CONFIG['dias_gratis']}")
    
    if len(OPCIONES_DISENO["tipo_pagina"]) != 7:
        errores.append("tipo_pagina debe tener 7 opciones")
    if len(OPCIONES_DISENO["diseno_visual"]) != 8:
        errores.append("diseno_visual debe tener 8 opciones")
    if len(OPCIONES_DISENO["tono"]) != 8:
        errores.append("tono debe tener 8 opciones")
    
    return errores

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def obtener_precio(concepto: str) -> float:
    """Obtiene el precio de un concepto (0 si no está definido)"""
    return PRECIOS.get(concepto, 0)

def es_gratis(concepto: str) -> bool:
    """Verifica si un concepto es gratis (precio = 0)"""
    return obtener_precio(concepto) == 0

# ============================================
# PRUEBA
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("VALIDANDO CONFIGURACION")
    print("=" * 60)
    
    errores = validar_config()
    if errores:
        print("ERRORES ENCONTRADOS:")
        for error in errores:
            print(f"   - {error}")
    else:
        print("Configuracion valida")
    
    print(f"\nResumen:")
    print(f"   Dias gratis: {CONFIG['dias_gratis']}")
    print(f"   Dias gracia: {CONFIG['dias_gracia']}")
    print(f"   Alertas: {CONFIG['alertas_dias']}")
    print(f"   Tipos usuario: {CONFIG['tipos_usuario']}")
    print(f"   Publisher: {CONFIG['publisher']}")
    print(f"   Total opciones diseno: {sum(len(v) for v in OPCIONES_DISENO.values())}")
    
    print(f"\nPrecios (vacios hasta definir modelo de negocio):")
    for concepto, precio in PRECIOS.items():
        estado = "GRATIS" if precio == 0 else f"${precio}"
        print(f"   {concepto}: {estado}")