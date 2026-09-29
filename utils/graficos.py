# utils/graficos.py
# ============================================
# GRAFICOS CON PLOTLY - SAMU IA V2.0
# ============================================
# Dark theme premium para el panel del dueno.
# Paleta moderna, lineas suaves, sin toolbar.
# Todo texto visible en espanol.
# ============================================

from datetime import datetime, timedelta
from collections import Counter

import plotly.graph_objects as go


# ==========================================
# PALETA MODERNA
# ==========================================
BG_CARD       = "#1e293b"       # fondo tarjeta (mismo que KPIs)
BG_PLOT       = "#1e293b"
TEXTO         = "#cbd5e1"       # texto claro
TEXTO_TITULO  = "#f1f5f9"       # texto titulos
GRILLA         = "rgba(255,255,255,0.06)"
BORDE         = "#334155"

COLOR_AZUL    = "#3b82f6"
COLOR_VIOLETA = "#8b5cf6"
COLOR_CORAL   = "#f43f5e"
COLOR_ESMER   = "#10b981"
COLOR_AMBAR   = "#f59e0b"
COLOR_CIAN    = "#06b6d4"

PALETA_DONUT = [
    COLOR_AZUL, COLOR_VIOLETA, COLOR_CORAL, COLOR_ESMER,
    COLOR_AMBAR, COLOR_CIAN, "#ec4899", "#84cc16",
]

# Layout base reutilizable
LAYOUT_BASE = dict(
    paper_bgcolor=BG_CARD,
    plot_bgcolor=BG_PLOT,
    font=dict(family="Inter, sans-serif", size=12, color=TEXTO),
    margin=dict(l=50, r=20, t=60, b=50),
    height=340,
    hoverlabel=dict(
        bgcolor=BG_CARD,
        bordercolor=BORDE,
        font=dict(color=TEXTO_TITULO, size=12),
    ),
)


def _config_plotly():
    """Config para st.plotly_chart (oculta toolbar)."""
    return {"displayModeBar": False, "staticPlot": False}


def _titulo(texto):
    return dict(
        text=texto,
        font=dict(size=15, color=TEXTO_TITULO, family="Inter, sans-serif"),
        x=0.02,
        xanchor="left",
        y=0.96,
        yanchor="top",
    )


def _ejes_base(x_titulo="", y_titulo=""):
    return dict(
        xaxis=dict(
            title=x_titulo,
            gridcolor=GRILLA,
            linecolor=BORDE,
            zeroline=False,
            tickfont=dict(size=11, color=TEXTO),
            title_font=dict(size=12, color=TEXTO),
        ),
        yaxis=dict(
            title=y_titulo,
            gridcolor=GRILLA,
            linecolor=BORDE,
            zeroline=False,
            tickfont=dict(size=11, color=TEXTO),
            title_font=dict(size=12, color=TEXTO),
        ),
    )


def _parse_fecha(val):
    if not val:
        return None
    try:
        if isinstance(val, datetime):
            return val
        s = str(val).replace("Z", "").split("+")[0].split(".")[0]
        return datetime.fromisoformat(s)
    except Exception:
        return None


# ==========================================
# GRAFICO 1 - EVENTOS POR DIA (linea suave)
# ==========================================
def eventos_por_dia(eventos, dias=30):
    hoy = datetime.now().date()
    inicio = hoy - timedelta(days=dias - 1)
    conteo = Counter()
    for e in eventos:
        f = _parse_fecha(e.get("created_at"))
        if f and f.date() >= inicio:
            conteo[f.date()] += 1

    fechas = [inicio + timedelta(days=i) for i in range(dias)]
    valores = [conteo.get(f, 0) for f in fechas]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fechas, y=valores,
        mode="lines+markers",
        line=dict(color=COLOR_CORAL, width=3, shape="spline", smoothing=1.3),
        marker=dict(size=7, color=COLOR_CORAL, line=dict(color=BG_CARD, width=2)),
        fill="tozeroy",
        fillcolor="rgba(244,63,94,0.12)",
        name="Eventos",
        hovertemplate="<b>%{x|%d %b}</b><br>Eventos: %{y}<extra></extra>",
    ))
    fig.update_layout(
        title=_titulo(f"Eventos por dia (ultimos {dias} dias)"),
        showlegend=False,
        **_ejes_base("Fecha", "Eventos"),
        **LAYOUT_BASE,
    )
    return fig


