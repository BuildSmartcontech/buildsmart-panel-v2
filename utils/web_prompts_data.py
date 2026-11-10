# utils/web_prompts_data.py
# ============================================
# CONSTANTES Y CONSTRUCTORES DE PROMPTS WEB
# ============================================
# V4.0: Master Template (Fuerza tipografia Tech, Bento Grid y Glassmorphism)
# ============================================

PALABRAS_PROHIBIDAS = [
    "en el mundo actual", "en la era digital", "es importante destacar",
    "cabe mencionar", "sin lugar a dudas", "en conclusion", "en resumen",
    "en definitiva", "en primer lugar", "en segundo lugar", "por otro lado",
    "asimismo", "de igual manera", "no obstante", "por lo tanto",
    "en el ambito de", "en el contexto de", "en la actualidad", "hoy en dia",
    "es fundamental", "es crucial", "es esencial", "juega un papel",
    "desempena un papel", "un abanico de", "un sinfin de", "un mundo de",
    "la clave del exito", "el secreto del exito", "una amplia gama",
    "una gran variedad", "soluciones integrales", "soluciones innovadoras",
    "soluciones personalizadas", "experiencia unica", "servicio excepcional",
    "calidad inigualable", "compromiso total", "atencion al detalle",
    "pasion por", "vision de futuro",
]

EFECTOS_AVANZADOS_PROMPT = """
EFECTOS VISUALES AVANZADOS (estilo React Bits, en CSS/JS vanilla):
- Texto animado: split-text, blur-text, shiny-text, count-up
- Fondos animados: gradientes animados, particulas sutiles, malla radial
- Cards interactivas: spotlight-card, hover-magnet
Implementar con CSS puro o JS vanilla. PROHIBIDO frameworks.
"""

DIRECTOR_DE_ARTE_PROMPT = """
Eres el Director de Arte y Disenador Frontend Senior del equipo.
Tu unico objetivo es entregar paginas web de nivel PREMIUM, MODERNAS y de ALTA GAMA.

PROCESO OBLIGATORIO:
1. Analiza el sector: Si es Tecnologia/Software, NO USES SERIF. Usa tipografia Sans-Serif moderna.
2. Aplica SIEMPRE un diseno "Bento Grid" (tarjetas organizadas en cuadricula).
3. Usa efectos de "Glassmorphism" (fondos semitransparentes con desenfoque).

ESTANDARES PREMIUM OBLIGATORIOS (Si no cumples esto, fallas):
- Tipografia: Usa SIEMPRE Google Fonts 'Plus Jakarta Sans' o 'Inter'. PROHIBIDO usar fuentes de revista (Playfair, Lora, Times) en sectores Tech.
- Fondos: Oscuro profundo (#0B0F19).
- Tarjetas: Fondo semi-transparente (rgba(255,255,255,0.03)), borde sutil (rgba(255,255,255,0.1)) y sombra interior.
- Botones: Degradados vibrantes (Cyan #00D4FF a Azul #0077FF).
- El resultado debe verse como una Startup de Silicon Valley valorada en millones.
""" + EFECTOS_AVANZADOS_PROMPT

REGLAS_CSS_PREMIUM = """
### DISENO PREMIUM OBLIGATORIO (CRITICO - COPIA ESTAS REGLAS):

**1. VARIABLES GLOBALES Y RESET:**
:root {
    --bg: #0B0F19;
    --card-bg: rgba(255, 255, 255, 0.03);
    --border: rgba(255, 255, 255, 0.08);
    --text: #F8FAFC;
    --text-muted: #94A3B8;
    --primary: #00D4FF;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    background-color: var(--bg);
    color: var(--text);
    font-family: 'Plus Jakarta Sans', sans-serif;
    line-height: 1.6;
}

**2. NAVEGACION (Fija y elegante):**
nav {
    padding: 20px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(11, 15, 25, 0.8);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--border);
    position: sticky; top: 0; z-index: 100;
}
nav a { color: var(--text); text-decoration: none; font-weight: 500; margin-left: 20px; }

**3. HERO SECTION (El impacto visual):**
.hero {
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 100px 20px;
    background: radial-gradient(circle at 50% 0%, rgba(0, 212, 255, 0.15) 0%, var(--bg) 70%);
}
.hero h1 {
    font-size: 4rem;
    font-weight: 800;
    letter-spacing: -2px;
    background: linear-gradient(90deg, #FFF, #00D4FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 24px;
    max-width: 800px;
}

**4. BENTO GRID (Servicios):**
.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
    padding: 80px 20px;
    max-width: 1200px;
    margin: 0 auto;
}
.card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 32px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
}
.card:hover {
    transform: translateY(-8px);
    border-color: rgba(0, 212, 255, 0.4);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}
.card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 16px;
    margin-bottom: 20px;
}

**5. BOTONES (CTA):**
.btn {
    display: inline-block;
    padding: 16px 32px;
    background: linear-gradient(135deg, #00D4FF 0%, #0077FF 100%);
    color: #FFF;
    font-weight: 700;
    border-radius: 100px;
    text-decoration: none;
    transition: all 0.3s ease;
    box-shadow: 0 10px 20px rgba(0, 119, 255, 0.2);
}
.btn:hover { transform: scale(1.05); box-shadow: 0 15px 30px rgba(0, 119, 255, 0.4); }

**6. FORMULARIO DE CONTACTO:**
.contacto { padding: 80px 20px; max-width: 600px; margin: 0 auto; }
input, textarea {
    width: 100%; padding: 16px;
    background: rgba(255,255,255,0.05);
    border: 1px solid var(--border);
    border-radius: 12px;
    color: #FFF; margin-bottom: 16px;
    font-family: inherit;
}
input:focus { outline: none; border-color: var(--primary); }
"""

