import sys, os
from pathlib import Path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import requests
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

headers_get = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
}
headers_post = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}

# PASO 1: Obtener un pedido REAL
print("=" * 60)
print("PASO 1: Buscar un pedido real")
print("=" * 60)

r = requests.get(
    f"{url}/rest/v1/pedidos_web?select=id,email,estado&order=created_at.desc&limit=5",
    headers=headers_get,
    timeout=15,
)

if r.status_code != 200:
    print(f"ERROR consultando pedidos: {r.status_code}")
    print(r.text)
    sys.exit(1)

pedidos = r.json()
if not pedidos:
    print("ERROR: No hay pedidos en la DB")
    sys.exit(1)

for p in pedidos:
    print(f"  ID: {p['id']}")
    print(f"  Email: {p.get('email')}")
    print(f"  Estado: {p.get('estado')}")
    print()

# Usar el primer pedido real
pedido_real_id = pedidos[0]["id"]
print(f"Usando pedido: {pedido_real_id}")
print()

# PASO 2: Test insert con UUID real
print("=" * 60)
print("PASO 2: Test insert anonimo en crm_leads")
print("=" * 60)

payload = {
    "pedido_web_id": pedido_real_id,
    "nombre": "Test Lead G11",
    "email": "test@ejemplo.com",
    "telefono": "300 111 2222",
    "mensaje": "Lead de prueba G11",
    "estado": "nuevo",
    "origen": "formulario_web",
}

r2 = requests.post(f"{url}/rest/v1/crm_leads", headers=headers_post, json=payload, timeout=15)
print(f"Status: {r2.status_code}")
print(f"Respuesta: {r2.text[:400]}")
print("=" * 60)

if r2.status_code in (200, 201):
    print("OK: El insert funciona. RLS esta bien configurada.")
elif r2.status_code in (401, 403):
    print("ERROR RLS: La policy no permite el insert")
elif r2.status_code == 409:
    print("ERROR FK: El pedido_web_id no existe (raro, usamos uno real)")
else:
    print(f"ERROR inesperado: {r2.status_code}")
