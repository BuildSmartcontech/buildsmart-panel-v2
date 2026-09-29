# utils/web_editor_v2.py
# ============================================
# EDITOR DE WEBS ESTRUCTURADO - V2.2
# ============================================
# V2.2: Propaga informacion detallada de cambios
# (aplicados + fallidos con razones)
# ============================================

import os
import sys
import re
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.web_prompts import generar_prompt_edicion_estructurada
except ImportError:
    from web_prompts import generar_prompt_edicion_estructurada

try:
    from utils.html_patcher import aplicar_cambios
except ImportError:
    from html_patcher import aplicar_cambios

try:
    from backend.gateway import gateway
except ImportError:
    try:
        from gateway import gateway
    except ImportError:
        gateway = None


MAX_INTENTOS = 3
TIEMPO_ESPERA = 2


# ============================================
# VALIDACION FLEXIBLE
# ============================================

def validar_html_editado(html):
    errores = []
    advertencias = []

    if not html or not html.strip():
        return {"valido": False, "errores": ["HTML vacio"], "advertencias": []}

    html_lower = html.lower()

    if len(html) < 500:
        errores.append("HTML muy corto")
    if "<html" not in html_lower:
        errores.append("Falta <html>")
    if "</html>" not in html_lower:
        errores.append("Falta </html>")
    if "<body" not in html_lower:
        errores.append("Falta <body>")
    if "</body>" not in html_lower:
        errores.append("Falta </body>")

    if "<title>" not in html_lower:
        advertencias.append("Sin <title>")
    if "viewport" not in html_lower:
        advertencias.append("Sin viewport")

    return {"valido": len(errores) == 0, "errores": errores, "advertencias": advertencias}


# ============================================
# EXTRAER ESTRUCTURA
# ============================================

def extraer_estructura_html(html):
    if not html:
        return "HTML vacio"

    partes = []

    imagenes = []
    patron_img = r'<img\s+([^>]*?)>'
    for match in re.finditer(patron_img, html, re.IGNORECASE):
        attrs = match.group(1)
        src_match = re.search(r'src\s*=\s*["\']([^"\']*)["\']', attrs, re.IGNORECASE)
        alt_match = re.search(r'alt\s*=\s*["\']([^"\']*)["\']', attrs, re.IGNORECASE)
        src = src_match.group(1) if src_match else "(sin src)"
        alt = alt_match.group(1) if alt_match else "(sin alt)"
        src_corto = src[:60] + "..." if len(src) > 60 else src
        imagenes.append(f"  - alt='{alt}' src='{src_corto}'")

    if imagenes:
        partes.append("IMAGENES (" + str(len(imagenes)) + "):\n" + "\n".join(imagenes[:15]))

    titulos = []
    for tag in ["h1", "h2", "h3"]:
        patron = r'<' + tag + r'[^>]*>(.*?)</' + tag + r'>'
        for match in re.finditer(patron, html, re.DOTALL | re.IGNORECASE):
            texto = re.sub(r'<[^>]+>', '', match.group(1)).strip()
            texto = texto[:80]
            if texto:
                titulos.append(f"  - <{tag}>{texto}</{tag}>")

    if titulos:
        partes.append("TITULOS (" + str(len(titulos)) + "):\n" + "\n".join(titulos[:10]))

    clases = set()
    patron_class = r'class\s*=\s*["\']([^"\']+)["\']'
    for match in re.finditer(patron_class, html, re.IGNORECASE):
        for c in match.group(1).split():
            clases.add(c)

    if clases:
        partes.append("CLASES CSS: " + ", ".join(sorted(list(clases))[:30]))

    colores = set()
    patron_color = r'#[0-9a-fA-F]{6}'
    for match in re.finditer(patron_color, html):
        colores.add(match.group(0).lower())

    if colores:
        partes.append("COLORES USADOS: " + ", ".join(sorted(list(colores))[:20]))

    partes.append("TAMANO HTML: " + str(len(html)) + " caracteres")

    return "\n\n".join(partes)


