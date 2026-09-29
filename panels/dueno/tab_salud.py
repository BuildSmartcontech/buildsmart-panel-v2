# panels/dueno/tab_salud.py
# ============================================
# TAB SALUD - Semaforo de APIs y servicios
# ============================================

import streamlit as st
from panels.dueno import comun as C


def renderizar(sb):
    st.markdown(f"### {C.E_SALUD} Salud del sistema")
    st.caption("Estado de las APIs y servicios. Timeout 8s por check.")

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        if st.button(f"{C.E_REFRESH} Verificar todo", use_container_width=True, type="primary"):
            st.session_state["_salud_cache"] = None
            st.rerun()

    if st.session_state.get("_salud_cache") is None:
        try:
            from utils import salud
            with st.spinner("Verificando APIs..."):
                st.session_state["_salud_cache"] = salud.check_todos()
        except Exception as e:
            st.error(f"Error cargando modulo de salud: {e}")
            return

    resultados = st.session_state.get("_salud_cache", {})

    if not resultados:
        st.info("Presiona 'Verificar todo' para empezar.")
        return

    total = len(resultados)
    ok = sum(1 for r in resultados.values() if r.get("ok"))
    sin_config = sum(1 for r in resultados.values() if not r.get("configurado"))
    caidos = total - ok - sin_config

    c1, c2, c3, c4 = st.columns(4)
    C._kpi(c1, f"{C.E_VERDE} Online", ok)
    C._kpi(c2, f"{C.E_AMARILLO} Sin config", sin_config)
    C._kpi(c3, f"{C.E_ROJO} Caidos", caidos)
    C._kpi(c4, "Total", total)

    st.divider()

    nombres_bonitos = {
        "supabase": "Supabase (Base de datos)",
        "netlify": "Netlify (Publicacion web)",
        "groq": "Groq (IA primaria)",
        "openrouter": "OpenRouter (IA respaldo)",
        "gemini": "Gemini (IA respaldo)",
        "backend": "Backend local (FastAPI)",
    }

    for nombre, r in resultados.items():
        titulo = nombres_bonitos.get(nombre, nombre)

        if not r.get("configurado"):
            icono = C.E_AMARILLO
            label = "SIN CONFIGURAR"
        elif r.get("ok"):
            icono = C.E_VERDE
            label = "ONLINE"
        else:
            icono = C.E_ROJO
            label = "CAIDO"

        with st.container(border=True):
            col_a, col_b, col_c = st.columns([3, 2, 2])
            with col_a:
                st.markdown(f"{icono} **{titulo}**")
                st.caption(r.get("msg", ""))
            with col_b:
                st.metric("Estado", label)
            with col_c:
                ms = r.get("ms", 0)
                if ms > 0:
                    st.metric("Latencia", f"{ms} ms")
                else:
                    st.metric("Latencia", "-")

    st.divider()
    st.caption("Los resultados se cachean. Presiona 'Verificar todo' para re-chequear.")