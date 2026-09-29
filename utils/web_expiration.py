# utils/web_expiration.py
# ============================================
# SISTEMA DE EXPIRACION (CANDADO DE 30 DIAS)
# ============================================
# VERSION FINAL CORREGIDA
# ============================================

import os
import sys
import datetime
import requests

# Agregar la raiz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar config
try:
    from config.web_config import CONFIG, MENSAJES, ESTADOS_WEB
except ImportError:
    CONFIG = {
        "dias_gratis": 30,
        "dias_gracia": 30,
        "alertas_dias": [15, 25, 29],
    }
    MENSAJES = {
        "alerta_15": "Tu web expira en 15 dias",
        "alerta_25": "Tu web expira en 5 dias",
        "alerta_29": "Ultimo dia",
    }
    ESTADOS_WEB = {
        "activa": "Web activa",
        "por_expirar": "Web proxima a expirar",
        "expirada": "Web expirada",
        "borrada": "Web eliminada",
    }

# Importar Supabase
try:
    from utils.supabase_client import supabase
except ImportError:
    try:
        from supabase_client import supabase
    except ImportError:
        supabase = None
        print("ADVERTENCIA: Supabase no disponible")


# ============================================
# CONSTANTES
# ============================================

DIAS_GRATIS = CONFIG.get("dias_gratis", 30)
DIAS_GRACIA = CONFIG.get("dias_gracia", 30)
ALERTAS_DIAS = CONFIG.get("alertas_dias", [15, 25, 29])


# ============================================
# FUNCION: CALCULAR DIAS RESTANTES
# ============================================

def calcular_dias_restantes(fecha_expiracion):
    """
    Calcula los dias que faltan para expirar.
    Redondea HACIA ARRIBA para que el dia 0 de simulacion sea 30.
    """
    
    if not fecha_expiracion:
        return None
    
    try:
        # Convertir a datetime si es string
        if isinstance(fecha_expiracion, str):
            fecha_expiracion = datetime.datetime.fromisoformat(
                fecha_expiracion.replace("Z", "+00:00")
            )
        
        # Asegurar timezone
        if fecha_expiracion.tzinfo is None:
            fecha_expiracion = fecha_expiracion.replace(tzinfo=datetime.timezone.utc)
        
        # Hora actual
        ahora = datetime.datetime.now(datetime.timezone.utc)
        
        # Diferencia en segundos
        diferencia_segundos = (fecha_expiracion - ahora).total_seconds()
        
        # Convertir a dias (redondeando hacia arriba con math.ceil)
        # Asi el dia 0 de simulacion = 30 dias
        import math
        dias = math.ceil(diferencia_segundos / 86400)
        
        return dias
    except Exception as e:
        print("Error calculando dias: " + str(e))
        return None


# ============================================
# FUNCION: DETERMINAR ESTADO
# ============================================

def determinar_estado(dias_restantes):
    """Determina el estado segun los dias restantes."""
    
    if dias_restantes is None:
        return "activa"
    
    if dias_restantes > 0:
        # Activa o por expirar
        if dias_restantes <= max(ALERTAS_DIAS):
            return "por_expirar"
        else:
            return "activa"
    else:
        # Expirada o borrada
        dias_desde_expiracion = abs(dias_restantes)
        
        # CAMBIO: usar >= para que el dia 60 sea "borrada"
        if dias_desde_expiracion >= DIAS_GRACIA:
            return "borrada"
        else:
            return "expirada"


# ============================================
# FUNCION: GENERAR ALERTA
# ============================================

def generar_alerta(dias_restantes):
    """Genera el mensaje de alerta segun los dias restantes."""
    
    if dias_restantes is None:
        return None
    
    # Solo alertar si esta en periodo activo (dias >= 0)
    if dias_restantes < 0:
        return None
    
    if dias_restantes <= 1:
        return MENSAJES.get("alerta_29", "Tu web expira hoy")
    elif dias_restantes <= 5:
        return MENSAJES.get("alerta_25", "Tu web expira en 5 dias")
    elif dias_restantes <= 15:
        return MENSAJES.get("alerta_15", "Tu web expira en 15 dias")
    else:
        return None


# ============================================
# FUNCION: OBTENER INFO DE WEB
# ============================================

