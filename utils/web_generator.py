# utils/web_generator.py
# ============================================
# GENERADOR DE WEBS CON IA - VERSION 4.2
# ============================================
# V4.2: Precalentamiento de imagenes Pollinations
#       (evita imagenes rotas cuando el cliente abre la web)
# V4.1: Marcadores multiples (SERVICIO, PRODUCTO, ARTICULO, ITEM)
# V4.0: Pasa campos extendidos al prompt
# V3.1: Fix sector declarado por el usuario
# ============================================

import os
import sys
import re
import time
import datetime

try:
    import requests as _requests
    REQUESTS_DISPONIBLE = True
except ImportError:
    REQUESTS_DISPONIBLE = False

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.web_prompts import generar_prompt_web, generar_prompt_resumen, generar_prompt_seo
    from utils.web_templates import renderizar_template
    from utils.web_validator import validar_completo, limpiar_html, resumen_validacion
except ImportError:
    from web_prompts import generar_prompt_web, generar_prompt_resumen, generar_prompt_seo
    from web_templates import renderizar_template
    from web_validator import validar_completo, limpiar_html, resumen_validacion

try:
    from backend.gateway import gateway
except ImportError:
    try:
        from gateway import gateway
    except ImportError:
        gateway = None
        print("ADVERTENCIA: gateway no disponible")

try:
    from utils.business_detector import analizar_negocio
    ANALISIS_DISPONIBLE = True
except ImportError:
    try:
        from business_detector import analizar_negocio
        ANALISIS_DISPONIBLE = True
    except ImportError:
        ANALISIS_DISPONIBLE = False

try:
    from utils.image_fetcher import (
        obtener_urls_imagenes_negocio,
        normalizar_sector,
        buscar_imagenes_sector,
    )
    IMAGENES_DISPONIBLES = True
except ImportError:
    try:
        from image_fetcher import (
            obtener_urls_imagenes_negocio,
            normalizar_sector,
            buscar_imagenes_sector,
        )
        IMAGENES_DISPONIBLES = True
    except ImportError:
        IMAGENES_DISPONIBLES = False
        print("ADVERTENCIA: Modulos de imagenes no disponibles")


MAX_INTENTOS = 3
TIEMPO_ESPERA = 2
SECTORES_GENERICOS = ["general", "negocio general", "default", "otros", "varios", ""]


def _es_sector_generico(sector):
    if not sector:
        return True
    return sector.lower().strip() in SECTORES_GENERICOS


def decidir_sector_para_imagenes(sector_original, sector_detectado):
    if not _es_sector_generico(sector_original):
        print("\n   Sector para imagenes: '" + str(sector_original) + "' (declarado)")
        return sector_original
    if sector_detectado and not _es_sector_generico(sector_detectado):
        print("\n   Sector para imagenes: '" + str(sector_detectado) + "' (IA)")
        return sector_detectado
    print("\n   Sector para imagenes: 'General'")
    return "General"


def _precalentar_imagenes(urls, timeout=45):
    """
    Fuerza a Pollinations.ai a generar las imagenes ANTES de guardar el HTML.

    Pollinations genera las imagenes LA PRIMERA VEZ que se pide una URL.
    Si el HTML se guarda y el cliente abre la web inmediatamente, el navegador
    pide las imagenes, Pollinations las empieza a generar, pero el navegador
    hace timeout antes de que esten listas.

    Solucion: pedir las URLs aqui para forzar la generacion.
    Cuando el cliente abra la web, las imagenes ya estan en cache CDN.
    """
    if not REQUESTS_DISPONIBLE or not urls:
        return 0

    print(f"\n   Precalentando {len(urls)} imagenes en Pollinations (puede tardar 30-90s)...")
    ok = 0
    for i, url in enumerate(urls, 1):
        try:
            r = _requests.get(url, timeout=timeout, stream=True)
            if r.status_code == 200:
                # Consumir los primeros bytes para asegurar que se genera
                _ = r.raw.read(1024)
                print(f"   [{i}/{len(urls)}] OK")
                ok += 1
            else:
                print(f"   [{i}/{len(urls)}] HTTP {r.status_code}")
            r.close()
        except Exception as e:
            print(f"   [{i}/{len(urls)}] Error: {str(e)[:60]}")

    print(f"   Precalentadas: {ok}/{len(urls)}")
    return ok


