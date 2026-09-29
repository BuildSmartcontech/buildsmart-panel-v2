# scripts/fix_buildsmart_texts.py
# ============================================
# REEMPLAZA TEXTOS "BuildSmart" -> "SAMU IA"
# ============================================
# Reemplazo quirurgico en archivos especificos.
# Respeta URLs, env vars y nombres tecnicos.
# ============================================

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Archivos a procesar
ARCHIVOS = [
    "panels/panel_base.py",
    "panels/panel_dueno.py",
    "panels/panel_usuario.py",
    "panels/onboarding.py",
    "modules/sidebar.py",
    "modules/header_footer.py",
]

# Reemplazos (orden importa)
REEMPLAZOS = [
    ("Bienvenido a BuildSmart Holdings", "Bienvenido a SAMU IA"),
    ("BuildSmart Holdings", "SAMU IA"),
    ("BUILDSMART HOLDINGS", "SAMU IA"),
    ("buildsmart holdings", "SAMU IA"),
    ("Bienvenido a BuildSmart", "Bienvenido a SAMU IA"),
    ("BuildSmart", "SAMU IA"),
]

# NUNCA tocar
PROTEGIDOS = [
    "buildsmart-webs.netlify.app",
    "buildsmart-panel",
    "BUILDSMART_ES_DUENO",
    "buildsmart_webs",
    "buildsmart-webs",
    "buildsmart@",
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
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()
    except Exception as e:
        return f"SKIP lectura: {e}"

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

    with open(path, "w", encoding="utf-8") as f:
        f.write(texto)

    return " | ".join(cambios)


def main():
    print("=" * 70)
    print("FIX TEXTS: BuildSmart -> SAMU IA")
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


if __name__ == "__main__":
    main()