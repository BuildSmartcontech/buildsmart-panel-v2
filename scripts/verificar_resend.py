import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("RESEND_API_KEY", "")
email = os.getenv("RESEND_FROM_EMAIL", "")
nombre = os.getenv("RESEND_FROM_NAME", "")

print("=" * 60)
print("VERIFICACION RESEND")
print("=" * 60)
print(f"API Key: {'OK' if key.startswith('re_') else 'FALTA o INCORRECTA'}")
print(f"  Prefijo: {key[:15]}..." if key else "  (vacio)")
print(f"From email: {email or '(vacio)'}")
print(f"From name: {nombre or '(vacio)'}")
print("=" * 60)
