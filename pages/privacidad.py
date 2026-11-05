import streamlit as st

st.set_page_config(page_title="Política de Privacidad - SAMU IA", page_icon="🔒")

st.title("🔒 Política de Tratamiento de Datos Personales")
st.caption("Última actualización: Noviembre 2026")

st.markdown("""
### 1. Responsable del Tratamiento
SAMU IA (en adelante, "La Plataforma"), con domicilio en Colombia, es el responsable del tratamiento de los datos personales recolectados a través de sus sitios web, formularios y servicios de automatización.

### 2. Datos que Recolectamos
- **Datos de Identificación:** Nombre, correo electrónico, teléfono.
- **Datos Comerciales:** Información de tu PIME (Nombre del negocio, sector, dirección).
- **Datos de Conversación (ARM):** Mensajes de WhatsApp enviados por tus clientes.

### 3. Uso de Inteligencia Artificial (Transparencia)
Para el funcionamiento del módulo ARM (Automated Relationship Manager), **las conversaciones de WhatsApp son procesadas por modelos de lenguaje de terceros** (Groq, OpenRouter, Google Gemini). SAMU IA no utiliza estas conversaciones para entrenar sus propios modelos.

### 4. Finalidad
Los datos son utilizados exclusivamente para:
- Generar tu página web con IA.
- Calificar leads y sincronizarlos con tu sistema Odoo.
- Enviarte notificaciones sobre tu cuenta.

### 5. Tus Derechos (Habeas Data)
Como titular de los datos, tienes derecho a conocer, actualizar, rectificar y solicitar la eliminación de tu información. Puedes ejercer estos derechos escribiendo a: **privacidad@samu-ia.com**.
""")