# utils/web_editor.py
# ============================================
# EDITOR DE WEBS CON IA
# ============================================
# Este archivo edita webs existentes usando la IA.
# El usuario da una instruccion y la IA regenera el HTML.
# ============================================

import os
import sys
import time
import datetime

# Agregar la raiz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar modulos
try:
    from utils.web_prompts import generar_prompt_edicion
    from utils.web_validator import validar_completo, limpiar_html, resumen_validacion
    from utils.web_storage import leer_web, guardar_web
except ImportError:
    from web_prompts import generar_prompt_edicion
    from web_validator import validar_completo, limpiar_html, resumen_validacion
    from web_storage import leer_web, guardar_web

# Importar gateway
try:
    from backend.gateway import gateway
except ImportError:
    try:
        from gateway import gateway
    except ImportError:
        gateway = None
        print("ADVERTENCIA: gateway no disponible")


# ============================================
# CONSTANTES
# ============================================

MAX_INTENTOS = 3
TIEMPO_ESPERA = 2


# ============================================
# FUNCION PRINCIPAL: EDITAR WEB
# ============================================

def editar_web(usuario_id, web_id, instruccion):
    """
    Edita una web existente usando IA.
    
    Args:
        usuario_id: ID del usuario
        web_id: ID de la web
        instruccion: texto del usuario describiendo el cambio
    
    Returns:
        dict con:
        {
            "exito": True/False,
            "html_anterior": "...",
            "html_nuevo": "...",
            "intentos": 1,
            "validacion": {...},
            "error": "..."
        }
    """
    
    print("=" * 60)
    print("EDITANDO WEB CON IA")
    print("=" * 60)
    print("Usuario: " + str(usuario_id)[:8])
    print("Web: " + str(web_id)[:8])
    print("Instruccion: " + instruccion[:100])
    
    # Verificar gateway
    if gateway is None:
        return {
            "exito": False,
            "html_anterior": None,
            "html_nuevo": None,
            "intentos": 0,
            "validacion": None,
            "error": "Gateway no disponible"
        }
    
    # 1. Leer HTML actual
    print("\n1. Leyendo HTML actual...")
    resultado_lectura = leer_web(usuario_id, web_id)
    
    if not resultado_lectura["exito"]:
        return {
            "exito": False,
            "html_anterior": None,
            "html_nuevo": None,
            "intentos": 0,
            "validacion": None,
            "error": "No se pudo leer la web: " + str(resultado_lectura["error"])
        }
    
    html_anterior = resultado_lectura["html"]
    print("HTML leido: " + str(len(html_anterior)) + " caracteres")
    
    # 2. Intentos de edicion
    for intento in range(1, MAX_INTENTOS + 1):
        print("\n" + "-" * 60)
        print("INTENTO " + str(intento) + "/" + str(MAX_INTENTOS))
        print("-" * 60)
        
        try:
            # Construir prompt de edicion
            print("Construyendo prompt de edicion...")
            prompt = generar_prompt_edicion(html_anterior, instruccion)
            print("Prompt: " + str(len(prompt)) + " caracteres")
            
            # Llamar a la IA
            print("Llamando a la IA...")
            sistema = "Eres un disenador web profesional. Edita el HTML segun la instruccion del usuario."
            
            respuesta, fuente = gateway.chat_inteligente(prompt, sistema)
            
            print("Respuesta de: " + fuente)
            print("Longitud: " + str(len(respuesta)) + " caracteres")
            
            # Limpiar HTML
            print("Limpiando HTML...")
            html_nuevo = limpiar_html(respuesta)
            
            # Validar
            print("Validando HTML...")
            validacion = validar_completo(html_nuevo)
            
            print("Valido: " + str(validacion["valido"]))
            if validacion["errores"]:
                print("Errores: " + str(len(validacion["errores"])))
                for err in validacion["errores"][:3]:
                    print("   - " + err)
            
            # Si es valido, retornar
            if validacion["valido"]:
                print("\n" + "=" * 60)
                print("WEB EDITADA EXITOSAMENTE")
                print("=" * 60)
                
                return {
                    "exito": True,
                    "html_anterior": html_anterior,
                    "html_nuevo": html_nuevo,
                    "intentos": intento,
                    "validacion": validacion,
                    "fuente": fuente,
                    "error": None
                }
            
            # Si no es valido, esperar y reintentar
            print("\nHTML invalido. Reintentando en " + str(TIEMPO_ESPERA) + "s...")
            time.sleep(TIEMPO_ESPERA)
            
        except Exception as e:
            print("Error en intento " + str(intento) + ": " + str(e))
            time.sleep(TIEMPO_ESPERA)
    
    # Si llegamos aqui, fallaron todos los intentos
    print("\n" + "=" * 60)
    print("FALLO DESPUES DE " + str(MAX_INTENTOS) + " INTENTOS")
    print("=" * 60)
    
    return {
        "exito": False,
        "html_anterior": html_anterior,
        "html_nuevo": None,
        "intentos": MAX_INTENTOS,
        "validacion": None,
        "fuente": None,
        "error": "No se pudo editar despues de " + str(MAX_INTENTOS) + " intentos"
    }


# ============================================
# FUNCION: EDITAR Y GUARDAR
# ============================================

