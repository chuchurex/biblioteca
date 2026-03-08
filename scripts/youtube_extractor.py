#!/usr/bin/env python3
"""
Extractor multi-canal de datos de YouTube.
Itera sobre los canales definidos en canales.json, obtiene playlists y episodios,
y genera datos/biblioteca_canales.json con la estructura completa.
"""

import json
import urllib.request
import urllib.parse
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPTS_DIR)
DATOS_DIR = os.path.join(ROOT_DIR, "datos")
CANALES_FILE = os.path.join(SCRIPTS_DIR, "canales.json")

os.makedirs(DATOS_DIR, exist_ok=True)


def make_request(url):
    """Hace una peticion a la API de YouTube"""
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read())
    except Exception as e:
        print(f"Error en peticion: {e}")
        return None


def get_channel_info(channel_id):
    """Obtiene informacion basica del canal"""
    params = {
        "part": "snippet,statistics,contentDetails",
        "id": channel_id,
        "key": API_KEY,
    }
    url = f"https://www.googleapis.com/youtube/v3/channels?{urllib.parse.urlencode(params)}"
    response = make_request(url)

    if response and response.get("items"):
        canal = response["items"][0]
        return {
            "nombre": canal["snippet"]["title"],
            "suscriptores": int(canal["statistics"].get("subscriberCount", "0")),
            "total_videos": canal["statistics"].get("videoCount", "0"),
            "uploads_playlist": canal["contentDetails"]["relatedPlaylists"]["uploads"],
        }
    return None


def get_all_playlists(channel_id):
    """Obtiene todas las playlists del canal"""
    playlists = []
    next_page_token = None

    while True:
        params = {
            "part": "snippet,contentDetails",
            "channelId": channel_id,
            "maxResults": "50",
            "key": API_KEY,
        }

        if next_page_token:
            params["pageToken"] = next_page_token

        url = f"https://www.googleapis.com/youtube/v3/playlists?{urllib.parse.urlencode(params)}"
        response = make_request(url)

        if not response:
            break

        items = response.get("items", [])
        if not items and not next_page_token:
            break

        for item in items:
            playlist_info = {
                "id": item["id"],
                "nombre": item["snippet"]["title"],
                "descripcion": item["snippet"].get("description", ""),
                "fecha_creacion": item["snippet"]["publishedAt"],
                "total_videos": item["contentDetails"]["itemCount"],
                "thumbnail": item["snippet"]["thumbnails"]
                .get("high", item["snippet"]["thumbnails"].get("default", {}))
                .get("url", ""),
            }
            playlists.append(playlist_info)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return playlists


def get_playlist_videos(playlist_id):
    """Obtiene todos los videos de una playlist"""
    videos = []
    next_page_token = None

    while True:
        params = {
            "part": "snippet,contentDetails",
            "playlistId": playlist_id,
            "maxResults": "50",
            "key": API_KEY,
        }

        if next_page_token:
            params["pageToken"] = next_page_token

        url = f"https://www.googleapis.com/youtube/v3/playlistItems?{urllib.parse.urlencode(params)}"
        response = make_request(url)

        if not response:
            break

        for item in response.get("items", []):
            if item["snippet"]["title"] in ["Deleted video", "Private video"]:
                continue

            video_info = {
                "video_id": item["contentDetails"]["videoId"],
                "titulo": item["snippet"]["title"],
                "descripcion": item["snippet"].get("description", ""),
                "fecha_publicacion": item["snippet"]["publishedAt"],
                "url": f"https://www.youtube.com/watch?v={item['contentDetails']['videoId']}",
                "thumbnail": item["snippet"]["thumbnails"]
                .get("high", item["snippet"]["thumbnails"].get("default", {}))
                .get("url", ""),
            }
            videos.append(video_info)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return videos


def parse_date(date_string):
    """Convierte fecha ISO a formato YYYY-MM-DD"""
    try:
        dt = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except:
        return date_string


