import os, hashlib, json, requests
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("NETLIFY_TOKEN", "")
site_id = os.getenv("NETLIFY_SITE_ID", "")

print("=" * 70)
print("DIAGNOSTICO NETLIFY - POST /deploys")
print("=" * 70)

# 1. Ver el token con repr (detecta caracteres ocultos)
print(f"\n1. Token (repr): {repr(token[:30])}...")
print(f"   Token len:    {len(token)}")
print(f"   Site ID:      {site_id}")

# 2. GET /user (verificacion)
r0 = requests.get("https://api.netlify.com/api/v1/user",
                  headers={"Authorization": f"Bearer {token}"}, timeout=15)
print(f"\n2. GET /user:  HTTP {r0.status_code}")
if r0.status_code == 200:
    print(f"   Email: {r0.json().get('email')}")

# 3. GET /sites/{site_id} (verificar acceso al sitio)
r1 = requests.get(f"https://api.netlify.com/api/v1/sites/{site_id}",
                  headers={"Authorization": f"Bearer {token}"}, timeout=15)
print(f"\n3. GET /sites/{{site_id}}: HTTP {r1.status_code}")
if r1.status_code == 200:
    d = r1.json()
    print(f"   Nombre: {d.get('name')}")
    print(f"   URL:    {d.get('url')}")

# 4. POST /sites/{site_id}/deploys (el que falla)
html = "<html><body>test</body></html>"
sha1 = hashlib.sha1(html.encode()).hexdigest()
payload = {"files": {"/test_debug.html": sha1}}

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}
print(f"\n4. POST /sites/{{site_id}}/deploys")
print(f"   Payload: {json.dumps(payload)}")
r2 = requests.post(f"https://api.netlify.com/api/v1/sites/{site_id}/deploys",
                   headers=headers, json=payload, timeout=15)
print(f"   HTTP: {r2.status_code}")
print(f"   Respuesta: {r2.text[:400]}")

# 5. Probar con URL alternativa (sin trailing)
site_id_clean = site_id.strip()
if site_id_clean != site_id:
    print(f"\n5. Diferencia en site_id: len={len(site_id)} vs {len(site_id_clean)}")

print("=" * 70)
