#!/usr/bin/env python3
"""
Resuelve Channel IDs de YouTube a partir de handles.
Puede resolver un handle específico por argumento o todos los canales de canales.json.
"""

import json
import sys
import urllib.request
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
CANALES_FILE = os.path.join(SCRIPTS_DIR, "canales.json")


def make_request(url):
    """Hace una peticion a la API de YouTube"""
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read())
    except Exception as e:
        print(f"Error en peticion: {e}")
        return None


def resolver_channel_id(handle):
    """Resuelve un handle de YouTube (@nombre) a un Channel ID"""
    params = {
        "part": "snippet,contentDetails",
        "forHandle": handle,
        "key": API_KEY,
    }

    url = f"https://www.googleapis.com/youtube/v3/channels?{urllib.parse.urlencode(params)}"
    data = make_request(url)

    if not data or not data.get("items"):
        print(f"  No se encontro canal con handle: @{handle}")
        return None

    canal = data["items"][0]
    channel_id = canal["id"]
    nombre = canal["snippet"]["title"]
    uploads_playlist = canal["contentDetails"]["relatedPlaylists"]["uploads"]

    print(f"  Canal: {nombre}")
    print(f"  Channel ID: {channel_id}")
    print(f"  Uploads Playlist ID: {uploads_playlist}")

    return {
        "channel_id": channel_id,
        "nombre": nombre,
        "uploads_playlist_id": uploads_playlist,
    }


def main():
    if not API_KEY:
        print("Error: YOUTUBE_API_KEY no configurada en .env")
        sys.exit(1)

    # Si se pasa un handle como argumento, resolver solo ese
    if len(sys.argv) > 1:
        handle = sys.argv[1].lstrip("@")
        print(f"Resolviendo Channel ID para @{handle}...\n")
        result = resolver_channel_id(handle)
        if result:
            print(f"\nAgrega a canales.json:")
            print(f'  "channelId": "{result["channel_id"]}"')
        return

    # Sin argumento: resolver todos los canales de canales.json
    if not os.path.exists(CANALES_FILE):
        print(f"Error: No se encontro {CANALES_FILE}")
        sys.exit(1)

    with open(CANALES_FILE, "r", encoding="utf-8") as f:
        canales = json.load(f)

    actualizados = 0
    for canal in canales:
        if not canal.get("activo", True):
            continue

        if canal.get("channelId"):
            print(f"@{canal['handle']}: ya tiene channelId ({canal['channelId']})")
            continue

        print(f"Resolviendo @{canal['handle']}...")
        result = resolver_channel_id(canal["handle"])
        if result:
            canal["channelId"] = result["channel_id"]
            actualizados += 1
        print()

    if actualizados > 0:
        with open(CANALES_FILE, "w", encoding="utf-8") as f:
            json.dump(canales, f, ensure_ascii=False, indent=2)
        print(f"\n{actualizados} canal(es) actualizado(s) en canales.json")
    else:
        print("\nTodos los canales ya tienen channelId.")


if __name__ == "__main__":
    main()
