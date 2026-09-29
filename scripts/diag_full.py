import os
from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print("DIAGNOSTICO .env")
print("=" * 70)

vars_netlify = ["NETLIFY_TOKEN", "NETLIFY_API_KEY", "NETLIFY_SITE_ID", "NETLIFY_SITE_URL"]
for v in vars_netlify:
    val = os.getenv(v, "")
    if val:
        print(f"{v:25} = {val[:12]}...{val[-6:]}  (len={len(val)})")
    else:
        print(f"{v:25} = (VACIO)")

print()
vars_cf = ["CLOUDFLARE_TOKEN", "CLOUDFLARE_ACCOUNT_ID", "CLOUDFLARE_PROJECT_NAME"]
for v in vars_cf:
    val = os.getenv(v, "")
    if val:
        print(f"{v:25} = {val[:12]}...{val[-6:]}  (len={len(val)})")
    else:
        print(f"{v:25} = (VACIO)")

print()
print("=" * 70)
print("ESTRUCTURA data/webs_generadas")
print("=" * 70)
from pathlib import Path
raiz = Path("data/webs_generadas")
if raiz.exists():
    niveles = {}
    for f in raiz.rglob("index.html"):
        rel = f.relative_to(raiz).as_posix()
        partes = rel.split("/")
        if len(partes) >= 2:
            tipo = "UUID/UUID (viejo)" if len(partes[0]) == 36 else "pedido_XXX/UUID (nuevo)"
            niveles[tipo] = niveles.get(tipo, 0) + 1
    for k, v in niveles.items():
        print(f"  {k}: {v} webs")

    print()
    print("  Primeras 5 webs:")
    for f in list(raiz.rglob("index.html"))[:5]:
        print(f"    {f.relative_to(raiz).as_posix()}")
else:
    print(f"  NO EXISTE: {raiz}")
print("=" * 70)
