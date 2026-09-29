# NOTAS_PROYECTO.md - SAMU IA (ex BuildSmart Holdings)

> Bitacora oficial del proyecto SAMU IA.
> Ultima actualizacion: 2026-09-18
> Version activa: 3.6

================================================================================
## 🏢 LOS NEGOCIOS DE SAMU IA (4 EN TOTAL)
================================================================================

### Negocio 1: WEB GANCHO (Servicio directo)
- Precio: $199 pago unico + $10/mes opcional (con administracion)
- Con CRM: +$10/mes adicional
- Sin CRM: solo pago unico, el cliente se la lleva
- Cliente: Personas/pequenos que solo necesitan web
- Estado: AMARILLO - Base lista, falta landing + login + cobro

### Negocio 2: PIME (Panel Multi-Negocio)
- Precio: $99/mes (provisional)
- Incluye: Web + CRM + Panel + Todos los modulos
- Cliente: Emprendedores y PIMEs
- Estado: VERDE - En desarrollo avanzado (V3.7 base + panel dueno V3.1)

### Negocio 3: DESDE CERO
- Precio: $99/mes (provisional)
- Incluye: Onboarding guiado completo
- Cliente: Emprendedores que empiezan desde 0
- Estado: VERDE - En desarrollo (onboarding.py existe)

### Negocio 4: ENTERPRISE
- Precio: $299/mes (provisional)
- Incluye: Todo + features avanzadas
- Cliente: Empresas grandes
- Estado: MORADO - En desarrollo (NO saldra al comercio aun)

================================================================================
## 🔀 ROUTER DE PANELES
================================================================================

### Variable de entorno: BUILDSMART_ES_DUENO

| Valor | Panel que se carga | Archivo |
|-------|-------------------|---------|
| True | Panel del Dueno (control total) | panels/panel_dueno.py |
| False | Panel de Usuario normal | panels/panel_usuario.py |
| No seteada | Default True (config_app.py) | Panel del Dueno |

### Como prender/apagar

**PowerShell (temporal):**
    $env:BUILDSMART_ES_DUENO = "True"
    $env:BUILDSMART_ES_DUENO = "False"

**Permanente (.env):**
    BUILDSMART_ES_DUENO=True

### Flujo en app.py
    from config_app import ES_DUENO
    from panels import panel_usuario, panel_dueno
    if ES_DUENO:
        panel_dueno.renderizar()
    else:
        panel_usuario.renderizar()

================================================================================
## 📏 REGLAS DE CODIGO (NUEVAS - 2026-09-18)
================================================================================

### Regla 1: Ningun archivo supera 400 lineas
- Si un archivo crece mas → modularizar en carpeta
- Aplica retroactivo cuando toquemos archivos grandes

### Regla 2: Ciclo cerrado o pendiente registrado
- Antes de arrancar: decidir si se cierra hoy o queda pendiente
- Si queda pendiente → registrar en esta bitacora con:
  - Que falta exactamente
  - Por que se pospone
  - Cuando retomar
- NADA "a medias" sin registro

### Regla 3: Orquestador protegido
- El orquestador de IA (chat + intents + personalidad) NUNCA se separa
- Cuando modularicemos panel_base.py:
  - Modulos perifericos (web, tareas, correo) → se separan
  - Orquestador → queda intacto en UN solo archivo
- Razon: efectividad del chat depende de coherencia entre intents + contexto + personalidad

### Regla 4: Prohibido scripts fix_encoding genericos
- Si hay mojibake → restaurar desde _backup_YYYYMMDD_HHMMSS/
- NO usar scripts genericos que borran emojis

### Regla 5: Archivo completo, nunca fragmentos
- Cada archivo enviado debe ser completo
- NO "busca esta linea y reemplaza"

### Regla 6: Visual 100% espanol
- UI visible al usuario: siempre espanol
- Codigo interno: como ha estado (mixed)
- App sera multi-idioma (global) → i18n pendiente

================================================================================
## 📊 ESTADO ACTUAL DE MODULOS
================================================================================

### COMPLETADOS Y FUNCIONANDO

**Nivel 1 - Panel del Dueno (4/4)**
| Modulo | Version | Estado |
|--------|---------|--------|
| M1: Logging automatico a eventos_app | V1.0 | OK |
| M2: Graficos Plotly dark premium | V2.0 | OK |
| M3: Filtros de fecha globales | V1.0 | OK |
| M4: Detalle cliente con historial | V1.0 | OK |

**Nivel 2 - Operaciones (3/7)**
| Modulo | Version | Estado |
|--------|---------|--------|
| M6: Suspender/reactivar cuentas | V1.0 | OK |
| M8: Republicar web forzado | V1.0 | OK |
| M11: Salud del sistema (6 APIs) | V2.0 | OK |
| M5: Moderacion de contenido | - | PENDIENTE |
| M7: Uso IA por usuario | - | PENDIENTE |
| M9: Staff/roles | - | PENDIENTE |
| M10: Auditoria de cambios | - | PENDIENTE |

**Otros modulos base**
| Modulo | Version |
|--------|---------|
| Generacion web con IA | V3.1 |
| Editor estructurado | V2.2 |
| Persistencia Supabase | V1.0 |
| Persistencia REST (supabase_rest.py) | V1.0 |
| Chat con dialectos (Intent Detection) | V1.2 |
| Personalidad custom por negocio | V1.0 |
| Diseño premium (cards flotantes) | V4.3 |
| Anti-alucinacion | V4.3 |
| Sistema Hibrido de Sectores | V1.2 |
| Web Premium (Netlify publico) | V3.0 |

