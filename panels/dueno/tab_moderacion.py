# panels/dueno/tab_moderacion.py
# ============================================
# TAB MODERACION - Revisar contenido IA
# ============================================
# Permite al dueno:
# - Ver personalidad custom de cada negocio
# - Ver descripciones
# - Ver tareas creadas
# - Editar o limpiar contenido inapropiado
# - Registrar cada accion en eventos_app
# ============================================

import streamlit as st
import datetime
from panels.dueno import comun as C


def _editar_negocio(sb, negocio_id, nuevo_data):
    """Actualiza el campo data JSON de un negocio."""
    try:
        sb.update("negocios", {"data": nuevo_data}, "id", negocio_id)
        return True, "Guardado"
    except Exception as e:
        return False, f"Error: {e}"


def _registrar_moderacion(negocio_id, usuario_id, accion, campo, detalle_extra=None):
    """Registra accion de moderacion en eventos_app."""
    try:
        from utils.logger import log_evento
        detalle = {
            "accion": accion,
            "campo": campo,
            "origen": "panel_dueno",
        }
        if detalle_extra:
            detalle.update(detalle_extra)

        log_evento(
            "moderar_contenido",
            usuario_id=usuario_id,
            negocio_id=negocio_id if C._uuid_valido(negocio_id) else None,
            detalle=detalle,
        )
    except Exception as e:
        print(f"[moderacion] Error registrando: {e}")


