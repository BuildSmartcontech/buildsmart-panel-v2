# panels/web/landing_data.py
# ============================================
# DATOS DE LA LANDING - Web Gancho SAMU IA
# ============================================
# V2.0: TODAS las webs son premium + hosting GRATIS 1 año
# V1.0: Version inicial
# ============================================


# ==========================================
# EMOJIS ASCII-SAFE
# ==========================================
E_CORONA    = "\U0001F451"
E_GLOBO     = "\U0001F310"
E_RAYO      = "\u26A1"
E_OK        = "\u2705"
E_X         = "\u274C"
E_DINERO    = "\U0001F4B0"
E_ESTRELLA  = "\u2B50"
E_LIBRO     = "\U0001F4D8"
E_LLAVE     = "\U0001F511"
E_PIN       = "\U0001F4CC"
E_TROFEO    = "\U0001F3C6"
E_ESCUDO    = "\U0001F6E1\uFE0F"
E_AVISO     = "\u26A0\uFE0F"
E_CEREBRO   = "\U0001F9E0"
E_GEMA      = "\U0001F48E"
E_REGALO    = "\U0001F381"


# ==========================================
# TIERS
# ==========================================
TIERS = [
    {
        "id": "tier1",
        "nombre": "Web Premium Esencial",
        "icono": E_GLOBO,
        "precio": 149,
        "precio_label": "USD 149",
        "pago_label": "pago unico",
        "subtitulo": "Tu presencia online premium",
        "hosting_badge": "1 AÑO HOSTING GRATIS (valor USD 60)",
        "features": [
            {"texto": "Web PREMIUM generada con IA", "pendiente": False},
            {"texto": "1 año de hosting GRATIS (valor USD 60)", "pendiente": False},
            {"texto": "Subdominio SAMU IA incluido", "pendiente": False},
            {"texto": "Diseño moderno y responsive", "pendiente": False},
            {"texto": "SEO basico incluido", "pendiente": False},
        ],
        "no_incluye": [
            "CRM de leads",
            "Dominio propio",
            "Panel de administracion",
        ],
        "cta": "Comprar Premium Esencial",
        "destacado": False,
    },
    {
        "id": "tier2",
        "nombre": "Web Premium + CRM",
        "icono": E_ESTRELLA,
        "precio": 299,
        "precio_label": "USD 299",
        "pago_label": "pago unico",
        "subtitulo": "Web premium + captura de clientes",
        "hosting_badge": "1 AÑO HOSTING GRATIS (valor USD 60)",
        "features": [
            {"texto": "Todo lo de Premium Esencial", "pendiente": False},
            {"texto": "1 año de hosting GRATIS (valor USD 60)", "pendiente": False},
            {"texto": "CRM de captura de leads", "pendiente": False},
            {"texto": "Formulario conectado a base de datos", "pendiente": False},
            {"texto": "Mini-panel para ver leads", "pendiente": False},
            {"texto": "Marcar leads: contactado / cerrado", "pendiente": False},
            {"texto": "Login por magic link", "pendiente": False},
        ],
        "no_incluye": [
            "Dominio propio",
            "Logo custom",
        ],
        "cta": "Comprar Premium + CRM",
        "destacado": True,
    },
    {
        "id": "tier3",
        "nombre": "Web Premium Plus",
        "icono": E_TROFEO,
        "precio": 499,
        "precio_label": "USD 499",
        "pago_label": "pago unico",
        "subtitulo": "Web premium + CRM + Dominio propio",
        "hosting_badge": "1 AÑO HOSTING GRATIS + DOMINIO (valor USD 75)",
        "features": [
            {"texto": "Todo lo de Premium + CRM", "pendiente": False},
            {"texto": "1 año de hosting GRATIS + dominio propio", "pendiente": False},
            {"texto": "CRM completo con historial", "pendiente": False},
            {"texto": "Logo custom subido por vos", "pendiente": False},
            {"texto": "Soporte prioritario (< 4h)", "pendiente": False},
            {"texto": "Efectos visuales premium (React Bits)", "pendiente": True},
        ],
        "no_incluye": [],
        "cta": "Comprar Premium Plus",
        "destacado": False,
    },
]


# ==========================================
# COMPARACION
# ==========================================
COMPARACION = [
    {"aspecto": "Precio web premium", "samu": "USD 149", "wix": "USD 200-300/año", "agencia": "USD 800+"},
    {"aspecto": "Hosting año 1", "samu": "GRATIS (valor $60)", "wix": "Incluido", "agencia": "Pago extra"},
    {"aspecto": "Comisiones de venta", "samu": "0%", "wix": "0%", "agencia": "0%"},
    {"aspecto": "Tiempo de entrega", "samu": "15 minutos", "wix": "3-5 dias", "agencia": "2-4 semanas"},
    {"aspecto": "CRM incluido", "samu": "Desde USD 299", "wix": "Pago extra", "agencia": "Pago extra"},
    {"aspecto": "Soporte en español", "samu": "Si", "wix": "Limitado", "agencia": "Si"},
    {"aspecto": "Generacion con IA", "samu": "Si", "wix": "No", "agencia": "No"},
]


