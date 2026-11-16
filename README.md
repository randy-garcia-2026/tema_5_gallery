# PixelForge

Pipeline en Python (Pillow) que convierte fotos JPG/PNG en una galería web:
thumbnails 300x300 → viñeta → watermark "© PixelForge" → `gallery/index.html`.

## Uso
```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
# Copia tus fotos a input/ y ejecuta:
./.venv/bin/python main.py
# Abre gallery/index.html en el navegador
```

Salida: `output/thumbnails/` (300x300), `output/processed/` (completas) y `gallery/index.html`.

Opciones: `--input`, `--output`, `--gallery`, `--vignette 0.6` (0 a 1), `--text "© Mi marca"`.

## Pruebas
```bash
./.venv/bin/python -m pytest
```

Ajustes por defecto (viñeta, opacidad del texto, calidad JPG) en `pixelforge/config.py`.