### PENDIENTES (por prioridad)

| Modulo | Prioridad |
|--------|-----------|
| Sistema webs individuales (Negocio 1) | ROJO CRITICO |
| Landing page 3+1 opciones | ROJO CRITICO |
| Login diferenciado por plan | ROJO CRITICO |
| Sistema de cobro (Stripe) | ROJO CRITICO |
| **Modularizacion de panel_dueno.py** | **ROJO CRITICO** |
| **Modularizacion de panel_base.py (orquestador protegido)** | **NARANJA ALTO** |
| Refactor salud.py config-driven | NARANJA ALTO |
| M5 Moderacion | NARANJA ALTO |
| M7 Uso IA por usuario | NARANJA ALTO |
| M9 Staff/roles | NARANJA ALTO |
| M10 Auditoria | NARANJA ALTO |
| Alertas visuales en panel | NARANJA ALTO |
| CRM completo | NARANJA ALTO |
| Codigos de barras | NARANJA ALTO |
| Contabilidad (Odoo Community) | NARANJA ALTO |
| Sucursales/Replicas (50%) | AMARILLO MEDIO |
| Cuotas detalladas de APIs (post-Stripe) | AMARILLO MEDIO |
| Nuevas API de Gemini (rotacion) | AMARILLO MEDIO |
| Logo automatico por nicho | AMARILLO MEDIO |
| Subir imagenes a Supabase Storage | AMARILLO MEDIO |
| i18n multi-idioma | AMARILLO MEDIO |
| Pulido visual final (emojis, textos truncados) | AMARILLO MEDIO |
| use_container_width → width (Streamlit 2025-12) | AMARILLO MEDIO |
| Toggle "modo admin puro" | AMARILLO BAJO |
| Negocio 4 Enterprise | AZUL LARGO PLAZO |
| App movil nativa | AZUL LARGO PLAZO |

================================================================================
## 🗄️ SUPABASE - TABLAS ACTIVAS
================================================================================

Proyecto: gbjsjbiyoyjzodznrjjj.supabase.co

### Tablas del sistema
- negocios (existente - columnas: id, usuario_id, data JSON, created_at, updated_at)
- historial_chat (existente)
- suscripciones (NUEVA 2026-09-17)
- eventos_app (NUEVA 2026-09-17)
- config_global (NUEVA 2026-09-17)
- usuarios_sistema (NUEVA 2026-09-18) - estado de cuentas

### IMPORTANTE: estructura de negocios
Los datos reales estan en `data` (JSON):
    {
      "id": "test_negocio_1",
      "usuario_id": "...",
      "data": { "nombre": "...", "sector": "...", "tareas": [...], ... },
      "created_at": "...",
      "updated_at": "..."
    }
Usar helper `_plano()` en panel_dueno para aplanar.

### config_global (9 claves)
- modo_app = "prueba"
- precio_web = 199
- precio_pime = 99
- precio_desde_cero = 99
- precio_enterprise = 299
- modificaciones_gratis_prod = 3
- modificaciones_gratis_prueba = 7
- costo_modificacion_extra = 5
- landing_activa = true

================================================================================
## 📁 ESTRUCTURA DEL PROYECTO
================================================================================

    buildsmart-panel/
    ├── app.py                      # Router principal (ES_DUENO)
    ├── config_app.py               # Config global
    ├── auto_sync.py                # Respaldo a Supabase
    ├── .env                        # Credenciales (NO subir a git)
    ├── NOTAS_PROYECTO.md           # Este archivo
    │
    ├── panels/
    │   ├── panel_base.py           # V5.3 - logica reutilizable
    │   ├── panel_dueno.py          # V3.1 - control total (7 tabs)
    │   ├── panel_usuario.py        # Envuelve base + onboarding
    │   └── onboarding.py
    │
    ├── panels/dueno/               # PROXIMO: modularizar panel_dueno
    │   ├── __init__.py             # Orquesta renderizar()
    │   ├── comun.py                # Helpers, emojis, filtros
    │   ├── tab_panel.py
    │   ├── tab_clientes.py
    │   ├── tab_ingresos.py
    │   ├── tab_webs.py
    │   ├── tab_registros.py
    │   ├── tab_config.py
    │   ├── tab_salud.py
    │   └── detalle_cliente.py
    │
    ├── modules/
    │   ├── css.py
    │   ├── header_footer.py
    │   └── sidebar.py
    │
    ├── utils/
    │   ├── supabase_rest.py        # Cliente REST minimal
    │   ├── supabase_client.py      # Cliente custom (historial_chat)
    │   ├── supabase_storage.py
    │   ├── netlify_publisher.py
    │   ├── web_publisher.py
    │   ├── web_generator.py
    │   ├── web_editor_v2.py
    │   ├── sector_detector.py
    │   ├── image_fetcher.py
    │   ├── logger.py               # Logging a eventos_app
    │   ├── graficos.py             # Graficos Plotly dark premium
    │   ├── salud.py                # Chequeo de APIs
    │   ├── chat_detector.py
    │   ├── ia.py
    │   ├── html_patcher.py
    │   ├── persistence.py
    │   ├── web_prompts.py
    │   └── (mas)
    │
    ├── backend/
    │   ├── gateway.py
    │   ├── main.py
    │   ├── orquestador.py
    │   └── (mas)
    │
    ├── scripts/
    │   ├── rename_to_samu_ia.py
    │   ├── fix_buildsmart_texts.py
    │   ├── restore_emojis.py
    │   └── (mas de utilidades)
    │
    └── data/
        ├── usuario_actual.txt
        ├── webs_generadas/
        └── webs_imagenes/cache/

