# panels/web/landing_data_v2.py
# ============================================
# DATOS Y CSS - LANDING V2.1 (DARK PREMIUM)
# ============================================

E_RAYO      = "\u26A1"
E_OK        = "\u2705"
E_X         = "\u274C"
E_ESTRELLA  = "\u2B50"
E_TROFEO    = "\U0001F3C6"
E_GEMA      = "\U0001F48E"
E_REGALO    = "\U0001F381"
E_AVISO     = "\u26A0\uFE0F"
E_GLOBO     = "\U0001F310"
E_CEREBRO   = "\U0001F9E0"
E_PIN       = "\U0001F4CC"
E_FUEGO     = "\U0001F525"
E_CHAT      = "\U0001F4AC"

from panels.web.logo_data import LOGO_HTML

from panels.web.logo_data import LOGO_HTML



TIERS = [
    {
        "id": "tier1", "nombre": "Web Premium Esencial", "icono": E_GLOBO,
        "precio": 149, "precio_label": "USD 149", "pago_label": "pago \u00fanico",
        "subtitulo": "Tu presencia online premium",
        "hosting_badge": "1 A\u00d1O HOSTING GRATIS",
        "features": [
            {"texto": "Web PREMIUM generada con IA", "pendiente": False},
            {"texto": "1 a\u00f1o de hosting GRATIS", "pendiente": False},
            {"texto": "Subdominio SAMU IA incluido", "pendiente": False},
            {"texto": "Dise\u00f1o moderno y responsive", "pendiente": False},
            {"texto": "SEO b\u00e1sico incluido", "pendiente": False},
        ],
        "no_incluye": ["CRM de leads", "Dominio propio"],
        "cta": "Elegir Esencial", "destacado": False,
    },
    {
        "id": "tier2", "nombre": "Web Premium + CRM", "icono": E_ESTRELLA,
        "precio": 299, "precio_label": "USD 299", "pago_label": "pago \u00fanico",
        "subtitulo": "Web premium + captura de clientes",
        "hosting_badge": "1 A\u00d1O HOSTING GRATIS",
        "features": [
            {"texto": "Todo lo de Premium Esencial", "pendiente": False},
            {"texto": "CRM de captura de leads", "pendiente": False},
            {"texto": "Formulario conectado a DB", "pendiente": False},
            {"texto": "Mini-panel para ver leads", "pendiente": False},
            {"texto": "Login por magic link", "pendiente": False},
        ],
        "no_incluye": ["Dominio propio"],
        "cta": "Elegir + CRM (Popular)", "destacado": True,
    },
    {
        "id": "tier3", "nombre": "Web Premium Plus", "icono": E_TROFEO,
        "precio": 499, "precio_label": "USD 499", "pago_label": "pago \u00fanico",
        "subtitulo": "Web + CRM + Dominio propio",
        "hosting_badge": "HOSTING + DOMINIO GRATIS",
        "features": [
            {"texto": "Todo lo de Premium + CRM", "pendiente": False},
            {"texto": "Dominio propio (.com) 1 a\u00f1o", "pendiente": False},
            {"texto": "CRM completo con historial", "pendiente": False},
            {"texto": "Logo custom subido por vos", "pendiente": False},
            {"texto": "Soporte prioritario (< 4h)", "pendiente": False},
        ],
        "no_incluye": [],
        "cta": "Elegir Premium Plus", "destacado": False,
    },
]

