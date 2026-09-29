import requests

token = "cfut_S0O4lrmJAVIWUWKIPd2cDNrAQrb7CuVgN2aqdZTS4acf0b5a"

print("=" * 60)
print("CUENTAS CLOUDFLARE DISPONIBLES")
print("=" * 60)

r = requests.get(
    "https://api.cloudflare.com/client/v4/accounts",
    headers={"Authorization": f"Bearer {token}"},
    timeout=10,
)

if r.status_code == 200:
    cuentas = r.json().get("result", [])
    if not cuentas:
        print("El token no tiene permisos para listar cuentas.")
        print("Necesitas crear un token nuevo con los permisos correctos.")
    else:
        for c in cuentas:
            print(f"Account ID: {c.get('id')}")
            print(f"  Nombre: {c.get('name')}")
else:
    print(f"Error: {r.status_code}")
    print(r.text[:300])
print("=" * 60)
