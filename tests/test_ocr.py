import os
import tempfile

from PIL import Image, ImageDraw, ImageFont

from image_ocr import extract, ocr_text, metadata_text


def _make_sample(path: str) -> None:
    img = Image.new("RGB", (240, 80), "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default()
    except Exception:  # pragma: no cover
        font = None
    draw.text((10, 10), "Hello OCR", fill="black", font=font)
    img.save(path)


def test_extract_returns_text():
    path = os.path.join(tempfile.gettempdir(), "image_ocr_test.png")
    try:
        _make_sample(path)
        out = extract(path)
        assert isinstance(out, str) and out, "extract() should return non-empty text"
        text, engine = ocr_text(path)
        # The default bitmap font can introduce letter-spacing; ignore whitespace.
        flattened = "".join(text.split())
        assert "HelloOCR" in flattened, f"OCR missed the text: {text!r}"
        assert "format: PNG" in metadata_text(path)
    finally:
        if os.path.exists(path):
            os.remove(path)
