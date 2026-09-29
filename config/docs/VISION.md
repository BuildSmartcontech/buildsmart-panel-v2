\# 🎯 BUILD SMART - VISIÓN Y ARQUITECTURA MAESTRA



> \*\*Última actualización:\*\* 2026-09-11

> \*\*Versión del proyecto:\*\* MVP en construcción (Fases 1-12 completadas)

> \*\*Próximo hito:\*\* FASE A - Autenticación



\---



\## 🌟 VISIÓN GENERAL



BuildSmart es una \*\*plataforma SaaS multi-producto\*\* que permite a personas y empresas:



1\. \*\*Crear páginas web profesionales con IA\*\* (producto estrella)

2\. \*\*Automatizar su negocio\*\* (email, redes sociales, investigación)

3\. \*\*Usar agentes IA\*\* para ejecutar tareas complejas

4\. \*\*Gestionar múltiples negocios\*\* desde un solo panel



\*\*Meta 2027:\*\* 10,000+ usuarios activos en LATAM + España + USA.



\---



\## 🎯 MODELO DE NEGOCIO



\*\*Tipo:\*\* Híbrido (individuales + empresas)



| Tipo de usuario | Qué quiere | Cómo se cobra |

|-----------------|-----------|---------------|

| \*\*Persona individual\*\* | Su web personal o de su negocio | Pago único por web + plan premium |

| \*\*Pequeño negocio\*\* | Web + automatización | Suscripción mensual |

| \*\*Empresa\*\* | Múltiples webs + multi-usuario | Licencia por empresa |



\*\*Producto estrella:\*\* Venta de creación de páginas web.



\---



\## 🏗️ PRODUCTOS DE LA PLATAFORMA



\### 📄 Producto 1: Páginas Web (foco comercial)

\- Generación con IA

\- Edición con IA

\- Publicación (local + Netlify futuro)

\- Expiración (30 días gratis, después premium)

\- Descarga (.zip)



\### 📧 Producto 2: Automatización

\- Email marketing

\- Redes sociales

\- Investigación de mercado

\- Scheduler de tareas



\### 🤖 Producto 3: Agentes IA

\- Orquestador LangGraph

\- Chat conversacional

\- Ejecución de tareas



\### 🏢 Producto 4: Panel Empresarial (futuro)

\- Multi-usuario

\- Roles y permisos

\- Reportes

\- API pública



\---



\## 📊 ESTADO ACTUAL DEL PROYECTO



\### ✅ COMPLETADO (12 FASES)



| Fase | Componente | Estado |

|------|-----------|--------|

| 1 | `config/web\_config.py` | ✅ |

| 2 | `web\_prompts`, `web\_templates`, `web\_validator` | ✅ |

| 3 | `web\_generator.py` | ✅ |

| 4 | `web\_storage.py` | ✅ |

| 5 | `web\_expiration.py` | ✅ |

| 6 | `web\_downloader.py` | ✅ |

| 7 | `web\_editor.py` | ✅ |

| 8 | `web\_publisher.py` | ✅ |

| 9 | `web\_module.py` (interfaz única) | ✅ |

| 10 | `backend/gateway.py` (max\_tokens 8000) | ✅ |

| 11 | `app.py` (integración) | ✅ |

| 12 | `backend/main.py` (rutas webs) | ✅ |



\### 🔄 PENDIENTE (Roadmap Comercial)



| Fase | Componente | Prioridad | Tiempo |

|------|-----------|-----------|--------|

| \*\*A\*\* | Autenticación (login/registro) | 🔴 CRÍTICA | 1.5-2 sem |

| \*\*B\*\* | Multi-tenant (empresas) | 🟡 ALTA | 2 sem |

| \*\*C\*\* | Panel admin | 🟡 MEDIA | 1-2 sem |

| \*\*D\*\* | API pública + Webhooks | 🟢 BAJA | 1-2 sem |

| \*\*E\*\* | Marketplace / White-label | 🟢 FUTURA | 3-4 sem |



\---



\## 🎯 ROADMAP POR HITOS



\### 🎯 HOY → 2 SEMANAS: MVP COMERCIAL



\*\*Objetivo:\*\* Login + creación de webs funcionando para 5-10 usuarios.



\- ✅ \*\*FASE A:\*\* Autenticación (login, registro, JWT)

\- ✅ \*\*FASE 2:\*\* Panel de webs mejorado

\- ✅ \*\*FASE 3:\*\* Pasarela de pagos (Stripe/MercadoPago)

\- ✅ \*\*FASE 4:\*\* Despliegue en Hugging Face Spaces



\*\*Resultado:\*\* BuildSmart listo para los primeros 10 clientes.



\### 🎯 SEMANA 3-6: ESTABILIZACIÓN



\*\*Objetivo:\*\* 50-100 usuarios usándolo sin problemas.



\- ✅ Mejorar UI/UX

\- ✅ Sistema de créditos

\- ✅ Historial de webs

\- ✅ Analytics básicos



\### 🎯 MES 2-3: MULTI-TENANT



\*\*Objetivo:\*\* Empresas pueden comprar licencias.



\- ✅ \*\*FASE B:\*\* Multi-empresa

\- ✅ \*\*FASE C:\*\* Panel admin

\- ✅ Facturación por empresa

\- ✅ Roles y permisos



\### 🎯 MES 4-6: ESCALADO



\*\*Objetivo:\*\* 1,000+ usuarios activos.



\- ✅ Migración Streamlit → React (si necesario)

\- ✅ Supabase Free → Pro

\- ✅ CDN para webs publicadas

\- ✅ API pública + Webhooks



\---



\## 📐 PRINCIPIOS ARQUITECTÓNICOS



| Principio | Aplicación |

|-----------|-----------|

| \*\*Modularidad\*\* | Cada producto es un módulo independiente |

| \*\*Multi-tenant desde el día 1\*\* | Aunque no se use aún, la estructura lo soporta |

| \*\*Aislamiento de datos\*\* | RLS garantiza que cada usuario ve solo lo suyo |

| \*\*API first\*\* | Todo se puede llamar por API (futuro) |

| \*\*Feature flags\*\* | Activar/desactivar módulos por usuario |

| \*\*Límites por plan\*\* | Cada plan tiene sus límites |

| \*\*No romper lo construido\*\* | Cada fase se suma, nunca se reemplaza |



\---



\## 🗄️ BASE DE DATOS



\### Tablas existentes



| Tabla | Propósito |

|-------|-----------|

| `usuarios` | Usuarios registrados |

| `negocios` | Negocios del panel |

| `paginas\_web` | Webs generadas |

| `pagos` | Pagos (futuro) |

| `codigo\_fuente` | Respaldo del código fuente |



\### Tablas propuestas (Fase B)



| Tabla | Propósito |

|-------|-----------|

| `empresas` | Multi-tenant |

| `planes` | Planes comerciales |

| `webs\_historial` | Historial de acciones |



\---



\## 📁 ESTRUCTURA DE CARPETAS (futuro)



