from pathlib import Path

for a in ["utils/web_prompts.py", "utils/web_prompts_data.py"]:
    p = Path(a)
    lineas = len(p.read_text(encoding="utf-8").splitlines())
    estado = "OK" if lineas < 400 else "EXCEDE 400"
    print(f"  [{estado:12s}] {a:40s} {lineas:4d} lineas")
