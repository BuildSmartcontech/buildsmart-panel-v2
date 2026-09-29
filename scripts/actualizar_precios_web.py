# scripts/actualizar_precios_web.py
# ============================================
# ACTUALIZAR PRECIOS WEB EN CONFIG_GLOBAL
# ============================================

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))


PRECIOS = {
    # WEB GANCHO (3 tiers)
    "web_precio_tier1": 149,          # Web Basica
    "web_precio_tier2": 299,          # Web + CRM
    "web_precio_tier3": 499,          # Web Premium

    # Renovaciones anuales
    "web_renovacion_tier1_2": 59,     # Renovacion T1/T2
    "web_renovacion_tier3": 79,       # Renovacion T3 (con dominio)

    # Notas
    "web_tier1_incluye": "Web + hosting 1 año + subdominio SAMU IA",
    "web_tier2_incluye": "Todo T1 + CRM captura + mini-panel",
    "web_tier3_incluye": "Todo T2 + dominio propio + CRM completo + logo custom + soporte prioritario",
}


def main():
    print("=" * 70)
    print("ACTUALIZAR PRECIOS WEB EN CONFIG_GLOBAL")
    print("=" * 70)

    try:
        from utils.supabase_rest import supabase_rest
        if not supabase_rest.disponible:
            print("ERROR: Supabase no disponible")
            return
    except Exception as e:
        print(f"ERROR: {e}")
        return

    for clave, valor in PRECIOS.items():
        try:
            # Verificar si existe
            existente = supabase_rest.table("config_global").select("*").eq("clave", clave).execute().data or []

            if existente:
                # Update
                supabase_rest.update(
                    "config_global",
                    {"valor": valor},
                    "clave",
                    clave,
                )
                print(f"  [UPDATE] {clave} = {valor}")
            else:
                # Insert
                supabase_rest.insert("config_global", {"clave": clave, "valor": valor})
                print(f"  [INSERT] {clave} = {valor}")

        except Exception as e:
            print(f"  [ERROR] {clave}: {e}")

    print("=" * 70)
    print("LISTO")


if __name__ == "__main__":
    main()