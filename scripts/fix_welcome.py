from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ARCHIVOS = [
    "panels/panel_base.py",
    "panels/panel_base_hooks.py",
    "panels/panel_usuario.py",
    "panels/panel_dueno.py",
    "panels/dueno/__init__.py",
]

# Reemplazos especificos (orden importa)
REEMPLAZOS = [
    ("Bienvenido a BuildSmart Holdings", "Bienvenido a SAMU IA"),
    ("Bienvenido a BuildSmart", "Bienvenido a SAMU IA"),
    ("BuildSmart Holdings", "SAMU IA"),
]

# NUNCA tocar
PROTEGIDOS = [
    "buildsmart-webs.netlify.app",
    "buildsmart-panel",
    "BUILDSMART_ES_DUENO",
    "buildsmart_webs",
    "@buildsmart.app",
    "@buildsmart.com",
]


def proteger(texto):
    for i, p in enumerate(PROTEGIDOS):
        texto = texto.replace(p, f"__PROT_{i}__")
    return texto


def desproteger(texto):
    for i, p in enumerate(PROTEGIDOS):
        texto = texto.replace(f"__PROT_{i}__", p)
    return texto


def procesar(path):
    try:
        original = path.read_text(encoding="utf-8")
    except Exception as e:
        return None

    texto = proteger(original)
    cambios = []
    for viejo, nuevo in REEMPLAZOS:
        if viejo in texto:
            n = texto.count(viejo)
            texto = texto.replace(viejo, nuevo)
            cambios.append(f"{viejo} -> {nuevo} (x{n})")

    texto = desproteger(texto)

    if texto == original:
        return None

    path.write_text(texto, encoding="utf-8")
    return " | ".join(cambios)


print("=" * 70)
print("FIX MENSAJE BIENVENIDA -> SAMU IA")
print("=" * 70)

total = 0
for archivo in ARCHIVOS:
    path = ROOT / archivo
    if not path.exists():
        print(f"  [--] {archivo} (no existe)")
        continue
    resultado = procesar(path)
    if resultado:
        print(f"  [OK] {archivo}")
        print(f"       {resultado}")
        total += 1
    else:
        print(f"  [--] {archivo} (sin cambios)")

print("=" * 70)
print(f"Total modificados: {total}")
print("=" * 70)
