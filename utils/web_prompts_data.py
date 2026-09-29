# utils/web_prompts_data.py
# ============================================
# CONSTANTES Y CONSTRUCTORES DE PROMPTS WEB
# ============================================
# V2.1: Reglas reforzadas CSS + Imagenes exactas
# V2.0: Instrucciones dinamicas para secciones nuevas
# V1.1: EFECTOS_AVANZADOS_PROMPT (React Bits)
# V1.0: Extraido de web_prompts.py
# ============================================


# ============================================
# PALABRAS PROHIBIDAS
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


# ============================================
# EFECTOS VISUALES AVANZADOS
# ============================================
EFECTOS_AVANZADOS_PROMPT = """

EFECTOS VISUALES AVANZADOS (estilo React Bits, en CSS/JS vanilla):
- Texto animado: split-text, blur-text, shiny-text, count-up
- Cursor personalizado: blob-cursor, magnet
- Fondos animados: gradientes animados, particulas sutiles, malla radial
- Cards interactivas: spotlight-card, hover-magnet
- Contenido animado: fadeContent (fade + slide suave)
- Stack: cards apiladas que se despliegan al scroll

Implementar con CSS puro o JS vanilla.
PROHIBIDO importar React, Vue, Angular o frameworks.
PROHIBIDO usar CDN de librerias (excepto Google Fonts).
Objetivo: look-and-feel React Bits SIN dependencias.
"""


# ============================================
# DIRECTOR DE ARTE
# ============================================
DIRECTOR_DE_ARTE_PROMPT = """
Eres el Director de Arte y Disenador Frontend Senior del equipo.
Tu responsabilidad es entregar paginas web de nivel premium, sin excepciones.

PROCESO DE TRABAJO:
1. Analiza el brief recibido.
2. Detecta el tipo de cliente/proyecto: creativo, lujo, startup,
   ingeniero, arquitecto, corporativo, tecnico.
3. Adapta el estilo de diseno al contexto, manteniendo SIEMPRE
   un estandar premium alto.
4. Genera la pagina completa priorizando calidad visual, claridad
   y percepcion de alto nivel.

ESTANDARES PREMIUM OBLIGATORIOS:
- Tipografia elegida con criterio profesional (Google Fonts).
- Espaciado generoso y ritmo visual claro.
- Jerarquia visual fuerte (tamanos, pesos, contraste).
- Paleta de colores sofisticada y coherente.
- Detalles cuidados: hover, transiciones, sombras sutiles, bordes.
- Animaciones CSS avanzadas:
    * scroll-driven animations (animation-timeline: view())
    * entradas elegantes y micro-interacciones discretas
- Soporte para prefers-reduced-motion.
- El resultado debe notarse premium a simple vista.

DIFERENCIACION DE ESTILO:
- Cliente creativo / lujo / marca: mas personalidad y elegancia expresiva.
- Cliente tecnico / ingeniero / empresa grande: mas sobriedad, precision.

ENTREGA:
- HTML + CSS limpio, moderno y bien estructurado.
- Animaciones CSS avanzadas integradas con criterio.
- Codigo organizado y listo para usar.
""" + EFECTOS_AVANZADOS_PROMPT


