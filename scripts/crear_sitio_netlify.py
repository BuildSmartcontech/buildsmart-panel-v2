import os, requests, json
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("NETLIFY_TOKEN", "")

print("=" * 70)
print("CREAR SITIO NETLIFY")
print("=" * 70)

payload = {"name": "buildsmart-webs"}

r = requests.post(
    "https://api.netlify.com/api/v1/sites",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json=payload,
    timeout=20,
)

if r.status_code not in (200, 201):
    print(f"ERROR {r.status_code}: {r.text[:300]}")
else:
    data = r.json()
    print(f"OK - Sitio creado")
    print(f"  Site ID: {data.get('id')}")
    print(f"  Nombre:  {data.get('name')}")
    print(f"  URL:     {data.get('url')}")
    print(f"  SSL:     {data.get('ssl_url')}")
    print()
    print("COPIA ESTE SITE_ID (lo usamos en el paso 2):")
    print(f"  NETLIFY_SITE_ID={data.get('id')}")
print("=" * 70)