# ==========================================
# FAQ
# ==========================================
FAQ_ITEMS = [
    {
        "pregunta": "¿Todas las webs son premium?",
        "respuesta": """
**SI.** Todas nuestras webs son de calidad premium.

La diferencia entre planes es **cuantas herramientas incluís**,
NO que tan bonita es tu web. Todas tienen:

- Diseño moderno y responsive
- Generacion con IA
- Hosting incluido 1 año
- SEO basico

La diferencia es:
- **Premium Esencial:** solo la web
- **Premium + CRM:** web + captura de clientes
- **Premium Plus:** web + CRM + dominio propio + soporte prioritario
        """,
    },
    {
        "pregunta": "¿El hosting es gratis?",
        "respuesta": """
**Si, el primer año es GRATIS** en todos los planes.

El hosting tiene un valor real de **USD 60/año**, pero nosotros lo
incluimos sin costo en tu pago unico. Asi no tenes que preocuparte
por facturas mensuales durante el primer año.

Despues del año 1:
- **Premium Esencial y Premium + CRM:** renovacion por USD 59/año
- **Premium Plus:** renovacion por USD 79/año (incluye dominio)
        """,
    },
    {
        "pregunta": "¿Que pasa despues del primer año?",
        "respuesta": """
Tenes **3 opciones**:

- **Opcion A:** Renovar por USD 59/año (o USD 79 en Premium Plus).
- **Opcion B:** Descargar el HTML de tu web y llevartela.
- **Opcion C:** Actualizar al plan PIME (USD 99/mes) y obtener el ERP completo.

**Sin secuestro de datos.** Vos decidis.
        """,
    },
    {
        "pregunta": "¿Necesito saber de diseño o programacion?",
        "respuesta": """
**No.** La IA genera tu web automaticamente basandose en la informacion
de tu negocio. Solo completas un formulario con datos basicos y en
minutos tenes tu pagina lista.
        """,
    },
    {
        "pregunta": "¿Puedo actualizar de Premium Esencial a Premium + CRM?",
        "respuesta": """
**Si.** En cualquier momento pagas la diferencia (USD 150) y agregamos
el CRM de captura de leads a tu web existente. No perdes nada.
        """,
    },
    {
        "pregunta": "¿Que metodos de pago aceptan?",
        "respuesta": """
Tarjetas de credito y debito via **Stripe** (Visa, Mastercard,
American Express). Proximamente otros metodos locales.
        """,
    },
]


# ==========================================
# EXPLICACION DEL CRM
# ==========================================
EXPLICACION_CRM = """
**CRM = Customer Relationship Management**
*(Gestion de Relaciones con Clientes)*

### ¿Para que sirve?

Es una herramienta que te permite:

- **Capturar** los datos de las personas que te contactan desde tu web
- **Organizar** tu lista de prospectos y clientes en un solo lugar
- **Marcar** el estado de cada uno (nuevo, contactado, cerrado)
- **Dar seguimiento** sin perder oportunidades en WhatsApp o papel

### ¿Como funciona en SAMU IA?

1. Un visitante entra a tu web y llena el formulario de contacto
2. Automaticamente queda guardado en tu CRM
3. Recibis una notificacion por email
4. Entras a tu mini-panel y ves todos los leads
5. Marca cada uno como "contactado" o "cerrado"

### Sin CRM vs Con CRM

| Sin CRM | Con CRM |
|---------|---------|
| Los leads se pierden en email | Todos los leads en un panel |
| WhatsApp sin seguimiento | Historial de cada contacto |
| No sabes cuantos te contactaron | Metricas claras |
| Cero organizacion | Estados: nuevo/contactado/cerrado |

**El CRM convierte tu web de "tarjeta de presentacion" a "maquina de clientes".**
"""


# ==========================================
# CSS
# ==========================================
CSS_LANDING = """
<style>
    .landing-hero {
        text-align: center;
        padding: 3rem 1rem 2rem 1rem;
    }
    .landing-hero h1 {
        font-size: 3rem;
        margin-bottom: 1rem;
        color: #1e293b;
    }
    .landing-hero p {
        font-size: 1.15rem;
        color: #64748b;
        max-width: 750px;
        margin: 0 auto 1rem auto;
        font-style: italic;
    }
    .hero-badge {
        display: inline-block;
        background: #fef3c7;
        color: #92400e;
        padding: 0.5rem 1rem;
        border-radius: 999px;
        font-weight: 600;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
    }
    .tier-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        padding: 2rem 1.5rem;
        height: 100%;
    }
    .tier-card.destacado {
        border-color: #3b82f6;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15);
    }
    .tier-titulo {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #1e293b;
    }
    .tier-subtitulo {
        color: #64748b;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
        font-style: italic;
    }
    .tier-precio {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 0.25rem;
    }
    .tier-pago-label {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-bottom: 1rem;
        font-style: italic;
    }
    .hosting-badge {
        background: #d1fae5;
        color: #065f46;
        padding: 0.5rem 0.75rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
    }
    .tier-features {
        list-style: none;
        padding: 0;
        margin: 1rem 0;
    }
    .tier-features li {
        padding: 0.4rem 0;
        color: #334155;
        font-size: 0.9rem;
    }
    .tier-no-incluye li {
        color: #94a3b8;
        text-decoration: line-through;
    }
    .badge-destacado {
        background: #3b82f6;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .badge-pendiente {
        background: #f59e0b;
        color: white;
        padding: 0.1rem 0.5rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-right: 0.4rem;
    }
    .seccion-titulo {
        text-align: center;
        font-size: 2rem;
        margin: 3rem 0 1rem 0;
        color: #1e293b;
        font-style: italic;
    }
    .beneficio-card {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .beneficio-card p {
        font-style: italic;
    }
    .todas-premium {
        background: linear-gradient(135deg, #dbeafe 0%, #ede9fe 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
    }
    .todas-premium h2 {
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    .todas-premium p {
        color: #475569;
        font-style: italic;
        max-width: 600px;
        margin: 0 auto;
    }
</style>
"""


if __name__ == "__main__":
    print(f"Tiers: {len(TIERS)}")
    print(f"Items comparacion: {len(COMPARACION)}")
    print(f"FAQ: {len(FAQ_ITEMS)}")
    print(f"CSS: {len(CSS_LANDING)} chars")
    for t in TIERS:
        print(f"  {t['nombre']}: {t['precio_label']}")