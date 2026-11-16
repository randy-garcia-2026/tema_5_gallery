"""Pruebas de vignette.py."""
import pytest
from PIL import Image, ImageChops

from pixelforge.vignette import aplicar_vineta


def _blanca():
    return Image.new("RGB", (200, 200), (255, 255, 255))


def test_fuerza_cero_no_cambia_la_imagen():
    resultado = aplicar_vineta(_blanca(), 0)
    assert ImageChops.difference(resultado, _blanca()).getbbox() is None


def test_fuerza_mayor_oscurece_mas_las_esquinas():
    suave = aplicar_vineta(_blanca(), 0.3).getpixel((0, 0))
    fuerte = aplicar_vineta(_blanca(), 0.9).getpixel((0, 0))
    assert sum(fuerte) < sum(suave)


@pytest.mark.parametrize("fuerza", [-5, 7])
def test_fuerza_fuera_de_rango_se_limita(fuerza):
    # No debe fallar y debe equivaler a 0 o a 1
    limitada = 0 if fuerza < 0 else 1
    a = aplicar_vineta(_blanca(), fuerza)
    b = aplicar_vineta(_blanca(), limitada)
    assert ImageChops.difference(a, b).getbbox() is None


def test_conserva_tamano_y_devuelve_rgb():
    resultado = aplicar_vineta(Image.new("RGBA", (120, 80), (255, 0, 0, 255)), 0.5)
    assert resultado.size == (120, 80)
    assert resultado.mode == "RGB"