def obtener_info_web(web_id):
    """Obtiene informacion de expiracion de una web."""
    
    if supabase is None:
        return {
            "exito": False,
            "error": "Supabase no disponible"
        }
    
    try:
        url = supabase.url + "/rest/v1/paginas_web"
        params = {
            "id": "eq." + web_id,
            "select": "*"
        }
        headers = supabase.headers.copy()
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if not data:
                return {
                    "exito": False,
                    "error": "Web no encontrada"
                }
            
            web = data[0]
            fecha_expiracion = web.get("fecha_expiracion")
            dias_restantes = calcular_dias_restantes(fecha_expiracion)
            estado = determinar_estado(dias_restantes)
            alerta = generar_alerta(dias_restantes)
            
            return {
                "exito": True,
                "web_id": web_id,
                "estado": estado,
                "dias_restantes": dias_restantes,
                "fecha_expiracion": fecha_expiracion,
                "alerta": alerta,
                "premium": web.get("premium", False),
                "error": None
            }
        else:
            return {
                "exito": False,
                "error": "Status " + str(response.status_code)
            }
    except Exception as e:
        return {
            "exito": False,
            "error": str(e)
        }


# ============================================
# FUNCION: ACTUALIZAR ESTADO EN SUPABASE
# ============================================

def actualizar_estado_web(web_id, nuevo_estado, alerta_enviada=None):
    """Actualiza el estado de una web en Supabase."""
    
    if supabase is None:
        return {
            "exito": False,
            "error": "Supabase no disponible"
        }
    
    try:
        url = supabase.url + "/rest/v1/paginas_web"
        params = {"id": "eq." + web_id}
        headers = supabase.headers.copy()
        headers["Prefer"] = "return=representation"
        
        data = {"estado": nuevo_estado}
        
        if alerta_enviada:
            data[alerta_enviada] = True
        
        response = requests.patch(url, headers=headers, params=params, json=data, timeout=10)
        
        if response.status_code in [200, 204]:
            return {
                "exito": True,
                "error": None
            }
        else:
            return {
                "exito": False,
                "error": "Status " + str(response.status_code)
            }
    except Exception as e:
        return {
            "exito": False,
            "error": str(e)
        }


# ============================================
# FUNCION: VERIFICAR TODAS LAS WEBS
# ============================================

def verificar_todas_las_webs():
    """Verifica todas las webs y actualiza sus estados."""
    
    print("=" * 60)
    print("VERIFICANDO TODAS LAS WEBS")
    print("=" * 60)
    
    if supabase is None:
        return {
            "exito": False,
            "error": "Supabase no disponible",
            "procesadas": 0
        }
    
    try:
        url = supabase.url + "/rest/v1/paginas_web"
        params = {"select": "*"}
        headers = supabase.headers.copy()
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code != 200:
            return {
                "exito": False,
                "error": "Status " + str(response.status_code),
                "procesadas": 0
            }
        
        webs = response.json()
        
        print("Total de webs: " + str(len(webs)))
        
        procesadas = 0
        expiradas = 0
        borradas = 0
        
        for web in webs:
            try:
                web_id = web.get("id")
                fecha_expiracion = web.get("fecha_expiracion")
                premium = web.get("premium", False)
                
                if premium:
                    continue
                
                dias = calcular_dias_restantes(fecha_expiracion)
                estado_actual = web.get("estado", "activa")
                nuevo_estado = determinar_estado(dias)
                
                if nuevo_estado != estado_actual:
                    print("   Web " + web_id[:8] + ": " + estado_actual + " -> " + nuevo_estado)
                    
                    alerta = None
                    if dias is not None and dias >= 0:
                        if not web.get("alerta_15_enviada") and dias <= 15:
                            alerta = "alerta_15_enviada"
                        elif not web.get("alerta_25_enviada") and dias <= 5:
                            alerta = "alerta_25_enviada"
                        elif not web.get("alerta_29_enviada") and dias <= 1:
                            alerta = "alerta_29_enviada"
                    
                    resultado = actualizar_estado_web(web_id, nuevo_estado, alerta)
                    
                    if resultado["exito"]:
                        procesadas += 1
                        if nuevo_estado == "expirada":
                            expiradas += 1
                        elif nuevo_estado == "borrada":
                            borradas += 1
            except Exception as e:
                print("   Error procesando web: " + str(e))
                continue
        
        print("\nResumen:")
        print("   Procesadas: " + str(procesadas))
        print("   Expiradas: " + str(expiradas))
        print("   Borradas: " + str(borradas))
        
        return {
            "exito": True,
            "procesadas": procesadas,
            "expiradas": expiradas,
            "borradas": borradas,
            "error": None
        }
    except Exception as e:
        return {
            "exito": False,
            "error": str(e),
            "procesadas": 0
        }