# ==========================================
# GRAFICO 2 - USUARIOS NUEVOS POR DIA (barras)
# ==========================================
def usuarios_nuevos_por_dia(negocios, dias=30):
    hoy = datetime.now().date()
    inicio = hoy - timedelta(days=dias - 1)

    primera_aparicion = {}
    for n in negocios:
        uid = n.get("usuario_id")
        f = _parse_fecha(n.get("created_at"))
        if uid and f:
            if uid not in primera_aparicion or f < primera_aparicion[uid]:
                primera_aparicion[uid] = f

    conteo = Counter()
    for uid, f in primera_aparicion.items():
        if f.date() >= inicio:
            conteo[f.date()] += 1

    fechas = [inicio + timedelta(days=i) for i in range(dias)]
    valores = [conteo.get(f, 0) for f in fechas]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=fechas, y=valores,
        marker=dict(
            color=COLOR_AZUL,
            line=dict(color=COLOR_AZUL, width=0),
        ),
        name="Usuarios nuevos",
        hovertemplate="<b>%{x|%d %b}</b><br>Nuevos: %{y}<extra></extra>",
    ))
    fig.update_layout(
        title=_titulo(f"Usuarios nuevos por dia (ultimos {dias} dias)"),
        showlegend=False,
        bargap=0.35,
        **_ejes_base("Fecha", "Usuarios nuevos"),
        **LAYOUT_BASE,
    )
    return fig


# ==========================================
# GRAFICO 3 - NEGOCIOS POR SECTOR (dona)
# ==========================================
def negocios_por_sector(negocios):
    conteo = Counter()
    for n in negocios:
        sector = n.get("sector") or n.get("sector_contexto") or "Sin sector"
        conteo[sector] += 1

    if not conteo:
        return None

    labels = list(conteo.keys())
    valores = list(conteo.values())

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=valores,
        hole=0.58,
        marker=dict(
            colors=PALETA_DONUT[:len(labels)],
            line=dict(color=BG_CARD, width=3),
        ),
        textinfo="label+percent",
        textfont=dict(size=11, color=TEXTO_TITULO),
        hovertemplate="<b>%{label}</b><br>Cantidad: %{value}<br>%{percent}<extra></extra>",
    )])
    fig.update_layout(
        title=_titulo("Negocios por sector"),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(size=11, color=TEXTO),
            bgcolor="rgba(0,0,0,0)",
        ),
        **LAYOUT_BASE,
    )
    return fig


# ==========================================
# GRAFICO 4 - WEBS POR SEMANA (barras)
# ==========================================
def webs_por_semana(negocios, semanas=8):
    hoy = datetime.now().date()
    inicio = hoy - timedelta(weeks=semanas)
    inicio = inicio - timedelta(days=inicio.weekday())

    conteo = Counter()
    for n in negocios:
        sitio = n.get("sitio_web") or {}
        url = n.get("web_url") or sitio.get("url_publica")
        if not url:
            continue
        f = _parse_fecha(n.get("updated_at") or n.get("created_at"))
        if f and f.date() >= inicio:
            semana_inicio = f.date() - timedelta(days=f.weekday())
            conteo[semana_inicio] += 1

    etiquetas = []
    valores = []
    for i in range(semanas):
        s = inicio + timedelta(weeks=i)
        etiquetas.append(s.strftime("%d/%m"))
        valores.append(conteo.get(s, 0))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=etiquetas, y=valores,
        marker=dict(
            color=COLOR_ESMER,
            line=dict(color=COLOR_ESMER, width=0),
        ),
        name="Webs publicadas",
        hovertemplate="<b>Semana %{x}</b><br>Webs: %{y}<extra></extra>",
    ))
    fig.update_layout(
        title=_titulo(f"Webs publicadas por semana (ultimas {semanas})"),
        showlegend=False,
        bargap=0.35,
        **_ejes_base("Semana", "Webs"),
        **LAYOUT_BASE,
    )
    return fig


# ==========================================
# CONFIG PARA STREAMLIT
# ==========================================
def render_plotly(st_module, fig):
    """Wrapper que aplica config sin toolbar."""
    st_module.plotly_chart(fig, use_container_width=True, config=_config_plotly())