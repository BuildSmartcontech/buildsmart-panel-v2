# config_app.py
# ============================================
# CONFIGURACION GLOBAL DE SAMU IA V4.1
# ============================================
# V4.1: Separa config por modelo de negocio:
#       - WEB GANCHO (solo web)
#       - NEGOCIO (PIME + DESDE CERO)
#       - SUCURSALES (expansion)
# V4.0: Lee config_global de Supabase (config-driven)
# ============================================

import os
import uuid
import streamlit as st


# ==========================================
# CARGA INICIAL DE CONFIG GLOBAL (una vez)
# ==========================================
_CONFIG_DB = {}
try:
    from utils.config_global import cargar_config
    _CONFIG_DB = cargar_config()
except Exception as e:
    print(f"[config_app] No se pudo cargar config_global: {e}")
    _CONFIG_DB = {}


def recargar_config():
    """
    Fuerza re-lectura de config_global.
    Se llama despues de guardar cambios en el panel dueno.
    """
    try:
        from utils.config_global import cargar_config
        global _CONFIG_DB
        global MODO, MODIFICACIONES_GRATIS, COSTO_MODIFICACION_EXTRA
        global SISTEMA_CREDITOS_ACTIVO, MOSTRAR_CREDITOS, LIMITE_WEBS
        global LIMITE_NEGOCIOS, LIMITE_IA_TOKENS, PERMITIR_PAGOS, DEBUG
        global LANDING_ACTIVA
        # Precios de planes
        global PRECIO_PIME, PRECIO_DESDE_CERO, PRECIO_ENTERPRISE
        # Web Gancho
        global WEB_GANCHO_PRECIO, WEB_GANCHO_ADMIN_PRECIO, WEB_GANCHO_CRM_PRECIO
        global WEB_GANCHO_MODS_LIMITE, WEB_GANCHO_COSTO_EXTRA
        # Sucursales
        global SUCURSAL_DESCUENTO_PORCENTAJE

        _CONFIG_DB = cargar_config(forzar=True)

        MODO = _CONFIG_DB.get("modo_app", "prueba")

        if MODO == "prueba":
            SISTEMA_CREDITOS_ACTIVO = False
            MOSTRAR_CREDITOS = False
            LIMITE_WEBS = 9999
            LIMITE_NEGOCIOS = 9999
            LIMITE_IA_TOKENS = 999999
            PERMITIR_PAGOS = False
            DEBUG = True
            MODIFICACIONES_GRATIS = int(_CONFIG_DB.get("negocio_modificaciones_gratis_prueba", 9))
        else:
            SISTEMA_CREDITOS_ACTIVO = True
            MOSTRAR_CREDITOS = True
            LIMITE_WEBS = 5
            LIMITE_NEGOCIOS = 1
            LIMITE_IA_TOKENS = 100000
            PERMITIR_PAGOS = True
            DEBUG = False
            MODIFICACIONES_GRATIS = int(_CONFIG_DB.get("negocio_modificaciones_gratis_prod", 3))

        COSTO_MODIFICACION_EXTRA = float(_CONFIG_DB.get("negocio_costo_modificacion_extra", 5))

        PRECIO_PIME = float(_CONFIG_DB.get("negocio_precio_pime", 99))
        PRECIO_DESDE_CERO = float(_CONFIG_DB.get("negocio_precio_desde_cero", 99))
        PRECIO_ENTERPRISE = float(_CONFIG_DB.get("negocio_precio_enterprise", 299))

        WEB_GANCHO_PRECIO = float(_CONFIG_DB.get("web_gancho_precio_individual", 199))
        WEB_GANCHO_ADMIN_PRECIO = float(_CONFIG_DB.get("web_gancho_administracion_precio", -1))
        WEB_GANCHO_CRM_PRECIO = float(_CONFIG_DB.get("web_gancho_crm_precio", -1))
        WEB_GANCHO_MODS_LIMITE = int(_CONFIG_DB.get("web_gancho_modificaciones_limite", -1))
        WEB_GANCHO_COSTO_EXTRA = float(_CONFIG_DB.get("web_gancho_costo_modificacion_extra", -1))

        SUCURSAL_DESCUENTO_PORCENTAJE = float(_CONFIG_DB.get("sucursal_descuento_porcentaje", 50))

        LANDING_ACTIVA = bool(_CONFIG_DB.get("landing_activa", True))

        return True
    except Exception as e:
        print(f"[config_app] Error recargando: {e}")
        return False


