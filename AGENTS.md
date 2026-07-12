# chuchurex — chuchurex.cl

Videoteca personal de crecimiento espiritual. Audiolibros, meditaciones y rutas de estudio curadas desde YouTube.

## Stack

- **Framework**: Astro 5 (output: static)
- **Estilos**: Tailwind CSS 3 (dark-first, paleta definida en DESIGN.md)
- **Tipografia**: DM Serif Display (display) + DM Sans (body)
- **Datos**: JSON estatico (`src/data/biblioteca.json` curado + `src/data/rutas.json` manual)
- **Deploy**: Cloudflare Pages
- **Puerto dev**: 4020

## Estructura

```
src/
├── components/     # Header, Footer, VideoPlayer, EpisodeCard, LibroCard, MeditacionCard, TemaCard, EdicionSelector
├── data/
│   ├── biblioteca.json   # Datos principales (temas, canales, libros, meditaciones, series)
│   └── rutas.json        # Rutas de estudio (curadas manualmente)
├── layouts/        # Layout.astro (SEO, Open Graph, JSON-LD)
├── lib/
│   ├── types.ts    # Tema, Canal, Libro, Meditacion, Serie, Episode, Ruta, PasoRuta
│   ├── utils.ts    # slugify, formatDate, isVideoAvailable, TIPO_LABELS
│   └── datos.ts    # Maps O(1) para lookup de todas las entidades
├── pages/
│   ├── index.astro
│   ├── 404.astro
│   ├── temas/
│   │   ├── index.astro              # Indice de temas
│   │   └── [tema]/index.astro       # Contenido por tema (agrupado por autor)
│   ├── libros/
│   │   ├── index.astro              # Todos los libros (agrupados por tema)
│   │   └── [libro]/
│   │       ├── index.astro          # Detalle libro + selector de ediciones
│   │       └── [episodio].astro     # Video player
│   ├── meditaciones/
│   │   ├── index.astro              # Todas las meditaciones
│   │   └── [meditacion]/
│   │       ├── index.astro          # Detalle meditacion + versiones
│   │       └── [episodio].astro     # Video player
│   └── rutas/
│       ├── index.astro              # Indice de rutas de estudio
│       └── [ruta]/index.astro       # Detalle de ruta con pasos
└── styles/global.css
scripts/
├── canales.json              # Config de 17 canales (handles, slugs, patrones)
├── resolver_channel_id.py    # Resuelve @handle → channelId
├── youtube_extractor.py      # Extrae playlists y episodios
├── obtener_estadisticas.py   # Vistas, likes, embeddable
└── limpiar_descripciones.py  # Limpia boilerplate de descripciones
```

## Comandos

```bash
# Desarrollo
npm run dev          # localhost:4020
npm run build        # Build estatico
npm run preview      # Preview del build

# Pipeline de datos (requiere YOUTUBE_API_KEY en .env)
python scripts/resolver_channel_id.py          # Resolver channelIds
python scripts/youtube_extractor.py            # Extraer datos
python scripts/obtener_estadisticas.py         # Agregar stats
python scripts/limpiar_descripciones.py        # Limpiar descripciones
cp datos/biblioteca_canales.json src/data/youtube/canales.json  # Copiar a src
```

## Jerarquia de datos

```
Tema (8 temas)
├── Libro (87 obras) → Edicion → Serie → Episode
└── Meditacion (3+ series) → Version → Serie → Episode

Ruta de estudio (curada manualmente, archivo separado)
└── PasoRuta → ref a Libro | Meditacion | Episode
```

- `src/data/biblioteca.json`: datos principales (generados por pipeline + curados)
- `src/data/rutas.json`: rutas de estudio (curadas manualmente, pipeline no lo toca)
- Los channel IDs van en `scripts/canales.json` (versionado)
- Solo `YOUTUBE_API_KEY` es secreto (va en `.env`)

## Design System

Leer DESIGN.md antes de tomar cualquier decision visual o de UI.
Tipografia, colores, spacing, layout y direccion estetica estan definidos ahi.
No desviarse sin aprobacion explicita del usuario.

- Dark-first, sin light mode
- Paleta: negro (#0C0C0E), dorado (#E8B04A), crema calido (#F0EDE8)
- Layout tipo streaming (carruseles horizontales, cards con hover)

## Notas

- Todas las rutas usan `getStaticPaths()` (static output)
- Los episodios se identifican por `video_id` en la URL
- El workflow de GitHub Actions actualiza datos cada 6h
- Validacion build-time: refs en rutas.json deben apuntar a libros/meditaciones existentes

## Skill routing

When the user's request matches an available skill, ALWAYS invoke it using the Skill
tool as your FIRST action. Do NOT answer directly, do NOT use other tools first.
The skill has specialized workflows that produce better results than ad-hoc answers.

Key routing rules:
- Product ideas, "is this worth building", brainstorming → invoke office-hours
- Bugs, errors, "why is this broken", 500 errors → invoke investigate
- Ship, deploy, push, create PR → invoke ship
- QA, test the site, find bugs → invoke qa
- Code review, check my diff → invoke review
- Update docs after shipping → invoke document-release
- Weekly retro → invoke retro
- Design system, brand → invoke design-consultation
- Visual audit, design polish → invoke design-review
- Architecture review → invoke plan-eng-review
- Save progress, checkpoint, resume → invoke checkpoint
- Code quality, health check → invoke health
