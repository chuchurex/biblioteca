// ---------------------------------------------------------------------------
// JSON-LD builders. Una sola fuente de verdad para el schema del sitio.
// Entidades enlazadas por @id estable para que los motores las unifiquen.
// ---------------------------------------------------------------------------
import type { Libro, Ruta, Tema } from './types';

const SITE = 'https://chuchurex.cl';
const WEBSITE_ID = `${SITE}/#website`;
const PERSON_ID = `${SITE}/about/#carlos`;

const SITE_DESC =
  'Biblioteca espiritual curada: audiolibros, conferencias, meditaciones y rutas de estudio en español.';

function abs(path: string): string {
  return new URL(path, SITE).href;
}

// Nodo Person mínimo, referenciable por @id desde cualquier publisher/author.
const publisherRef = { '@id': PERSON_ID };

// --- Globales -------------------------------------------------------------

export function buildWebSite() {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    '@id': WEBSITE_ID,
    url: `${SITE}/`,
    name: 'chuchurex',
    description: SITE_DESC,
    inLanguage: 'es',
    publisher: publisherRef,
  };
}

// Person completo: va solo en /about/. Mismo @id que el publisherRef.
export function buildPerson(opts: { jobTitle: string; sameAs: string[] }) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Person',
    '@id': PERSON_ID,
    name: 'Carlos Martínez',
    url: `${SITE}/about/`,
    image: abs('/images/about/carlos.webp'),
    jobTitle: opts.jobTitle,
    description:
      'Curador de chuchurex.cl, una biblioteca espiritual que ordena audiolibros, conferencias y meditaciones de YouTube en rutas de estudio.',
    sameAs: opts.sameAs,
  };
}

// --- Breadcrumbs ----------------------------------------------------------

export function buildBreadcrumb(items: { name: string; path: string }[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((it, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: it.name,
      item: abs(it.path),
    })),
  };
}

// --- Por tipo de página ---------------------------------------------------

export function buildLibro(libro: Libro, _totalEps: number) {
  return {
    '@context': 'https://schema.org',
    '@type': 'CreativeWork',
    name: libro.titulo,
    ...(libro.autor && { author: { '@type': 'Person', name: libro.autor } }),
    ...(libro.descripcion && { description: libro.descripcion }),
    ...(libro.thumbnail && { image: libro.thumbnail }),
    url: abs(`/libros/${libro.slug}/`),
    inLanguage: 'es',
    isPartOf: { '@id': WEBSITE_ID },
    publisher: publisherRef,
  };
}

export function buildRuta(
  ruta: Ruta,
  pasos: { titulo: string; href: string }[],
) {
  return {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name: ruta.titulo,
    description: ruta.descripcion,
    url: abs(`/rutas/${ruta.slug}/`),
    itemListOrder: 'https://schema.org/ItemListOrderAscending',
    numberOfItems: pasos.length,
    itemListElement: pasos.map((p, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: p.titulo,
      url: abs(p.href),
    })),
  };
}

export function buildTema(tema: Tema, _totalTitulos: number) {
  return {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: tema.nombre,
    description: tema.descripcion,
    url: abs(`/temas/${tema.slug}/`),
    inLanguage: 'es',
    isPartOf: { '@id': WEBSITE_ID },
    about: { '@type': 'Thing', name: tema.nombre },
  };
}