def obtener_imagenes_para_web(sector, cantidad_servicios=4, texto_negocio="", negocio_info=None,
                              precalentar=True):
    """Retorna dict con URLs de imagenes coherentes con el negocio."""
    if not IMAGENES_DISPONIBLES:
        return {"hero": None, "servicios": []}

    info = negocio_info or {}
    if not info.get("sector"):
        info["sector"] = sector
    if not info.get("descripcion"):
        info["descripcion"] = texto_negocio

    print("\n   Generando URLs con Pollinations.ai...")
    print("   Negocio: " + str(info.get("nombre", ""))[:60])
    print("   Sector: " + str(info.get("sector", "")))

    urls_data = obtener_urls_imagenes_negocio(info, cantidad=cantidad_servicios + 1)

    if not urls_data:
        print("   No se pudieron generar URLs")
        return {"hero": None, "servicios": []}

    resultado = {
        "hero": urls_data[0]["url_regular"],
        "servicios": [u["url_regular"] for u in urls_data[1:cantidad_servicios + 1]],
        "hero_prompt": urls_data[0]["descripcion"],
        "fuente": "pollinations",
    }

    print("   Hero URL: OK")
    print("   Servicios URL: " + str(len(resultado["servicios"])))

    # Precalentar imagenes para evitar que salgan rotas
    if precalentar:
        todas_urls = [resultado["hero"]] + resultado["servicios"]
        todas_urls = [u for u in todas_urls if u]
        _precalentar_imagenes(todas_urls)

    return resultado


def inyectar_imagenes_en_html(html, imagenes):
    """
    Inyecta URLs de imagenes en el HTML.
    Acepta multiples variantes de marcadores.
    """
    if not imagenes:
        return html

    hero = imagenes.get("hero")
    servicios = imagenes.get("servicios", [])

    if not hero and not servicios:
        return html

    html_modificado = html
    contador = 0

    # HERO
    if hero:
        marcadores_hero = [
            "{{HERO_IMAGE}}", "{{IMAGEN_HERO}}", "{{HERO}}",
            "{{IMAGEN_PRINCIPAL}}", "{{BANNER}}",
        ]
        reemplazado = False
        for marcador in marcadores_hero:
            if marcador in html_modificado:
                html_modificado = html_modificado.replace(marcador, hero)
                reemplazado = True
                contador += 1
                print(f"   Hero inyectado: {marcador}")
        if not reemplazado:
            html_modificado = inyectar_hero_automatico(html_modificado, hero)
            print("   Hero inyectado (automatico)")

    # SERVICIOS / PRODUCTOS
    if servicios:
        variantes = [
            "SERVICIO", "SERVICIOS", "PRODUCTO", "PRODUCTOS",
            "ARTICULO", "ARTICULOS", "ITEM", "ITEMS",
            "IMAGEN", "IMAGENES", "PROYECTO", "PROYECTOS",
            "GALERIA", "FOTO", "FOTOS", "CARD", "CARDS",
        ]

        for i, url in enumerate(servicios, 1):
            for variante in variantes:
                marcadores = [
                    "{{" + variante + "_" + str(i) + "}}",
                    "{{IMAGEN_" + variante + "_" + str(i) + "}}",
                ]
                for marcador in marcadores:
                    if marcador in html_modificado:
                        html_modificado = html_modificado.replace(marcador, url)
                        contador += 1
                        print(f"   Inyectado: {marcador} -> servicio_{i}")

        # Fallback generico: cualquier <img src="{{...}}">
        patron_generico = r'(<img[^>]*src=")\{\{[A-Z_0-9]+\}\}(")'
        matches = list(re.finditer(patron_generico, html_modificado))
        for i, match in enumerate(matches):
            if i < len(servicios):
                reemplazo = match.group(1) + servicios[i] + match.group(2)
                html_modificado = html_modificado.replace(match.group(0), reemplazo, 1)
                contador += 1
                print(f"   Fallback generico: reemplazado {match.group(0)[:50]}")

    # Placeholders de texto
    if hero:
        patrones = [
            r'<div[^>]*>\s*Imagen de la empresa\s*</div>',
            r'<div[^>]*>\s*Imagen[^<]{0,50}</div>',
        ]
        for patron in patrones:
            resultado = re.sub(
                patron,
                '<img src="' + hero + '" alt="Imagen de la empresa" style="width:100%;height:auto;border-radius:20px;" loading="lazy">',
                html_modificado,
                flags=re.IGNORECASE | re.DOTALL,
            )
            if resultado != html_modificado:
                html_modificado = resultado
                contador += 1

    # Cuadros grises
    if servicios:
        patron = r'<div[^>]*class="[^"]*proyecto-img[^"]*"[^>]*>.*?</div>'
        matches = list(re.finditer(patron, html_modificado, re.DOTALL))
        for i, match in enumerate(matches):
            if i < len(servicios):
                reemplazo = '<img src="' + servicios[i] + '" alt="Imagen ' + str(i + 1) + '" style="width:100%;height:200px;object-fit:cover;border-radius:12px;" loading="lazy">'
                html_modificado = html_modificado.replace(match.group(0), reemplazo, 1)
                contador += 1

    print("   Imagenes inyectadas: " + str(contador))
    return html_modificado


