# -*- coding: utf-8 -*-
from pathlib import Path
notas = Path("NOTAS_PROYECTO.md")
contenido = """

### 2026-09-25 - Bloque 3 (Web Generator V4.0) COMPLETADO

**5 archivos modificados:**
- utils/web_prompts_data.py V2.0
  - Reglas CSS premium (cubic-bezier, scroll-driven animations)
  - Instrucciones condicionales: Ubicacion, Horarios, Redes, WhatsApp
  - Funcion construir_instrucciones_dinamicas()
- utils/web_prompts.py V6.0
  - generar_prompt_web() recibe 10 campos extendidos
  - Inyecta instrucciones dinamicas segun datos disponibles
  - Prompt basico: ~7000 chars | Completo: ~10000 chars
- utils/web_generator.py V4.0
  - generar_web() pasa campos extendidos a generar_prompt_web()
  - Log de campos activos
- utils/web_module.py V2.0
  - crear_web() pasa TODOS los 15 campos (antes solo 5)
  - Normaliza nombre/nombre_negocio y whatsapp/telefono
- panels/dueno/pedidos_web_acciones.py V3.2
  - Arma datos_negocio completo desde el pedido
  - Log de campos extendidos activos

**Resultados:**
- La IA genera secciones automaticas segun campos del pedido
- Si hay direccion -> seccion Ubicacion con Google Maps embed
- Si hay horarios -> seccion Horarios con tabla premium
- Si hay redes -> iconos SVG en footer con links
- Si hay anio -> mencion en Sobre Nosotros
- Si hay WhatsApp -> boton con link wa.me
- Si hay email -> email visible en contacto

**Compatibilidad:**
- Prompt de edicion V1 y V2 siguen funcionando
- Deteccion de sector con IA no cambia
- Imagenes Pollinations sin cambios

"""
with open(notas, "a", encoding="utf-8") as f:
    f.write(contenido)
print("OK bitacora actualizada")
