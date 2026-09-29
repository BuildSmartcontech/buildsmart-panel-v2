import os, requests, json
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("CLOUDFLARE_TOKEN", "")
account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
project = os.getenv("CLOUDFLARE_PROJECT_NAME", "buildsmart-webs")

url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project}/deployments"

r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=15)

print("=" * 70)
print("ULTIMOS DEPLOYMENTS EN CLOUDFLARE")
print("=" * 70)

if r.status_code != 200:
    print(f"ERROR {r.status_code}: {r.text[:300]}")
else:
    deployments = r.json().get("result", [])
    print(f"Total: {len(deployments)}\n")

    for d in deployments[:3]:
        stage = d.get("latest_stage", {})
        print(f"URL: {d.get('url', '?')}")
        print(f"  Branch: {d.get('environment', '?')}")
        print(f"  Created: {d.get('created_on', '?')}")
        print(f"  Stage: {stage.get('name', '?')} - {stage.get('status', '?')}")
        print()

    # Files del ultimo deploy
    if deployments:
        ultimo = deployments[0]
        d_id = ultimo.get("id")
        print(f"=== Archivos del ultimo deploy ({d_id}) ===")

        url_files = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project}/deployments/{d_id}/history/logs"
        rf = requests.get(url_files, headers={"Authorization": f"Bearer {token}"}, timeout=15)
        if rf.status_code == 200:
            data = rf.json().get("result", [])
            for log in data[-5:]:
                print(f"  {log.get('message', '?')}")
print("=" * 70)