SECTORES_PRO = [
    {
        "titulo": "Consultorios Odontol\u00f3gicos",
        "desc": "Agenda de citas, ficha de pacientes, galer\u00eda de antes/despu\u00e9s y recordatorios autom\u00e1ticos.",
        "imagen": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=800&q=80",
        "color": "#00D4FF",
    },
    {
        "titulo": "Estudios de Arquitectura",
        "desc": "Portafolio de proyectos, renders 3D, ficha t\u00e9cnica de obras y formulario de cotizaci\u00f3n.",
        "imagen": "https://images.unsplash.com/photo-1487958449943-2429e8be8625?auto=format&fit=crop&w=800&q=80",
        "color": "#0077FF",
    },
    {
        "titulo": "Firmas de Ingenier\u00eda",
        "desc": "Presentaci\u00f3n de servicios t\u00e9cnicos, casos de \u00e9xito, certificaciones y contacto directo con ingenieros.",
        "imagen": "https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=800&q=80",
        "color": "#00D4FF",
    },
    {
        "titulo": "Empresas Corporativas",
        "desc": "Sitio institucional, secci\u00f3n de inversionistas, blog corporativo y portal de proveedores.",
        "imagen": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80",
        "color": "#0077FF",
    },
]

COMPARACION = [
    {"aspecto": "Precio inicial", "samu": "USD 149 (\u00fanico)", "wix": "USD 200+/a\u00f1o", "squarespace": "USD 192+/a\u00f1o", "polsia": "20% de tus ventas"},
    {"aspecto": "Comisi\u00f3n por venta", "samu": "0% (Tuyo es tuyo)", "wix": "0%", "squarespace": "0%", "polsia": "20% (Eterno)"},
    {"aspecto": "Tiempo de entrega", "samu": "24-48 horas", "wix": "3-5 d\u00edas", "squarespace": "3-5 d\u00edas", "polsia": "1-2 semanas"},
    {"aspecto": "Tecnolog\u00eda IA", "samu": "Groq + Gemini", "wix": "B\u00e1sica", "squarespace": "Nula", "polsia": "B\u00e1sica"},
    {"aspecto": "CRM incluido", "samu": "S\u00ed (Tier 2+)", "wix": "Pago extra", "squarespace": "Pago extra", "polsia": "No"},
    {"aspecto": "Soporte en espa\u00f1ol", "samu": "Humano real", "wix": "Bots/Foros", "squarespace": "Bots/Foros", "polsia": "S\u00ed"},
]

BONUS_ITEMS = [
    {"icono": E_CEREBRO, "titulo": "An\u00e1lisis Profundo con IA", "valor": "USD 99", "desc": "Reporte personalizado de tu sector, competencia y oportunidades."},
    {"icono": E_RAYO, "titulo": "3 Modificaciones Gratis", "valor": "USD 15", "desc": "Cambia textos, colores o secciones. La IA lo hace en segundos."},
    {"icono": E_GLOBO, "titulo": "Hosting Premium 1 A\u00f1o", "valor": "USD 60", "desc": "CDN global, sin l\u00edmites de tr\u00e1fico y sin multas por exceso."},
]

TESTIMONIOS = [
    {"nombre": "Mar\u00eda G.", "texto": "El pan de masa madre es simplemente espectacular, lo recomiendo a todos mis compa\u00f1eros de oficina.", "rol": "Cliente frecuente"},
    {"nombre": "Juan P.", "texto": "Los croissants son los mejores de la ciudad, perfectos para el desayuno.", "rol": "Vecino del barrio"},
    {"nombre": "Laura S.", "texto": "Me encanta la tarta de frutas, fresca y con una base ligera. Ideal para reuniones familiares.", "rol": "Cliente desde 2019"},
]

DEMO_BAKERY = {
    "titulo": "Panader\u00eda Premium Los Tres Amigos",
    "subtitulo": "Artesan\u00eda en masa madre y reposter\u00eda premium",
    "descripcion": "Mira lo que SAMU IA dise\u00f1\u00f3 para una panader\u00eda local en Bogot\u00e1 en un parpadeo. Textos persuasivos, im\u00e1genes generadas por IA y secciones autom\u00e1ticas (Ubicaci\u00f3n, Horarios, Contacto). Tu negocio se ver\u00e1 as\u00ed de premium hoy mismo.",
    "imagen_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=1200&q=80"
}

