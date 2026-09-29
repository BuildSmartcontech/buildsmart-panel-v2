# utils/persistence.py
# ============================================
# PERSISTENCIA EN SUPABASE - V1.0
# ============================================
# Usa el cliente existente de supabase_client.py
# para guardar y cargar negocios.
# ============================================

import os
import sys
import json
import requests
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.supabase_client import supabase
except ImportError:
    from supabase_client import supabase


# ============================================
# VERIFICACION
# ============================================

def esta_disponible():
    """Verifica si Supabase esta configurado."""
    if supabase is None:
        return False
    return bool(supabase.disponible and supabase.url and supabase.key)


# ============================================
# GUARDAR NEGOCIO
# ============================================

def guardar_negocio(usuario_id, negocio_id, negocio_data):
    """
    Guarda o actualiza un negocio en Supabase.
    Returns: (exito: bool, mensaje: str)
    """
    if not esta_disponible():
        return False, "Supabase no disponible"

    if not usuario_id or not negocio_id:
        return False, "Falta usuario_id o negocio_id"

    try:
        data_limpia = _limpiar_data(negocio_data)

        payload = {
            "id": negocio_id,
            "usuario_id": str(usuario_id),
            "data": data_limpia,
            "updated_at": datetime.datetime.now().isoformat()
        }

        headers = dict(supabase.headers)
        headers["Prefer"] = "resolution=merge-duplicates"

        r = requests.post(
            supabase.url + "/rest/v1/negocios",
            headers=headers,
            json=payload,
            timeout=15
        )

        if r.status_code in (200, 201, 204):
            return True, "Guardado correctamente"
        else:
            return False, "Error " + str(r.status_code) + ": " + r.text[:200]

    except Exception as e:
        return False, "Error: " + str(e)


# ============================================
# CARGAR NEGOCIOS
# ============================================

def cargar_negocios(usuario_id):
    """
    Carga todos los negocios del usuario.
    Returns: (exito: bool, negocios: dict | error: str)
    """
    if not esta_disponible():
        return False, "Supabase no disponible"

    if not usuario_id:
        return False, "Falta usuario_id"

    try:
        params = {"usuario_id": "eq." + str(usuario_id)}

        r = requests.get(
            supabase.url + "/rest/v1/negocios",
            headers=supabase.headers,
            params=params,
            timeout=15
        )

        if r.status_code != 200:
            return False, "Error " + str(r.status_code) + ": " + r.text[:200]

        data = r.json()
        negocios = {}
        for row in data:
            negocios[row["id"]] = row["data"]

        return True, negocios

    except Exception as e:
        return False, "Error: " + str(e)


# ============================================
# CARGAR UN NEGOCIO
# ============================================

def cargar_negocio(usuario_id, negocio_id):
    """Carga un negocio especifico."""
    if not esta_disponible():
        return False, "Supabase no disponible"

    try:
        params = {
            "id": "eq." + negocio_id,
            "usuario_id": "eq." + str(usuario_id)
        }

        r = requests.get(
            supabase.url + "/rest/v1/negocios",
            headers=supabase.headers,
            params=params,
            timeout=15
        )

        if r.status_code != 200:
            return False, "Error " + str(r.status_code)

        data = r.json()
        if data and len(data) > 0:
            return True, data[0]["data"]
        return False, "No encontrado"

    except Exception as e:
        return False, "Error: " + str(e)


# ============================================
# ELIMINAR NEGOCIO
# ============================================

def eliminar_negocio(usuario_id, negocio_id):
    """Elimina un negocio."""
    if not esta_disponible():
        return False, "Supabase no disponible"

    try:
        params = {
            "id": "eq." + negocio_id,
            "usuario_id": "eq." + str(usuario_id)
        }

        r = requests.delete(
            supabase.url + "/rest/v1/negocios",
            headers=supabase.headers,
            params=params,
            timeout=15
        )

        if r.status_code in (200, 204):
            return True, "Eliminado"
        return False, "Error " + str(r.status_code)

    except Exception as e:
        return False, "Error: " + str(e)


# ============================================
# UTILIDADES
# ============================================

def _limpiar_data(data):
    """Limpia el diccionario para que sea JSON-serializable."""
    if isinstance(data, dict):
        return {k: _limpiar_data(v) for k, v in data.items() if not k.startswith("_")}
    elif isinstance(data, list):
        return [_limpiar_data(item) for item in data]
    elif isinstance(data, (str, int, float, bool)) or data is None:
        return data
    else:
        return str(data)


# ============================================
# TEST
# ============================================

def test_persistence():
    print("=" * 60)
    print("TEST PERSISTENCIA SUPABASE")
    print("=" * 60)

    if not esta_disponible():
        print("\nERROR: Supabase no disponible")
        print("Verifica tu archivo .env con SUPABASE_URL y SUPABASE_KEY")
        return

    print("\nSupabase disponible: SI")
    print("URL: " + supabase.url)

    usuario_test = "00000000-0000-0000-0000-000000000001"
    negocio_id = "test_negocio_1"

    negocio_test = {
        "id": negocio_id,
        "nombre": "Dulceria Test",
        "sector": "alimentos",
        "descripcion": "Test de persistencia",
        "tareas": [
            {"id": 1, "titulo": "Tarea 1", "estado": "TODO"},
            {"id": 2, "titulo": "Tarea 2", "estado": "HECHO"}
        ]
    }

    print("\n1. Guardando negocio de prueba...")
    ok, msg = guardar_negocio(usuario_test, negocio_id, negocio_test)
    print("   " + ("OK" if ok else "FALLO") + ": " + msg)

    if not ok:
        print("\nSugerencias:")
        print("   - Verifica que la tabla 'negocios' exista en Supabase")
        print("   - Verifica que el .env tenga SUPABASE_KEY correcta")
        print("   - Verifica que la clave sea 'service_role' o 'anon'")
        return

    print("\n2. Cargando negocios...")
    ok, data = cargar_negocios(usuario_test)

    if ok:
        print("   Negocios encontrados: " + str(len(data)))
        if negocio_id in data:
            n = data[negocio_id]
            print("   Nombre: " + n.get("nombre", ""))
            print("   Tareas: " + str(len(n.get("tareas", []))))
            print("\n   EXITO: Persistencia funciona correctamente")
        else:
            print("   ERROR: Negocio no encontrado tras guardar")
    else:
        print("   FALLO: " + str(data))

    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_persistence()