================================================================================
## 📋 HISTORIAL DE CAMBIOS
================================================================================

### 2026-09-18 - Plan de modularizacion aprobado
- Acordado modularizar panel_dueno.py (FASE 0)
- Registradas 6 reglas nuevas de codigo (ver seccion REGLAS)
- Registrado pendiente: modularizar panel_base.py (protegido orquestador)
- Registrado pendiente: refactor salud.py config-driven
- Registrado pendiente: cuotas detalladas de APIs (post-Stripe)
- Regla clave: ningun archivo pasa de 400 lineas

### 2026-09-18 - Modulo 11 (Salud del sistema) COMPLETADO
- utils/salud.py V2 - Bootstrap de path para standalone
- 6 checks: Supabase, Netlify, Groq, OpenRouter, Gemini, Backend
- panel_dueno.py V3.1 con tab Salud integrada
- Todos los servicios reportan estado real + latencia

### 2026-09-18 - Modulo 8 (Republicar web) COMPLETADO
- panel_dueno.py V3.0
- Boton Republicar en tab Clientes, tab Webs y detalle cliente
- Reutiliza utils.web_publisher.publicar_web()
- Registra evento republicar_web en eventos_app

### 2026-09-18 - Modulo 6 (Suspender/Reactivar) COMPLETADO
- Tabla usuarios_sistema en Supabase
- panel_dueno.py V2.9
- KPI Suspendidos en tab Panel
- Botones suspender/reactivar con motivo en tab Clientes
- Estado visible en detalle cliente

### 2026-09-17 - Modulo 4 (Detalle cliente) COMPLETADO
- panel_dueno.py V2.8 con _plano() para leer data JSON de Supabase
- Vista individual con KPIs, negocios, historial de acciones
- Boton "Ver detalle" en tab Clientes

### 2026-09-17 - Modulo 3 (Filtros de fecha) COMPLETADO
- Selector global con 6 opciones: 7d / 30d / Este mes / Hoy / Todo / Custom
- Aplica a todas las tabs y KPIs

### 2026-09-17 - Modulo 2 (Graficos Plotly) COMPLETADO
- utils/graficos.py V2.0 con dark premium
- 4 graficos: eventos/dia, usuarios nuevos/dia, sectores, webs/semana
- Sin toolbar, paleta moderna

### 2026-09-17 - Modulo 1 (Logging automatico) COMPLETADO
- utils/logger.py V1.0 - fire-and-forget con thread daemon
- 10 puntos de logging en panel_base.py
- eventos_app se llena automaticamente

### 2026-09-17 - Renombrado BuildSmart -> SAMU IA
- Scripts/rename_to_samu_ia.py (14 archivos)
- config_app.py NOMBRE_APP = "SAMU IA"
- URLs protegidas (buildsmart-webs.netlify.app sigue funcionando)

### 2026-09-17 - Panel Dueno V2.2 a V2.4
- 6 tabs: Panel, Clientes, Ingresos, Webs, Registros, Configuracion
- KPIs globales, listas, editor config
- Emojis via constantes ASCII-safe (\U0001F451)

### 2026-09-16 - SQL inicial Panel Dueno
- Tablas: suscripciones, eventos_app, config_global
- Cliente utils/supabase_rest.py V1.0

================================================================================
## 🚨 PENDIENTES REGISTRADOS (NO OLVIDAR)
================================================================================

### P1: Modularizar panel_dueno.py (FASE 0 - AHORA)
- Que falta: separar en panels/dueno/ con 10 archivos
- Por que: archivo actual es 1500 lineas, insostenible
- Cuando: ahora mismo (esta sesion)

### P2: Modularizar panel_base.py (FASE 0.2 - despues de Nivel 2)
- Que falta: separar en panels/base/ con orquestador protegido
- Por que: mismo problema (1200 lineas y creciendo)
- Cuando: despues de completar Nivel 2 (Modulos 5, 7, 9, 10)
- PROTECCION: el orquestador (responder_chat, _ejecutar_intent,
  _obtener_personalidad, construir_contexto_negocio) NO se separa
  - Razon: la efectividad del chat depende de coherencia entre
    intents + contexto + personalidad
  - Plan: modulos perifericos se separan, orquestador queda intacto

### P3: Refactor salud.py config-driven
- Que falta: JSON con servicios, salud.py lee dinamicamente
- Por que: agregar IA nueva requiere editar codigo actualmente
- Cuando: despues de FASE 0 (modularizacion)

### P4: Cuotas detalladas de APIs (post-Stripe)
- Que falta: tracking de gasto, proyeccion de agotamiento, alertas
- Por que: necesita Stripe primero para conocer cuotas reales
- Cuando: despues de integrar Stripe

### P5: Alertas visuales en panel dueno
- Que falta: banner si algun servicio esta caido o cuota alta
- Por que: hoy solo se ve al entrar a tab Salud
- Cuando: despues de FASE 0

