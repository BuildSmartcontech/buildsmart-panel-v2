import streamlit as st

st.set_page_config(page_title="Términos y Condiciones - SAMU IA", page_icon="📜")

st.title("📜 Términos y Condiciones del Servicio")

st.markdown("""
### 1. Naturaleza del Servicio
SAMU IA proporciona herramientas de software para la creación de páginas web con IA y automatización de ventas (CRM y ARM). **SAMU IA no es una agencia de marketing ni un BSP (Business Solution Provider) autorizado por Meta.**

### 2. Costos de Terceros (Meta, BSP e IA)
El cliente reconoce y acepta que los costos de:
- La API de WhatsApp Cloud (Meta).
- El BSP (Twilio, 360dialog, etc.).
- Los tokens de consumo de IA (Groq, OpenRouter, Gemini).
**Corren por cuenta exclusiva del cliente.** SAMU IA no factura ni gestiona estos pagos.

### 3. Plan Premium Plus y ARM
El plan Premium Plus tiene un costo de configuración inicial y una **suscripción mensual (USD 150)** por el uso del software ARM. El límite es de **1,500 conversaciones procesadas al mes**. Superar este límite generará cobros adicionales o requerirá el paso al plan Enterprise.

### 4. Responsabilidad sobre los Datos
El cliente es el único responsable de obtener el consentimiento de sus clientes finales para el envío de mensajes de WhatsApp y el tratamiento de sus datos, cumpliendo con las normativas locales de su país.
""")