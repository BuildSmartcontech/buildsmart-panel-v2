# backend/herramientas.py - Herramientas para la Arquitectura C
# ============================================
# VERSIÓN 7.4 - CON DUCKDUCKGO FUNCIONAL
# ============================================

import os
import requests
import time

# ============================================
# DUCKDUCKGO - BÚSQUEDA CORREGIDA
# ============================================

def buscar(consulta: str) -> str:
    """Busca en DuckDuckGo y devuelve resultados"""
    try:
        print(f"   🔍 Buscando: {consulta}")
        
        # Usar DuckDuckGo Instant Answer API
        url = "https://api.duckduckgo.com/"
        params = {
            "q": consulta,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1,
            "t": "buildsmart"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        print(f"   📥 Código DuckDuckGo: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            resultados = []
            
            # 1. Resumen principal
            if data.get("AbstractText"):
                resultados.append(f"📝 RESUMEN:\n{data['AbstractText'][:500]}")
            
            # 2. Definición
            if data.get("Definition"):
                resultados.append(f"📖 DEFINICIÓN:\n{data['Definition'][:200]}")
            
            # 3. Temas relacionados
            temas = data.get("RelatedTopics", [])
            if temas:
                resultados.append(f"\n🔗 TEMAS RELACIONADOS:")
                for topic in temas[:5]:
                    if "Text" in topic:
                        texto = topic['Text']
                        if ' - ' in texto:
                            texto = texto.split(' - ')[0]
                        resultados.append(f"• {texto[:150]}")
            
            # 4. Enlace de referencia
            if data.get("AbstractURL"):
                resultados.append(f"\n🔗 Fuente: {data['AbstractURL']}")
            
            if resultados:
                return "\n\n".join(resultados)
            else:
                return f"No se encontraron resultados para: {consulta}"
        else:
            return f"Error en la búsqueda: {response.status_code}"
            
    except requests.exceptions.Timeout:
        return "⏳ Tiempo de espera agotado en la búsqueda"
    except requests.exceptions.ConnectionError:
        return "❌ Error de conexión en la búsqueda"
    except Exception as e:
        return f"❌ Error en la búsqueda: {str(e)}"

# ============================================
# BUSCAR CON ALTERNATIVA (DUCKDUCKGO LITE)
# ============================================

def buscar_lite(consulta: str) -> str:
    """Busca usando DuckDuckGo Lite (versión más ligera)"""
    try:
        print(f"   🔍 Buscando (Lite): {consulta}")
        
        url = "https://lite.duckduckgo.com/lite/"
        params = {"q": consulta}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Extraer resultados de la página HTML
            import re
            texto = response.text
            resultados = []
            
            # Buscar resultados con expresión regular
            patron = r'<a rel="nofollow" href="([^"]+)">([^<]+)</a>'
            matches = re.findall(patron, texto)
            
            if matches:
                resultados.append("🔗 RESULTADOS ENCONTRADOS:")
                for url_result, titulo in matches[:5]:
                    resultados.append(f"• {titulo[:100]}")
                    resultados.append(f"  {url_result[:100]}")
                return "\n".join(resultados)
            else:
                return f"No se encontraron resultados para: {consulta}"
        else:
            return f"Error en la búsqueda Lite: {response.status_code}"
            
    except Exception as e:
        return f"❌ Error en búsqueda Lite: {str(e)}"

# ============================================
# HERRAMIENTAS - CLASE PRINCIPAL
# ============================================

class Herramientas:
    def __init__(self):
        self.buscar = buscar
        self.buscar_lite = buscar_lite
    
    def buscar(self, consulta: str) -> str:
        return buscar(consulta)
    
    def buscar_lite(self, consulta: str) -> str:
        return buscar_lite(consulta)

herramientas = Herramientas()

# ============================================
# PRUEBA
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 PROBANDO HERRAMIENTAS - VERSIÓN 7.4")
    print("=" * 60)
    
    print("\n🔍 Prueba 1: Búsqueda normal")
    resultado = buscar("noticias construcción 2026")
    print(resultado)
    
    print("\n" + "=" * 60)
    print("\n🔍 Prueba 2: Búsqueda Lite")
    resultado = buscar_lite("construcción")
    print(resultado)