### P6: Pulido visual final
- Que falta: emojis rotos residuales, textos truncados, use_container_width
- Por que: cosmetico, no funcional
- Cuando: al final de todo Nivel 1+2

### P7: i18n multi-idioma
- Que falta: utils/i18n.py con diccionarios
- Por que: app sera global, no implementar aun
- Cuando: post-lanzamiento

================================================================================
## ⚠️ COSAS QUE NO HACER
================================================================================

1. NO facturacion electronica por ahora
2. NO prometer funciones que no existen
3. NO inventar datos en respuestas IA
4. NO usar base64 para imagenes
5. NO permitir multiples webs por negocio
6. NO modificar supabase_client.py sin probar
7. NO subir .env a Git
8. NO mezclar los 4 negocios en el codigo
9. NO usar here-strings en PowerShell
10. NO mandar fragmentos de archivo
11. NO mezclar idiomas en lo VISUAL (UI 100% espanol siempre)
12. NO olvidar pulido visual (pase final)
13. NO implementar i18n todavia
14. NO usar scripts fix_encoding genericos
15. NO crear archivos de mas de 400 lineas

================================================================================
## 📌 RECORDATORIOS
================================================================================

- Antes de cada cambio: respaldo con `python auto_sync.py --once`
- Cada archivo enviado debe ser COMPLETO
- Probar cada cambio aislado antes de integrar
- Documentar cada cambio en este archivo
- Idioma codigo: ingles variables, espanol UI
- Regla de oro: no romper nada de lo que ya funciona
- Metodo de archivos: PowerShell + code archivo.py
- App sera multi-idioma (global) → crear utils/i18n.py CUANDO llegue

================================================================================
## 👥 EQUIPO
================================================================================

- Dueno/CEO: Antonio (LENOVO)
- Arquitecto IA: Claude/GPT (asistente)
- Proyecto: SAMU IA (ex BuildSmart Holdings)

================================================================================
## 🔗 URLs Y RECURSOS
================================================================================

- Supabase: https://supabase.com/dashboard/project/gbjsjbiyoyjzodznrjjj
- Netlify: https://buildsmart-webs.netlify.app
- Repo local: C:\Users\LENOVO\Desktop\buildsmart-panel
- Streamlit: http://localhost:8501

================================================================================
## 📖 COMO USAR ESTE ARCHIVO
================================================================================

- Al EMPEZAR sesion nueva: pegar este archivo completo al chat
- Durante sesion: trabajar normal
- Al TERMINAR sesion: actualizar seccion HISTORIAL DE CAMBIOS
- Antes de apagar PC: respaldo + guardar

================================================================================
FIN DEL ARCHIVO
================================================================================
### P-Y: Recomendaciones del reporte de IA (2026-09-22)

Extraidas del analisis profundo. Todas deben considerarse en el roadmap.

RECOMENDACIONES:
- R1 (Alta): Acelerar integracion React Bits
  - Diferenciador visual vs competidores con plantillas genericas
  - Migrar generador a React para integrar 110+ componentes
  - Impacto en percepcion de valor PIME/Enterprise

- R2 (Critica): Fortalecer modulo "Marketing con IA"
  - Debe ser punta de lanza del plan USD 99/mes
  - Si el cliente genera investigacion de mercado con IA, justifica el precio
  - Ya existe market_research.py, integrarlo al flujo del cliente

- R3 (Critica): Optimizar embudo WEB -> PIME
  - Plan WEB Gancho con limites claros (solo web, sin CRM/inventario)
  - Al intentar usar CRM/inventario, sugerir upgrade a PIME no intrusivo
  - WEB + CRM debe ser competitivo para reducir friccion

- R4 (Alta): Enfatizar seguridad y roles de Staff en marketing
  - Destacar: delegar tareas sin exponer caja ni configuracion
  - Clave para PYMES 5-20 empleados formalizando procesos

- R5 (Media): Preparar escalabilidad de Sucursales
  - Disenar jerarquia multi-tenant desde ahora en Supabase
  - Un cliente con 3 sucursales = 4.5 clientes PIME de ingreso

- R6 (Alta): Documentar el comando [EJECUTAR]
  - Guias de usuario + demos en video
  - Es el diferenciador mas fuerte, debe ser visible en ventas

PROXIMOS PASOS (del reporte):
- P1 (Bloqueante): Completar Login real (Supabase Auth) + Stripe
- P2 (Bloqueante): Lanzar Landing publica 3+1 opciones
- P3 (Critica): Desarrollar CRM completo (corazon de retencion)
- P4 (Alta): Integracion codigos de barras (deal-breaker retail/alimentos)
- P5 (Critica): Piloto con 10 clientes reales - validar TTV < 15 min
- P6 (Alta): Documentar el Analisis Profundo (demo de ventas)

INSIGHT CRITICO:
"Sin un CRM funcional, el cliente no vera valor en el plan PIME a mediano plazo."
El CRM paso de modulo pendiente a prioridad #1 despues de Login+Stripe+Landing.

ORDEN REVISADO SEGUN EL REPORTE:
1. Landing 3+1        (bloqueante)
2. Login (Auth)       (bloqueante)
3. Stripe             (bloqueante)
4. CRM completo       (retencion critica)
5. Codigos de barras  (deal-breaker retail)
6. Piloto 10 clientes (validacion)
### P-Z: Segundas recomendaciones del reporte IA (2026-09-22)

