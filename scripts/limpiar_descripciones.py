#!/usr/bin/env python3
"""
Limpia las descripciones de episodios eliminando boilerplate repetitivo.
Usa patrones base comunes + patrones específicos por canal desde canales.json.
Se ejecuta como paso del pipeline después de obtener_estadisticas.py.
"""

import json
import re
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS_DIR = os.path.join(ROOT_DIR, "datos")
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = os.path.join(DATOS_DIR, "biblioteca_canales.json")
CANALES_FILE = os.path.join(SCRIPTS_DIR, "canales.json")

# Patrones base comunes a todos los canales
BASE_PATTERNS = [
    # URLs
    r"https?://\S+",
    # Hashtags sueltos
    r"^#\w+(\s+#\w+)*$",
    # Suscripción genérica
    r"^Suscr[ií]b[iaeo]n?[st]e.*",
    r"^Subscribe.*",
    # Redes genéricas
    r"^(Síguenos|Seguinos|Follow us).*",
]


def build_patterns(canal_slug, canales_config):
    """Construye los patrones compilados para un canal"""
    patterns = [re.compile(p, re.IGNORECASE) for p in BASE_PATTERNS]

    # Buscar patrones específicos del canal
    for config in canales_config:
        if config["slug"] == canal_slug:
            for p in config.get("patronesLimpieza", []):
                patterns.append(re.compile(p, re.IGNORECASE))
            break

    return patterns


def clean_description(desc, patterns):
    if not desc:
        return desc

    lines = desc.split("\n")
    cleaned = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            cleaned.append("")
            continue

        should_remove = any(pat.search(stripped) for pat in patterns)
        if not should_remove:
            cleaned.append(line)

    # Trim trailing/leading empty lines
    while cleaned and not cleaned[-1].strip():
        cleaned.pop()
    while cleaned and not cleaned[0].strip():
        cleaned.pop(0)

    # Collapse 3+ consecutive empty lines into 2
    result = []
    empty_count = 0
    for line in cleaned:
        if not line.strip():
            empty_count += 1
            if empty_count <= 2:
                result.append(line)
        else:
            empty_count = 0
            result.append(line)

    return "\n".join(result)


def main():
    if not os.path.exists(INPUT_FILE):
        print(f"No se encontro {INPUT_FILE}")
        sys.exit(1)

    # Cargar config de canales para patrones
    canales_config = []
    if os.path.exists(CANALES_FILE):
        with open(CANALES_FILE, "r", encoding="utf-8") as f:
            canales_config = json.load(f)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        canales = json.load(f)

    total = 0
    cleaned_count = 0

    for canal in canales:
        patterns = build_patterns(canal["canal_slug"], canales_config)
        for programa in canal["programas"]:
            for ep in programa["episodios"]:
                total += 1
                original = ep.get("descripcion", "")
                cleaned = clean_description(original, patterns)
                if cleaned != original:
                    cleaned_count += 1
                    ep["descripcion"] = cleaned

    with open(INPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(canales, f, ensure_ascii=False, indent=2)

    print(f"Descripciones procesadas: {total}")
    print(f"Limpiadas: {cleaned_count}")


if __name__ == "__main__":
    main()
