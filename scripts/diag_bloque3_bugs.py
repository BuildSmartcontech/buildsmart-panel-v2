from pathlib import Path
import re

html = Path("test_bloque3.html").read_text(encoding="utf-8")

print("=" * 70)
print(f"ANALISIS DEL HTML ({len(html)} chars)")
print("=" * 70)

# 1. Marcadores de servicios
print("\n1. MARCADORES DE IMAGENES")
for m in ["{{HERO_IMAGE}}", "{{SERVICIO_1}}", "{{SERVICIO_2}}",
          "{{SERVICIO_3}}", "{{SERVICIO_4}}"]:
    count = html.count(m)
    print(f"  {m}: {count} ocurrencias")

# 2. Imagenes reales inyectadas
print("\n2. IMAGENES REALES")
imgs = re.findall(r'<img[^>]+src="([^"]+)"', html)
for i, url in enumerate(imgs[:10], 1):
    print(f"  {i}. {url[:100]}")

# 3. Como aparecen las img en las cards
print("\n3. CONTEXTO DE IMAGENES EN CARDS")
matches = re.findall(r'<img[^>]{0,200}>', html)
for m in matches[:8]:
    print(f"  {m[:200]}")
    print()

# 4. Colores de texto problematicos
print("\n4. COLORES DE TEXTO (buscando gris claro)")
colores = re.findall(r'color:\s*([#a-zA-Z0-9(),\s]+);', html)
from collections import Counter
contador = Counter(colores)
for color, count in contador.most_common(15):
    print(f"  {color.strip()}: {count} veces")

# 5. Backgrounds problemáticos
print("\n5. BACKGROUNDS (buscando negro/oscuro)")
bgs = re.findall(r'background[^:]*:\s*([^;]+);', html)
bg_counter = Counter(bgs)
for bg, count in bg_counter.most_common(10):
    print(f"  {bg.strip()[:80]}: {count}")

# 6. Ver si hay texto gris claro
print("\n6. TEXTOS PROBLEMATICOS (gris claro)")
grises_claros = re.findall(r'color:\s*#(?:[c-fC-F][0-9a-fA-F]{5}|[0-9a-fA-F]{3,5})\b', html)
print(f"  Total colores gris claro: {len(grises_claros)}")
for g in set(grises_claros[:10]):
    print(f"  {g}")

print("=" * 70)
