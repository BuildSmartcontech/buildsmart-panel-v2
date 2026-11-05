# utils/odoo_service.py
# ============================================
# SERVICIO DE ODOO COMMUNITY (XML-RPC)
# ============================================

import os
import xmlrpc.client
import streamlit as st

def obtener_credenciales():
    """Lee de Secrets o Variables de Entorno."""
    url = os.getenv("ODOO_URL") or st.secrets.get("ODOO_URL", "http://localhost:8069")
    db = os.getenv("ODOO_DB") or st.secrets.get("ODOO_DB", "odoo_db")
    user = os.getenv("ODOO_USER") or st.secrets.get("ODOO_USER", "admin")
    password = os.getenv("ODOO_PASS") or st.secrets.get("ODOO_PASS", "admin")
    return url, db, user, password

def crear_lead_odoo(nombre, telefono, descripcion, email=None):
    """Crea un Lead en el CRM de Odoo."""
    url, db, user, password = obtener_credenciales()
    
    try:
        # Autenticación
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, user, password, {})
        if not uid:
            raise Exception("Credenciales de Odoo inválidas")

        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        # Crear Lead
        lead_data = {
            'name': f"Lead ARM: {nombre}",
            'contact_name': nombre,
            'phone': telefono,
            'email_from': email or '',
            'description': descripcion,
            'type': 'lead',
        }
        
        lead_id = models.execute_kw(db, uid, password, 'crm.lead', 'create', [lead_data])
        print(f"[ODOO] Lead creado exitosamente ID: {lead_id}")
        return True, lead_id
    except Exception as e:
        print(f"[ODOO ERROR] No se pudo crear el lead: {e}")
        return False, str(e)