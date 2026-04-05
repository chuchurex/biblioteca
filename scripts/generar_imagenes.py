"""
Generador de imagenes para chuchurex.cl via Gemini API.

Genera imagenes para temas y rutas de estudio que no tienen thumbnail.
Usa Gemini 2.5 Flash (imagen) o el modelo que este disponible.

Requisitos:
  pip install google-genai Pillow

Uso:
  export GEMINI_API_KEY=tu_clave
  python scripts/generar_imagenes.py                  # genera todas las faltantes
  python scripts/generar_imagenes.py --solo temas     # solo temas
  python scripts/generar_imagenes.py --solo rutas     # solo rutas
  python scripts/generar_imagenes.py --slug ayurveda  # una sola imagen
  python scripts/generar_imagenes.py --listar         # solo muestra prompts, no genera
"""

import json
import os
import sys
import argparse
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BIBLIOTECA_JSON = PROJECT_ROOT / "src" / "data" / "biblioteca.json"
RUTAS_JSON = PROJECT_ROOT / "src" / "data" / "rutas.json"
OUTPUT_DIR = PROJECT_ROOT / "public" / "images"

# Modelo Gemini para generacion de imagenes
# Opciones: gemini-2.0-flash-exp, gemini-2.5-flash-preview-04-17
# Si falla, probar con el otro
MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.0-flash-exp")

# Estilo base para todas las imagenes (coherencia visual)
STYLE_PREFIX = (
    "Dark moody cinematic illustration, minimal and elegant. "
    "Color palette: deep black (#0C0C0E) background, warm gold (#E8B04A) accents, "
    "cream (#F0EDE8) highlights. Atmospheric lighting, subtle grain texture. "
    "No text, no words, no letters, no watermarks. "
    "Aspect ratio 16:9, high quality. "
)

# ---------------------------------------------------------------------------
# Prompts para cada tema
# ---------------------------------------------------------------------------

TEMA_PROMPTS: dict[str, str] = {
    "ley-del-uno": (
        "A radiant golden octahedron floating in deep space, emanating concentric "
        "rings of light. Subtle nebula in the background with warm gold and cream tones. "
        "Represents cosmic unity and the Law of One. Mystical, transcendent atmosphere."
    ),
    "antroposofia": (
        "An ethereal tree of life with luminous golden roots extending into dark earth "
        "and branches reaching into a starry cosmos. A single human silhouette stands "
        "at the base, arms slightly raised. Organic forms, biodynamic feeling. "
        "Represents Rudolf Steiner's spiritual science."
    ),
    "chamanismo-tolteca": (
        "A desert landscape at twilight with a lone cactus silhouette against a deep "
        "dark sky. A golden eagle soars overhead leaving a trail of luminous particles. "
        "A subtle portal of light opens in the distance. Nagual energy, Castaneda's world. "
        "Mystical Mexican desert atmosphere."
    ),
    "cuarto-camino": (
        "The Enneagram symbol, the well-known nine-pointed geometric figure used "
        "in the Fourth Way tradition of Gurdjieff and Ouspensky. Golden lines on "
        "black background. A single candle flame at the center. "
        "Sacred geometry, inner work."
    ),
    "astrologia": (
        "A celestial natal chart rendered in golden lines against a dark cosmic "
        "background. Zodiac constellations shimmer faintly. Saturn prominently visible "
        "with its rings catching golden light. Birth chart as map of the soul. "
        "Evolutionary astrology atmosphere."
    ),
    "hermetismo": (
        "The Flower of Life sacred geometry pattern in luminous gold on dark background. "
        "Overlaid with the Hermetic caduceus symbol. Subtle alchemical symbols float "
        "in the periphery. Sacred geometry, as above so below. "
        "Ancient wisdom, esoteric knowledge."
    ),
    "consciencia": (
        "A human silhouette seated in meditation, dissolving into particles of golden "
        "light that merge with infinite dark space. The boundary between self and cosmos "
        "is blurred. Non-dual awareness. No separation between observer and observed. "
        "Serene, vast, awake."
    ),
    "ayurveda": (
        "Three flowing streams of energy in gold, warm copper, and cool cream "
        "intertwining in a spiral pattern against a dark background. Subtle botanical "
        "elements (herbs, leaves) float around. Represents the three doshas: "
        "Vata, Pitta, Kapha. Ancient Indian healing wisdom."
    ),
    "lobsang-rampa": (
        "The Potala Palace silhouette against a dark Himalayan sky. A luminous third eye "
        "symbol glows in warm gold above the palace. Prayer flags catch faint light. "
        "Tibetan mysticism, monastic life, ancient wisdom. "
        "The mountains are vast and the sky is infinite."
    ),
}

# ---------------------------------------------------------------------------
# Prompts para cada ruta de estudio
# ---------------------------------------------------------------------------