# ==========================================
# MODO DE OPERACION
# ==========================================
MODO = _CONFIG_DB.get("modo_app", "prueba")


# ==========================================
# TIPO DE USUARIO
# ==========================================
_es_dueno_str = os.getenv("BUILDSMART_ES_DUENO", "True")
ES_DUENO = _es_dueno_str.lower() == "true"


# ==========================================
# IDENTIFICACION DE USUARIO
# ==========================================
def obtener_usuario_actual():
    """Retorna el ID del usuario actual."""
    if "usuario_id" in st.session_state and st.session_state.usuario_id:
        return st.session_state.usuario_id

    ruta = os.path.join("data", "usuario_actual.txt")
    try:
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                usuario_id = f.read().strip()
                if usuario_id:
                    st.session_state.usuario_id = usuario_id
                    return usuario_id
    except Exception:
        pass

    usuario_id = str(uuid.uuid4())
    try:
        os.makedirs("data", exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(usuario_id)
    except Exception:
        pass

    st.session_state.usuario_id = usuario_id
    return usuario_id


# ==========================================
# CONFIGURACION SEGUN MODO
# ==========================================
if MODO == "prueba":
    SISTEMA_CREDITOS_ACTIVO = False
    MOSTRAR_CREDITOS = False
    LIMITE_WEBS = 9999
    LIMITE_NEGOCIOS = 9999
    LIMITE_IA_TOKENS = 999999
    PERMITIR_PAGOS = False
    DEBUG = True
    MODIFICACIONES_GRATIS = int(_CONFIG_DB.get("negocio_modificaciones_gratis_prueba", 9))
else:
    SISTEMA_CREDITOS_ACTIVO = True
    MOSTRAR_CREDITOS = True
    LIMITE_WEBS = 5
    LIMITE_NEGOCIOS = 1
    LIMITE_IA_TOKENS = 100000
    PERMITIR_PAGOS = True
    DEBUG = False
    MODIFICACIONES_GRATIS = int(_CONFIG_DB.get("negocio_modificaciones_gratis_prod", 3))


# ==========================================
# COSTOS DE MODIFICACION (para negocios PIME/Desde Cero)
# ==========================================
COSTO_MODIFICACION_EXTRA = float(_CONFIG_DB.get("negocio_costo_modificacion_extra", 5))


# ==========================================
# PRECIOS DE PLANES (negocios)
# ==========================================
PRECIO_PIME = float(_CONFIG_DB.get("negocio_precio_pime", 99))
PRECIO_DESDE_CERO = float(_CONFIG_DB.get("negocio_precio_desde_cero", 99))
PRECIO_ENTERPRISE = float(_CONFIG_DB.get("negocio_precio_enterprise", 299))


# ==========================================
# WEB GANCHO (Negocio 1 - solo web)
# ==========================================
# Valores -1 significan "POR DEFINIR"
WEB_GANCHO_PRECIO = float(_CONFIG_DB.get("web_gancho_precio_individual", 199))
WEB_GANCHO_ADMIN_PRECIO = float(_CONFIG_DB.get("web_gancho_administracion_precio", -1))
WEB_GANCHO_CRM_PRECIO = float(_CONFIG_DB.get("web_gancho_crm_precio", -1))
WEB_GANCHO_MODS_LIMITE = int(_CONFIG_DB.get("web_gancho_modificaciones_limite", -1))
WEB_GANCHO_COSTO_EXTRA = float(_CONFIG_DB.get("web_gancho_costo_modificacion_extra", -1))


# ==========================================
# SUCURSALES / EXPANSION
# ==========================================
SUCURSAL_DESCUENTO_PORCENTAJE = float(_CONFIG_DB.get("sucursal_descuento_porcentaje", 50))


# ==========================================
# LANDING
# ==========================================
LANDING_ACTIVA = bool(_CONFIG_DB.get("landing_activa", True))


# ==========================================
# VERSION
# ==========================================
VERSION = "4.1"
NOMBRE_APP = "SAMU IA"