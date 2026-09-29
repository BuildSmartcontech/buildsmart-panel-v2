from pathlib import Path
for a in ["utils/email_pedidos.py", "panels/web/checkout.py", "panels/web/panel_cliente.py", "panels/web/__init__.py", "utils/magic_link.py"]:
    p = Path(a)
    if p.exists():
        lineas = len(p.read_text(encoding="utf-8").splitlines())
        estado = "OK" if lineas < 400 else "EXCEDE"
        print(f"  [{estado:8s}] {a:40s} {lineas:4d} lineas")
