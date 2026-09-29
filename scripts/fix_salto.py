from pathlib import Path

RUTA = Path("NOTAS_PROYECTO.md")
texto = RUTA.read_text(encoding="utf-8")

# Buscar el patron roto
VIEJO = 'para iterar durante los primeros 6 meses."### P-WEB:'
NUEVO = 'para iterar durante los primeros 6 meses."\n\n### P-WEB:'

if VIEJO in texto:
    texto = texto.replace(VIEJO, NUEVO, 1)
    RUTA.write_text(texto, encoding="utf-8")
    print("OK. Salto de linea arreglado.")
else:
    print("No se encontro el patron roto. Puede que ya este bien.")
