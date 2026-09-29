# panels/web/landing_v2.py
# ============================================
# LANDING PUBLICA V2.1 - DARK PREMIUM
# ============================================

import streamlit as st
from panels.web import landing_data_v2 as D


def _renderizar_header():
    st.markdown(
        f'<div class="header-logo">'
        f'{D.LOGO_HTML}'
        f'</div>',
        unsafe_allow_html=True
    )


def _renderizar_hero():
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown(
        '<div class="ai-badge">'
        f'{D.E_RAYO} Potenciado por Groq + OpenRouter + Gemini'
        '</div>', 
        unsafe_allow_html=True
    )
    st.markdown(
        '<h1 class="hero-title">Tu Negocio en Internet con IA.<br>En 60 Segundos y por un \u00danico Pago.</h1>', 
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="hero-subtitle">Sin cuotas mensuales eternas. SAMU IA crea tu p\u00e1gina web premium, '
        'te entrega un CRM automatizado y hosting gratis por 1 a\u00f1o.</p>', 
        unsafe_allow_html=True
    )
    
    if st.button(f"{D.E_RAYO} Crear mi Web Ahora", key="hero_cta", use_container_width=False):
        st.session_state["_web_checkout_tier"] = "tier2"
        st.session_state["_web_subruta"] = "checkout"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def _renderizar_demo():
    demo = D.DEMO_BAKERY
    st.markdown(f'<h2 class="section-title">{D.E_GEMA} As\u00ed se ve tu negocio en SAMU IA</h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="section-subtitle">{demo["subtitulo"]}</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown(
            f'<div class="browser-mockup">'
            '<div class="browser-header">'
            '<div class="browser-dot"></div><div class="browser-dot"></div><div class="browser-dot"></div>'
            '</div>'
            f'<img src="{demo["imagen_url"]}" class="browser-img" alt="Demo Web">'
            '</div>', 
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(f"### {demo['titulo']}", unsafe_allow_html=True)
        st.markdown(demo["descripcion"])
        st.markdown(f"**Resultado:** Web publicada en 24h con secciones autom\u00e1ticas de Ubicaci\u00f3n, Horarios y Contacto.")


def _renderizar_sectores():
    st.markdown(f'<h2 class="section-title">{D.E_GLOBO} Para cada profesi\u00f3n</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">SAMU IA se adapta a tu industria. As\u00ed se ver\u00eda tu sitio.</p>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, sector in enumerate(D.SECTORES_PRO):
        with cols[i % 2]:
            st.markdown(
                f'<div class="sector-card">'
                f'<img src="{sector["imagen"]}" class="sector-img" alt="{sector["titulo"]}">'
                f'<div class="sector-overlay">'
                f'<span class="sector-tag" style="background:{sector["color"]}">CASO REAL</span>'
                f'<div class="sector-title">{sector["titulo"]}</div>'
                f'<div class="sector-desc">{sector["desc"]}</div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True
            )


def _renderizar_tiers():
    st.markdown(f'<h2 class="section-title">{D.E_GLOBO} Elige tu Plan</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Pago \u00fanico. Sin letras chicas. Hosting gratis el primer a\u00f1o.</p>', unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, tier in enumerate(D.TIERS):
        with cols[i]:
            destacado = "destacado" if tier["destacado"] else ""
            badge = '<div class="badge-popular">M\u00c1S POPULAR</div>' if tier["destacado"] else ''
            
            features_html = "".join([f"<li>{D.E_OK} {f['texto']}</li>" for f in tier["features"]])
            no_incluye_html = "".join([f"<li style='color:#64748B'>{D.E_X} {item}</li>" for item in tier["no_incluye"]])
            
            html = (
                f'<div class="glass-card tier-card {destacado}">{badge}'
                f'<h3>{tier["icono"]} {tier["nombre"]}</h3>'
                f'<p style="color:#94A3B8; font-size:0.9rem">{tier["subtitulo"]}</p>'
                f'<div class="tier-precio">{tier["precio_label"]}</div>'
                f'<p style="color:#64748B; font-size:0.85rem; margin-top:-10px">{tier["pago_label"]}</p>'
                f'<ul class="tier-features">{features_html}{no_incluye_html}</ul>'
                f'</div>'
            )
            st.markdown(html, unsafe_allow_html=True)
            
            btn_type = "primary" if tier["destacado"] else "secondary"
            if st.button(tier["cta"], key=f"cta_{tier['id']}", use_container_width=True, type=btn_type):
                st.session_state["_web_checkout_tier"] = tier["id"]
                st.session_state["_web_subruta"] = "checkout"
                st.rerun()


def _renderizar_bonus():
    st.markdown(f'<h2 class="section-title">{D.E_REGALO} Bonus de Lanzamiento</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Valor total: USD 174. Gratis para los primeros 50 clientes.</p>', unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, bonus in enumerate(D.BONUS_ITEMS):
        with cols[i]:
            st.markdown(
                f'<div class="glass-card" style="text-align:center">'
                f'<div style="font-size:2.5rem; margin-bottom:1rem">{bonus["icono"]}</div>'
                f'<h3>{bonus["titulo"]}</h3>'
                f'<p style="color:#00D4FF; font-weight:700">Valor: {bonus["valor"]}</p>'
                f'<p>{bonus["desc"]}</p>'
                f'</div>', 
                unsafe_allow_html=True
            )


def _renderizar_comparacion():
    st.markdown(f'<h2 class="section-title">{D.E_FUEGO} SAMU IA vs La Competencia</h2>', unsafe_allow_html=True)
    
    tabla = '<table class="comparison-table"><thead><tr><th>Aspecto</th><th style="color:#00D4FF">SAMU IA</th><th>Wix</th><th>Squarespace</th><th>Polsia</th></tr></thead><tbody>'
    for c in D.COMPARACION:
        tabla += f"<tr><td>{c['aspecto']}</td><td><b>{c['samu']}</b></td><td>{c['wix']}</td><td>{c['squarespace']}</td><td>{c['polsia']}</td></tr>"
    tabla += '</tbody></table>'
    st.markdown(tabla, unsafe_allow_html=True)


def _renderizar_testimonios():
    st.markdown(f'<h2 class="section-title">{D.E_CHAT} Lo que dicen los clientes</h2>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, t in enumerate(D.TESTIMONIOS):
        with cols[i]:
            st.markdown(
                f'<div class="glass-card">'
                f'<p style="font-style:italic; color:#CBD5E1">"{t["texto"]}"</p>'
                f'<p style="color:#00D4FF; font-weight:700; margin-top:1rem">{t["nombre"]}</p>'
                f'<p style="font-size:0.8rem; color:#64748B">{t["rol"]}</p>'
                f'</div>', 
                unsafe_allow_html=True
            )


def _renderizar_faq():
    st.markdown(f'<h2 class="section-title">{D.E_PIN} Preguntas Frecuentes</h2>', unsafe_allow_html=True)
    for item in D.FAQ_ITEMS:
        with st.expander(item["pregunta"]):
            st.markdown(item["respuesta"])


def _renderizar_footer():
    st.markdown(
        '<div class="footer-solido">'
        '<p><span class="footer-brand">SAMU IA</span> \u00b7 Tu Orquestador Digital \u00b7 2026</p>'
        '<p style="margin-top:0.5rem; font-size:0.75rem">Colombia \u00b7 LATAM \u00b7 Global</p>'
        '</div>',
        unsafe_allow_html=True
    )


def renderizar():
    st.markdown(D.CSS_LANDING_V2, unsafe_allow_html=True)
    
    _renderizar_header()
    _renderizar_hero()
    st.divider()
    _renderizar_demo()
    st.divider()
    _renderizar_sectores()
    st.divider()
    _renderizar_tiers()
    st.divider()
    _renderizar_bonus()
    st.divider()
    _renderizar_comparacion()
    st.divider()
    _renderizar_testimonios()
    st.divider()
    _renderizar_faq()
    _renderizar_footer()


if __name__ == "__main__":
    renderizar()


