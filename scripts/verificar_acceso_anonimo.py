import requests

url = "https://buildsmart-samu.netlify.app/pedido_c8c1f3c3/b406912c-e176-4786-85c9-76d225d4a13e/"

print("=" * 70)
print("VERIFICAR ACCESO ANONIMO AL SITIO")
print("=" * 70)

r = requests.get(url, timeout=15)
print(f"URL: {url}")
print(f"Status: {r.status_code}")
print(f"Content-Type: {r.headers.get('content-type', '?')}")

if r.status_code == 200:
    print(f"\n  [OK] Sitio PUBLICO - carga sin login")
    print(f"  Tamano: {len(r.text)} bytes")
    if "Los Tres Amigos" in r.text:
        print(f"  [OK] Contenido correcto: 'Los Tres Amigos' detectado")
elif r.status_code == 401:
    print(f"\n  [FAIL] Sitio PRIVADO - sigue pidiendo login")
else:
    print(f"\n  [WARN] Status inesperado: {r.status_code}")

r2 = requests.get("https://buildsmart-samu.netlify.app/", timeout=15)
print(f"\nRoot del sitio: {r2.status_code}")
print("=" * 70)
