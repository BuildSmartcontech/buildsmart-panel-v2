from pathlib import Path

def diagnosticar(nombre, ruta):
    p = Path(ruta)
    print(f"=== {nombre} ===")
    if not p.exists():
        print(f"  NO EXISTE: {ruta}")
        print()
        return
    t = p.read_text(encoding="utf-8")
    lineas = len(t.splitlines())
    emojis_reales = sum(1 for c in t if ord(c) >= 0x1F000)
    tiene_dinamico = "_COSTO_DINAMICO" in t
    tiene_mojibake = "ðŸ" in t
    tiene_logging = "log_evento" in t
    print(f"  Ruta: {ruta}")
    print(f"  Lineas: {lineas}")
    print(f"  Emojis reales: {emojis_reales}")
    print(f"  Tiene mojibake (ðŸ): {tiene_mojibake}")
    print(f"  Tiene _COSTO_DINAMICO: {tiene_dinamico}")
    print(f"  Tiene logging (log_evento): {tiene_logging}")
    print()

diagnosticar("ACTUAL panels/panel_base.py", "panels/panel_base.py")
diagnosticar("BACKUP rename", "_backup_rename_20260917_212956/panels/panel_base.py")
diagnosticar("BACKUP costo", "panels/panel_base_pre_costo.py")
