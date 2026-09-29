# backend/storage.py - Storage

import psycopg2
import os
from dotenv import load_dotenv
import json

load_dotenv()

class Storage:
    def __init__(self):
        self.conn_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'postgres'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'mi_password')
        }
    
    def get_connection(self):
        return psycopg2.connect(**self.conn_params)
    
    def guardar_tarea(self, negocio_id, titulo, descripcion, categoria, creditos=1):
        """Guardar una tarea en la base de datos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tareas (negocio_id, titulo, descripcion, categoria, creditos, estado)
            VALUES (%s, %s, %s, %s, %s, 'TODO')
            RETURNING id
        """, (negocio_id, titulo, descripcion, categoria, creditos))
        tarea_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return tarea_id
    
    def obtener_tareas(self, negocio_id=None):
        """Obtener tareas de un negocio"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if negocio_id:
            cursor.execute("""
                SELECT id, titulo, descripcion, categoria, estado, creditos, creado_en
                FROM tareas
                WHERE negocio_id = %s AND estado != 'HECHO'
                ORDER BY creado_en DESC
            """, (negocio_id,))
        else:
            cursor.execute("""
                SELECT id, titulo, descripcion, categoria, estado, creditos, creado_en
                FROM tareas
                WHERE estado != 'HECHO'
                ORDER BY creado_en DESC
            """)
        tareas = cursor.fetchall()
        cursor.close()
        conn.close()
        return tareas

storage = Storage()