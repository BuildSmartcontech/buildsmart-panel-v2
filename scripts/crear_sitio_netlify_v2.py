import os, requests, json
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("NETLIFY_TOKEN", "")

# Nombres a intentar (por si alguno esta tomado)
nombres = ["buildsmart-samu", "buildsmart-ia", "samu-webs", "samu-ia-webs"]

print("=" * 70)
print("CREAR SITIO NETLIFY")
print("=" * 70)

for nombre in nombres:
    print(f"\nIntentando: {nombre}...")
    r = requests.post(
        "https://api.netlify.com/api/v1/sites",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"name": nombre},
        timeout=20,
    )

    if r.status_code in (200, 201):
        data = r.json()
        print(f"\n  OK - Sitio creado")
        print(f"  Site ID: {data.get('id')}")
        print(f"  Nombre:  {data.get('name')}")
        print(f"  URL:     {data.get('url')}")
        print(f"  SSL:     {data.get('ssl_url')}")
        print()
        print("  COPIA ESTO EN EL .env:")
        print(f"  NETLIFY_SITE_ID={data.get('id')}")
        break
    else:
        print(f"  FALLO {r.status_code}: {r.text[:150]}")

print("=" * 70)
