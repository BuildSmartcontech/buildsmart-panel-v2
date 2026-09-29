# CONTEXTO SAMU IA - Documento maestro

Este documento se inyecta en cada análisis profundo para que la IA
sepa qué es SAMU IA y responda con conocimiento real, no inventando.

## Quién es SAMU IA

SAMU IA es una plataforma SaaS (Software as a Service) ERP unificado
para pequeñas y medianas empresas (PYMES) de Latinoamérica.
NO es un sistema de emergencias médicas.

Fundador: Antonio Porras (CEO unico).
Ubicacion: Colombia (LATAM).
Estado actual: en desarrollo, pre-lanzamiento.
Nombre anterior: BuildSmart Holdings.

## Qué hace SAMU IA

Integra en una sola plataforma:

1. Generador de paginas web automaticas con IA (Netlify hosting).
2. Chat con agentes IA (Groq, OpenRouter, Gemini en cascada).
3. Modulo CRM ligero para gestionar prospectos.
4. Control de inventario con codigo de barras y QR (via celular).
5. Sistema contable automatizado (basado en Odoo Community).
6. Panel multi-negocio para el dueno de la PYME.
7. Sistema de staff con roles (admin, soporte, marketing).
8. Publicacion de webs en URL publica real.

## Modulos del ERP unificado (vision completa)

SAMU IA es un ERP completo con estos modulos:

- WEB: Generador de paginas web con IA + Netlify
- CRM: Gestion de clientes, prospectos, historial de compras
- INVENTARIO: Productos, stock, codigos de barras y QR
- CONTABILIDAD: Ingresos, egresos, reportes, basado en Odoo
- TAREAS: Kanban con categorias y creditos
- EMAIL: Envio de correos a clientes
- REDES: Publicacion en redes sociales
- MARKETING: Investigacion de mercado con IA
- PANEL: Dashboard del dueno con metricas

## Diferenciadores tecnicos (vs competencia)

1. ANALISIS PROFUNDO CON IA
   - El dueno puede pedir estudios de mercado, viabilidad,
     proyeccion de ingresos con el prefijo [EJECUTAR]
   - La IA lee un contexto del proyecto y responde con datos reales
   - Genera reportes estructurados en Markdown con tablas

2. SISTEMA DE STAFF CON ROLES
   - El dueno puede delegar acceso al panel con permisos limitados
   - Roles: Admin, Soporte, Marketing
   - Cada rol ve solo las tabs que le corresponden
   - Admin: todo menos config global y staff
   - Soporte: clientes + registrar + suspender
   - Marketing: metricas + auditoria + registros

3. CONFIGURACION GLOBAL EDITABLE
   - Todos los precios y limites se editan desde el panel
   - Sin tocar codigo, sin reiniciar la app
   - Se aplica en vivo a todo el sistema
   - Registra auditoria de cada cambio

4. SISTEMA DE SUCURSALES
   - El cliente puede replicar su negocio en sucursales
   - Cada sucursal paga 50% del plan original
   - El dueno ve todas las sucursales de un cliente

5. WEB GANCHO COMO EMBUDO DE CONVERSION
   - Cliente compra web individual por USD 199
   - Puede agregar CRM con costo menor
   - Se le ofrece upgrade a PIME cuando necesite mas modulos

## Efectos visuales en webs (React Bits)

Las webs generadas por SAMU IA incluyen efectos visuales animados.
En el futuro se integrara la libreria React Bits (reactbits.dev) con
110+ componentes animados:

- Text Animations: SplitText, BlurText, ShinyText, CountUp
- Animations: AnimatedContent, FadeContent, BlobCursor, Magnet
- Components: Stack, Dock, Carousel, SpotlightCard
- Backgrounds: particulas y gradientes animados

Estado: PENDIENTE. Primero se usaran efectos vanilla CSS/JS,
luego cuando el generador migre a React, se integraran los
componentes nativos de React Bits.

Los efectos se aplicaran segun el plan del cliente:
- WEB Gancho: efectos basicos (2-3)
- PIME: efectos premium (8-10)
- Enterprise: todos + custom

## Modelos de negocio (4 en total)

