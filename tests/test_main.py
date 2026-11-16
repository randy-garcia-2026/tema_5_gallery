"""Pruebas de la línea de comandos (main.py) y del pipeline con opciones."""
import sys

import pytest
from PIL import Image

import main
from pixelforge import pipeline


def _una_foto(carpeta):
    carpeta.mkdir()
    Image.new("RGB", (400, 300), (100, 150, 200)).save(carpeta / "foto.png")


def test_cli_procesa_y_crea_galeria(tmp_path, monkeypatch, capsys):
    _una_foto(tmp_path / "in")
    monkeypatch.setattr(sys, "argv", [
        "main.py",
        "--input", str(tmp_path / "in"),
        "--output", str(tmp_path / "out"),
        "--gallery", str(tmp_path / "gal"),
        "--vignette", "0.3",
        "--text", "© Prueba",
    ])

    main.main()

    assert "1 procesadas, 0 omitidas" in capsys.readouterr().out
    assert (tmp_path / "out" / "thumbnails" / "foto.jpg").exists()
    assert (tmp_path / "gal" / "index.html").exists()


def test_cli_carpeta_de_entrada_inexistente(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py", "--input", str(tmp_path / "nada")])
    with pytest.raises(SystemExit) as error:
        main.main()
    assert "no existe" in str(error.value)


def test_pipeline_sin_imagenes_no_crea_galeria(tmp_path):
    (tmp_path / "in").mkdir()
    pipeline.ejecutar(tmp_path / "in", tmp_path / "out", gallery_dir=tmp_path / "gal")
    assert not (tmp_path / "gal").exists()


def test_pipeline_galeria_por_defecto_junto_a_output(tmp_path):
    _una_foto(tmp_path / "in")
    pipeline.ejecutar(tmp_path / "in", tmp_path / "out")
    assert (tmp_path / "gallery" / "index.html").exists()


def test_pipeline_guarda_png_como_jpg_con_tamano_original(tmp_path):
    _una_foto(tmp_path / "in")
    pipeline.ejecutar(tmp_path / "in", tmp_path / "out")
    assert Image.open(tmp_path / "out" / "processed" / "foto.jpg").size == (400, 300)
