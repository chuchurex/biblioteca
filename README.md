# Biblioteca

Videoteca de crecimiento personal. Organiza contenido de YouTube (audiolibros, cursos, meditaciones) por tema, autor y rutas de estudio.

## Desarrollo

**Puerto**: 4020

```bash
# Levantar servidor de desarrollo
npm run dev

# Preview del build de producción
npm run preview

# Build estático
npm run build
```

## Matar el puerto

```bash
# Ver qué proceso usa el puerto
lsof -i :4020

# Matar el proceso en el puerto
lsof -ti:4020 | xargs kill -9
```
