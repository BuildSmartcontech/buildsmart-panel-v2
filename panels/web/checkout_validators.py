# panels/web/checkout_validators.py
# ============================================
# VALIDADORES Y CONSTANTES DEL CHECKOUT
# ============================================
# V1.0: Extraido de checkout.py (split 400 lineas)
# ============================================

import re
from utils.paises import obtener_prefijo, PAISES_DEFAULT


SECTORES = [
    "Selecciona un sector...",
    "Alimentos y bebidas",
    "Restaurante / Comida rapida",
    "Panaderia / Pasteleria",
    "Cafeteria / Bar",
    "Moda / Ropa / Accesorios",
    "Belleza / Peluqueria / Spa",
    "Salud / Consultorio / Clinica",
    "Farmacia / Drogueria",
    "Servicios profesionales",
    "Tecnologia / Software",
    "Educacion / Academia",
    "Construccion / Remodelacion",
    "Inmobiliaria",
    "Automotriz / Taller",
    "Turismo / Agencia de viajes",
    "Hotel / Hospedaje",
    "Fitness / Gimnasio / Deporte",
    "Mascotas / Veterinaria",
    "Flores / Decoracion",
    "Joyeria / Relojeria",
    "Muebles / Hogar",
    "Manualidades / Artesanias",
    "Marketing / Publicidad",
    "Fotografia / Video",
    "Eventos / Catering",
    "Transporte / Logistica",
    "Agricultura / Ganaderia",
    "Ferreteria / Materiales",
    "Papeleria / Libreria",
    "Jugueteria",
    "Optica",
    "Licoreria",
    "Distribucion / Mayorista",
    "Manufactura / Fabrica",
    "Consultoria",
    "Contabilidad / Fiscal",
    "Legal / Abogados",
    "Arquitectura / Diseno",
    "Otro (especificar abajo)",
]


CAMPOS_OPCIONALES = [
    ("telefono",         "Tu telefono personal"),
    ("whatsapp_negocio", "WhatsApp del negocio"),
    ("email_contacto",   "Email del negocio"),
    ("direccion",        "Direccion fisica"),
    ("horarios",         "Horarios de atencion"),
    ("instagram",        "Instagram"),
    ("facebook",         "Facebook"),
    ("tiktok",           "TikTok"),
    ("anio_fundacion",   "Ano de fundacion"),
    ("publico_objetivo", "Publico objetivo"),
]


def normalizar_whatsapp(valor, prefijo="+57"):
    """Normaliza WhatsApp con prefijo (respeta +XX explicito)."""
    if not valor:
        return ""
    limpio = re.sub(r"[^\d+]", "", valor)
    if limpio.startswith("+"):
        return limpio
    return prefijo + limpio


def whatsapp_valido(valor):
    """Valida formato WhatsApp (10-15 digitos)."""
    if not valor:
        return True
    digitos = re.sub(r"\D", "", valor)
    return 10 <= len(digitos) <= 15


def normalizar_instagram(valor):
    """Limpia @ de Instagram."""
    if not valor:
        return ""
    return valor.strip().lstrip("@").lower()


def validar_formulario(datos_form, sector_sel, sector_otro):
    """Valida el formulario completo. Devuelve lista de errores."""
    errores = []

    if not datos_form["nombre"].strip():
        errores.append("Falta tu nombre")
    if not datos_form["email"].strip() or "@" not in datos_form["email"]:
        errores.append("Email invalido")
    if not datos_form["nombre_negocio"].strip():
        errores.append("Falta el nombre del negocio")
    if sector_sel == "Selecciona un sector...":
        errores.append("Selecciona un sector")
    if sector_sel == "Otro (especificar abajo)" and not sector_otro.strip():
        errores.append("Especifica tu sector")
    if not datos_form["descripcion"].strip():
        errores.append("Falta la descripcion")
    if not datos_form["ciudad"].strip():
        errores.append("Falta la ciudad")

    prefijo = obtener_prefijo(datos_form.get("pais", PAISES_DEFAULT))

    if datos_form.get("whatsapp_negocio") and datos_form["whatsapp_negocio"].strip():
        wa_norm = normalizar_whatsapp(datos_form["whatsapp_negocio"], prefijo)
        if not whatsapp_valido(wa_norm):
            errores.append("WhatsApp invalido (10-15 digitos)")

    if datos_form.get("email_contacto") and datos_form["email_contacto"].strip():
        if "@" not in datos_form["email_contacto"]:
            errores.append("Email del negocio invalido")

    if datos_form.get("anio_fundacion") and datos_form["anio_fundacion"].strip():
        try:
            anio = int(datos_form["anio_fundacion"].strip())
            if anio < 1800 or anio > 2030:
                errores.append("Ano de fundacion invalido")
        except ValueError:
            errores.append("Ano de fundacion debe ser un numero")

    return errores


def calcular_faltantes(datos_form):
    """Devuelve lista de labels de campos opcionales vacios."""
    faltantes = []
    for campo, label in CAMPOS_OPCIONALES:
        val = datos_form.get(campo, "")
        if not val or not str(val).strip():
            faltantes.append(label)
    return faltantes


if __name__ == "__main__":
    print(f"Sectores: {len(SECTORES) - 1} (+ 'Otro')")
    print(f"Campos opcionales: {len(CAMPOS_OPCIONALES)}")
    print(f"Test WhatsApp: {normalizar_whatsapp('3001234567', '+57')}")
    print(f"Test Instagram: {normalizar_instagram('@MiNegocio')}")