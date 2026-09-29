# scripts/restore_emojis.py
# ============================================
# RESTAURADOR DE EMOJIS V6 - Reemplazo directo
# ============================================
# Lee el backup .bak3 (con mojibake), reemplaza cada
# grupo mojibake por el emoji real, guarda como UTF-8.
#
# Ventaja: no analiza strings, no toca comillas.
# Python I/O => 0% riesgo de re-corromper.
# ============================================

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKUP = ROOT / "panels" / "panel_base.py.bak3"
DESTINO = ROOT / "panels" / "panel_base_restored.py"


CP1252_REV = {
    0x20AC: 0x80, 0x201A: 0x82, 0x0192: 0x83, 0x201E: 0x84,
    0x2026: 0x85, 0x2020: 0x86, 0x2021: 0x87, 0x02C6: 0x88,
    0x2030: 0x89, 0x0160: 0x8A, 0x2039: 0x8B, 0x0152: 0x8C,
    0x017D: 0x8E, 0x2018: 0x91, 0x2019: 0x92, 0x201C: 0x93,
    0x201D: 0x94, 0x2022: 0x95, 0x2013: 0x96, 0x2014: 0x97,
    0x02DC: 0x98, 0x2122: 0x99, 0x0161: 0x9A, 0x203A: 0x9B,
    0x0153: 0x9C, 0x017E: 0x9E, 0x0178: 0x9F,
}


def char_to_byte(c):
    cp = ord(c)
    if cp < 0x80:
        return cp
    if cp in CP1252_REV:
        return CP1252_REV[cp]
    if 0xA0 <= cp <= 0xFF:
        return cp
    return None


def decodificar(grupo):
    """Intenta decodificar un grupo mojibake -> texto original."""
    bytes_list = [char_to_byte(c) for c in grupo]
    if None in bytes_list:
        return None
    try:
        decoded = bytes(bytes_list).decode("utf-8")
        # Solo aceptar si al menos un caracter es simbolo/emoji (>= U+2000)
        if any(ord(c) >= 0x2000 for c in decoded):
            return decoded
        return None
    except (UnicodeDecodeError, ValueError):
        return None


def fix_group(match):
    """Reemplaza un grupo mojibake por el texto original."""
    grupo = match.group(0)
    out = []
    i = 0
    while i < len(grupo):
        max_len = min(12, len(grupo) - i)
        encontrado = False
        for length in range(max_len, 1, -1):
            sub = grupo[i:i + length]
            decoded = decodificar(sub)
            if decoded:
                out.append(decoded)
                i += length
                encontrado = True
                break
        if not encontrado:
            out.append(grupo[i])
            i += 1
    return "".join(out)


def main():
    print("=" * 70)
    print("RESTAURADOR DE EMOJIS V6 - Reemplazo directo")
    print("=" * 70)

    if not BACKUP.exists():
        print(f"ERROR: No existe {BACKUP}")
        print("Verifica que panel_base.py.bak3 este en panels/")
        return

    texto = BACKUP.read_text(encoding="utf-8")
    grupos = re.findall(r"[^\x00-\x7F]{2,}", texto)
    print(f"Grupos mojibake encontrados: {len(grupos)}")

    resultado = re.sub(r"[^\x00-\x7F]{2,}", fix_group, texto)

    emojis_recuperados = sum(1 for c in resultado if ord(c) >= 0x2000)
    print(f"Emojis recuperados: {emojis_recuperados}")

    DESTINO.write_text(resultado, encoding="utf-8")
    print(f"Guardado: {DESTINO.name}")
    print("Verifica con:")
    print('  python -c "import ast; ast.parse(open(\'panels/panel_base_restored.py\', encoding=\'utf-8\').read()); print(\'OK\')"')


if __name__ == "__main__":
    main()