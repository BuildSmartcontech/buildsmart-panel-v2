import os, requests
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("CLOUDFLARE_TOKEN", "")

if not token or not token.startswith("cfut_"):
    print("ERROR: Token no configurado en .env")
    exit(1)

print("=" * 60)
print("CUENTAS CLOUDFLARE")
print("=" * 60)

r = requests.get(
    "https://api.cloudflare.com/client/v4/accounts",
    headers={"Authorization": f"Bearer {token}"},
    timeout=10,
)

if r.status_code == 200:
    cuentas = r.json().get("result", [])
    if cuentas:
        for c in cuentas:
            print(f"Account ID: {c.get('id')}")
            print(f"  Nombre: {c.get('name')}")
    else:
        print("Sin cuentas. Verificar permisos del token.")
else:
    print(f"Error: {r.status_code}")
    print(r.text[:300])
print("=" * 60)