Nuevas recomendaciones del segundo analisis (con contexto completo):

R7 (Alta): Limitar "Ejecuciones Profundas" por plan
  - Si el costo de IA sube, limitar numero de analisis profundos mensuales
  - PIME: X ejecuciones/mes (a definir)
  - Enterprise: ilimitadas
  - Prevenir abuso del analisis profundo

R8 (Media): Validar los 66 sectores con beta usuarios en Colombia
  - Ajustar prompts de IA especificos por sector
  - Contabilidad para Servicios difiere de Retail

R9 (Alta): Marketing con casos reales
  - Casos: "panaderia en Bogota usa SAMU IA para inventario"
  - Comparacion directa: "Deja de pagar el 20% de Polsia"
  - Ejemplos especificos > genericos

R10 (Alta): Estrategia de contenido basada en TTV
  - Eslogan: "Tu negocio digitalizado en 15 minutos"
  - Central en la landing publica

ROADMAP RECOMENDADO (del reporte):
- Semana 1-2: Supabase Auth + Stripe + CRM UI
- Semana 3-4: Beta privado con 10-20 PYMES
- Mes 2: Landing publica + marketing
- Mes 3: Lanzamiento + QR + React migration prep

RIESGOS IDENTIFICADOS:
- Capacidad de soporte (fundador unico = cuello de botella)
- Complejidad contable (adaptacion DIAN Colombia + LATAM)
- Adopcion IA (usuarios deben confiar - mostrar contexto leido)

INSIGHT CRITICO:
"El break-even bajo (22 clientes) da margen de seguridad
 para iterar durante los primeros 6 meses."

### P-WEB: Decisiones de precios para producto WEB (2026-09-22)

Basado en estudio tecnico de IA. Precios finales aprobados:

TIERS WEB:
- Tier 1: Web Basica - USD 149 (antes $199)
  Incluye: web + hosting 1 año + subdominio SAMU IA
- Tier 2: Web + CRM - USD 299 (antes $249)
  Incluye: todo T1 + CRM captura + mini-panel
- Tier 3: Web Premium - USD 499
  Incluye: todo T2 + dominio propio + CRM completo + logo custom + soporte prioritario

RENOVACION ANUAL:
- T1/T2: USD 59/año
- T3: USD 79/año (incluye dominio)

VALORES EN config_global:
- web_precio_tier1 = 149
- web_precio_tier2 = 299
- web_precio_tier3 = 499
- web_renovacion_tier1_2 = 59
- web_renovacion_tier3 = 79

ANALISIS DEL ESTUDIO:
- Margen bruto: 83-90% por venta
- CAC objetivo: < USD 150
- Break-even: 10 ventas/mes mixtas
- Renovacion clave para sostenibilidad

FLUJO DE COMPRA:
- Compra -> formulario -> pago Stripe -> generacion -> entrega por email
- URL: subdominio SAMU IA (T1/T2) o dominio propio (T3)
- Post-pago: acceso a mini-panel para ver leads (T2/T3)

EMBUDO DE UPSELL:
- T1 -> T2: +USD 150 (cuando recibe leads)
- T2 -> T3: +USD 200 (cuando quiere dominio/logo)
- WEB -> PIME: $99/mes (cuando necesita ERP completo)

ESTRATEGIA DE PRECIOS APROBADA.
### P-WEB-DIRECTOR-ARTE: Integracion Director de Arte (2026-09-22)

Cambio importante en la generacion de webs. Se inyecto un system prompt
de "Director de Arte" al inicio del prompt de generacion.

Archivos modificados:
- utils/web_prompts_data.py (NUEVO, 228 lineas)
  - PALABRAS_PROHIBIDAS (41 frases)
  - DIRECTOR_DE_ARTE_PROMPT (1441 chars)
  - REGLAS_CSS_PREMIUM, REGLAS_CODIGO, REGLAS_IMAGENES, REGLAS_SALIDA
  - construir_reglas_contenido()

- utils/web_prompts.py V5.0 (285 lineas, antes 383)
  - Importa de web_prompts_data
  - Director de Arte integrado en generar_prompt_web()
  - Bootstrap de path para standalone
  - Backup: web_prompts_backup_YYYYMMDD.py

Motivo:
- Mejorar calidad premium automatica de TODAS las webs generadas
- Diferenciacion de estilo por tipo de cliente (creativo/lujo vs tecnico/corporativo)
- Cumplir regla: maximo 400 lineas por archivo

El Director de Arte incluye:
- Proceso de trabajo (analizar brief, detectar tipo de cliente)
- Estandares obligatorios (tipografia, espaciado, jerarquia, hover, animaciones)
- Diferenciacion de estilo segun cliente
- Scroll-driven animations + prefers-reduced-motion

Estado: IMPLEMENTADO. Pendiente PROBAR con generacion real.

Notas:
- El prompt original decia "Breve justificacion del enfoque (2-4 lineas)"
  pero fue removido para no romper el parser que espera SOLO HTML.
  ### P-PAGOS: Pasarelas de pago - Analisis y decision (2026-09-22)

CONTEXTO:
Necesitamos procesar pagos para Web Gancho ($149/$299/$499)
y suscripciones PIME ($99/mes).

ANALISIS DE OPCIONES:

