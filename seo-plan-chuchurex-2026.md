# Plan SEO + AEO — chuchurex.cl v2 — Q2/Q3 2026

**Owner:** Carlos Martínez (chuchurex)
**Última actualización:** 2026-06-18
**Cadencia de revisión:** mensual (regla: si este doc lleva 6 semanas sin actualizarse, está muerto)
**Estado del sitio:** v2 lanzada el 2026-06-10. El dominio antes alojaba un portafolio personal (no una biblioteca v1), con presencia de búsqueda casi nula (ver Fase 0). GA4 activo (G-P2G8CL5J2V). GSC: propiedad de dominio verificada, sitemap enviado. Automatización de GSC vía service account (no gcloud); detalle al final de Fase 0.
**Repo y hosting:** este sitio es el proyecto `biblioteca` (Astro, output estático SSG), Cloudflare Pages, sirviendo el dominio raíz chuchurex.cl. `biblioteca.chuchurex.cl` y `www` redirigen 301 a la raíz. Todo el trabajo técnico de este plan se ejecuta en este repo (`~/Sites/active/biblioteca`), NO en el repo `chuchurex/chuchurex` (que hoy es solo portafolio + API en chuchurex.pages.dev).

---

## Contexto

chuchurex.cl es una biblioteca espiritual curada: 86 contenidos (audiolibros, lecturas comentadas), 6 rutas de estudio, 9 temas y 1.713 episodios sobre antroposofía, Ley del Uno, chamanismo tolteca, Cuarto Camino, astrología evolutiva y afines. Todo en español.

**Objetivos de negocio (no SEO):**
1. El sitio es el destino final de las visitas (no es funnel hacia eluno.org ni elultimodisco.cl).
2. Visibilidad personal de Carlos como autor/creador del sitio (atribución de entidad), NO como funnel de contratación de desarrollo web.
3. Que el sitio se vuelva una herramienta de estudio popular y recurrente.

**Sobre el objetivo 2 (acotado):** la /about/ con schema Person y `sameAs` (GitHub, LinkedIn) es una nota de autoría legítima y machine-readable: ata la entidad "chuchurex" ↔ "Carlos Martínez". Pero este sitio gana autoridad temática en espiritualidad, no en "desarrollo web", así que NO esperar que ranque para captar pega de dev. Esa meta es un proyecto SEO aparte sobre el portafolio (chuchurex.pages.dev) y no se persigue desde este plan. Nota: "Carlos Martínez" es un nombre muy común; la desambiguación depende de los `sameAs` y menciones externas consistentes, no del schema solo.

---

## Pirámide (producto → solución → problema → audiencia)

| Nivel | Páginas | Keywords ejemplo | Prioridad |
|---|---|---|---|
| Producto (transaccional) | /libros/[slug]/ | "cómo conocer los mundos superiores audiolibro español", "ley del uno audiolibro", "evangelio de juan steiner audio" | 1 |
| Solución (consideración) | /rutas/[slug]/ | "en qué orden leer a castaneda", "por dónde empezar con steiner", "orden libros castaneda" | 2 (y prioridad 1 en AEO) |
| Problema (exploración) | /temas/[slug]/ | "qué es la antroposofía", "qué es el cuarto camino", "qué es la ley del uno" | 3 |
| Audiencia (awareness) | /meditaciones/, home | "meditaciones guiadas español" | 4 (competencia brutal, no perseguir aún) |

Nota: en nivel producto los competidores SERP son YouTube, Spotify e Ivoox, no sitios web. La ventaja diferencial del sitio es la curaduría + orden + contexto, no el hosting del audio.

---

## Objetivos SMART (borrador, ajustar con baseline)

1. Indexación completa: 100% de URLs nuevas indexadas en GSC antes del 2026-07-15.
2. Tráfico orgánico no-branded: establecer baseline en julio 2026 y crecer 3x para diciembre 2026 (HIPÓTESIS - sin datos de la v2 aún, recalibrar con primer mes de GSC).
3. Visibilidad AEO como fuente primaria: de baseline (medición junio 2026) a 40%+ en las 5 preguntas test para septiembre 2026.
4. Entidad personal: que la búsqueda "carlos martínez chuchurex desarrollador" y consultas AI sobre el creador del sitio devuelvan información correcta para agosto 2026.

---

## Fase 0 — Post-lanzamiento (CERRADA, verificada en GSC 2026-06-18)

