import os
from pathlib import Path

print("=" * 70)
print("AUDITORIA LIMPIA: llamadas a publicar_web()")
print("=" * 70)

raiz = Path(".")
patron = "publicar_web("
hallazgos = []

for archivo in raiz.rglob("*.py"):
    if not archivo.is_file():
        continue
    s = str(archivo)
    if any(x in s for x in ["venv", "__pycache__", "_backups", "backup", "corrupto", "restored"]):
        continue

    try:
        contenido = archivo.read_text(encoding="utf-8")
    except Exception:
        continue

    for i, linea in enumerate(contenido.split("\n"), 1):
        if patron in linea and not linea.strip().startswith("#"):
            # Ignorar definiciones de funcion
            if "def publicar_web" in linea:
                continue
            hallazgos.append((str(archivo), i, linea.strip()[:90]))

print(f"\nTotal llamadas reales: {len(hallazgos)}\n")
for archivo, linea, codigo in hallazgos:
    print(f"  {archivo}:{linea}")
    print(f"    {codigo}")

print()
print("Esperado: 4-5 llamadas (panel_base, comun, pedidos_web_acciones, web_module)")
print("=" * 70)
