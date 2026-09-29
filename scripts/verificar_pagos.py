from pathlib import Path

archivos = [
    "panels/web/pagos/__init__.py",
    "panels/web/pagos/base.py",
    "panels/web/pagos/manual.py",
]

print("=" * 70)
print("ADAPTADOR DE PAGOS")
print("=" * 70)
for a in archivos:
    p = Path(a)
    if p.exists():
        lineas = len(p.read_text(encoding="utf-8").splitlines())
        print(f"  [OK] {a:40s} {lineas:4d} lineas")
    else:
        print(f"  [--] {a:40s} NO EXISTE")
print("=" * 70)
