import os
from dotenv import load_dotenv
load_dotenv()

sb_url = os.getenv("SUPABASE_URL", "")
sb_key = os.getenv("SUPABASE_KEY", "")
sb_anon = os.getenv("SUPABASE_ANON_KEY", "")

print("=" * 60)
print("VERIFICACION KEYS")
print("=" * 60)
print(f"SUPABASE_URL:          {'OK' if sb_url else 'FALTA'}")
print(f"SUPABASE_KEY (secret): {'OK' if sb_key else 'FALTA'}")
print(f"  Prefijo: {sb_key[:20]}..." if sb_key else "  (vacio)")
print(f"SUPABASE_ANON_KEY:     {'OK' if sb_anon else 'FALTA'}")
print(f"  Prefijo: {sb_anon[:25]}..." if sb_anon else "  (vacio)")
print()

if sb_key and sb_anon:
    if sb_key == sb_anon:
        print("ERROR: Las keys son IGUALES")
        print("       SUPABASE_KEY deberia ser secret/sb_secret_")
        print("       SUPABASE_ANON_KEY deberia ser publishable/sb_publishable_")
    else:
        print("OK: Las 2 keys son diferentes")
print("=" * 60)
