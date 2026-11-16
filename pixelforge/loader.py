"""Búsqueda y apertura de imágenes de la carpeta de entrada."""
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

from . import config


def listar_imagenes(carpeta: Path) -> list[Path]:
    """Devuelve los archivos JPG/PNG de la carpeta, ordenados por nombre."""
    return sorted(
        p for p in Path(carpeta).iterdir()
        if p.is_file() and p.suffix.lower() in config.EXTENSIONES
    )


def abrir_imagen(ruta: Path) -> Image.Image | None:
    """Abre una imagen, corrige su orientación EXIF y la pasa a RGB.

    Devuelve None (y avisa) si el archivo está corrupto.
    """
    try:
        with Image.open(ruta) as img:
            img = ImageOps.exif_transpose(img)
            # Las transparencias se aplanan sobre fondo blanco
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGBA")
                fondo = Image.new("RGB", img.size, (255, 255, 255))
                fondo.paste(img, mask=img.getchannel("A"))
                return fondo
            return img.convert("RGB")
    except (UnidentifiedImageError, OSError) as error:
        print(f"  [aviso] No se pudo abrir {ruta.name}: {error}")
        return None
