import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from utils.supabase_rest import supabase_rest

print("=" * 100)
print("URLS DE PANEL LISTAS PARA ABRIR")
print("=" * 100)

rows = supabase_rest.table("pedidos_web").select("*").order("created_at", desc=True).limit(10).execute().data or []

for p in rows:
    pid = p.get("id", "?")[:12]
    email = p.get("email", "?")
    estado = p.get("estado", "?")
    tier = p.get("tier", "?")
    token = p.get("magic_token") or ""

    print(f"\n[{pid}] {email} - Tier {tier} - {estado}")

    if token:
        url = f"http://localhost:8501/?web=panel&token={token}"
        print(f"URL: {url}")
    else:
        print("URL: (sin token, este pedido es viejo)")

print("\n" + "=" * 100)