Stripe (originalmente planeado):
- ESTADO: NO DISPONIBLE para Colombia
- Razon: Stripe no permite crear cuentas con direccion colombiana
- Alternativa: Crear LLC en USA (4-6 semanas, cientos de USD)
- DEScartado por ahora (complejidad + costo)

Wompi (Bancolombia):
- ESTADO: Bloqueado por cuenta bancaria
- Ventaja: Acepta tarjetas + PSE + Nequi + Daviplata
- Soporta suscripciones recurrentes
- REQUISITO: Cuenta de ahorros/corriente Bancolombia con 30+ dias
- El dueno NO tiene esa cuenta actualmente
- DEScartado hasta obtener la cuenta

ALTERNATIVAS A EVALUAR:

1. ePayco (Colombia)
   - Acepta tarjetas + PSE + efectivo
   - No requiere cuenta especifica de banco
   - Popular en SaaS colombianos
   - PRIORIDAD: ALTA

2. Mercado Pago (Colombia)
   - Acepta tarjetas + PSE
   - Facil integracion
   - Cobros recurrentes disponibles
   - PRIORIDAD: MEDIA

3. PayU Latam
   - Acepta tarjetas + PSE + efectivo
   - Mas enterprise
   - PRIORIDAD: BAJA (mas complejo)

4. PayPal
   - Funciona en Colombia
   - Cobros internacionales
   - PRIORIDAD: BAJA (no es popular en PYMEs LATAM)

DECISION ESTRATEGICA:

1. NO bloquear el desarrollo por el gateway
2. Construir TODO el flujo de Web Gancho con un "adaptador de pagos"
3. El adaptador puede conectarse a: Wompi, ePayco, Mercado Pago, Stripe
4. Modo "manual" para testing: el dueno marca pedidos como pagados
5. Cuando el dueno obtenga cuenta bancaria → conectar gateway real

PROXIMA ACCION:
- Investigar ePayco como opcion primaria
- Requisitos de ePayco para Colombia
- Si requiere cuenta bancaria especifica, evaluar Mercado Pago
### P-WEB-CRM: CRM + Paneles de Web Gancho (2026-09-22)

Faltante para terminar Web Gancho:

BLOQUES PENDIENTES:
- G5: Adaptador de pagos (modo manual por ahora)
- G6: Formulario post-pago
- G7: Generacion + publicacion automatica
- G8: Email de entrega
- G9: Mini-panel del cliente (2h)
- G10: Panel del dueno con tab "Pedidos Web" (1.5h)
- G11: CRM de leads funcional - conectar formulario a DB (1h)
- G12: Magic link login cliente (1.5h)

TOTAL: ~10h

LOS 3 NIVELES DE CRM + PANEL:

1. CRM del cliente (Web Gancho)
   - Quien ve: cliente que compro Tier 2 o 3
   - Que ve: leads capturados, estado, notas
   - Donde vive: tabla crm_leads (ya creada)

2. Panel del cliente
   - Quien ve: cliente que compro cualquier tier
   - Que ve: su web, estado, modificar, sus leads, renovacion
   - Donde vive: URL tipo samu-ia.com/cliente/mi-negocio

3. Panel del dueno
   - Quien ve: dueno (Antonio)
   - Que ve: TODOS los pedidos, estado, ver web + datos, marcar pagado
   - Donde vive: tab nueva en panel dueno

NOTA CRITICA:
El CRM tiene tabla crm_leads creada, pero falta el endpoint
que conecta el formulario HTML de la web con esa tabla.
Hoy el formulario solo envia email. Debe guardar en DB.

ORDEN RECOMENDADO:
1. G5 (adaptador manual) - desbloquea todo
2. G6 (formulario post-pago) - captura datos
3. G7 (generacion automatica) - crea la web
4. G8 (email entrega) - cierra el flujo
5. G10 (panel dueno) - vos controlas
6. G9 (mini-panel cliente) - cliente ve su web
7. G11 (CRM funcional) - captura leads
8. G12 (magic link) - login cliente
### P-WEB-CHECKOUT: Flujo Checkout + Panel Pedidos (2026-09-22)

BLOQUES COMPLETADOS:

G5: Adaptador de pagos + Checkout
- panels/web/pagos/__init__.py (100 lineas) - Router de proveedores
- panels/web/pagos/base.py (77 lineas) - Interfaz abstracta
- panels/web/pagos/manual.py (94 lineas) - Proveedor manual
- panels/web/checkout.py (278 lineas) - Formulario + instrucciones
- panels/web/__init__.py V2.0 - Router con subruta checkout
- panels/web/landing.py V4.0 - Boton "Comprar" lleva al checkout

G10: Panel del dueno - Pedidos Web
- panels/dueno/tab_pedidos_web.py (303 lineas) - Tab nuevo
- panels/dueno/__init__.py V6.0 - 12 tabs, filtrado por rol
- utils/staff.py V2.0 - Agrega permisos pedidos_web.ver/gestionar

DATOS DE PAGO EN config_global:
- pago_proveedor = "manual"
- pago_nequi = "300 123 4567" (placeholder - editar)
- pago_daviplata = "300 123 4567" (placeholder - editar)
- pago_bancolombia_ahorros = "000-000000-00" (placeholder - editar)
- pago_titular = "Antonio Porras" (placeholder)
- pago_email_comprobante = "pagos@samu-ia.com" (placeholder)

