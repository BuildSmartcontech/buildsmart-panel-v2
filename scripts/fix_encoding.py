# scripts/fix_encoding.py
# ============================================
# REPARA MOJIBAKE (UTF-8 corrompido)
# ============================================
# Cuando un archivo UTF-8 se lee como Latin-1
# y se re-guarda como UTF-8, los emojis se
# convierten en cosas como "ðŸ"‹" (📋).
#
# Este script invierte el proceso.
# ============================================

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Archivos a reparar
ARCHIVOS = [
    "panels/panel_base.py",
    "panels/panel_dueno.py",
    "panels/panel_usuario.py",
    "panels/onboarding.py",
    "modules/sidebar.py",
    "modules/header_footer.py",
    "modules/css.py",
]


def reparar_archivo(path, backup=True):
    try:
        with open(path, "r", encoding="utf-8") as f:
            contenido_original = f.read()
    except Exception as e:
        return f"SKIP: {e}"

    # Intentar decodificar el mojibake
    try:
        reparado = contenido_original.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        # Algunos emojis no caben en latin-1; probar cp1252
        try:
            reparado = contenido_original.encode("cp1252").decode("utf-8")
        except Exception:
            return "SKIP: no se pudo reparar (probablemente ya esta OK)"

    if reparado == contenido_original:
        return "OK: sin cambios (ya estaba bien)"

    # Backup
    if backup:
        backup_path = Path(str(path) + ".bak")
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(contenido_original)

    with open(path, "w", encoding="utf-8") as f:
        f.write(reparado)

    # Contar emojis recuperados
    emojis = sum(1 for c in reparado if ord(c) > 0x1F000)
    return f"REPARADO ({emojis} emojis recuperados)"


def main():
    print("=" * 70)
    print("REPARANDO ENCODING")
    print("=" * 70)

    for archivo in ARCHIVOS:
        path = ROOT / archivo
        if not path.exists():
            print(f"  [--] {archivo} (no existe)")
            continue

        resultado = reparar_archivo(path)
        print(f"  [{resultado[:3]}] {archivo}")
        if "REPARADO" in resultado or "SKIP" in resultado:
            print(f"        {resultado}")

    print("=" * 70)
    print("Listo. Si algo se rompe, cada archivo tiene .bak")
    print("=" * 70)


if __name__ == "__main__":
    main()