# ============================================
# REGLAS CSS PREMIUM (V2.1 reforzadas)
# ============================================
REGLAS_CSS_PREMIUM = """
### DISENO PREMIUM OBLIGATORIO:

**CARDS (tarjetas de servicios, productos, etc):**
.card, .service-card, .producto, .servicio {
    background: #ffffff;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    padding: 24px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid #f0f0f0;
}
.card:hover, .service-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.15);
}

**BOTONES:**
.btn, .button, .cta {
    background: [COLOR_PRIMARIO];
    color: #ffffff;
    padding: 14px 32px;
    border-radius: 50px;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
}
.btn:hover, .button:hover, .cta:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}

**IMAGENES dentro de cards:**
.card img {
    border-radius: 12px;
    width: 100%;
    height: 200px;
    object-fit: cover;
}

**HERO:**
- Imagen redondeada (border-radius: 20px)
- Padding generoso (min 80px vertical)
- Boton principal flotante

### ANIMACIONES SEGURAS (CRITICO):

REGLA DE ORO: NUNCA uses opacity: 0 como estado inicial de textos sin una animacion CONFIRMADA que los vuelva a opacity:1.

Patron OBLIGATORIO para animaciones scroll:

.animate-on-scroll {
    opacity: 0;
    transform: translateY(20px);
    animation: fadeUp 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    animation-timeline: view();
    animation-range: entry 0% cover 30%;
}
@keyframes fadeUp {
    to { opacity: 1; transform: translateY(0); }
}
@supports not (animation-timeline: view()) {
    .animate-on-scroll {
        opacity: 1 !important;
        transform: none !important;
        animation: none !important;
    }
}
@media (prefers-reduced-motion: reduce) {
    .animate-on-scroll {
        opacity: 1 !important;
        transform: none !important;
        animation: none !important;
    }
}

PROHIBIDO:
- opacity: 0 sin animation-fill-mode: forwards
- opacity: 0 sin @supports not (animation-timeline) fallback
- Animaciones con duracion mayor a 1.5s para textos principales
- Textos con color: #ccc, #ddd, #eee, #f0f0f0

### CONTRASTE DE TEXTO (CRITICO):

1. Textos sobre fondo BLANCO: usar #1a1a1a, #222, #333 o #4a5568 (minimo).
2. Textos secundarios (subtitulos): minimo #4a5568 sobre blanco.
3. Textos sobre fondo OSCURO: usar #ffffff o #f8f9fa.
4. PROHIBIDO: #ccc, #ddd, #eee, #f0f0f0, rgba(0,0,0,0.3) para texto.
5. PROHIBIDO: usar opacity en el contenedor padre (afecta hijos).

REGLAS ADICIONALES:
1. Usa GRID o FLEX (grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)))
2. Gap entre cards: 24px minimo
3. NO uses tablas para layout
4. NO uses estilos inline (usa clases)
5. Todas las cards DEBEN tener hover effect
6. Todos los botones DEBEN tener border-radius de al menos 8px
7. Los inputs deben tener border-radius y border suave
"""


# ============================================
# SECCION UBICACION
# ============================================
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


# ============================================
# SECCION HORARIOS
# ============================================
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


# ============================================
# REDES SOCIALES
# ============================================
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


# ============================================
# INSTRUCCIONES DINAMICAS
# ============================================
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
            "- Formato: <a href=\"https://wa.me/" + wa_limpio + "\">WhatsApp</a>\n"
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


# ============================================
# REGLAS DE CONTENIDO
# ============================================
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


# ============================================
# REGLAS DE CODIGO
# ============================================
REGLAS_CODIGO = (
    "### REGLAS DE CODIGO:\n"
    "1. Empezar con <!DOCTYPE html> y terminar con </html>.\n"
    "2. Incluir <html>, <head>, <body> completas.\n"
    "3. En <head>: meta charset, meta viewport, meta description, title, style.\n"
    "4. CSS embebido en <style>.\n"
    "5. Cerrar todas las etiquetas.\n"
    "6. HTML5 semantico.\n"
    "7. Responsive (mobile-first con media queries).\n"
    "8. Sin frameworks externos.\n"
    "9. Minimo 3000 caracteres.\n\n"
    "### PROHIBICIONES:\n"
    "PROHIBIDO prefers-color-scheme: dark.\n"
    "PROHIBIDO fondo negro.\n\n"
    "### COLORES:\n"
    "1. Fondo BLANCO (#ffffff) o gris claro (#f8f9fa).\n"
    "2. Texto OSCURO (#222222 o #333333).\n"
    "3. Hero PUEDE tener color de marca.\n\n"
)


