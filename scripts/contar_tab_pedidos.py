from pathlib import Path
p = Path("panels/dueno/tab_pedidos_web.py")
lineas = len(p.read_text(encoding="utf-8").splitlines())
print(f"  [{'OK' if lineas < 400 else 'EXCEDE'}] tab_pedidos_web.py - {lineas} lineas")
