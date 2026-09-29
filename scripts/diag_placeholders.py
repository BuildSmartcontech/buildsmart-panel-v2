import sys, re
from pathlib import Path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

ruta = Path("data/webs_generadas/pedido_c8c1f3c3/c100f486-7717-4863-a5c2-5c61e458cb54/index.html")

print("=" * 70)
print("DIAGNOSTICO PLACEHOLDERS")
print("=" * 70)

if not ruta.exists():
    print(f"NO EXISTE: {ruta}")
    sys.exit(1)

html = ruta.read_text(encoding="utf-8")

# Buscar placeholders restantes
placeholders = re.findall(r"\{\{[A-Z_]+\}\}", html)

print(f"Total placeholders encontrados: {len(placeholders)}")
print()

if placeholders:
    from collections import Counter
    conteo = Counter(placeholders)
    for ph, cnt in conteo.most_common():
        print(f"  {ph}: {cnt} veces")
else:
    print("  (ninguno)")
print()

# Ver el form para debug
form_match = re.search(r'<form[^>]*>.*?</form>', html, re.DOTALL | re.IGNORECASE)
if form_match:
    form = form_match.group(0)
    print(f"Formulario (primeros 500 chars):")
    print("-" * 70)
    print(form[:500])
    print("-" * 70)
