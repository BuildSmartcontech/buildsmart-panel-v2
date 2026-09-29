import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

usuario_id = "pedido_c8c1f3c3"
web_id = "81bb99b3-37e1-4bd2-a13b-c0935214470e"

ruta = Path("data") / "webs_generadas" / usuario_id / web_id / "index.html"

print("=" * 70)
print(f"DIAGNOSTICO HTML")
print("=" * 70)
print(f"Ruta: {ruta}")
print(f"Existe: {ruta.exists()}")

if ruta.exists():
    html = ruta.read_text(encoding="utf-8")
    print(f"Tamaño: {len(html):,} chars")
    print()
    # 1. Verificar formulario inyectado
    tiene_script = "<script>" in html and "crm_leads" in html
    tiene_pedido = web_id in html or "c8c1f3c3" in html
    print(f"[{'OK' if tiene_script else 'NO'}] Formulario inyectado (crm_leads)")
    print(f"[{'OK' if tiene_pedido else 'NO'}] PEDIDO_ID presente")

    # 2. Verificar imagen del hero
    import re
    imgs = re.findall(r'<img[^>]*src="([^"]+)"', html)
    print(f"\nImagenes encontradas: {len(imgs)}")
    for i, url in enumerate(imgs[:5], 1):
        print(f"  {i}. {url[:90]}")

    # 3. Verificar que hay un <form>
    forms = re.findall(r'<form[^>]*>', html)
    print(f"\nForms: {len(forms)}")
    for f in forms[:3]:
        print(f"  {f[:100]}")

    # 4. Verificar cierre del body
    tiene_body_cierre = "</body>" in html.lower()
    print(f"\n[{'OK' if tiene_body_cierre else 'NO'}] </body> presente")
