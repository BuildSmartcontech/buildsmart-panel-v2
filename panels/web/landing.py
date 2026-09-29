# panels/web/landing.py
# ============================================
# LANDING PUBLICA - Web Gancho SAMU IA
# ============================================
# V4.0: Boton "Comprar" lleva al checkout real
# V3.0: Todas premium + hosting gratis visible
# V2.0: Usa landing_data + fix HTML
# V1.0: Version inicial
# ============================================

import streamlit as st
from panels.web import landing_data as D


# ==========================================
# HERO
# ==========================================
def _renderizar_hero():
    html = (
        '<div class="landing-hero">'
        f'<h1>{D.E_CORONA} SAMU IA Web</h1>'
        '<div class="hero-badge">'
        f'{D.E_GEMA} TODAS NUESTRAS WEBS SON PREMIUM'
        '</div>'
        '<p>Tu pagina web profesional generada con IA en minutos. '
        'Sin comisiones mensuales. Sin curva de aprendizaje. '
        f'<b>{D.E_REGALO} 1 año de hosting GRATIS</b> incluido.</p>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


# ==========================================
# BANNER PENDIENTES
# ==========================================
def _renderizar_banner_pendientes():
    pendientes = []
    for tier in D.TIERS:
        for f in tier.get("features", []):
            if f.get("pendiente"):
                pendientes.append(f"{tier['nombre']}: {f['texto']}")

    if not pendientes:
        return

    with st.expander(f"{D.E_AVISO} Aviso: features en desarrollo ({len(pendientes)})", expanded=False):
        st.markdown(
            f"**Las siguientes features estan en desarrollo y se activaran pronto:**\n\n"
            + "\n".join([f"- {p}" for p in pendientes])
        )
        st.caption("Todos los planes comprados incluyen estas features cuando esten listas, sin costo adicional.")


# ==========================================
# CARD DE UN TIER
# ==========================================
def _renderizar_card(tier):
    destacado = tier.get("destacado", False)
    clase_card = "tier-card destacado" if destacado else "tier-card"

    # Features con badges
    features_html = ""
    for f in tier["features"]:
        if f.get("pendiente"):
            features_html += f'<li><span class="badge-pendiente">PROXIMAMENTE</span> {f["texto"]}</li>'
        else:
            features_html += f'<li>{D.E_OK} {f["texto"]}</li>'

    # No incluye
    no_incluye_html = ""
    if tier.get("no_incluye"):
        for item in tier["no_incluye"]:
            no_incluye_html += f'<li>{D.E_X} {item}</li>'

    badge = '<div class="badge-destacado">MAS POPULAR</div>' if destacado else ''
    hosting_badge = tier.get("hosting_badge", "")

    html = (
        f'<div class="{clase_card}">'
        f'{badge}'
        f'<div class="tier-titulo">{tier["icono"]} {tier["nombre"]}</div>'
        f'<div class="tier-subtitulo">{tier["subtitulo"]}</div>'
        f'<div class="tier-precio">{tier["precio_label"]}</div>'
        f'<div class="tier-pago-label">{tier["pago_label"]}</div>'
        f'<div class="hosting-badge">{D.E_REGALO} {hosting_badge}</div>'
        f'<ul class="tier-features">{features_html}</ul>'
        f'<ul class="tier-features tier-no-incluye">{no_incluye_html}</ul>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

    st.write("")
    if st.button(
        tier["cta"],
        key=f"cta_{tier['id']}",
        use_container_width=True,
        type="primary" if destacado else "secondary",
    ):
        # Ir al checkout
        st.session_state["_web_checkout_tier"] = tier["id"]
        st.session_state["_web_subruta"] = "checkout"
        st.rerun()


# ==========================================
# SECCION: TODAS PREMIUM (diferencial)
# ==========================================
def _renderizar_todas_premium():
    html = (
        '<div class="todas-premium">'
        f'<h2>{D.E_GEMA} Todas nuestras webs son PREMIUM</h2>'
        '<p>No vendemos webs "basicas" ni "feas". '
        'Todas nuestras webs incluyen diseño moderno, generacion con IA '
        'y hosting gratis el primer año. La diferencia entre planes es '
        'cuantas herramientas incluís, no la calidad visual.</p>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


# ==========================================
# BOTON: QUE ES EL CRM
# ==========================================
def _renderizar_boton_crm():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.expander(f"{D.E_CEREBRO} ¿Que es un CRM y para que sirve?"):
            st.markdown(D.EXPLICACION_CRM)


# ==========================================
# BENEFICIOS
# ==========================================
def _renderizar_beneficios():
    st.markdown(f'<div class="seccion-titulo">{D.E_RAYO} Por que elegirnos</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        html = (
            '<div class="beneficio-card">'
            f'<h3>{D.E_RAYO} Rapido</h3>'
            '<p>Tu web lista en menos de 15 minutos. '
            'Sin contratar diseñadores ni esperar semanas.</p>'
            '</div>'
        )
        st.markdown(html, unsafe_allow_html=True)

    with col2:
        html = (
            '<div class="beneficio-card">'
            f'<h3>{D.E_DINERO} Sin comisiones</h3>'
            '<p>Pago unico, sin comisiones sobre tus ventas. '
            'Otros cobran 20%, nosotros USD 0.</p>'
            '</div>'
        )
        st.markdown(html, unsafe_allow_html=True)

    with col3:
        html = (
            '<div class="beneficio-card">'
            f'<h3>{D.E_ESCUDO} Sin lock-in</h3>'
            '<p>Si no renovas, te llevas el HTML de tu web. '
            'Sin secuestro de datos.</p>'
            '</div>'
        )
        st.markdown(html, unsafe_allow_html=True)


# ==========================================
# COMPARACION
# ==========================================
def _renderizar_comparacion():
    st.markdown(f'<div class="seccion-titulo">{D.E_LIBRO} Nosotros vs la competencia</div>', unsafe_allow_html=True)

    tabla = "| Aspecto | SAMU IA | Wix/Squarespace | Agencia |\n"
    tabla += "|---------|---------|-----------------|---------|\n"
    for c in D.COMPARACION:
        tabla += f"| {c['aspecto']} | **{c['samu']}** | {c['wix']} | {c['agencia']} |\n"

    st.markdown(tabla)


# ==========================================
# FAQ
# ==========================================
def _renderizar_faq():
    st.markdown(f'<div class="seccion-titulo">{D.E_PIN} Preguntas frecuentes</div>', unsafe_allow_html=True)
    for item in D.FAQ_ITEMS:
        with st.expander(item["pregunta"]):
            st.markdown(item["respuesta"])


# ==========================================
# RENDER PRINCIPAL
# ==========================================
def renderizar():
    """Renderiza la landing publica de Web Gancho."""

    st.markdown(D.CSS_LANDING, unsafe_allow_html=True)

    _renderizar_banner_pendientes()
    _renderizar_hero()

    st.markdown(f'<div class="seccion-titulo">{D.E_GLOBO} Elegi tu plan</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, tier in enumerate(D.TIERS):
        with cols[i]:
            _renderizar_card(tier)

    _renderizar_todas_premium()
    _renderizar_boton_crm()
    _renderizar_beneficios()
    _renderizar_comparacion()
    _renderizar_faq()

    st.divider()
    st.caption("SAMU IA · El ERP de las PYMES latinoamericanas · 2026")


if __name__ == "__main__":
    renderizar()