def parsear_json_cambios(texto):
    if not texto:
        return None
    texto = texto.strip()
    if texto.startswith("```"):
        texto = re.sub(r'^```(?:json)?\s*', '', texto)
        texto = re.sub(r'\s*```$', '', texto)
    inicio = texto.find("{")
    fin = texto.rfind("}")
    if inicio == -1 or fin == -1:
        return None
    json_str = texto[inicio:fin + 1]
    try:
        data = json.loads(json_str)
        if "cambios" in data and isinstance(data["cambios"], list):
            return data
        return None
    except json.JSONDecodeError:
        return None


# ============================================
# EDITAR WEB
# ============================================

def editar_web_v2(usuario_id, web_id, instruccion, contexto_negocio="", html_actual=None):
    print("=" * 60)
    print("EDITANDO WEB (ESTRUCTURADO) - V2.2")
    print("=" * 60)
    print("Instruccion: " + instruccion[:100])

    if gateway is None:
        return {
            "exito": False, "html_anterior": None, "html_nuevo": None,
            "intentos": 0, "error": "Gateway no disponible",
            "cambios_aplicados": 0, "aplicados": [], "fallidos": [],
            "cambios_totales": 0
        }

    if html_actual is None:
        try:
            from utils.web_storage import leer_web
        except ImportError:
            from web_storage import leer_web
        resultado_lectura = leer_web(usuario_id, web_id)
        if not resultado_lectura["exito"]:
            return {
                "exito": False, "html_anterior": None, "html_nuevo": None,
                "intentos": 0, "error": "No se pudo leer: " + str(resultado_lectura.get("error")),
                "cambios_aplicados": 0, "aplicados": [], "fallidos": [],
                "cambios_totales": 0
            }
        html_actual = resultado_lectura["html"]

    print("HTML leido: " + str(len(html_actual)) + " caracteres")

    print("\nExtrayendo estructura del HTML...")
    estructura = extraer_estructura_html(html_actual)
    print("Estructura: " + str(len(estructura)) + " caracteres (resumida)")

    for intento in range(1, MAX_INTENTOS + 1):
        print("\n" + "-" * 60)
        print("INTENTO " + str(intento) + "/" + str(MAX_INTENTOS))
        print("-" * 60)

        try:
            print("Construyendo prompt estructurado...")
            prompt = generar_prompt_edicion_estructurada(estructura, instruccion, contexto_negocio)
            print("Prompt: " + str(len(prompt)) + " caracteres")

            print("Llamando a la IA...")
            sistema = "Eres un editor web estructurado. Devuelves SOLO JSON con los cambios."
            respuesta, fuente = gateway.chat_inteligente(prompt, sistema)

            print("Respuesta de: " + fuente)
            print("Longitud: " + str(len(respuesta)) + " caracteres")

            print("Parseando JSON de cambios...")
            data = parsear_json_cambios(respuesta)

            if not data:
                print("[WARN] Respuesta no tiene JSON valido")
                time.sleep(TIEMPO_ESPERA)
                continue

            cambios = data.get("cambios", [])
            explicacion = data.get("explicacion", "")
            print("Cambios detectados: " + str(len(cambios)))
            if explicacion:
                print("Explicacion: " + explicacion[:100])

            if not cambios:
                print("[WARN] La IA no propuso cambios")
                time.sleep(TIEMPO_ESPERA)
                continue

            print("Aplicando cambios al HTML...")
            resultado_patcher = aplicar_cambios(html_actual, cambios)

            print("Cambios aplicados: " + str(resultado_patcher["cambios_aplicados"]) + "/" + str(len(cambios)))

            print("\n--- APLICADOS ---")
            for a in resultado_patcher.get("aplicados", []):
                print("  OK: " + a["descripcion"])

            print("\n--- FALLIDOS ---")
            for f in resultado_patcher.get("fallidos", []):
                print("  FALLO: " + f["descripcion"] + " | " + f["razon"])

            if not resultado_patcher["exito"]:
                print("[WARN] Ningun cambio se pudo aplicar")
                time.sleep(TIEMPO_ESPERA)
                continue

            html_nuevo = resultado_patcher["html_nuevo"]

            print("Validando HTML...")
            validacion = validar_html_editado(html_nuevo)
            print("Valido: " + str(validacion["valido"]))

            if not validacion["valido"]:
                print("HTML con errores criticos. Reintentando...")
                time.sleep(TIEMPO_ESPERA)
                continue

            print("\n" + "=" * 60)
            print("WEB EDITADA EXITOSAMENTE - V2.2")
            print("=" * 60)

            return {
                "exito": True,
                "html_anterior": html_actual,
                "html_nuevo": html_nuevo,
                "intentos": intento,
                "fuente": fuente,
                "cambios_aplicados": resultado_patcher["cambios_aplicados"],
                "cambios_totales": len(cambios),
                "aplicados": resultado_patcher.get("aplicados", []),
                "fallidos": resultado_patcher.get("fallidos", []),
                "explicacion": explicacion,
                "error": None
            }

        except Exception as e:
            print("Error en intento " + str(intento) + ": " + str(e))
            time.sleep(TIEMPO_ESPERA)

    return {
        "exito": False, "html_anterior": html_actual, "html_nuevo": None,
        "intentos": MAX_INTENTOS, "fuente": None,
        "cambios_aplicados": 0, "aplicados": [], "fallidos": [],
        "cambios_totales": 0,
        "error": "No se pudieron aplicar cambios tras " + str(MAX_INTENTOS) + " intentos"
    }