def editar_y_guardar(usuario_id, web_id, instruccion):
    """
    Edita una web y guarda el resultado automaticamente.
    """
    
    print("=" * 60)
    print("EDITANDO Y GUARDANDO WEB")
    print("=" * 60)
    
    # 1. Editar
    resultado = editar_web(usuario_id, web_id, instruccion)
    
    if not resultado["exito"]:
        return {
            "exito": False,
            "html_nuevo": None,
            "guardado": False,
            "error": resultado["error"]
        }
    
    # 2. Guardar el HTML nuevo
    print("\n2. Guardando HTML editado...")
    
    html_nuevo = resultado["html_nuevo"]
    
    # Guardar en archivos (sobrescribir)
    try:
        from utils.web_storage import guardar_en_archivos
    except ImportError:
        from web_storage import guardar_en_archivos
    
    resultado_guardado = guardar_en_archivos(usuario_id, web_id, html_nuevo)
    
    if resultado_guardado["exito"]:
        print("HTML guardado: " + resultado_guardado["ruta"])
    
    return {
        "exito": True,
        "html_nuevo": html_nuevo,
        "guardado": resultado_guardado["exito"],
        "ruta": resultado_guardado.get("ruta"),
        "error": None
    }


# ============================================
# FUNCION: LISTAR CAMBIOS COMUNES
# ============================================

def obtener_sugerencias_cambios():
    """Devuelve una lista de cambios comunes sugeridos."""
    
    return [
        "Cambia el color principal a azul",
        "Cambia el color principal a verde",
        "Agrega una seccion de precios",
        "Agrega una seccion de FAQ",
        "Quita la seccion de testimonios",
        "Cambia el titulo del hero",
        "Agrega un formulario de contacto",
        "Agrega un boton de WhatsApp",
        "Cambia la tipografia a una mas moderna",
        "Agrega una galeria de imagenes",
        "Simplifica el diseno",
        "Hazlo mas colorido",
        "Cambia el tono a mas profesional",
        "Agrega una seccion de equipo",
        "Agrega redes sociales en el footer",
    ]


# ============================================
# PRUEBA (con HTML COMPLETO)
# ============================================

def test_editor():
    """Prueba el editor de webs."""
    
    print("=" * 60)
    print("PROBANDO EDITOR DE WEBS")
    print("=" * 60)
    
    try:
        from utils.web_storage import guardar_usuario, guardar_web, generar_uuid
    except ImportError:
        from web_storage import guardar_usuario, guardar_web, generar_uuid
    
    # 1. Crear usuario y web
    print("\n1. Creando usuario y web de prueba...")
    
    usuario_test = guardar_usuario(
        email="test_edit_" + generar_uuid()[:8] + "@test.com",
        nombre="Test Editor"
    )
    
    if usuario_test is None:
        print("No se pudo crear usuario")
        return
    
    web_test = generar_uuid()
    
    # HTML COMPLETO de prueba (con DOCTYPE, html, head, body, style)
    html_test = (
        "<!DOCTYPE html>\n"
        "<html lang=\"es\">\n"
        "<head>\n"
        "    <meta charset=\"UTF-8\">\n"
        "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        "    <meta name=\"description\" content=\"Web de prueba para SAMU IA\">\n"
        "    <title>Mi Negocio</title>\n"
        "    <style>\n"
        "        body { font-family: sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }\n"
        "        h1 { color: #0f3460; }\n"
        "        p { color: #333; }\n"
        "    </style>\n"
        "</head>\n"
        "<body>\n"
        "    <header><h1>Hola Mundo</h1></header>\n"
        "    <main><p>Esta es una web de prueba para SAMU IA.</p></main>\n"
        "    <footer><p>Contacto: test@test.com</p></footer>\n"
        "</body>\n"
        "</html>"
    )
    
    resultado = guardar_web(
        usuario_id=usuario_test,
        web_id=web_test,
        html=html_test,
        datos_extra={"tipo_pagina": "Landing Page"}
    )
    
    print("Web creada: " + web_test[:8])
    print("HTML: " + str(len(html_test)) + " caracteres")
    
    # 2. Ver sugerencias
    print("\n2. Sugerencias de cambios disponibles:")
    sugerencias = obtener_sugerencias_cambios()
    for i, sug in enumerate(sugerencias[:5], 1):
        print("   " + str(i) + ". " + sug)
    
    # 3. Editar web
    print("\n3. Editando web con instruccion de prueba...")
    instruccion = "Cambia el titulo principal a 'Bienvenido a SAMU IA'"
    
    resultado = editar_web(usuario_test, web_test, instruccion)
    
    if resultado["exito"]:
        print("\nEdicion EXITOSA")
        print("   Intentos: " + str(resultado["intentos"]))
        print("   HTML anterior: " + str(len(resultado["html_anterior"])) + " caracteres")
        print("   HTML nuevo: " + str(len(resultado["html_nuevo"])) + " caracteres")
        print("   Fuente: " + str(resultado["fuente"]))
    else:
        print("\nEdicion FALLIDA")
        print("   Error: " + str(resultado["error"]))
    
    print("\n" + "=" * 60)
    print("PRUEBA COMPLETADA")
    print("=" * 60)


# ============================================
# EJECUTAR PRUEBA
# ============================================

if __name__ == "__main__":
    test_editor()