PERMISOS STAFF V2.0:
- admin: 13 permisos (todos excepto config y staff)
- soporte: 6 permisos (ver clientes + pedidos + suspender)
- marketing: 5 permisos (metricas + auditoria)

FLUJO COMPLETO FUNCIONANDO:
1. Cliente entra a landing: ?web=landing
2. Click "Comprar" en cualquier tier
3. Aparece formulario (datos personales + negocio)
4. Click "Confirmar compra" -> crea pedido en pedidos_web
5. Cliente ve instrucciones de pago (Nequi/Daviplata/email)
6. Dueno entra a tab "Pedidos Web" en panel
7. Click "Marcar como PAGADO" -> estado cambia
8. KPIs y filtros se actualizan
9. Botones cambian a "Generar web ahora" + "Marcar como ENTREGADO"

PENDIENTE (proximos bloques):
- G6: Formulario post-pago (ya integrado, probar en local)
- G7: Generacion automatica al marcar pagado (boton actual es placeholder)
- G8: Email de entrega al cliente
- G9: Mini-panel del cliente Web
- G11: CRM de leads funcional
- G12: Magic link login cliente
### P-WEB-EMAIL: Email automatico con Resend (2026-09-23)

BLOQUE G8 COMPLETADO:

Archivos:
- utils/email_pedidos.py (177 lineas, NUEVO)
  - Template de entrega (URL + resumen + renovacion)
  - Template de rechazo
  - enviar_email_entrega(pedido)
  - enviar_email_rechazo(pedido, motivo)

- utils/email_sender.py V2.0 (REESCRITO)
  - Resend como motor principal
  - SMTP como fallback legacy
  - Clase EmailSender con .enviar_correo()
  - Propiedades: .disponible, .motor_activo

- panels/dueno/pedidos_web_acciones.py V2.0
  - Al terminar generacion, envia email automatico
  - Log de email_entrega_enviado en eventos_app

Configuracion .env:
- RESEND_API_KEY=re_xxxxx
- RESEND_FROM_EMAIL=onboarding@resend.dev
- RESEND_FROM_NAME=SAMU IA

Flujo:
1. Dueno clickea "Generar web ahora"
2. Web se genera con IA
3. Se publica en Netlify
4. Pedido pasa a "entregado"
5. Email automatico al cliente con URL publica

Test realizado 2026-09-23:
- Email recibido en antonioempresarial9@gmail.com
- From: SAMU IA <onboarding@resend.dev>
- Subject: "Test SAMU IA"
- Body correcto

PROXIMOS PASOS:
- G9: Mini-panel del cliente (2h)
- G11: CRM de leads funcional (1h)
- G12: Magic link login cliente (1.5h)

NOTAS:
- Resend permite 3000 emails/mes gratis
- Dominio personalizado (onboarding@samu-ia.com) requiere verificar dominio en Resend
- Por ahora usa onboarding@resend.dev (oficial de Resend)
### P-WEB-PANEL-CLIENTE: Mini-panel del cliente (2026-09-23)

BLOQUE G9 COMPLETADO:

Archivos:
- utils/magic_link.py (NUEVO)
  - Generacion de tokens (64 chars hex)
  - Validacion con expiracion (30 dias)
  - construir_url_panel() para armar la URL

- panels/web/panel_cliente.py (394 lineas, NUEVO)
  - _renderizar_login() - pantalla si no hay token
  - _renderizar_panel() - panel principal
  - _renderizar_leads() - lista de leads del CRM
  - _renderizar_lead() - lead individual con botones
  - Soporta tokens validos/invalidos/expirados

- panels/web/__init__.py V3.0
  - Router con subruta "panel"

- panels/web/checkout.py V2.0
  - Genera magic token al crear pedido
  - Envia email #1 con link al panel

- utils/email_pedidos.py V2.0
  - Template de entrega incluye link del panel
  - _seccion_panel() agrega la URL con token

SQL aplicado:
- ALTER TABLE pedidos_web ADD COLUMN magic_token TEXT
- ALTER TABLE pedidos_web ADD COLUMN magic_token_expira TIMESTAMPTZ
- INDEX idx_pedidos_web_token

URL de acceso:
- Cliente: http://localhost:8501/?web=panel&token=XXX
- Token real: 64 chars hex, unico por pedido

Funcionalidades del panel del cliente:
- Ver estado del pedido (pendiente/pagado/entregado)
- Ver URL publica de la web cuando este lista
- Abrir la web en nueva pestana
- Ver info del negocio
- Ver fecha de compra y datos del pedido
- Ver info de renovacion (1 año gratis)
- Ver leads capturados (Tier 2/3)
- Marcar leads como contactado/cerrado/perdido

Estado verificado 2026-09-23:
- Token valido → panel funciona
- Token invalido → "Acceso denegado"
- URL publica: buildsmart-webs.netlify.app/pedido_XXX/YYY
- Botones funcionales

Pendiente de este modulo:
- G11: CRM de leads funcional (conectar formulario de la web generada)
- G12: Reenvio automatico de magic link por email (opcional)

Notas:
- Existe 1 pedido corrupto en DB (63a620c5): entregado pero sin web_url
- Fue por marcar ENTREGADO manualmente sin generar la web
- No es bug del codigo, fue test manual
- Limpiar en proximo reset de DB
### P-GATEWAY-FIX: Modelos IA actualizados (2026-09-24)

