# utils/sector_detector.py
# ============================================
# DETECTOR HIBRIDO DE SECTORES - V1.2
# ============================================
# V1.2: Cache en memoria para evitar llamadas repetidas a IA
#       Mismo negocio = 1 sola deteccion
# ============================================

import os
import sys
import json
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend.gateway import gateway
    GATEWAY_DISPONIBLE = True
except ImportError:
    try:
        from gateway import gateway
        GATEWAY_DISPONIBLE = True
    except ImportError:
        GATEWAY_DISPONIBLE = False
        gateway = None


# ============================================
# CACHE EN MEMORIA
# ============================================
# Evita llamar a la IA multiples veces para el mismo negocio
# Key: nombre_normalizado + "|" + sector_normalizado
# Value: dict con el resultado de detectar_sector_completo

_CACHE_DETECCIONES = {}


def _clave_cache(nombre, sector):
    """Genera clave unica para el cache."""
    nombre_norm = (nombre or "").lower().strip()[:100]
    sector_norm = (sector or "").lower().strip()[:50]
    return nombre_norm + "|" + sector_norm


def limpiar_cache():
    """Limpia el cache (util al cambiar de negocio)."""
    global _CACHE_DETECCIONES
    _CACHE_DETECCIONES = {}
    print("[SECTOR] Cache limpiado")


def info_cache():
    """Retorna informacion del cache."""
    return {
        "total": len(_CACHE_DETECCIONES),
        "claves": list(_CACHE_DETECCIONES.keys())
    }


# ============================================
# BASE DE CONOCIMIENTO LOCAL
# ============================================

