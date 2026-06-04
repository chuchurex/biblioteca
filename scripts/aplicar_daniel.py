#!/usr/bin/env python3
"""Aplica datos/daniel_disponibles.json a la serie/meditacion de Daniel en biblioteca.json."""

import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIBLIOTECA = os.path.join(ROOT_DIR, "src", "data", "biblioteca.json")
DISPONIBLES = os.path.join(ROOT_DIR, "datos", "daniel_disponibles.json")
SLUG = "sudja-meditacion-diaria-2026"
NUEVO_NOMBRE = "Vive Meditación Diariamente - Sudja Meditación"

with open(DISPONIBLES, "r", encoding="utf-8") as f:
    episodios = json.load(f)
with open(BIBLIOTECA, "r", encoding="utf-8") as f:
    data = json.load(f)

nuevo_thumb = episodios[0]["thumbnail"] if episodios else None

serie = next(s for s in data["series"] if s["slug"] == SLUG)
serie["nombre"] = NUEVO_NOMBRE
serie["episodios"] = episodios
if nuevo_thumb:
    serie["thumbnail"] = nuevo_thumb

med = next(m for m in data["meditaciones"] if m["slug"] == SLUG)
med["titulo"] = NUEVO_NOMBRE
if nuevo_thumb:
    med["thumbnail"] = nuevo_thumb

with open(BIBLIOTECA, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Serie actualizada: {len(episodios)} episodios (meditaciones >= 35 min)")
print(f"  thumbnail: {nuevo_thumb}")
