import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import os
from dotenv import load_dotenv
load_dotenv()

# Limpiar cache de env vars
os.environ.pop("EMAIL_USER", None)
os.environ.pop("EMAIL_PASSWORD", None)
load_dotenv(override=True)

print("=" * 60)
print("VERIFICACION POST-FIX")
print("=" * 60)
print(f"RESEND_API_KEY: {'SI' if os.getenv('RESEND_API_KEY') else 'NO'}")
print(f"EMAIL_USER (Gmail): {'SI - QUEDO ACTIVO' if os.getenv('EMAIL_USER') else 'NO - OK'}")
print(f"EMAIL_PASSWORD (Gmail): {'SI - QUEDO ACTIVO' if os.getenv('EMAIL_PASSWORD') else 'NO - OK'}")
print()

from utils.email_sender import email_sender
print(f"Motor activo: {email_sender.motor_activo}")
print(f"Disponible: {email_sender.disponible}")
print()
if email_sender.motor_activo == "resend":
    print("OK: Solo Resend activo")
else:
    print(f"AVISO: Motor es '{email_sender.motor_activo}' - revisar .env")
print("=" * 60)
