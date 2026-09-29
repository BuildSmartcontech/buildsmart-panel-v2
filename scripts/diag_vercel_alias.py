import os, base64, json, requests
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("VERCEL_TOKEN", "")
api = "https://api.vercel.com"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# 1. Listar los ultimos deployments
print("=" * 70)
print("ULTIMOS DEPLOYMENTS EN VERCEL")
print("=" * 70)

r = requests.get(f"{api}/v6/deployments?limit=3", headers=headers, timeout=15)
if r.status_code != 200:
    print(f"ERROR {r.status_code}: {r.text[:300]}")
    exit(1)

deployments = r.json().get("deployments", [])
for d in deployments:
    print(f"\nID:      {d.get('uid')}")
    print(f"  Name:    {d.get('name')}")
    print(f"  URL:     {d.get('url')}")
    print(f"  Target:  {d.get('target')}")
    print(f"  Aliases: {d.get('alias', [])}")   # CLAVE: URLs estables
    print(f"  Created: {d.get('created')}")

# 2. Ver detalle del ultimo para saber su alias estable
if deployments:
    d = deployments[0]
    uid = d.get("uid")
    print("\n" + "=" * 70)
    print(f"DETALLE DEPLOY {uid}")
    print("=" * 70)

    r2 = requests.get(f"{api}/v13/deployments/{uid}", headers=headers, timeout=15)
    if r2.status_code == 200:
        info = r2.json()
        print(f"Name:      {info.get('name')}")
        print(f"URL corta: {info.get('url')}")
        print(f"Alias:     {info.get('alias', [])}")
        print(f"Alias final: {info.get('aliasAssigned')}")
        print(f"Target:    {info.get('target')}")
        # Listar todos los campos top-level para ver que hay
        print(f"\nTodos los campos disponibles:")
        for k in sorted(info.keys()):
            v = info[k]
            if isinstance(v, (str, int, bool, type(None))):
                print(f"  {k}: {str(v)[:80]}")
print("=" * 70)
