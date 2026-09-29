# panels/dueno/tab_staff.py
# ============================================
# TAB STAFF - Gestion de sub-usuarios con roles
# ============================================
# Permite al dueno:
# - Ver todo el staff (activo e inactivo)
# - Crear nuevo staff con rol
# - Cambiar rol
# - Activar/desactivar
# - Eliminar
# - Ver permisos por rol
# ============================================

import streamlit as st
import datetime
from panels.dueno import comun as C


def _registrar_accion(accion, usuario_id, detalle_extra=None):
    """Registra accion de staff en eventos_app."""
    try:
        from utils.logger import log_evento
        detalle = {
            "accion": accion,
            "staff_usuario_id": usuario_id,
            "origen": "panel_dueno_staff",
        }
        if detalle_extra:
            detalle.update(detalle_extra)
        log_evento("staff_accion", detalle=detalle)
    except Exception as e:
        print(f"[tab_staff] Error registrando: {e}")


def renderizar(sb):
    st.markdown(f"### {C.E_USUARIO} Staff y Roles")
    st.caption("Gestiona sub-usuarios con permisos limitados.")

    # ==========================================
    # Importar modulo de staff
    # ==========================================
    try:
        from utils import staff as S
    except Exception as e:
        st.error(f"Error cargando modulo staff: {e}")
        return

    # ==========================================
    # KPIs
    # ==========================================
    staff_lista = S.listar_staff(sb)

    total = len(staff_lista)
    activos = sum(1 for s in staff_lista if s.get("activo"))
    admins = sum(1 for s in staff_lista if s.get("rol") == "admin")
    soportes = sum(1 for s in staff_lista if s.get("rol") == "soporte")
    marketing = sum(1 for s in staff_lista if s.get("rol") == "marketing")

    c1, c2, c3, c4, c5 = st.columns(5)
    C._kpi(c1, f"{C.E_USUARIO} Total", total)
    C._kpi(c2, f"{C.E_OK} Activos", activos)
    C._kpi(c3, "Admin", admins)
    C._kpi(c4, "Soporte", soportes)
    C._kpi(c5, "Marketing", marketing)

    st.divider()

    # ==========================================
    # Crear nuevo staff
    # ==========================================
    with st.expander(f"{C.E_LLAVE} Crear nuevo staff", expanded=False):
        with st.form("form_crear_staff"):
            col1, col2 = st.columns(2)

            with col1:
                nuevo_usuario_id = st.text_input(
                    "Usuario ID (UUID)",
                    placeholder="Ej: 61dcd466-d937-45c4-8bb6-612a0a8548a1",
                    help="El UUID del usuario al que se le asigna el rol",
                )
                nuevo_nombre = st.text_input("Nombre completo", placeholder="Ej: Maria Perez")

            with col2:
                nuevo_email = st.text_input("Email (opcional)", placeholder="Ej: maria@samu-ia.com")
                nuevo_rol = st.selectbox(
                    "Rol",
                    options=S.roles_disponibles(),
                    format_func=lambda r: f"{S.info_rol(r)['nombre']} - {S.info_rol(r)['descripcion']}",
                )

            nuevo_notas = st.text_area("Notas internas (opcional)", height=80)

            if st.form_submit_button(f"{C.E_OK} Crear staff", use_container_width=True, type="primary"):
                if not nuevo_usuario_id.strip():
                    st.warning(f"{C.E_AVISO} El Usuario ID es obligatorio")
                elif not nuevo_nombre.strip():
                    st.warning(f"{C.E_AVISO} El nombre es obligatorio")
                else:
                    ok, msg = S.crear_staff(
                        sb,
                        nuevo_usuario_id.strip(),
                        nuevo_nombre.strip(),
                        nuevo_email.strip(),
                        nuevo_rol,
                        nuevo_notas.strip(),
                    )
                    if ok:
                        _registrar_accion("crear_staff", nuevo_usuario_id.strip(), {"rol": nuevo_rol, "nombre": nuevo_nombre})
                        st.success(f"{C.E_OK} {msg}")
                        st.rerun()
                    else:
                        st.error(f"{C.E_AVISO} {msg}")

    st.divider()

    # ==========================================
    # Lista de staff
    # ==========================================
    if not staff_lista:
        st.info(f"{C.E_AVISO} Aun no hay staff registrado. Crea el primero arriba.")
        return

    st.markdown(f"#### {C.E_CLIENTES} Staff registrado ({total})")

    # Filtros
    col_f1, col_f2 = st.columns([2, 2])
    with col_f1:
        filtro_rol = st.selectbox(
            "Filtrar por rol",
            ["(todos)"] + list(S.ROLES.keys()),
            key="staff_filtro_rol",
        )
    with col_f2:
        filtro_estado = st.selectbox(
            "Filtrar por estado",
            ["(todos)", "Activos", "Inactivos"],
            key="staff_filtro_estado",
        )

    # Aplicar filtros
    filtrados = []
    for s in staff_lista:
        if filtro_rol != "(todos)" and s.get("rol") != filtro_rol:
            continue
        activo = s.get("activo", True)
        if filtro_estado == "Activos" and not activo:
            continue
        if filtro_estado == "Inactivos" and activo:
            continue
        filtrados.append(s)

    st.caption(f"Mostrando {len(filtrados)} de {total}")

    # ==========================================
    # Renderizar cada staff
    # ==========================================
    for s in filtrados:
        usuario_id = s.get("usuario_id", "?")
        nombre = s.get("nombre", "Sin nombre")
        email = s.get("email") or "-"
        rol = s.get("rol", "?")
        activo = s.get("activo", True)
        notas = s.get("notas", "")
        fecha = str(s.get("created_at", ""))[:19].replace("T", " ")
        info_rol = S.info_rol(rol)

        # Icono de estado
        if activo:
            icono_estado = C.E_OK
            label_estado = "ACTIVO"
        else:
            icono_estado = C.E_PROHIBIDO
            label_estado = "INACTIVO"

        titulo = f"{icono_estado} {nombre} - {info_rol['nombre']} [{label_estado}]"

        with st.expander(titulo):
            # Info principal
            col_a, col_b = st.columns([3, 2])
            with col_a:
                st.markdown(f"**Usuario ID:** `{usuario_id}`")
                st.markdown(f"**Email:** {email}")
                st.markdown(f"**Rol actual:** {info_rol['nombre']} ({rol})")
                st.caption(f"Descripcion: {info_rol['descripcion']}")
                if notas:
                    st.caption(f"{C.E_LIBRO} Notas: {notas}")
            with col_b:
                st.markdown(f"**Estado:** {label_estado}")
                st.caption(f"Creado: {fecha}")
                st.caption(f"Permisos: {len(info_rol['permisos'])}")

            st.divider()

            # ======================================
            # Acciones: cambiar rol / activar / eliminar
            # ======================================
            col_rol, col_estado, col_del = st.columns(3)

            # Cambiar rol
            with col_rol:
                st.markdown("**Cambiar rol**")
                nuevo_rol = st.selectbox(
                    "Nuevo rol",
                    options=S.roles_disponibles(),
                    index=S.roles_disponibles().index(rol) if rol in S.roles_disponibles() else 0,
                    key=f"rol_{usuario_id}",
                    label_visibility="collapsed",
                )
                if st.button(
                    f"{C.E_ENGANCHE} Aplicar",
                    key=f"btn_rol_{usuario_id}",
                    use_container_width=True,
                    disabled=(nuevo_rol == rol),
                ):
                    ok, msg = S.cambiar_rol(sb, usuario_id, nuevo_rol)
                    if ok:
                        _registrar_accion("cambiar_rol", usuario_id, {"rol_anterior": rol, "rol_nuevo": nuevo_rol})
                        st.success(f"{C.E_OK} Rol cambiado a {nuevo_rol}")
                        st.rerun()
                    else:
                        st.error(f"{C.E_AVISO} {msg}")

            # Activar / Desactivar
            with col_estado:
                st.markdown("**Estado**")
                if activo:
                    if st.button(
                        f"{C.E_CANDADO} Desactivar",
                        key=f"btn_estado_{usuario_id}",
                        use_container_width=True,
                    ):
                        ok, msg = S.desactivar_staff(sb, usuario_id)
                        if ok:
                            _registrar_accion("desactivar_staff", usuario_id, {"rol": rol})
                            st.success(f"{C.E_OK} Staff desactivado")
                            st.rerun()
                        else:
                            st.error(f"{C.E_AVISO} {msg}")
                else:
                    if st.button(
                        f"{C.E_ABIERTO} Reactivar",
                        key=f"btn_estado_{usuario_id}",
                        use_container_width=True,
                    ):
                        ok, msg = S.activar_staff(sb, usuario_id)
                        if ok:
                            _registrar_accion("reactivar_staff", usuario_id, {"rol": rol})
                            st.success(f"{C.E_OK} Staff reactivado")
                            st.rerun()
                        else:
                            st.error(f"{C.E_AVISO} {msg}")

            # Eliminar (con confirmacion)
            with col_del:
                st.markdown("**Eliminar**")
                if st.button(
                    f"{C.E_PROHIBIDO} Eliminar",
                    key=f"btn_del_{usuario_id}",
                    use_container_width=True,
                ):
                    st.session_state[f"confirmar_del_{usuario_id}"] = True

                if st.session_state.get(f"confirmar_del_{usuario_id}", False):
                    st.warning(f"{C.E_AVISO} Esto elimina permanentemente a {nombre}")
                    col_si, col_no = st.columns(2)
                    with col_si:
                        if st.button(f"{C.E_LLAVE} Confirmar", key=f"conf_del_{usuario_id}", use_container_width=True):
                            ok, msg = S.eliminar_staff(sb, usuario_id)
                            if ok:
                                _registrar_accion("eliminar_staff", usuario_id, {"nombre": nombre, "rol": rol})
                                st.session_state[f"confirmar_del_{usuario_id}"] = False
                                st.success(f"{C.E_OK} Staff eliminado")
                                st.rerun()
                            else:
                                st.error(f"{C.E_AVISO} {msg}")
                    with col_no:
                        if st.button("Cancelar", key=f"canc_del_{usuario_id}", use_container_width=True):
                            st.session_state[f"confirmar_del_{usuario_id}"] = False
                            st.rerun()

    st.divider()

    # ==========================================
    # Info de roles disponibles
    # ==========================================
    with st.expander(f"{C.E_TUBO} Ver roles y permisos", expanded=False):
        st.markdown("### Roles disponibles")
        for rol_key, info in S.ROLES.items():
            st.markdown(f"#### {info['nombre']} (`{rol_key}`)")
            st.caption(info["descripcion"])
            if "*" in info["permisos"]:
                st.info(f"{C.E_OK} **Todos los permisos**")
            else:
                st.markdown("**Permisos:**")
                for p in info["permisos"]:
                    st.text(f"  - {p}")
            st.markdown("")

    st.divider()
    st.caption(f"{C.E_LIBRO} Cada accion se registra en eventos_app (tipo: staff_accion).")