# Biblioteca (chuchurex.cl)

Videoteca de crecimiento personal. Organiza contenido de YouTube (audiolibros, meditaciones y rutas de estudio) por tema, autor y ruta curada. Sitio estatico construido con Astro 5 y Tailwind, desplegado en Cloudflare Pages.

## Stack

- **Framework**: Astro 5 (output estatico)
- **Estilos**: Tailwind CSS 3 (dark-first, ver DESIGN.md)
- **Datos**: JSON estatico en `src/data/` (sin base de datos)
- **Deploy**: Cloudflare Pages
- **Puerto dev**: 4020

## Desarrollo

```bash
npm install          # primera vez

npm run dev          # servidor de desarrollo en localhost:4020
npm run build        # build estatico a dist/
npm run preview      # preview del build en el puerto 4020
```

## Matar el puerto

```bash
# Ver que proceso usa el puerto
lsof -i :4020

# Matar el proceso en el puerto
lsof -ti:4020 | xargs kill -9
```

## Datos

El sitio se alimenta de dos archivos JSON en `src/data/`:

- `biblioteca.json`: datos principales (temas, canales, libros, meditaciones, series). Se genera con el pipeline de YouTube y luego se cura a mano.
- `rutas.json`: rutas de estudio curadas manualmente. El pipeline no lo toca.

Jerarquia: cada Tema agrupa Libros y Meditaciones; cada Libro/Meditacion tiene ediciones o versiones que apuntan a Series y Episodios de YouTube. Las Rutas referencian libros, meditaciones o episodios existentes (se validan en el build).

## Pipeline de datos (YouTube)

Los scripts Python en `scripts/` extraen y actualizan el contenido desde la YouTube Data API. Requieren `YOUTUBE_API_KEY` en `.env` (unico secreto; copiar desde `.env.example`). Los canales configurados viven en `scripts/canales.json` (versionado).

```bash
python scripts/resolver_channel_id.py     # resuelve @handle -> channelId
python scripts/youtube_extractor.py       # extrae playlists y episodios
python scripts/obtener_estadisticas.py    # agrega vistas, likes, embeddable
python scripts/limpiar_descripciones.py   # limpia boilerplate de descripciones
```

Un workflow de GitHub Actions revisa la disponibilidad de los videos periodicamente (`.github/workflows/verificar-videos.yml`).

## Estructura

```
src/
├── components/   # Header, Footer, VideoPlayer, cards (Libro, Meditacion, Tema, Ruta, Episode), EdicionSelector
├── data/         # biblioteca.json + rutas.json
├── layouts/      # Layout.astro (SEO, Open Graph, JSON-LD)
├── lib/          # types.ts, utils.ts, datos.ts (lookups), schema.ts
├── pages/        # index, temas/, libros/, meditaciones/, rutas/, about/, 404
└── styles/
scripts/          # pipeline de datos en Python
```

Todas las rutas usan `getStaticPaths()`; los episodios se identifican por `video_id` en la URL.

## Diseno

Antes de tocar UI, leer DESIGN.md: tipografia, paleta (dark-first, dorado sobre negro), spacing y direccion estetica tipo streaming (carruseles horizontales, cards con hover).
