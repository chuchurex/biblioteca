"""Investigación: buscar en YouTube todos los videos de Claudio Naranjo.

Usa search.list con varias queries y paginación, deduplica por video_id,
enriquece con videos.list (duración, vistas, embeddable) y guarda JSON.
"""
import json
import os
import time
import urllib.parse
import urllib.request

API_KEY = None
with open(os.path.join(os.path.dirname(__file__), "..", ".env")) as f:
    for line in f:
        if line.startswith("YOUTUBE_API_KEY"):
            API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
            break

BASE = "https://www.googleapis.com/youtube/v3"

QUERIES = [
    "Claudio Naranjo",
    "Claudio Naranjo entrevista",
    "Claudio Naranjo conferencia",
    "Claudio Naranjo eneagrama",
    "Claudio Naranjo gestalt",
    "Claudio Naranjo educación",
    "Claudio Naranjo documental",
    "Claudio Naranjo SAT",
    "Claudio Naranjo meditación",
    "Claudio Naranjo psicología de los eneatipos",
]


def get(endpoint, **params):
    params["key"] = API_KEY
    url = f"{BASE}/{endpoint}?{urllib.parse.urlencode(params)}"
    for intento in range(6):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            if e.code in (403, 429):
                raise SystemExit(f"Cuota/permiso: {e.code} {body[:300]}")
            if intento == 5:
                raise SystemExit(f"HTTP {e.code}: {body[:300]}")
            time.sleep(2 * (intento + 1))
        except (urllib.error.URLError, OSError) as e:
            if intento == 5:
                raise SystemExit(f"Error de red persistente: {e}")
            time.sleep(2 * (intento + 1))


videos = {}
for q in QUERIES:
    page_token = None
    paginas = 0
    while True:
        params = dict(part="snippet", q=q, type="video", maxResults=50,
                      relevanceLanguage="es")
        if page_token:
            params["pageToken"] = page_token
        data = get("search", **params)
        for item in data.get("items", []):
            vid = item["id"]["videoId"]
            if vid in videos:
                continue
            s = item["snippet"]
            videos[vid] = {
                "video_id": vid,
                "titulo": s["title"],
                "canal": s["channelTitle"],
                "channel_id": s["channelId"],
                "fecha": s["publishedAt"][:10],
                "descripcion": s.get("description", ""),
            }
        page_token = data.get("nextPageToken")
        paginas += 1
        if not page_token or paginas >= 4:  # máx 200 resultados por query
            break
    print(f"  '{q}': acumulado {len(videos)} videos únicos")

# Enriquecer con duración, vistas y embeddable
ids = list(videos.keys())
for i in range(0, len(ids), 50):
    lote = ids[i:i + 50]
    data = get("videos", part="contentDetails,statistics,status",
               id=",".join(lote))
    for item in data.get("items", []):
        v = videos.get(item["id"])
        if not v:
            continue
        v["duracion"] = item["contentDetails"].get("duration", "")
        v["vistas"] = int(item["statistics"].get("viewCount", 0))
        v["embeddable"] = item["status"].get("embeddable", False)

out = os.path.join(os.path.dirname(__file__), "..", "datos",
                   "investigacion_claudio_naranjo.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w") as f:
    json.dump(sorted(videos.values(), key=lambda v: -v.get("vistas", 0)),
              f, ensure_ascii=False, indent=2)
print(f"\nTotal: {len(videos)} videos únicos -> {out}")

# Resumen por canal
canales = {}
for v in videos.values():
    c = canales.setdefault(v["canal"], {"n": 0, "vistas": 0})
    c["n"] += 1
    c["vistas"] += v.get("vistas", 0)
print("\nTop 25 canales por cantidad de videos:")
for nombre, c in sorted(canales.items(), key=lambda x: -x[1]["n"])[:25]:
    print(f"  {c['n']:4d} videos | {c['vistas']:>12,} vistas | {nombre}")
