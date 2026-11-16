"""PixelForge: punto de entrada de línea de comandos."""
import argparse
from pathlib import Path

from pixelforge import config, pipeline


def main() -> None:
    p = argparse.ArgumentParser(description="Thumbnails + viñeta + watermark + galería web")
    p.add_argument("--input", type=Path, default=config.INPUT_DIR, help="carpeta de imágenes")
    p.add_argument("--output", type=Path, default=config.OUTPUT_DIR, help="carpeta de salida")
    p.add_argument("--gallery", type=Path, default=config.GALLERY_DIR, help="carpeta de la galería")
    p.add_argument("--vignette", type=float, default=config.VIGNETTE_STRENGTH,
                   help="intensidad de la viñeta, de 0 a 1")
    p.add_argument("--text", default=config.WATERMARK_TEXT, help="texto del watermark")
    args = p.parse_args()

    if not args.input.is_dir():
        raise SystemExit(f"La carpeta de entrada no existe: {args.input}")

    print(f"Procesando {args.input} ...")
    ok, omitidas = pipeline.ejecutar(
        args.input, args.output, args.vignette, args.text, args.gallery
    )
    print(f"Listo: {ok} procesadas, {omitidas} omitidas.")
    if ok:
        print(f"Galería: {args.gallery / 'index.html'}")
    else:
        print("No se encontraron imágenes JPG/PNG válidas.")


if __name__ == "__main__":
    main()
