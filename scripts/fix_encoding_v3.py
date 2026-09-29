# scripts/fix_encoding_v3.py
# ============================================
# MOJIBAKE STRIPPER V3
# ============================================
# Borra secuencias de 2+ caracteres no-ASCII consecutivos
# (mojibake de emojis). Preserva acentos simples (ñ, á).
# No usa escapes \uXXXX (evita romper f-strings).
# ============================================

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ARCHIVOS = [
    "panels/panel_base.py",
    "panels/panel_dueno.py",
    "panels/panel_usuario.py",
    "panels/onboarding.py",
    "modules/sidebar.py",
    "modules/header_footer.py",
    "modules/css.py",
]


def strip_mojibake(text):
    # Coincide con 2 o mas caracteres no-ASCII consecutivos (mojibake)
    # No toca acentos solos (ñ, á, é) porque son 1 solo char no-ASCII
    return re.sub(r"[^\x00-\x7F]{2,}", "", text)


def main():
    print("=" * 70)
    print("MOJIBAKE STRIPPER V3")
    print("=" * 70)
    for archivo in ARCHIVOS:
        path = ROOT / archivo
        if not path.exists():
            print(f"  [--] {archivo} (no existe)")
            continue
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()

        backup = Path(str(path) + ".bak3")
        with open(backup, "w", encoding="utf-8") as f:
            f.write(original)

        fixed = strip_mojibake(original)

        with open(path, "w", encoding="utf-8") as f:
            f.write(fixed)

        removed = len(original) - len(fixed)
        print(f"  [OK] {archivo} -> -{removed} chars")

    print("=" * 70)
    print("Listo. Backups: *.bak3")
    print("=" * 70)


if __name__ == "__main__":
    main()