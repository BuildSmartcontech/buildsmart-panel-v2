# panels/panel_base.py
# ============================================
# PANEL BASE - CODIGO COMPARTIDO
# V5.6: Cobro automático por modificaciones extra (ePayco / Manual).
# ============================================

import streamlit as st
import datetime
import random
import re
import requests
import os
import hashlib
from config_app import MODO, ES_DUENO, SISTEMA_CREDITOS_ACTIVO, MOSTRAR_CREDITOS

try:
    from config_app import MODIFICACIONES_GRATIS
except ImportError:
    MODIFICACIONES_GRATIS = 7 if MODO == "prueba" else 3

try:
    from config_app import COSTO_MODIFICACION_EXTRA as _COSTO_DINAMICO
    COSTO_MODIFICACION_EXTRA = _COSTO_DINAMICO
except ImportError:
    COSTO_MODIFICACION_EXTRA = 5

PERSONALIDAD_DEFAULT = """Eres el Orquestador de SAMU IA, un asistente inteligente especializado en gestion de negocios.

Tu estilo:
- Profesional, claro y directo
- Empatico con el usuario
- Enfocado en resultados
- Entiendes dialectos latinoamericanos, typos y spanglish
- Respondes en espanol claro y breve (max 3 parrafos)"""

GUIAS_POR_CATEGORIA = {
    "ESTRATEGIA": "Define en papel: (1) Que vendes exactamente, (2) A quien, (3) Por que te eligen a ti y no a la competencia. Escribe 3 oraciones para cada punto.",
    "DISEÑO": "Usa el chat para mejorar tu web. Ejemplos: 'modificar mi web: cambia el titulo a X', 'agrega una seccion de Y', 'ponle imagenes de Z a los cuadros'.",
    "MARKETING": "Investiga 3 competidores directos. Anota: precios, que promocionan, en que redes estan. Define en 1 frase en que te diferencias.",
    "VENTAS": "Escribe una lista de 10 clientes potenciales (nombre + contacto). Contacta a 3 hoy por WhatsApp, llamada o correo.",
    "FINANZAS": "Anota tus ingresos y gastos de esta semana en una hoja. Identifica en que gastas mas y si puedes reducirlo.",
    "CONTABILIDAD": "Configura tu plan de cuentas basico. Empieza por: Caja, Bancos, Ventas, Gastos operativos. Esto estara integrado con Odoo pronto.",
    "OPERACIONES": "Documenta paso a paso como haces tu producto/servicio principal. Graba un video corto mostrando el proceso.",
    "EQUIPO": "Capacita a tu equipo. Muestrales el panel, el Kanban y como mover tareas. Define roles claros para cada uno.",
    "CONTENIDO": "Planifica 4 publicaciones para la proxima semana. Formato: Lunes (producto), Miercoles (tips), Viernes (promo), Domingo (historia).",
    "INVESTIGACIÓN": "Analiza 3 competidores: precios, fortalezas, debilidades. Escribe 5 hallazgos que puedas aplicar a tu negocio.",
    "PUBLICIDAD": "Define un presupuesto diario minimo ($5-10 USD). Prueba 2 anuncios con imagenes distintas y mide cual funciona mejor.",
    "INVENTARIO": "Registra tus productos con cantidad actual y precio. Pronto podras escanear codigos de barras con la camara de tu celular.",
    "CRM": "Importa tu base de clientes: nombre, contacto, ultima compra. Clasificalos en: nuevos, recurrentes, inactivos.",
    "REDES": "Conecta tus redes sociales. Publica 3 veces por semana minimo. Usa imagenes reales de tus productos.",
    "PRODUCTO": "Define tu producto estrella. Describe: que es, para quien, por que es especial, cuanto cuesta producirlo y cuanto lo vendes.",
    "ATENCION": "Escribe las 5 preguntas mas comunes de tus clientes y prepara respuestas cortas y claras para cada una.",
    "LOGISTICA": "Define como entregas tu producto: en tienda, a domicilio, punto de encuentro. Establece tiempos y costos.",
    "GENERAL": "Divide esta tarea en 3 pasos concretos y pequeños. Empieza por el mas rapido de completar.",
}

# IMPORTS ORIGINALES
try:
    from utils.web_module import (puede_crear_web, crear_web, descargar_web, obtener_estado_web, listar_webs)
    WEB_DISPONIBLE = True
except ImportError:
    WEB_DISPONIBLE = False
    puede_crear_web = crear_web = descargar_web = obtener_estado_web = listar_webs = None

try:
    from utils.web_editor_v2 import editar_y_guardar_v2
    EDITOR_DISPONIBLE = True
except ImportError:
    try:
        from web_editor_v2 import editar_y_guardar_v2
        EDITOR_DISPONIBLE = True
    except ImportError:
        EDITOR_DISPONIBLE = False
        editar_y_guardar_v2 = None

try:
    from utils.web_publisher import publicar_web, obtener_url_web
    PUBLISHER_DISPONIBLE = True
except ImportError:
    try:
        from web_publisher import publicar_web, obtener_url_web
        PUBLISHER_DISPONIBLE = True
    except ImportError:
        PUBLISHER_DISPONIBLE = False
        publicar_web = obtener_url_web = None

try:
    from utils.sector_detector import detectar_sector_completo, limpiar_cache
    SECTOR_DETECTOR_DISPONIBLE = True
except ImportError:
    try:
        from sector_detector import detectar_sector_completo, limpiar_cache
        SECTOR_DETECTOR_DISPONIBLE = True
    except ImportError:
        SECTOR_DETECTOR_DISPONIBLE = False
        detectar_sector_completo = limpiar_cache = None

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

try:
    from utils.chat_detector import detectar_intencion
    DETECTOR_DISPONIBLE = True
except ImportError:
    try:
        from chat_detector import detectar_intencion
        DETECTOR_DISPONIBLE = True
    except ImportError:
        DETECTOR_DISPONIBLE = False
        detectar_intencion = None

try:
    from utils.persistence import (guardar_negocio, cargar_negocios, eliminar_negocio, esta_disponible)
    PERSISTENCIA_DISPONIBLE = True
except ImportError:
    try:
        from persistence import (guardar_negocio, cargar_negocios, eliminar_negocio, esta_disponible)
        PERSISTENCIA_DISPONIBLE = True
    except ImportError:
        PERSISTENCIA_DISPONIBLE = False
        guardar_negocio = cargar_negocios = eliminar_negocio = esta_disponible = None

try:
    from config_app import obtener_usuario_actual
    USUARIO_DISPONIBLE = True
except ImportError:
    USUARIO_DISPONIBLE = False
    def obtener_usuario_actual(): return "usuario_default"

try:
    from utils.email_sender import email_sender
    EMAIL_DISPONIBLE = True
