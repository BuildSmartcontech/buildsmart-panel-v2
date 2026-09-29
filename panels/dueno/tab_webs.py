# panels/dueno/tab_webs.py
# ============================================
# TAB WEBS - Lista de webs publicadas + republicar
# ============================================

import streamlit as st
from panels.dueno import comun as C


def renderizar(sb, inicio, fin):
    st.markdown(f"### {C.E_GLOBO} Webs publicadas")

    try:
        data_neg = sb.table("negocios").select("*").execute().data or []
    except Exception as e:
        st.error(f"Error: {e}")
        return

    negocios_todos = [C._plano(n) for n in data_neg]
    negocios = [n for n in negocios_todos if C._dentro_de_rango(n, "created_at", inicio, fin)]

    webs = []
    for n in negocios:
        sitio = n.get("sitio_web") or {}
        url = n.get("web_url") or sitio.get("url_publica")
        if url:
            webs.append({
                "negocio": n.get("nombre", "Sin nombre"),
                "negocio_id": n.get("id", "?"),
                "web_id": sitio.get("archivo_generado"),
                "usuario": str(n.get("usuario_id", "?"))[:12],
                "url": url,
                "fecha": n.get("updated_at") or n.get("created_at", "?"),
            })

    st.metric("Total webs en rango", len(webs))
    st.divider()

    if not webs:
        st.info(f"{C.E_AVISO} No hay webs publicadas en el rango seleccionado.")
        return

    for w in webs:
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 4, 2])
            c1.markdown(f"**{C.E_CORONA} {w['negocio']}**")
            c2.markdown(f"[{w['url']}]({w['url']})")
            c3.caption(f"{w['usuario']} - {str(w['fecha'])[:10]}")

            if w["web_id"]:
                col_btn, _ = st.columns([1, 3])
                with col_btn:
                    if st.button(f"{C.E_REFRESH} Republicar", key=f"repub_tab_{w['negocio_id']}", use_container_width=True):
                        with st.spinner("Republicando..."):
                            exito, mensaje, url_nueva = C._republicar_web(w["negocio_id"], w["web_id"])
                        if exito:
                            st.success(f"{C.E_OK} {mensaje}")
                            if url_nueva:
                                st.markdown(f"{C.E_GLOBO} [{url_nueva}]({url_nueva})")
                            C._registrar_republicacion(sb, w["negocio_id"], w["web_id"], url_nueva, True, mensaje)
                        else:
                            st.error(f"{C.E_AVISO} {mensaje}")
                            C._registrar_republicacion(sb, w["negocio_id"], w["web_id"], "", False, mensaje)