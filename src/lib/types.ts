// ---------------------------------------------------------------------------
// Taxonomía
// ---------------------------------------------------------------------------

export interface Tema {
  slug: string;
  nombre: string;
  descripcion: string;
  icono?: string;
}

export interface Canal {
  slug: string;
  nombre: string;
  canal_id: string;
  suscriptores?: number;
}

// ---------------------------------------------------------------------------
// Libros (cualquier contenido de aprendizaje)
// ---------------------------------------------------------------------------

export type TipoEdicion =
  | 'audiolibro'
  | 'curso'
  | 'documental'
  | 'conferencia'
  | 'clase'
  | 'lectura-comentada'
  | 'pdf'
  | 'ebook';

export interface Edicion {
  tipo: TipoEdicion;
  nombre: string;        // "Narrado por Chavenato", "Curso completo"
  serie?: string;        // slug → Serie (YouTube)
  url?: string;          // recurso externo (futuro)
}

export interface Libro {
  slug: string;
  titulo: string;
  autor: string;
  descripcion: string;
  thumbnail?: string;
  temas: string[];
  ediciones: Edicion[];
}

// ---------------------------------------------------------------------------
// Meditaciones (contenido de práctica)
// ---------------------------------------------------------------------------

export interface VersionMeditacion {
  formato: 'video-youtube' | 'audio' | 'texto';
  nombre: string;
  serie?: string;        // slug → Serie (YouTube)
  url?: string;          // recurso externo (futuro)
}

export interface Meditacion {
  slug: string;
  titulo: string;
  guia: string;          // nombre del guía (equivale a "autor")
  descripcion: string;
  thumbnail?: string;
  temas: string[];
  tipo?: string;         // "guiada", "silencio", etc.
  versiones: VersionMeditacion[];
}

// ---------------------------------------------------------------------------
// Rutas de estudio
// ---------------------------------------------------------------------------

export interface PasoRuta {
  orden: number;
  tipo: 'libro' | 'meditacion';
  ref: string;              // slug del libro o meditación
  nota?: string;
}

export interface Ruta {
  slug: string;
  titulo: string;
  descripcion: string;
  nivel: 'principiante' | 'intermedio' | 'avanzado';
  temas: string[];
  duracion_estimada?: string;
  pasos: PasoRuta[];
}

// ---------------------------------------------------------------------------
// Contenido YouTube (capa interna)
// ---------------------------------------------------------------------------

export interface Episode {
  video_id: string;
  titulo: string;
  url: string;
  fecha_emision: string;
  thumbnail: string;
  descripcion?: string;
  vistas?: number;
  likes?: number;
  comentarios?: number;
  embeddable?: boolean;
}

export interface Serie {
  nombre: string;
  slug: string;
  descripcion: string;
  thumbnail?: string;
  canal: string;         // slug del canal
  temas: string[];
  formato: string;       // tipo original (para referencia)
  idioma?: string;       // "es" | "en" | "multi"
  autores?: string[];
  episodios: Episode[];
}

// ---------------------------------------------------------------------------
// Estructura raíz del JSON
// ---------------------------------------------------------------------------

export interface Biblioteca {
  temas: Tema[];
  canales: Canal[];
  libros: Libro[];
  meditaciones: Meditacion[];
  series: Serie[];
}
