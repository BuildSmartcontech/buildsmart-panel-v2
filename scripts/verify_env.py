import os
from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print("VERIFICACION .env NETLIFY")
print("=" * 70)

for var in ["NETLIFY_TOKEN", "NETLIFY_API_KEY", "NETLIFY_SITE_ID", "NETLIFY_SITE_URL"]:
    val = os.getenv(var, "")
    if val:
        print(f"  {var:20} = {val[:20]}...{val[-6:]}")
    else:
        print(f"  {var:20} = (VACIO)")

print()
print("Esperado:")
print("  NETLIFY_TOKEN    = nfp_...  (OK)")
print("  NETLIFY_API_KEY  = (VACIO)")
print("  NETLIFY_SITE_ID  = c55778ca-...")
print("  NETLIFY_SITE_URL = (VACIO)")
print("=" * 70)
