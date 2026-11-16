"""Pruebas de loader.py: listar y abrir imágenes."""
from PIL import Image

from pixelforge.loader import abrir_imagen, listar_imagenes


def test_listar_filtra_extensiones_y_ordena(tmp_path):
    for nombre in ["b.jpg", "a.PNG", "c.jpeg", "notas.txt", "d.gif"]:
        (tmp_path / nombre).write_bytes(b"x")
    (tmp_path / "subcarpeta.jpg").mkdir()  # una carpeta no cuenta

    nombres = [p.name for p in listar_imagenes(tmp_path)]

    assert nombres == ["a.PNG", "b.jpg", "c.jpeg"]


def test_abrir_devuelve_rgb(tmp_path):
    Image.new("L", (10, 10), 128).save(tmp_path / "gris.png")
    img = abrir_imagen(tmp_path / "gris.png")
    assert img.mode == "RGB"


def test_abrir_transparencia_se_aplana_sobre_blanco(tmp_path):
    Image.new("RGBA", (10, 10), (0, 0, 0, 0)).save(tmp_path / "vacia.png")
    img = abrir_imagen(tmp_path / "vacia.png")
    assert img.mode == "RGB"
    assert img.getpixel((5, 5)) == (255, 255, 255)


def test_abrir_corrige_orientacion_exif(tmp_path):
    # Orientación EXIF 6 = hay que rotar 90°, así que 40x20 pasa a 20x40
    original = Image.new("RGB", (40, 20), (10, 20, 30))
    exif = Image.Exif()
    exif[0x0112] = 6
    original.save(tmp_path / "rotada.jpg", exif=exif)

    assert abrir_imagen(tmp_path / "rotada.jpg").size == (20, 40)


def test_abrir_archivo_corrupto_devuelve_none(tmp_path, capsys):
    ruta = tmp_path / "roto.jpg"
    ruta.write_text("no soy una imagen")

    assert abrir_imagen(ruta) is None
    assert "roto.jpg" in capsys.readouterr().out  # avisa por consola
