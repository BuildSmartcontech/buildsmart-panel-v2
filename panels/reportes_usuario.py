# panels/reportes_usuario.py
# ============================================
# REPORTES DEL USUARIO - SAMU IA
# ============================================
# V1.1: Fix filtro - solo muestra reportes tipo='usuario' (no del dueno)
# V1.0: Version inicial
# ============================================

import streamlit as st
from config_app import obtener_usuario_actual


# ==========================================
# EMOJIS
# ==========================================
E_REPORTE   = "\U0001F4C4"
E_DOC       = "\U0001F4C4"
E_CALENDAR  = "\U0001F4C5"
E_LUPA      = "\U0001F50D"
E_OK        = "\u2705"
E_AVISO     = "\u26A0\uFE0F"
E_RAYO      = "\u26A1"
E_LOGO      = "\U0001F4CA"
E_DINERO    = "\U0001F4B0"
E_GLOBO     = "\U0001F310"
E_MANO      = "\U0001F44B"
E_ENGANCHE  = "\u2699\uFE0F"


NOMBRES_SUBTIPO = {
    "marketing": f"{E_RAYO} Marketing",
    "finanzas": f"{E_DINERO} Finanzas",
    "competencia": f"{E_LOGO} Competencia",
    "web": f"{E_GLOBO} Web",
    "operacion": f"{E_ENGANCHE} Operacion",
    "general": f"{E_DOC} General",
}


def _get_supabase():
    try:
        from utils.supabase_rest import supabase_rest
        if supabase_rest.disponible:
            return supabase_rest
    except Exception:
        pass
    return None


def _cargar_reportes():
    """Carga los reportes del usuario actual (solo tipo='usuario')."""
    sb = _get_supabase()
    if sb is None:
        return []

    try:
        uid = obtener_usuario_actual()
        if not uid:
            return []

        # Filtro doble: por usuario_id Y por tipo='usuario'
        r = (sb.table("reportes")
             .select("*")
             .eq("usuario_id", uid)
             .eq("tipo", "usuario")
             .execute())

        if r.error:
            print(f"[reportes_usuario] Error: {r.error}")
            return []

        reportes = r.data or []
        reportes.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return reportes
    except Exception as e:
        print(f"[reportes_usuario] Error cargando: {e}")
        return []


def _fmt_fecha(iso_str):
    """Formatea timestamp ISO a fecha local legible."""
    if not iso_str:
        return "?"
    try:
        from datetime import datetime
        s = str(iso_str).replace("Z", "")
        if "+" in s and "T" in s:
            base = s.rsplit("+", 1)[0]
            if "." in base:
                base = base.split(".")[0]
            dt = datetime.fromisoformat(base)
        else:
            if "." in s:
                s = s.split(".")[0]
            dt = datetime.fromisoformat(s)
        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return str(iso_str)[:19].replace("T", " ")


def renderizar():
    """Renderiza la seccion de 'Mis Reportes' en el panel usuario."""

    reportes = _cargar_reportes()

    st.divider()
    st.subheader(f"{E_REPORTE} Mis Reportes")

    if not reportes:
        st.info(
            f"{E_AVISO} Aun no has generado ningun reporte.\n\n"
            f"**¿Como generar uno?**\n"
            f"Escribi en el chat de abajo algo como:\n"
            f"- *\"Analiza mi marketing\"*\n"
            f"- *\"Analiza mis finanzas\"*\n"
            f"- *\"Analiza mi competencia\"*\n"
            f"- *\"Analiza mi web\"*\n\n"
            f"La IA va a generar un analisis personalizado con los datos de tu negocio."
        )
        return

    total = len(reportes)
    subtipos = {}
    for r in reportes:
        st_key = r.get("subtipo", "general")
        subtipos[st_key] = subtipos.get(st_key, 0) + 1

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total", total)
    with c2:
        st.metric("Marketing", subtipos.get("marketing", 0))
    with c3:
        st.metric("Finanzas", subtipos.get("finanzas", 0))
    with c4:
        st.metric("Otros", total - subtipos.get("marketing", 0) - subtipos.get("finanzas", 0))

    st.caption(f"{E_LUPA} Mostrando {total} reporte(s)")

    filtro = st.selectbox(
        "Filtrar por tipo",
        ["(todos)"] + list(NOMBRES_SUBTIPO.keys()),
        format_func=lambda x: "(todos)" if x == "(todos)" else NOMBRES_SUBTIPO.get(x, x),
        key="reportes_usuario_filtro",
    )

    for r in reportes:
        subtipo = r.get("subtipo", "general")
        if filtro != "(todos)" and subtipo != filtro:
            continue

        titulo_subtipo = NOMBRES_SUBTIPO.get(subtipo, subtipo.capitalize())
        consulta = r.get("consulta", "")[:80]
        fecha = _fmt_fecha(r.get("created_at"))
        fuente = r.get("fuente", "?")
        tiempo_s = r.get("tiempo_ms", 0) / 1000

        titulo = f"{E_CALENDAR} [{fecha}] {titulo_subtipo} - {consulta}..."

        with st.expander(titulo):
            col_info, col_acciones = st.columns([3, 1])

            with col_info:
                st.caption(f"**Consulta completa:** {r.get('consulta', '')}")
                st.caption(f"{E_RAYO} Generado con {fuente} en {tiempo_s:.1f}s")

            with col_acciones:
                contenido_md = r.get("reporte", "")
                if contenido_md:
                    fecha_archivo = fecha.replace("/", "-").replace(":", "").replace(" ", "_")
                    nombre_archivo = f"reporte_{subtipo}_{fecha_archivo}.md"

                    st.download_button(
                        f"{E_DOC} Descargar",
                        data=contenido_md,
                        file_name=nombre_archivo,
                        mime="text/markdown",
                        key=f"descargar_reporte_{r.get('id', '?')}",
                        use_container_width=True,
                    )

            st.divider()
            st.markdown(r.get("reporte", "_(vacio)_"))


if __name__ == "__main__":
    print("=" * 70)
    print("TEST REPORTES USUARIO")
    print("=" * 70)
    print(f"Subtipos soportados: {', '.join(NOMBRES_SUBTIPO.keys())}")
    print("Filtro: solo tipo='usuario' (excluye reportes del dueno)")
    print("=" * 70)