def process_channel(canal_config):
    """Procesa un canal completo y retorna su estructura de datos"""
    channel_id = canal_config["channelId"]
    slug = canal_config["slug"]
    handle = canal_config.get("handle", "")
    nombre = canal_config.get("nombre", handle or slug)

    print(f"\n{'='*60}")
    print(f"  Canal: {nombre}")
    print(f"{'='*60}")

    # Info del canal
    print("  Obteniendo info del canal...")
    canal_info = get_channel_info(channel_id)
    if not canal_info:
        print("  Error: No se pudo obtener info del canal")
        return None

    print(f"  Nombre: {canal_info['nombre']}")
    print(f"  Suscriptores: {canal_info['suscriptores']}")

    # Playlists
    print("  Obteniendo playlists...")
    playlists = get_all_playlists(channel_id)
    print(f"  Se encontraron {len(playlists)} playlists")

    # Procesar cada playlist
    programas = []
    for i, playlist in enumerate(playlists, 1):
        print(
            f"    [{i}/{len(playlists)}] {playlist['nombre']}... ", end="", flush=True
        )
        videos = get_playlist_videos(playlist["id"])

        programa = {
            "programa": playlist["nombre"],
            "playlist_id": playlist["id"],
            "descripcion": playlist["descripcion"],
            "total_episodios": len(videos),
            "fecha_creacion": parse_date(playlist["fecha_creacion"]),
            "thumbnail_programa": playlist["thumbnail"],
            "episodios": [],
        }

        for video in videos:
            episodio = {
                "video_id": video["video_id"],
                "titulo": video["titulo"],
                "url": video["url"],
                "fecha_emision": parse_date(video["fecha_publicacion"]),
                "thumbnail": video["thumbnail"],
                "descripcion": video["descripcion"],
            }
            programa["episodios"].append(episodio)

        # Ordenar episodios por fecha (mas reciente primero)
        programa["episodios"].sort(key=lambda x: x["fecha_emision"], reverse=True)

        if programa["episodios"]:
            programa["ultimo_episodio"] = programa["episodios"][0]["fecha_emision"]
        else:
            programa["ultimo_episodio"] = "1900-01-01"

        programas.append(programa)
        print(f"{len(videos)} videos")

    # Ordenar programas por ultimo episodio
    programas.sort(key=lambda x: x.get("ultimo_episodio", ""), reverse=True)

    return {
        "canal": canal_config.get("nombre", canal_info["nombre"]),
        "canal_id": channel_id,
        "canal_slug": slug,
        "canal_handle": handle or canal_info["nombre"],
        "suscriptores": canal_info["suscriptores"],
        "programas": programas,
    }


def main():
    print("=" * 60)
    print("  Extractor Multi-Canal — Biblioteca")
    print("=" * 60)

    if not API_KEY:
        print("Error: YOUTUBE_API_KEY no configurada en .env")
        sys.exit(1)

    if not os.path.exists(CANALES_FILE):
        print(f"Error: No se encontro {CANALES_FILE}")
        sys.exit(1)

    with open(CANALES_FILE, "r", encoding="utf-8") as f:
        canales_config = json.load(f)

    activos = [c for c in canales_config if c.get("activo", True) and c.get("channelId")]
    if not activos:
        print("No hay canales activos con channelId configurado.")
        print("Ejecuta primero: python scripts/resolver_channel_id.py")
        sys.exit(1)

    print(f"Canales a procesar: {len(activos)}")

    # Procesar cada canal
    resultado = []
    for canal_config in activos:
        canal_data = process_channel(canal_config)
        if canal_data:
            resultado.append(canal_data)

    # Exportar
    print(f"\n{'='*60}")
    print("  Exportando datos...")

    output_file = os.path.join(DATOS_DIR, "biblioteca_canales.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print(f"  Guardado: {output_file}")

    # Resumen
    total_programas = sum(len(c["programas"]) for c in resultado)
    total_episodios = sum(
        sum(p["total_episodios"] for p in c["programas"]) for c in resultado
    )

    print(f"\n  RESUMEN:")
    print(f"  Canales: {len(resultado)}")
    print(f"  Programas: {total_programas}")
    print(f"  Episodios: {total_episodios}")
    print("=" * 60)


if __name__ == "__main__":
    main()
