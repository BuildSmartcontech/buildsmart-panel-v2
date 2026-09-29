# panels/panel_base_hooks.py
# ============================================
# HOOKS DE PANEL_BASE - SAMU IA
# ============================================
# V2.1: Guarda reportes de analisis en tabla reportes
# V2.0: Analisis profundo
# V1.0: Logging de eventos
# ============================================

import uuid as _uuid_lib


def _uuid_valido(val):
    """Verifica si un string es UUID valido."""
    if not val:
        return False
    try:
        _uuid_lib.UUID(str(val))
        return True
    except Exception:
        return False


def aplicar_hooks():
    """Envuelve funciones clave de panel_base."""
    try:
        from panels import panel_base as _base
    except Exception as e:
        print(f"[hooks] No se pudo importar panel_base: {e}")
        return

    if getattr(_base, "_hooks_aplicados", False):
        return

    # Logging
    try:
        from utils.logger import log_evento, log_error
        _aplicar_hooks_logging(_base, log_evento, log_error)
        print("[hooks] Logging hooks aplicados")
    except Exception as e:
        print(f"[hooks] Error aplicando hooks de logging: {e}")

    # Analisis profundo
    try:
        _aplicar_hook_analisis(_base)
        print("[hooks] Analisis profundo hook aplicado")
    except Exception as e:
        print(f"[hooks] Error aplicando hook de analisis: {e}")

    _base._hooks_aplicados = True


# ==========================================
# LOGGING (V1.0)
# ==========================================
def _aplicar_hooks_logging(_base, log_evento, log_error):
    """Envuelve funciones con logging."""

    _orig_crear_negocio = _base.crear_negocio

    def crear_negocio_hooked(nombre, icono, descripcion, tipo="desde_cero", datos_extra=None):
        negocio_id = _orig_crear_negocio(nombre, icono, descripcion, tipo, datos_extra)
        try:
            log_evento(
                "crear_negocio",
                negocio_id=negocio_id,
                detalle={"nombre": str(nombre)[:100], "tipo": str(tipo)[:30], "origen": "hook"},
            )
        except Exception:
            pass
        return negocio_id

    _base.crear_negocio = crear_negocio_hooked

    _orig_mover_tarea = _base.mover_tarea

    def mover_tarea_hooked(negocio_id, tarea_id, nuevo_estado):
        resultado = _orig_mover_tarea(negocio_id, tarea_id, nuevo_estado)
        if resultado:
            try:
                log_evento(
                    "mover_tarea",
                    negocio_id=negocio_id,
                    detalle={"tarea_id": tarea_id, "nuevo_estado": str(nuevo_estado)[:30], "origen": "hook"},
                )
            except Exception:
                pass
        return resultado

    _base.mover_tarea = mover_tarea_hooked

    _orig_generar_web = _base.generar_sitio_web_con_ia

    def generar_web_hooked(negocio_id, datos_extra=None):
        exito, msg = _orig_generar_web(negocio_id, datos_extra)
        try:
            if exito:
                log_evento(
                    "generar_web",
                    negocio_id=negocio_id,
                    detalle={"exito": True, "msg": str(msg)[:200], "origen": "hook"},
                )
            else:
                log_error("web_generator", str(msg)[:200], negocio_id=negocio_id)
        except Exception:
            pass
        return exito, msg

    _base.generar_sitio_web_con_ia = generar_web_hooked

    _orig_modificar_web = _base.modificar_web_con_ia

    def modificar_web_hooked(negocio_id, instruccion):
        exito, msg = _orig_modificar_web(negocio_id, instruccion)
        try:
            log_evento(
                "modificar_web",
                negocio_id=negocio_id,
                detalle={"instruccion": str(instruccion)[:200], "exito": exito, "origen": "hook"},
            )
        except Exception:
            pass
        return exito, msg

    _base.modificar_web_con_ia = modificar_web_hooked

    _orig_vincular = _base.vincular_web_existente

    def vincular_hooked(negocio_id, url):
        exito, msg = _orig_vincular(negocio_id, url)
        try:
            if exito:
                log_evento(
                    "vincular_web",
                    negocio_id=negocio_id,
                    detalle={"url": str(url)[:200], "origen": "hook"},
                )
        except Exception:
            pass
        return exito, msg

    _base.vincular_web_existente = vincular_hooked

    _orig_config_asistente = _base.configurar_asistente

    def config_asistente_hooked(negocio_id, prompt_personalizado):
        exito, msg = _orig_config_asistente(negocio_id, prompt_personalizado)
        try:
            if exito:
                log_evento(
                    "configurar_asistente",
                    negocio_id=negocio_id,
                    detalle={"longitud": len(str(prompt_personalizado)), "origen": "hook"},
                )
        except Exception:
            pass
        return exito, msg

    _base.configurar_asistente = config_asistente_hooked