**El riesgo original (perder el equity de una "v1") era falso.** La verificación vía API de GSC (`sc-domain:chuchurex.cl`, propiedad de dominio verificada) mostró:
- Tráfico total últimos 73 días: **7 clicks, 59 impresiones**. Esto es un cold start, no una migración con equity en juego.
- Las únicas queries son el nombre de marca mal tecleado (`chuchure`, `chuchurek`). No hay autoridad temática previa que rescatar.
- Lo que tenía impresiones históricas **no era una biblioteca v1**, era el **sitio anterior (portafolio)** que vivía en el dominio: `/about.html` (20 impr), `/icei/` (12 impr), `/flor/`, `/1-2-3-sali/`, `/privacidad`. Todas dan 404 hoy.

**Conclusión:** el archivo `public/_redirects` (que mapea el cambio de slugs tema→libros de la biblioteca) es correcto mantenerlo para links viejos, pero NO recupera tráfico relevante. El trabajo real es de cold start: indexar las 1.790 URLs y construir autoridad desde cero (Fase 2 + 3).

**Hallazgo abierto:** existe un subdominio `admision.chuchurex.cl` con contenido ajeno (UChile/SAE). Como la propiedad GSC es de dominio, ensucia los datos. Decidir si se separa o se filtra en los reportes.

| # | Acción | Ejecutor | Estado |
|---:|---|---|---|
| 0.1 | Exportar URLs históricas con impresiones/clicks vía API GSC | Claude Code | HECHO — solo legacy del portafolio, sin equity de biblioteca |
| 0.2 | Mapear URLs viejas → nuevas con 301s | Claude Code | HECHO — `_redirects` cubre slugs biblioteca; añadido `/about.html`→`/about/`; resto del portafolio se deja en 404 a propósito |
| 0.3 | Verificar sitemap generado y enviado en GSC | Carlos | HECHO — `sitemap-index.xml` enviado 2026-06-15, leído 2026-06-16, 0 errores, 1.790 URLs |
| 0.4 | Verificar robots.txt no bloquea nada crítico | Claude Code | HECHO — `Allow: /` + referencia al sitemap (commit 94045e1) |
| 0.5 | Revisar GSC Cobertura primeros 14 días: 404s, soft 404s, duplicados | Carlos | En curso — sin errores de sitemap; revisar indexación de las 1.790 |
| 0.6 | Verificar que el HTML SSG trae el contenido clave sin depender de JS | Claude Code | Pendiente |
| 0.7 | Confirmar si las URLs cambiaron | Claude Code | HECHO — sí cambiaron (`/{tema}/{libro}` → `/libros/{libro}`), redirects construidos |

**Acceso GSC para automatización (Fase 4.1):** service account `revisor-dominios@chuchurex-seo.iam.gserviceaccount.com` (siteOwner), key en `~/Sites/_security-runbook/gsc-service-account.json` (fuera del repo). Scope `webmasters`. Nota: `gcloud auth` NO sirve para GSC (su allowlist de scopes excluye Search Console); usar siempre el SA.

## Fase 1 — Baseline (semanas 1-2)

| # | Acción | Ejecutor | Estado |
|---:|---|---|---|
| 1.1 | Audit AEO de 5 preguntas (ver sección AEO abajo) en ChatGPT, Claude, Perplexity y Gemini, en incógnito. Guardar como aeo-baseline-2026-06-XX.csv | Carlos (manual, incógnito obligatorio) | Pendiente |
| 1.2 | Pull GSC v1: top queries y top pages históricos como referencia de qué ya rankeaba | Claude Code (API) | Pendiente |
| 1.3 | Radiografía de competidores: hermandadblanca.org, bibliotecas antroposóficas online, upasika, canales Ivoox/YouTube que rankean en web para las keywords de nivel producto y solución | Carlos + Claude | Pendiente |

## Fase 2 — Fundamentos técnicos (semanas 2-3)

| # | Acción | Ejecutor | Estado |
|---:|---|---|---|
| 2.1 | Schema JSON-LD: WebSite + publisher Person, BreadcrumbList global | Claude Code | HECHO (2026-06-18) — `src/lib/schema.ts`. WebSite movido a solo el home, Person como publisher por @id. SearchAction omitido a propósito (no hay buscador aún y Google retiró el sitelinks searchbox) |
| 2.2 | Schema por tipo de página: /libros/ y /meditaciones/ → CreativeWork (author real), /rutas/ → ItemList con itemListOrder, /temas/ → CollectionPage. NO usar HowTo ni FAQPage | Claude Code | HECHO (2026-06-18) — los 5 tipos + episodios (VideoObject) |
| 2.3 | Validar TODO schema en validator.schema.org antes de deploy | Claude Code + Carlos | HECHO — 0 errores / 0 warnings en los 5 tipos |
| 2.4 | Meta descriptions únicas por página | Claude Code | HECHO — detalle (libro/ruta/tema/medit/about) e índices pasan description propia; el default del Layout solo cubre páginas sin una específica |
| 2.5 | Person schema en /about/: Carlos Martínez, jobTitle, sameAs | Claude Code | HECHO — jobTitle "Desarrollador front end", sameAs GitHub + Instagram |
| 2.6 | Core Web Vitals: medir LCP, INP, CLS | Claude Code | PARCIAL — PSI bloqueado (rate limit anónimo / no reusar key YouTube). Auditoría de recursos: home 6.5KB gzip, GA4 async, imgs lazy, sin scripts bloqueantes. Único render-blocking externo: Google Fonts (mitigado con preconnect + display=swap). Optimización opcional pendiente: self-hostear fuentes. Falta medición Lighthouse formal |
| 2.7 | Canonicals autorreferentes, verificar paginaciones/filtros | Claude Code | HECHO — canonical autorreferente en el Layout; no hay paginación ni filtros en los índices |

