# scripts/fix_encoding_v2.py
# ============================================
# REPARADOR DE MOJIBAKE V2
# ============================================
# Detecta SOLO los grupos mojibake (emojis rotos)
# y los reemplaza por escapes \U (100% ASCII-safe).
#
# Diferencia con v1: no intenta decodificar todo el
# archivo, solo los grupos que son claramente mojibake.
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


# Mapa: byte cp1252 -> byte real (para revertir mojibake)
# Solo el rango especial 0x80-0x9F; el resto es igual a latin-1
CP1252_REVERSE = {
    0x20AC: 0x80, 0x201A: 0x82, 0x0192: 0x83, 0x201E: 0x84,
    0x2026: 0x85, 0x2020: 0x86, 0x2021: 0x87, 0x02C6: 0x88,
    0x2030: 0x89, 0x0160: 0x8A, 0x2039: 0x8B, 0x0152: 0x8C,
    0x017D: 0x8E, 0x2018: 0x91, 0x2019: 0x92, 0x201C: 0x93,
    0x201D: 0x94, 0x2022: 0x95, 0x2013: 0x96, 0x2014: 0x97,
    0x02DC: 0x98, 0x2122: 0x99, 0x0161: 0x9A, 0x203A: 0x9B,
    0x0153: 0x9C, 0x017E: 0x9E, 0x0178: 0x9F,
}


def char_a_byte(c):
    cp = ord(c)
    if cp < 0x80:
        return cp
    if cp in CP1252_REVERSE:
        return CP1252_REVERSE[cp]
    if 0xA0 <= cp <= 0xFF:
        return cp
    return None


def reemplazar_grupo(match):
    """Intenta revertir el grupo mojibake. Si falla, lo deja igual."""
    bloque = match.group(0)
    # Probar de mayor a menor longitud
    for start in range(len(bloque)):
        for end in range(len(bloque), start, -1):
            sub = bloque[start:end]
            try:
                bytes_list = [char_a_byte(c) for c in sub]
                if None in bytes_list:
                    continue
                decoded = bytes(bytes_list).decode("utf-8")
                # Solo aceptar si el resultado son caracteres "raros"
                # (emojis o símbolos > U+2000), NO letras normales
                if all(ord(c) >= 0x2000 or ord(c) < 0x80 for c in decoded):
                    if any(ord(c) >= 0x2000 for c in decoded):
                        # Reemplazar por escape \U / \u
                        escapes = ""
                        for c in decoded:
                            cp = ord(c)
                            if cp < 0x80:
                                escapes += c
                            elif cp <= 0xFFFF:
                                escapes += f"\\u{cp:04X}"
                            else:
                                escapes += f"\\U{cp:08X}"
                        # Reemplazar el sub en el bloque
                        prefix = bloque[:start]
                        suffix = bloque[end:]
                        return prefix + escapes + suffix
            except (UnicodeDecodeError, ValueError):
                continue
    return bloque  # no se pudo, dejar igual


def reparar_archivo(path):
    with open(path, "r", encoding="utf-8") as f:
        original = f.read()

    # Detectar grupos de 2+ caracteres no-ASCII consecutivos
    patron = re.compile(r"[^\x00-\x7F]{2,}")
    reparado = patron.sub(reemplazar_grupo, original)

    if reparado == original:
        return "sin cambios"

    # Backup
    backup = Path(str(path) + ".bak2")
    with open(backup, "w", encoding="utf-8") as f:
        f.write(original)

    with open(path, "w", encoding="utf-8") as f:
        f.write(reparado)

    # Contar escapes insertados
    n_escapes = reparado.count("\\U") + reparado.count("\\u")
    return f"reparado ({n_escapes} emojis convertidos a escape)"


def main():
    print("=" * 70)
    print("REPARADOR MOJIBAKE V2")
    print("=" * 70)

    for archivo in ARCHIVOS:
        path = ROOT / archivo
        if not path.exists():
            print(f"  [--] {archivo} (no existe)")
            continue
        resultado = reparar_archivo(path)
        simbolo = "OK" if "reparado" in resultado else "--"
        print(f"  [{simbolo}] {archivo} -> {resultado}")

    print("=" * 70)
    print("Listo. Backups: *.bak2")
    print("=" * 70)


if __name__ == "__main__":
    main()