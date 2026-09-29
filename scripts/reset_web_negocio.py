# scripts\reset_web_negocio.py
# ============================================
# RESET WEB DE UN NEGOCIO (SOLO DESARROLLO)
# ============================================
# Borra el sitio_web del negocio en Supabase para
# permitir regenerar con el nuevo Director de Arte.
# ============================================

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))


def resetear_web(nombre_negocio="Fabricante de Velas"):
    from utils.supabase_rest import supabase_rest
    if not supabase_rest.disponible:
        print("ERROR: Supabase no disponible")
        return

    rows = supabase_rest.table("negocios").select("*").execute().data or []
    encontrado = None
    for r in rows:
        data = r.get("data") or {}
        if data.get("nombre") == nombre_negocio:
            encontrado = r
            break

    if not encontrado:
        print(f"No se encontro negocio: {nombre_negocio}")
        return

    negocio_id = encontrado.get("id")
    data = dict(encontrado.get("data") or {})

    data["sitio_web"] = {
        "url": "",
        "url_publica": "",
        "visitantes": 0,
        "ingresos": "$0.00",
        "actualizado": "SIN CREAR",
        "archivo_generado": None,
        "vinculada": False,
    }
    data["modificaciones_usadas"] = 0

    supabase_rest.update("negocios", {"data": data}, "id", negocio_id)
    print(f"[OK] Web reseteada para: {nombre_negocio}")
    print(f"     Negocio ID: {negocio_id}")
    print(f"     Ahora podes generar una web nueva con Director de Arte V5.0")


if __name__ == "__main__":
    resetear_web()
