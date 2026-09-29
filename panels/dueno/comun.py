# panels/dueno/comun.py
# ============================================
# HELPERS COMPARTIDOS - Panel Dueno SAMU IA
# ============================================
# V1.2: Fix real de timezone usando fromisoformat
# V1.1: Intento fallido
# V1.0: Version inicial
# ============================================

import streamlit as st
import datetime
import json
import uuid as _uuid_lib


# ==========================================
# EMOJIS
# ==========================================
E_CORONA    = "\U0001F451"
E_PANEL     = "\U0001F4CA"
E_CLIENTES  = "\U0001F465"
E_DINERO    = "\U0001F4B0"
E_GLOBO     = "\U0001F310"
E_LIBRO     = "\U0001F4DC"
E_ENGANCHE  = "\u2699\uFE0F"
E_OK        = "\u2705"
E_AVISO     = "\u26A0\uFE0F"
E_RAYO      = "\u26A1"
E_TARJETA   = "\U0001F4B3"
E_TUBO      = "\U0001F9EA"
E_PIN       = "\U0001F4CC"
E_RELOJ     = "\U0001F550"
E_CALENDAR  = "\U0001F4C5"
E_LUPA      = "\U0001F50D"
E_GRAFICO   = "\U0001F4C8"
E_FLECHA    = "\u2B05\uFE0F"
E_OJO       = "\U0001F441\uFE0F"
E_USUARIO   = "\U0001F464"
E_HISTORIAL = "\U0001F4DC"
E_PROHIBIDO = "\U0001F6AB"
E_CANDADO   = "\U0001F512"
E_ABIERTO   = "\U0001F513"
E_LLAVE     = "\U0001F511"
E_REFRESH   = "\U0001F504"
E_SALUD     = "\U0001FA7A"
E_VERDE     = "\U0001F7E2"
E_ROJO      = "\U0001F534"
E_AMARILLO  = "\U0001F7E1"


# ==========================================
# SUPABASE
# ==========================================
def _get_supabase():
    try:
        from utils.supabase_rest import supabase_rest
        if supabase_rest.disponible:
            return supabase_rest
    except Exception as e:
        print(f"[panel_dueno] Error supabase_rest: {e}")
    try:
        from utils.supabase_client import supabase as sb
        if sb is not None and hasattr(sb, "table"):
            return sb
    except Exception:
        pass
    return None


def _plano(n):
    if not n:
        return {}
    base = dict(n)
    data = n.get("data")
    if isinstance(data, dict):
        for k, v in data.items():
            if k not in base or base[k] in (None, "", {}):
                base[k] = v
    return base


def _uuid_valido(val):
    if not val:
        return False
    try:
        _uuid_lib.UUID(str(val))
        return True
    except Exception:
        return False


# ==========================================
# REPUBLICAR WEB
# ==========================================
def _republicar_web(negocio_id, web_id):
    try:
        from utils.web_publisher import publicar_web
    except ImportError:
        try:
            from web_publisher import publicar_web
        except ImportError:
            return False, "Modulo web_publisher no disponible", ""

    try:
        usuario_id = f"usuario_{negocio_id}"
        print(f"[REPUBLICAR] {usuario_id} / {web_id}")
        resultado = publicar_web(usuario_id, web_id)

        if resultado.get("exito"):
            url = resultado.get("url_publica", "")
            tipo = resultado.get("tipo", "desconocido")
            cacheado = resultado.get("cacheado", False)
            return True, f"Republicado ({tipo}{' - cacheado' if cacheado else ''})", url
        else:
            error = resultado.get("error", "Error desconocido")
            return False, f"Error: {error}", ""
    except Exception as e:
        return False, f"Excepcion: {e}", ""


def _registrar_republicacion(sb, negocio_id, web_id, url_nueva, exito, mensaje):
    try:
        from utils.logger import log_evento
        log_evento(
            "republicar_web",
            negocio_id=negocio_id if _uuid_valido(negocio_id) else None,
            detalle={
                "web_id": web_id,
                "url_nueva": url_nueva,
                "exito": exito,
                "mensaje": mensaje[:200],
                "origen": "panel_dueno",
            }
        )
    except Exception as e:
        print(f"[panel_dueno] Error registrando republicacion: {e}")


