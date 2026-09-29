# utils/web_prompts_builder.py
# ============================================
# CONSTRUCTORES DE INSTRUCCIONES DINAMICAS
# ============================================
# V1.0: Extraido de web_prompts_data (split 400 lineas)
# ============================================

from utils.web_prompts_data import (
    REGLAS_SECCION_UBICACION,
    REGLAS_SECCION_HORARIOS,
    REGLAS_REDES_SOCIALES,
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