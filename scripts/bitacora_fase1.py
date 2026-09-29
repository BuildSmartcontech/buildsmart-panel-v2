# -*- coding: utf-8 -*-
from pathlib import Path

notas = Path("NOTAS_PROYECTO.md")

contenido = """

================================================================================
## 🗓️ BITACORA - 2026-09-25 (segunda parte de jornada)
================================================================================

### ✅ COMPLETADO

**Formulario de contacto premium:**
- formulario_leads.py V4.0 con botones WhatsApp + Llamar + Email
- SVG inline (sin emojis en codigo)
- Estilos premium (gradientes, hover, cubic-bezier)
- Pedidos_web_acciones.py V3.1 lee telefono + nombre negocio del pedido

**Checkout extendido (WhatsApp del negocio):**
- checkout.py V3.0 con campo "WhatsApp del negocio"
- Normalizacion automatica a formato internacional (+57...)
- Se guarda en datos_negocio.whatsapp_negocio

**Cloudflare V5.2 FUNCIONANDO:**
- Bug 8000006/8000096 resuelto
- Fix: manifest como CAMPO en data (no archivo)
- Fix: files con (hash, (None, content)) - sin filename/mime
- PROVIDERS_DESHABILITADOS = ["netlify"]
- Cloudflare habilitado como fallback

**Estado actual de proveedores:**
- Vercel: 99/100 deploys disponibles (principal)
- Cloudflare: 500/500 (fallback habilitado)
- Netlify: DESHABILITADO (cuenta suspendida)

**URL de la web del pedido c8c1f3c3:**
- https://samu-ia-b406912c-buildsmartcontech.vercel.app
- Con botones WhatsApp/Tel/Email funcionando

### 🎯 FASE 1 - PLAN DE CIERRE (para lanzar taller de webs)

**BLOQUE 1 (1.5h): Checkout extendido V4.0**
- 9 campos nuevos: email_contacto, direccion, ciudad, pais, horarios, instagram, facebook, tiktok, anio_fundacion
- Sector como dropdown (evita typos)
- Decisiones pendientes: dropdown vs texto, cuales campos finales

**BLOQUE 2 (2.5h): Brief + preview + aprobacion**
- Nuevos estados: brief_completado -> en_revision -> aprobado -> publicado
- Cliente recibe email "Cuentanos que quieres" al confirmar pago
- Panel del cliente con formulario de brief
- Preview en iframe + botones aprobar/rechazar
- Solo al aprobar -> publica en URL estable

**BLOQUE 3 (1.5h): Web generator V4.0**
- Prompt de IA usa los 9 campos nuevos
- La IA genera secciones automaticamente:
  - Si hay direccion -> seccion "Ubicacion" con mapa
  - Si hay horarios -> seccion "Horarios"
  - Si hay Instagram -> icono + link en footer
- Inyectar iconos de redes sociales

**FASE 1 = Web taller funcionando 100% automatico**

### 🔵 PENDIENTES (despues de Fase 1)

- Registro ePayco (necesita landing publica primero)
- Webhook de pago automatico
- Landing publica en dominio samu-ia.com
- Panel del dueno completo
- React Bits (Fase 2 - post-lanzamiento)
- PIME, Enterprise (Fase 3+)

================================================================================
"""

with open(notas, "a", encoding="utf-8") as f:
    f.write(contenido)

print("Bitacora actualizada")
print()

with open(notas, "r", encoding="utf-8") as f:
    lineas = f.readlines()
print(f"Total lineas: {len(lineas)}")
print()
print("Ultimas 20 lineas:")
for l in lineas[-20:]:
    print(l.rstrip())
