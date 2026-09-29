# utils/web_module.py
# ============================================
# INTERFAZ UNICA DEL SISTEMA DE WEBS
# ============================================
# V2.0: Pasa TODOS los campos del negocio a generar_web()
#       (direccion, horarios, redes, anio, whatsapp, etc)
# V1.0: Version inicial
# ============================================

import os
import sys
import uuid
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Config
try:
    from config.web_config import CONFIG, OPCIONES_DISENO, PRECIOS
except ImportError:
    CONFIG = {}
    OPCIONES_DISENO = {}
    PRECIOS = {}

# Storage
try:
    from utils.web_storage import (
        guardar_web as _guardar_web,
        leer_web as _leer_web,
        listar_webs as _listar_webs,
        eliminar_web as _eliminar_web,
        generar_uuid,
        guardar_usuario as _guardar_usuario,
    )
except ImportError:
    from web_storage import (
        guardar_web as _guardar_web,
        leer_web as _leer_web,
        listar_webs as _listar_webs,
        eliminar_web as _eliminar_web,
        generar_uuid,
        guardar_usuario as _guardar_usuario,
    )

# Generator
try:
    from utils.web_generator import generar_web as _generar_web
except ImportError:
    try:
        from web_generator import generar_web as _generar_web
    except ImportError:
        _generar_web = None

# Editor
try:
    from utils.web_editor import editar_web as _editar_web
except ImportError:
    try:
        from web_editor import editar_web as _editar_web
    except ImportError:
        _editar_web = None

# Expiration
try:
    from utils.web_expiration import obtener_info_web as _info_web
except ImportError:
    try:
        from web_expiration import obtener_info_web as _info_web
    except ImportError:
        _info_web = None

# Downloader
try:
    from utils.web_downloader import descargar_web as _descargar_web
except ImportError:
    try:
        from web_downloader import descargar_web as _descargar_web
    except ImportError:
        _descargar_web = None

# Publisher
try:
    from utils.web_publisher import publicar_web as _publicar_web
except ImportError:
    try:
        from web_publisher import publicar_web as _publicar_web
    except ImportError:
        _publicar_web = None


def puede_crear_web(usuario_id):
    """Verifica si el usuario puede crear una web."""
    print("=" * 60)
    print("VERIFICANDO PERMISO PARA CREAR WEB")
    print("=" * 60)
    print("Usuario: " + str(usuario_id)[:8])

    resultado = _listar_webs(usuario_id)

    if not resultado["exito"]:
        return {
            "autorizado": False,
            "razon": "Error consultando webs: " + str(resultado["error"]),
            "es_extra": False,
            "modo": "solo_pagina",
            "webs_actuales": 0,
        }

    webs_actuales = len(resultado["webs"])
    print("Webs actuales: " + str(webs_actuales))

    es_extra = webs_actuales > 0

    return {
        "autorizado": True,
        "razon": "Puede crear web" + (" extra" if es_extra else ""),
        "es_extra": es_extra,
        "modo": "solo_pagina",
        "webs_actuales": webs_actuales,
    }


def _construir_datos_completos(datos_negocio):
    """
    Construye dict con TODOS los campos que acepta generar_web().
    V2.0: incluye campos extendidos.
    """
    # Normalizar nombre (acepta "nombre" o "nombre_negocio")
    nombre = datos_negocio.get("nombre") or datos_negocio.get("nombre_negocio") or "Mi Negocio"

    # Normalizar whatsapp (acepta "whatsapp_negocio" o "telefono_negocio")
    whatsapp = (
        datos_negocio.get("whatsapp_negocio")
        or datos_negocio.get("telefono_negocio")
        or ""
    )

    return {
        "nombre":             nombre,
        "sector":             datos_negocio.get("sector", "General"),
        "descripcion":        datos_negocio.get("descripcion", ""),
        "publico_objetivo":   datos_negocio.get("publico_objetivo", ""),
        "diferenciadores":    datos_negocio.get("diferenciadores", ""),
        # Campos extendidos V2.0
        "direccion":          datos_negocio.get("direccion", ""),
        "ciudad":             datos_negocio.get("ciudad", ""),
        "pais":               datos_negocio.get("pais", ""),
        "horarios":           datos_negocio.get("horarios", ""),
        "instagram":          datos_negocio.get("instagram", ""),
        "facebook":           datos_negocio.get("facebook", ""),
        "tiktok":             datos_negocio.get("tiktok", ""),
        "anio_fundacion":     datos_negocio.get("anio_fundacion", ""),
        "email_contacto":     datos_negocio.get("email_contacto", ""),
        "whatsapp_negocio":   whatsapp,
    }


