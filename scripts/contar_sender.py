from pathlib import Path
p = Path("utils/email_sender.py")
lineas = len(p.read_text(encoding="utf-8").splitlines())
print(f"  [{'OK' if lineas < 400 else 'EXCEDE'}] email_sender.py - {lineas} lineas")
