# panels/dueno/tab_config.py
# ============================================
# TAB CONFIGURACION - Editor de config_global
# ============================================
# V5.0: Categorias separadas por modelo de negocio
#       - WEB GANCHO (solo web)
#       - PIME / DESDE CERO (crear negocio)
#       - SUCURSALES (expansion)
#       Soporta valores -1 = POR DEFINIR
# V4.0: Agrupacion + descripciones + selectbox modo_app
# ============================================

import streamlit as st
import datetime
from panels.dueno import comun as C


# ==========================================
# METADATOS: descripcion + grupo + tipo por clave
# ==========================================
METADATOS = {
    # ----- SISTEMA -----
    "modo_app": {
        "grupo": "SISTEMA",
        "descripcion": "Cambia TODO el sistema entre prueba y produccion. En produccion se activan limites reales y cobros.",
        "tipo": "modo",
        "opciones": ["prueba", "produccion"],
    },
    "landing_activa": {
        "grupo": "SISTEMA",
        "descripcion": "Activa/desactiva la landing publica con los planes.",
        "tipo": "booleano",
    },

    # ----- WEB GANCHO (Modelo 1 - solo web) -----
    "web_gancho_precio_individual": {
        "grupo": "WEB GANCHO (solo web)",
        "descripcion": "Precio base que paga el cliente por su web individual.",
        "tipo": "entero",
        "sufijo": "USD (pago unico)",
    },
    "web_gancho_administracion_precio": {
        "grupo": "WEB GANCHO (solo web)",
        "descripcion": "Precio mensual de administrar la web del cliente (hosting + ajustes).",
        "tipo": "entero",
        "sufijo": "USD/mes",
        "pendiente_ok": True,
    },
    "web_gancho_crm_precio": {
        "grupo": "WEB GANCHO (solo web)",
        "descripcion": "Precio adicional si el cliente quiere CRM junto con su web individual.",
        "tipo": "entero",
        "sufijo": "USD/mes",
        "pendiente_ok": True,
    },
    "web_gancho_modificaciones_limite": {
        "grupo": "WEB GANCHO (solo web)",
        "descripcion": "Cuantas modificaciones puede hacer el cliente ANTES de que empiece a cobrarse extra.",
        "tipo": "entero",
        "sufijo": "modificaciones",
        "pendiente_ok": True,
    },
    "web_gancho_costo_modificacion_extra": {
        "grupo": "WEB GANCHO (solo web)",
        "descripcion": "Precio por cada modificacion de web despues de pasar el limite.",
        "tipo": "entero",
        "sufijo": "USD",
        "pendiente_ok": True,
    },

    # ----- PIME / DESDE CERO (Modelo 2 - crear negocio) -----
    "negocio_precio_pime": {
        "grupo": "PIME / DESDE CERO (crear negocio)",
        "descripcion": "Precio mensual del plan PIME (web + CRM + panel + todos los modulos).",
        "tipo": "entero",
        "sufijo": "USD/mes",
    },
    "negocio_precio_desde_cero": {
        "grupo": "PIME / DESDE CERO (crear negocio)",
        "descripcion": "Precio mensual del plan DESDE CERO (onboarding guiado para emprendedores).",
        "tipo": "entero",
        "sufijo": "USD/mes",
    },
    "negocio_precio_enterprise": {
        "grupo": "PIME / DESDE CERO (crear negocio)",
        "descripcion": "Precio mensual del plan ENTERPRISE (empresas grandes, proximamente).",
        "tipo": "entero",
        "sufijo": "USD/mes",
    },
    "negocio_modificaciones_gratis_prueba": {
        "grupo": "PIME / DESDE CERO (crear negocio)",
        "descripcion": "Cuantas modificaciones de web regala el sistema en MODO PRUEBA.",
        "tipo": "entero",
        "sufijo": "modificaciones",
    },
    "negocio_modificaciones_gratis_prod": {
        "grupo": "PIME / DESDE CERO (crear negocio)",
        "descripcion": "Cuantas modificaciones de web regala el sistema en MODO PRODUCCION.",
        "tipo": "entero",
        "sufijo": "modificaciones",
    },
    "negocio_costo_modificacion_extra": {
        "grupo": "PIME / DESDE CERO (crear negocio)",
        "descripcion": "Precio por cada modificacion despues de agotar las gratis.",
        "tipo": "entero",
        "sufijo": "USD",
    },

    # ----- SUCURSALES (Modelo 3 - expansion) -----
    "sucursal_descuento_porcentaje": {
        "grupo": "SUCURSALES (expansion)",
        "descripcion": "Porcentaje del plan que paga una sucursal nueva. Ej: 50 = paga 50% del plan original.",
        "tipo": "entero",
        "sufijo": "%",
    },
}

