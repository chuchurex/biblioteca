#!/usr/bin/env python3
"""
Obtiene estadisticas de vistas de los videos de todos los canales
y agrega datos de vistas, likes, comentarios y embeddable a cada episodio.
"""

import json
import urllib.request
import urllib.parse
import os
import sys
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS_DIR = os.path.join(ROOT_DIR, "datos")
INPUT_FILE = os.path.join(DATOS_DIR, "biblioteca_canales.json")


def make_request(url):
    """Hace una peticion a la API de YouTube"""
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read())
    except Exception as e:
        print(f"Error en peticion: {e}")
        return None


def get_video_stats(video_ids):
    """Obtiene estadisticas y estado de embed de videos en lotes de 50"""
    stats = {}

    for i in range(0, len(video_ids), 50):
        batch = video_ids[i : i + 50]
        params = {
            "part": "statistics,status",
            "id": ",".join(batch),
            "key": API_KEY,
        }
        url = f"https://www.googleapis.com/youtube/v3/videos?{urllib.parse.urlencode(params)}"
        response = make_request(url)

        if response:
            for item in response.get("items", []):
                video_id = item["id"]
                views = int(item["statistics"].get("viewCount", 0))
                likes = int(item["statistics"].get("likeCount", 0))
                comments = int(item["statistics"].get("commentCount", 0))
                embeddable = item.get("status", {}).get("embeddable", True)
                stats[video_id] = {
                    "vistas": views,
                    "likes": likes,
                    "comentarios": comments,
                    "embeddable": embeddable,
                }

    return stats


def main():
    print("=" * 60)
    print("  Estadisticas Multi-Canal — Biblioteca")
    print("=" * 60)

    if not API_KEY:
        print("Error: YOUTUBE_API_KEY no configurada en .env")
        sys.exit(1)

    if not os.path.exists(INPUT_FILE):
        print(f"Error: No se encontro {INPUT_FILE}")
        print("Ejecuta primero: python scripts/youtube_extractor.py")
        sys.exit(1)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        canales = json.load(f)

    # Recolectar todos los video IDs
    all_video_ids = []
    for canal in canales:
        for programa in canal["programas"]:
            for ep in programa["episodios"]:
                vid = ep.get("video_id")
                if vid:
                    all_video_ids.append(vid)

    print(f"Total videos a consultar: {len(all_video_ids)}")
    print("Obteniendo estadisticas (en lotes de 50)...")

    stats = get_video_stats(all_video_ids)
    print(f"Estadisticas obtenidas: {len(stats)} videos")

    # Agregar stats a cada episodio
    blocked_count = 0
    for canal in canales:
        for programa in canal["programas"]:
            for ep in programa["episodios"]:
                vid = ep.get("video_id")
                if vid and vid in stats:
                    ep["vistas"] = stats[vid]["vistas"]
                    ep["likes"] = stats[vid]["likes"]
                    ep["comentarios"] = stats[vid]["comentarios"]
                    ep["embeddable"] = stats[vid]["embeddable"]
                    if not stats[vid]["embeddable"]:
                        blocked_count += 1
                else:
                    ep["vistas"] = 0
                    ep["likes"] = 0
                    ep["comentarios"] = 0
                    ep["embeddable"] = True

    if blocked_count > 0:
        print(f"  ATENCION: {blocked_count} video(s) bloqueados para embed")

    # Guardar con estadisticas
    with open(INPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(canales, f, ensure_ascii=False, indent=2)
    print(f"  Guardado: {INPUT_FILE}")

    # Top videos
    print()
    todos_episodios = []
    for canal in canales:
        for programa in canal["programas"]:
            for ep in programa["episodios"]:
                if ep.get("vistas", 0) > 0:
                    todos_episodios.append(
                        {
                            "titulo": ep["titulo"],
                            "vistas": ep["vistas"],
                            "canal": canal["canal"],
                        }
                    )

    todos_episodios.sort(key=lambda x: x["vistas"], reverse=True)
    print("  TOP 10 VIDEOS MAS VISTOS:")
    for i, ep in enumerate(todos_episodios[:10], 1):
        print(f"    {i}. {ep['titulo'][:50]}")
        print(f"       {ep['vistas']:,} vistas | {ep['canal']}")

    print()
    print("  Estadisticas completadas.")
    print("=" * 60)


if __name__ == "__main__":
    main()