def crear_web(usuario_id, datos_negocio, opciones=None):
    """
    Crea una web completa.

    V2.0: pasa TODOS los campos al generador.
    """
    print("=" * 60)
    print("CREANDO WEB COMPLETA")
    print("=" * 60)
    print("Usuario: " + str(usuario_id)[:8])

    permiso = puede_crear_web(usuario_id)

    if not permiso["autorizado"]:
        return {
            "exito": False,
            "web_id": None,
            "url_publicada": None,
            "html": None,
            "error": permiso["razon"],
        }

    if _generar_web is None:
        return {
            "exito": False,
            "web_id": None,
            "url_publicada": None,
            "html": None,
            "error": "Generador no disponible",
        }

    print("\nGenerando web con IA...")

    datos_completos = _construir_datos_completos(datos_negocio)

    # Contar campos extendidos con valor
    campos_ext = ["direccion", "ciudad", "pais", "horarios", "instagram",
                  "facebook", "tiktok", "anio_fundacion", "email_contacto",
                  "whatsapp_negocio"]
    activos = sum(1 for c in campos_ext if datos_completos.get(c))
    print(f"Campos extendidos activos: {activos}/{len(campos_ext)}")

    resultado_gen = _generar_web(
        datos_negocio=datos_completos,
        opciones=opciones or {},
    )

    if not resultado_gen["exito"]:
        return {
            "exito": False,
            "web_id": None,
            "url_publicada": None,
            "html": None,
            "error": "Error generando web: " + str(resultado_gen.get("error")),
        }

    html = resultado_gen["html"]
    print("HTML generado: " + str(len(html)) + " caracteres")

    web_id = generar_uuid()

    print("\nGuardando web...")
    resultado_guardar = _guardar_web(
        usuario_id=usuario_id,
        web_id=web_id,
        html=html,
        datos_extra={
            "tipo_pagina": opciones.get("tipo_pagina") if opciones else None,
            "diseno": opciones.get("diseno") if opciones else None,
            "tono": opciones.get("tono") if opciones else None,
            "es_extra": permiso["es_extra"],
        },
    )

    if not resultado_guardar["exito"]:
        return {
            "exito": False,
            "web_id": None,
            "url_publicada": None,
            "html": None,
            "error": "Error guardando web: " + str(resultado_guardar.get("error")),
        }

    print("\nPublicando web...")
    url_publicada = None
    if _publicar_web is not None:
        resultado_pub = _publicar_web(usuario_id, web_id)
        if resultado_pub["exito"]:
            url_publicada = resultado_pub["url_publicada"]

    print("\n" + "=" * 60)
    print("WEB CREADA EXITOSAMENTE")
    print("=" * 60)
    print("Web ID: " + web_id)
    print("URL: " + str(url_publicada))

    return {
        "exito": True,
        "web_id": web_id,
        "url_publicada": url_publicada,
        "html": html,
        "error": None,
    }


def editar_web(usuario_id, web_id, instruccion):
    if _editar_web is None:
        return {"exito": False, "html_nuevo": None, "error": "Editor no disponible"}
    resultado = _editar_web(usuario_id, web_id, instruccion)
    if not resultado["exito"]:
        return {"exito": False, "html_nuevo": None, "error": resultado.get("error")}
    return {"exito": True, "html_nuevo": resultado["html_nuevo"], "error": None}


def descargar_web(usuario_id, web_id):
    if _descargar_web is None:
        return {"exito": False, "ruta_zip": None, "es_gratis": False,
                "error": "Descargador no disponible"}
    return _descargar_web(usuario_id, web_id)


def obtener_estado_web(web_id):
    if _info_web is None:
        return {"exito": False, "estado": "desconocido",
                "error": "Modulo expiration no disponible"}
    return _info_web(web_id)


def listar_webs(usuario_id):
    return _listar_webs(usuario_id)


def eliminar_web(usuario_id, web_id):
    return _eliminar_web(usuario_id, web_id)


if __name__ == "__main__":
    print("=" * 60)
    print("TEST WEB MODULE V2.0")
    print("=" * 60)
    print("Cambios V2.0:")
    print("  - Pasa TODOS los campos extendidos a generar_web()")
    print()
    print("Test _construir_datos_completos:")
    test = _construir_datos_completos({
        "nombre_negocio": "Panaderia Test",
        "sector": "alimentos",
        "descripcion": "Test",
        "direccion": "Calle 123",
        "ciudad": "Bogota",
        "whatsapp_negocio": "+573001234567",
    })
    print(f"  nombre: {test['nombre']}")
    print(f"  whatsapp_negocio: {test['whatsapp_negocio']}")
    print(f"  direccion: {test['direccion']}")
    print(f"  ciudad: {test['ciudad']}")
    print(f"  Total campos: {len(test)}")
    print("=" * 60)