// ---------------------------------------------------------------------------
// Taxonomía
// ---------------------------------------------------------------------------

export interface Tema {
  slug: string;
  nombre: string;
  descripcion: string;
  icono?: string;
}

export interface Formato {
  slug: string;
  nombre: string;
  descripcion: string;
}

export interface Canal {
  slug: string;
  nombre: string;
  canal_id: string;
  suscriptores?: number;
}

// ---------------------------------------------------------------------------
// Obras (audiolibros agrupados)
// ---------------------------------------------------------------------------

export interface Obra {
  slug: string;           // ej: "las-ensenanzas-de-don-juan"
  titulo: string;         // "Las Enseñanzas de Don Juan"
  autor: string;          // "Carlos Castaneda"
  descripcion: string;
  thumbnail?: string;
  temas: string[];        // slugs de temas
  versiones: string[];    // slugs de series que son versiones de esta obra
}

// ---------------------------------------------------------------------------
// Contenido
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
  canal: string;       // slug del canal
  temas: string[];     // slugs de temas (mínimo 1)
  formato: string;     // slug del formato
  idioma?: string;     // "es" | "en" | "multi"
  autores?: string[];  // nombres libres (Castaneda, Steiner, etc.)
  obra?: string;       // slug de la obra a la que pertenece (si es versión de un audiolibro)
  episodios: Episode[];
}

// ---------------------------------------------------------------------------
// Estructura raíz del JSON
// ---------------------------------------------------------------------------

export interface Biblioteca {
  temas: Tema[];
  formatos: Formato[];
  canales: Canal[];
  obras: Obra[];
  series: Serie[];
}
