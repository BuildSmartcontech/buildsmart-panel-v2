# utils/web_prompts_data.py
# ============================================
# CONSTANTES Y CONSTRUCTORES DE PROMPTS WEB
# ============================================
# V3.0: Forza el diseño Dark Premium (fondo oscuro)
#       e inyección obligatoria de {{FORMULARIO}}
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
Tu responsabilidad es entregar paginas web de nivel premium, sin excepciones.

PROCESO DE TRABAJO:
1. Analiza el brief. Detecta el tipo de cliente (tech, creativo, corporativo).
2. Aplica SIEMPRE un estandar premium: tipografia elegante, espaciado generoso, animaciones sutiles.
3. El resultado debe notarse moderno y de alto nivel a simple vista.

ESTANDARES PREMIUM OBLIGATORIOS:
- Tipografia profesional (Google Fonts: Inter, Space Grotesk, Playfair Display).
- Efecto "Glassmorphism" en cards y navbar.
- Animaciones CSS avanzadas (scroll-driven, hover magnético).
""" + EFECTOS_AVANZADOS_PROMPT

REGLAS_CSS_PREMIUM = """
### DISENO PREMIUM OBLIGATORIO (CRITICO):

**ESTILO GENERAL (DARK PREMIUM):**
- Fondo general: Oscuro profundo (#050A14 o #0F172A).
- Textos principales: Blanco (#FFFFFF) o gris muy claro (#F8FAFC).
- Textos secundarios: Gris azulado (#94A3B8).
- Acentos: Degradados vibrantes (ej. cyan #00D4FF, azul #0077FF, purpura #8B5CF6).

**CARDS (Efecto Cristal):**
.card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 32px;
    transition: all 0.3s ease;
}
.card:hover {
    transform: translateY(-5px);
    border-color: rgba(0, 212, 255, 0.3);
    box-shadow: 0 10px 30px rgba(0, 212, 255, 0.1);
}

**BOTONES:**
.btn {
    background: linear-gradient(90deg, #00D4FF 0%, #0077FF 100%);
    color: #FFFFFF;
    padding: 14px 32px;
    border-radius: 50px;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
}
.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0, 212, 255, 0.3);
}

**FORMULARIO (CRITICO):**
- Los inputs deben tener fondo oscuro (rgba(255,255,255,0.05)) y texto blanco.
- Border: 1px solid rgba(255,255,255,0.1).
- Border-radius: 8px. Padding: 12px.
"""

REGLAS_CODIGO = (
    "### REGLAS DE CODIGO:\n"
    "1. Empezar con <!DOCTYPE html> y terminar con </html>.\n"
    "2. Incluir <html>, <head>, <body> completas.\n"
    "3. En <head>: meta charset, meta viewport, meta description, title, style.\n"
    "4. CSS embebido en <style>.\n"
    "5. HTML5 semantico y Responsive (mobile-first).\n"
    "6. Minimo 3000 caracteres.\n\n"
    "### COLORES Y FONDO:\n"
    "OBLIGATORIO: Fondo oscuro (#050A14). NO uses fondos blancos.\n"
    "OBLIGATORIO: Textos blancos o grises claros.\n\n"
)

REGLAS_IMAGENES = (
    "### IMAGENES (CRITICO - usar marcadores EXACTOS):\n"
    "HERO (1 vez):\n"
    "   <img src=\"{{HERO_IMAGE}}\" alt=\"Imagen principal\" style=\"width:100%;height:auto;border-radius:20px;\">\n"
    "SERVICIOS / PRODUCTOS (4 veces, SIN excepcion):\n"
    "   <div class=\"card\">\n"
    "     <img src=\"{{SERVICIO_1}}\" alt=\"[nombre]\" style=\"width:100%;height:200px;object-fit:cover;border-radius:12px;\">\n"
    "     <h3>[Nombre]</h3><p>[Descripcion]</p>\n"
    "   </div>\n"
    "   (Repetir para SERVICIO_2, SERVICIO_3, SERVICIO_4).\n"
    "NO inventes otras etiquetas. NO uses URLs directas.\n"
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
    # (Se mantiene igual que en tu archivo actual, no requiere cambios)
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
        instrucciones.append(f"\n### UBICACION:\n- Direccion: {direccion}\n- Ciudad: {ciudad}\n- Pais: {pais or 'no especificado'}\n")
        secciones_extra.append("Ubicacion")
    if horarios:
        instrucciones.append(f"\n### HORARIOS:\n- Horarios: {horarios}\n")
        secciones_extra.append("Horarios")
    redes = []
    if instagram: redes.append(f"Instagram: @{instagram.lstrip('@')}")
    if facebook: redes.append(f"Facebook: {facebook}")
    if tiktok: redes.append(f"TikTok: @{tiktok.lstrip('@')}")
    if redes:
        instrucciones.append("\n### REDES:\n" + "\n".join([f"- {r}" for r in redes]) + "\n")
    if anio:
        instrucciones.append(f"\n### HISTORIA:\n- Ano de fundacion: {anio}\n")
    if email_contacto:
        instrucciones.append(f"\n### EMAIL:\n- Incluye el email {email_contacto} en contacto.\n")
    if whatsapp:
        wa_limpio = whatsapp.replace("+", "").replace(" ", "")
        instrucciones.append(f"\n### WHATSAPP:\n- Boton: <a href=\"https://wa.me/{wa_limpio}\" class=\"btn\">WhatsApp</a>\n")

    if secciones_extra:
        instrucciones.insert(0, "\n### SECCIONES EXTRA:\n" + "\n".join([f"- {s}" for s in secciones_extra]) + "\n")
    return "\n".join(instrucciones)

def construir_reglas_contenido(sector, lista_negra):
    return (
        "\n## REGLAS DE CONTENIDO\n"
        "### PROHIBIDO USAR:\n" + lista_negra + "\n\n"
        "### ANTI-ALUCINACION:\n"
        "1. NO INVENTES telefonos, direcciones, emails o nombres.\n"
        "2. SOLO usa los datos proporcionados.\n"
        "3. Lenguaje natural y directo.\n\n"
    )