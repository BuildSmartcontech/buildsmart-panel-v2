from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVO = ROOT / "panels" / "panel_base.py"

VIEJO = "COSTO_MODIFICACION_EXTRA = 5"
NUEVO = """try:
    from config_app import COSTO_MODIFICACION_EXTRA as _COSTO_DINAMICO
    COSTO_MODIFICACION_EXTRA = _COSTO_DINAMICO
except ImportError:
    COSTO_MODIFICACION_EXTRA = 5"""

texto = ARCHIVO.read_text(encoding="utf-8")

if "_COSTO_DINAMICO" in texto:
    print("Ya estaba aplicado. Sin cambios.")
elif VIEJO not in texto:
    print(f"ERROR: no se encontro '{VIEJO}'")
else:
    nuevo_texto = texto.replace(VIEJO, NUEVO, 1)
    ARCHIVO.write_text(nuevo_texto, encoding="utf-8")
    print("OK. Cambio de costo aplicado.")
