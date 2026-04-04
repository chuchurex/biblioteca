# TODOS

## Fase 1.5: Busqueda y Tests

### Setup Vitest para tests unitarios
- **Que**: Configurar Vitest + tests para funciones en datos.ts (getAllRutas, getRutaBySlug, validacion de refs)
- **Por que**: Fase 1.5 agrega busqueda (Pagefind) con logica mas compleja que necesita tests
- **Contexto**: Hoy no hay tests. La validacion build-time cubre el riesgo principal de Fase 1. El framework de tests deberia estar listo antes de agregar busqueda.
- **Depende de**: Fase 1 completada

### Integrar Pagefind para busqueda client-side
- **Que**: Agregar Pagefind para busqueda sobre titulos, autores, temas, descripciones
- **Por que**: 1,730+ episodios no son navegables solo con filtros
- **Contexto**: Pagefind se integra post-build en sitios estaticos Astro. Requiere configuracion de que campos indexar y pesos de ranking.
- **Depende de**: Fase 1 completada, sitio en produccion

### Filtros avanzados en /libros/ y /meditaciones/
- **Que**: Filtros client-side por tema, autor, tipo de edicion, duracion (meditaciones)
- **Contexto**: Vanilla JS o Alpine.js, persistir estado en URL query params
- **Depende de**: Fase 1 completada