# ==========================================
# ESTADO DE CUENTAS
# ==========================================
def _obtener_estados_usuarios(sb):
    try:
        rows = sb.table("usuarios_sistema").select("*").execute().data or []
        return {r.get("usuario_id"): r for r in rows if r.get("usuario_id")}
    except Exception as e:
        print(f"[panel_dueno] Error leyendo usuarios_sistema: {e}")
        return {}


def _estado_de(uid, estados):
    info = estados.get(uid, {})
    return info.get("estado") or "activo"


def _cambiar_estado_usuario(sb, uid, nuevo_estado, motivo, quien):
    try:
        existente = sb.table("usuarios_sistema").select("*").eq("usuario_id", uid).execute().data or []
        payload = {
            "usuario_id": uid,
            "estado": nuevo_estado,
            "motivo": motivo,
            "fecha_accion": datetime.datetime.now().isoformat(),
            "quien_accion": quien,
            "updated_at": datetime.datetime.now().isoformat(),
        }
        if existente:
            sb.update("usuarios_sistema", payload, "usuario_id", uid)
        else:
            sb.insert("usuarios_sistema", payload)
        return True, f"Estado cambiado a {nuevo_estado}"
    except Exception as e:
        return False, f"Error: {e}"


# ==========================================
# FILTROS DE FECHA
# ==========================================
def _parse_fecha_segura(val):
    """
    Convierte un timestamp ISO (con timezone) a datetime LOCAL naive.
    Supabase devuelve UTC con +00:00. Lo convertimos a hora local
    del sistema para comparar correctamente con datetime.now().
    """
    if not val:
        return None
    try:
        # Si ya es datetime, usarlo directo
        if isinstance(val, datetime.datetime):
            dt = val
        else:
            s = str(val).strip()
            # Normalizar Z a +00:00
            if s.endswith("Z"):
                s = s[:-1] + "+00:00"
            # Python 3.11+ parsea ISO 8601 completo con timezone
            dt = datetime.datetime.fromisoformat(s)

        # Si tiene timezone (aware), convertir a local naive
        if dt.tzinfo is not None:
            dt = dt.astimezone().replace(tzinfo=None)

        return dt
    except Exception:
        return None


def _dentro_de_rango(item, campo, inicio, fin):
    if inicio is None and fin is None:
        return True
    f = _parse_fecha_segura(item.get(campo))
    if f is None:
        return False
    if inicio and f < inicio:
        return False
    if fin and f > fin:
        return False
    return True


def _selector_rango():
    opciones = [
        "Ultimos 7 dias",
        "Ultimos 30 dias",
        "Este mes",
        "Hoy",
        "Todo el historial",
        "Personalizado",
    ]
    col1, col2 = st.columns([2, 3])
    with col1:
        rango = st.selectbox("Rango de fechas", opciones, index=1, key="filtro_fecha_rango")

    ahora = datetime.datetime.now()
    hoy = ahora.date()

    if rango == "Hoy":
        inicio = datetime.datetime.combine(hoy, datetime.time.min)
        fin = ahora
        etiqueta = f"Hoy ({hoy.strftime('%d/%m/%Y')})"
    elif rango == "Ultimos 7 dias":
        inicio = datetime.datetime.combine(hoy - datetime.timedelta(days=6), datetime.time.min)
        fin = ahora
        etiqueta = f"{inicio.strftime('%d/%m/%Y')} a {fin.strftime('%d/%m/%Y')}"
    elif rango == "Ultimos 30 dias":
        inicio = datetime.datetime.combine(hoy - datetime.timedelta(days=29), datetime.time.min)
        fin = ahora
        etiqueta = f"{inicio.strftime('%d/%m/%Y')} a {fin.strftime('%d/%m/%Y')}"
    elif rango == "Este mes":
        inicio = datetime.datetime(hoy.year, hoy.month, 1)
        fin = ahora
        etiqueta = f"{inicio.strftime('%d/%m/%Y')} a {fin.strftime('%d/%m/%Y')}"
    elif rango == "Personalizado":
        with col2:
            fechas = st.date_input(
                "Selecciona el rango",
                value=(hoy - datetime.timedelta(days=29), hoy),
                key="filtro_fecha_custom",
            )
        if isinstance(fechas, tuple) and len(fechas) == 2:
            inicio = datetime.datetime.combine(fechas[0], datetime.time.min)
            fin = datetime.datetime.combine(fechas[1], datetime.time.max)
            etiqueta = f"{fechas[0].strftime('%d/%m/%Y')} a {fechas[1].strftime('%d/%m/%Y')}"
        else:
            inicio = datetime.datetime.combine(hoy - datetime.timedelta(days=29), datetime.time.min)
            fin = ahora
            etiqueta = "Rango invalido - usando ultimos 30 dias"
    else:
        inicio = None
        fin = None
        etiqueta = "Todo el historial"

    return inicio, fin, etiqueta


