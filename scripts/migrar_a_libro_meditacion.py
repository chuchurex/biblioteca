#!/usr/bin/env python3
"""
Migra biblioteca.json del modelo Obra/Serie al modelo Libro/Meditación.

Input:  src/data/biblioteca.json (formato actual)
Output: src/data/biblioteca.json (formato nuevo)

Backup del original en src/data/biblioteca.backup.json
"""

import json
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "src" / "data" / "biblioteca.json"
BACKUP = ROOT / "src" / "data" / "biblioteca.backup.json"
OUTPUT = INPUT  # sobreescribe

# ---------------------------------------------------------------------------
# Series de meditación (se convierten en Meditación)
# ---------------------------------------------------------------------------
MEDITATION_SLUGS = {
    "el-camino-sin-sendero-meditaciones",
    "sudja-meditacion-diaria-2026",
    "meditaciones-guiadas-ramiro-calle",
}

# ---------------------------------------------------------------------------
# Documentales bilingües (se agrupan en un solo Libro)
# ---------------------------------------------------------------------------
BILINGUAL_GROUPS = [
    {
        "slug": "samadhi",
        "titulo": "Samadhi",
        "autor": "Daniel Schmidt",
        "descripcion": "Trilogía documental sobre meditación, la ilusión del yo y el camino sin sendero.",
        "temas": ["consciencia"],
        "series": [
            {"serie_slug": "samadhi-espanol", "nombre": "Documental (Español)"},
            {"serie_slug": "samadhi-english", "nombre": "Documentary (English)"},
        ],
    },
    {
        "slug": "mundos-internos-mundos-externos",
        "titulo": "Mundos Internos, Mundos Externos",
        "autor": "Daniel Schmidt",
        "descripcion": "Documental en 4 partes sobre la conexión entre mundos internos y externos: Akasha, la espiral, la serpiente y el loto, más allá del pensamiento.",
        "temas": ["consciencia"],
        "series": [
            {"serie_slug": "mundos-internos-mundos-externos-es", "nombre": "Documental (Español)"},
            {"serie_slug": "inner-worlds-outer-worlds-en", "nombre": "Documentary (English)"},
        ],
    },
]

# Todos los slugs que ya se manejan como bilingüe
BILINGUAL_SERIE_SLUGS = set()
for group in BILINGUAL_GROUPS:
    for s in group["series"]:
        BILINGUAL_SERIE_SLUGS.add(s["serie_slug"])


# ---------------------------------------------------------------------------
# Mapeo de formato de serie → TipoEdicion
# ---------------------------------------------------------------------------
FORMATO_A_TIPO = {
    "audiolibro": "audiolibro",
    "curso": "curso",
    "documental": "documental",
    "conferencia": "conferencia",
    "clase": "clase",
    "lectura-comentada": "lectura-comentada",
    "podcast": "conferencia",  # podcasts → conferencia
    "meditacion-guiada": "clase",  # no debería llegar aquí para Libros
    "meditacion": "clase",         # no debería llegar aquí para Libros
}

FORMATO_NOMBRES = {
    "audiolibro": "Audiolibro",
    "curso": "Curso completo",
    "documental": "Documental",
    "conferencia": "Conferencia",
    "clase": "Clase",
    "lectura-comentada": "Lectura comentada",
    "podcast": "Conferencia",
}


def load_data():
    with open(INPUT, "r", encoding="utf-8") as f:
        return json.load(f)


def build_serie_map(data):
    return {s["slug"]: s for s in data["series"]}


def build_canal_map(data):
    return {c["slug"]: c for c in data["canales"]}


def serie_to_edicion(serie, canal_map, multi_version=False):
    """Convierte una serie en una Edicion de Libro."""
    formato = serie.get("formato", "audiolibro")
    tipo = FORMATO_A_TIPO.get(formato, "audiolibro")

    if multi_version and tipo == "audiolibro":
        canal = canal_map.get(serie["canal"])
        nombre = f"Narrado por {canal['nombre']}" if canal else "Audiolibro"
    else:
        nombre = FORMATO_NOMBRES.get(formato, formato.capitalize())

    edicion = {
        "tipo": tipo,
        "nombre": nombre,
        "serie": serie["slug"],
    }
    return edicion


def obra_to_libro(obra, serie_map, canal_map):
    """Convierte una Obra actual en un Libro."""
    versiones = obra.get("versiones", [])
    multi = len(versiones) > 1

    ediciones = []
    thumbnail = obra.get("thumbnail")

    for v_slug in versiones:
        serie = serie_map.get(v_slug)
        if not serie:
            continue
        edicion = serie_to_edicion(serie, canal_map, multi_version=multi)
        ediciones.append(edicion)
        if not thumbnail and serie.get("thumbnail"):
            thumbnail = serie["thumbnail"]

    libro = {
        "slug": obra["slug"],
        "titulo": obra["titulo"],
        "autor": obra["autor"],
        "descripcion": obra.get("descripcion", ""),
        "temas": obra["temas"],
        "ediciones": ediciones,
    }
    if thumbnail:
        libro["thumbnail"] = thumbnail

    return libro


