import os, json, hashlib, requests
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("CLOUDFLARE_TOKEN", "")
account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
project = os.getenv("CLOUDFLARE_PROJECT_NAME", "buildsmart-webs")

print("=" * 70)
print("VERIFICAR DEPLOY EN CLOUDFLARE")
print("=" * 70)

# Listar deployments
url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project}/deployments"
r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=15)

if r.status_code != 200:
    print(f"ERROR: {r.status_code}")
    print(r.text[:300])
else:
    deployments = r.json().get("result", [])
    if not deployments:
        print("Sin deployments")
    else:
        d = deployments[0]
        print(f"Ultimo deploy ID: {d.get('id')}")
        print(f"URL:              {d.get('url')}")
        print(f"Environment:      {d.get('environment', '?')}")
        print(f"Stage:            {d.get('latest_stage', {}).get('name', '?')} - {d.get('latest_stage', {}).get('status', '?')}")

        # Consultar archivos del deploy
        files_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project}/deployments/{d.get('id')}"
        rf = requests.get(files_url, headers={"Authorization": f"Bearer {token}"}, timeout=15)
        if rf.status_code == 200:
            info = rf.json().get("result", {})
            files = info.get("files", [])
            print(f"\nArchivos en el deploy: {len(files)}")
            for f in files[:5]:
                print(f"  - {f}")
            if len(files) > 5:
                print(f"  ... y {len(files) - 5} mas")
print("=" * 70)
