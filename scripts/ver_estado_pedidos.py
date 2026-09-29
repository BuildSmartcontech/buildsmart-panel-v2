import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from utils.supabase_rest import supabase_rest

print("=" * 70)
print("ESTADO REAL DE LOS PEDIDOS")
print("=" * 70)

rows = supabase_rest.table("pedidos_web").select("*").order("created_at", desc=True).limit(5).execute().data or []

for p in rows:
    pid = p.get("id", "?")[:12]
    estado = p.get("estado", "?")
    web_url = p.get("web_url") or "(VACIO)"
    web_id = p.get("web_id") or "(VACIO)"
    print(f"[{pid}]")
    print(f"  estado: {estado}")
    print(f"  web_url: {web_url[:60]}")
    print(f"  web_id: {web_id[:30]}")
    print()