# ============================================
# REGLAS DE IMAGENES (V2.1 reforzadas)
# ============================================
REGLAS_IMAGENES = (
    "### IMAGENES (CRITICO - usar marcadores EXACTOS):\n"
    "\n"
    "USA UNICAMENTE estos marcadores literales (NO inventes otros):\n"
    "\n"
    "HERO (1 vez):\n"
    "   <img src=\"{{HERO_IMAGE}}\" alt=\"Imagen principal\" style=\"width:100%;height:auto;border-radius:20px;\">\n"
    "\n"
    "SERVICIOS / PRODUCTOS (4 veces, SIN excepcion):\n"
    "   <div class=\"card\">\n"
    "     <img src=\"{{SERVICIO_1}}\" alt=\"[nombre]\" style=\"width:100%;height:200px;object-fit:cover;border-radius:12px;\">\n"
    "     <h3>[Nombre]</h3>\n"
    "     <p>[Descripcion]</p>\n"
    "   </div>\n"
    "   <div class=\"card\">\n"
    "     <img src=\"{{SERVICIO_2}}\" alt=\"[nombre]\">...\n"
    "   </div>\n"
    "   <div class=\"card\">\n"
    "     <img src=\"{{SERVICIO_3}}\" alt=\"[nombre]\">...\n"
    "   </div>\n"
    "   <div class=\"card\">\n"
    "     <img src=\"{{SERVICIO_4}}\" alt=\"[nombre]\">...\n"
    "   </div>\n"
    "\n"
    "PROHIBIDO usar: PRODUCTO_X, ARTICULO_X, ITEM_X, IMAGEN_X, FOTO_X.\n"
    "SOLO HERO_IMAGE y SERVICIO_1 hasta SERVICIO_4.\n"
    "\n"
    "PROHIBIDO div gris como placeholder.\n"
    "PROHIBIDO usar URLs directas de imagenes.\n\n"
)


# ============================================
# REGLAS DE SALIDA
# ============================================
REGLAS_SALIDA = (
    "### FORMATO DE SALIDA:\n"
    "Devuelve SOLO el HTML, empezando con <!DOCTYPE html> y terminando con </html>.\n"
    "SIN explicaciones, SIN bloques markdown.\n\n"
    "Genera el HTML completo ahora:"
)


# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    print("=" * 60)
    print("TEST WEB PROMPTS DATA V2.1")
    print("=" * 60)
    print("Palabras prohibidas: " + str(len(PALABRAS_PROHIBIDAS)))
    print("Director de Arte: " + str(len(DIRECTOR_DE_ARTE_PROMPT)) + " chars")
    print("Reglas CSS: " + str(len(REGLAS_CSS_PREMIUM)) + " chars")
    print("Reglas Ubicacion: " + str(len(REGLAS_SECCION_UBICACION)) + " chars")
    print("Reglas Horarios: " + str(len(REGLAS_SECCION_HORARIOS)) + " chars")
    print("Reglas Redes: " + str(len(REGLAS_REDES_SOCIALES)) + " chars")
    print("Reglas Imagenes: " + str(len(REGLAS_IMAGENES)) + " chars")
    print("")
    print("Verificaciones V2.1:")
    print("  Contraste texto:     " + ("SI" if "CONTRASTE DE TEXTO" in REGLAS_CSS_PREMIUM else "NO"))
    print("  Animaciones seguras: " + ("SI" if "ANIMACIONES SEGURAS" in REGLAS_CSS_PREMIUM else "NO"))
    print("  @supports fallback:  " + ("SI" if "@supports not" in REGLAS_CSS_PREMIUM else "NO"))
    print("  Marcadores exactos:  " + ("SI" if "marcadores EXACTOS" in REGLAS_IMAGENES else "NO"))
    print("  Prohibe PRODUCTO_X:  " + ("SI" if "PROHIBIDO usar" in REGLAS_IMAGENES else "NO"))
    print("=" * 60)