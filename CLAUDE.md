# Biblioteca — biblioteca.chuchurex.cl

Videoteca multi-canal de YouTube. Organiza videos de múltiples canales por sus playlists nativas.

## Stack

- **Framework**: Astro 5 (output: static)
- **Estilos**: Tailwind CSS 3 (paleta `brand-*` azul tinta/crema/verde)
- **Tipografía**: Inter
- **Datos**: JSON estático generado por scripts Python
- **Deploy**: Cloudflare Pages (futuro)
- **Puerto dev**: 4020

## Estructura

```
src/
├── components/     # Header, Footer, VideoPlayer, EpisodeCard, ChannelCard, FranjaRow
├── data/youtube/   # canales.json (generado por pipeline)
├── layouts/        # Layout.astro (SEO, Open Graph, JSON-LD)
├── lib/
│   ├── types.ts    # Canal, Programa, Episode
│   ├── utils.ts    # slugify, formatDate, formatNumber
│   └── datos.ts    # Maps O(1) para lookup de canales/videos
├── pages/
│   ├── index.astro
│   ├── 404.astro
│   └── canales/
│       └── [canal]/
│           ├── index.astro           # Programas del canal
│           └── [programa]/
│               ├── index.astro       # Episodios del programa
│               └── [episodio].astro  # Video player
└── styles/global.css
scripts/
├── canales.json              # Config de canales (handles, slugs, patrones)
├── resolver_channel_id.py    # Resuelve @handle → channelId
├── youtube_extractor.py      # Extrae playlists y episodios
├── obtener_estadisticas.py   # Vistas, likes, embeddable
└── limpiar_descripciones.py  # Limpia boilerplate de descripciones
```

## Comandos

```bash
# Desarrollo
npm run dev          # localhost:4020
npm run build        # Build estático
npm run preview      # Preview del build

# Pipeline de datos (requiere YOUTUBE_API_KEY en .env)
python scripts/resolver_channel_id.py          # Resolver channelIds
python scripts/youtube_extractor.py            # Extraer datos
python scripts/obtener_estadisticas.py         # Agregar stats
python scripts/limpiar_descripciones.py        # Limpiar descripciones
cp datos/biblioteca_canales.json src/data/youtube/canales.json  # Copiar a src
```

## Jerarquía de datos

Canal > Programa (playlist) > Episodio (video)

- Los channel IDs van en `scripts/canales.json` (versionado)
- Solo `YOUTUBE_API_KEY` es secreto (va en `.env`)
- `src/data/youtube/canales.json` es el archivo que consume Astro

## Paleta de colores

- `brand-600` (#1E3A5F): Azul primario (tinta)
- `brand-400` (#1E6B52): Verde acento (marcapáginas)
- `brand-50` (#F5F7FA): Fondo claro
- `brand-900` (#0A1628): Fondo oscuro
- Misma convención `brand-*` que lahoradelanostalgia.com

## Notas

- Todas las rutas usan `getStaticPaths()` (static output)
- Los episodios se identifican por `video_id` en la URL
- El workflow de GitHub Actions actualiza datos cada 6h
