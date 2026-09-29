from pathlib import Path
for a in ["panels/web/checkout.py", "panels/web/pagos/__init__.py", "panels/web/pagos/base.py", "panels/web/pagos/manual.py"]:
    p = Path(a)
    if p.exists():
        lineas = len(p.read_text(encoding="utf-8").splitlines())
        estado = "OK" if lineas < 400 else "EXCEDE"
        print(f"  [{estado:8s}] {a:40s} {lineas:4d} lineas")
