import sys
from pathlib import Path

# Bootstrap de path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import os
from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("DIAGNOSTICO EMAIL")
print("=" * 60)
print(f"RESEND_API_KEY: {'SI' if os.getenv('RESEND_API_KEY') else 'NO'}")
print(f"EMAIL_USER (Gmail): {'SI' if os.getenv('EMAIL_USER') else 'NO'}")
print(f"EMAIL_PASSWORD (Gmail): {'SI' if os.getenv('EMAIL_PASSWORD') else 'NO'}")
print()

from utils.email_sender import email_sender
print(f"Motor activo: {email_sender.motor_activo}")
print(f"Disponible: {email_sender.disponible}")

# Test de envio
print()
print("=" * 60)
print("TEST DE ENVIO (a tu email)")
print("=" * 60)
resultado = email_sender.enviar_correo(
    "antonioempresarial9@gmail.com",
    "Test diagnostico SAMU IA",
    "Este email es una prueba para saber que motor se usa."
)
print(f"Resultado: {resultado}")
print("=" * 60)
