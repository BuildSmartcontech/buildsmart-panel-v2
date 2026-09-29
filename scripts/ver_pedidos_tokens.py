import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from utils.supabase_rest import supabase_rest

print("=" * 70)
print("PEDIDOS EN LA BASE DE DATOS")
print("=" * 70)

rows = supabase_rest.table("pedidos_web").select("*").order("created_at", desc=True).limit(10).execute().data or []

if not rows:
    print("  No hay pedidos. Necesitas hacer una compra primero.")
else:
    for p in rows:
        pid = p.get("id", "?")[:12]
        email = p.get("email", "?")
        tier = p.get("tier", "?")
        estado = p.get("estado", "?")
        token = p.get("magic_token") or "(sin token)"
        token_short = token[:20] + "..." if len(token) > 20 else token
        print(f"  [{pid}] {email} - Tier {tier} - {estado}")
        print(f"           Token: {token_short}")
        print()

print("=" * 70)
