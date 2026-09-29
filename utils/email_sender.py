# utils/email_sender.py
# ============================================
# ENVIO DE EMAILS - SAMU IA
# ============================================
# V2.0: Resend como motor principal + fallback SMTP
# V1.0: SMTP con Gmail (version anterior)
#
# Interfaz compatible con version anterior:
#   email_sender.enviar_correo(destino, asunto, contenido)
# ============================================

import os
from dotenv import load_dotenv

load_dotenv()


# ==========================================
# RESEND (motor principal)
# ==========================================
def _enviar_resend(destino, asunto, contenido):
    """
    Envia email usando Resend API.
    Returns: (exito: bool, mensaje: str)
    """
    try:
        import resend
    except ImportError:
        return False, "SDK resend no instalado (pip install resend)"

    api_key = os.getenv("RESEND_API_KEY", "")
    if not api_key or not api_key.startswith("re_"):
        return False, "RESEND_API_KEY no configurada"

    from_email = os.getenv("RESEND_FROM_EMAIL", "onboarding@resend.dev")
    from_name = os.getenv("RESEND_FROM_NAME", "SAMU IA")

    resend.api_key = api_key

    try:
        params = {
            "from": f"{from_name} <{from_email}>",
            "to": [destino],
            "subject": asunto,
            "text": contenido,
        }
        result = resend.Emails.send(params)

        # Resend puede devolver dict con id o error
        if isinstance(result, dict):
            if result.get("error"):
                return False, f"Resend error: {result['error']}"
            return True, f"Email enviado via Resend (id: {result.get('id', '?')})"

        return True, "Email enviado via Resend"

    except Exception as e:
        return False, f"Resend excepcion: {str(e)[:200]}"


# ==========================================
# SMTP (fallback legacy)
# ==========================================
def _enviar_smtp(destino, asunto, contenido):
    """
    Envia email via SMTP (Gmail u otro).
    Se usa como fallback si Resend falla.
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.header import Header

    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    try:
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
    except ValueError:
        smtp_port = 587

    email_user = os.getenv("EMAIL_USER", "")
    email_pass = os.getenv("EMAIL_PASSWORD", "")

    if not email_user or not email_pass:
        return False, "SMTP no configurado (falta EMAIL_USER o EMAIL_PASSWORD)"

    try:
        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = destino
        msg["Subject"] = Header(asunto, "utf-8").encode()
        msg.attach(MIMEText(contenido, "plain", "utf-8"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)
        server.quit()

        return True, "Email enviado via SMTP"

    except Exception as e:
        return False, f"SMTP error: {str(e)[:200]}"


# ==========================================
# CLASE PRINCIPAL
# ==========================================
class EmailSender:
    """
    Cliente de envio de emails.

    Prioridad:
    1. Resend (si RESEND_API_KEY esta configurada)
    2. SMTP (si EMAIL_USER y EMAIL_PASSWORD estan configurados)
    """

    def __init__(self):
        self.resend_key = os.getenv("RESEND_API_KEY", "")
        self.smtp_user = os.getenv("EMAIL_USER", "")
        self.smtp_pass = os.getenv("EMAIL_PASSWORD", "")

    @property
    def disponible(self):
        """True si al menos un motor esta configurado."""
        return bool(self.resend_key or (self.smtp_user and self.smtp_pass))

    @property
    def motor_activo(self):
        """Nombre del motor activo."""
        if self.resend_key and self.resend_key.startswith("re_"):
            return "resend"
        if self.smtp_user and self.smtp_pass:
            return "smtp"
        return "ninguno"

    def enviar_correo(self, destino, asunto, contenido):
        """
        Envia un email. Interfaz compatible con version anterior.

        Args:
            destino (str): Email del destinatario
            asunto (str): Asunto del email
            contenido (str): Cuerpo del email (texto plano)

        Returns:
            str: Mensaje con el resultado
        """
        if not destino or "@" not in destino:
            return "ERROR: Email destino invalido"

        if not self.disponible:
            return "ERROR: Ningun motor de email configurado (.env)"

        # Intento 1: Resend
        if self.motor_activo == "resend":
            exito, msg = _enviar_resend(destino, asunto, contenido)
            if exito:
                return f"OK: {msg}"
            print(f"[email_sender] Resend fallo: {msg}. Intentando SMTP...")

        # Intento 2: SMTP (fallback o principal si no hay Resend)
        if self.smtp_user and self.smtp_pass:
            exito, msg = _enviar_smtp(destino, asunto, contenido)
            if exito:
                return f"OK: {msg}"
            return f"ERROR: {msg}"

        return "ERROR: No hay fallback disponible"


# ==========================================
# SINGLETON (compatible con version anterior)
# ==========================================
email_sender = EmailSender()


# ==========================================
# TEST MANUAL
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print("TEST EMAIL SENDER V2.0")
    print("=" * 60)
    print(f"Disponible: {email_sender.disponible}")
    print(f"Motor activo: {email_sender.motor_activo}")
    print()

    # Test de validacion (no envia)
    r = email_sender.enviar_correo("invalido", "Test", "Test")
    print(f"Validacion destino invalido: {r}")
    print()

    print("Para probar envio real, ejecutar:")
    print('  python -c "from utils.email_sender import email_sender; ')
    print('             print(email_sender.enviar_correo(\'tu@email.com\', \'Test SAMU IA\', \'Hola desde SAMU IA\'))"')
    print("=" * 60)