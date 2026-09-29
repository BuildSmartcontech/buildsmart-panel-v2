# utils/supabase_client.py
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class SupabaseClient:
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_KEY')
        self.headers = {
            'apikey': self.key,
            'Authorization': f'Bearer {self.key}',
            'Content-Type': 'application/json'
        }
        self.disponible = bool(self.url and self.key)
    
    def guardar_historial(self, mensaje, respuesta, modelo=None, negocio_id=None, fuente=None, usuario='anonimo'):
        if not self.disponible:
            return False
        
        data = {
            'usuario': usuario,
            'mensaje': mensaje,
            'respuesta': respuesta,
            'modelo_usado': modelo,
            'negocio_id': negocio_id,
            'fuente': fuente
        }
        
        try:
            r = requests.post(f'{self.url}/rest/v1/historial_chat', headers=self.headers, json=data, timeout=10)
            return r.status_code == 201
        except:
            return False
    
    def obtener_historial(self, usuario='anonimo', limite=10):
        if not self.disponible:
            return []
        
        params = {'usuario': f'eq.{usuario}', 'order': 'created_at.desc', 'limit': limite}
        try:
            r = requests.get(f'{self.url}/rest/v1/historial_chat', headers=self.headers, params=params, timeout=10)
            return r.json() if r.status_code == 200 else []
        except:
            return []

supabase = SupabaseClient()

if __name__ == "__main__":
    print("🧪 Probando Supabase")
    ok = supabase.guardar_historial("Prueba", "Respuesta OK", "openrouter", "buildsmart")
    print(f"✅ Guardado: {ok}")
    historial = supabase.obtener_historial(limite=3)
    print(f"📊 Historial: {len(historial)} registros")