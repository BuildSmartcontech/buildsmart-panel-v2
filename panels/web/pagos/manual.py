# panels/web/pagos/manual.py
# ============================================
# PROVEEDOR DE PAGOS MANUAL - SAMU IA
# ============================================
# V2.0: Formato markdown con bullets (mejor visual)
# V1.0: Version inicial
# ============================================

try:
    from panels.web.pagos.base import ProveedorPago
except ImportError:
    import sys
    from pathlib import Path
    _ROOT = Path(__file__).resolve().parent.parent.parent.parent
    sys.path.insert(0, str(_ROOT))
    from panels.web.pagos.base import ProveedorPago


class PagoManual(ProveedorPago):
    """Proveedor de pagos manual."""

    nombre = "manual"
    soporta_suscripciones = False
    usa_webhooks = False

    def __init__(self, datos_pago=None):
        """
        Args:
            datos_pago (dict): Datos bancarios que se le muestran
                al cliente. Ej:
                {
                    "nequi": "300 123 4567",
                    "daviplata": "300 123 4567",
                    "bancolombia_ahorros": "123-456789-00",
                    "titular": "Antonio Porras",
                    "email_comprobante": "pagos@samu-ia.com"
                }
        """
        self.datos_pago = datos_pago or {}

    def crear_pago(self, pedido_id, monto, descripcion, metadata=None):
        """Crea un pedido en estado 'pendiente_pago_manual'."""
        lineas = []
        lineas.append(f"### Para completar tu compra, transferi **USD {monto:.0f}** a:")
        lineas.append("")

        metodos = []
        if self.datos_pago.get("nequi"):
            metodos.append(f"- **Nequi:** {self.datos_pago['nequi']}")
        if self.datos_pago.get("daviplata"):
            metodos.append(f"- **Daviplata:** {self.datos_pago['daviplata']}")
        if self.datos_pago.get("bancolombia_ahorros"):
            metodos.append(f"- **Bancolombia (ahorros):** {self.datos_pago['bancolombia_ahorros']}")
        if self.datos_pago.get("titular"):
            metodos.append(f"- **Titular:** {self.datos_pago['titular']}")

        if metodos:
            lineas.extend(metodos)
        else:
            lineas.append("- (Datos de pago pendientes de configurar)")

        lineas.append("")

        if self.datos_pago.get("email_comprobante"):
            lineas.append(f"### Despues, envia el comprobante a:")
            lineas.append("")
            lineas.append(f"**{self.datos_pago['email_comprobante']}**")
            lineas.append("")

        lineas.append("---")
        lineas.append("Tu pedido se activara cuando confirmemos el pago. "
                      "Normalmente en menos de **24 horas**.")

        instrucciones = "\n".join(lineas)

        return {
            "exito": True,
            "pago_id": f"manual_{pedido_id}",
            "estado": "pendiente_pago_manual",
            "url_pago": None,
            "instrucciones": instrucciones,
            "error": None,
        }

    def verificar_pago(self, pago_id):
        """El dueno confirma manualmente. Por defecto: pendiente."""
        return {
            "estado": "pendiente",
            "pagado": False,
            "error": None,
        }

    def info_instrucciones(self):
        return (
            "Modo de pago manual. El cliente debe transferir por fuera "
            "(Nequi, transferencia, etc.) y el dueno confirma el pago "
            "desde el panel."
        )