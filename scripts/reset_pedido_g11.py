import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from utils.supabase_rest import supabase_rest

pedido_id = "c8c1f3c3-184d-4804-afa9-74cf197c7b1b"

print("=" * 70)
print(f"RESET PEDIDO {pedido_id}")
print("=" * 70)

# Resetear a "pagado" para poder regenerar
supabase_rest.update(
    "pedidos_web",
    {
        "estado": "pagado",
        "web_id": None,
        "web_url": None,
        "entregado_at": None,
    },
    "id",
    pedido_id,
)

print("OK: Pedido reseteado a 'pagado'")
print()
print("Ahora:")
print("1. Abri el panel dueno")
print("2. Tab Pedidos Web")
print("3. Click 'Generar web ahora' en este pedido")
print("4. El formulario se va a inyectar automaticamente")
