# utils/staff.py
# ============================================
# GESTION DE STAFF - SAMU IA
# ============================================
# V2.0: Agrega permisos para Pedidos Web
# V1.0: Version inicial
#
# Helpers para gestionar sub-usuarios con roles.
# Roles disponibles: dueno, admin, soporte, marketing
# ============================================

import datetime


# ==========================================
# DEFINICION DE ROLES Y PERMISOS
# ==========================================
ROLES = {
    "dueno": {
        "nombre": "Dueno",
        "descripcion": "Control total del sistema",
        "permisos": ["*"],  # Todos
    },
    "admin": {
        "nombre": "Administrador",
        "descripcion": "Todo menos configuracion global y staff",
        "permisos": [
            "panel.ver",
            "clientes.ver",
            "clientes.suspender",
            "pedidos_web.ver",
            "pedidos_web.gestionar",
            "ingresos.ver",
            "webs.ver",
            "webs.republicar",
            "uso_ia.ver",
            "moderacion.usar",
            "auditoria.ver",
            "registros.ver",
            "salud.ver",
        ],
    },
    "soporte": {
        "nombre": "Soporte",
        "descripcion": "Ver clientes y pedidos, suspender/reactivar",
        "permisos": [
            "panel.ver",
            "clientes.ver",
            "clientes.suspender",
            "pedidos_web.ver",
            "registros.ver",
            "salud.ver",
        ],
    },
    "marketing": {
        "nombre": "Marketing",
        "descripcion": "Ver metricas y auditar contenido",
        "permisos": [
            "panel.ver",
            "clientes.ver",
            "uso_ia.ver",
            "auditoria.ver",
            "registros.ver",
        ],
    },
}


def roles_disponibles():
    """Devuelve lista de roles disponibles (sin dueno)."""
    return ["admin", "soporte", "marketing"]


def info_rol(rol):
    """Devuelve dict con informacion del rol."""
    return ROLES.get(rol, {"nombre": rol, "descripcion": "?", "permisos": []})


def tiene_permiso(rol, permiso):
    """Verifica si un rol tiene un permiso."""
    if not rol:
        return False
    info = ROLES.get(rol)
    if not info:
        return False
    if "*" in info["permisos"]:
        return True
    return permiso in info["permisos"]


# ==========================================
# CRUD
# ==========================================
def listar_staff(sb):
    """Lista todo el staff activo e inactivo."""
    try:
        rows = sb.table("staff").select("*").order("created_at", desc=True).execute().data or []
        return rows
    except Exception as e:
        print(f"[staff] Error listando: {e}")
        return []


def obtener_staff(sb, usuario_id):
    """Devuelve info de un staff por usuario_id."""
    try:
        rows = sb.table("staff").select("*").eq("usuario_id", usuario_id).execute().data or []
        return rows[0] if rows else None
    except Exception as e:
        print(f"[staff] Error obteniendo: {e}")
        return None


def crear_staff(sb, usuario_id, nombre, email, rol, notas=""):
    """Crea un nuevo miembro del staff."""
    if rol not in ROLES:
        return False, f"Rol invalido: {rol}"

    if rol == "dueno":
        return False, "No se puede crear otro dueno"

    existente = obtener_staff(sb, usuario_id)
    if existente:
        return False, f"Ya existe staff con usuario_id {usuario_id}"

    try:
        payload = {
            "usuario_id": usuario_id,
            "nombre": nombre.strip()[:100],
            "email": (email or "").strip()[:200],
            "rol": rol,
            "activo": True,
            "notas": (notas or "").strip()[:500],
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }
        sb.insert("staff", payload)
        return True, f"Staff creado: {nombre} ({rol})"
    except Exception as e:
        return False, f"Error: {e}"


def actualizar_staff(sb, usuario_id, cambios):
    """Actualiza campos de un staff existente."""
    try:
        payload = dict(cambios)
        payload["updated_at"] = datetime.datetime.now().isoformat()
        sb.update("staff", payload, "usuario_id", usuario_id)
        return True, "Actualizado"
    except Exception as e:
        return False, f"Error: {e}"


def cambiar_rol(sb, usuario_id, nuevo_rol):
    """Cambia el rol de un staff."""
    if nuevo_rol not in ROLES:
        return False, f"Rol invalido: {nuevo_rol}"
    if nuevo_rol == "dueno":
        return False, "No se puede asignar rol dueno"
    return actualizar_staff(sb, usuario_id, {"rol": nuevo_rol})


def activar_staff(sb, usuario_id):
    """Activa un staff."""
    return actualizar_staff(sb, usuario_id, {"activo": True})


def desactivar_staff(sb, usuario_id):
    """Desactiva (no borra) un staff."""
    return actualizar_staff(sb, usuario_id, {"activo": False})


def eliminar_staff(sb, usuario_id):
    """Elimina definitivamente un staff."""
    try:
        sb.delete("staff", "usuario_id", usuario_id)
        return True, "Eliminado"
    except Exception as e:
        return False, f"Error: {e}"


# ==========================================
# TEST MANUAL
# ==========================================
if __name__ == "__main__":
    print("=" * 70)
    print("TEST STAFF MODULE V2.0")
    print("=" * 70)
    print(f"Roles disponibles: {', '.join(ROLES.keys())}")
    print()
    for rol in ROLES:
        info = info_rol(rol)
        print(f"[{rol}]")
        print(f"  Nombre: {info['nombre']}")
        print(f"  Descripcion: {info['descripcion']}")
        print(f"  Permisos: {len(info['permisos'])}")
        print()

    print("Test de permisos:")
    print(f"  admin tiene 'pedidos_web.ver'? {tiene_permiso('admin', 'pedidos_web.ver')}")
    print(f"  admin tiene 'pedidos_web.gestionar'? {tiene_permiso('admin', 'pedidos_web.gestionar')}")
    print(f"  soporte tiene 'pedidos_web.ver'? {tiene_permiso('soporte', 'pedidos_web.ver')}")
    print(f"  soporte tiene 'pedidos_web.gestionar'? {tiene_permiso('soporte', 'pedidos_web.gestionar')}")
    print(f"  marketing tiene 'pedidos_web.ver'? {tiene_permiso('marketing', 'pedidos_web.ver')}")
    print(f"  dueno tiene 'pedidos_web.gestionar'? {tiene_permiso('dueno', 'pedidos_web.gestionar')}")
    print("=" * 70)