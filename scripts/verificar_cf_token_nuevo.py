import requests

token = "cfut_S0O4lrmJAVIWUWKIPd2cDNrAQrb7CuVgN2aqdZTS4acf0b5a"

print("=" * 60)
print("VERIFICACION CLOUDFLARE TOKEN (NUEVO)")
print("=" * 60)

r = requests.get(
    "https://api.cloudflare.com/client/v4/user/tokens/verify",
    headers={"Authorization": f"Bearer {token}"},
    timeout=10,
)

print(f"Status: {r.status_code}")
print(f"Respuesta: {r.text[:400]}")
print("=" * 60)

if r.status_code == 200:
    data = r.json()
    if data.get("success"):
        print("OK: Token valido y activo")
    else:
        print("ERROR: Token no activo")