REGLAS_SECCION_UBICACION = """
### SECCION UBICACION (OBLIGATORIA porque hay direccion):
Genera una seccion <section id="ubicacion" class="ubicacion"> con:
1. Titulo "Donde estamos" o "Visitanos"
2. Mapa embebido de Google Maps usando iframe.
"""

REGLAS_SECCION_HORARIOS = """
### SECCION HORARIOS (OBLIGATORIA porque hay horarios):
Genera una seccion <section id="horarios" class="horarios"> con:
1. Titulo "Horarios de atencion"
2. Card premium con la lista de horarios.
"""

REGLAS_REDES_SOCIALES = """
### REDES SOCIALES EN FOOTER:
En el footer, agrega una fila de iconos SVG inline para las redes que existan.
Usa SVGs oficiales simples. NO uses librerias externas.
"""

REGLAS_CODIGO = (
    "### REGLAS DE CODIGO:\n"
    "1. Empezar con <!DOCTYPE html> y terminar con </html>.\n"
    "2. Incluir <html>, <head>, <body> completas.\n"
    "3. En <head>: meta charset, meta viewport, title, y el CDN de Google Fonts para 'Plus Jakarta Sans'.\n"
    "4. CSS embebido en <style> respetando ESTRICTAMENTE el 'DISENO PREMIUM OBLIGATORIO'.\n"
    "5. Minimo 3000 caracteres.\n\n"
)

REGLAS_IMAGENES = (
    "### IMAGENES (CRITICO):\n"
    "USA EXACTAMENTE el marcador {{HERO_IMAGE}} para la imagen principal.\n"
    "USA EXACTAMENTE los marcadores {{SERVICIO_1}}, {{SERVICIO_2}}, {{SERVICIO_3}} para las tarjetas.\n"
    "NO uses URLs reales, solo los marcadores.\n"
)

REGLAS_FORMULARIO = (
    "### FORMULARIO DE CONTACTO (CRITICO):\n"
    "En la seccion de Contacto, DEBES incluir EXACTAMENTE este bloque:\n"
    "<div id=\"formulario-contacto\">{{FORMULARIO}}</div>\n"
    "NO crees tu propio <form> en HTML. Solo pon el div con el marcador.\n"
)

REGLAS_SALIDA = (
    "### FORMATO DE SALIDA:\n"
    "Devuelve SOLO el HTML, empezando con <!DOCTYPE html> y terminando con </html>.\n"
    "SIN explicaciones, SIN bloques markdown.\n\n"
    "Genera el HTML completo ahora:"
)

