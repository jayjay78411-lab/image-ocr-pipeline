# image-ocr

Extract text and metadata from images **without a vision model**. When the model
you're using can't read image input, this local OCR pipeline turns an image into
plain text so it can still be reasoned about.

- Local OCR via [`rapidocr-onnxruntime`](https://pypi.org/project/rapidocr-onnxruntime/)
  (no external binaries, no API keys).
- Metadata extraction (format, size, DPI, EXIF, embedded PNG text chunks) via Pillow.
- Importable API + CLI.

## Install

```bash
pip install .
# or, for development
pip install -e .
```

The OCR engine is installed automatically on first use if it isn't present.

## CLI usage

```bash
# Plain text (metadata + OCR)
image-ocr path/to/image.png

# Structured JSON
image-ocr path/to/image.png --json

# OCR only
image-ocr path/to/image.png --no-metadata
```

## Library usage

```python
from image_ocr import extract, ocr_text, metadata_text

text = extract("screenshot.png")          # metadata + OCR block
ocr, engine = ocr_text("screenshot.png")   # just the OCR text
meta = metadata_text("screenshot.png")     # just the metadata
```

## When to use

Use this as a fallback whenever a model reports it "does not support image input"
or otherwise cannot view an image: run `image-ocr` on the file and feed the
returned text back to the model as the image's content.

## License

MIT
