from pathlib import Path

RUTA = Path("config/contexto_samu_ia.md")

if not RUTA.exists():
    print("NO EXISTE el archivo de contexto")
else:
    ctx = RUTA.read_text(encoding="utf-8")
    print(f"Contexto: {len(ctx)} chars")
    print(f"Staff: {'staff' in ctx.lower()}")
    print(f"Sucursales: {'sucursal' in ctx.lower()}")
    print(f"KPIs (CAC o Churn): {'CAC' in ctx or 'Churn' in ctx}")
    print(f"Config editable: {'config editable' in ctx.lower() or 'configuracion global' in ctx.lower()}")
    print(f"Analisis profundo: {'analisis profundo' in ctx.lower()}")
    print(f"React Bits: {'React Bits' in ctx}")