FAQ_ITEMS = [
    {"pregunta": "\u00bfCu\u00e1l es la diferencia entre los planes?", "respuesta": "La calidad visual es PREMIUM en los 3. La diferencia son las herramientas: el Tier 1 es solo la web. El Tier 2 agrega un CRM para capturar clientes. El Tier 3 incluye dominio propio y soporte VIP."},
    {"pregunta": "\u00bfEl hosting es realmente gratis?", "respuesta": "S\u00ed, el primer a\u00f1o es 100% GRATIS en todos los planes. Usamos infraestructura de alto rendimiento (Vercel/Cloudflare). Despu\u00e9s del a\u00f1o 1, la renovaci\u00f3n es de solo USD 59/a\u00f1o."},
    {"pregunta": "\u00bfQu\u00e9 m\u00e9todos de pago aceptan?", "respuesta": "Aceptamos transferencias bancarias locales (Nequi, Daviplata, Bancolombia) y tarjetas de cr\u00e9dito/d\u00e9bito a trav\u00e9s de nuestra pasarela segura ePayco."},
    {"pregunta": "\u00bfCu\u00e1ntas modificaciones gratis tengo?", "respuesta": "Todos los planes incluyen 3 modificaciones gratis gestionadas por nuestra IA. Si necesitas cambios extra despu\u00e9s, tienen un costo de USD 5 cada uno."},
    {"pregunta": "\u00bfCu\u00e1nto tarda en estar lista mi web?", "respuesta": "Una vez confirmamos tu pago, nuestra IA genera, dise\u00f1a y publica tu web en un promedio de 24 a 48 horas. Recibir\u00e1s la URL en tu correo."},
    {"pregunta": "\u00bfQu\u00e9 pasa si no me gusta el dise\u00f1o?", "respuesta": "Tus 3 modificaciones gratis sirven exactamente para eso. Ajustamos colores, textos y secciones hasta que quedes 100% satisfecho antes de la entrega final."},
]

CSS_LANDING_V2 = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Space+Grotesk:wght@500;700&display=swap');

