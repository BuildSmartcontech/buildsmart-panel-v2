import os
from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("DIAGNOSTICO EMAIL")
print("=" * 60)
print(f"RESEND_API_KEY configurada: {'SI' if os.getenv('RESEND_API_KEY') else 'NO'}")
print(f"EMAIL_USER (Gmail) configurado: {'SI' if os.getenv('EMAIL_USER') else 'NO'}")
print(f"EMAIL_PASSWORD configurado: {'SI' if os.getenv('EMAIL_PASSWORD') else 'NO'}")
print()

# Verificar email_sender actual
from utils.email_sender import email_sender
print(f"Motor activo: {email_sender.motor_activo}")
print(f"Disponible: {email_sender.disponible}")
print("=" * 60)