def inyectar_hero_automatico(html, hero_url):
    patron_hero = r'<section[^>]*class="[^"]*hero[^"]*"[^>]*>'
    match = re.search(patron_hero, html, re.IGNORECASE)
    if match:
        estilo = ' style="background-image: url(\'' + hero_url + '\'); background-size: cover; background-position: center; position: relative;"'
        nuevo_tag = match.group(0).replace(">", estilo + ">")
        return html.replace(match.group(0), nuevo_tag, 1)

    patron_header = r'<header[^>]*>'
    match = re.search(patron_header, html, re.IGNORECASE)
    if match:
        estilo = ' style="background-image: url(\'' + hero_url + '\'); background-size: cover; background-position: center;"'
        nuevo_tag = match.group(0).replace(">", estilo + ">")
        return html.replace(match.group(0), nuevo_tag, 1)

    return html


# ============================================
# FUNCION PRINCIPAL V4.2
# ============================================

def generar_web(datos_negocio, opciones=None, usar_template=True, con_imagenes=True):
    """Genera una pagina web completa usando IA + imagenes URLs."""
    print("=" * 60)
    print("GENERANDO WEB CON IA - V4.2")
    print("=" * 60)

    if gateway is None:
        return {
            "exito": False, "html": None, "intentos": 0,
            "validacion": None, "sector_detectado": None,
            "imagenes_usadas": None, "error": "Gateway no disponible"
        }

    sector_detectado = None
    recomendaciones = None

    if ANALISIS_DISPONIBLE:
        print("\n1. Analizando negocio...")
        texto_analisis = (
            datos_negocio.get("descripcion", "") + " " +
            datos_negocio.get("sector", "") + " " +
            datos_negocio.get("nombre", "")
        )
        analisis = analizar_negocio(texto_analisis)
        sector_detectado = analisis.get("sector")
        confianza = analisis.get("confianza", 0)
        print("   Sector detectado: " + str(sector_detectado))
        print("   Confianza: " + str(confianza))
        if confianza >= 0.5:
            recomendaciones = analisis
            print("   Usando recomendaciones del sector")

    nombre = datos_negocio.get("nombre", "Mi Negocio")
    sector_original = datos_negocio.get("sector", "")
    descripcion = datos_negocio.get("descripcion", "Descripcion del negocio")
    publico = datos_negocio.get("publico_objetivo", "")
    diferenciadores = datos_negocio.get("diferenciadores", "")
    colores = datos_negocio.get("colores", "#0f3460, #f39c12")

    direccion = datos_negocio.get("direccion", "")
    ciudad = datos_negocio.get("ciudad", "")
    pais = datos_negocio.get("pais", "")
    horarios = datos_negocio.get("horarios", "")
    instagram = datos_negocio.get("instagram", "")
    facebook = datos_negocio.get("facebook", "")
    tiktok = datos_negocio.get("tiktok", "")
    anio_fundacion = datos_negocio.get("anio_fundacion", "")
    email_contacto = datos_negocio.get("email_contacto", "")
    whatsapp_negocio = datos_negocio.get("whatsapp_negocio", "")

    print(f"   Campos extendidos: dir={bool(direccion)} ciu={bool(ciudad)} "
          f"hor={bool(horarios)} ig={bool(instagram)} fb={bool(facebook)} "
          f"tk={bool(tiktok)} anio={bool(anio_fundacion)} "
          f"mail={bool(email_contacto)} wa={bool(whatsapp_negocio)}")

    sector_para_imagenes = decidir_sector_para_imagenes(sector_original, sector_detectado)
    texto_negocio = (nombre + " " + descripcion + " " + diferenciadores).strip()

    if opciones is None:
        if recomendaciones:
            opciones = {
                "tipo_pagina": recomendaciones.get("tipo_pagina", "Landing Page"),
                "diseno": recomendaciones.get("diseno", "Moderno"),
                "tono": recomendaciones.get("tono", "Profesional"),
                "secciones": recomendaciones.get("secciones"),
                "logica": "Formulario de contacto",
                "funcionalidades": ["SEO optimizado", "Animaciones"],
            }
        else:
            opciones = {
                "tipo_pagina": "Landing Page",
                "diseno": "Moderno",
                "tono": "Profesional",
                "secciones": ["Hero", "Servicios", "Sobre Nosotros", "Contacto"],
                "logica": "Formulario de contacto",
                "funcionalidades": ["SEO optimizado", "Animaciones"],
            }

    print("\n2. Datos del negocio:")
    print("   Nombre: " + nombre)
    print("   Sector: " + str(sector_original))

    imagenes = None
    if con_imagenes and IMAGENES_DISPONIBLES:
        print("\n3. Generando imagenes...")
        negocio_info = {
            "nombre": nombre,
            "sector": sector_para_imagenes,
            "descripcion": descripcion,
        }
        imagenes = obtener_imagenes_para_web(
            sector_para_imagenes,
            texto_negocio=texto_negocio,
            negocio_info=negocio_info,
            precalentar=True,
        )

    for intento in range(1, MAX_INTENTOS + 1):
        print("\n" + "-" * 60)
        print("INTENTO " + str(intento) + "/" + str(MAX_INTENTOS))
        print("-" * 60)

        try:
            print("Construyendo prompt...")
            prompt = generar_prompt_web(
                nombre_negocio=nombre,
                sector=sector_original or sector_detectado or "general",
                descripcion=descripcion,
                publico_objetivo=publico,
                diferenciadores=diferenciadores,
                tono=opciones.get("tono", "Profesional"),
                colores=colores,
                tipo_pagina=opciones.get("tipo_pagina", "Landing Page"),
                diseno=opciones.get("diseno", "Moderno"),
                secciones=opciones.get("secciones"),
                logica=opciones.get("logica", "Estatica"),
                funcionalidades=opciones.get("funcionalidades"),
                direccion=direccion,
                ciudad=ciudad,
                pais=pais,
                horarios=horarios,
                instagram=instagram,
                facebook=facebook,
                tiktok=tiktok,
                anio_fundacion=anio_fundacion,
                email_contacto=email_contacto,
                whatsapp_negocio=whatsapp_negocio,
            )

            print("Prompt: " + str(len(prompt)) + " caracteres")
            print("Llamando a la IA...")
            sistema = "Eres un disenador web profesional. Genera codigo HTML/CSS limpio y moderno."

            respuesta, fuente = gateway.chat_inteligente(prompt, sistema)

            print("Respuesta de: " + fuente)
            print("Longitud: " + str(len(respuesta)) + " caracteres")

            print("Limpiando HTML...")
            html = limpiar_html(respuesta)

            if imagenes and (imagenes.get("hero") or imagenes.get("servicios")):
                print("Inyectando imagenes...")
                html = inyectar_imagenes_en_html(html, imagenes)
                print("HTML con imagenes: " + str(len(html)) + " caracteres")

            print("Validando HTML...")
            validacion = validar_completo(html)

            print("Valido: " + str(validacion["valido"]))
            if validacion["errores"]:
                for err in validacion["errores"][:3]:
                    print("   - " + err)

            if validacion["valido"]:
                print("\n" + "=" * 60)
                print("WEB GENERADA EXITOSAMENTE - V4.2")
                print("=" * 60)

                return {
                    "exito": True,
                    "html": html,
                    "intentos": intento,
                    "validacion": validacion,
                    "fuente": fuente,
                    "sector_detectado": sector_detectado,
                    "sector_usado_imagenes": sector_para_imagenes,
                    "imagenes_usadas": imagenes,
                    "error": None,
                }

            print("\nHTML invalido. Reintentando en " + str(TIEMPO_ESPERA) + "s...")
            time.sleep(TIEMPO_ESPERA)

        except Exception as e:
            print("Error en intento " + str(intento) + ": " + str(e))
            time.sleep(TIEMPO_ESPERA)

    return {
        "exito": False, "html": None, "intentos": MAX_INTENTOS,
        "validacion": None, "fuente": None,
        "sector_detectado": sector_detectado,
        "imagenes_usadas": imagenes,
        "error": "No se pudo generar HTML valido",
    }


def generar_resumen(html):
    if gateway is None:
        return "Gateway no disponible"
    try:
        prompt = generar_prompt_resumen(html)
        sistema = "Eres un experto en marketing digital."
        respuesta, fuente = gateway.chat_rapido(prompt, sistema)
        return limpiar_html(respuesta)
    except Exception as e:
        return "Error: " + str(e)


def generar_seo(nombre_negocio, sector, descripcion):
    if gateway is None:
        return {}
    try:
        prompt = generar_prompt_seo(nombre_negocio, sector, descripcion)
        sistema = "Eres un experto en SEO."
        respuesta, fuente = gateway.chat_rapido(prompt, sistema)
        import json
        try:
            return json.loads(respuesta)
        except Exception:
            return {}
    except Exception as e:
        return {}


if __name__ == "__main__":
    print("=" * 60)
    print("TEST WEB GENERATOR V4.2")
    print("=" * 60)
    print("Cambios V4.2:")
    print("  - Precalentamiento de imagenes Pollinations")
    print("    (evita imagenes rotas en el cliente)")
    print("=" * 60)