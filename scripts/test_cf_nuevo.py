import requests

token = "cfut_wEPGX5unEbwc08lHLDvn3CIG8y1gBDVdBReIwb0Me22bb616"
account_id = "a199b1f3b7be3a3b814502c3aa717719"

print("=" * 60)
print("TEST CLOUDFLARE - TOKEN NUEVO")
print("=" * 60)

# 1. Verify token
r = requests.get(
    "https://api.cloudflare.com/client/v4/user/tokens/verify",
    headers={"Authorization": f"Bearer {token}"},
    timeout=10,
)
print(f"[1] Verify: {r.status_code}")

# 2. List accounts
r = requests.get(
    "https://api.cloudflare.com/client/v4/accounts",
    headers={"Authorization": f"Bearer {token}"},
    timeout=10,
)
print(f"[2] Accounts: {r.status_code}")
if r.status_code == 200:
    for c in r.json().get("result", []):
        print(f"    - {c.get('name')} ({c.get('id')})")

# 3. List/create pages project
r = requests.get(
    f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects",
    headers={"Authorization": f"Bearer {token}"},
    timeout=10,
)
print(f"[3] Pages projects: {r.status_code}")
if r.status_code == 200:
    for p in r.json().get("result", []):
        print(f"    - {p.get('name')}")
elif r.status_code == 403:
    print(f"    ERROR 403: {r.json().get('errors', [])}")

print("=" * 60)
