# panels/web/pagos/epayco.py
# ============================================
# PROVEEDOR DE PAGOS EPAYCO
# ============================================

import os
import requests
import streamlit as st
from panels.web.pagos.base import ProveedorPago

class EpaycoProveedor(ProveedorPago):
    nombre = "epayco"
    soporta_suscripciones = False
    usa_webhooks = True

    def __init__(self, datos_pago=None):
        # Cargar llaves desde Secrets o Variables de Entorno
        try:
            self.public_key = st.secrets.get("EPAYCO_PUBLIC_KEY", os.getenv("EPAYCO_PUBLIC_KEY"))
            self.private_key = st.secrets.get("EPAYCO_PRIVATE_KEY", os.getenv("EPAYCO_PRIVATE_KEY"))
            self.customer_id = st.secrets.get("EPAYCO_CUSTOMER_ID", os.getenv("EPAYCO_CUSTOMER_ID"))
            self.test_mode = st.secrets.get("EPAYCO_TEST_MODE", "true").lower() == "true"
        except Exception:
            self.public_key = os.getenv("EPAYCO_PUBLIC_KEY")
            self.private_key = os.getenv("EPAYCO_PRIVATE_KEY")
            self.customer_id = os.getenv("EPAYCO_CUSTOMER_ID")
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

        # ePayco usa un endpoint de checkout estándar
        base_url = "https://checkout.epayco.co/checkout.php"
        
        # En un flujo real, se debe generar una sesión de pago vía API. 
        # Para simplificar la integración estándar (Split/Checkout), redirigimos con parámetros.
        # NOTA: ePayco recomienda usar su SDK oficial. Esta es una aproximación REST.
        
        # Construimos los parámetros básicos de ePayco
        params = {
            "public_key": self.public_key,
            "amount": int(float(monto) * 100), # ePayco maneja centavos para COP, pero si es USD, ver documentación
            "currency": "USD",
            "description": descripcion[:255],
            "invoice": pedido_id,
            "name": "Cliente SAMU IA",
            "email": metadata.get("email", "cliente@samu-ia.com") if metadata else "cliente@samu-ia.com",
            "response": "https://samu-ia.streamlit.app/?web=checkout", # URL a donde vuelve el usuario
            "confirmation": "https://samu-ia.streamlit.app/api/webhook_epayco", # URL de webhook
        }

        # NOTA: Para producción, debes generar un token de sesión con la API de ePayco
        # usando el private_key. Aquí simulamos el link de redirección.
        url_pago = f"{base_url}?public_key={self.public_key}&invoice={pedido_id}&amount={monto}&currency=USD&description={descripcion}"

        return {
            "exito": True,
            "pago_id": f"epayco_{pedido_id}",
            "estado": "pendiente_pago_epayco",
            "url_pago": url_pago,
            "instrucciones": f"Serás redirigido a ePayco para completar el pago de USD {monto}.",
            "error": None
        }

    def verificar_pago(self, pago_id):
        # Aquí se consultaría a la API de ePayco el estado real
        return {
            "estado": "pendiente",
            "pagado": False,
            "error": None
        }

    def procesar_webhook(self, payload):
        # Aquí se procesa la confirmación de ePayco
        return {
            "procesado": True,
            "pedido_id": payload.get("x_id_invoice"),
            "estado": "pagado" if payload.get("x_response") == "Aceptada" else "rechazado",
            "error": None
        }