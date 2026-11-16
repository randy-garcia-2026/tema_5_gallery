"""Orquestación: input/ -> procesado -> output/ + galería."""
from pathlib import Path

from PIL import Image

from . import config
from .gallery import generar_galeria
from .loader import abrir_imagen, listar_imagenes
from .thumbnail import crear_thumbnail
from .vignette import aplicar_vineta
from .watermark import aplicar_watermark


def _procesar(img: Image.Image, fuerza: float, texto: str) -> Image.Image:
    # Orden importante: viñeta primero, para que el texto no se oscurezca
    return aplicar_watermark(aplicar_vineta(img, fuerza), texto)


def ejecutar(
    input_dir: Path = config.INPUT_DIR,
    output_dir: Path = config.OUTPUT_DIR,
    fuerza: float = config.VIGNETTE_STRENGTH,
    texto: str = config.WATERMARK_TEXT,
    gallery_dir: Path | None = None,
) -> tuple[int, int]:
    """Procesa todas las imágenes. Devuelve (procesadas, omitidas)."""
    input_dir, output_dir = Path(input_dir), Path(output_dir)
    # Por defecto la galería va en una carpeta "gallery" junto a output/
    gallery_dir = Path(gallery_dir) if gallery_dir else output_dir.parent / "gallery"
    thumbs_dir, full_dir = output_dir / "thumbnails", output_dir / "processed"
    thumbs_dir.mkdir(parents=True, exist_ok=True)
    full_dir.mkdir(parents=True, exist_ok=True)

    procesadas, omitidas, nombres = 0, 0, []
    for ruta in listar_imagenes(input_dir):
        img = abrir_imagen(ruta)
        if img is None:
            omitidas += 1
            continue

        # Todo se guarda como JPG (las transparencias ya se aplanaron al abrir)
        nombre = ruta.stem + ".jpg"
        _procesar(img, fuerza, texto).save(full_dir / nombre, quality=config.JPG_QUALITY)
        # El thumbnail se recorta primero: la viñeta y el texto quedan proporcionados a 300x300
        _procesar(crear_thumbnail(img), fuerza, texto).save(
            thumbs_dir / nombre, quality=config.JPG_QUALITY
        )
        nombres.append(nombre)
        procesadas += 1
        print(f"  [ok] {ruta.name}")

    if nombres:
        generar_galeria(gallery_dir, output_dir, nombres)
    return procesadas, omitidas
