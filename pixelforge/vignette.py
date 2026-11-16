"""Filtro de viñeta (bordes oscurecidos)."""
from PIL import Image

from . import config


def aplicar_vineta(img: Image.Image, fuerza: float = config.VIGNETTE_STRENGTH) -> Image.Image:
    """Oscurece los bordes con una máscara radial.

    radial_gradient('L') es negro en el centro (0) y blanco en los bordes (255).
    Esa máscara, escalada por `fuerza`, decide cuánto negro se mezcla en cada píxel.
    """
    fuerza = max(0.0, min(1.0, fuerza))
    mascara = Image.radial_gradient("L").resize(img.size, Image.BICUBIC)
    mascara = mascara.point(lambda v: int(v * fuerza))
    negro = Image.new("RGB", img.size, (0, 0, 0))
    return Image.composite(negro, img.convert("RGB"), mascara)
