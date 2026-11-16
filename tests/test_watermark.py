"""Pruebas de watermark.py."""
from PIL import Image, ImageChops

from pixelforge import watermark
from pixelforge.watermark import aplicar_watermark


def _negra(tam=(300, 300)):
    return Image.new("RGB", tam, (0, 0, 0))


def test_conserva_tamano_y_devuelve_rgb():
    resultado = aplicar_watermark(_negra((400, 200)))
    assert resultado.size == (400, 200)
    assert resultado.mode == "RGB"


def test_dibuja_texto_en_esquina_inferior_derecha():
    resultado = aplicar_watermark(_negra(), "ABC", opacidad=255)
    diferencia = ImageChops.difference(resultado, _negra())
    izq, arriba, der, abajo = diferencia.getbbox()
    # El texto está en la mitad inferior derecha y no toca la esquina superior izquierda
    assert izq > 100 and arriba > 200
    assert der <= 300 and abajo <= 300


def test_opacidad_cero_no_cambia_la_imagen():
    resultado = aplicar_watermark(_negra(), "ABC", opacidad=0)
    assert ImageChops.difference(resultado, _negra()).getbbox() is None


def test_mas_opacidad_da_texto_mas_brillante():
    tenue = aplicar_watermark(_negra(), "ABC", opacidad=40).getextrema()
    fuerte = aplicar_watermark(_negra(), "ABC", opacidad=250).getextrema()
    assert fuerte[0][1] > tenue[0][1]


def test_imagen_diminuta_no_falla():
    assert aplicar_watermark(_negra((20, 20))).size == (20, 20)


def test_fuente_alternativa_si_no_existe_ninguna(monkeypatch):
    monkeypatch.setattr(watermark.config, "FONT_PATHS", ["/no/existe.ttf"])
    assert aplicar_watermark(_negra()).size == (300, 300)