def construir_instrucciones_dinamicas(datos_negocio):
    """Genera instrucciones condicionales segun campos disponibles."""
    instrucciones = []
    secciones_extra = []

    direccion = (datos_negocio.get("direccion") or "").strip()
    ciudad = (datos_negocio.get("ciudad") or "").strip()
    pais = (datos_negocio.get("pais") or "").strip()
    horarios = (datos_negocio.get("horarios") or "").strip()
    instagram = (datos_negocio.get("instagram") or "").strip()
    facebook = (datos_negocio.get("facebook") or "").strip()
    tiktok = (datos_negocio.get("tiktok") or "").strip()
    anio = (datos_negocio.get("anio_fundacion") or "").strip()
    email_contacto = (datos_negocio.get("email_contacto") or "").strip()
    whatsapp = (datos_negocio.get("whatsapp_negocio") or "").strip()

    if direccion and ciudad:
        instrucciones.append(
            "\n### DATOS PARA SECCION UBICACION:\n"
            "- Direccion: " + direccion + "\n"
            "- Ciudad: " + ciudad + "\n"
            "- Pais: " + (pais or "no especificado") + "\n"
        )
        instrucciones.append(REGLAS_SECCION_UBICACION)
        secciones_extra.append("Ubicacion")

    if horarios:
        instrucciones.append(
            "\n### DATOS PARA SECCION HORARIOS:\n- Horarios: " + horarios + "\n"
        )
        instrucciones.append(REGLAS_SECCION_HORARIOS)
        secciones_extra.append("Horarios")

    redes = []
    if instagram: redes.append("Instagram: @" + instagram.lstrip("@"))
    if facebook: redes.append("Facebook: " + facebook)
    if tiktok: redes.append("TikTok: @" + tiktok.lstrip("@"))

    if redes:
        instrucciones.append(
            "\n### DATOS PARA REDES SOCIALES:\n" +
            "\n".join(["- " + r for r in redes]) + "\n"
        )
        instrucciones.append(REGLAS_REDES_SOCIALES)

    if anio:
        instrucciones.append("\n### DATO HISTORICO:\n- Ano de fundacion: " + anio + "\n")

    if email_contacto:
        instrucciones.append("\n### EMAIL DE CONTACTO:\n- Incluye el email " + email_contacto + " en la seccion de contacto.\n")

    if whatsapp:
        wa_limpio = whatsapp.replace("+", "").replace(" ", "")
        instrucciones.append("\n### WHATSAPP:\n- Boton: <a href=\"https://wa.me/" + wa_limpio + "\" class=\"btn\">WhatsApp</a>\n")

    if secciones_extra:
        instrucciones.insert(
            0,
            "\n### SECCIONES EXTRA REQUERIDAS:\n" +
            "\n".join(["- " + s for s in secciones_extra]) + "\n\nORDEN SUGERIDO: Hero, Servicios, Sobre Nosotros, "
            + ", ".join(secciones_extra) + ", Contacto\n"
        )
    return "\n".join(instrucciones)


def construir_reglas_contenido(sector, lista_negra):
    """Reglas de contenido con datos dinamicos."""
    return (
        "\n## REGLAS DE CONTENIDO\n\n"
        "### PROHIBIDO USAR ESTAS FRASES:\n" + lista_negra + "\n\n"
        "### ANTI-ALUCINACION (CRITICO):\n"
        "1. PROHIBIDO INVENTAR numeros de telefono.\n"
        "2. PROHIBIDO INVENTAR direcciones.\n"
        "3. PROHIBIDO INVENTAR emails.\n"
        "4. PROHIBIDO INVENTAR anos de fundacion.\n"
        "5. PROHIBIDO INVENTAR nombres de clientes.\n"
        "6. PROHIBIDO INVENTAR certificaciones o premios.\n"
        "7. Si falta info, usa texto generico sin datos.\n"
        "8. SOLO usa los datos que aparecen en la seccion DATOS.\n\n"
        "### REGLAS DE ESTILO:\n"
        "1. NO uses rayas largas.\n"
        "2. NO uses emojis en el contenido.\n"
        "3. NO uses frases genericas de IA.\n"
        "4. SI usa ejemplos del sector " + sector + ".\n"
        "5. SI usa lenguaje natural y directo.\n\n"
    )


if __name__ == "__main__":
    print("=" * 60)
    print("TEST WEB PROMPTS DATA V4.0 (Master Template)")
    print("=" * 60)
    print("Palabras prohibidas: " + str(len(PALABRAS_PROHIBIDAS)))
    print("Director de Arte: " + str(len(DIRECTOR_DE_ARTE_PROMPT)) + " chars")
    print("Reglas CSS: " + str(len(REGLAS_CSS_PREMIUM)) + " chars")
    print("Reglas Ubicacion: " + str(len(REGLAS_SECCION_UBICACION)) + " chars")
    print("Reglas Horarios: " + str(len(REGLAS_SECCION_HORARIOS)) + " chars")
    print("Reglas Redes: " + str(len(REGLAS_REDES_SOCIALES)) + " chars")
    print("Reglas Imagenes: " + str(len(REGLAS_IMAGENES)) + " chars")
    print("Reglas Formulario: " + str(len(REGLAS_FORMULARIO)) + " chars")
    print("=" * 60)