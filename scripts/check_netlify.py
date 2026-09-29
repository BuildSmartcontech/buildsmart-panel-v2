import os, requests
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("NETLIFY_TOKEN", "")
print(f"Token prefijo: {token[:20]}...")

r = requests.get(
    "https://api.netlify.com/api/v1/user",
    headers={"Authorization": f"Bearer {token}"},
    timeout=10,
)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    print(f"Email: {r.json().get('email')}")
else:
    print(f"ERROR: {r.text[:200]}")
