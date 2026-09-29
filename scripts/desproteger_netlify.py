import os, json, requests
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("NETLIFY_TOKEN", "")
site_id = os.getenv("NETLIFY_SITE_ID", "")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

print("=" * 70)
print("ESTADO ACTUAL DEL SITIO NETLIFY")
print("=" * 70)

# 1. Info del sitio
r = requests.get(f"https://api.netlify.com/api/v1/sites/{site_id}",
                 headers=headers, timeout=15)
if r.status_code != 200:
    print(f"ERROR {r.status_code}: {r.text[:300]}")
    exit(1)

data = r.json()
print(f"Nombre:         {data.get('name')}")
print(f"URL:            {data.get('url')}")
print(f"SSL URL:        {data.get('ssl_url')}")
print(f"State:          {data.get('state')}")
print(f"Password:       {data.get('password')}")
print(f"Published:      {data.get('published_deploy', {}).get('id')}")
print(f"Account slug:   {data.get('account_slug')}")
print(f"Account name:   {data.get('account_name')}")

# 2. Verificar usuario de la cuenta
print()
print("=" * 70)
print("CUENTA DEL TOKEN")
print("=" * 70)
ru = requests.get("https://api.netlify.com/api/v1/user",
                  headers=headers, timeout=15)
if ru.status_code == 200:
    user = ru.json()
    print(f"Email:          {user.get('email')}")
    print(f"Nombre:         {user.get('full_name')}")
    print(f"ID:             {user.get('id')}")

# 3. Desproteger el sitio
print()
print("=" * 70)
print("QUITANDO PASSWORD PROTECTION")
print("=" * 70)

r2 = requests.patch(
    f"https://api.netlify.com/api/v1/sites/{site_id}",
    headers=headers,
    json={"password": None},
    timeout=15,
)
print(f"PATCH password=null: HTTP {r2.status_code}")
if r2.status_code == 200:
    print(f"  Nuevo password: {r2.json().get('password')}")
    print(f"  Nuevo state:    {r2.json().get('state')}")
else:
    print(f"  ERROR: {r2.text[:300]}")

# 4. Intentar tambien con string vacio
if r2.status_code != 200 or r2.json().get("password"):
    r3 = requests.patch(
        f"https://api.netlify.com/api/v1/sites/{site_id}",
        headers=headers,
        json={"password": ""},
        timeout=15,
    )
    print(f"\nPATCH password='': HTTP {r3.status_code}")
    if r3.status_code == 200:
        print(f"  Nuevo password: {r3.json().get('password')}")

# 5. Verificar
print()
print("=" * 70)
print("VERIFICACION FINAL")
print("=" * 70)
rv = requests.get(f"https://api.netlify.com/api/v1/sites/{site_id}",
                  headers=headers, timeout=15)
if rv.status_code == 200:
    v = rv.json()
    pwd = v.get("password")
    state = v.get("state")
    print(f"Password:       {pwd}")
    print(f"State:          {state}")
    if not pwd:
        print("\n  ✅ Password protection DESACTIVADA")
    else:
        print("\n  ❌ Password protection SIGUE ACTIVA")
print("=" * 70)
