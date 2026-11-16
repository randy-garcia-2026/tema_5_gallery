"""Pruebas de gallery.py."""
from pixelforge.gallery import generar_galeria


def test_crea_index_y_css(tmp_path):
    destino = generar_galeria(tmp_path / "gallery", tmp_path / "out", ["foto.jpg"])

    assert destino == tmp_path / "gallery" / "index.html"
    assert destino.exists()
    assert (tmp_path / "gallery" / "style.css").exists()


def test_rutas_relativas_a_thumbnails_y_processed(tmp_path):
    destino = generar_galeria(tmp_path / "gallery", tmp_path / "out", ["foto.jpg"])
    pagina = destino.read_text(encoding="utf-8")

    assert 'src="../out/thumbnails/foto.jpg"' in pagina
    assert 'href="../out/processed/foto.jpg"' in pagina


def test_resumen_singular_y_plural(tmp_path):
    uno = generar_galeria(tmp_path / "g1", tmp_path / "out", ["a.jpg"])
    dos = generar_galeria(tmp_path / "g2", tmp_path / "out", ["a.jpg", "b.jpg"])

    assert "1 imagen procesada" in uno.read_text(encoding="utf-8")
    assert "2 imágenes procesadas" in dos.read_text(encoding="utf-8")


def test_escapa_caracteres_especiales_del_nombre(tmp_path):
    destino = generar_galeria(tmp_path / "gallery", tmp_path / "out", ['<b>"x".jpg'])
    pagina = destino.read_text(encoding="utf-8")

    assert "<b>" not in pagina  # no se inyecta HTML
    assert "&lt;b&gt;" in pagina


def test_crea_carpeta_de_galeria_si_no_existe(tmp_path):
    destino = generar_galeria(tmp_path / "a" / "b" / "gallery", tmp_path / "out", [])
    assert destino.exists()
