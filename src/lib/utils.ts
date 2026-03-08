import type { Episode } from './types';

export function slugify(text: string): string {
  return text.toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

/**
 * Extrae el video ID de una URL de YouTube o lo devuelve si ya es un ID.
 */
export function getVideoId(url: string): string {
  try {
    if (url.includes('youtu.be/')) {
      return url.split('youtu.be/')[1].split(/[?&#]/)[0];
    }
    const urlObj = new URL(url);
    return urlObj.searchParams.get('v') || '';
  } catch {
    return url;
  }
}

/**
 * Verifica que un episodio no sea un video eliminado o privado.
 */
export function isVideoAvailable(ep: Episode): boolean {
  if (ep.titulo === 'Deleted video' || ep.titulo === 'Private video') return false;
  return true;
}

/**
 * Genera un slug para un programa.
 */
export function getProgramaSlug(nombre: string): string {
  return slugify(nombre);
}

/**
 * Genera un slug para un episodio basado en su título.
 */
export function getEpisodioSlug(titulo: string, videoId: string): string {
  const slug = slugify(titulo);
  // Usar primeros 60 chars del slug + videoId para unicidad
  const truncated = slug.substring(0, 60).replace(/-$/, '');
  return `${truncated}-${videoId}`;
}

/**
 * Formatea fecha en español chileno.
 */
export function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('es-CL', {
    year: 'numeric', month: 'long', day: 'numeric'
  });
}

/**
 * Formatea un número con separadores de miles.
 */
export function formatNumber(num: number): string {
  return num.toLocaleString('es-CL');
}
