import os, requests
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("NETLIFY_TOKEN", "")

print("=" * 70)
print("SITIOS EN LA CUENTA NETLIFY (samupor527)")
print("=" * 70)

r = requests.get(
    "https://api.netlify.com/api/v1/sites",
    headers={"Authorization": f"Bearer {token}"},
    timeout=15,
)

if r.status_code != 200:
    print(f"ERROR {r.status_code}: {r.text[:200]}")
else:
    sites = r.json()
    print(f"Total: {len(sites)} sitios\n")
    for s in sites:
        print(f"Nombre: {s.get('name')}")
        print(f"  Site ID: {s.get('id')}")
        print(f"  URL:     {s.get('url')}")
        print(f"  SSL:     {s.get('ssl_url')}")
        print()
print("=" * 70)
