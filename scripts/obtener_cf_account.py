import requests

token = "cfut_v9LJAlxfDBVfFzcPvq6t34k4eDHZB0GLjfTJ7i6gb6589343"

print("=" * 60)
print("CUENTAS CLOUDFLARE DISPONIBLES")
print("=" * 60)

r = requests.get(
    "https://api.cloudflare.com/client/v4/accounts",
    headers={"Authorization": f"Bearer {token}"},
    timeout=10,
)

print(f"Status: {r.status_code}")
print()

if r.status_code == 200:
    data = r.json()
    cuentas = data.get("result", [])
    if not cuentas:
        print("No hay cuentas accesibles con este token.")
        print("El token necesita permisos de Account.")
    else:
        for c in cuentas:
            print(f"Account ID: {c.get('id')}")
            print(f"  Nombre: {c.get('name')}")
            print()
else:
    print(f"Error: {r.text[:400]}")
print("=" * 60)
