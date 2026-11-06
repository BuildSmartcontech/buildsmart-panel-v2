import streamlit as st

st.set_page_config(page_title="Política de Privacidad - SAMU IA", page_icon="🔒")

st.title("🔒 Política de Tratamiento de Datos Personales (SAMU IA)")
st.caption("Última actualización: Noviembre 2026")

st.markdown("""
### 1. Calidad del Tratamiento de Datos

SAMU IA (en adelante, "La Plataforma"), con domicilio en Colombia y correo de contacto privacidad@samu-ia.com, actúa en las siguientes calidades de acuerdo con la Ley 1581 de 2012:
- **Responsable del Tratamiento:** Respecto a los datos de identificación y facturación de nuestros clientes directos que adquieren los planes comerciales.
- **Encargado del Tratamiento:** Respecto a los datos de conversación, capturas de prospectos (leads) y registros del CRM que los clientes capturen de forma orgánica a través de las herramientas del software.

### 2. Datos Objeto de Tratamiento

Para la correcta ejecución y despliegue de la plataforma, recolectamos de manera directa o mediante automatizaciones:
- **Datos de Identificación y Contacto:** Nombre completo, dirección de correo electrónico y número de teléfono móvil del usuario registrado.
- **Datos Corporativos y Técnicos:** Información comercial del negocio, sector del mercado, dirección física y credenciales de autenticación para integraciones externas (claves de API).
- **Datos de Conversación y Operación (Módulo ARM):** Registros de texto, metadatos e interacciones enviadas por los usuarios finales a los canales de mensajería (WhatsApp) enlazados de manera autónoma por el cliente.

### 3. Transparencia en el Uso de Inteligencia Artificial y Transferencia Internacional

Para la ejecución del Agente de Respuesta Automática (ARM), los flujos de conversación entrantes de WhatsApp son procesados en tiempo real mediante interfaces de programación (APIs) por modelos de lenguaje administrados por subprocesadores externos ubicados en el extranjero (Groq Inc., Google LLC y OpenRouter).
- Al aceptar la presente política, el titular autoriza expresamente la transferencia internacional de sus datos hacia dichas jurisdicciones.
- SAMU IA garantiza mediante acuerdos y políticas técnicas que dichos proveedores procesan la información de manera estrictamente temporal y confidencial.
- Ningún dato personal o histórico de conversación provisto a las APIs corporativas es utilizado para entrenar modelos de lenguaje públicos de terceros.

### 4. Finalidades del Tratamiento

Los datos personales recolectados bajo este marco se utilizarán estrictamente para las siguientes actividades legítimas:
- La generación técnica, optimización constante y alojamiento en servidores de páginas web personalizadas con Inteligencia Artificial.
- La calificación automática de prospectos (leads) en los chats y su posterior sincronización opcional con el sistema ERP Odoo parametrizado por el cliente.
- El envío de notificaciones internas de soporte, alertas de seguridad, actualizaciones técnicas y avisos de consumo de los recursos de la cuenta.

### 5. Ejercicio de Derechos (Hábeas Data y GDPR)

Como titular de la información, te asisten los derechos legales de conocer, actualizar, rectificar y solicitar la supresión de tus datos personales, así como revocar la autorización otorgada en los términos normativos vigentes.
- Podrás ejercer estos derechos en cualquier momento remitiendo una solicitud formal detallando tu identidad al correo electrónico: **privacidad@samu-ia.com**.
- Las consultas de información serán resueltas en un plazo máximo de diez (10) días hábiles y los reclamos o solicitudes de eliminación en quince (15) días hábiles, de conformidad con lo estipulado por la legislación colombiana.
""")