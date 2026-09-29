# panels/__init__.py
# ============================================
# Inicializacion de modulos de paneles
# ============================================
# Al importar panels, aplica los hooks de logging
# sobre panel_base para registrar eventos automaticamente.
# ============================================

# Aplicar hooks de logging (silencioso si falla)
try:
    from panels import panel_base_hooks
    panel_base_hooks.aplicar_hooks()
except Exception as e:
    print(f"[panels] No se pudieron aplicar hooks: {e}")