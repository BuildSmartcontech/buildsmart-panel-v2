# panels/web/pagos/base.py
# ============================================
# INTERFAZ BASE DE PROVEEDORES DE PAGO
# ============================================
# Define el "contrato" que todo proveedor de pagos
# debe cumplir. Cualquier pasarela (Manual, Wompi,
# ePayco, Stripe, Mercado Pago) hereda de esta clase.
# ============================================

from abc import ABC, abstractmethod


class ProveedorPago(ABC):
    """
    Interfaz abstracta para proveedores de pago.

    Cualquier implementacion (manual, wompi, epayco)
    debe heredar de esta clase y sobrescribir los
    metodos abstractos.
    """

    nombre = "base"
    soporta_suscripciones = False
    usa_webhooks = False

    @abstractmethod
    def crear_pago(self, pedido_id, monto, descripcion, metadata=None):
        """
        Crea un intento de pago.

        Args:
            pedido_id (str): ID del pedido en pedidos_web
            monto (float): Monto en USD
            descripcion (str): Concepto del pago
            metadata (dict): Datos extra opcionales

        Returns:
            dict: {
                "exito": bool,
                "pago_id": str,
                "estado": str,
                "url_pago": str or None,
                "instrucciones": str,
                "error": str or None
            }
        """
        pass

    @abstractmethod
    def verificar_pago(self, pago_id):
        """
        Consulta el estado actual de un pago.

        Returns:
            dict: {
                "estado": str,
                "pagado": bool,
                "error": str or None
            }
        """
        pass

    def procesar_webhook(self, payload):
        """
        Procesa una notificacion webhook de la pasarela.
        Por defecto no hace nada (proveedores sin webhook).
        """
        return {
            "procesado": False,
            "pedido_id": None,
            "estado": None,
            "error": "Webhooks no soportados",
        }

    def info_instrucciones(self):
        """Instrucciones para mostrar al cliente."""
        return ""