from pathlib import Path
for a in ["panels/dueno/pedidos_web_acciones.py", "utils/formulario_leads.py"]:
    p = Path(a)
    if p.exists():
        lineas = len(p.read_text(encoding="utf-8").splitlines())
        estado = "OK" if lineas < 400 else "EXCEDE"
        print(f"  [{estado:8s}] {a:40s} {lineas:4d} lineas")
