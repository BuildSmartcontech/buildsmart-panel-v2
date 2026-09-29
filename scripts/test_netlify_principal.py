import os, requests
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("NETLIFY_TOKEN", "")
print("=" * 60)
print("TEST CUENTA PRINCIPAL NETLIFY")
print("=" * 60)

r = requests.get(
    "https://api.netlify.com/api/v1/user",
    headers={"Authorization": f"Bearer {token}"},
    timeout=10,
)

if r.status_code == 200:
    data = r.json()
    print(f"Email: {data.get('email', '?')}")
    print(f"Nombre: {data.get('full_name', '?')}")
    print(f"Status: OK")
else:
    print(f"ERROR: {r.status_code} - {r.text[:200]}")
print("=" * 60)
