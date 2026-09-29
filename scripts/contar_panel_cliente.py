from pathlib import Path
p = Path("panels/web/panel_cliente.py")
lineas = len(p.read_text(encoding="utf-8").splitlines())
print(f"  [{'OK' if lineas < 400 else 'EXCEDE'}] panel_cliente.py - {lineas} lineas")
