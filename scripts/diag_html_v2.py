import sys, re
from pathlib import Path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from utils.supabase_rest import supabase_rest

# Buscar el pedido para saber su nuevo web_id
r = supabase_rest.table("pedidos_web").select("*").eq("id", "c8c1f3c3-184d-4804-afa9-74cf197c7b1b").execute()
if not r.data:
    print("ERROR: Pedido no encontrado")
    sys.exit(1)

p = r.data[0]
web_id = p.get("web_id")
web_url = p.get("web_url")
usuario_id = "pedido_c8c1f3c3"

print("=" * 70)
print("DIAGNOSTICO HTML V2")
print("=" * 70)
print(f"Web ID: {web_id}")
print(f"URL: {web_url}")
print()

ruta = Path("data") / "webs_generadas" / usuario_id / str(web_id) / "index.html"
print(f"Ruta: {ruta}")
print(f"Existe: {ruta.exists()}")

if ruta.exists():
    html = ruta.read_text(encoding="utf-8")
    print(f"Tamaño: {len(html):,} chars")
    print()
    tiene_script = "crm_leads" in html
    tiene_pedido = "c8c1f3c3-184d-4804-afa9-74cf197c7b1b" in html
    tiene_fetch = "fetch(" in html
    print(f"[{'OK' if tiene_script else 'NO'}] Formulario (crm_leads)")
    print(f"[{'OK' if tiene_pedido else 'NO'}] PEDIDO_ID")
    print(f"[{'OK' if tiene_fetch else 'NO'}] fetch()")
