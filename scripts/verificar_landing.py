from pathlib import Path
p = Path("panels/web/landing.py")
print(f"Lineas: {len(p.read_text(encoding='utf-8').splitlines())}")
