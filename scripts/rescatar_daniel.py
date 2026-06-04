#!/usr/bin/env python3
"""
Rescata las meditaciones disponibles de Daniel Miccael Sais desde la playlist
"VIVE MEDITACION DIARIAMENTE", saltando videos eliminados/privados, y verifica
disponibilidad real contra videos.list (status).

Genera datos/daniel_disponibles.json con los episodios disponibles en el formato
de la serie de biblioteca.json. No modifica biblioteca.json (eso es paso aparte).
"""

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
PLAYLIST_ID = "PLMb586Jx16enUZduxpPXqMG-AeBawUeB9"  # VIVE MEDITACION DIARIAMENTE
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_FILE = os.path.join(ROOT_DIR, "datos", "daniel_disponibles.json")


def req(url):
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read())


def parse_date(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except Exception:
        return s


def fetch_playlist(playlist_id):
    """Items de la playlist saltando eliminados/privados por titulo."""
    items = []
    token = None
    while True:
        p = {"part": "snippet,contentDetails", "playlistId": playlist_id,
             "maxResults": "50", "key": API_KEY}
        if token:
            p["pageToken"] = token
        r = req("https://www.googleapis.com/youtube/v3/playlistItems?" + urllib.parse.urlencode(p))
        for it in r.get("items", []):
            title = it["snippet"]["title"]
            if title in ("Deleted video", "Private video"):
                continue
            cd = it["contentDetails"]
            items.append({
                "video_id": cd["videoId"],
                "titulo": title,
                "descripcion": it["snippet"].get("description", ""),
                "fecha": parse_date(cd.get("videoPublishedAt") or it["snippet"]["publishedAt"]),
                "thumb": it["snippet"]["thumbnails"].get("high",
                          it["snippet"]["thumbnails"].get("default", {})).get("url", ""),
            })
        token = r.get("nextPageToken")
        if not token:
            break
    return items


def parse_duration(iso):
    """PT#H#M#S -> segundos."""
    h = m = s = 0
    num = ""
    for ch in iso.replace("PT", ""):
        if ch.isdigit():
            num += ch
        elif ch == "H":
            h = int(num); num = ""
        elif ch == "M":
            m = int(num); num = ""
        elif ch == "S":
            s = int(num); num = ""
    return h * 3600 + m * 60 + s


def verify_available(video_ids):
    """videos.list -> dict {id: duracion_seg} de ids disponibles (public/unlisted)."""
    info = {}
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]
        url = "https://www.googleapis.com/youtube/v3/videos?" + urllib.parse.urlencode(
            {"part": "status,contentDetails", "id": ",".join(batch), "key": API_KEY})
        r = req(url)
        for it in r.get("items", []):
            if it["status"].get("privacyStatus") in ("public", "unlisted"):
                info[it["id"]] = parse_duration(it["contentDetails"]["duration"])
    return info


def main():
    if not API_KEY:
        raise SystemExit("YOUTUBE_API_KEY no configurada")

    print("Extrayendo playlist VIVE MEDITACION DIARIAMENTE...")
    raw = fetch_playlist(PLAYLIST_ID)
    print(f"  items no marcados como deleted/private: {len(raw)}")

    # Dedup por video_id
    by_id = {}
    for it in raw:
        by_id.setdefault(it["video_id"], it)
    print(f"  unicos: {len(by_id)}")

    print("Verificando disponibilidad y duracion contra videos.list...")
    info = verify_available(list(by_id.keys()))
    disponibles_all = [it for vid, it in by_id.items() if vid in info]
    print(f"  disponibles confirmados: {len(disponibles_all)}")

    # Filtrar por duracion: meditaciones son >= 35 min
    MIN_SEG = 35 * 60
    disponibles = [it for it in disponibles_all if info[it["video_id"]] >= MIN_SEG]
    descartados = len(disponibles_all) - len(disponibles)
    print(f"  descartados por durar < 35 min: {descartados}")
    print(f"  meditaciones (>= 35 min): {len(disponibles)}")

    # Distribucion por año
    por_anio = {}
    for it in disponibles:
        anio = it["fecha"][:4]
        por_anio[anio] = por_anio.get(anio, 0) + 1
    print("\nDistribucion por año:")
    for anio in sorted(por_anio):
        print(f"  {anio}: {por_anio[anio]}")

    # Convertir a formato de episodio de la serie y ordenar por fecha desc
    episodios = [{
        "video_id": it["video_id"],
        "titulo": it["titulo"],
        "url": f"https://www.youtube.com/watch?v={it['video_id']}",
        "fecha_emision": it["fecha"],
        "thumbnail": it["thumb"],
        "descripcion": it["descripcion"],
    } for it in disponibles]
    episodios.sort(key=lambda x: x["fecha_emision"], reverse=True)

    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(episodios, f, ensure_ascii=False, indent=2)
    print(f"\nGuardado: {OUT_FILE} ({len(episodios)} episodios)")


if __name__ == "__main__":
    main()