# ==========================================
# GUARDAR REPORTE (V2.1)
# ==========================================
def _guardar_reporte(consulta, resultado, contexto_usuario=None):
    """Guarda el reporte generado en la tabla 'reportes'."""
    try:
        from utils.supabase_rest import supabase_rest
        if not supabase_rest.disponible:
            return

        from config_app import obtener_usuario_actual
        usuario_id = obtener_usuario_actual() or "anonimo"

        # Negocio (si aplica)
        negocio_id = None
        if contexto_usuario:
            # El contexto usuario trae el nombre pero necesitamos el ID
            try:
                import streamlit as st
                negocio_sel = st.session_state.get("negocio_seleccionado")
                if negocio_sel and _uuid_valido(negocio_sel):
                    negocio_id = negocio_sel
            except Exception:
                pass

        payload = {
            "usuario_id": usuario_id,
            "negocio_id": negocio_id,
            "tipo": resultado.get("tipo", "usuario"),
            "subtipo": resultado.get("subtipo", "general"),
            "consulta": str(consulta)[:2000],
            "reporte": str(resultado.get("reporte", ""))[:50000],
            "fuente": resultado.get("fuente", "?"),
            "tiempo_ms": int(resultado.get("tiempo_ms", 0)),
        }

        supabase_rest.insert("reportes", payload)
        print(f"[hook_analisis] Reporte guardado en tabla 'reportes'")

    except Exception as e:
        print(f"[hook_analisis] Error guardando reporte (no critico): {e}")


# ==========================================
# ANALISIS PROFUNDO (V2.1)
# ==========================================
def _aplicar_hook_analisis(_base):
    """
    Envuelve responder_chat para detectar prompts largos y procesarlos
    como analisis profundo. Guarda el reporte en Supabase.
    """
    try:
        from utils import analisis_profundo as AP
    except Exception as e:
        raise Exception(f"No se pudo importar analisis_profundo: {e}")

    _orig_responder_chat = _base.responder_chat

    def responder_chat_hooked(mensaje, BACKEND_ACTIVO):
        try:
            es_analisis = AP.es_analisis_profundo(mensaje)
        except Exception as e:
            print(f"[hook_analisis] Error detectando: {e}")
            es_analisis = False

        if not es_analisis:
            return _orig_responder_chat(mensaje, BACKEND_ACTIVO)

        print(f"[hook_analisis] Detectado analisis profundo ({len(mensaje.split())} palabras)")

        # Contexto del negocio si aplica
        contexto_usuario = None
        try:
            import streamlit as st
            if hasattr(st, "session_state"):
                negocio_sel = st.session_state.get("negocio_seleccionado")
                if negocio_sel:
                    negocio = st.session_state.get("negocios", {}).get(negocio_sel)
                    if negocio:
                        contexto_usuario = AP.extraer_contexto_negocio(negocio)
        except Exception as e:
            print(f"[hook_analisis] Error obteniendo contexto: {e}")

        # Generar reporte
        try:
            resultado = AP.generar_analisis(mensaje, contexto_usuario)
        except Exception as e:
            return (
                f"❌ Error generando analisis: {str(e)[:200]}",
                "Sistema"
            )

        if not resultado.get("exito"):
            return (
                f"❌ No se pudo generar el analisis: {resultado.get('error', 'Error desconocido')}",
                "Sistema"
            )

        # Guardar en tabla reportes
        _guardar_reporte(mensaje, resultado, contexto_usuario)

        # Log del evento
        try:
            from utils.logger import log_evento
            log_evento(
                "analisis_profundo",
                detalle={
                    "tipo": resultado.get("tipo"),
                    "subtipo": resultado.get("subtipo", "general"),
                    "fuente": resultado.get("fuente"),
                    "tiempo_ms": resultado.get("tiempo_ms"),
                    "longitud_prompt": len(mensaje),
                    "origen": "hook_analisis",
                },
            )
        except Exception:
            pass

        reporte = resultado.get("reporte", "")
        fuente = resultado.get("fuente", "?")
        return reporte, f"Analista ({fuente})"

    _base.responder_chat = responder_chat_hooked