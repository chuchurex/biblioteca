import type { Episode } from './types';
import type { TipoEdicion } from './types';

export function slugify(text: string): string {
  return text.toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

/**
 * Verifica que un episodio no sea un video eliminado o privado.
 */
export function isVideoAvailable(ep: Episode): boolean {
  if (ep.titulo === 'Deleted video' || ep.titulo === 'Private video') return false;
  return true;
}

/**
 * Formatea fecha en español chileno.
 */
export function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  if (isNaN(date.getTime())) return '';
  return date.toLocaleDateString('es-CL', {
    year: 'numeric', month: 'long', day: 'numeric'
  });
}

/**
 * Labels legibles para tipos de edición.
 */
export const TIPO_LABELS: Record<TipoEdicion, string> = {
  audiolibro: 'Audiolibro',
  curso: 'Curso',
  documental: 'Documental',
  conferencia: 'Conferencia',
  clase: 'Clase',
  'lectura-comentada': 'Lectura comentada',
  pdf: 'PDF',
  ebook: 'eBook',
};
