# utils/business_detector.py
# ============================================
# DETECTOR AUTOMATICO DE SECTOR DE NEGOCIO
# ============================================
# Analiza una descripcion de negocio y detecta:
# - Sector (construccion, panaderia, abogados, etc.)
# - Tipo de pagina recomendado
# - Diseno recomendado
# - Tono recomendado
# - Secciones recomendadas
# ============================================

import re


# ============================================
# BASE DE CONOCIMIENTO DE SECTORES
# ============================================

SECTORES = {
    "construccion": {
        "keywords": ["construccion", "construir", "obra", "edificio", "arquitectura",
                     "reforma", "albañil", "casa", "edificar", "proyecto civil"],
        "tipo_pagina": "Landing Page",
        "diseno": "Moderno",
        "tono": "Profesional",
        "secciones": ["Hero", "Servicios", "Proyectos", "Sobre Nosotros", "Testimonios", "Contacto"],
    },
    "panaderia": {
        "keywords": ["panaderia", "pan", "pasteleria", "pastel", "bolleria",
                     "reposteria", "postre", "torta", "cupcake", "bakery"],
        "tipo_pagina": "Landing Page",
        "diseno": "Natural",
        "tono": "Cercano",
        "secciones": ["Hero", "Productos", "Sobre Nosotros", "Testimonios", "Contacto"],
    },
    "restaurante": {
        "keywords": ["restaurante", "restaurant", "comida", "cocina", "chef",
                     "menu", "plato", "bar", "cafeteria", "cafe"],
        "tipo_pagina": "Landing Page",
        "diseno": "Elegante",
        "tono": "Cercano",
        "secciones": ["Hero", "Menu", "Sobre Nosotros", "Galeria", "Testimonios", "Contacto"],
    },
    "abogados": {
        "keywords": ["abogado", "abogados", "juridico", "legal", "ley", "leyes",
                     "bufete", "notario", "demanda", "asesoria legal", "juridica"],
        "tipo_pagina": "Sitio Corporativo",
        "diseno": "Corporativo",
        "tono": "Formal",
        "secciones": ["Hero", "Servicios", "Equipo", "Casos", "Testimonios", "Contacto"],
    },
    "medicos": {
        "keywords": ["medico", "medicos", "clinica", "hospital", "salud",
                     "doctor", "consulta", "paciente", "tratamiento", "cirugia"],
        "tipo_pagina": "Sitio Corporativo",
        "diseno": "Moderno",
        "tono": "Profesional",
        "secciones": ["Hero", "Servicios", "Equipo", "Testimonios", "FAQ", "Contacto"],
    },
    "dentistas": {
        "keywords": ["dentista", "dental", "odontologia", "odontologo",
                     "diente", "brackets", "ortodoncia", "sonrisa", "implante"],
        "tipo_pagina": "Landing Page",
        "diseno": "Moderno",
        "tono": "Cercano",
        "secciones": ["Hero", "Servicios", "Equipo", "Testimonios", "FAQ", "Contacto"],
    },
    "tecnologia": {
        "keywords": ["tecnologia", "software", "app", "aplicacion", "web",
                     "digital", "sistema", "programacion", "desarrollo", "ti", "informatica"],
        "tipo_pagina": "Landing Page",
        "diseno": "Tecnologico",
        "tono": "Directo",
        "secciones": ["Hero", "Productos", "Servicios", "Sobre Nosotros", "Precios", "FAQ", "Contacto"],
    },
    "marketing": {
        "keywords": ["marketing", "publicidad", "branding", "redes sociales",
                     "seo", "campaña", "agencia", "digital", "contenido"],
        "tipo_pagina": "Landing Page",
        "diseno": "Creativo",
        "tono": "Inspirador",
        "secciones": ["Hero", "Servicios", "Proyectos", "Sobre Nosotros", "Testimonios", "Contacto"],
    },
    "diseno": {
        "keywords": ["diseno", "diseñador", "grafico", "grafica", "branding",
                     "logo", "creatividad", "ilustracion", "arte digital", "web design"],
        "tipo_pagina": "Portafolio",
        "diseno": "Creativo",
        "tono": "Inspirador",
        "secciones": ["Hero", "Proyectos", "Servicios", "Sobre Nosotros", "Contacto"],
    },
    "fotografia": {
        "keywords": ["fotografia", "fotografo", "camara", "estudio",
                     "sesion", "boda", "evento", "retrato", "book", "photos"],
        "tipo_pagina": "Portafolio",
        "diseno": "Elegante",
        "tono": "Inspirador",
        "secciones": ["Hero", "Galeria", "Proyectos", "Servicios", "Sobre Nosotros", "Contacto"],
    },
    "moda": {
        "keywords": ["moda", "ropa", "boutique", "tienda de ropa", "fashion",
                     "estilo", "tendencia", "vestidos", "coleccion", "indumentaria"],
        "tipo_pagina": "E-commerce",
        "diseno": "Elegante",
        "tono": "Inspirador",
        "secciones": ["Hero", "Productos", "Colecciones", "Sobre Nosotros", "Contacto"],
    },
    "belleza": {
        "keywords": ["belleza", "estetica", "salon", "spa", "maquillaje",
                     "cosmeticos", "peluqueria", "uñas", "manicure", "belleza integral"],
        "tipo_pagina": "Landing Page",
        "diseno": "Elegante",
        "tono": "Cercano",
        "secciones": ["Hero", "Servicios", "Galeria", "Precios", "Testimonios", "Contacto"],
    },
    "gimnasio": {
        "keywords": ["gimnasio", "gym", "fitness", "entrenamiento", "crossfit",
                     "deporte", "musculacion", "pesas", "cardio", "personal trainer"],
        "tipo_pagina": "Landing Page",
        "diseno": "Tecnologico",
        "tono": "Inspirador",
        "secciones": ["Hero", "Servicios", "Planes", "Equipo", "Testimonios", "Contacto"],
    },
    "educacion": {
        "keywords": ["educacion", "escuela", "colegio", "universidad", "academia",
                     "curso", "clase", "profesor", "estudiante", "formacion", "capacitacion"],
        "tipo_pagina": "Sitio Corporativo",
        "diseno": "Corporativo",
        "tono": "Profesional",
        "secciones": ["Hero", "Programas", "Sobre Nosotros", "Equipo", "Testimonios", "Contacto"],
    },
    "inmobiliaria": {
        "keywords": ["inmobiliaria", "bienes raices", "propiedades", "casa",
                     "apartamento", "venta", "alquiler", "arriendo", "real estate", "propiedad"],
        "tipo_pagina": "Landing Page",
        "diseno": "Corporativo",
        "tono": "Profesional",
        "secciones": ["Hero", "Propiedades", "Servicios", "Sobre Nosotros", "Testimonios", "Contacto"],
    },
    "transporte": {
        "keywords": ["transporte", "logistica", "envio", "carga", "camion",
                     "mudanza", "delivery", "mensajeria", "flete", "shipping"],
        "tipo_pagina": "Landing Page",
        "diseno": "Corporativo",
        "tono": "Directo",
        "secciones": ["Hero", "Servicios", "Cobertura", "Precios", "Sobre Nosotros", "Contacto"],
    },
    "turismo": {
        "keywords": ["turismo", "viaje", "agencia", "tour", "vacaciones",
                     "destino", "hotel", "reserva", "travel", "aventura"],
        "tipo_pagina": "Landing Page",
        "diseno": "Natural",
        "tono": "Inspirador",
        "secciones": ["Hero", "Destinos", "Paquetes", "Testimonios", "Galeria", "Contacto"],
    },
    "hotel": {
        "keywords": ["hotel", "hostal", "alojamiento", "hospedaje", "habitacion",
                     "suite", "resort", "posada", "cabaña", "hospedaria"],
        "tipo_pagina": "Landing Page",
        "diseno": "Elegante",
        "tono": "Cercano",
        "secciones": ["Hero", "Habitaciones", "Servicios", "Galeria", "Testimonios", "Contacto"],
    },
    "floristeria": {
        "keywords": ["floristeria", "flores", "ramos", "arreglos florales",
                     "plantas", "jardin", "flor", "bouquet", "decoracion floral"],
        "tipo_pagina": "Landing Page",
        "diseno": "Natural",
        "tono": "Cercano",
        "secciones": ["Hero", "Productos", "Ocasiones", "Sobre Nosotros", "Contacto"],
    },
    "joyeria": {
        "keywords": ["joyeria", "joyas", "oro", "plata", "anillo",
                     "collar", "pulsera", "reloj", "bisuteria", "diamante"],
        "tipo_pagina": "Landing Page",
        "diseno": "Elegante",
        "tono": "Profesional",
        "secciones": ["Hero", "Productos", "Colecciones", "Sobre Nosotros", "Contacto"],
    },
    "muebles": {
        "keywords": ["muebles", "muebleria", "mobiliario", "decoracion",
                     "interior", "hogar", "sala", "comedor", "cocina", "dormitorio"],
        "tipo_pagina": "Landing Page",
        "diseno": "Moderno",
        "tono": "Cercano",
        "secciones": ["Hero", "Productos", "Ambientes", "Sobre Nosotros", "Contacto"],
    },
    "veterinaria": {
        "keywords": ["veterinaria", "veterinario", "mascota", "perro", "gato",
                     "animal", "consulta", "vacuna", "peluqueria canina", "pet"],
        "tipo_pagina": "Landing Page",
        "diseno": "Natural",
        "tono": "Cercano",
        "secciones": ["Hero", "Servicios", "Equipo", "Testimonios", "FAQ", "Contacto"],
    },
    "contabilidad": {
        "keywords": ["contabilidad", "contador", "contable", "impuestos",
                     "auditoria", "fiscal", "finanzas", "tributario", "declaracion"],
        "tipo_pagina": "Sitio Corporativo",
        "diseno": "Corporativo",
        "tono": "Formal",
        "secciones": ["Hero", "Servicios", "Equipo", "Testimonios", "FAQ", "Contacto"],
    },
    "consultoria": {
        "keywords": ["consultoria", "consultor", "asesoria", "estrategia",
                     "business", "empresa", "management", "consulting", "coaching"],
        "tipo_pagina": "Sitio Corporativo",
        "diseno": "Corporativo",
        "tono": "Profesional",
        "secciones": ["Hero", "Servicios", "Casos", "Equipo", "Testimonios", "Contacto"],
    },
    "eventos": {
        "keywords": ["eventos", "fiesta", "boda", "cumpleaños", "celebracion",
                     "catering", "organizacion", "salon", "banquete", "party"],
        "tipo_pagina": "Landing Page",
        "diseno": "Elegante",
        "tono": "Inspirador",
        "secciones": ["Hero", "Servicios", "Galeria", "Testimonios", "Contacto"],
    },
}