def serie_independiente_to_libro(serie, canal_map):
    """Convierte una serie independiente (no meditación, no bilingüe) en un Libro."""
    autor = (serie.get("autores") or ["Desconocido"])[0]
    formato = serie.get("formato", "audiolibro")
    tipo = FORMATO_A_TIPO.get(formato, "audiolibro")
    nombre = FORMATO_NOMBRES.get(formato, formato.capitalize())

    edicion = {
        "tipo": tipo,
        "nombre": nombre,
        "serie": serie["slug"],
    }

    libro = {
        "slug": serie["slug"],
        "titulo": serie["nombre"],
        "autor": autor,
        "descripcion": serie.get("descripcion", ""),
        "temas": serie.get("temas", []),
        "ediciones": [edicion],
    }
    if serie.get("thumbnail"):
        libro["thumbnail"] = serie["thumbnail"]

    return libro


def bilingual_group_to_libro(group, serie_map):
    """Convierte un grupo bilingüe en un Libro con múltiples ediciones."""
    ediciones = []
    thumbnail = None

    for entry in group["series"]:
        serie = serie_map.get(entry["serie_slug"])
        if not serie:
            continue
        edicion = {
            "tipo": "documental",
            "nombre": entry["nombre"],
            "serie": serie["slug"],
        }
        ediciones.append(edicion)
        if not thumbnail and serie.get("thumbnail"):
            thumbnail = serie["thumbnail"]

    libro = {
        "slug": group["slug"],
        "titulo": group["titulo"],
        "autor": group["autor"],
        "descripcion": group["descripcion"],
        "temas": group["temas"],
        "ediciones": ediciones,
    }
    if thumbnail:
        libro["thumbnail"] = thumbnail

    return libro


def serie_to_meditacion(serie):
    """Convierte una serie de meditación en una Meditación."""
    guia = (serie.get("autores") or ["Desconocido"])[0]

    version = {
        "formato": "video-youtube",
        "nombre": "Meditación guiada",
        "serie": serie["slug"],
    }

    meditacion = {
        "slug": serie["slug"],
        "titulo": serie["nombre"],
        "guia": guia,
        "descripcion": serie.get("descripcion", ""),
        "temas": serie.get("temas", []),
        "tipo": "guiada",
        "versiones": [version],
    }
    if serie.get("thumbnail"):
        meditacion["thumbnail"] = serie["thumbnail"]

    return meditacion


def clean_serie(serie):
    """Elimina el campo 'obra' de una serie."""
    s = copy.deepcopy(serie)
    s.pop("obra", None)
    return s


def migrate(data):
    serie_map = build_serie_map(data)
    canal_map = build_canal_map(data)

    # Recopilar slugs de series que pertenecen a alguna obra
    series_con_obra = set()
    for obra in data.get("obras", []):
        for v in obra.get("versiones", []):
            series_con_obra.add(v)

    # 1. Temas y canales sin cambios
    temas = data["temas"]
    canales = data["canales"]

    # 2. Series limpias (sin campo "obra")
    series = [clean_serie(s) for s in data["series"]]

    # 3. Obras → Libros
    libros = []
    for obra in data.get("obras", []):
        libro = obra_to_libro(obra, serie_map, canal_map)
        libros.append(libro)

    # 4. Grupos bilingües → Libros
    for group in BILINGUAL_GROUPS:
        libro = bilingual_group_to_libro(group, serie_map)
        libros.append(libro)

    # 5. Series independientes → Libros o Meditaciones
    meditaciones = []
    for serie in data["series"]:
        slug = serie["slug"]

        # Ya está en una obra
        if slug in series_con_obra:
            continue

        # Ya fue manejada como bilingüe
        if slug in BILINGUAL_SERIE_SLUGS:
            continue

        # Es meditación
        if slug in MEDITATION_SLUGS:
            med = serie_to_meditacion(serie)
            meditaciones.append(med)
            continue

        # Serie independiente → Libro
        libro = serie_independiente_to_libro(serie, canal_map)
        libros.append(libro)

    # Ordenar libros por tema principal, luego por autor, luego por titulo
    libros.sort(key=lambda l: (l["temas"][0] if l["temas"] else "", l["autor"].lower(), l["titulo"].lower()))

    # Ordenar meditaciones por titulo
    meditaciones.sort(key=lambda m: m["titulo"].lower())

    result = {
        "temas": temas,
        "canales": canales,
        "libros": libros,
        "meditaciones": meditaciones,
        "series": series,
    }

    return result


def main():
    print(f"Leyendo {INPUT}...")
    data = load_data()

    print(f"  Temas: {len(data['temas'])}")
    print(f"  Canales: {len(data['canales'])}")
    print(f"  Formatos: {len(data.get('formatos', []))}")
    print(f"  Obras: {len(data.get('obras', []))}")
    print(f"  Series: {len(data['series'])}")

    # Backup
    print(f"\nBackup → {BACKUP}")
    with open(BACKUP, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Migrar
    result = migrate(data)

    print(f"\nResultado:")
    print(f"  Temas: {len(result['temas'])}")
    print(f"  Canales: {len(result['canales'])}")
    print(f"  Libros: {len(result['libros'])}")
    print(f"  Meditaciones: {len(result['meditaciones'])}")
    print(f"  Series: {len(result['series'])}")

    # Escribir
    print(f"\nEscribiendo {OUTPUT}...")
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("¡Migración completada!")


if __name__ == "__main__":
    main()
