"""Generación de miniaturas cuadradas."""
from PIL import Image, ImageOps

from . import config


def crear_thumbnail(img: Image.Image, size=config.THUMB_SIZE) -> Image.Image:
    """Recorta al centro y redimensiona sin deformar la imagen."""
    return ImageOps.fit(img, size, Image.LANCZOS)