# Sectores por defecto (si no se detecta nada)
SECTOR_DEFAULT = {
    "tipo_pagina": "Landing Page",
    "diseno": "Moderno",
    "tono": "Profesional",
    "secciones": ["Hero", "Servicios", "Sobre Nosotros", "Contacto"],
}


# ============================================
# FUNCIONES
# ============================================

def limpiar_texto(texto):
    """Limpia el texto para analisis."""
    if not texto:
        return ""
    
    # Minusculas
    texto = texto.lower()
    
    # Quitar acentos (simple)
    reemplazos = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "à": "a", "è": "e", "ì": "i", "ò": "o", "ù": "u",
        "ä": "a", "ë": "e", "ï": "i", "ö": "o", "ü": "u",
        "ñ": "n", "ç": "c",
    }
    for viejo, nuevo in reemplazos.items():
        texto = texto.replace(viejo, nuevo)
    
    return texto


def detectar_sector(descripcion):
    """
    Detecta el sector de un negocio segun su descripcion.
    
    Args:
        descripcion: texto con la descripcion del negocio
    
    Returns:
        nombre del sector detectado ("construccion", "panaderia", etc.)
        o None si no se detecta.
    """
    if not descripcion:
        return None
    
    texto = limpiar_texto(descripcion)
    
    # Contar coincidencias por sector
    puntuaciones = {}
    
    for sector, info in SECTORES.items():
        puntuacion = 0
        for keyword in info["keywords"]:
            keyword_limpia = limpiar_texto(keyword)
            if keyword_limpia in texto:
                # Premiar palabras mas largas
                puntuacion += len(keyword_limpia)
        
        if puntuacion > 0:
            puntuaciones[sector] = puntuacion
    
    if not puntuaciones:
        return None
    
    # Retornar el sector con mayor puntuacion
    return max(puntuaciones, key=puntuaciones.get)


