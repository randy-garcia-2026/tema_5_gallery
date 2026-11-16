"""Generación de la galería web (HTML + CSS)."""
import html
import os
import shutil
from pathlib import Path
from string import Template

from . import config


def generar_galeria(gallery_dir: Path, output_dir: Path, nombres: list[str]) -> Path:
    """Crea index.html y style.css en gallery_dir.

    `nombres` son los archivos ya procesados (existen en output_dir/thumbnails y /processed).
    Las rutas del HTML son relativas, así que funciona abriéndolo directamente (file://).
    """
    gallery_dir, output_dir = Path(gallery_dir), Path(output_dir)
    gallery_dir.mkdir(parents=True, exist_ok=True)
    rel = Path(os.path.relpath(output_dir, gallery_dir)).as_posix()
    items = "\n".join(
        f'    <a class="tarjeta" href="{rel}/processed/{html.escape(n)}">'
        f'<img src="{rel}/thumbnails/{html.escape(n)}" alt="{html.escape(Path(n).stem)}" '
        f'loading="lazy" width="300" height="300">'
        f'<span>{html.escape(Path(n).stem)}</span></a>'
        for n in nombres
    )
    total = len(nombres)
    resumen = "1 imagen procesada" if total == 1 else f"{total} imágenes procesadas"
    plantilla = Template((config.TEMPLATES_DIR / "gallery.html").read_text(encoding="utf-8"))
    pagina = plantilla.substitute(resumen=resumen, items=items)

    destino = gallery_dir / "index.html"
    destino.write_text(pagina, encoding="utf-8")
    shutil.copyfile(config.TEMPLATES_DIR / "style.css", gallery_dir / "style.css")
    return destino
