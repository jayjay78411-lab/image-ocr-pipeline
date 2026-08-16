"""Image OCR fallback: extract text/metadata from images without a vision model.

Public API:
    from image_ocr import extract, ocr_text, metadata_text
    text = extract("photo.png")
"""
from __future__ import annotations

from .core import ocr_text
from .metadata import metadata_text

__all__ = ["extract", "ocr_text", "metadata_text"]


def extract(image_path: str, with_metadata: bool = True) -> str:
    """Return a human-readable text block describing the image's content.

    Combines OCR text with useful metadata so a non-vision model can reason
    about the image. Returns plain text suitable for printing or feeding to a
    language model.
    """
    text, _engine = ocr_text(image_path)
    out: list[str] = []
    if with_metadata:
        out.append("=== METADATA ===")
        out.append(metadata_text(image_path))
        out.append("")
    out.append("=== OCR TEXT ===")
    out.append(text if text else "(no text detected)")
    return "\n".join(out)
