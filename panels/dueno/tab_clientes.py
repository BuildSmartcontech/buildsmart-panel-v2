# panels/dueno/tab_clientes.py
# ============================================
# TAB CLIENTES - Lista + suspender/reactivar
# ============================================

import streamlit as st
from panels.dueno import comun as C


def renderizar(sb, inicio, fin):
    st.markdown(f"### {C.E_CLIENTES} Clientes y sus negocios")

    try:
        data_neg = sb.table("negocios").select("*").execute().data or []
    except Exception as e:
        st.error(f"Error leyendo negocios: {e}")
        return

    negocios_todos = [C._plano(n) for n in data_neg]
    negocios = [n for n in negocios_todos if C._dentro_de_rango(n, "created_at", inicio, fin)]

    if not negocios:
        st.info(f"{C.E_AVISO} No hay negocios en el rango seleccionado.")
        return

    estados = C._obtener_estados_usuarios(sb)

    por_usuario = {}
    for n in negocios:
        uid = n.get("usuario_id", "sin_usuario")
        por_usuario.setdefault(uid, []).append(n)

    total_usuarios = len(por_usuario)
    total_suspendidos = sum(1 for uid in por_usuario if C._estado_de(uid, estados) == "suspendido")

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1: st.metric("Total usuarios", total_usuarios)
    with col_m2: st.metric("Activos", total_usuarios - total_suspendidos)
    with col_m3: st.metric("Suspendidos", total_suspendidos)

    st.divider()
    busqueda = st.text_input("Buscar por nombre o usuario", "")

    for uid, lista in por_usuario.items():
        nombre_neg = lista[0].get("nombre", "?") if lista else "?"
        if busqueda and busqueda.lower() not in (str(uid) + str(nombre_neg)).lower():
            continue

        estado = C._estado_de(uid, estados)
        info_estado = estados.get(uid, {})
        icono_estado = C.E_OK if estado == "activo" else C.E_PROHIBIDO

        titulo_exp = f"{icono_estado} Usuario {str(uid)[:12]}... - {len(lista)} negocio(s) [{estado}]"

        with st.expander(titulo_exp):
            col_e1, col_e2 = st.columns([2, 2])

            with col_e1:
                if estado == "suspendido":
                    st.error(
                        f"{C.E_PROHIBIDO} **Suspendido**\n\n"
                        f"Motivo: {info_estado.get('motivo', 'Sin especificar')}\n\n"
                        f"Fecha: {str(info_estado.get('fecha_accion', '?'))[:19].replace('T', ' ')}\n\n"
                        f"Por: `{str(info_estado.get('quien_accion', '?'))[:20]}`"
                    )
                else:
                    st.success(f"{C.E_OK} **Cuenta activa**")

            with col_e2:
                if estado == "suspendido":
                    if st.button(f"{C.E_ABIERTO} Reactivar cuenta", key=f"react_{uid}", use_container_width=True):
                        ok, msg = C._cambiar_estado_usuario(
                            sb, uid, "activo",
                            "Reactivado por el dueno",
                            "antonio"
                        )
                        if ok:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                else:
                    if st.button(f"{C.E_CANDADO} Suspender cuenta", key=f"susp_{uid}", use_container_width=True):
                        st.session_state[f"modal_susp_{uid}"] = True

                if st.session_state.get(f"modal_susp_{uid}", False):
                    motivo = st.text_input(
                        "Motivo de la suspension",
                        key=f"motivo_{uid}",
                        placeholder="Ej: Uso indebido del servicio",
                    )
                    col_conf, col_canc = st.columns(2)
                    with col_conf:
                        if st.button(f"{C.E_LLAVE} Confirmar", key=f"conf_susp_{uid}", use_container_width=True):
                            if motivo.strip():
                                ok, msg = C._cambiar_estado_usuario(
                                    sb, uid, "suspendido",
                                    motivo.strip(),
                                    "antonio"
                                )
                                if ok:
                                    st.session_state[f"modal_susp_{uid}"] = False
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)
                            else:
                                st.warning(f"{C.E_AVISO} Ingresa un motivo")
                    with col_canc:
                        if st.button("Cancelar", key=f"canc_susp_{uid}", use_container_width=True):
                            st.session_state[f"modal_susp_{uid}"] = False
                            st.rerun()

            st.divider()

            for n in lista:
                C._renderizar_negocio_con_acciones(sb, n)

            st.divider()
            if st.button(f"{C.E_OJO} Ver detalle completo", key=f"detalle_{uid}", use_container_width=True):
                st.session_state.cliente_detalle_id = uid
                st.rerun()