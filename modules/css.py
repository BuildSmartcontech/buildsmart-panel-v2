# modules/css.py
# ============================================
# CSS PERSONALIZADO DE SAMU IA
# ============================================

import streamlit as st

def renderizar_css():
    """Renderiza el CSS personalizado."""
    st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1a1a2e, #16213e, #0f3460);
        padding: 1rem 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #0f3460;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .business-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        border: 2px solid #e0e0e0;
        transition: all 0.3s;
        cursor: pointer;
    }
    .business-card:hover {
        border-color: #0f3460;
        box-shadow: 0 4px 12px rgba(15,52,96,0.2);
    }
    .business-card.selected {
        border-color: #0f3460;
        background: #f0f4ff;
    }
    .status-active {
        color: #00a65a;
        font-weight: bold;
    }
    .task-card {
        background: white;
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 0.5rem;
        border: 1px solid #e0e0e0;
        transition: all 0.2s;
    }
    .task-card:hover {
        border-color: #0f3460;
        box-shadow: 0 2px 8px rgba(15,52,96,0.1);
    }
    .task-card.todo { border-left: 4px solid #f39c12; }
    .task-card.done { border-left: 4px solid #2ecc71; opacity: 0.7; }
    .task-card.in-progress { border-left: 4px solid #3498db; }
    .agent-badge {
        background: #0f3460;
        color: white;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
    }
    .credit-badge {
        background: #f39c12;
        color: white;
        padding: 2px 8px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: bold;
    }
    .footer {
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid #e0e0e0;
        color: #888;
        font-size: 0.8rem;
        text-align: center;
    }
    .chat-message-user {
        background: #0f3460;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .chat-message-agent {
        background: #e8ecf1;
        color: #1a1a2e;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin-bottom: 10px;
        max-width: 80%;
        margin-left: auto;
    }
    .chat-message-processing {
        background: #fff3cd;
        color: #856404;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin-bottom: 10px;
        max-width: 80%;
        margin-left: auto;
        border: 1px solid #ffc107;
    }
    .timeline-item {
        padding: 8px 0;
        border-bottom: 1px solid #f0f0f0;
        font-size: 0.9rem;
    }
    .section-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #0f3460;
        margin-bottom: 0.5rem;
    }
    .status-badge {
        padding: 2px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: bold;
    }
    .status-badge.activo { background: #d4edda; color: #155724; }
    .status-badge.inactivo { background: #f8d7da; color: #721c24; }
    .status-badge.en-pausa { background: #fff3cd; color: #856404; }
    .social-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 0.5rem;
        border: 1px solid #e0e0e0;
    }
    .social-card:hover { border-color: #0f3460; }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    .processing-text { animation: pulse 1.5s ease-in-out infinite; }
    .feature-badge {
        background: #28a745;
        color: white;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.6rem;
        font-weight: bold;
        display: inline-block;
        margin-left: 5px;
    }
    .feature-badge.off { background: #dc3545; }
    .backend-status {
        background: #e8f4fd;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        color: #0f3460;
        border: 1px solid #0f3460;
    }
    .web-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        border: 2px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .web-card.activa { border-left: 5px solid #00a65a; }
    .web-card.por_expirar { border-left: 5px solid #f39c12; }
    .web-card.expirada { border-left: 5px solid #dc3545; }
    
    /* ===== PANEL DUENO ===== */
    .owner-header {
        background: linear-gradient(90deg, #2c1810, #4a2810, #6b3410);
        padding: 1rem 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .owner-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #f39c12;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .kpi-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #e0e0e0;
        text-align: center;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        color: #0f3460;
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #888;
        text-transform: uppercase;
    }
    .alert-warning {
        background: #fff3cd;
        color: #856404;
        padding: 10px 15px;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin-bottom: 10px;
    }
    .alert-success {
        background: #d4edda;
        color: #155724;
        padding: 10px 15px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin-bottom: 10px;
    }
    .alert-danger {
        background: #f8d7da;
        color: #721c24;
        padding: 10px 15px;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)