# ==========================================
# COMPONENTES VISUALES
# ==========================================
def _kpi(col, label, valor):
    with col:
        st.markdown(f"""
        <div style="background:#1e293b;padding:16px;border-radius:10px;text-align:center;border:1px solid #334155;">
            <div style="font-size:28px;font-weight:700;color:#f1f5f9;">{valor}</div>
            <div style="font-size:12px;color:#94a3b8;margin-top:4px;">{label}</div>
        </div>
        """, unsafe_allow_html=True)


def _renderizar_negocio_con_acciones(sb, n):
    negocio_id = n.get("id", "?")
    web_id = (n.get("sitio_web") or {}).get("archivo_generado")
    web_url = n.get("web_url") or (n.get("sitio_web") or {}).get("url_publica")

    with st.container(border=True):
        col_a, col_b = st.columns([3, 2])
        with col_a:
            st.markdown(f"**{E_CORONA} {n.get('nombre', 'Sin nombre')}**")
            sector = n.get("sector") or n.get("sector_contexto") or "Sin sector"
            st.caption(f"Sector: {sector}")
            if n.get("descripcion"):
                st.text(str(n.get("descripcion"))[:100])
        with col_b:
            if web_url:
                st.markdown(f"{E_GLOBO} [{web_url}]({web_url})")
            else:
                st.caption("Sin web publicada")
            creado = str(n.get("created_at", ""))[:19].replace("T", " ")
            if creado:
                st.caption(f"Creado: {creado}")

        if web_id:
            col_btn1, col_btn2 = st.columns([1, 3])
            with col_btn1:
                if st.button(f"{E_REFRESH} Republicar", key=f"repub_{negocio_id}", use_container_width=True):
                    with st.spinner("Republicando en Netlify..."):
                        exito, mensaje, url_nueva = _republicar_web(negocio_id, web_id)
                    if exito:
                        st.success(f"{E_OK} {mensaje}")
                        if url_nueva:
                            st.markdown(f"{E_GLOBO} Nueva URL: [{url_nueva}]({url_nueva})")
                        _registrar_republicacion(sb, negocio_id, web_id, url_nueva, True, mensaje)
                    else:
                        st.error(f"{E_AVISO} {mensaje}")
                        _registrar_republicacion(sb, negocio_id, web_id, "", False, mensaje)


def _renderizar_evento_linea(e):
    fecha = str(e.get("created_at", ""))[:19].replace("T", " ")
    tipo = e.get("tipo", "?")
    detalle = e.get("detalle") or {}

    if tipo == "login":
        st.text(f"[{fecha}] {E_USUARIO} Inicio de sesion")
    elif tipo == "crear_negocio":
        nombre = detalle.get("nombre", "?")
        st.text(f"[{fecha}] {E_CORONA} Creo negocio: {nombre}")
    elif tipo == "generar_web":
        url = detalle.get("url_publica", "")
        st.text(f"[{fecha}] {E_GLOBO} Genero web: {url[:60]}")
    elif tipo == "modificar_web":
        instruc = detalle.get("instruccion", "")[:60]
        st.text(f"[{fecha}] {E_ENGANCHE} Modifico web: {instruc}")
    elif tipo == "republicar_web":
        exito = detalle.get("exito", False)
        icono = E_OK if exito else E_AVISO
        st.text(f"[{fecha}] {E_REFRESH} {icono} Republico web: {detalle.get('mensaje', '')[:50]}")
    elif tipo == "crear_tarea":
        titulo = detalle.get("titulo", "?")
        st.text(f"[{fecha}] {E_PIN} Creo tarea: {titulo}")
    elif tipo == "mover_tarea":
        titulo = detalle.get("titulo", "?")[:40]
        estado_t = detalle.get("nuevo_estado", "?")
        st.text(f"[{fecha}] Tarea '{titulo}' -> {estado_t}")
    elif tipo == "error":
        modulo = detalle.get("modulo", "?")
        st.text(f"[{fecha}] {E_AVISO} Error en {modulo}")
    else:
        st.text(f"[{fecha}] {tipo}")