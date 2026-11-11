# utils/web_module.py
# ============================================
# INTERFAZ UNICA DEL SISTEMA DE WEBS
# ============================================
# V3.0: Pasa los campos Base64 (logo y fotos) al generador.
# ============================================

import os
import sys
import uuid
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.web_storage import (guardar_web as _guardar_web, leer_web as _leer_web, listar_webs as _listar_webs, eliminar_web as _eliminar_web, generar_uuid, guardar_usuario as _guardar_usuario)
except ImportError:
    from web_storage import (guardar_web as _guardar_web, leer_web as _leer_web, listar_webs as _listar_webs, eliminar_web as _eliminar_web, generar_uuid, guardar_usuario as _guardar_usuario)

try:
    from utils.web_generator import generar_web as _generar_web
except ImportError:
    try:
        from web_generator import generar_web as _generar_web
    except ImportError:
        _generar_web = None

try:
    from utils.web_editor import editar_web as _editar_web
except ImportError:
    try:
        from web_editor import editar_web as _editar_web
    except ImportError:
        _editar_web = None

try:
    from utils.web_publisher import publicar_web as _publicar_web
except ImportError:
    try:
        from web_publisher import publicar_web as _publicar_web
    except ImportError:
        _publicar_web = None

def puede_crear_web(usuario_id):
    resultado = _listar_webs(usuario_id)
    if not resultado["exito"]:
        return {"autorizado": False, "razon": "Error consultando webs", "es_extra": False}
    webs_actuales = len(resultado["webs"])
    es_extra = webs_actuales > 0
    return {"autorizado": True, "razon": "Puede crear web", "es_extra": es_extra}

def _construir_datos_completos(datos_negocio):
    nombre = datos_negocio.get("nombre") or datos_negocio.get("nombre_negocio") or "Mi Negocio"
    whatsapp = (datos_negocio.get("whatsapp_negocio") or datos_negocio.get("telefono_negocio") or "")

    return {
        "nombre":             nombre,
        "sector":             datos_negocio.get("sector", "General"),
        "descripcion":        datos_negocio.get("descripcion", ""),
        "publico_objetivo":   datos_negocio.get("publico_objetivo", ""),
        "diferenciadores":    datos_negocio.get("diferenciadores", ""),
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
        # --- AQUI ESTABA EL PROBLEMA: PASAMOS LAS IMAGENES ---
        "logo_b64":           datos_negocio.get("logo_b64"),
        "fotos_b64":          datos_negocio.get("fotos_b64", [])
    }

def crear_web(usuario_id, datos_negocio, opciones=None):
    permiso = puede_crear_web(usuario_id)
    if not permiso["autorizado"]:
        return {"exito": False, "web_id": None, "url_publicada": None, "html": None, "error": permiso["razon"]}

    if _generar_web is None:
        return {"exito": False, "web_id": None, "url_publicada": None, "html": None, "error": "Generador no disponible"}

    datos_completos = _construir_datos_completos(datos_negocio)
    resultado_gen = _generar_web(datos_negocio=datos_completos, opciones=opciones or {})

    if not resultado_gen["exito"]:
        return {"exito": False, "web_id": None, "url_publicada": None, "html": None, "error": "Error generando web: " + str(resultado_gen.get("error"))}

    html = resultado_gen["html"]
    web_id = generar_uuid()

    resultado_guardar = _guardar_web(
        usuario_id=usuario_id, web_id=web_id, html=html,
        datos_extra={"tipo_pagina": opciones.get("tipo_pagina") if opciones else None, "diseno": opciones.get("diseno") if opciones else None, "es_extra": permiso["es_extra"]}
    )

    if not resultado_guardar["exito"]:
        return {"exito": False, "web_id": None, "url_publicada": None, "html": None, "error": "Error guardando web: " + str(resultado_guardar.get("error"))}

    url_publicada = None
    if _publicar_web is not None:
        resultado_pub = _publicar_web(usuario_id, web_id)
        if resultado_pub["exito"]: url_publicada = resultado_pub["url_publicada"]

    return {"exito": True, "web_id": web_id, "url_publicada": url_publicada, "html": html, "error": None}