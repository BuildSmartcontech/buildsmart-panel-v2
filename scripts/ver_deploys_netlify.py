import os, json, requests
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("NETLIFY_TOKEN", "")
site_id = os.getenv("NETLIFY_SITE_ID", "")
headers = {"Authorization": f"Bearer {token}"}

print("=" * 70)
print("DEPLOYS DE NETLIFY")
print("=" * 70)

r = requests.get(
    f"https://api.netlify.com/api/v1/sites/{site_id}/deploys?per_page=3",
    headers=headers, timeout=15,
)
if r.status_code == 200:
    deploys = r.json()
    print(f"Total recientes: {len(deploys)}\n")
    for d in deploys:
        print(f"ID:      {d.get('id')}")
        print(f"  URL:     {d.get('url')}")
        print(f"  State:   {d.get('state')}")
        print(f"  Branch:  {d.get('branch')}")
        print(f"  Created: {d.get('created_at')}")
        print(f"  Deploy URL: {d.get('deploy_ssl_url')}")
        print()
else:
    print(f"ERROR {r.status_code}: {r.text[:300]}")

print("=" * 70)
print("URLs PUBLICAS PARA PROBAR")
print("=" * 70)
print()
print("URL con path (lo que generamos):")
print("https://buildsmart-samu.netlify.app/pedido_c8c1f3c3/b406912c-e176-4786-85c9-76d225d4a13e/")
print()
print("URL de la raiz del sitio:")
print("https://buildsmart-samu.netlify.app/")
print()
print("URL con /index.html explicito:")
print("https://buildsmart-samu.netlify.app/pedido_c8c1f3c3/b406912c-e176-4786-85c9-76d225d4a13e/index.html")
print("=" * 70)
