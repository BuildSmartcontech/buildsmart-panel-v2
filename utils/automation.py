# utils/automation.py - Automatización 24/7

import threading
import time
import datetime
import random

class AutomationScheduler:
    def __init__(self):
        self.tareas_programadas = []
        self.activo = False
    
    def agregar_tarea(self, nombre, funcion, intervalo_minutos):
        """Agregar una tarea programada"""
        self.tareas_programadas.append({
            'nombre': nombre,
            'funcion': funcion,
            'intervalo': intervalo_minutos * 60,
            'ultima_ejecucion': None
        })
    
    def iniciar(self):
        """Iniciar el scheduler en segundo plano"""
        self.activo = True
        thread = threading.Thread(target=self._ejecutar_bucle)
        thread.daemon = True
        thread.start()
        return "✅ Scheduler iniciado"
    
    def _ejecutar_bucle(self):
        """Bucle principal del scheduler"""
        while self.activo:
            ahora = time.time()
            for tarea in self.tareas_programadas:
                if not tarea['ultima_ejecucion'] or (ahora - tarea['ultima_ejecucion']) > tarea['intervalo']:
                    try:
                        tarea['funcion']()
                        tarea['ultima_ejecucion'] = ahora
                        print(f"✅ Ejecutada tarea: {tarea['nombre']}")
                    except Exception as e:
                        print(f"❌ Error en {tarea['nombre']}: {e}")
            time.sleep(60)  # Verificar cada minuto
    
    def detener(self):
        """Detener el scheduler"""
        self.activo = False
        return "⏹️ Scheduler detenido"

scheduler = AutomationScheduler()

# ========== TAREAS AUTOMÁTICAS ==========
def tarea_nocturna():
    """Ejecutar tareas nocturnas"""
    print(f"🌙 Turno nocturno ejecutado: {datetime.datetime.now()}")
    # Aquí se pueden agregar tareas como:
    # - Investigar noticias
    # - Generar contenido
    # - Resumir datos

def tarea_diaria():
    """Ejecutar tareas diarias"""
    print(f"📅 Tarea diaria ejecutada: {datetime.datetime.now()}")

def tarea_semanal():
    """Ejecutar tareas semanales"""
    print(f"📊 Tarea semanal ejecutada: {datetime.datetime.now()}")