BLOQUE CRITICO COMPLETADO:

Problema detectado:
- Groq intentaba modelos viejos: qwen3.6-27b (404) y qwen3.8-27b (rate limited)
- La generacion de webs fallaba con "No se pudo generar HTML valido"
- Los 3 intentos fallaban consecutivamente

Fix aplicado en backend/gateway.py V8.2:

MODELOS_GROQ actualizados:
- Antes: qwen/qwen3.6-27b + qwen/qwen3.8-27b (2 modelos rotos)
- Ahora: openai/gpt-oss-120b + openai/gpt-oss-20b + qwen/qwen3.8-27b

MODELOS_GEMINI actualizados:
- Antes: gemini-3.1-flash-lite (no existe)
- Ahora: gemini-2.0-flash-exp + gemini-1.5-flash

MODELOS_OPENROUTER sin cambios:
- nvidia/nemotron-3-super-120b-a12b:free
- deepseek/deepseek-chat-v3.1:free
- meta-llama/llama-3.3-70b-instruct:free
- qwen/qwen-2.5-72b-instruct:free

Cambios tecnicos:
- Sin mojibake en comentarios
- Codigo ASCII-safe
- Backup: backend/gateway_v81_backup_YYYYMMDD_HHMMSS.py

Test realizado 2026-09-24:
- chat_rapido: OK via groq (gpt-oss-120b)
- chat_inteligente: OK via groq (gpt-oss-120b)
- Respuesta en menos de 15s

Impacto:
- Generacion de webs vuelve a funcionar
- Analisis profundo mas rapido
- Chat del usuario mas rapido
- Cascada IA robusta (4 proveedores)

Nota:
- El cascade prioriza Groq (mas rapido) → OpenRouter → Gemini → Ollama
- Si Groq cae, sigue funcionando con los otros 3
### 2026-09-25 - MVP WEBS FUNCIONANDO 🎉

ESTADO FINAL DEL BLOQUE WEBS:

**Netlify (proveedor principal):**
- Cuenta: samuellesmes (samupor527@gmail.com)
- Sitio: buildsmart-samu.netlify.app (PUBLICO)
- Token: NETLIFY_TOKEN (nfp_pbicKQcT...)
- Site ID: c55778ca-6aee-4fb8-ac43-3ea0c1835a64
- Cuota: 300 deploys/mes
- Usados: 2

**Cloudflare (proveedor fallback - DESHABILITADO):**
- Token: cfut_wEPGX5u... (valido)
- Proyecto: buildsmart-webs
- Cuota: 500 deploys/mes
- BUG: error 8000006 en deployments (API)
- Hash BLAKE3 correcto (len=32)
- Flujo Direct Upload completo implementado (V5.0)
- Bloqueado hasta que Cloudflare arregle el bug

**Provider Manager V1.1:**
- PROVIDERS_DESHABILITADOS = ["cloudflare"]
- Selecciona automaticamente por cuota restante
- Failover automatico si el principal falla
- Tracking en data/provider_usage.json

**Limpieza de codigo:**
- 28 backups de utils/ movidos a _backups/
- 17 backups de panels/ movidos a _backups/
- config/utils/ (duplicado legacy) movido a _backups/
- Utils ahora: 46 archivos .py limpios
- Panels ahora: 7 archivos .py limpios

**Auditoria de consumo:**
- 5 llamadas reales a publicar_web() (controlado)
- Cero loops
- Publicacion va DIRECTO a Netlify sin intentar Cloudflare

**Flujo verificado end-to-end:**
1. IA genera HTML (Groq) → 1 token IA
2. Guarda en disco local → $0
3. Guarda metadata en Supabase → $0
4. ProviderManager selecciona Netlify → $0
5. Netlify publica → 1 credito
6. Web publica: https://buildsmart-samu.netlify.app/{usuario}/{web}/

**G11 CERRADO:**
- Formulario en la web guarda lead en crm_leads
- Mensaje verde confirmado en navegador
- 2 leads en DB (test)

**PENDIENTES:**
- Arreglar error Cloudflare 8000006 (bug API)
- Cuando se arregle: quitar "cloudflare" de PROVIDERS_DESHABILITADOS
- Actualizar provider_manager para sitios nuevos nacidos publicos
- Landing 3+1 opciones
- Login diferenciado por plan
- Stripe/Wompi



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


### 2026-09-25 - Fase 1 Bloque 1 completado

**Checkout V4.3 sin st.form:**
- Sacado st.form, usa st.container implicito
- Razon: st.form NO permite labels dinamicos
- Fix: rerun en cada cambio de pais -> prefijo WhatsApp dinamico
- Pais dropdown con 29 paises globales (LATAM primero)
- utils/paises.py NUEVO con prefijos internacionales

**Pendiente critico (para fase cloud):**
- Streamlit NO escala bien a produccion multi-usuario
- Cada rerun consume CPU del server
- Migracion sugerida: FastAPI + React, o Streamlit Cloud + tuning
- Anotado para fase post-lanzamiento (no bloquea MVP)

**Regla 400 lineas:**
- checkout.py crecio a ~625 lineas
- Se dividira en 3 archivos:
  - checkout_validators.py (~120 lineas)
  - checkout_data.py (~200 lineas)
  - checkout.py (~320 lineas)



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