.stApp { background-color: #050A14 !important; }
.block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 1200px; }
h1, h2, h3, h4 { color: #FFFFFF !important; font-family: 'Space Grotesk', sans-serif !important; }
p, li, label { color: #94A3B8 !important; }

.header-logo {
    display: flex; align-items: center; justify-content: center;
    padding: 4rem 1rem 2rem; margin-bottom: 4rem;
    min-height: 380px;
}
.logo-real {
    height: 260px !important;
    width: auto !important;
    max-width: 90% !important;
    border-radius: 20px;
    filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.4)) drop-shadow(0 0 40px rgba(0, 119, 255, 0.2));
    transition: transform 0.4s ease, filter 0.4s ease;
    animation: logoFloat 6s ease-in-out infinite;
}
.logo-real:hover { 
    transform: scale(1.04); 
    filter: drop-shadow(0 0 30px rgba(0, 212, 255, 0.6)) drop-shadow(0 0 60px rgba(0, 119, 255, 0.3));
}
@keyframes logoFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}
.logo-real:hover { 
    transform: scale(1.03); 
    filter: drop-shadow(0 0 35px rgba(0, 212, 255, 0.7));
}
.logo-real {
    height: 260px !important;
    width: auto !important;
    max-width: 90% !important;
    border-radius: 20px;
    filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.4)) drop-shadow(0 0 40px rgba(0, 119, 255, 0.2));
    transition: transform 0.4s ease, filter 0.4s ease;
    animation: logoFloat 6s ease-in-out infinite;
}
.logo-real:hover { 
    transform: scale(1.04); 
    filter: drop-shadow(0 0 30px rgba(0, 212, 255, 0.6)) drop-shadow(0 0 60px rgba(0, 119, 255, 0.3));
}
@keyframes logoFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}
.logo-real:hover { transform: scale(1.08); }
.logo-real {
    height: 260px !important;
    width: auto !important;
    max-width: 90% !important;
    border-radius: 20px;
    filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.4)) drop-shadow(0 0 40px rgba(0, 119, 255, 0.2));
    transition: transform 0.4s ease, filter 0.4s ease;
    animation: logoFloat 6s ease-in-out infinite;
}
.logo-real:hover { 
    transform: scale(1.04); 
    filter: drop-shadow(0 0 30px rgba(0, 212, 255, 0.6)) drop-shadow(0 0 60px rgba(0, 119, 255, 0.3));
}
@keyframes logoFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}
.logo-real:hover { transform: scale(1.05); }
.logo-real {
    height: 260px !important;
    width: auto !important;
    max-width: 90% !important;
    border-radius: 20px;
    filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.4)) drop-shadow(0 0 40px rgba(0, 119, 255, 0.2));
    transition: transform 0.4s ease, filter 0.4s ease;
    animation: logoFloat 6s ease-in-out infinite;
}
.logo-real:hover { 
    transform: scale(1.04); 
    filter: drop-shadow(0 0 30px rgba(0, 212, 255, 0.6)) drop-shadow(0 0 60px rgba(0, 119, 255, 0.3));
}
@keyframes logoFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}
.logo-real:hover { transform: scale(1.05); }
.logo-real {
    height: 260px !important;
    width: auto !important;
    max-width: 90% !important;
    border-radius: 20px;
    filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.4)) drop-shadow(0 0 40px rgba(0, 119, 255, 0.2));
    transition: transform 0.4s ease, filter 0.4s ease;
    animation: logoFloat 6s ease-in-out infinite;
}
.logo-real:hover { 
    transform: scale(1.04); 
    filter: drop-shadow(0 0 30px rgba(0, 212, 255, 0.6)) drop-shadow(0 0 60px rgba(0, 119, 255, 0.3));
}
@keyframes logoFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}
.logo-real:hover { transform: scale(1.08); }
.logo-real {
    height: 260px !important;
    width: auto !important;
    max-width: 90% !important;
    border-radius: 20px;
    filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.4)) drop-shadow(0 0 40px rgba(0, 119, 255, 0.2));
    transition: transform 0.4s ease, filter 0.4s ease;
    animation: logoFloat 6s ease-in-out infinite;
}
.logo-real:hover { 
    transform: scale(1.04); 
    filter: drop-shadow(0 0 30px rgba(0, 212, 255, 0.6)) drop-shadow(0 0 60px rgba(0, 119, 255, 0.3));
}
@keyframes logoFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}
.logo-real:hover { transform: scale(1.05); }
.header-logo svg {
    width: 56px; height: 56px; flex-shrink: 0;
    filter: drop-shadow(0 0 12px rgba(0, 212, 255, 0.4));
}
.header-logo svg {
    width: 40px; height: 40px; flex-shrink: 0;
}
.header-logo-text {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.4rem; font-weight: 700; color: #FFF;
    letter-spacing: 3px;
    text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
}
.header-logo-text span { color: #00D4FF; }
.header-logo-text span { color: #00D4FF; }
.header-logo-text span { color: #00D4FF; }

.hero-container { text-align: center; padding: 2rem 1rem 3rem; }
.hero-title { 
    font-size: 3.2rem; font-weight: 700; line-height: 1.1; margin-bottom: 1.5rem;
    background: linear-gradient(90deg, #00D4FF 0%, #0077FF 50%, #00D4FF 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-size: 200% auto; animation: shine 3s linear infinite;
}
@keyframes shine { to { background-position: 200% center; } }
.hero-subtitle { font-size: 1.2rem; color: #94A3B8; max-width: 700px; margin: 0 auto 2rem; line-height: 1.6; }
.ai-badge { 
    display: inline-flex; align-items: center; gap: 8px; 
    background: rgba(0, 212, 255, 0.1); border: 1px solid rgba(0, 212, 255, 0.3);
    padding: 6px 16px; border-radius: 999px; font-size: 0.85rem; color: #00D4FF;
    margin-bottom: 1.5rem; font-weight: 600;
}

.glass-card {
    background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px;
    padding: 2rem; min-height: 280px; transition: all 0.3s ease;
    display: flex; flex-direction: column; align-items: center;
}
.glass-card:hover { transform: translateY(-5px); border-color: rgba(0, 212, 255, 0.3); }
.glass-card h3 {
    word-break: keep-all;
    hyphens: none;
    text-align: center;
}

.tier-card { height: 100%; display: flex; flex-direction: column; }
.tier-card.destacado { 
    border-color: #00D4FF; 
    box-shadow: 0 0 30px rgba(0, 212, 255, 0.15); 
    position: relative;
    padding-bottom: 2.5rem !important;
}
.tier-precio { font-size: 2.5rem; font-weight: 700; color: #FFF; margin: 1rem 0; }
.tier-features { list-style: none; padding: 0; margin: 1.5rem 0; flex-grow: 1; }
.tier-features li { padding: 8px 0; color: #CBD5E1; font-size: 0.95rem; border-bottom: 1px solid rgba(255,255,255,0.05); }
.badge-popular { 
    position: absolute; top: -12px; left: 50%; transform: translateX(-50%);
    background: #00D4FF; color: #050A14; padding: 4px 12px; border-radius: 999px;
    font-size: 0.75rem; font-weight: 700; text-transform: uppercase;
}

.browser-mockup {
    background: #1E293B; border-radius: 12px; overflow: hidden;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1);
}
.browser-header { background: #0F172A; padding: 12px; display: flex; gap: 8px; }
.browser-dot { width: 12px; height: 12px; border-radius: 50%; background: #EF4444; }
.browser-dot:nth-child(2) { background: #F59E0B; }
.browser-dot:nth-child(3) { background: #10B981; }
.browser-img { width: 100%; height: auto; display: block; }

.sector-card {
    position: relative; overflow: hidden;
    border-radius: 16px; height: 320px;
    cursor: pointer; transition: all 0.4s ease;
}
.sector-card:hover { transform: translateY(-8px); }
.sector-img {
    width: 100%; height: 100%; object-fit: cover;
    transition: transform 0.6s ease;
}
.sector-card:hover .sector-img { transform: scale(1.08); }
.sector-overlay {
    position: absolute; bottom: 0; left: 0; right: 0;
    background: linear-gradient(to top, rgba(5,10,20,0.95) 0%, rgba(5,10,20,0.7) 60%, transparent 100%);
    padding: 2rem 1.5rem 1.5rem;
}
.sector-tag {
    display: inline-block; padding: 4px 10px; border-radius: 999px;
    font-size: 0.7rem; font-weight: 700; color: #050A14;
    margin-bottom: 0.5rem; text-transform: uppercase;
}
.sector-title { color: #FFF; font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem; }
.sector-desc { color: #CBD5E1; font-size: 0.85rem; line-height: 1.5; }

.comparison-table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
.comparison-table th { text-align: left; padding: 12px; color: #00D4FF; border-bottom: 1px solid rgba(255,255,255,0.1); font-size: 0.9rem; }
.comparison-table td { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #CBD5E1; font-size: 0.9rem; }
.comparison-table tr:hover { background: rgba(255,255,255,0.02); }

.section-title { text-align: center; font-size: 2.2rem; margin: 4rem 0 1rem; color: #FFF; }
.section-subtitle { text-align: center; color: #94A3B8; margin-bottom: 3rem; font-size: 1.05rem; }

.footer-solido {
    background: #111827;
    border-top: 1px solid rgba(255,255,255,0.08);
    padding: 2rem 1rem;
    text-align: center;
    margin-top: 4rem;
}
.footer-solido p { color: #64748B; font-size: 0.85rem; margin: 0; }
.footer-solido .footer-brand { color: #00D4FF; font-weight: 600; }
</style>
"""