except ImportError:
    EMAIL_DISPONIBLE = False
    email_sender = None

try:
    from utils.social_poster import social_poster
    SOCIAL_DISPONIBLE = True
except ImportError:
    SOCIAL_DISPONIBLE = False
    social_poster = None

try:
    from utils.automation import scheduler, tarea_nocturna, tarea_diaria, tarea_semanal
    AUTOMATION_DISPONIBLE = True
except ImportError:
    AUTOMATION_DISPONIBLE = False
    scheduler = None

try:
    from utils.market_research import market_research
    RESEARCH_DISPONIBLE = True
except ImportError:
    RESEARCH_DISPONIBLE = False
    market_research = None


BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')
SECTORES_GENERICOS = ["negocio general", "general", "default", "", "negocio"]

def verificar_backend():
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

def obtener_ruta_web_local(negocio_id, web_id):
    return os.path.join("data", "webs_generadas", f"usuario_{negocio_id}", web_id, "index.html")

def leer_html_web(negocio_id, web_id):
    ruta = obtener_ruta_web_local(negocio_id, web_id)
    if os.path.exists(ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None
    return None

def hash_html(html):
    if not html: return "vacio"
    return hashlib.md5(html.encode("utf-8")).hexdigest()[:10]

def obtener_guia_dinamica(sector, nombre="", descripcion=""):
    if SECTOR_DETECTOR_DISPONIBLE and detectar_sector_completo:
        try:
            resultado = detectar_sector_completo(nombre, descripcion, sector)
            return {
                "guia": resultado.get("guia", ""),
                "contexto": resultado.get("contexto", sector),
                "keywords": resultado.get("keywords_imagenes", []),
                "sector_key": resultado.get("sector_key", "default"),
                "fuente": resultado.get("fuente", "default"),
            }
        except Exception as e:
            print("[PANEL] Error guia: " + str(e))

    return {"guia": "", "contexto": sector, "keywords": [], "sector_key": "default", "fuente": "default"}

def _necesita_migracion(negocio):
    if not negocio: return False
    contexto = negocio.get("sector_contexto", "").lower().strip()
    key = negocio.get("sector_key", "").lower().strip()
    if not contexto: return True
    if contexto in SECTORES_GENERICOS: return True
    if not key or key == "default": return True
    if not negocio.get("sector_guia", "").strip(): return True
    return False

def _migrar_negocio_silencioso(negocio):
    try:
        nombre = negocio.get("nombre", "")
        descripcion = negocio.get("descripcion", "")
        sector = negocio.get("sector", "General")
        info = obtener_guia_dinamica(sector, nombre, descripcion)
        negocio["sector_contexto"] = info.get("contexto", sector)
        negocio["sector_key"] = info.get("sector_key", "default")
        negocio["sector_guia"] = info.get("guia", "")
        return True
    except Exception as e:
        print("[MIGRACION] Error (silencioso): " + str(e))
        return False

def migrar_negocios_viejos():
    if "negocios" not in st.session_state: return 0
    migrados = 0
    for neg_id, negocio in st.session_state.negocios.items():
        if _necesita_migracion(negocio):
            if _migrar_negocio_silencioso(negocio):
                migrados += 1
    if migrados > 0:
        st.session_state["_hash_negocios"] = "forzar_guardado"
    return migrados

def inicializar_session_state():
    if "negocio_seleccionado" not in st.session_state: st.session_state.negocio_seleccionado = None
    if "chat_historial" not in st.session_state:
        st.session_state.chat_historial = [{"role": "agent", "agente": "Orquestador", "content": "👋 ¡Bienvenido a SAMU IA! Soy tu asistente."}]
    if "scheduler_activo" not in st.session_state: st.session_state.scheduler_activo = False
    if "mostrar_crear_web" not in st.session_state: st.session_state.mostrar_crear_web = False
    if "web_preview_activa" not in st.session_state: st.session_state.web_preview_activa = None
    if "modal_modificar_web" not in st.session_state: st.session_state.modal_modificar_web = False
    if "modal_config_asistente" not in st.session_state: st.session_state.modal_config_asistente = False

    if "negocios" not in st.session_state:
        negocios_cargados = {}
        usuario_id = obtener_usuario_actual()

        if PERSISTENCIA_DISPONIBLE and esta_disponible():
            try:
                ok, data = cargar_negocios(usuario_id)
                if ok and data:
                    negocios_cargados = data
                    print("[PERSIST] Cargados " + str(len(data)) + " negocios")
                else:
                    print("[PERSIST] Sin negocios previos")
            except Exception as e:
                print("[PERSIST] Error cargando: " + str(e))
        else:
            print("[PERSIST] Supabase no disponible")

        if not negocios_cargados and ES_DUENO:
            negocios_cargados = {
                "buildsmart": {
                    "id": "buildsmart", "nombre": "BuildSmart", "icono": "🏗️",
                    "descripcion": "Mi negocio de construccion", "sector": "construccion",
                    "tipo": "desde_cero", "custom_personality": "",
                    "sector_contexto": "Constructora", "sector_key": "construccion",
                    "sector_guia": "Documenta servicios: obra civil, remodelacion, ampliacion.",
                    "metricas": {"Proyectos": 0, "Clientes": 0, "Ingresos": "$0", "Prospectos": 0},
                    "creditos": 12, "modificaciones_usadas": 0, "pago_web_hecha": False,
                    "sitio_web": {"url": "", "url_publica": "", "visitantes": 0, "ingresos": "$0.00", "actualizado": "HACE 1 HORA", "archivo_generado": None, "vinculada": False},
                    "rutinas": {"turno_nocturno": True, "diario": True, "semanal": False},
                    "equipos": [{"nombre": "Antonio", "rol": "Fundador", "email": "antonio@buildsmart.com"}],
                    "agentes": [
                        {"nombre": "Orquestador", "estado": "Activo", "rol": "Coordinador General"},
                        {"nombre": "Marketing", "estado": "Activo", "rol": "Contenido y SEO"},
                        {"nombre": "Ventas", "estado": "Activo", "rol": "Prospeccion y Cierre"}
                    ],
                    "tareas": [{"id": 1, "titulo": "Definir mision y vision", "categoria": "ESTRATEGIA", "estado": "TODO", "creditos": 1, "tiempo": "HACE 2H"}],
                    "documentos": [], "redes_sociales": {"twitter": {"conectado": False, "usuario": "", "ultimo_tweet": ""}, "instagram": {"conectado": False, "usuario": "", "ultimo_post": ""}, "linkedin": {"conectado": False, "usuario": ""}},
                    "anuncios": {"activo": False, "presupuesto_diario": "$0", "experimentos": []},
                    "correo": {"email": "contacto@buildsmart.com", "enviados": 0, "recibidos": 0, "ultimo": ""},
                    "timeline": [{"accion": "Negocio creado", "fecha": "2026-09-03 10:00", "tipo": "info"}],
                    "color": "#0f3460"
                }
            }

        st.session_state.negocios = negocios_cargados
        st.session_state["_hash_negocios"] = hash_html(str(negocios_cargados))

    if "migracion_hecha" not in st.session_state:
        try:
            migrar_negocios_viejos()
        except Exception as e:
            print("[MIGRACION] Error general (silencioso): " + str(e))
        st.session_state["migracion_hecha"] = True

def auto_guardar():
    if "negocios" not in st.session_state: return
    if not PERSISTENCIA_DISPONIBLE or not esta_disponible(): return
    negocios_actuales = st.session_state.negocios
    hash_actual = hash_html(str(negocios_actuales))
    if st.session_state.get("_hash_negocios") == hash_actual: return
    try:
        usuario_id = obtener_usuario_actual()
        guardados = 0; errores = 0
        for neg_id, neg_data in negocios_actuales.items():
            ok, msg = guardar_negocio(usuario_id, neg_id, neg_data)
            if ok: guardados += 1
            else: errores += 1
        print("[PERSIST] Guardados: " + str(guardados) + " | Errores: " + str(errores))
        st.session_state["_hash_negocios"] = hash_actual
    except Exception as e:
        print("[PERSIST] Error auto_guardar: " + str(e))

def crear_negocio(nombre, icono, descripcion, tipo="desde_cero", datos_extra=None):
    datos_extra = datos_extra or {}
    if "negocios" not in st.session_state: st.session_state.negocios = {}
    id_generado = re.sub(r'[^a-zA-Z0-9]', '_', nombre.lower()) + "_" + str(len(st.session_state.negocios) + 1)
    colores = ["#2ecc71", "#f39c12", "#9b59b6", "#1abc9c", "#e67e22", "#3498db", "#e74c3c", "#2c3e50"]
    color_idx = len(st.session_state.negocios) % len(colores)
    sector_real = datos_extra.get("sector", "General")

    if not sector_real or sector_real.lower() in ["general", ""]:
        info_auto = obtener_guia_dinamica("General", nombre, descripcion)
        if info_auto.get("contexto") and info_auto.get("contexto") != "Negocio general":
            sector_real = info_auto.get("contexto")

    info_sector = obtener_guia_dinamica(sector_real, nombre, descripcion)
    guia_sector = info_sector.get("guia", "")
    contexto_sector = info_sector.get("contexto", sector_real)
    sector_key = info_sector.get("sector_key", "default")

    if tipo == "desde_cero":
        tareas = [
            {"id": 1, "titulo": "Definir la mision y vision", "categoria": "ESTRATEGIA", "estado": "TODO", "creditos": 1, "tiempo": "PENDIENTE"},
            {"id": 2, "titulo": "Crear la pagina web", "categoria": "DISEÑO", "estado": "TODO", "creditos": 2, "tiempo": "PENDIENTE"},
            {"id": 3, "titulo": "Conseguir los primeros clientes", "categoria": "VENTAS", "estado": "TODO", "creditos": 2, "tiempo": "PENDIENTE"}
        ]
        agentes = [
            {"nombre": "Orquestador", "estado": "Activo", "rol": "Coordinador General"},
            {"nombre": "Marketing", "estado": "Activo", "rol": "Contenido y SEO"},
            {"nombre": "Ventas", "estado": "Activo", "rol": "Prospeccion y Cierre"}
        ]
        sitio_web = {"url": "", "url_publica": "", "visitantes": 0, "ingresos": "$0.00", "actualizado": "SIN CREAR", "archivo_generado": None, "vinculada": False}
        timeline_inicial = [
            {"accion": f"Negocio '{nombre}' creado desde cero", "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "tipo": "info"},
            {"accion": f"Sector detectado: {contexto_sector}", "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "tipo": "info"}
        ]
        mensaje = f"✅ ¡Negocio **{nombre}** creado desde cero! Tienes {len(tareas)} tareas iniciales. ¿Quieres generar tu web ahora?"
    else:
        tareas = [
            {"id": 1, "titulo": f"Digitalizar procesos de {contexto_sector}", "categoria": "ESTRATEGIA", "estado": "TODO", "creditos": 1, "tiempo": "PENDIENTE"},
            {"id": 2, "titulo": "Migrar informacion existente al sistema", "categoria": "OPERACIONES", "estado": "TODO", "creditos": 1, "tiempo": "PENDIENTE"},
            {"id": 3, "titulo": "Capacitar al equipo en la nueva plataforma", "categoria": "EQUIPO", "estado": "TODO", "creditos": 1, "tiempo": "PENDIENTE"}
        ]
        agentes = [
            {"nombre": "Orquestador", "estado": "Activo", "rol": "Coordinador General"},
            {"nombre": "Operaciones", "estado": "Activo", "rol": "Migracion y Procesos"}
        ]
        sitio_web = {"url": "", "url_publica": "", "visitantes": 0, "ingresos": "$0.00", "actualizado": "SIN WEB", "archivo_generado": None, "vinculada": False}
        timeline_inicial = [
            {"accion": f"Negocio '{nombre}' importado al sistema", "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "tipo": "info"},
            {"accion": f"Sector detectado: {contexto_sector}", "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "tipo": "info"}
        ]
        mensaje = f"✅ ¡Negocio **{nombre}** adaptado! Hemos preparado {len(tareas)} tareas segun tu sector."

    nuevo_negocio = {
        "id": id_generado, "nombre": nombre, "icono": icono, "descripcion": descripcion, "sector": sector_real,
        "sector_contexto": contexto_sector, "sector_key": sector_key, "sector_guia": guia_sector, "tipo": tipo,
        "custom_personality": "", "metricas": {"Proyectos": 0, "Clientes": 0, "Ingresos": "$0", "Prospectos": 0},
        "creditos": 10, "modificaciones_usadas": 0, "pago_web_hecha": False, "sitio_web": sitio_web,
        "rutinas": {"turno_nocturno": True, "diario": True, "semanal": False},
        "equipos": [{"nombre": "Fundador", "rol": "Propietario", "email": "fundador@empresa.com"}],
        "agentes": agentes, "tareas": tareas, "documentos": [],
        "redes_sociales": {"twitter": {"conectado": False, "usuario": "", "ultimo_tweet": ""}, "instagram": {"conectado": False, "usuario": "", "ultimo_post": ""}, "linkedin": {"conectado": False, "usuario": ""}},
        "anuncios": {"activo": False, "presupuesto_diario": "$0", "experimentos": []},
        "correo": {"email": f"{nombre.lower().replace(' ', '-')}@buildsmart.app", "enviados": 0, "recibidos": 0, "ultimo": ""},
        "timeline": timeline_inicial, "color": colores[color_idx]
    }
    st.session_state.negocios[id_generado] = nuevo_negocio
    st.session_state.chat_historial.append({"role": "agent", "agente": "Orquestador", "content": mensaje})
    st.session_state.negocio_seleccionado = id_generado
    return id_generado

def mover_tarea(negocio_id, tarea_id, nuevo_estado):
    negocio = st.session_state.negocios.get(negocio_id)
    if negocio:
        for tarea in negocio["tareas"]:
            if tarea["id"] == tarea_id:
                tarea["estado"] = nuevo_estado
                tarea["tiempo"] = f"HACE {random.randint(1, 60)} MIN"
                negocio["timeline"].append({
                    "accion": f"Tarea '{tarea['titulo'][:30]}...' movida a {nuevo_estado}",
                    "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "tipo": "tarea"
                })
                if nuevo_estado == "HECHO" and SISTEMA_CREDITOS_ACTIVO:
                    negocio["creditos"] = negocio.get("creditos", 10) + 1
                return True
    return False

# --- FUNCIONES DE IA Y WEB ---
def generar_sitio_web_con_ia(negocio_id, datos_extra=None):
    if not WEB_DISPONIBLE: return False, "❌ Modulo web no disponible"
    negocio = st.session_state.negocios.get(negocio_id)
    if not negocio: return False, "❌ Negocio no encontrado"
    if negocio['sitio_web'].get('archivo_generado'): return False, "⚠️ Este negocio ya tiene una web. Usa 'Modificar mi web' para hacer cambios."
    usuario_id = f"usuario_{negocio_id}"
    try:
        sector_negocio = negocio.get("sector", "General")
        datos_negocio = {
            "nombre": negocio["nombre"], "sector": sector_negocio, "descripcion": negocio["descripcion"],
            "publico_objetivo": datos_extra.get("publico_objetivo", "Clientes potenciales") if datos_extra else "Clientes potenciales",
            "diferenciadores": datos_extra.get("diferenciadores", "Calidad y experiencia") if datos_extra else "Calidad y experiencia",
        }
        if datos_extra is None: datos_extra = {}
        if "sector" not in datos_extra: datos_extra["sector"] = sector_negocio
        
        opciones = {
            "tipo_pagina": datos_extra.get("tipo_pagina", "Landing Page") if datos_extra else "Landing Page",
            "diseno": datos_extra.get("diseno", "Moderno") if datos_extra else "Moderno",
            "tono": datos_extra.get("tono", "Profesional") if datos_extra else "Profesional",
        }
        resultado = crear_web(usuario_id, datos_negocio, opciones)
        if not resultado["exito"]: return False, f"❌ Error generando web: {resultado.get('error', 'Desconocido')}"
        
        web_id = resultado.get("web_id")
        negocio['sitio_web']['archivo_generado'] = web_id
        negocio['sitio_web']['actualizado'] = "AHORA"
        negocio['sitio_web']['vinculada'] = False
        
        url_publica = ""
        if PUBLISHER_DISPONIBLE and publicar_web:
            print("\n[WEB] Publicando en Netlify...")
            resultado_pub = publicar_web(usuario_id, web_id)
            if resultado_pub.get("exito"):
                url_publica = resultado_pub.get("url_publica", "")
                tipo_pub = resultado_pub.get("tipo", "desconocido")
                print("[WEB] Publicado: " + str(url_publica) + " (" + tipo_pub + ")")
                negocio['sitio_web']['url'] = url_publica
                negocio['sitio_web']['url_publica'] = url_publica
                negocio['timeline'].append({"accion": f"🚀 Web publicada en internet: {url_publica}", "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "tipo": "info"})
            else:
                negocio['sitio_web']['url'] = resultado.get("url_publicada", "")
                negocio['sitio_web']['url_publica'] = ""
        else:
            negocio['sitio_web']['url'] = resultado.get("url_publicada", "")
            negocio['sitio_web']['url_publica'] = ""

        negocio['timeline'].append({"accion": f"🌐 Web generada con IA: {web_id[:8]}", "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "tipo": "info"})
        msg = f"✅ Web generada correctamente.\n\n"
        if url_publica:
            msg += f"🌎 **URL publica:** {url_publica}\n\nYa puedes compartirla con tus clientes."
        msg += f"\n\nTienes {MODIFICACIONES_GRATIS} modificaciones gratis."
        return True, msg
    except Exception as e: return False, f"❌ Error: {str(e)}"

def modificar_web_con_ia(negocio_id, instruccion):
    if not EDITOR_DISPONIBLE: return False, "❌ Modulo de edicion no disponible"
    negocio = st.session_state.negocios.get(negocio_id)
    if not negocio: return False, "❌ Negocio no encontrado"
    web_id = negocio['sitio_web'].get('archivo_generado')
    if not web_id: return False, "⚠️ Primero debes generar tu web."
    
    usadas = negocio.get("modificaciones_usadas", 0)
    
    # --- NUEVA LÓGICA DE COBRO ---
    if usadas >= MODIFICACIONES_GRATIS:
        from panels.web.pagos import obtener_proveedor, proveedor_actual
        prov_nombre = proveedor_actual()
        proveedor = obtener_proveedor(prov_nombre, {})
        pedido_id = f"mod_extra_{negocio_id}_{int(datetime.datetime.now().timestamp())}"
        
        res_pago = proveedor.crear_pago(
            pedido_id=pedido_id,
            monto=COSTO_MODIFICACION_EXTRA,
            descripcion=f"Modificacion extra web - {negocio.get('nombre')}",
            metadata={"email": "cliente@samu-ia.com"}
        )
        
        if res_pago.get("exito"):
            url_pago = res_pago.get("url_pago")
            if url_pago:
                return False, f"⚠️ Has agotado las {MODIFICACIONES_GRATIS} modificaciones gratis.\n\nPara aplicar este nuevo cambio, debes pagar **${COSTO_MODIFICACION_EXTRA} USD**.\n\n👉 [**Haz clic aquí para pagar con ePayco**]({url_pago})"
            else:
                return False, f"⚠️ Has agotado las {MODIFICACIONES_GRATIS} modificaciones gratis.\n\nEsta modificacion tiene un costo de **${COSTO_MODIFICACION_EXTRA} USD**.\n\nPor favor transfiere usando los datos manuales y envía el comprobante a pagos@samu-ia.com."
        else:
            return False, f"⚠️ Has agotado las {MODIFICACIONES_GRATIS} modificaciones gratis.\n\nEsta modificacion tiene un costo de **${COSTO_MODIFICACION_EXTRA} USD**.\n\n(Ocurrió un error generando el link de pago automático)."

    usuario_id = f"usuario_{negocio_id}"
    contexto = f"Negocio: {negocio.get('nombre', '')}\nSector: {negocio.get('sector', 'General')}\nDescripcion: {negocio.get('descripcion', '')}"
    
    try:
        resultado = editar_y_guardar_v2(usuario_id, web_id, instruccion, contexto)
        if resultado.get("exito"):
            negocio["modificaciones_usadas"] = usadas + 1
            negocio['sitio_web']['actualizado'] = "AHORA"
            restantes = MODIFICACIONES_GRATIS - negocio["modificaciones_usadas"]
            aplicados = resultado.get("aplicados", [])
            fallidos = resultado.get("fallidos", [])
            cambios_ok = resultado.get("cambios_aplicados", 0)
            cambios_total = resultado.get("cambios_totales", 0)
            
            url_publica = negocio['sitio_web'].get('url_publica', '')
            if PUBLISHER_DISPONIBLE and publicar_web:
                print("\n[MOD] Re-publicando en Netlify...")
                resultado_pub = publicar_web(usuario_id, web_id)
                if resultado_pub.get("exito"):
                    url_publica = resultado_pub.get("url_publica", "")
                    negocio['sitio_web']['url'] = url_publica
                    negocio['sitio_web']['url_publica'] = url_publica
                    print("[MOD] Republicado: " + str(url_publica))
            
            negocio['timeline'].append({"accion": f"✏️ Web modificada: {cambios_ok}/{cambios_total} cambios ({negocio['modificaciones_usadas']}/{MODIFICACIONES_GRATIS})", "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "tipo": "info"})
            st.session_state.web_preview_activa = web_id
            
            msg = "📊 **Resumen de tu solicitud:**\n\n"
            if aplicados:
                msg += f"✅ **{len(aplicados)} APLICADO(S):**\n"
                for a in aplicados[:5]:
                    detalle = a.get("detalle", "")
                    if detalle: msg += f"   • {a['descripcion']} — _{detalle}_\n"
                    else: msg += f"   • {a['descripcion']}\n"
                if len(aplicados) > 5: msg += f"   • ... y {len(aplicados) - 5} mas\n"
                msg += "\n"
            if fallidos:
                msg += f"❌ **{len(fallidos)} NO APLICADO(S):**\n"
                for f in fallidos[:5]:
                    msg += f"   • {f['descripcion']}\n     Motivo: {f['razon']}\n"
                    if f.get("sugerencia"): msg += f"     Sugerencia: _{f['sugerencia']}_\n"
                if len(fallidos) > 5: msg += f"   • ... y {len(fallidos) - 5} mas\n"
                msg += "\n"
            if url_publica: msg += f"🌎 **URL publica actualizada:** {url_publica}\n\n"
            if restantes > 0: msg += f"💡 Te quedan **{restantes} de {MODIFICACIONES_GRATIS}** modificaciones gratis."
            else: msg += f"⚠️ Has usado tus {MODIFICACIONES_GRATIS} modificaciones gratis. La proxima tendra un costo de **${COSTO_MODIFICACION_EXTRA} USD**."
            return True, msg
        else:
            fallidos = resultado.get("fallidos", [])
            if fallidos:
                msg = "❌ **No pude aplicar los cambios:**\n\n"
                for f in fallidos[:5]:
                    msg += f"   • {f['descripcion']}\n     Motivo: {f['razon']}\n"
                    if f.get("sugerencia"): msg += f"     Sugerencia: _{f['sugerencia']}_\n"
                msg += "\n💡 Intenta reformular tu peticion de otra forma."
                return False, msg
            else: return False, f"❌ No pude aplicar el cambio: {resultado.get('error', 'Desconocido')}"
    except Exception as e: return False, f"❌ Error: {str(e)}"

def vincular_web_existente(negocio_id, url):
    negocio = st.session_state.negocios.get(negocio_id)
    if not negocio: return False, "❌ Negocio no encontrado"
    if not url or not url.strip(): return False, "⚠️ Ingresa una URL valida."
    url = url.strip()
    if not (url.startswith("http://") or url.startswith("https://")): url = "https://" + url
    negocio['sitio_web']['url'] = url
    negocio['sitio_web']['url_publica'] = url
    negocio['sitio_web']['actualizado'] = "VINCULADA"
    negocio['sitio_web']['vinculada'] = True
    negocio['sitio_web']['archivo_generado'] = None
    negocio['timeline'].append({"accion": f"🔗 Web vinculada: {url}", "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "tipo": "info"})
    return True, f"✅ Web vinculada: {url}"

def configurar_asistente(negocio_id, prompt_personalizado):
    negocio = st.session_state.negocios.get(negocio_id)
    if not negocio: return False, "❌ Negocio no encontrado"
    if not prompt_personalizado or not prompt_personalizado.strip(): return False, "⚠️ El prompt no puede estar vacio"
    negocio["custom_personality"] = prompt_personalizado.strip()
    negocio['timeline'].append({"accion": "⚙️ Personalidad del asistente actualizada", "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "tipo": "info"})
    preview = prompt_personalizado.strip()[:120]
    if len(prompt_personalizado) > 120: preview += "..."
    return True, f"✅ Personalidad guardada correctamente.\n\n**Vista previa:**\n_{preview}_\n\nTu asistente ahora seguira estas instrucciones en todas las consultas."

def enviar_correo_negocio(negocio_id, destino, asunto, contenido):
    if not EMAIL_DISPONIBLE: return "❌ Modulo email no disponible"
    negocio = st.session_state.negocios.get(negocio_id)
    if not negocio: return "❌ Negocio no encontrado"
    try:
        resultado = email_sender.enviar_correo(destino, asunto, contenido)
        negocio['correo']['enviados'] += 1
        negocio['correo']['ultimo'] = asunto
        return resultado
    except Exception as e: return f"❌ Error: {str(e)}"

def publicar_en_twitter(negocio_id, mensaje):
    if not SOCIAL_DISPONIBLE: return "❌ Modulo social no disponible"
    negocio = st.session_state.negocios.get(negocio_id)
    if not negocio: return "❌ Negocio no encontrado"
    try: return social_poster.publicar_twitter(mensaje)
    except Exception as e: return f"❌ Error: {str(e)}"

def iniciar_automatizacion():
    if not AUTOMATION_DISPONIBLE: return "❌ Modulo de automatizacion no disponible"
    if st.session_state.scheduler_activo: return "⏹️ La automatizacion ya esta activa"
    try:
        scheduler.agregar_tarea("Turno Nocturno", tarea_nocturna, 60)
        scheduler.agregar_tarea("Tarea Diaria", tarea_diaria, 360)
        scheduler.agregar_tarea("Tarea Semanal", tarea_semanal, 10080)
        resultado = scheduler.iniciar()
        st.session_state.scheduler_activo = True
        return resultado
    except Exception as e: return f"❌ Error: {str(e)}"

def detener_automatizacion():
    if not AUTOMATION_DISPONIBLE: return "❌ Modulo de automatizacion no disponible"
    try:
        resultado = scheduler.detener()
        st.session_state.scheduler_activo = False
        return resultado
    except Exception as e: return f"❌ Error: {str(e)}"

def investigar_mercado(tema):
    if not RESEARCH_DISPONIBLE: return "❌ Modulo de investigacion no disponible"
    try: return market_research.investigar(tema)
    except Exception as e: return f"❌ Error: {str(e)}"

def construir_contexto_negocio():
    if not st.session_state.negocio_seleccionado: return "No hay negocio seleccionado."
    negocio = st.session_state.negocios.get(st.session_state.negocio_seleccionado)
    if not negocio: return "Negocio no encontrado."
    
    # REGLA ESPECIAL PARA EL DUEÑO
    if ES_DUENO:
        return f"""
- MODO ADMINISTRADOR: El usuario es el DUEÑO de SAMU IA.
- Estás en el Panel de Control Total.
- El "negocio" seleccionado en pantalla ({negocio.get('nombre')}) es solo para probar el sistema.
- Recuerda: SAMU IA es la plataforma principal, no un cliente de Web Gancho.
- Tu objetivo es ayudar al dueño a gestionar la plataforma, revisar métricas y probar funcionalidades.
- Modo actual: {MODO}
"""

    # CONTEXTO NORMAL PARA CLIENTES
    total_tareas = len(negocio.get("tareas", []))
    tareas_hechas = len([t for t in negocio.get("tareas", []) if t["estado"] == "HECHO"])
    tareas_pendientes = total_tareas - tareas_hechas
    mods_usadas = negocio.get("modificaciones_usadas", 0)
    mods_restantes = max(0, MODIFICACIONES_GRATIS - mods_usadas)
    tiene_web = bool(negocio['sitio_web'].get('archivo_generado'))
    web_vinculada = negocio['sitio_web'].get('vinculada', False)
    web_id = negocio['sitio_web'].get('archivo_generado', "")
    url_publica = negocio['sitio_web'].get('url_publica', "")
    if tiene_web: estado_web = f"SI tiene web generada (URL: {url_publica[:60] if url_publica else 'sin URL publica'})"
    elif web_vinculada: estado_web = f"SI tiene web vinculada externa ({negocio['sitio_web'].get('url', '')})"
    else: estado_web = "NO tiene web aun"
    tiene_personalidad = bool(negocio.get("custom_personality", ""))
    sector_contexto = negocio.get("sector_contexto", negocio.get("sector", "General"))
    return f"""
- Negocio: {negocio.get('nombre', '')}
- Sector: {negocio.get('sector', 'General')}
- Contexto del sector: {sector_contexto}
- Descripcion: {negocio.get('descripcion', '')}
- Web: {estado_web}
- Modificaciones usadas: {mods_usadas}/{MODIFICACIONES_GRATIS} (quedan {mods_restantes} gratis)
- Tareas: {total_tareas} total, {tareas_pendientes} pendientes
- Correos enviados: {negocio.get('correo', {}).get('enviados', 0)}
- Agentes: {len(negocio.get('agentes', []))}
- Personalidad custom: {'SI' if tiene_personalidad else 'NO (usa default)'}
- Modo: {MODO}
"""

def _construir_mensaje_estado(negocio):
    return "📊 **Estado del negocio**\n(Detalles en la interfaz)"

def _construir_mensaje_fuera_de_tema(nombre_negocio):
    return f"""🚫 **Estoy enfocado exclusivamente en {nombre_negocio}.**
Habla como quieras, pero mantengamos el foco en tu negocio. 🎯"""

def _ejecutar_intent(intent, params, mensaje_original):
    if intent == "crear_web":
        if not st.session_state.negocio_seleccionado: return "🌐 Selecciona un negocio primero.", "Sistema"
        negocio = st.session_state.negocios[st.session_state.negocio_seleccionado]
        if negocio['sitio_web'].get('archivo_generado'): return "⚠️ Ya tienes una web. Dime que quieres cambiar y la modifico.", "Web"
        resultado, msg = generar_sitio_web_con_ia(st.session_state.negocio_seleccionado)
        return msg, "Web Generator" if resultado else "Sistema"
    if intent == "modificar_web":
        if not st.session_state.negocio_seleccionado: return "🌐 Selecciona un negocio primero.", "Sistema"
        negocio = st.session_state.negocios[st.session_state.negocio_seleccionado]
        if not negocio['sitio_web'].get('archivo_generado'): return "⚠️ Aun no tienes web. Dime 'crear mi web' para generarla.", "Web"
        instruccion = params.get("instruccion", mensaje_original)
        resultado, msg = modificar_web_con_ia(st.session_state.negocio_seleccionado, instruccion)
        return msg, "Web Editor" if resultado else "Sistema"
    if intent == "vincular_web":
        if not st.session_state.negocio_seleccionado: return "🌐 Selecciona un negocio primero.", "Sistema"
        url = params.get("url", "")
        if not url: return "🔗 Dime la URL de tu web.", "Web"
        ok, msg = vincular_web_existente(st.session_state.negocio_seleccionado, url)
        return msg, "Web" if ok else "Sistema"
    if intent == "ver_modificaciones":
        if not st.session_state.negocio_seleccionado: return "✏️ Selecciona un negocio primero.", "Web"
        negocio = st.session_state.negocios[st.session_state.negocio_seleccionado]
        usadas = negocio.get("modificaciones_usadas", 0)
        restantes = max(0, MODIFICACIONES_GRATIS - usadas)
        return f"✏️ Modificaciones usadas: {usadas}/{MODIFICACIONES_GRATIS}\nTe quedan **{restantes} gratis**.", "Web"
    if intent == "ver_tareas":
        if not st.session_state.negocio_seleccionado: return "📋 Selecciona un negocio primero.", "Operaciones"
        negocio = st.session_state.negocios[st.session_state.negocio_seleccionado]
        pendientes = [t for t in negocio["tareas"] if t["estado"] != "HECHO"]
        if pendientes:
            lista = "\n".join([f"  • {t['titulo']} ({t['estado']})" for t in pendientes])
            return f"📋 Tienes {len(pendientes)} tareas pendientes:\n{lista}", "Operaciones"
        return "✅ No tienes tareas pendientes. ¡Todo al dia!", "Operaciones"
    if intent == "crear_tarea":
        if not st.session_state.negocio_seleccionado: return "📋 Selecciona un negocio primero.", "Operaciones"
        negocio = st.session_state.negocios[st.session_state.negocio_seleccionado]
        titulo = params.get("titulo", mensaje_original)
        categoria = params.get("categoria", "ESTRATEGIA")
        nuevo_id = max([t["id"] for t in negocio["tareas"]] + [0]) + 1
        negocio["tareas"].append({"id": nuevo_id, "titulo": titulo, "categoria": categoria, "estado": "TODO", "creditos": 1, "tiempo": "PENDIENTE"})
        negocio["timeline"].append({"accion": f"➕ Tarea creada: '{titulo[:40]}...'", "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "tipo": "tarea"})
        return f"✅ Tarea creada: '{titulo}'", "Operaciones"
    if intent == "enviar_correo":
        if not EMAIL_DISPONIBLE: return "❌ Sistema de correo no disponible.", "Sistema"
        destino = params.get("destino", "")
        asunto = params.get("asunto", "Mensaje desde BuildSmart")
        contenido = params.get("contenido", "Mensaje enviado desde BuildSmart")
        if not destino: return "📧 Necesito un email. Formato: 'manda un correo a correo@ejemplo.com'", "Correo"
        try:
            resultado = email_sender.enviar_correo(destino, asunto, contenido)
            if st.session_state.negocio_seleccionado and "✅" in resultado:
                negocio = st.session_state.negocios[st.session_state.negocio_seleccionado]
                negocio['correo']['enviados'] += 1
                negocio['correo']['ultimo'] = asunto
            return resultado, "Correo"
        except Exception as e: return f"❌ Error: {str(e)}", "Sistema"
    if intent == "investigar":
        tema = params.get("tema", mensaje_original)
        return f"🔍 Usa la seccion 'Investigacion de Mercado' en el dashboard para investigar: {tema}", "Sistema"
    if intent == "ver_web":
        if not st.session_state.negocio_seleccionado: return "🌐 Selecciona un negocio primero.", "Web"
        negocio = st.session_state.negocios[st.session_state.negocio_seleccionado]
        url_publica = negocio['sitio_web'].get('url_publica', '')
        web_id = negocio['sitio_web'].get('archivo_generado')
        if url_publica:
            st.session_state.web_preview_activa = web_id
            return f"🌎 **Tu web publica:** {url_publica}\n\nCompartela con tus clientes.", "Web"
        elif web_id:
            st.session_state.web_preview_activa = web_id
            return "👁️ Mira abajo, en 'MIS PAGINAS WEB' esta tu vista previa.", "Web"
        elif negocio['sitio_web'].get('vinculada'): return f"🔗 Tu web esta vinculada: {negocio['sitio_web']['url']}", "Web"
        return "⚠️ Aun no tienes web.", "Web"
    if intent == "estado_negocio":
        if not st.session_state.negocio_seleccionado: return "📊 Selecciona un negocio primero.", "Sistema"
        negocio = st.session_state.negocios.get(st.session_state.negocio_seleccionado)
        if not negocio: return "📊 Negocio no encontrado.", "Sistema"
        return _construir_mensaje_estado(negocio), "Estado"
    if intent == "configurar_asistente":
        if not st.session_state.negocio_seleccionado: return "🌐 Selecciona un negocio primero.", "Sistema"
        prompt_personalizado = params.get("prompt", mensaje_original)
        ok, msg = configurar_asistente(st.session_state.negocio_seleccionado, prompt_personalizado)
        return msg, "Configurador" if ok else "Sistema"
    if intent == "fuera_de_tema":
        nombre_negocio = "tu negocio"
        if st.session_state.negocio_seleccionado:
            negocio = st.session_state.negocios.get(st.session_state.negocio_seleccionado)
            if negocio: nombre_negocio = negocio.get('nombre', 'tu negocio')
        return _construir_mensaje_fuera_de_tema(nombre_negocio), "Orquestador"
    if intent == "ayuda":
        return """
📚 **PUEDES PEDIRME (en tus palabras):**

**🌐 Web:**
- "hazme la web" (si no tienes)
- "cambia el color del titulo a rojo"
- "cuantas modificaciones me quedan"
- "dame la URL de mi web"

**📋 Tareas:**
- "que tengo pendiente"
- "agrega tarea: llamar a Juan"

**📧 Correo:**
- "manda un correo a juan@x.com"

**📊 Estado:**
- "como va mi negocio"

**⚙️ Personalidad:**
- "Eres SAMU IA, actua como Director de Operaciones..." (personaliza el asistente)

_Habla como quieras. Entiendo dialectos, typos y spanglish._ 🎯
""", "Orquestador"
    return None, None

def _obtener_personalidad(negocio):
    if not negocio: return PERSONALIDAD_DEFAULT
    custom = negocio.get("custom_personality", "")
    if custom and custom.strip(): return custom.strip()
    return PERSONALIDAD_DEFAULT

def responder_chat(mensaje, BACKEND_ACTIVO):
    if not DETECTOR_DISPONIBLE: return "❌ Sistema de chat no disponible.", "Sistema"
    contexto = construir_contexto_negocio()
    resultado = detectar_intencion(mensaje, contexto)
    if not resultado["exito"]: return f"❌ No pude entender tu mensaje. Intenta de nuevo.\n\n_Detalle: {resultado.get('error', '')[:100]}_", "Sistema"
    intent = resultado["intent"]
    params = resultado["params"]
    confianza = resultado["confianza"]
    respuesta, agente = _ejecutar_intent(intent, params, mensaje)
    if respuesta is not None:
        if confianza < 0.6 and intent == "consultar": respuesta += f"\n\n_No estoy 100% seguro. Si queria otra cosa, intenta de nuevo._"
        return respuesta, agente

    if GATEWAY_DISPONIBLE and gateway is not None:
        try:
            negocio = None
            if st.session_state.negocio_seleccionado: negocio = st.session_state.negocios.get(st.session_state.negocio_seleccionado)
            personalidad = _obtener_personalidad(negocio)
            sistema = f"""{personalidad}

=========================================================
CONTEXTO DEL USUARIO (datos reales):
=========================================================
{contexto}

=========================================================
REGLAS OBLIGATORIAS (CRITICAS):
=========================================================

1. SOLO hablas de temas relacionados con el negocio del usuario:
   - Su web (crear, modificar, ver)
   - Sus tareas
   - Su correo
   - Sus redes sociales
   - Su investigacion de mercado
   - Como usar BuildSmart
   - Configurar la personalidad del asistente

2. NUNCA respondas sobre temas ajenos al negocio (chistes, historia, politica, ciencia, etc.)

3. USA SOLO LOS DATOS del CONTEXTO de arriba.
   NO INVENTES ventas, clientes, inventario, contabilidad o metricas.

4. Si te preguntan por algo que NO esta en el contexto:
   "Esa funcion estara disponible pronto. Por ahora puedo ayudarte con: web, tareas, correo, redes sociales e investigacion."

5. Responde en espanol claro y breve.
6. Entiende dialectos latinoamericanos, typos y spanglish.
7. Se util, amable y profesional.
8. Menciona funcionalidades futuras (contabilidad, inventario con codigo de barras) cuando sea relevante.
"""
            respuesta_ia, fuente_ia = gateway.chat_inteligente(mensaje, sistema)
            icono = "🧠" if fuente_ia == "local" else "☁️"
            return f"{respuesta_ia}\n\n---\n{icono} *Usando: {fuente_ia}*", f"Asistente ({fuente_ia})"
        except Exception as e: return f"❌ Error generando respuesta: {str(e)}", "Sistema"

    return "❌ No pude procesar tu mensaje. Intenta con: `ayuda`", "Sistema"


# --- CALLBACKS PARA EVITAR RERUN INFINITO EN BOTONES ---
def _cb_seleccionar_negocio(key):
    st.session_state.negocio_seleccionado = key

def _cb_mover_tarea(negocio_id, tarea_id, nuevo_estado):
    mover_tarea(negocio_id, tarea_id, nuevo_estado)


def renderizar_seleccion_negocio():
    st.subheader("📋 Tus Negocios")
    if st.session_state.negocios:
        cols = st.columns(min(len(st.session_state.negocios), 4))
        for idx, (key, negocio) in enumerate(st.session_state.negocios.items()):
            with cols[idx % 4]:
                selected = st.session_state.negocio_seleccionado == key
                border_color = negocio["color"] if selected else "#e0e0e0"
                bg_color = "#f0f4ff" if selected else "white"
                creditos_html = f'<span>💳 {negocio.get("creditos", 0)}</span>' if MOSTRAR_CREDITOS else ""
                icono_str = negocio.get("icono", "") or ""
                icono_html = f'<span style="font-size: 2rem;">{icono_str}</span>' if icono_str else ""

                html_card = (
                    f'<div class="business-card" style="border-color: {border_color}; background: {bg_color}; padding: 10px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px;">'
                    f'<div style="display: flex; justify-content: space-between; align-items: center;">'
                    f'<div>{icono_html}<h4 style="margin: 0; color: {negocio["color"]};">{negocio["nombre"]}</h4><small style="color: #888;">{negocio["descripcion"][:40]}...</small></div>'
                    f'<div><span style="font-size: 0.8rem;">{"✅" if selected else "🔘"}</span></div>'
                    f'</div>'
                    f'<div style="display: flex; gap: 0.5rem; margin-top: 0.5rem; font-size: 0.7rem;">'
                    f'<span>📋 {negocio["metricas"]["Proyectos"]}</span><span>👥 {negocio["metricas"]["Clientes"]}</span>'
                    f'<span>💰 {negocio["metricas"]["Ingresos"]}</span>{creditos_html}'
                    f'</div></div>'
                )
                st.markdown(html_card, unsafe_allow_html=True)
                st.button("Seleccionar", key=f"select_{key}", use_container_width=True, on_click=_cb_seleccionar_negocio, args=(key,))
    else:
        st.info("👈 Crea tu primer negocio usando el boton '➕ CREAR NEGOCIO' en el panel lateral.")
    st.divider()

def renderizar_dashboard_negocio():
    if not st.session_state.negocio_seleccionado or st.session_state.negocio_seleccionado not in st.session_state.negocios:
        st.info("👈 Selecciona un negocio para ver su dashboard.")
        return

    negocio = st.session_state.negocios[st.session_state.negocio_seleccionado]
    st.markdown(f"## {negocio.get('icono', '')} {negocio['nombre']}".strip())
    
    if MOSTRAR_CREDITOS:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col5: st.metric("💳 Creditos", negocio.get("creditos", 0))
    else:
        col1, col2, col3, col4 = st.columns(4)

    with col1: st.metric("📋 Proyectos", negocio["metricas"]["Proyectos"])
    with col2: st.metric("👥 Clientes", negocio["metricas"]["Clientes"])
    with col3: st.metric("💰 Ingresos", negocio["metricas"]["Ingresos"])
    with col4: st.metric("🎯 Prospectos", negocio["metricas"]["Prospectos"])

    st.subheader("📋 Tareas")
    tareas_todo = [t for t in negocio["tareas"] if t["estado"] == "TODO"]
    tareas_progreso = [t for t in negocio["tareas"] if t["estado"] == "EN_PROGRESO"]
    tareas_hecho = [t for t in negocio["tareas"] if t["estado"] == "HECHO"]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### ⏳ TODO")
        for tarea in tareas_todo:
            with st.container(border=True):
                st.markdown(f"**{tarea['titulo']}**")
                st.button("▶️ Iniciar", key=f"iniciar_{tarea['id']}", on_click=_cb_mover_tarea, args=(st.session_state.negocio_seleccionado, tarea["id"], "EN_PROGRESO"))

    with col2:
        st.markdown("### 🔄 En Progreso")
        for tarea in tareas_progreso:
            with st.container(border=True):
                st.markdown(f"**{tarea['titulo']}**")
                col_a, col_b = st.columns(2)
                with col_a: st.button("⬅️ Volver", key=f"volver_{tarea['id']}", on_click=_cb_mover_tarea, args=(st.session_state.negocio_seleccionado, tarea["id"], "TODO"))
                with col_b: st.button("✅", key=f"completar_{tarea['id']}", on_click=_cb_mover_tarea, args=(st.session_state.negocio_seleccionado, tarea["id"], "HECHO"))

    with col3:
        st.markdown("### ✅ HECHO")
        for tarea in tareas_hecho:
            with st.container(border=True):
                st.markdown(f"**{tarea['titulo']}**")

    st.divider()

def renderizar_chat(BACKEND_ACTIVO):
    st.divider()
    st.subheader("💬 Chat con Agentes")

    with st.container(border=True):
        if st.session_state.chat_historial:
            for msg in st.session_state.chat_historial[-10:]:
                if msg["role"] == "user":
                    st.markdown(f"**👤 Tu:** {msg['content']}")
                else:
                    agente_nombre = msg.get('agente', 'Agente')
                    st.markdown(f"**🤖 {agente_nombre}:** {msg['content']}")
                st.divider()

    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            mensaje = st.text_input("Habla como quieras...", key="chat_input", label_visibility="collapsed")
        with col2:
            enviar = st.form_submit_button("📤 Enviar", use_container_width=True)

        if enviar and mensaje:
            st.session_state.chat_historial.append({"role": "user", "content": mensaje})
            with st.spinner("🤖 Procesando..."):
                respuesta, agente = responder_chat(mensaje, BACKEND_ACTIVO)
                st.session_state.chat_historial.append({"role": "agent", "agente": agente, "content": respuesta})
            st.rerun()