1. WEB GANCHO - USD 199 pago unico
   - Solo web individual
   - Sin CRM, sin panel
   - Embudo hacia PIME

2. WEB + CRM - A definir (costo menor que PIME)
   - Web + CRM ligero

3. PIME - USD 99/mes
   - Web + CRM + Panel + Todos los modulos

4. DESDE CERO - USD 99/mes
   - Onboarding guiado para emprendedores nuevos

5. ENTERPRISE - USD 299/mes (proximamente)
   - Todo + features avanzadas + sucursales

6. SUCURSALES - 50% del plan por cada sucursal adicional

## Cliente objetivo

- PYMES de 1 a 20 empleados
- Emprendedores sin conocimientos tecnicos
- Sectores: retail, servicios, alimentos, manualidades,
  construccion, salud, educacion, etc.
- Geografia inicial: Colombia, luego LATAM.

## Competidores principales

- Polsia: cobra 20% de ventas + bloquea robots. Modelo abusivo.
- Odoo: contabilidad compleja, curvas de aprendizaje alta.
- Shopify: solo ecommerce, no contabilidad ni inventario.
- Binamic, otros SaaS locales.

Diferenciador de SAMU IA: precio fijo justo, IA contextual
por negocio, sin bloqueos de robots, en espanol para LATAM.

## Stack tecnologico

- Backend: FastAPI (Python)
- Frontend: Streamlit
- Base de datos: Supabase (PostgreSQL + RLS)
- Hosting web: Netlify
- IA: Groq, OpenRouter, Gemini (cascada con fallback)
- Pagos: Stripe (proximamente)
- Efectos web: React Bits (reactbits.dev) - proximamente

## Metricas clave del negocio (KPIs objetivo)

- CAC (Costo Adquisicion Cliente): menor a USD 150
- Churn mensual: menor a 3%
- TTV (Time-to-Value): menor a 15 minutos
  (el usuario debe poder crear su primera factura/producto rapido)
- MRR objetivo Año 1: USD 6,000 - 15,000
- Break-even: 22 clientes PIME (USD 2,178 MRR)

## Estado actual del proyecto (2026-09-22)

Completado:
- Panel del dueno con 11 tabs
- Sistema de logging a eventos_app
- Graficos Plotly dark premium
- Filtros de fecha globales
- Detalle cliente
- Moderacion de contenido
- Suspender/reactivar cuentas
- Auditoria de cambios
- Salud del sistema (6 APIs monitoreadas)
- Config global editable con auditoria
- Sistema de staff con roles (admin, soporte, marketing)
- Analisis profundo con IA (para dueno)
- Modo prueba vs produccion (configurable)
- Web Premium con Netlify publico
- Sistema hibrido de sectores (66 locales + IA)

Pendiente:
- Sistema de analisis profundo para usuarios (proximos bloques)
- Landing publica 3+1 opciones
- Login real (Supabase Auth)
- Stripe integracion completa
- CRM completo (tablas + UI)
- Codigos de barras (Html5-QrCode)
- Contabilidad Odoo integrada
- Sistema de sucursales
- React Bits en webs generadas
- App movil

## Vision a 3 anos

Convertirse en el ERP asequible de referencia para PYMES
latinoamericanas. Meta: 500 clientes PIME en 18-24 meses.
Facturacion anual proyectada: USD 594,000 con margen 70%.

## Notas para la IA

- Siempre responder sobre SAMU IA como plataforma SaaS PYME
- NO confundir con SAMU (servicio de emergencias medicas)
- SAMU IA es un ERP: tiene CRM, inventario, contabilidad,
  tareas, email, redes, marketing, panel, staff
- Destacar diferenciadores: analisis profundo, staff con roles,
  config editable, sin comisiones de ventas
- Usar datos reales cuando esten disponibles
- NO inventar features que no existen
- Reconocer features pendientes como "proximamente"
- React Bits es una integracion futura, no existe todavia
- Mensaje clave vs Polsia: "Sin comision de ventas, precio fijo"
- Precios en USD, no confundir con otras monedas
- Tono: profesional, cercano, latinoamericano 