SECTORES_LOCALES = {
    # ===== ALIMENTOS =====
    "panaderia": {
        "keywords_imagenes": ["artisan bakery bread", "fresh bread loaves", "pastry baker"],
        "guia": "Define tu producto estrella (pan, torta, etc), precios por unidad y por docena, y horario de atencion.",
        "contexto": "Panaderia artesanal"
    },
    "pasteleria": {
        "keywords_imagenes": ["cake decoration", "pastry chef", "colorful cakes"],
        "guia": "Define tipos de tortas, tamaños, precios, y tiempo de anticipacion para pedidos personalizados.",
        "contexto": "Pasteleria y reposteria"
    },
    "dulceria": {
        "keywords_imagenes": ["colorful candies", "sweets assortment", "chocolate truffles"],
        "guia": "Clasifica por tipo de dulce (chocolates, gomitas, tradicionales), precios y presentaciones.",
        "contexto": "Dulceria y confiteria"
    },
    "arepas": {
        "keywords_imagenes": ["venezuelan arepas", "corn cakes", "arepas on plate"],
        "guia": "Define tipos de arepas (queso, chicharron, etc), presentacion (unidad o paquete) y precios.",
        "contexto": "Areperia"
    },
    "cafeteria": {
        "keywords_imagenes": ["coffee shop barista", "coffee cup latte art", "espresso machine"],
        "guia": "Define menu de bebidas calientes/frias, snacks, precios y horario.",
        "contexto": "Cafeteria"
    },
    "restaurante": {
        "keywords_imagenes": ["restaurant food dish", "chef plating", "gourmet dining"],
        "guia": "Define menu completo con entradas, platos fuertes, postres, bebidas y precios.",
        "contexto": "Restaurante"
    },
    "heladeria": {
        "keywords_imagenes": ["ice cream scoops", "colorful gelato", "ice cream cone"],
        "guia": "Define sabores, tamaños (cono, vaso, litro), toppings y precios.",
        "contexto": "Heladeria"
    },
    "catering": {
        "keywords_imagenes": ["catering buffet", "elegant food service", "event catering"],
        "guia": "Define paquetes para eventos (15, 50, 100 personas), menus y precios.",
        "contexto": "Servicio de catering"
    },

    # ===== CONSTRUCCION =====
    "construccion": {
        "keywords_imagenes": ["construction site worker", "building construction", "architecture"],
        "guia": "Documenta servicios: obra civil, remodelacion, ampliacion. Incluye fotos de proyectos anteriores.",
        "contexto": "Constructora"
    },
    "reformas": {
        "keywords_imagenes": ["home renovation", "interior remodeling", "modern kitchen"],
        "guia": "Define tipos de reforma (cocina, baño, integral), presupuesto por m2 y tiempo estimado.",
        "contexto": "Reformas y remodelacion"
    },
    "electricista": {
        "keywords_imagenes": ["electrician working", "electrical wiring", "electrical panel"],
        "guia": "Define servicios (instalacion, reparacion, certificados), tarifas por hora o por trabajo.",
        "contexto": "Servicios electricos"
    },
    "plomeria": {
        "keywords_imagenes": ["plumber working pipes", "plumbing repair", "bathroom plumbing"],
        "guia": "Define servicios (fugas, instalacion, destapes), tarifas por visita y por hora.",
        "contexto": "Servicios de plomeria"
    },
    "carpinteria": {
        "keywords_imagenes": ["carpenter woodworking", "custom furniture", "wood workshop"],
        "guia": "Muestra trabajos: muebles a medida, puertas, closets. Precios por proyecto.",
        "contexto": "Carpinteria"
    },
    "pintura": {
        "keywords_imagenes": ["painter working", "colorful wall paint", "paint roller"],
        "guia": "Define servicios (interior, exterior, decorativo), precio por m2 y tiempo.",
        "contexto": "Pintura y acabados"
    },
    "cerrajeria": {
        "keywords_imagenes": ["locksmith keys", "door lock installation", "key cutting"],
        "guia": "Define servicios (aperturas, cambio de cerraduras, copias), precio por servicio.",
        "contexto": "Cerrajeria"
    },

    # ===== PROFESIONALES =====
    "abogados": {
        "keywords_imagenes": ["lawyer office", "legal books justice", "lawyer working"],
        "guia": "Define areas de practica (civil, penal, laboral), consulta inicial y honorarios.",
        "contexto": "Bufete de abogados"
    },
    "contabilidad": {
        "keywords_imagenes": ["accountant working", "financial documents", "calculator numbers"],
        "guia": "Define servicios (declaraciones, nomina, asesoria), precios mensuales o por servicio.",
        "contexto": "Contabilidad"
    },
    "consultoria": {
        "keywords_imagenes": ["business consulting", "strategy meeting", "professional advisor"],
        "guia": "Define areas de consultoria, metodologia, paquetes y precios por hora o proyecto.",
        "contexto": "Consultoria empresarial"
    },
    "marketing": {
        "keywords_imagenes": ["marketing team", "social media content", "digital marketing"],
        "guia": "Define servicios (redes, SEO, ads), paquetes mensuales y precios.",
        "contexto": "Marketing digital"
    },
    "diseno_grafico": {
        "keywords_imagenes": ["graphic design workspace", "designer creative", "branding"],
        "guia": "Define servicios (logo, identidad, piezas graficas), precios por proyecto.",
        "contexto": "Diseño grafico"
    },
    "fotografia": {
        "keywords_imagenes": ["photographer camera", "photo studio lighting", "professional photoshoot"],
        "guia": "Define servicios (bodas, eventos, productos, retratos), paquetes y precios.",
        "contexto": "Fotografia profesional"
    },
    "arquitectura": {
        "keywords_imagenes": ["architect blueprints", "modern architecture", "architectural design"],
        "guia": "Define servicios (planos, renders, direccion de obra), precios por proyecto.",
        "contexto": "Estudio de arquitectura"
    },

    # ===== SALUD =====
    "medicos": {
        "keywords_imagenes": ["doctor hospital", "medical consultation", "healthcare professional"],
        "guia": "Define especialidades, horarios de consulta, precios y forma de agendar.",
        "contexto": "Consultorio medico"
    },
    "dentistas": {
        "keywords_imagenes": ["dentist office", "dental clinic", "tooth smile"],
        "guia": "Define servicios (limpieza, ortodoncia, implantes), precios y financiamiento.",
        "contexto": "Consultorio odontologico"
    },
    "psicologia": {
        "keywords_imagenes": ["therapy session", "psychologist office", "mental health"],
        "guia": "Define tipo de terapia (individual, pareja, familiar), duracion y precio por sesion.",
        "contexto": "Consultorio psicologico"
    },
    "nutricion": {
        "keywords_imagenes": ["nutritionist food", "healthy meal plan", "fresh vegetables"],
        "guia": "Define servicios (plan nutricional, seguimiento), precios y modalidades (presencial/online).",
        "contexto": "Nutricion y dietetica"
    },
    "veterinaria": {
        "keywords_imagenes": ["veterinarian pet", "vet dog cat", "animal clinic"],
        "guia": "Define servicios (consulta, vacunacion, cirugia), precios y horarios.",
        "contexto": "Clinica veterinaria"
    },
    "farmacia": {
        "keywords_imagenes": ["pharmacy medicines", "pharmacist", "drugstore shelves"],
        "guia": "Define categorias de productos, servicio de domicilio y horarios.",
        "contexto": "Farmacia"
    },
    "optica": {
        "keywords_imagenes": ["optician eyeglasses", "glasses display", "eye exam"],
        "guia": "Define marcas, tipos de lentes, servicio de examen visual y precios.",
        "contexto": "Optica"
    },

    # ===== BELLEZA =====
    "peluqueria": {
        "keywords_imagenes": ["hair salon", "hairstylist working", "haircut style"],
        "guia": "Define servicios (corte, color, tratamientos), precios y duracion aproximada.",
        "contexto": "Peluqueria"
    },
    "barberia": {
        "keywords_imagenes": ["barber shop", "barber haircut", "grooming man"],
        "guia": "Define servicios (corte, barba, afeitado), precios y horarios.",
        "contexto": "Barberia"
    },
    "spa": {
        "keywords_imagenes": ["spa massage", "relaxing spa", "wellness treatment"],
        "guia": "Define servicios (masajes, faciales, corporales), duracion y precios.",
        "contexto": "Spa y bienestar"
    },
    "unas": {
        "keywords_imagenes": ["nail art salon", "manicure", "nail polish colors"],
        "guia": "Define servicios (manicure, pedicure, diseño), precios y tiempo.",
        "contexto": "Salon de uñas"
    },
    "maquillaje": {
        "keywords_imagenes": ["makeup artist", "professional makeup", "cosmetics application"],
        "guia": "Define servicios (social, novia, quinceañera), precios y servicios a domicilio.",
        "contexto": "Maquillaje profesional"
    },
    "tatuajes": {
        "keywords_imagenes": ["tattoo artist", "tattoo studio", "tattoo design"],
        "guia": "Define estilos, tamaño, precio por hora y requisitos de higiene.",
        "contexto": "Estudio de tatuajes"
    },

    # ===== FITNESS =====
    "gimnasio": {
        "keywords_imagenes": ["gym fitness equipment", "workout training", "fitness class"],
        "guia": "Define planes (mensual, trimestral, anual), horarios y servicios adicionales.",
        "contexto": "Gimnasio"
    },
    "entrenador_personal": {
        "keywords_imagenes": ["personal trainer", "fitness coach", "gym workout"],
        "guia": "Define modalidades (presencial, online), paquetes y precios por sesion.",
        "contexto": "Entrenamiento personal"
    },
    "yoga": {
        "keywords_imagenes": ["yoga class", "yoga pose", "meditation studio"],
        "guia": "Define clases (hatha, vinyasa, meditacion), horarios y precios.",
        "contexto": "Estudio de yoga"
    },

    # ===== EDUCACION =====
    "academia": {
        "keywords_imagenes": ["classroom learning", "students studying", "teacher classroom"],
        "guia": "Define cursos, duracion, modalidad (presencial/online) y precios.",
        "contexto": "Academia"
    },
    "idiomas": {
        "keywords_imagenes": ["language class", "learning languages", "books study"],
        "guia": "Define idiomas, niveles, duracion de cursos y precios por nivel.",
        "contexto": "Escuela de idiomas"
    },
    "musica": {
        "keywords_imagenes": ["music teacher", "instrument lesson", "music studio"],
        "guia": "Define instrumentos, niveles, clases (individual/grupal) y precios.",
        "contexto": "Academia de musica"
    },

    # ===== RETAIL =====
    "ropa": {
        "keywords_imagenes": ["clothing store", "fashion boutique", "clothes rack"],
        "guia": "Define categorias (dama, caballero, niños), precios y metodos de envio.",
        "contexto": "Tienda de ropa"
    },
    "joyeria": {
        "keywords_imagenes": ["jewelry display", "gold jewelry", "rings necklaces"],
        "guia": "Define materiales (oro, plata, acero), piedras y precios por pieza.",
        "contexto": "Joyeria"
    },
    "zapateria": {
        "keywords_imagenes": ["shoe store", "shoes display", "leather shoes"],
        "guia": "Define marcas, tipos (deportivo, casual, formal), precios y tallas.",
        "contexto": "Zapateria"
    },
    "muebles": {
        "keywords_imagenes": ["furniture store", "modern furniture", "interior decor"],
        "guia": "Define categorias (sala, comedor, dormitorio), precios y servicio de entrega.",
        "contexto": "Muebleria"
    },
    "tecnologia": {
        "keywords_imagenes": ["technology devices", "electronics store", "gadgets"],
        "guia": "Define categorias (celulares, computadoras, accesorios), garantia y precios.",
        "contexto": "Tienda de tecnologia"
    },
    "floristeria": {
        "keywords_imagenes": ["flower shop", "colorful bouquet", "floral arrangement"],
        "guia": "Define tipos de arreglos, precios y servicio de entrega.",
        "contexto": "Floristeria"
    },
    "mascotas": {
        "keywords_imagenes": ["pet store", "pet food", "puppy kitten"],
        "guia": "Define categorias (alimentos, accesorios, servicios), precios y servicios.",
        "contexto": "Tienda de mascotas"
    },
    "jardineria": {
        "keywords_imagenes": ["gardening landscaping", "garden design", "green plants nursery"],
        "guia": "Define servicios (mantenimiento, diseño, venta de plantas), precios por m2 o visita.",
        "contexto": "Jardineria y vivero"
    },

    # ===== AUTOMOTRIZ =====
    "taller_mecanico": {
        "keywords_imagenes": ["auto mechanic", "car repair shop", "mechanic working"],
        "guia": "Define servicios (reparacion, mantenimiento, diagnostico), precios por servicio.",
        "contexto": "Taller mecanico"
    },
    "lavadero_autos": {
        "keywords_imagenes": ["car wash", "car cleaning", "shiny car"],
        "guia": "Define servicios (basico, completo, detallado), precios por tipo de vehiculo.",
        "contexto": "Lavadero de autos"
    },
    "transporte": {
        "keywords_imagenes": ["cargo transport", "delivery truck", "logistics vehicle"],
        "guia": "Define servicios (carga, mudanzas, delivery), tarifas por distancia.",
        "contexto": "Transporte y logistica"
    },

    # ===== EVENTOS =====
    "eventos": {
        "keywords_imagenes": ["event setup", "party decoration", "elegant event"],
        "guia": "Define tipos de eventos (bodas, cumpleaños, corporativos), paquetes y precios.",
        "contexto": "Organizacion de eventos"
    },
    "wedding_planner": {
        "keywords_imagenes": ["wedding planning", "elegant wedding", "bride groom"],
        "guia": "Define paquetes (basico, completo, premium), servicios incluidos y precios.",
        "contexto": "Wedding planner"
    },
    "dj": {
        "keywords_imagenes": ["dj mixing", "dj party", "audio equipment"],
        "guia": "Define servicios (fiestas, bodas, corporativos), equipo incluido y precios.",
        "contexto": "DJ profesional"
    },

    # ===== HOGAR =====
    "limpieza": {
        "keywords_imagenes": ["home cleaning", "clean house", "cleaning service"],
        "guia": "Define servicios (residencial, comercial, profunda), precios por tamaño.",
        "contexto": "Servicio de limpieza"
    },
    "mudanzas": {
        "keywords_imagenes": ["moving truck", "moving boxes", "furniture moving"],
        "guia": "Define servicios (locales, larga distancia), tarifas por hora y personal.",
        "contexto": "Mudanzas"
    },

    # ===== INMOBILIARIA =====
    "inmobiliaria": {
        "keywords_imagenes": ["real estate house", "modern property", "key house"],
        "guia": "Define tipos de inmuebles (casa, apto, local), zonas y servicios de asesoria.",
        "contexto": "Inmobiliaria"
    },

    # ===== TURISMO =====
    "hotel": {
        "keywords_imagenes": ["hotel room", "hotel lobby", "hospitality"],
        "guia": "Define tipos de habitacion, servicios incluidos, tarifas por temporada.",
        "contexto": "Hotel"
    },
    "turismo": {
        "keywords_imagenes": ["travel destination", "tour guide", "tourism landmark"],
        "guia": "Define destinos, paquetes, duracion y precios por persona.",
        "contexto": "Agencia de turismo"
    },

    # ===== FINANZAS =====
    "seguros": {
        "keywords_imagenes": ["insurance protection", "insurance agent", "family protection"],
        "guia": "Define tipos (vida, auto, hogar, salud), aseguradoras y cotizacion.",
        "contexto": "Agencia de seguros"
    },
    "financiera": {
        "keywords_imagenes": ["financial planning", "investment growth", "money finance"],
        "guia": "Define productos (creditos, inversiones), requisitos y tasas.",
        "contexto": "Asesoria financiera"
    },

    # ===== MANUFACTURA =====
    "imprenta": {
        "keywords_imagenes": ["printing press", "graphic printing", "print design"],
        "guia": "Define servicios (tarjetas, volantes, banners), precios por cantidad.",
        "contexto": "Imprenta"
    },
    "fabricacion": {
        "keywords_imagenes": ["factory production", "manufacturing process", "industrial workshop"],
        "guia": "Define productos fabricados, capacidad de produccion y precios al mayor.",
        "contexto": "Manufactura"
    },

    # ===== DISTRIBUCION =====
    "distribuidora": {
        "keywords_imagenes": ["warehouse distribution", "wholesale goods", "logistics center"],
        "guia": "Define categorias, pedidos minimos, precios al mayor y cobertura.",
        "contexto": "Distribuidora mayorista"
    },

    # ===== DEFAULT =====
    "default": {
        "keywords_imagenes": ["professional business", "modern office", "business team"],
        "guia": "Define tus servicios principales, precios, publico objetivo y forma de contacto.",
        "contexto": "Negocio general"
    },
}