def obtener_recomendaciones(sector):
    """
    Obtiene las recomendaciones de diseño para un sector.
    
    Returns:
        dict con tipo_pagina, diseno, tono, secciones
    """
    if sector and sector in SECTORES:
        info = SECTORES[sector]
        return {
            "sector": sector,
            "tipo_pagina": info["tipo_pagina"],
            "diseno": info["diseno"],
            "tono": info["tono"],
            "secciones": info["secciones"].copy(),
        }
    
    return {
        "sector": "default",
        "tipo_pagina": SECTOR_DEFAULT["tipo_pagina"],
        "diseno": SECTOR_DEFAULT["diseno"],
        "tono": SECTOR_DEFAULT["tono"],
        "secciones": SECTOR_DEFAULT["secciones"].copy(),
    }


def analizar_negocio(descripcion):
    """
    Funcion principal: analiza un negocio y retorna TODO.
    
    Args:
        descripcion: texto con la descripcion del negocio
    
    Returns:
        {
            "sector": "construccion",
            "tipo_pagina": "Landing Page",
            "diseno": "Moderno",
            "tono": "Profesional",
            "secciones": [...],
            "confianza": 0.85,  # Que tan seguro esta
            "keywords_detectadas": [...]
        }
    """
    if not descripcion:
        return {
            **obtener_recomendaciones(None),
            "confianza": 0.0,
            "keywords_detectadas": []
        }
    
    texto = limpiar_texto(descripcion)
    sector = detectar_sector(descripcion)
    
    # Contar keywords detectadas
    keywords_detectadas = []
    if sector:
        for kw in SECTORES[sector]["keywords"]:
            if limpiar_texto(kw) in texto:
                keywords_detectadas.append(kw)
    
    recomendaciones = obtener_recomendaciones(sector)
    
    # Calcular confianza (0-1)
    if not keywords_detectadas:
        confianza = 0.0
    else:
        confianza = min(1.0, len(keywords_detectadas) * 0.3)
    
    return {
        **recomendaciones,
        "confianza": round(confianza, 2),
        "keywords_detectadas": keywords_detectadas,
    }


