# Design System - chuchurex.cl

## Producto

- **Que es:** Videoteca personal de crecimiento espiritual. Audiolibros, documentales, meditaciones y rutas de estudio curadas desde YouTube.
- **Para quien:** Buscadores espirituales hispanohablantes que tambien consumen Netflix, HBO y YouTube.
- **Dominio:** chuchurex.cl
- **Tipo:** Streaming/catalogo dark-first. No es una biblioteca academica, es un espacio inmersivo para explorar contenido.

## Direccion estetica

- **Referencia:** Netflix, HBO Max, Criterion Channel. Contenido serio en envoltorio atractivo.
- **Mood:** Inmersivo, calido, cinematico. Entras y te quedas.
- **Decoracion:** Intencional. Gradientes sutiles, bordes luminosos en hover, glow dorado. Sin ornamentos gratuitos.
- **Principio:** El contenido es espiritual pero la presentacion compite con entretenimiento. La gente no deberia salir corriendo.

## Tipografia

- **Display/Titulos:** DM Serif Display - serif con personalidad moderna, no academica
- **Cuerpo/UI:** DM Sans - geometrica, limpia, excelente legibilidad en fondos oscuros
- **Carga:** Google Fonts
  ```
  https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=DM+Serif+Display:ital@0;1&display=swap
  ```
- **Escala:**
  - 64px / h1 hero (DM Serif Display 700)
  - 28-32px / h2 section (DM Serif Display 700)
  - 20-22px / h3 card title (DM Serif Display 700)
  - 17px / body large
  - 14-16px / body
  - 12-13px / meta, secondary
  - 10-11px / badges, labels (DM Sans 600, uppercase, tracking 0.1em)

## Color

- **Approach:** Dark-first con acentos calidos

| Token | Hex | Uso |
|-------|-----|-----|
| bg | #0C0C0E | Fondo principal |
| bg-raised | #141418 | Superficies elevadas |
| bg-card | #1A1A20 | Cards, paneles |
| bg-hover | #222228 | Hover states |
| text | #F0EDE8 | Texto primario (crema calido, no blanco puro) |
| text-secondary | #9A968E | Texto secundario, descripciones |
| text-muted | #5A574F | Metadata, placeholders |
| accent | #E8B04A | Dorado. Acento principal, CTAs, enlaces activos |
| accent-glow | rgba(232,176,74,0.15) | Sombras doradas en hover |
| accent-soft | rgba(232,176,74,0.08) | Fondos sutiles de badges |
| warm | #C4785A | Terracota. Acento por tema |
| cool | #5A8EC4 | Azul. Acento por tema |
| green | #5AC47A | Verde. Badges principiante, acento por tema |

- **Bordes:** rgba(255,255,255,0.04) default, rgba(255,255,255,0.08) hover, rgba(232,176,74,0.2) accent hover
- **Dark mode:** Es el modo principal. No hay light mode.

## Spacing

- **Base:** 4px
- **Densidad:** Comfortable
- **Escala:** 4, 8, 12, 16, 20, 24, 32, 48, 60, 80
- **Padding sections:** 24px horizontal (mobile 20px), 60px vertical
- **Container:** max-width implicito por padding 48px en desktop

## Layout

- **Approach:** Streaming/catalogo
- **Patron principal:** Filas horizontales con scroll (content-row)
- **Cards:** flex horizontal, scroll-snap, gap 16px
- **Rutas:** Cards anchas (380px), con barra de color superior por tema
- **Temas:** Grid 4 columnas (2 en mobile)
- **Hero:** 85vh, contenido alineado abajo-izquierda, gradientes de fondo
- **Border radius:** 8px default (radius), 16px cards grandes (radius-lg)

## Componentes clave

### Nav
- Fixed, transparente con gradiente. Solido con blur al scrollear.
- Logo: "chuchu" blanco + "rex" dorado (DM Serif Display)
- Links: 14px DM Sans 500, text-secondary, active/hover text blanco con underline dorado

### Hero
- 85vh, gradientes radiales sutiles de fondo (dorado y azul)
- Badge animado (dot pulsante)
- Titulo 64px con palabra clave en italica dorada
- CTA primario dorado + secundario glass

### Cards (Libros)
- 240px ancho, aspect-ratio 16/9 thumbnail
- Hover: scale 1.08 en imagen, play button dorado aparece, titulo se vuelve dorado
- Badge de episodios sobre la imagen
- Gradiente inferior en hover para legibilidad

### Ruta Cards
- 380px ancho, borde superior de 3px con gradiente por tema
- Badge de nivel (verde principiante, dorado intermedio)
- Footer con dots de progreso + duracion
- Hover: elevacion, borde dorado, sombra profunda

### Tema Items
- Grid, fondo bg-card, icono con fondo de color sutil
- Hover: elevacion sutil

### Stats Bar
- Flex centrado, numeros en DM Serif Display 36px
- Labels uppercase tracking wide

## Movimiento

- **Approach:** Intencional, no minimal. El sitio tiene que sentirse vivo.
- **Easing:** cubic-bezier(0.16, 1, 0.3, 1) para transforms, ease para colores
- **Duracion:** 0.3s transiciones, 0.4s cards, 0.6s image scale
- **Efectos:**
  - Cards: scale imagen en hover, play button fade-in con scale
  - Rutas: translateY(-4px) + sombra en hover
  - Nav: transicion de transparente a blur al scrollear
  - Hero badge: dot con pulse animation infinito
  - Botones: translateY(-1px) + glow en hover

## Decisiones

| Fecha | Decision | Razon |
|-------|----------|-------|
| 2026-04-04 | Dark-first, no light mode | El contenido es video/audio. Fondo oscuro es el estandar en streaming. |
| 2026-04-04 | DM Serif Display + DM Sans | Reemplazan Cormorant Garamond + Nunito Sans. Mas modernas, mejor en dark. |
| 2026-04-04 | Layout tipo streaming | Carruseles horizontales en vez de grids. Netflix-like. La gente sabe usar esto. |
| 2026-04-04 | Nombre: chuchurex | Marca personal. El dominio es la marca. Sin nombre de producto separado. |
| 2026-04-04 | Sin light mode | Un solo modo reduce complejidad. El contenido es consumo nocturno/inmersivo. |
