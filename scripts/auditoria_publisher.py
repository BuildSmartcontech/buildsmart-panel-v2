import os
from pathlib import Path

print("=" * 70)
print("AUDITORIA: donde se llama publicar_web()")
print("=" * 70)

raiz = Path(".")
patrones = ["publicar_web(", "publicar_carpeta(", "publicar_html("]
extensiones = [".py"]

hallazgos = []

for archivo in raiz.rglob("*"):
    if not archivo.is_file():
        continue
    if archivo.suffix not in extensiones:
        continue
    # Ignorar backups y venv
    if "backup" in archivo.name.lower():
        continue
    if "venv" in str(archivo):
        continue
    if "__pycache__" in str(archivo):
        continue

    try:
        contenido = archivo.read_text(encoding="utf-8")
    except Exception:
        continue

    lineas = contenido.split("\n")
    for i, linea in enumerate(lineas, 1):
        for patron in patrones:
            if patron in linea and not linea.strip().startswith("#"):
                hallazgos.append({
                    "archivo": str(archivo),
                    "linea": i,
                    "codigo": linea.strip()[:100],
                })

# Agrupar por archivo
por_archivo = {}
for h in hallazgos:
    if h["archivo"] not in por_archivo:
        por_archivo[h["archivo"]] = []
    por_archivo[h["archivo"]].append(h)

print(f"\nTotal llamadas encontradas: {len(hallazgos)}\n")

for archivo, llamadas in sorted(por_archivo.items()):
    print(f"\n{archivo} ({len(llamadas)} llamadas)")
    for c in llamadas:
        print(f"  L{c['linea']}: {c['codigo']}")

print("=" * 70)
print("Analisis:")
print("  - 1-2 archivos con 1-2 llamadas = OK (controlado)")
print("  - Muchas llamadas o loops = problema de consumo")
print("=" * 70)