# ============================================
# TEST
# ============================================

def test_detector():
    """Prueba el detector de sectores."""
    
    print("=" * 60)
    print("PROBANDO DETECTOR DE SECTORES")
    print("=" * 60)
    print()
    
    casos_test = [
        "Panadería La Espiga, 30 años haciendo el mejor pan en Medellín",
        "Constructora XYZ, especialistas en obra civil y reformas de casas",
        "Bufete de abogados especializados en derecho laboral y demandas",
        "Clínica dental Sonrisa Feliz, ortodoncia y implantes",
        "Restaurante La Trattoria, cocina italiana tradicional",
        "Gimnasio FitLife, entrenamiento personal y crossfit",
        "Agencia de marketing digital, SEO y redes sociales",
        "Fotógrafo profesional para bodas y eventos",
        "Veterinaria Patitas, consultas y peluquería canina",
        "Consultoría empresarial y estrategia de negocios",
        "Texto sin relación con ningún sector específico",
    ]
    
    for texto in casos_test:
        print("-" * 60)
        print("Descripcion: " + texto[:60] + ("..." if len(texto) > 60 else ""))
        print("-" * 60)
        
        resultado = analizar_negocio(texto)
        
        print("  Sector detectado: " + resultado["sector"])
        print("  Confianza: " + str(resultado["confianza"]))
        print("  Tipo de pagina: " + resultado["tipo_pagina"])
        print("  Diseno: " + resultado["diseno"])
        print("  Tono: " + resultado["tono"])
        print("  Secciones: " + ", ".join(resultado["secciones"]))
        
        if resultado["keywords_detectadas"]:
            print("  Keywords: " + ", ".join(resultado["keywords_detectadas"]))
        
        print()
    
    print("=" * 60)
    print("PRUEBA COMPLETADA")
    print("=" * 60)


if __name__ == "__main__":
    test_detector()