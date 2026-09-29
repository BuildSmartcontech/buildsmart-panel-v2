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

if not url or not key:
    print("ERROR: SUPABASE_URL o SUPABASE_KEY no configurados")
    sys.exit(1)

# Headers como si fuera el formulario publico (anon key)
headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}

# Usar un pedido real que exista
pedido_id = "c8c1f3c3-184d-4884-af9a-74cf197c7b1b"

payload = {
    "pedido_web_id": pedido_id,
    "nombre": "Test Lead G11",
    "email": "test@ejemplo.com",
    "telefono": "300 111 2222",
    "mensaje": "Este es un lead de prueba G11",
    "estado": "nuevo",
    "origen": "formulario_web",
}

print("=" * 60)
print("TEST INSERT ANONIMO EN crm_leads")
print("=" * 60)

r = requests.post(f"{url}/rest/v1/crm_leads", headers=headers, json=payload, timeout=15)
print(f"Status: {r.status_code}")
print(f"Respuesta: {r.text[:500]}")
print("=" * 60)

if r.status_code in (200, 201):
    print("OK: El insert funciona")
else:
    print("ERROR: Revisar policy RLS")
    print(f"Detalle: {r.text}")
