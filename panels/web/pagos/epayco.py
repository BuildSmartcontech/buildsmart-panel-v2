# panels/web/pagos/epayco.py
# ============================================
# PROVEEDOR DE PAGOS EPAYCO - V2.0
# ============================================

import os
import streamlit as st
from panels.web.pagos.base import ProveedorPago

class EpaycoProveedor(ProveedorPago):
    nombre = "epayco"
    soporta_suscripciones = False
    usa_webhooks = True

    def __init__(self, datos_pago=None):
        try:
            self.public_key = st.secrets.get("EPAYCO_PUBLIC_KEY", os.getenv("EPAYCO_PUBLIC_KEY"))
            self.private_key = st.secrets.get("EPAYCO_PRIVATE_KEY", os.getenv("EPAYCO_PRIVATE_KEY"))
            self.test_mode = st.secrets.get("EPAYCO_TEST_MODE", "true").lower() == "true"
        except Exception:
            self.public_key = os.getenv("EPAYCO_PUBLIC_KEY")
            self.private_key = os.getenv("EPAYCO_PRIVATE_KEY")
            self.test_mode = os.getenv("EPAYCO_TEST_MODE", "true").lower() == "true"

        if not self.public_key or not self.private_key:
            print("[EPAYCO] Faltan llaves de configuración en Secrets.")
            self.disponible = False
        else:
            self.disponible = True

    def crear_pago(self, pedido_id, monto, descripcion, metadata=None):
        if not self.disponible:
            return {
                "exito": False,
                "error": "Pasarela ePayco no configurada. Usa pago manual.",
                "url_pago": None
            }

        # Extraemos el token del cliente para que ePayco nos lo devuelva en la URL
        token = metadata.get("token", "") if metadata else ""
        
        # URL a la que ePayco devolverá al usuario después de pagar
        # Incluimos el token y los parámetros para que el panel sepa qué actualizar
        base_response = "https://samu-ia.streamlit.app/?web=panel"
        
        response_url = f"{base_response}&token={token}&pago=exitoso&id_pago={pedido_id}"
        
        # Construimos el link de pago de ePayco (Split/Checkout)
        url_pago = (
            f"https://checkout.epayco.co/checkout.php"
            f"?public_key={self.public_key}"
            f"&invoice={pedido_id}"
            f"&amount={monto}"
            f"&currency=USD"
            f"&description={descripcion}"
            f"&response={response_url}"
            f"&confirmation=https://samu-ia.streamlit.app/api/webhook_epayco"
        )

        return {
            "exito": True,
            "pago_id": f"epayco_{pedido_id}",
            "estado": "pendiente_pago_epayco",
            "url_pago": url_pago,
            "instrucciones": f"Serás redirigido a ePayco para completar el pago de USD {monto}.",
            "error": None
        }