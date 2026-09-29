# utils/verificar_modelos.py - Verificar qué modelos están activos

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def verificar_modelo(identificador):
    """
    Verifica si un modelo está disponible en OpenRouter.
    Retorna True si está disponible, False si no.
    """
    api_key = os.getenv('OPENROUTER_API_KEY', '')
    if not api_key:
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": identificador,
            "messages": [{"role": "user", "content": "Hola"}],
            "max_tokens": 1
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        return response.status_code == 200
            
    except Exception:
        return False

def obtener_modelos_activos(modelos_dict):
    """Recibe un diccionario de modelos y retorna solo los que están activos."""
    activos = {}
    for key, modelo in modelos_dict.items():
        print(f"🔍 Verificando {modelo['nombre']}...")
        if verificar_modelo(modelo['identificador']):
            activos[key] = modelo
            print(f"   ✅ Activo")
        else:
            print(f"   ❌ No disponible")
    return activos