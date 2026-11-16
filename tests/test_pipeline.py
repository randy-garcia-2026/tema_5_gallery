"""Pruebas con imágenes sintéticas (no necesitan fotos reales)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image

from pixelforge import pipeline
from pixelforge.vignette import aplicar_vineta


def _crear_entrada(carpeta: Path) -> None:
    carpeta.mkdir()
    Image.new("RGB", (800, 400), (200, 120, 40)).save(carpeta / "ancha.jpg")
    Image.new("RGB", (300, 900), (40, 120, 200)).save(carpeta / "alta.JPG")
    Image.new("RGBA", (500, 500), (0, 200, 0, 128)).save(carpeta / "transp.png")
    (carpeta / "roto.jpg").write_text("esto no es una imagen")
    (carpeta / "notas.txt").write_text("se ignora")


def test_pipeline_completo(tmp_path):
    entrada, salida = tmp_path / "in", tmp_path / "out"
    _crear_entrada(entrada)

    ok, omitidas = pipeline.ejecutar(entrada, salida)

    assert (ok, omitidas) == (3, 1)
    for thumb in (salida / "thumbnails").glob("*.jpg"):
        assert Image.open(thumb).size == (300, 300)
    assert len(list((salida / "processed").glob("*.jpg"))) == 3
    galeria = tmp_path / "gallery"
    pagina = (galeria / "index.html").read_text(encoding="utf-8")
    assert pagina.count("<img") == 3
    assert "../out/thumbnails/" in pagina
    assert (galeria / "style.css").exists()


def test_vineta_oscurece_bordes_no_centro():
    img = Image.new("RGB", (200, 200), (255, 255, 255))
    resultado = aplicar_vineta(img, 0.8)
    centro, esquina = resultado.getpixel((100, 100)), resultado.getpixel((0, 0))
    assert sum(centro) > sum(esquina)
    assert centro[0] > 240  # el centro casi no cambia


def test_carpeta_sin_imagenes(tmp_path):
    entrada = tmp_path / "vacia"
    entrada.mkdir()
    assert pipeline.ejecutar(entrada, tmp_path / "out") == (0, 0)
