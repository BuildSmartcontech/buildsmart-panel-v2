# utils/database.py - Conexión y operaciones con PostgreSQL

import os
import psycopg2
import pandas as pd
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.conn_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'postgres'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'mi_password')
        }
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establecer conexión a la base de datos"""
        try:
            self.connection = psycopg2.connect(**self.conn_params)
            self.cursor = self.connection.cursor()
            return True
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False
    
    def disconnect(self):
        """Cerrar conexión"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """Ejecutar una consulta SQL"""
        try:
            self.cursor.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return True
        except Exception as e:
            print(f"Error en consulta: {e}")
            return None
    
    def get_dataframe(self, query, params=None):
        """Ejecutar consulta y devolver DataFrame"""
        return pd.read_sql(query, self.connection, params=params)
    
    # ========== MÉTODOS ESPECÍFICOS ==========
    
    def get_negocios(self):
        """Obtener todos los negocios"""
        query = """
            SELECT id, nombre, icono, descripcion, color, 
                   metricas, configuracion, creado_en
            FROM negocios
            WHERE activo = true
            ORDER BY creado_en DESC
        """
        return self.get_dataframe(query)
    
    def get_tareas(self, negocio_id=None):
        """Obtener tareas de un negocio"""
        query = """
            SELECT t.*, n.nombre as negocio_nombre
            FROM tareas t
            JOIN negocios n ON t.negocio_id = n.id
            WHERE t.estado = 'PENDIENTE'
        """
        if negocio_id:
            query += f" AND t.negocio_id = {negocio_id}"
        query += " ORDER BY t.prioridad DESC, t.creado_en ASC"
        return self.get_dataframe(query)
    
    def get_agentes(self, negocio_id=None):
        """Obtener agentes de un negocio"""
        query = """
            SELECT a.*, n.nombre as negocio_nombre
            FROM agentes a
            JOIN negocios n ON a.negocio_id = n.id
            WHERE a.activo = true
        """
        if negocio_id:
            query += f" AND a.negocio_id = {negocio_id}"
        return self.get_dataframe(query)
    
    def crear_tarea(self, titulo, descripcion, categoria, negocio_id, prioridad='MEDIA'):
        """Crear una nueva tarea"""
        query = """
            INSERT INTO tareas (titulo, descripcion, categoria, negocio_id, prioridad)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        result = self.execute_query(query, (titulo, descripcion, categoria, negocio_id, prioridad))
        return result[0][0] if result else None

# Instancia global para usar en toda la aplicación
db = Database()