# Orden de grupos en la UI
ORDEN_GRUPOS = [
    "SISTEMA",
    "WEB GANCHO (solo web)",
    "PIME / DESDE CERO (crear negocio)",
    "SUCURSALES (expansion)",
]


# ==========================================
# HELPERS
# ==========================================
def _registrar_auditoria(sb, clave, valor_anterior, valor_nuevo, quien, motivo=""):
    try:
        payload = {
            "clave": clave,
            "valor_anterior": valor_anterior,
            "valor_nuevo": valor_nuevo,
            "quien": quien,
            "motivo": motivo,
            "created_at": datetime.datetime.now().isoformat(),
        }
        sb.insert("config_auditoria", payload)
    except Exception as e:
        print(f"[tab_config] Error registrando auditoria: {e}")


def _aplicar_cambio_en_vivo():
    try:
        from utils.config_global import invalidar_cache
        invalidar_cache()
    except Exception as e:
        print(f"[tab_config] Error invalidando cache: {e}")

    try:
        from config_app import recargar_config
        recargar_config()
    except Exception as e:
        print(f"[tab_config] Error recargando config_app: {e}")


def _guardar(sb, clave, valor_anterior, valor_nuevo):
    try:
        from utils.supabase_rest import supabase_rest
        supabase_rest.update(
            "config_global",
            {"valor": valor_nuevo, "updated_at": datetime.datetime.now().isoformat()},
            "clave",
            clave,
        )
        _registrar_auditoria(
            sb, clave,
            valor_anterior=valor_anterior,
            valor_nuevo=valor_nuevo,
            quien="antonio",
            motivo="Cambio desde panel dueno",
        )
        _aplicar_cambio_en_vivo()
        return True, "Guardado y aplicado"
    except Exception as e:
        return False, str(e)


def _es_pendiente(valor):
    """Detecta si un valor esta como POR DEFINIR (centinela -1)."""
    try:
        return int(valor) == -1
    except Exception:
        return False


# ==========================================
# RENDER PRINCIPAL
# ==========================================
def renderizar(sb):
    st.markdown(f"### {C.E_ENGANCHE} Configuracion global")
    st.caption(f"{C.E_LIBRO} Cada cambio se aplica en vivo y queda registrado en Auditoria.")

    try:
        rows = sb.table("config_global").select("*").execute().data or []
    except Exception as e:
        st.error(f"Tabla 'config_global' no lista: {e}")
        return

    if not rows:
        st.info("Sin configuraciones. Ejecuta el SQL inicial.")
        return

    config_map = {r.get("clave"): r.get("valor") for r in rows if r.get("clave")}

    # Contar pendientes
    pendientes = sum(1 for k, v in config_map.items()
                     if METADATOS.get(k, {}).get("pendiente_ok") and _es_pendiente(v))

    if pendientes > 0:
        st.warning(
            f"{C.E_AVISO} **{pendientes} valor(es) POR DEFINIR** "
            f"(marcados con -1). Editarlos cuando tengas los numeros finales."
        )

    # Agrupar
    grupos = {}
    huerfanos = []

    for clave, valor in config_map.items():
        meta = METADATOS.get(clave)
        if meta:
            grupos.setdefault(meta["grupo"], []).append((clave, valor, meta))
        else:
            huerfanos.append((clave, valor, {}))

    # Renderizar
    for grupo_nombre in ORDEN_GRUPOS:
        if grupo_nombre not in grupos:
            continue

        st.markdown(f"#### {C.E_PIN} {grupo_nombre}")
        st.divider()

        for clave, valor, meta in grupos[grupo_nombre]:
            _renderizar_clave(sb, clave, valor, meta)

        st.markdown("")

    if huerfanos:
        with st.expander(f"{C.E_AVISO} Configuraciones sin categoria ({len(huerfanos)})", expanded=False):
            for clave, valor, _ in huerfanos:
                _renderizar_clave(sb, clave, valor, {})

    st.divider()
    st.caption(f"{C.E_OK} Los cambios se aplican en vivo. Algunos requieren reiniciar sesion (F5).")


