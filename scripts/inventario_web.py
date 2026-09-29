from pathlib import Path

archivos = [
    "utils/web_generator.py",
    "utils/web_prompts.py",
    "utils/web_templates.py",
    "utils/web_editor_v2.py",
    "utils/web_publisher.py",
    "utils/netlify_publisher.py",
    "utils/web_validator.py",
    "utils/html_patcher.py",
    "utils/image_fetcher.py",
    "utils/sector_detector.py",
    "utils/web_module.py",
]

print("=" * 70)
print("INVENTARIO DE ARCHIVOS WEB")
print("=" * 70)

for a in archivos:
    p = Path(a)
    if p.exists():
        lineas = len(p.read_text(encoding="utf-8").splitlines())
        tamano = p.stat().st_size
        print(f"  [OK] {a:40s} {lineas:5d} lineas ({tamano:,} bytes)")
    else:
        print(f"  [--] {a:40s} NO EXISTE")

print("=" * 70)
