#!/usr/bin/env python3
"""
Verifica la disponibilidad de TODOS los videos del sitio contra la API de
YouTube y poda de src/data/biblioteca.json lo que ya no esta visible
(eliminado o en privado), manejando la cascada completa:

  episodio caido -> serie vacia -> edicion/version muerta -> libro/meditacion
  huerfano.

Reglas de seguridad:
  - No agrega videos nuevos (eso requiere curaduria manual): solo poda.
  - Un libro/meditacion que quedaria huerfano pero esta referenciado en una
    ruta de estudio NO se elimina: se reporta como conflicto para revision
    manual (evita romper la validacion build-time de rutas).
  - Repara thumbnails que apunten a un video caido.

Uso:
    python scripts/verificar_disponibilidad.py            # dry-run (no escribe)
    python scripts/verificar_disponibilidad.py --aplicar  # aplica cambios
"""

import json
import os
import re
import sys
import urllib.parse
import urllib.request

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_KEY = os.getenv("YOUTUBE_API_KEY")
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIBLIOTECA = os.path.join(ROOT_DIR, "src", "data", "biblioteca.json")
RUTAS = os.path.join(ROOT_DIR, "src", "data", "rutas.json")
THUMB_RE = re.compile(r"/vi/([^/]+)/")


def req(url):
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read())


def disponibles_set(video_ids):
    """Set de video_ids disponibles (public/unlisted) segun videos.list."""
    ok = set()
    ids = list(video_ids)
    for i in range(0, len(ids), 50):
        batch = ids[i:i + 50]
        url = "https://www.googleapis.com/youtube/v3/videos?" + urllib.parse.urlencode(
            {"part": "status", "id": ",".join(batch), "key": API_KEY})
        r = req(url)
        for it in r.get("items", []):
            if it["status"].get("privacyStatus") in ("public", "unlisted"):
                ok.add(it["id"])
    return ok


def thumb_video_id(thumb):
    if not thumb:
        return None
    m = THUMB_RE.search(thumb)
    return m.group(1) if m else None


def rutas_refs():
    """Slugs referenciados en pasos de rutas.json (campo 'ref')."""
    if not os.path.exists(RUTAS):
        return set()
    with open(RUTAS, "r", encoding="utf-8") as f:
        rutas = json.load(f)
    return {p.get("ref") for r in rutas for p in r.get("pasos", []) if p.get("ref")}


def main():
    aplicar = "--aplicar" in sys.argv
    if not API_KEY:
        print("Error: YOUTUBE_API_KEY no configurada")
        sys.exit(1)

    with open(BIBLIOTECA, "r", encoding="utf-8") as f:
        data = json.load(f)

    series = data.get("series", [])
    all_ids = {ep["video_id"] for s in series for ep in s.get("episodios", [])}
    print(f"Verificando {len(all_ids)} videos en {len(series)} series...")

    ok = disponibles_set(all_ids)
    caidos = all_ids - ok
    print(f"  disponibles: {len(ok)}  |  caidos: {len(caidos)}")

    # 1. Podar episodios caidos
    total_eliminados = 0
    series_afectadas = []
    for s in series:
        eliminados = [ep for ep in s.get("episodios", []) if ep["video_id"] in caidos]
        if eliminados:
            antes = len(s["episodios"])
            s["episodios"] = [ep for ep in s["episodios"] if ep["video_id"] in ok]
            total_eliminados += len(eliminados)
            series_afectadas.append((s["slug"], len(eliminados), antes, len(s["episodios"])))

    # 2. Series con/sin episodios
    series_vivas = {s["slug"] for s in series if s.get("episodios")}
    series_vacias = [s["slug"] for s in series if not s.get("episodios")]

    # 3. Limpiar ediciones/versiones que apuntan a series sin episodios
    for lib in data.get("libros", []):
        lib["ediciones"] = [e for e in lib.get("ediciones", []) if e["serie"] in series_vivas]
    for med in data.get("meditaciones", []):
        med["versiones"] = [v for v in med.get("versiones", []) if v["serie"] in series_vivas]

    # 4. Detectar huerfanos (sin ediciones/versiones vivas) y resolver conflictos con rutas
    refs = rutas_refs()
    conflictos = []
    libros_eliminados, meds_eliminadas = [], []

    nuevos_libros = []
    for lib in data.get("libros", []):
        if lib.get("ediciones"):
            nuevos_libros.append(lib)
        elif lib["slug"] in refs:
            conflictos.append(("libro", lib["slug"]))
            nuevos_libros.append(lib)  # se mantiene para no romper la ruta
        else:
            libros_eliminados.append(lib["slug"])
    data["libros"] = nuevos_libros

    nuevas_meds = []
    for med in data.get("meditaciones", []):
        if med.get("versiones"):
            nuevas_meds.append(med)
        elif med["slug"] in refs:
            conflictos.append(("meditacion", med["slug"]))
            nuevas_meds.append(med)
        else:
            meds_eliminadas.append(med["slug"])
    data["meditaciones"] = nuevas_meds

    # 5. Eliminar series vacias (salvo que sostengan un huerfano en conflicto)
    conflicto_slugs = {s for _, s in conflictos}
    series_protegidas = set()
    for lib in data["libros"]:
        if lib["slug"] in conflicto_slugs:
            series_protegidas |= {e["serie"] for e in lib.get("ediciones", [])}
    data["series"] = [s for s in series if s.get("episodios") or s["slug"] in series_protegidas]

    # 6. Reparar thumbnails caidos -> primer episodio disponible de su serie
    primer_ep = {s["slug"]: (s["episodios"][0]["video_id"] if s.get("episodios") else None)
                 for s in data["series"]}

    def fix_thumb(obj, serie_slug):
        vid = thumb_video_id(obj.get("thumbnail"))
        if vid and vid in caidos and primer_ep.get(serie_slug):
            obj["thumbnail"] = f"https://i.ytimg.com/vi/{primer_ep[serie_slug]}/hqdefault.jpg"
            return True
        return False

    thumbs = 0
    for s in data["series"]:
        thumbs += fix_thumb(s, s["slug"])
    for lib in data["libros"]:
        if lib.get("ediciones"):
            thumbs += fix_thumb(lib, lib["ediciones"][0]["serie"])
    for med in data["meditaciones"]:
        if med.get("versiones"):
            thumbs += fix_thumb(med, med["versiones"][0]["serie"])

    # Reporte
    if series_afectadas:
        print("\nSeries con videos eliminados:")
        for slug, n, antes, desp in series_afectadas:
            print(f"  - {slug}: -{n}  ({antes} -> {desp})")
    if libros_eliminados:
        print(f"\nLibros eliminados (huerfanos): {', '.join(libros_eliminados)}")
    if meds_eliminadas:
        print(f"Meditaciones eliminadas (huerfanas): {', '.join(meds_eliminadas)}")
    if conflictos:
        print("\nCONFLICTOS (huerfanos referenciados en rutas, revisar a mano):")
        for tipo, slug in conflictos:
            print(f"  - {tipo}: {slug}")

    print(f"\nResumen: {total_eliminados} episodios, {len(series_vacias)} series vacias, "
          f"{len(libros_eliminados)} libros, {len(meds_eliminadas)} meditaciones, "
          f"{thumbs} thumbnails reparados.")

    if not (total_eliminados or libros_eliminados or meds_eliminadas or thumbs):
        print("Sin cambios. Todo disponible.")
        return

    if aplicar:
        with open(BIBLIOTECA, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("\nAplicado a biblioteca.json")
    else:
        print("\nDry-run. Ejecuta con --aplicar para guardar.")


if __name__ == "__main__":
    main()
