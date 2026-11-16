"""Watermark de texto semitransparente."""
from PIL import Image, ImageDraw, ImageFont

from . import config


def _cargar_fuente(tamano: int):
    for ruta in config.FONT_PATHS:
        try:
            return ImageFont.truetype(ruta, tamano)
        except OSError:
            continue
    return ImageFont.load_default(tamano)


def aplicar_watermark(
    img: Image.Image,
    texto: str = config.WATERMARK_TEXT,
    opacidad: int = config.WATERMARK_OPACITY,
) -> Image.Image:
    """Dibuja el texto en la esquina inferior derecha, proporcional al ancho."""
    base = img.convert("RGBA")
    capa = Image.new("RGBA", base.size, (255, 255, 255, 0))
    dibujo = ImageDraw.Draw(capa)

    fuente = _cargar_fuente(max(10, base.width // 12))
    caja = dibujo.textbbox((0, 0), texto, font=fuente)
    ancho, alto = caja[2] - caja[0], caja[3] - caja[1]
    margen = max(4, base.width // 40)
    x = base.width - ancho - margen - caja[0]
    y = base.height - alto - margen - caja[1]

    dibujo.text((x, y), texto, font=fuente, fill=(255, 255, 255, opacidad))
    return Image.alpha_composite(base, capa).convert("RGB")
