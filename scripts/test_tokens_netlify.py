import os, requests
from dotenv import load_dotenv
load_dotenv()

tokens = {
    "NETLIFY_TOKEN":   os.getenv("NETLIFY_TOKEN", ""),
    "NETLIFY_API_KEY": os.getenv("NETLIFY_API_KEY", ""),
}

site_id = os.getenv("NETLIFY_SITE_ID", "")

print("=" * 70)
print("TEST DE TOKENS NETLIFY")
print("=" * 70)

for nombre, token in tokens.items():
    if not token:
        print(f"\n[{nombre}] VACIO")
        continue

    print(f"\n[{nombre}] {token[:15]}...")
    r = requests.get(
        "https://api.netlify.com/api/v1/user",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    if r.status_code == 200:
        data = r.json()
        print(f"  OK - Email: {data.get('email')}")
        print(f"  OK - Nombre: {data.get('full_name', '?')}")
    else:
        print(f"  FALLO - Status {r.status_code}: {r.text[:150]}")

print()
print("=" * 70)
print("TEST DEL SITIO")
print("=" * 70)
for nombre, token in tokens.items():
    if not token:
        continue
    print(f"\n[{nombre}] Consultando sitio {site_id}...")
    r = requests.get(
        f"https://api.netlify.com/api/v1/sites/{site_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    if r.status_code == 200:
        data = r.json()
        print(f"  OK - Nombre: {data.get('name')}")
        print(f"  OK - URL:    {data.get('url')}")
        print(f"  OK - SSL:    {data.get('ssl_url')}")
    else:
        print(f"  FALLO - Status {r.status_code}: {r.text[:150]}")
print("=" * 70)
