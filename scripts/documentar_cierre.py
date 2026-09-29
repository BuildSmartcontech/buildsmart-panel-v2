# -*- coding: utf-8 -*-
from pathlib import Path
from datetime import datetime

notas = Path("NOTAS_PROYECTO.md")

contenido = """

### 2026-09-25 - BLOQUE WEBS CERRADO (Vercel como principal)

**PROVEEDOR PRINCIPAL: VERCEL**
- URL estable: https://samu-ia-{web_id[:8]}-buildsmartcontech.vercel.app
- Tambien disponible: https://samu-ia-{web_id[:8]}.vercel.app (mas corta)
- Cuota: 100 deploys/dia (Free plan)
- Token: VERCEL_TOKEN (en .env)
- API: POST /v13/deployments con files en base64
- Devuelve aliases estables (no efimeros)

**CLOUDFLARE (fallback - bug API pendiente):**
- Cuota: 500 deploys/mes
- Error 8000006 en POST /deployments
- Codigo V5.1 intenta arreglarlo enviando manifest como archivo multipart
- Hash BLAKE3 correcto (len=32)
- DESHABILITADO hasta validar fix

**NETLIFY (deshabilitado):**
- Cuenta samuellesmes suspendida por sistema antifraude
- Provocaba 401 en todos los endpoints
- PROVIDERS_DESHABILITADOS = ["netlify"]

**LIMPIEZA DE CODIGO:**
- 28 backups de utils/ movidos a _backups/
- 17 backups de panels/ movidos a _backups/
- config/utils/ (legacy) movida a _backups/
- utils/ ahora: 46 archivos activos
- panels/ ahora: 7 archivos activos

**AUDITORIA DE CONSUMO:**
- 5 llamadas reales a publicar_web() (controlado)
- Publicacion DIRECTA al provider elegido (sin intentos fallidos)
- Failover automatico entre providers habilitados

**FLUJO COMPLETO VALIDADO:**
1. IA genera HTML (Groq) - 1 token IA
2. Guarda en disco local - $0
3. Guarda metadata en Supabase - $0
4. ProviderManager elige Vercel (100/100 restantes)
5. Vercel publica - 1 credito
6. URL estable devuelta al cliente

**G11 CERRADO:**
- Formulario guarda leads en crm_leads
- 2 leads verificados en DB

**PENDIENTES DOCUMENTADOS:**
- Cloudflare V5.1 sin validar (probable fix del 8000006)
- Actualizar provider_manager para sitios nuevos nacidos publicos
- Landing 3+1 opciones
- Login diferenciado por plan (Supabase Auth)
- Sistema de cobro (Wompi/ePayco/MercadoPago)
- CRM completo

"""

with open(notas, "a", encoding="utf-8") as f:
    f.write(contenido)

print("NOTAS_PROYECTO.md actualizado con UTF-8 correcto")

# Verificar ultimas 30 lineas
print()
print("=" * 70)
print("ULTIMAS 30 LINEAS:")
print("=" * 70)
with open(notas, "r", encoding="utf-8") as f:
    lineas = f.readlines()
for l in lineas[-30:]:
    print(l.rstrip())
