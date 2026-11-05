# modules/header_footer.py
# ============================================
# HEADER Y FOOTER COMPARTIDOS
# ============================================

import streamlit as st
import datetime
from config_app import MODO, ES_DUENO, VERSION, NOMBRE_APP

E_CORONA    = "\U0001F451"
E_GLOBO     = "\U0001F310"
E_EMAIL     = "\U0001F4E7"
E_PAJARO    = "\U0001F426"
E_OK        = "\u2705"
E_X         = "\u274C"
E_REFRESH   = "\U0001F504"
E_RAYO      = "\u26A1"
E_LUPA      = "\U0001F50D"
E_AVISO     = "\u26A0\uFE0F"

def renderizar_header(BACKEND_ACTIVO, modulos):
    """Renderiza el header principal."""
    hora = datetime.datetime.now().strftime("%H:%M")

    if ES_DUENO:
        backend_icon = f"{E_OK} Backend Activo" if BACKEND_ACTIVO else f"{E_AVISO} Backend Inactivo"
        html = (
            '<div class="owner-header" style="padding: 1rem; background: #0f3460; color: white; border-radius: 10px; margin-bottom: 1rem;">'
            '<div style="display: flex; justify-content: space-between; align-items: center;">'
            '<div>'
            f'<h1 style="margin: 0;">{E_CORONA} {NOMBRE_APP} - PANEL DUENO</h1>'
            f'<p style="margin: 0; opacity: 0.9;">Modo: <b>{MODO.upper()}</b> | {backend_icon} | Version {VERSION}</p>'
            '</div>'
            '<div>'
            f'<span style="background: #2ecc71; padding: 5px 10px; border-radius: 5px;">{E_CORONA} ADMIN</span>'
            f'<span style="margin-left: 1rem;">{E_REFRESH} {hora}</span>'
            '</div>'
            '</div>'
            '</div>'
        )
        st.markdown(html, unsafe_allow_html=True)
    else:
        modulos_str = ""
        if modulos.get("web"): modulos_str += E_GLOBO
        if modulos.get("email"): modulos_str += E_EMAIL
        if modulos.get("social"): modulos_str += E_PAJARO
        if modulos.get("automation"): modulos_str += E_RAYO
        if modulos.get("research"): modulos_str += E_LUPA

        backend_icon = E_OK if BACKEND_ACTIVO else ""
        sub_linea = f"Panel de Control Multi-Negocio {backend_icon} {modulos_str}".strip()

        html = (
            '<div class="main-header" style="padding: 1rem; background: #f8f9fa; color: #333; border-radius: 10px; margin-bottom: 1rem; border: 1px solid #ddd;">'
            '<div style="display: flex; justify-content: space-between; align-items: center;">'
            '<div>'
            f'<h1 style="margin: 0;">{NOMBRE_APP}</h1>'
            f'<p style="margin: 0; opacity: 0.8;">{sub_linea}</p>'
            '</div>'
            '<div>'
            f'<span style="background: #2ecc71; color: white; padding: 5px 10px; border-radius: 5px;">{E_OK} SISTEMA ACTIVO</span>'
            f'<span style="margin-left: 1rem;">{E_REFRESH} {hora}</span>'
            '</div>'
            '</div>'
            '</div>'
        )
        st.markdown(html, unsafe_allow_html=True)

def renderizar_footer(BACKEND_ACTIVO, modulos):
    """Renderiza el footer principal."""
    backend_icon = E_OK if BACKEND_ACTIVO else E_X
    web_icon = E_OK if modulos.get('web') else E_X
    email_icon = E_OK if modulos.get('email') else E_X
    social_icon = E_OK if modulos.get('social') else E_X
    auto_icon = E_OK if modulos.get('automation') else E_X
    research_icon = E_OK if modulos.get('research') else E_X
    fecha = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    texto = (
        f"{NOMBRE_APP} v{VERSION} | Modo: {MODO} | Backend: {backend_icon} | "
        f"Web: {web_icon} | Email: {email_icon} | Social: {social_icon} | "
        f"Auto: {auto_icon} | Research: {research_icon} | {fecha}"
    )
    html = f'<div class="footer" style="text-align: center; padding: 1rem; color: #888; font-size: 0.8rem; margin-top: 2rem;">{texto}</div>'
    st.markdown(html, unsafe_allow_html=True)