# ============================================
# FUNCIONES AUXILIARES
# ============================================

def normalizar_texto(texto):
    if not texto:
        return ""
    texto = texto.lower().strip()
    texto = texto.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    texto = texto.replace("ñ", "n")
    texto = texto.replace("ü", "u")
    texto = texto.replace("_", " ")
    texto = re.sub(r'[^a-z0-9\s]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()


def _contiene_palabra_completa(texto_normalizado, palabra):
    if not texto_normalizado or not palabra:
        return False
    palabra_norm = normalizar_texto(palabra)
    if not palabra_norm:
        return False
    patron = r'\b' + re.escape(palabra_norm) + r'\b'
    return re.search(patron, texto_normalizado) is not None


# ============================================
# DETECCION LOCAL
# ============================================

def buscar_sector_local(nombre, descripcion, sector):
    texto_completo = normalizar_texto(nombre + " " + descripcion + " " + sector)
    sector_norm = normalizar_texto(sector)

    # PRIORIDAD 1: match exacto
    if sector_norm in SECTORES_LOCALES:
        return sector_norm, SECTORES_LOCALES[sector_norm]

    # PRIORIDAD 2: sector_key como palabra completa
    for sector_key, datos in SECTORES_LOCALES.items():
        if sector_key == "default":
            continue
        key_norm = normalizar_texto(sector_key)
        if _contiene_palabra_completa(texto_completo, key_norm):
            return sector_key, datos

    # PRIORIDAD 3: keywords como palabras completas
    for sector_key, datos in SECTORES_LOCALES.items():
        if sector_key == "default":
            continue
        keywords = datos.get("keywords_imagenes", [])
        for kw in keywords:
            if not kw:
                continue
            palabras_kw = normalizar_texto(kw).split()
            if not palabras_kw:
                continue
            primera_palabra = palabras_kw[0]
            if len(primera_palabra) >= 4 and _contiene_palabra_completa(texto_completo, primera_palabra):
                return sector_key, datos

    return None, None


# ============================================
# DETECCION CON IA
# ============================================

def detectar_sector_ia(nombre, descripcion, sector):
    if not GATEWAY_DISPONIBLE or gateway is None:
        return None

    prompt = f"""Eres un analizador de negocios. Debes analizar este negocio y devolver SOLO un JSON con informacion para generar imagenes y guias.

NEGOCIO:
- Nombre: {nombre}
- Sector declarado: {sector}
- Descripcion: {descripcion}

RESPONDE CON ESTE FORMATO JSON EXACTO:
{{
  "sector_identificado": "nombre del sector en minusculas y sin tildes",
  "keywords_imagenes": ["keyword en ingles 1", "keyword en ingles 2", "keyword en ingles 3"],
  "guia": "Guia corta en espanol (max 2 oraciones) de 3 pasos concretos para arrancar este negocio",
  "contexto": "Descripcion muy corta del sector (3-5 palabras)"
}}

REGLAS:
- keywords_imagenes: 3 terminos EN INGLES, buscables en Unsplash, relacionados al producto/servicio especifico
- guia: en ESPANOL, 3 pasos concretos y accionables
- contexto: en ESPANOL, 3-5 palabras maximo
- Devuelve SOLO el JSON, sin markdown, sin explicaciones

EJEMPLO:
Para "Fabricante de velas artesanales":
{{"sector_identificado": "velas artesanales", "keywords_imagenes": ["handmade candles", "artisan candle workshop", "scented candles"], "guia": "Define tipos de velas, aromas y tamaños. Calcula costo de produccion. Crea 5 fotos de producto con buena iluminacion.", "contexto": "Velas artesanales"}}

Responde SOLO con el JSON:"""

    try:
        sistema = "Eres un analizador de negocios. Devuelves SOLO JSON valido sin markdown."
        respuesta, fuente = gateway.chat_inteligente(prompt, sistema)

        respuesta = respuesta.strip()
        if respuesta.startswith("```"):
            respuesta = re.sub(r'^```(?:json)?\s*', '', respuesta)
            respuesta = re.sub(r'\s*```$', '', respuesta)

        inicio = respuesta.find("{")
        fin = respuesta.rfind("}")

        if inicio == -1 or fin == -1:
            return None

        data = json.loads(respuesta[inicio:fin + 1])

        if "keywords_imagenes" not in data:
            return None

        return {
            "sector_identificado": data.get("sector_identificado", sector),
            "keywords_imagenes": data.get("keywords_imagenes", ["business", "product"]),
            "guia": data.get("guia", "Define tu producto/servicio, precios y publico objetivo."),
            "contexto": data.get("contexto", sector),
            "fuente": "ia_" + str(fuente)
        }

    except Exception as e:
        print("[SECTOR] Error IA: " + str(e))
        return None


# ============================================
# FUNCION PRINCIPAL CON CACHE
# ============================================

def detectar_sector_completo(nombre, descripcion, sector):
    """
    Sistema hibrido CON CACHE:
    1. Busca en cache (rapido)
    2. Busca local (rapido, gratis)
    3. Usa IA (lento, paga)
    4. Cachea el resultado para futuras llamadas
    """
    # ==========================================
    # 1. VERIFICAR CACHE
    # ==========================================
    clave = _clave_cache(nombre, sector)

    if clave in _CACHE_DETECCIONES:
        print("[SECTOR] CACHE HIT: " + str(sector) + " -> " + str(_CACHE_DETECCIONES[clave].get("contexto")))
        resultado_cache = _CACHE_DETECCIONES[clave].copy()
        resultado_cache["cacheado"] = True
        return resultado_cache

    # ==========================================
    # 2. BUSCAR LOCAL
    # ==========================================
    print("[SECTOR] Cache miss. Buscando: " + str(sector) + " | " + str(nombre)[:40])

    sector_key, datos = buscar_sector_local(nombre, descripcion, sector)

    if datos:
        print("[SECTOR] LOCAL: " + str(sector_key))
        resultado = {
            "sector_key": sector_key,
            "keywords_imagenes": datos["keywords_imagenes"],
            "guia": datos["guia"],
            "contexto": datos["contexto"],
            "fuente": "local",
            "cacheado": False
        }
        _CACHE_DETECCIONES[clave] = resultado.copy()
        return resultado

    # ==========================================
    # 3. USAR IA
    # ==========================================
    print("[SECTOR] No en local, usando IA...")
    datos_ia = detectar_sector_ia(nombre, descripcion, sector)

    if datos_ia:
        print("[SECTOR] IA: " + str(datos_ia.get("contexto")))
        resultado = {
            "sector_key": datos_ia.get("sector_identificado", "custom"),
            "keywords_imagenes": datos_ia["keywords_imagenes"],
            "guia": datos_ia["guia"],
            "contexto": datos_ia["contexto"],
            "fuente": datos_ia.get("fuente", "ia"),
            "cacheado": False
        }
        _CACHE_DETECCIONES[clave] = resultado.copy()
        return resultado

    # ==========================================
    # 4. FALLBACK DEFAULT
    # ==========================================
    print("[SECTOR] Usando DEFAULT")
    datos_default = SECTORES_LOCALES["default"]
    resultado = {
        "sector_key": "default",
        "keywords_imagenes": datos_default["keywords_imagenes"],
        "guia": datos_default["guia"],
        "contexto": datos_default["contexto"],
        "fuente": "default",
        "cacheado": False
    }
    _CACHE_DETECCIONES[clave] = resultado.copy()
    return resultado


def obtener_keywords_imagenes(sector, nombre="", descripcion=""):
    resultado = detectar_sector_completo(nombre, descripcion, sector)
    return resultado["keywords_imagenes"]


def obtener_guia_tarea(sector, nombre="", descripcion=""):
    resultado = detectar_sector_completo(nombre, descripcion, sector)
    return resultado["guia"]


# ============================================
# TEST
# ============================================

def test_detector():
    print("=" * 60)
    print("TEST SECTOR DETECTOR HIBRIDO V1.2 (CON CACHE)")
    print("=" * 60)

    pruebas = [
        ("Panaderia La Espiga", "Pan artesanal", "panaderia"),
        ("Fabricante de Velas", "Velas artesanales aromaticas", "manualidades"),
        ("Lavadero Pro", "Lavado de autos", "automotriz"),
    ]

    for nombre, desc, sector in pruebas:
        print("\n" + "-" * 60)
        print("Negocio: " + nombre)

        # Llamar 3 veces para ver el cache funcionar
        for i in range(3):
            resultado = detectar_sector_completo(nombre, desc, sector)
            print("  Llamada " + str(i+1) + ": " + resultado["contexto"] + " (cacheado: " + str(resultado.get("cacheado", False)) + ")")

    print("\n" + "=" * 60)
    print("Info del cache:")
    info = info_cache()
    print("  Total entradas: " + str(info["total"]))
    for k in info["claves"]:
        print("  - " + k)
    print("=" * 60)


if __name__ == "__main__":
    test_detector()