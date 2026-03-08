import bibliotecaData from '../data/biblioteca.json';
import type { Biblioteca, Tema, Formato, Canal, Serie, Episode } from './types';
import { isVideoAvailable } from './utils';

const db = bibliotecaData as Biblioteca;

// ---------------------------------------------------------------------------
// Índices O(1)
// ---------------------------------------------------------------------------

const TEMA_MAP = new Map<string, Tema>();
for (const t of db.temas) TEMA_MAP.set(t.slug, t);

const FORMATO_MAP = new Map<string, Formato>();
for (const f of db.formatos) FORMATO_MAP.set(f.slug, f);

const CANAL_MAP = new Map<string, Canal>();
for (const c of db.canales) CANAL_MAP.set(c.slug, c);

const SERIE_MAP = new Map<string, Serie>();
for (const s of db.series) SERIE_MAP.set(s.slug, s);

const VIDEO_MAP = new Map<string, { episode: Episode; serie: Serie }>();
for (const serie of db.series) {
  for (const ep of serie.episodios) {
    if (!VIDEO_MAP.has(ep.video_id) && isVideoAvailable(ep)) {
      VIDEO_MAP.set(ep.video_id, { episode: ep, serie });
    }
  }
}

// Índice invertido: tema slug → series
const SERIES_POR_TEMA = new Map<string, Serie[]>();
for (const serie of db.series) {
  for (const temaSlug of serie.temas) {
    const arr = SERIES_POR_TEMA.get(temaSlug) ?? [];
    arr.push(serie);
    SERIES_POR_TEMA.set(temaSlug, arr);
  }
}

// Índice invertido: formato slug → series
const SERIES_POR_FORMATO = new Map<string, Serie[]>();
for (const serie of db.series) {
  const arr = SERIES_POR_FORMATO.get(serie.formato) ?? [];
  arr.push(serie);
  SERIES_POR_FORMATO.set(serie.formato, arr);
}

// Índice invertido: canal slug → series
const SERIES_POR_CANAL = new Map<string, Serie[]>();
for (const serie of db.series) {
  const arr = SERIES_POR_CANAL.get(serie.canal) ?? [];
  arr.push(serie);
  SERIES_POR_CANAL.set(serie.canal, arr);
}

// ---------------------------------------------------------------------------
// Taxonomía
// ---------------------------------------------------------------------------

export function getAllTemas(): Tema[] {
  return db.temas;
}

export function getTemaBySlug(slug: string): Tema | undefined {
  return TEMA_MAP.get(slug);
}

export function getAllFormatos(): Formato[] {
  return db.formatos;
}

export function getFormatoBySlug(slug: string): Formato | undefined {
  return FORMATO_MAP.get(slug);
}

export function getAllCanales(): Canal[] {
  return db.canales;
}

export function getCanalBySlug(slug: string): Canal | undefined {
  return CANAL_MAP.get(slug);
}

// ---------------------------------------------------------------------------
// Series
// ---------------------------------------------------------------------------

export function getAllSeries(): Serie[] {
  return db.series;
}

export function getSerieBySlug(slug: string): Serie | undefined {
  return SERIE_MAP.get(slug);
}

export function getSeriesByTema(temaSlug: string): Serie[] {
  return SERIES_POR_TEMA.get(temaSlug) ?? [];
}

export function getSeriesByFormato(formatoSlug: string): Serie[] {
  return SERIES_POR_FORMATO.get(formatoSlug) ?? [];
}

export function getSeriesByCanal(canalSlug: string): Serie[] {
  return SERIES_POR_CANAL.get(canalSlug) ?? [];
}

// ---------------------------------------------------------------------------
// Episodios
// ---------------------------------------------------------------------------

export function getSerieEpisodios(serie: Serie): Episode[] {
  return serie.episodios.filter(isVideoAvailable);
}

export function getVideoData(videoId: string): { episode: Episode; serie: Serie } | undefined {
  return VIDEO_MAP.get(videoId);
}

// ---------------------------------------------------------------------------
// Helpers de contexto (para breadcrumbs, etc.)
// ---------------------------------------------------------------------------

/** Devuelve el tema principal de una serie (el primero de la lista). */
export function getTemaPrincipal(serie: Serie): Tema | undefined {
  return TEMA_MAP.get(serie.temas[0]);
}

/** Devuelve el canal de una serie. */
export function getCanalDeSerie(serie: Serie): Canal | undefined {
  return CANAL_MAP.get(serie.canal);
}

/** Cuenta total de episodios disponibles en un tema. */
export function contarEpisodiosPorTema(temaSlug: string): number {
  const series = SERIES_POR_TEMA.get(temaSlug) ?? [];
  return series.reduce((sum, s) => sum + getSerieEpisodios(s).length, 0);
}