## Fase 3 — AEO on-page en rutas y temas (semanas 4-6)

Las rutas son el activo AEO principal: responden exactamente las preguntas que la gente le hace a las IAs ("en qué orden leer X").

| # | Acción | Ejecutor | Estado |
|---:|---|---|---|
| 3.1 | Reescribir intro de cada ruta con entidades + tripletes | Carlos + Claude Code | HECHO (2026-06-18) — campo `respuesta` por ruta en rutas.json: sujeto chuchurex.cl, orden explícito, entidades nombradas. Revisar voz si hace falta |
| 3.2 | Chunking: cada H2 en formato pregunta, respuesta standalone que menciona chuchurex.cl | Carlos + Claude Code | HECHO (2026-06-18) — campo `pregunta` renderizado como H2 + `respuesta` tras el intro. Sin FAQPage (prohibido); Q&A como HTML on-page |
| 3.3 | Páginas /temas/: párrafo inicial que defina la entidad en formato cita-able antes del listado | Carlos + Claude Code | Pendiente — las /temas/ ya tienen `descripcion` arriba; falta darle formato definición cita-able ("La antroposofía es...") |
| 3.4 | Internal linking piramidal: temas → rutas → libros, anchors descriptivos | Claude Code | Pendiente |
| 3.5 | Evaluar llms.txt en raíz del sitio | Claude Code | HECHO (2026-06-18) — `public/llms.txt` generado desde datos (rutas + temas + secciones), en vivo |

## Fase 4 — Medir e iterar (desde semana 6, recurrente)

| # | Acción | Frecuencia |
|---:|---|---|
| 4.1 | Rutina GSC mensual: pull vía API, filtrar posiciones 11-20 y 4-7, calcular Net Opportunity = (0.20 × impresiones) − clicks, actualizar backlog | Mensual, 1ra semana |
| 4.2 | Re-medición AEO (mismas 5 preguntas, mismos motores, incógnito) | Días 30 y 60 post-baseline |
| 4.3 | A/B de titles: una variable a la vez, esperar 2-4 semanas entre cambios | Por iteración |

---

## AEO — Las 5 preguntas baseline (propuesta)

1. "¿En qué orden debo leer los libros de Carlos Castaneda?" (solución)
2. "¿Dónde puedo escuchar la Ley del Uno (Material de Ra) en español?" (producto)
3. "¿Por dónde empiezo a estudiar a Rudolf Steiner?" (solución)
4. "¿Qué es el Cuarto Camino de Gurdjieff?" (problema)
5. "¿Hay alguna biblioteca de audiolibros de espiritualidad en español?" (categoría/comparativa)

Métricas: visibilidad por mención y visibilidad como fuente primaria (URL citada). La segunda es la que importa. Meta de largo plazo: 51%+.

---

## Proyección

Sin datos de la v2 todavía no hay proyección defendible (regla: data > supuestos). Después del primer mes completo de GSC, aplicar: potencial = búsquedas mensuales de keywords objetivo × tasa de captura (conservador 14%, intermedio 20%, agresivo 30%) y registrar acá.

---

## Próximos pasos inmediatos

1. Fase 0 cerrada (verificada en GSC). El foco pasa a cold start: indexación + autoridad.
2. Esta semana: correr el baseline AEO (Fase 1.1) antes de tocar contenido, para poder demostrar impacto después.
3. En Claude Code: ejecutar Fase 2 sobre ESTE repo (`~/Sites/active/biblioteca`, Astro). Prioridad de mayor ROI según lo verificado: schema por tipo de página (2.2), Person en /about/ (2.5), mover el `WebSite` schema a solo el home y añadir BreadcrumbList (2.1), luego AEO en rutas (Fase 3).
4. Decidir qué hacer con el subdominio `admision.chuchurex.cl` (contenido ajeno que ensucia la propiedad de dominio en GSC).