def editar_y_guardar_v2(usuario_id, web_id, instruccion, contexto_negocio=""):
    print("=" * 60)
    print("EDITANDO Y GUARDANDO WEB (V2.2)")
    print("=" * 60)

    resultado = editar_web_v2(usuario_id, web_id, instruccion, contexto_negocio)

    if not resultado["exito"]:
        return {
            "exito": False, "html_nuevo": None, "guardado": False,
            "error": resultado["error"],
            "cambios_aplicados": 0,
            "cambios_totales": 0,
            "aplicados": [],
            "fallidos": resultado.get("fallidos", [])
        }

    print("\nGuardando HTML editado...")
    try:
        from utils.web_storage import guardar_en_archivos
    except ImportError:
        from web_storage import guardar_en_archivos

    resultado_guardado = guardar_en_archivos(usuario_id, web_id, resultado["html_nuevo"])

    if resultado_guardado["exito"]:
        print("HTML guardado: " + resultado_guardado["ruta"])

    return {
        "exito": True,
        "html_nuevo": resultado["html_nuevo"],
        "guardado": resultado_guardado["exito"],
        "ruta": resultado_guardado.get("ruta"),
        "cambios_aplicados": resultado.get("cambios_aplicados", 0),
        "cambios_totales": resultado.get("cambios_totales", 0),
        "aplicados": resultado.get("aplicados", []),
        "fallidos": resultado.get("fallidos", []),
        "explicacion": resultado.get("explicacion", ""),
        "error": None
    }


# ============================================
# TEST
# ============================================

def test_editor():
    print("=" * 60)
    print("TEST EDITOR ESTRUCTURADO V2.2")
    print("=" * 60)

    if gateway is None:
        print("Gateway no disponible")
        return

    html_test = """<!DOCTYPE html>
<html><head>
<style>
body { background: #ffffff; }
h1 { color: #0f3460; }
</style>
</head><body>
<header><h1>Dulceria El Cielo</h1></header>
<main>
<div class="producto">
<img src="" alt="Cupcakes">
<h2>Cupcakes</h2>
</div>
<div class="producto">
<img src="" alt="Bombones">
<h2>Bombones</h2>
</div>
</main>
</body></html>"""

    print("\nHTML test: " + str(len(html_test)) + " caracteres")

    resultado = editar_web_v2(
        "usuario_test", "web_test",
        "ponle imagenes de dulces a los cuadros vacios y cambia el titulo a rojo",
        contexto_negocio="Dulceria con cupcakes y bombones",
        html_actual=html_test
    )

    if resultado["exito"]:
        print("\n" + "=" * 60)
        print("EXITO")
        print("=" * 60)
        print("Cambios aplicados: " + str(resultado["cambios_aplicados"]) + "/" + str(resultado["cambios_totales"]))

        print("\n--- APLICADOS ---")
        for a in resultado.get("aplicados", []):
            print("  OK: " + a["descripcion"])

        print("\n--- FALLIDOS ---")
        for f in resultado.get("fallidos", []):
            print("  FALLO: " + f["descripcion"] + " | " + f["razon"])
    else:
        print("\nFALLO: " + str(resultado["error"]))
        for f in resultado.get("fallidos", []):
            print("  " + f["descripcion"] + " | " + f["razon"])


if __name__ == "__main__":
    test_editor()