# ============================================
# FUNCION: SIMULAR DIAS
# ============================================

def simular_dias(web_id, dias_desde_hoy):
    """
    Simula el paso de X dias en una web.
    
    La fecha de expiracion se calcula como:
    hoy + DIAS_GRATIS - dias_desde_hoy
    
    Ejemplos:
    - simular_dias(web, 0)  -> quedan 30 dias
    - simular_dias(web, 15) -> quedan 15 dias
    - simular_dias(web, 30) -> quedan 0 dias (expira hoy)
    - simular_dias(web, 60) -> expiro hace 30 dias (borrada)
    """
    
    if supabase is None:
        return {
            "exito": False,
            "error": "Supabase no disponible"
        }
    
    try:
        # Calcular nueva fecha: hoy + (30 - dias_desde_hoy)
        nueva_fecha = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            days=(DIAS_GRATIS - dias_desde_hoy)
        )
        
        url = supabase.url + "/rest/v1/paginas_web"
        params = {"id": "eq." + web_id}
        headers = supabase.headers.copy()
        headers["Prefer"] = "return=representation"
        
        data = {"fecha_expiracion": nueva_fecha.isoformat()}
        
        response = requests.patch(url, headers=headers, params=params, json=data, timeout=10)
        
        if response.status_code in [200, 204]:
            print("Simulados " + str(dias_desde_hoy) + " dias en web " + web_id[:8])
            return {
                "exito": True,
                "error": None
            }
        else:
            return {
                "exito": False,
                "error": "Status " + str(response.status_code)
            }
    except Exception as e:
        return {
            "exito": False,
            "error": str(e)
        }


# ============================================
# PRUEBA
# ============================================

def test_expiration():
    """Prueba el sistema de expiracion."""
    
    print("=" * 60)
    print("PROBANDO SISTEMA DE EXPIRACION")
    print("=" * 60)
    
    try:
        from utils.web_storage import guardar_usuario, guardar_web, generar_uuid
    except ImportError:
        from web_storage import guardar_usuario, guardar_web, generar_uuid
    
    # 1. Crear usuario y web
    print("\n1. Creando usuario y web de prueba...")
    
    usuario_test = guardar_usuario(
        email="test_exp_" + generar_uuid()[:8] + "@test.com",
        nombre="Test Expiracion"
    )
    
    if usuario_test is None:
        print("No se pudo crear usuario")
        return
    
    web_test = generar_uuid()
    html_test = "<!DOCTYPE html><html><head><title>Test</title></head><body><h1>Test</h1></body></html>"
    
    resultado = guardar_web(
        usuario_id=usuario_test,
        web_id=web_test,
        html=html_test,
        datos_extra={"tipo_pagina": "Landing Page"}
    )
    
    print("Web creada: " + web_test[:8])
    
    # 2. Probar cada dia
    dias_a_probar = [0, 15, 25, 29, 30, 45, 60]
    
    for dia in dias_a_probar:
        print("\n" + "-" * 60)
        print("SIMULANDO DIA " + str(dia))
        print("-" * 60)
        
        simular_dias(web_test, dia)
        
        info = obtener_info_web(web_test)
        
        if info["exito"]:
            print("   Estado: " + info["estado"])
            print("   Dias restantes: " + str(info["dias_restantes"]))
            print("   Alerta: " + str(info["alerta"]))
        else:
            print("   Error: " + info["error"])
    
    # 3. Verificar todas las webs
    print("\n" + "=" * 60)
    print("VERIFICANDO TODAS LAS WEBS")
    print("=" * 60)
    
    resultado = verificar_todas_las_webs()
    
    print("\n" + "=" * 60)
    print("PRUEBA COMPLETADA")
    print("=" * 60)


# ============================================
# EJECUTAR PRUEBA
# ============================================

if __name__ == "__main__":
    test_expiration()