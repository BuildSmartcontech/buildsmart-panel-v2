import os, requests
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("GROQ_API_KEY", "")
r = requests.get(
    "https://api.groq.com/openai/v1/models",
    headers={"Authorization": f"Bearer {key}"},
    timeout=10,
)
models = [m["id"] for m in r.json().get("data", [])]

print("=" * 70)
print(f"MODELOS GROQ DISPONIBLES ({len(models)})")
print("=" * 70)
for m in sorted(models):
    print(f"  {m}")
print("=" * 70)
