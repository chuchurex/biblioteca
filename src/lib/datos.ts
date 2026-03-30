import bibliotecaData from '../data/biblioteca.json';
import type { Biblioteca, Tema, Canal, Serie, Episode, Libro, Meditacion } from './types';
import { isVideoAvailable } from './utils';

const db = bibliotecaData as Biblioteca;

// ---------------------------------------------------------------------------
// Índices O(1)
// ---------------------------------------------------------------------------

const TEMA_MAP = new Map<string, Tema>();
for (const t of db.temas) TEMA_MAP.set(t.slug, t);

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

// Índice invertido: canal slug → series
const SERIES_POR_CANAL = new Map<string, Serie[]>();
for (const serie of db.series) {
  const arr = SERIES_POR_CANAL.get(serie.canal) ?? [];
  arr.push(serie);
  SERIES_POR_CANAL.set(serie.canal, arr);
}

// ---------------------------------------------------------------------------
// Índices de Libros
// ---------------------------------------------------------------------------

const LIBRO_MAP = new Map<string, Libro>();
for (const l of db.libros) LIBRO_MAP.set(l.slug, l);

const LIBROS_POR_TEMA = new Map<string, Libro[]>();
for (const libro of db.libros) {
  for (const temaSlug of libro.temas) {
    const arr = LIBROS_POR_TEMA.get(temaSlug) ?? [];
    arr.push(libro);
    LIBROS_POR_TEMA.set(temaSlug, arr);
  }
}

// ---------------------------------------------------------------------------
// Índices de Meditaciones
// ---------------------------------------------------------------------------

const MEDITACION_MAP = new Map<string, Meditacion>();
for (const m of db.meditaciones) MEDITACION_MAP.set(m.slug, m);

const MEDITACIONES_POR_TEMA = new Map<string, Meditacion[]>();
for (const med of db.meditaciones) {
  for (const temaSlug of med.temas) {
    const arr = MEDITACIONES_POR_TEMA.get(temaSlug) ?? [];
    arr.push(med);
    MEDITACIONES_POR_TEMA.set(temaSlug, arr);
  }
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

export function getAllCanales(): Canal[] {
  return db.canales;
}

export function getCanalBySlug(slug: string): Canal | undefined {
  return CANAL_MAP.get(slug);
}

// ---------------------------------------------------------------------------
// Libros
// ---------------------------------------------------------------------------

export function getAllLibros(): Libro[] {
  return db.libros;
}

export function getLibroBySlug(slug: string): Libro | undefined {
  return LIBRO_MAP.get(slug);
}

export function getLibrosByTema(temaSlug: string): Libro[] {
  return LIBROS_POR_TEMA.get(temaSlug) ?? [];
}

export interface EdicionData {
  edicion: Libro['ediciones'][0];
  serie: Serie | undefined;
  episodios: Episode[];
  canal: Canal | undefined;
}

/** Resuelve las ediciones de un libro con sus series, episodios y canales. */
export function getEdicionesDeLLibro(libro: Libro): EdicionData[] {
  return libro.ediciones.map(edicion => {
    const serie = edicion.serie ? SERIE_MAP.get(edicion.serie) : undefined;
    const episodios = serie ? getSerieEpisodios(serie) : [];
    const canal = serie ? CANAL_MAP.get(serie.canal) : undefined;
    return { edicion, serie, episodios, canal };
  });
}

/** Total de episodios disponibles sumando todas las ediciones de un libro. */
export function contarEpisodiosLibro(libro: Libro): number {
  return libro.ediciones.reduce((sum, ed) => {
    const serie = ed.serie ? SERIE_MAP.get(ed.serie) : undefined;
    return sum + (serie ? getSerieEpisodios(serie).length : 0);
  }, 0);
}

// ---------------------------------------------------------------------------
// Meditaciones
// ---------------------------------------------------------------------------

export function getAllMeditaciones(): Meditacion[] {
  return db.meditaciones;
}

export function getMeditacionBySlug(slug: string): Meditacion | undefined {
  return MEDITACION_MAP.get(slug);
}

export function getMeditacionesByTema(temaSlug: string): Meditacion[] {
  return MEDITACIONES_POR_TEMA.get(temaSlug) ?? [];
}

export interface VersionData {
  version: Meditacion['versiones'][0];
  serie: Serie | undefined;
  episodios: Episode[];
  canal: Canal | undefined;
}

/** Resuelve las versiones de una meditación con sus series, episodios y canales. */
export function getVersionesDeMeditacion(med: Meditacion): VersionData[] {
  return med.versiones.map(version => {
    const serie = version.serie ? SERIE_MAP.get(version.serie) : undefined;
    const episodios = serie ? getSerieEpisodios(serie) : [];
    const canal = serie ? CANAL_MAP.get(serie.canal) : undefined;
    return { version, serie, episodios, canal };
  });
}

/** Total de episodios disponibles sumando todas las versiones de una meditación. */
export function contarEpisodiosMeditacion(med: Meditacion): number {
  return med.versiones.reduce((sum, v) => {
    const serie = v.serie ? SERIE_MAP.get(v.serie) : undefined;
    return sum + (serie ? getSerieEpisodios(serie).length : 0);
  }, 0);
}

// ---------------------------------------------------------------------------
// Contenido mixto por tema
// ---------------------------------------------------------------------------

export interface AutorGroup {
  autor: string;
  libros: Libro[];
  meditaciones: Meditacion[];
}

/** Agrupa todo el contenido de un tema por autor/guía. */
export function getContenidoPorAutor(temaSlug: string): AutorGroup[] {
  const libros = getLibrosByTema(temaSlug);
  const meditaciones = getMeditacionesByTema(temaSlug);
  const map = new Map<string, AutorGroup>();

  for (const l of libros) {
    const key = l.autor;
    if (!map.has(key)) map.set(key, { autor: key, libros: [], meditaciones: [] });
    map.get(key)!.libros.push(l);
  }

  for (const m of meditaciones) {
    const key = m.guia;
    if (!map.has(key)) map.set(key, { autor: key, libros: [], meditaciones: [] });
    map.get(key)!.meditaciones.push(m);
  }

  return [...map.values()].sort((a, b) => {
    const countA = a.libros.reduce((sum, l) => sum + contarEpisodiosLibro(l), 0)
      + a.meditaciones.reduce((sum, m) => sum + contarEpisodiosMeditacion(m), 0);
    const countB = b.libros.reduce((sum, l) => sum + contarEpisodiosLibro(l), 0)
      + b.meditaciones.reduce((sum, m) => sum + contarEpisodiosMeditacion(m), 0);
    return countB - countA;
  });
}

/** Cuenta total de episodios disponibles en un tema (libros + meditaciones). */
export function contarEpisodiosPorTema(temaSlug: string): number {
  const libros = getLibrosByTema(temaSlug);
  const meds = getMeditacionesByTema(temaSlug);
  let total = 0;
  for (const l of libros) total += contarEpisodiosLibro(l);
  for (const m of meds) total += contarEpisodiosMeditacion(m);
  return total;
}

// ---------------------------------------------------------------------------
// Series (capa interna YouTube)
// ---------------------------------------------------------------------------

export function getAllSeries(): Serie[] {
  return db.series;
}

export function getSerieBySlug(slug: string): Serie | undefined {
  return SERIE_MAP.get(slug);
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
// Helpers de contexto
// ---------------------------------------------------------------------------

export function getCanalDeSerie(serie: Serie): Canal | undefined {
  return CANAL_MAP.get(serie.canal);
}
