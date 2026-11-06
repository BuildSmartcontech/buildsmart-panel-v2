import streamlit as st

st.set_page_config(page_title="Política de Privacidad - SAMU IA", page_icon="🔒")

st.title("🔒 Política de Tratamiento de Datos Personales (SAMU IA)")
st.caption("Última actualización: Noviembre 2026")

st.markdown("""
### 1. Calidad del Tratamiento de Datos
SAMU IA (en adelante, "La Plataforma"), con domicilio en Colombia y correo de contacto **privacidad@samu-ia.com**, actúa en las siguientes calidades de acuerdo con la Ley 1581 de 2012:
- **Responsable del Tratamiento:** Respecto a los datos de identificación y facturación de nuestros clientes directos que adquieren los planes.
- **Encargado del Tratamiento:** Respecto a los datos de conversación, leads y registros del CRM que los clientes capturen de forma orgánica a través del software.

### 2. Datos Objeto de Tratamiento
Para la ejecución de la plataforma, recolectamos:
- **Datos de Identificación y Contacto:** Nombre, correo electrónico, teléfono del usuario registrado.
- **Datos Corporativos:** Información del negocio, sector comercial, dirección y credenciales de API.
- **Datos de Conversación y Operación (Módulo ARM):** Registros de texto e interacciones enviadas por los usuarios finales a los canales de WhatsApp enlazados por el cliente.

### 3. Transparencia en el Uso de Inteligencia Artificial y Transferencia Internacional
Para la ejecución del Agente de Respuesta Automática (ARM), los flujos de conversación de WhatsApp son procesados en tiempo real mediante interfaces de programación (APIs) por modelos de lenguaje de subprocesadores externos ubicados en el extranjero (**Groq Inc., Google LLC, OpenRouter**). Al aceptar esta política, el titular autoriza expresamente la transferencia internacional de sus datos. SAMU IA garantiza mediante acuerdos técnicos que dichos proveedores procesan la información de manera temporal y confidencial, y que ningún dato o conversación es utilizado para entrenar modelos de lenguaje públicos de terceros.

### 4. Finalidades del Tratamiento
Los datos recolectados se utilizarán estrictamente para:
- La generación técnica y alojamiento de páginas web optimizadas con IA.
- La calificación automática de prospectos (leads) y su sincronización opcional con el sistema ERP Odoo del cliente.
- El envío de notificaciones de soporte, actualizaciones técnicas y alertas de consumo del plan.

### 5. Ejercicio de Derechos (Hábeas Data y GDPR)
Como titular de la información, te asisten los derechos legales de conocer, actualizar, rectificar y solicitar la supresión de tus datos personales, así como revocar la autorización otorgada. Podrás ejercer estos derechos en cualquier momento remitiendo una solicitud formal detallando tu identidad al correo electrónico: **privacidad@samu-ia.com**. Las consultas serán resueltas en un plazo máximo de diez (10) días hábiles y los reclamos en quince (15) días hábiles según la legislación colombiana.
""")