import os, json, base64, hashlib, requests
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

try:
    import blake3 as _blake3
except ImportError:
    print("FALTA: pip install blake3")
    exit(1)

token = os.getenv("CLOUDFLARE_TOKEN", "")
account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
project = os.getenv("CLOUDFLARE_PROJECT_NAME", "buildsmart-webs")
headers = {"Authorization": f"Bearer {token}"}

print("=" * 70)
print("TEST API NUEVA CLOUDFLARE (Wrangler-style)")
print("=" * 70)

# 1. Pedir JWT de upload
url_jwt = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project}/upload-token"
r = requests.get(url_jwt, headers=headers, timeout=15)
print(f"\n1. Upload-token: HTTP {r.status_code}")
if r.status_code != 200:
    print(f"   ERROR: {r.text[:300]}")
    exit(1)
jwt = r.json().get("result", {}).get("jwt", "")
if not jwt:
    print(f"   No hay JWT. Respuesta completa:")
    print(json.dumps(r.json(), indent=2)[:500])
    exit(1)
print(f"   JWT OK: {jwt[:30]}...")

# 2. Preparar un archivo de prueba
usuario_id = "pedido_c8c1f3c3"
web_id = "b406912c-e176-4786-85c9-76d225d4a13e"
ruta = Path("data/webs_generadas") / usuario_id / web_id / "index.html"
if not ruta.exists():
    print(f"\n   No existe: {ruta}")
    exit(1)

content = ruta.read_bytes()
ext = "html"
b64 = base64.b64encode(content).decode("ascii")
h = _blake3.blake3((b64 + ext).encode("ascii")).hexdigest()[:32]
print(f"\n2. Archivo: {ruta.name} ({len(content)} bytes)")
print(f"   Hash BLAKE3: {h}")

# 3. Subir asset con la API nueva
url_upload = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/assets/upload"
payload = [{
    "key": h,
    "value": base64.b64encode(content).decode("ascii"),
    "metadata": {"contentType": "text/html"},
    "base64": True,
}]
r2 = requests.post(
    url_upload,
    headers={"Authorization": f"Bearer {jwt}", "Content-Type": "application/json"},
    json=payload,
    timeout=30,
)
print(f"\n3. Upload asset: HTTP {r2.status_code}")
print(f"   Respuesta: {r2.text[:300]}")
print("=" * 70)
