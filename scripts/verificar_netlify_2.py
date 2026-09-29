import os
from dotenv import load_dotenv
load_dotenv()

t_main = os.getenv("NETLIFY_TOKEN", "")
t_back = os.getenv("NETLIFY_TOKEN_BACKUP", "")

print("=" * 60)
print("NETLIFY - 2 CUENTAS")
print("=" * 60)
print(f"Principal: {'OK' if t_main.startswith('nfp_') else 'FALTA'} ({t_main[:20]}...)")
print(f"Respaldo:  {'OK' if t_back.startswith('nfp_') else 'FALTA'} ({t_back[:20]}...)")
print()

if t_main and t_back and t_main != t_back:
    print("OK: 2 tokens diferentes listos")
elif not t_back:
    print("AVISO: Falta el token de respaldo")
else:
    print("ERROR: Tokens iguales")
print("=" * 60)
