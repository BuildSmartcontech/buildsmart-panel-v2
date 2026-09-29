# scripts/rename_to_samu_ia.py
# ============================================
# RENOMBRADO MASIVO: BuildSmart -> SAMU IA
# ============================================
# - Reemplaza "BuildSmart Holdings" y "BuildSmart" en archivos .py
# - Respeta URLs (buildsmart-webs.netlify.app)
# - Respeta env vars (BUILDSMART_ES_DUENO)
# - Crea backup ANTES de tocar
# - Idempotente: correr 2 veces = mismo resultado
# ============================================

import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
BACKUP_DIR = ROOT / f"_backup_rename_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# Carpetas a procesar
CARPETAS = ["panels", "modules", "utils", "backend"]
RAIZ_ARCHIVOS = ["config_app.py", "app.py"]

# Carpetas y archivos a NO tocar
SKIP_DIRS = {
    "venv", ".venv", "__pycache__", ".git", "data", "config",
    "docs", "scripts", ".streamlit", "RESPALDO_WEBS_20260910_165201",
    "pdfs", "websites",
}

# Reemplazos (orden importa: el mas largo primero)
REEMPLAZOS = [
    ("BuildSmart Holdings", "SAMU IA"),
    ("BUILDSMART HOLDINGS", "SAMU IA"),
    ("buildsmart holdings", "SAMU IA"),
    ("BuildSmart HOLDINGS", "SAMU IA"),
    ("BuildSmart", "SAMU IA"),
    ("BUILDSMART", "SAMU IA"),
]

# NUNCA tocar esto (URLs, env vars, paths criticos)
PROTEGIDOS = [
    "buildsmart-webs.netlify.app",
    "buildsmart-panel",
    "BUILDSMART_ES_DUENO",
    "buildsmart_webs",
    "buildsmart-webs",
    "buildsmart@",
]


def proteger(texto):
    for i, p in enumerate(PROTEGIDOS):
        texto = texto.replace(p, f"__PROT_{i}__")
    return texto


def desproteger(texto):
    for i, p in enumerate(PROTEGIDOS):
        texto = texto.replace(f"__PROT_{i}__", p)
    return texto


def procesar_archivo(path):
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
            cambios.append(f"{viejo}->{nuevo} (x{n})")

    texto = desproteger(texto)

    if texto == original:
        return None

    # Backup
    backup_path = BACKUP_DIR / path.relative_to(ROOT)
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup_path)

    with open(path, "w", encoding="utf-8") as f:
        f.write(texto)

    return " | ".join(cambios)


def main():
    print("=" * 70)
    print(f"RENOMBRADO A SAMU IA")
    print(f"Backup: {BACKUP_DIR.name}")
    print("=" * 70)

    total = 0
    for carpeta in CARPETAS:
        base = ROOT / carpeta
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            if any(skip in path.parts for skip in SKIP_DIRS):
                continue
            resultado = procesar_archivo(path)
            if resultado:
                rel = path.relative_to(ROOT)
                print(f"  [OK] {rel}")
                print(f"       {resultado}")
                total += 1

    # Archivos sueltos en la raiz
    for nombre in RAIZ_ARCHIVOS:
        path = ROOT / nombre
        if path.exists():
            resultado = procesar_archivo(path)
            if resultado:
                print(f"  [OK] {nombre}")
                print(f"       {resultado}")
                total += 1

    print("=" * 70)
    print(f"Total modificados: {total}")
    print(f"Backup en: {BACKUP_DIR}")
    print("Si algo se rompe, copia del backup.")
    print("=" * 70)


if __name__ == "__main__":
    main()