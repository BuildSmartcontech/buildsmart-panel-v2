# panels/web/pagos/__init__.py
# ============================================
# ADAPTADOR DE PAGOS - SAMU IA
# ============================================
# Router que elige el proveedor de pagos segun la
# configuracion del sistema.
#
# Proveedores disponibles:
#   - manual:      Confirmacion manual por el dueno
#   - wompi:       Bancolombia (proximamente)
#   - epayco:      Davivienda (proximamente)
#   - mercadopago: (futuro)
#
# Cambiar de proveedor = 1 linea en config_global:
#   UPDATE config_global SET valor='"wompi"' WHERE clave='pago_proveedor';
# ============================================

from panels.web.pagos.manual import PagoManual


# Proveedores registrados
_PROVEEDORES = {
    "manual": PagoManual,
    # "wompi": WompiProvider,       # Descomentar cuando este listo
    # "epayco": EPaycoProvider,     # Descomentar cuando este listo
}


def obtener_proveedor(nombre=None, datos_pago=None):
    """
    Devuelve una instancia del proveedor de pagos.

    Args:
        nombre (str, opcional): Nombre del proveedor.
            Si no se pasa, lee de config_global (clave 'pago_proveedor').
        datos_pago (dict, opcional): Configuracion especifica.

    Returns:
        ProveedorPago: instancia lista para usar
    """
    if nombre is None:
        try:
            from utils.config_global import obtener
            nombre = obtener("pago_proveedor", "manual")
        except Exception:
            nombre = "manual"

    clase = _PROVEEDORES.get(nombre)
    if not clase:
        print(f"[pagos] Proveedor '{nombre}' no encontrado. Usando 'manual'.")
        clase = PagoManual
        nombre = "manual"

    # El proveedor manual acepta datos_pago
    if nombre == "manual":
        return clase(datos_pago=datos_pago)

    return clase()


def listar_proveedores():
    """Devuelve la lista de proveedores disponibles."""
    return list(_PROVEEDORES.keys())


def proveedor_actual():
    """Devuelve el nombre del proveedor configurado."""
    try:
        from utils.config_global import obtener
        return obtener("pago_proveedor", "manual")
    except Exception:
        return "manual"


# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    print("=" * 60)
    print("TEST ADAPTADOR DE PAGOS")
    print("=" * 60)
    print(f"Proveedores disponibles: {listar_proveedores()}")
    print(f"Proveedor actual: {proveedor_actual()}")
    print()

    p = obtener_proveedor("manual", datos_pago={"nequi": "300 123 4567"})
    print(f"Instancia: {p.nombre}")
    print(f"Soporta suscripciones: {p.soporta_suscripciones}")
    print(f"Usa webhooks: {p.usa_webhooks}")
    print()

    result = p.crear_pago("test_001", 149, "Web Gancho Tier 1")
    print(f"Crear pago exito: {result['exito']}")
    print(f"Estado: {result['estado']}")
    print(f"Pago ID: {result['pago_id']}")
    print()
    print("Instrucciones generadas:")
    print("-" * 60)
    print(result["instrucciones"])
    print("-" * 60)