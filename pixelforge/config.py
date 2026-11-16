"""Constantes ajustables del pipeline."""
from pathlib import Path

# Carpetas
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"  # contiene thumbnails/ y processed/
GALLERY_DIR = BASE_DIR / "gallery"  # contiene index.html y style.css
TEMPLATES_DIR = BASE_DIR / "templates"

# Extensiones aceptadas (en minúsculas)
EXTENSIONES = {".jpg", ".jpeg", ".png"}

# Thumbnail
THUMB_SIZE = (300, 300)

# Viñeta: 0 = sin efecto, 1 = bordes totalmente negros
VIGNETTE_STRENGTH = 0.6

# Watermark
WATERMARK_TEXT = "© PixelForge"
WATERMARK_OPACITY = 120  # 0 (invisible) a 255 (sólido)
FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "DejaVuSans.ttf",
]

# Calidad de guardado JPG
JPG_QUALITY = 85
