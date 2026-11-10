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

REGLAS_SECCION_UBICACION = """
### SECCION UBICACION (OBLIGATORIA porque hay direccion):

Genera una seccion <section id="ubicacion" class="ubicacion"> con:
1. Titulo "Donde estamos" o "Visitanos"
2. Layout en 2 columnas (grid):
   - Columna izquierda: datos de direccion con icono SVG de pin + ciudad + pais
   - Columna derecha: mapa embebido de Google Maps
3. El mapa usa iframe SIN API key:
   <iframe src="https://www.google.com/maps?q=DIRECCION,CIUDAD&output=embed"
           width="100%" height="400" style="border:0;border-radius:16px;"
           loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
4. Estilos premium: card con sombra, border-radius 16px, hover sutil
5. Responsive: en mobile se apila en 1 columna

IMPORTANTE:
- URL-encode la direccion y ciudad (espacios a %20, comas a %2C)
- Usa el formato exacto: https://www.google.com/maps?q=DIRECCION,CIUDAD&output=embed
- NO uses la API de Google Maps (no tenemos key)
"""

REGLAS_SECCION_HORARIOS = """
### SECCION HORARIOS (OBLIGATORIA porque hay horarios):

Genera una seccion <section id="horarios" class="horarios"> con:
1. Titulo "Horarios de atencion"
2. Card premium con la lista de horarios
3. Si el texto tiene formato "Lun-Vie 8am-6pm, Sab 9am-1pm":
   - Separa por comas y genera filas <div class="horario-row">
   - Cada fila: <span class="horario-dia">...</span> <span class="horario-hora">...</span>
4. Estilos: fondo blanco, border-radius 16px, padding 24px, hover sutil
5. Anade badge verde si dice "Abierto ahora" (opcional)
"""

REGLAS_REDES_SOCIALES = """
### REDES SOCIALES EN FOOTER (OBLIGATORIO si hay redes):

En el footer, agrega una fila de iconos SVG inline para las redes que existan:
- Instagram: https://instagram.com/{usuario}
- Facebook: https://facebook.com/{usuario}
- TikTok: https://tiktok.com/@{usuario}

Formato HTML:
<a href="URL_RED" target="_blank" rel="noopener" class="social-icon" aria-label="Instagram">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
    <!-- path SVG de la red -->
  </svg>
</a>

Estilos:
.social-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: rgba(255,255,255,0.1);
    color: #ffffff;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    margin: 0 8px;
}
.social-icon:hover {
    transform: translateY(-3px);
    background: rgba(255,255,255,0.2);
}

Usa SVGs oficiales simples (path de 24x24). NO uses librerias externas.
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
    if instagram:
        redes.append("Instagram: @" + instagram.lstrip("@"))
    if facebook:
        redes.append("Facebook: " + facebook)
    if tiktok:
        redes.append("TikTok: @" + tiktok.lstrip("@"))

    if redes:
        instrucciones.append(
            "\n### DATOS PARA REDES SOCIALES:\n" +
            "\n".join(["- " + r for r in redes]) +
            "\n"
        )
        instrucciones.append(REGLAS_REDES_SOCIALES)

    if anio:
        instrucciones.append(
            "\n### DATO HISTORICO:\n"
            "- Ano de fundacion: " + anio + "\n"
            "- Mencionalo en la seccion 'Sobre nosotros' de forma natural.\n"
        )

    if email_contacto:
        instrucciones.append(
            "\n### EMAIL DE CONTACTO:\n"
            "- Incluye el email " + email_contacto + " en la seccion de contacto.\n"
        )

    if whatsapp:
        wa_limpio = whatsapp.replace("+", "").replace(" ", "")
        instrucciones.append(
            "\n### WHATSAPP:\n"
            "- Incluye un boton/enlace de WhatsApp con el numero " + whatsapp + ".\n"
            "- Formato: <a href=\"https://wa.me/" + wa_limpio + "\" class=\"btn\">WhatsApp</a>\n"
        )

    if secciones_extra:
        instrucciones.insert(
            0,
            "\n### SECCIONES EXTRA REQUERIDAS:\n" +
            "\n".join(["- " + s for s in secciones_extra]) +
            "\n\nORDEN SUGERIDO: Hero, Servicios, Sobre Nosotros, "
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
    print("TEST WEB PROMPTS DATA V3.0")
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