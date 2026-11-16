"""Pruebas de thumbnail.py."""
import pytest
from PIL import Image

from pixelforge import config
from pixelforge.thumbnail import crear_thumbnail


@pytest.mark.parametrize("tam", [(800, 400), (300, 900), (50, 50), (300, 300)])
def test_thumbnail_siempre_tiene_tamano_fijo(tam):
    assert crear_thumbnail(Image.new("RGB", tam)).size == config.THUMB_SIZE


def test_thumbnail_recorta_al_centro_sin_deformar():
    # Izquierda roja, centro verde, derecha azul: el recorte central debe ser verde
    img = Image.new("RGB", (900, 300))
    img.paste((255, 0, 0), (0, 0, 300, 300))
    img.paste((0, 255, 0), (300, 0, 600, 300))
    img.paste((0, 0, 255), (600, 0, 900, 300))

    thumb = crear_thumbnail(img)

    assert thumb.getpixel((5, 150)) == (0, 255, 0)
    assert thumb.getpixel((295, 150)) == (0, 255, 0)


def test_thumbnail_tamano_personalizado():
    assert crear_thumbnail(Image.new("RGB", (500, 200)), (100, 50)).size == (100, 50)