def _renderizar_clave(sb, clave, valor, meta):
    tipo = meta.get("tipo", "auto")
    descripcion = meta.get("descripcion", "")
    sufijo = meta.get("sufijo", "")
    opciones = meta.get("opciones", [])
    pendiente_ok = meta.get("pendiente_ok", False)
    es_pendiente = _es_pendiente(valor)

    if tipo == "auto":
        if isinstance(valor, bool):
            tipo = "booleano"
        elif isinstance(valor, int):
            tipo = "entero"
        elif isinstance(valor, float):
            tipo = "decimal"
        else:
            tipo = "texto"

    col_label, col_editor, col_btn = st.columns([3, 3, 1])

    with col_label:
        # Marcar visualmente si esta pendiente
        if es_pendiente and pendiente_ok:
            st.markdown(f"**`{clave}`** {C.E_AVISO} *POR DEFINIR*")
        else:
            st.markdown(f"**`{clave}`**")
        if descripcion:
            st.caption(descripcion)

    nuevo = None
    with col_editor:
        if tipo == "modo":
            try:
                idx = opciones.index(valor) if valor in opciones else 0
            except Exception:
                idx = 0
            nuevo = st.selectbox(
                label=f"valor_{clave}",
                options=opciones,
                index=idx,
                key=f"cfg_{clave}",
                label_visibility="collapsed",
            )
        elif tipo == "booleano":
            nuevo = st.checkbox(
                label=f"valor_{clave}",
                value=bool(valor),
                key=f"cfg_{clave}",
                label_visibility="collapsed",
            )
        elif tipo == "entero":
            val_actual = int(valor) if valor is not None else 0
            nuevo = int(st.number_input(
                label=f"valor_{clave}",
                value=val_actual,
                step=1,
                key=f"cfg_{clave}",
                label_visibility="collapsed",
            ))
        elif tipo == "decimal":
            nuevo = float(st.number_input(
                label=f"valor_{clave}",
                value=float(valor) if valor is not None else 0.0,
                key=f"cfg_{clave}",
                label_visibility="collapsed",
            ))
        else:
            nuevo = st.text_input(
                label=f"valor_{clave}",
                value=str(valor) if valor is not None else "",
                key=f"cfg_{clave}",
                label_visibility="collapsed",
            )

        if sufijo:
            if es_pendiente and pendiente_ok:
                st.caption(f"Unidad: {sufijo} | Escribi el valor real para reemplazar -1")
            else:
                st.caption(f"Unidad: {sufijo}")

    cambio = nuevo != valor

    with col_btn:
        st.write("")
        st.write("")
        if st.button(
            "Guardar",
            key=f"save_{clave}",
            disabled=not cambio,
            use_container_width=True,
        ):
            ok, msg = _guardar(sb, clave, valor, nuevo)
            if ok:
                st.success(f"{C.E_OK} {msg}: {clave} = {nuevo}")
                st.rerun()
            else:
                st.error(f"{C.E_AVISO} {msg}")

    if cambio:
        st.caption(f"{C.E_AVISO} Cambio pendiente: `{valor}` -> `{nuevo}`")

    st.markdown("")