def renderizar(sb, inicio, fin):
    st.markdown(f"### {C.E_ENGANCHE} Moderacion de contenido")
    st.caption("Revisar, editar o limpiar contenido generado por IA.")

    # Cargar negocios
    try:
        data_neg = sb.table("negocios").select("*").execute().data or []
    except Exception as e:
        st.error(f"Error leyendo negocios: {e}")
        return

    if not data_neg:
        st.info(f"{C.E_AVISO} No hay negocios registrados.")
        return

    negocios = [C._plano(n) for n in data_neg]

    # ==========================================
    # KPIs
    # ==========================================
    total = len(negocios)
    con_personalidad = sum(1 for n in negocios if (n.get("custom_personality") or "").strip())
    con_tareas = sum(1 for n in negocios if n.get("tareas"))
    total_tareas = sum(len(n.get("tareas") or []) for n in negocios)
    con_descripcion = sum(1 for n in negocios if (n.get("descripcion") or "").strip())

    c1, c2, c3, c4, c5 = st.columns(5)
    C._kpi(c1, f"{C.E_CORONA} Negocios", total)
    C._kpi(c2, f"{C.E_TUBO} Con personalidad", con_personalidad)
    C._kpi(c3, f"{C.E_PIN} Con tareas", con_tareas)
    C._kpi(c4, f"{C.E_LIBRO} Total tareas", total_tareas)
    C._kpi(c5, f"{C.E_LIBRO} Con descripcion", con_descripcion)

    st.divider()

    # ==========================================
    # Filtros
    # ==========================================
    col_f1, col_f2 = st.columns([2, 2])
    with col_f1:
        busqueda = st.text_input("Buscar por nombre, usuario o texto", "", key="mod_busqueda")
    with col_f2:
        filtro_tipo = st.selectbox(
            "Filtrar por",
            ["(todos)", "Con personalidad custom", "Con tareas", "Con descripcion"],
            key="mod_filtro_tipo",
        )

    # Aplicar filtros
    filtrados = []
    for n in negocios:
        if filtro_tipo == "Con personalidad custom" and not (n.get("custom_personality") or "").strip():
            continue
        if filtro_tipo == "Con tareas" and not n.get("tareas"):
            continue
        if filtro_tipo == "Con descripcion" and not (n.get("descripcion") or "").strip():
            continue

        if busqueda:
            texto = (
                str(n.get("nombre", ""))
                + str(n.get("usuario_id", ""))
                + str(n.get("descripcion", ""))
                + str(n.get("custom_personality", ""))
            ).lower()
            if busqueda.lower() not in texto:
                continue
        filtrados.append(n)

    st.caption(f"Mostrando {len(filtrados)} de {total} negocios")
    st.divider()

    if not filtrados:
        st.info(f"{C.E_AVISO} Ningun negocio coincide con los filtros.")
        return

    # ==========================================
    # Lista de negocios
    # ==========================================
    for n in filtrados:
        negocio_id = n.get("id", "?")
        usuario_id = n.get("usuario_id", "?")
        nombre = n.get("nombre", "Sin nombre")

        with st.expander(f"{C.E_CORONA} {nombre} - `{str(usuario_id)[:12]}...`"):
            # ======================================
            # Personalidad custom
            # ======================================
            personalidad = (n.get("custom_personality") or "").strip()

            st.markdown(f"#### {C.E_TUBO} Personalidad custom")
            if personalidad:
                st.warning(f"{C.E_AVISO} **Personalidad custom activa** ({len(personalidad)} caracteres)")
                with st.container(border=True):
                    st.code(personalidad[:2000] + ("..." if len(personalidad) > 2000 else ""), language="text")

                col_edit, col_clear, _ = st.columns([1, 1, 2])

                with col_edit:
                    if st.button(f"{C.E_ENGANCHE} Editar", key=f"mod_edit_pers_{negocio_id}", use_container_width=True):
                        st.session_state[f"modal_edit_pers_{negocio_id}"] = True

                with col_clear:
                    if st.button(f"{C.E_PROHIBIDO} Limpiar", key=f"mod_clear_pers_{negocio_id}", use_container_width=True):
                        st.session_state[f"modal_clear_pers_{negocio_id}"] = True

                # Modal Editar
                if st.session_state.get(f"modal_edit_pers_{negocio_id}", False):
                    with st.form(f"form_edit_pers_{negocio_id}"):
                        st.markdown("**Editar personalidad**")
                        nuevo_texto = st.text_area(
                            "Nuevo contenido",
                            value=personalidad,
                            height=250,
                            key=f"edit_pers_text_{negocio_id}",
                        )
                        motivo = st.text_input(
                            "Motivo de la edicion",
                            placeholder="Ej: Lenguaje inapropiado",
                            key=f"edit_pers_motivo_{negocio_id}",
                        )

                        col_ok, col_cancel = st.columns(2)
                        with col_ok:
                            if st.form_submit_button(f"{C.E_LLAVE} Guardar", use_container_width=True):
                                if not motivo.strip():
                                    st.warning(f"{C.E_AVISO} Ingresa un motivo")
                                else:
                                    nuevo_data = dict(n.get("data") or {})
                                    nuevo_data["custom_personality"] = nuevo_texto.strip()

                                    ok, msg = _editar_negocio(sb, negocio_id, nuevo_data)
                                    if ok:
                                        _registrar_moderacion(
                                            negocio_id, usuario_id,
                                            "editar_personalidad", "custom_personality",
                                            {"motivo": motivo.strip(), "longitud_nueva": len(nuevo_texto)},
                                        )
                                        st.session_state[f"modal_edit_pers_{negocio_id}"] = False
                                        st.success(f"{C.E_OK} {msg}")
                                        st.rerun()
                                    else:
                                        st.error(f"{C.E_AVISO} {msg}")

                        with col_cancel:
                            if st.form_submit_button("Cancelar", use_container_width=True):
                                st.session_state[f"modal_edit_pers_{negocio_id}"] = False
                                st.rerun()

                # Modal Limpiar
                if st.session_state.get(f"modal_clear_pers_{negocio_id}", False):
                    with st.form(f"form_clear_pers_{negocio_id}"):
                        st.warning(f"{C.E_AVISO} **Vas a borrar la personalidad custom.** El negocio volvera a la default.")
                        motivo = st.text_input(
                            "Motivo",
                            placeholder="Ej: Contenido ofensivo",
                            key=f"clear_pers_motivo_{negocio_id}",
                        )

                        col_ok, col_cancel = st.columns(2)
                        with col_ok:
                            if st.form_submit_button(f"{C.E_PROHIBIDO} Confirmar limpieza", use_container_width=True):
                                if not motivo.strip():
                                    st.warning(f"{C.E_AVISO} Ingresa un motivo")
                                else:
                                    nuevo_data = dict(n.get("data") or {})
                                    nuevo_data["custom_personality"] = ""

                                    ok, msg = _editar_negocio(sb, negocio_id, nuevo_data)
                                    if ok:
                                        _registrar_moderacion(
                                            negocio_id, usuario_id,
                                            "limpiar_personalidad", "custom_personality",
                                            {"motivo": motivo.strip()},
                                        )
                                        st.session_state[f"modal_clear_pers_{negocio_id}"] = False
                                        st.success(f"{C.E_OK} Personalidad limpiada")
                                        st.rerun()
                                    else:
                                        st.error(f"{C.E_AVISO} {msg}")

                        with col_cancel:
                            if st.form_submit_button("Cancelar", use_container_width=True):
                                st.session_state[f"modal_clear_pers_{negocio_id}"] = False
                                st.rerun()
            else:
                st.info("Sin personalidad custom (usa default).")

            st.divider()

            # ======================================
            # Descripcion
            # ======================================
            descripcion = (n.get("descripcion") or "").strip()

            st.markdown(f"#### {C.E_LIBRO} Descripcion")
            if descripcion:
                with st.container(border=True):
                    st.text(descripcion[:1000] + ("..." if len(descripcion) > 1000 else ""))

                col_edit, col_clear, _ = st.columns([1, 1, 2])

                with col_edit:
                    if st.button(f"{C.E_ENGANCHE} Editar", key=f"mod_edit_desc_{negocio_id}", use_container_width=True):
                        st.session_state[f"modal_edit_desc_{negocio_id}"] = True

                if st.session_state.get(f"modal_edit_desc_{negocio_id}", False):
                    with st.form(f"form_edit_desc_{negocio_id}"):
                        nuevo_texto = st.text_area(
                            "Nueva descripcion",
                            value=descripcion,
                            height=150,
                            key=f"edit_desc_text_{negocio_id}",
                        )
                        motivo = st.text_input(
                            "Motivo",
                            key=f"edit_desc_motivo_{negocio_id}",
                        )

                        col_ok, col_cancel = st.columns(2)
                        with col_ok:
                            if st.form_submit_button(f"{C.E_LLAVE} Guardar", use_container_width=True):
                                if not motivo.strip():
                                    st.warning(f"{C.E_AVISO} Ingresa un motivo")
                                else:
                                    nuevo_data = dict(n.get("data") or {})
                                    nuevo_data["descripcion"] = nuevo_texto.strip()

                                    ok, msg = _editar_negocio(sb, negocio_id, nuevo_data)
                                    if ok:
                                        _registrar_moderacion(
                                            negocio_id, usuario_id,
                                            "editar_descripcion", "descripcion",
                                            {"motivo": motivo.strip()},
                                        )
                                        st.session_state[f"modal_edit_desc_{negocio_id}"] = False
                                        st.success(f"{C.E_OK} {msg}")
                                        st.rerun()
                                    else:
                                        st.error(f"{C.E_AVISO} {msg}")

                        with col_cancel:
                            if st.form_submit_button("Cancelar", use_container_width=True):
                                st.session_state[f"modal_edit_desc_{negocio_id}"] = False
                                st.rerun()
            else:
                st.info("Sin descripcion.")

            st.divider()

            # ======================================
            # Tareas
            # ======================================
            tareas = n.get("tareas") or []

            st.markdown(f"#### {C.E_PIN} Tareas ({len(tareas)})")

            if not tareas:
                st.info("Sin tareas.")
            else:
                for t in tareas:
                    tarea_id = t.get("id", "?")
                    titulo = t.get("titulo", "Sin titulo")
                    categoria = t.get("categoria", "-")
                    estado_t = t.get("estado", "-")

                    with st.container(border=True):
                        col_info, col_btn = st.columns([4, 1])
                        with col_info:
                            st.markdown(f"**{titulo}**")
                            st.caption(f"Categoria: {categoria} | Estado: {estado_t} | ID: {tarea_id}")
                        with col_btn:
                            if st.button(
                                f"{C.E_PROHIBIDO}",
                                key=f"mod_del_tarea_{negocio_id}_{tarea_id}",
                                use_container_width=True,
                                help="Eliminar esta tarea",
                            ):
                                st.session_state[f"modal_del_tarea_{negocio_id}_{tarea_id}"] = True

                        if st.session_state.get(f"modal_del_tarea_{negocio_id}_{tarea_id}", False):
                            with st.form(f"form_del_tarea_{negocio_id}_{tarea_id}"):
                                st.warning(f"{C.E_AVISO} **Vas a eliminar la tarea:** '{titulo}'")
                                motivo = st.text_input("Motivo", key=f"del_tarea_motivo_{negocio_id}_{tarea_id}")

                                col_ok, col_cancel = st.columns(2)
                                with col_ok:
                                    if st.form_submit_button(f"{C.E_PROHIBIDO} Eliminar", use_container_width=True):
                                        if not motivo.strip():
                                            st.warning(f"{C.E_AVISO} Ingresa un motivo")
                                        else:
                                            nuevas_tareas = [x for x in tareas if x.get("id") != tarea_id]
                                            nuevo_data = dict(n.get("data") or {})
                                            nuevo_data["tareas"] = nuevas_tareas

                                            ok, msg = _editar_negocio(sb, negocio_id, nuevo_data)
                                            if ok:
                                                _registrar_moderacion(
                                                    negocio_id, usuario_id,
                                                    "eliminar_tarea", "tareas",
                                                    {"motivo": motivo.strip(), "tarea_id": tarea_id, "titulo": titulo[:100]},
                                                )
                                                st.session_state[f"modal_del_tarea_{negocio_id}_{tarea_id}"] = False
                                                st.success(f"{C.E_OK} Tarea eliminada")
                                                st.rerun()
                                            else:
                                                st.error(f"{C.E_AVISO} {msg}")

                                with col_cancel:
                                    if st.form_submit_button("Cancelar", use_container_width=True):
                                        st.session_state[f"modal_del_tarea_{negocio_id}_{tarea_id}"] = False
                                        st.rerun()

    st.divider()
    st.caption(f"{C.E_LIBRO} Cada accion de moderacion se registra en eventos_app (tipo: moderar_contenido).")