RUTA_PROMPTS: dict[str, str] = {
    "camino-guerrero-tolteca": (
        "A warrior's path through a mystical desert at night. Golden footprints "
        "lead toward a distant luminous crack in reality. A nagual's double walks "
        "ahead as a shadow. Peyote cacti glow faintly. Five stepping stones mark "
        "the path. Toltec warrior's journey of perception."
    ),
    "introduccion-consciencia": (
        "A spiral staircase of golden light ascending through layers of dark space. "
        "Each step becomes more transparent, more luminous. At the top, pure awareness "
        "as a soft golden glow. The journey from sleep to awakening. "
        "Beginner's path to consciousness."
    ),
    "astrologia-carta-natal": (
        "Hands holding a luminous circular natal chart that radiates golden light. "
        "The chart projects zodiac symbols into the surrounding darkness. "
        "A personal map of the cosmos. Self-discovery through the stars. "
        "Intimate, personal, revelatory."
    ),
    "fundamentos-antroposofia": (
        "An open golden book floating in dark space, its pages radiating light. "
        "From the book emerges a vision of the threefold human: thinking (head, gold), "
        "feeling (heart, warm copper), willing (limbs, cream). "
        "Rudolf Steiner's foundational teachings. Entry point to spiritual science."
    ),
    "evangelios-steiner": (
        "Four luminous golden streams converging from the four cardinal directions "
        "into a central point of brilliant light. Each stream has a distinct character "
        "but they unite. Dark atmospheric background. "
        "The four Gospels as esoteric documents. Steiner's Christology."
    ),
    "vida-muerte-steiner": (
        "A golden threshold between two worlds: on one side, earthly life as a faint "
        "landscape; on the other, luminous spiritual realms with subtle forms. "
        "A soul passes through as a stream of golden light. "
        "The journey between incarnations. Life, death, and beyond."
    ),
}

# ---------------------------------------------------------------------------
# Generador
# ---------------------------------------------------------------------------

def get_client():
    """Inicializa el cliente de Gemini."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY no esta definida.")
        print("  export GEMINI_API_KEY=tu_clave")
        sys.exit(1)

    try:
        from google import genai
        return genai.Client(api_key=api_key)
    except ImportError:
        print("Error: falta el paquete google-genai")
        print("  pip install google-genai Pillow")
        sys.exit(1)


def generar_imagen(client, slug: str, prompt: str, output_path: Path, model: str = MODEL):
    """Genera una imagen con Gemini y la guarda en output_path."""
    full_prompt = STYLE_PREFIX + prompt

    print(f"  Generando: {slug}")
    print(f"    Modelo: {model}")
    print(f"    Destino: {output_path}")

    try:
        response = client.models.generate_content(
            model=model,
            contents=[full_prompt],
            config={
                "response_modalities": ["image", "text"],
            },
        )

        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data is not None:
                # Guardar imagen
                output_path.parent.mkdir(parents=True, exist_ok=True)

                import base64
                image_bytes = part.inline_data.data
                if isinstance(image_bytes, str):
                    image_bytes = base64.b64decode(image_bytes)

                with open(output_path, 'wb') as f:
                    f.write(image_bytes)

                print(f"    OK ({output_path.stat().st_size // 1024} KB)")
                return True

        print(f"    WARN: respuesta sin imagen")
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text') and part.text:
                    print(f"    Texto: {part.text[:200]}")
        return False

    except Exception as e:
        print(f"    ERROR: {e}")
        return False


def listar_prompts(items: dict[str, str], categoria: str):
    """Muestra los prompts sin generar."""
    print(f"\n{'='*60}")
    print(f"  {categoria} ({len(items)} imagenes)")
    print(f"{'='*60}")
    for slug, prompt in items.items():
        print(f"\n--- {slug} ---")
        print(f"Prompt: {STYLE_PREFIX}{prompt}")


def main():
    parser = argparse.ArgumentParser(description="Genera imagenes para chuchurex.cl via Gemini API")
    parser.add_argument("--solo", choices=["temas", "rutas"], help="Generar solo temas o rutas")
    parser.add_argument("--slug", help="Generar solo un slug especifico")
    parser.add_argument("--listar", action="store_true", help="Solo mostrar prompts, no generar")
    parser.add_argument("--modelo", default=MODEL, help=f"Modelo Gemini (default: {MODEL})")
    parser.add_argument("--forzar", action="store_true", help="Regenerar aunque ya exista")
    args = parser.parse_args()

    # Construir lista de trabajo
    trabajo: list[tuple[str, str, Path]] = []

    if args.solo != "rutas":
        for slug, prompt in TEMA_PROMPTS.items():
            if args.slug and slug != args.slug:
                continue
            path = OUTPUT_DIR / "temas" / f"{slug}.webp"
            trabajo.append((slug, prompt, path))

    if args.solo != "temas":
        for slug, prompt in RUTA_PROMPTS.items():
            if args.slug and slug != args.slug:
                continue
            path = OUTPUT_DIR / "rutas" / f"{slug}.webp"
            trabajo.append((slug, prompt, path))

    if not trabajo:
        print(f"No hay imagenes para generar (slug '{args.slug}' no encontrado)")
        return

    # Modo listar
    if args.listar:
        for slug, prompt, path in trabajo:
            exists = " [existe]" if path.exists() else ""
            print(f"\n--- {slug}{exists} ---")
            print(f"  Archivo: {path.relative_to(PROJECT_ROOT)}")
            print(f"  Prompt: {STYLE_PREFIX}{prompt}")
        print(f"\nTotal: {len(trabajo)} imagenes")
        return

    # Filtrar existentes
    if not args.forzar:
        pendientes = [(s, p, path) for s, p, path in trabajo if not path.exists()]
        saltadas = len(trabajo) - len(pendientes)
        if saltadas:
            print(f"Saltando {saltadas} imagenes que ya existen (usa --forzar para regenerar)")
        trabajo = pendientes

    if not trabajo:
        print("Todas las imagenes ya existen.")
        return

    # Generar
    print(f"\nGenerando {len(trabajo)} imagenes con {args.modelo}...\n")
    client = get_client()

    ok = 0
    fail = 0
    for i, (slug, prompt, path) in enumerate(trabajo, 1):
        print(f"[{i}/{len(trabajo)}]")
        if generar_imagen(client, slug, prompt, path, model=args.modelo):
            ok += 1
        else:
            fail += 1

        # Rate limiting entre llamadas
        if i < len(trabajo):
            time.sleep(2)

    print(f"\nResultado: {ok} generadas, {fail} fallidas")


if __name__ == "__main__":
    main()
