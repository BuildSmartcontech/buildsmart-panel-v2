# panels/web/onboarding_arm.py
# ============================================
# ASISTENTE DE ONBOARDING - ARM PREMIUM PLUS
# ============================================
# V1.1: Checkbox legal Meta y fix de variables entre pasos.
# ============================================

import streamlit as st
try:
    from utils.supabase_rest import supabase_rest
except ImportError:
    supabase_rest = None

def renderizar(cliente_id):
    st.markdown("## 🤖 Configuración de tu ARM (Vendedor Automático)")
    st.info("¡Felicidades por tu plan Premium Plus! Para que la IA venda por ti, necesitamos conectar tu WhatsApp y tu Odoo.")

    paso = st.session_state.get("arm_paso", 1)
    
    if paso == 1:
        st.markdown("### Paso 1: Requisitos previos")
        st.markdown("""
        Para que el ARM funcione, necesitas tener listo:
        1. **Cuenta de Meta Business:** Verificada y con método de pago registrado (los costos de conversación de WhatsApp corren por tu cuenta).
        2. **Un BSP (Business Solution Provider):** Te recomendamos Twilio o 360dialog para conectar tu número a la API oficial de Meta.
        3. **Odoo Community:** Tu sistema contable instalado y accesible por internet.
        4. **API Key de IA:** Una cuenta en OpenRouter o Groq (te daremos un tutorial).
        """)
        if st.button("Ya tengo todo, continuar", type="primary"):
            st.session_state["arm_paso"] = 2
            st.rerun()

    elif paso == 2:
        st.markdown("### Paso 2: Conectar tu Odoo")
        st.caption("Estos datos nos permiten enviar los leads calificados a tu sistema contable.")
        with st.form("form_odoo"):
            odoo_url = st.text_input("URL de Odoo", placeholder="https://tu-odoo.com")
            odoo_db = st.text_input("Nombre de la Base de Datos")
            odoo_user = st.text_input("Usuario (Email)")
            odoo_pass = st.text_input("Contraseña", type="password")
            
            if st.form_submit_button("Probar Conexión", type="primary"):
                if odoo_url and odoo_user and odoo_pass:
                    # Guardar en session_state para usarlo en el paso 3
                    st.session_state["arm_odoo_url"] = odoo_url
                    st.session_state["arm_odoo_db"] = odoo_db
                    st.session_state["arm_odoo_user"] = odoo_user
                    st.session_state["arm_odoo_pass"] = odoo_pass
                    
                    st.success("✅ Conexión a Odoo exitosa. Credenciales guardadas.")
                    st.session_state["arm_paso"] = 3
                    st.rerun()
                else:
                    st.error("Completa todos los campos.")

    elif paso == 3:
        st.markdown("### Paso 3: Conectar WhatsApp (Meta API)")
        st.caption("Pega el Token de acceso de tu BSP y el ID de tu número de teléfono.")
        with st.form("form_meta"):
            meta_token = st.text_input("Token de Acceso (Permanent Token)", type="password")
            phone_id = st.text_input("ID del Número de Teléfono (Phone Number ID)")
            
            # NUEVO CHECKBOX LEGAL META
            acepta_meta = st.checkbox(
                "Acepto que soy el único responsable de mi cuenta de Meta Business, del pago de las conversaciones y de contar con el consentimiento de mis clientes para recibir mensajes."
            )
            
            if st.form_submit_button("Guardar y Activar ARM", type="primary"):
                if not acepta_meta:
                    st.error("Debes aceptar la cláusula de responsabilidad de Meta para continuar.")
                    return
                
                if meta_token and phone_id:
                    # Recuperar variables de Odoo del paso 2
                    odoo_url = st.session_state.get("arm_odoo_url", "")
                    odoo_db = st.session_state.get("arm_odoo_db", "")
                    odoo_user = st.session_state.get("arm_odoo_user", "")
                    odoo_pass = st.session_state.get("arm_odoo_pass", "")

                    if supabase_rest and supabase_rest.disponible:
                        try:
                            supabase_rest.table("clientes").update({
                                "odoo_url": odoo_url, "odoo_db": odoo_db,
                                "odoo_user": odoo_user, "odoo_pass": odoo_pass,
                                "meta_token": meta_token, "phone_id": phone_id,
                                "plan": "premium_plus"
                            }).eq("id", cliente_id).execute()
                        except Exception as e:
                            st.error(f"Error guardando: {e}")
                            return

                    st.balloons()
                    st.success("🎉 ¡ARM Activado! La IA ya está lista para responder en tu WhatsApp y guardar leads en tu Odoo.")
                    st.session_state["arm_paso"] = 1
                else:
                    st.error("Completa todos los campos.")