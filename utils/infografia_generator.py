# utils/infografia_generator.py - Generador de infografías con Gemini Imagen
import os
from backend.gateway import gateway

def generar_infografia_plan(plan: str) -> str:
    """
    Genera una infografía del plan usando Gemini Imagen
    
    Args:
        plan: Texto del plan
    
    Returns:
        str: Ruta de la imagen generada
    """
    # Extraer puntos clave del plan
    prompt = f"""
    Crea una infografía profesional para un plan de marketing de construcción.
    Incluye:
    1. Título llamativo
    2. 3-5 objetivos principales
    3. 3-4 estrategias clave
    4. KPIs de éxito
    
    Información del plan:
    {plan[:1000]}
    
    Genera una imagen estilo infografía profesional.
    """
    
    try:
        from backend.gateway import gateway as gw
        resultado = gw.generar_imagen(prompt)
        return resultado
    except Exception as e:
        return f"Error generando infografía: {str(e)}"

if __name__ == "__main__":
    # Prueba
    test_plan = "Plan de marketing para construcción. Objetivos: incrementar ventas, mejorar presencia digital."
    print("🧪 Probando infografía...")
    resultado = generar_infografia_plan(test_plan)
    print(f"📊 Resultado: {resultado}")