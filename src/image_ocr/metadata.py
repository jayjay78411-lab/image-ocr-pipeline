"""Extract useful metadata from images (EXIF + embedded PNG text chunks)."""
from __future__ import annotations

from PIL import Image


def metadata_text(image_path: str) -> str:
    """Return a plain-text summary of an image's metadata."""
    try:
        im = Image.open(image_path)
    except Exception as exc:  # pragma: no cover - defensive
        return f"metadata error: {exc}"

    parts: list[str] = [
        f"format: {im.format}",
        f"size: {im.size[0]}x{im.size[1]}",
        f"mode: {im.mode}",
    ]

    info = im.info or {}
    for key in ("dpi", "srgb", "gamma", "bits", "comments"):
        if key in info:
            parts.append(f"{key}: {info[key]}")

    # Embedded text chunks (e.g. PNG iTXt/tEXt/zTXt).
    try:
        text_info = getattr(im, "text", None)
        if text_info:
            for tk, tv in text_info.items():
                parts.append(f"text[{tk}]: {tv}")
    except Exception:
        pass

    # EXIF, if present.
    try:
        exif = im.getexif()
        if exif:
            for k, v in exif.items():
                parts.append(f"exif[{k}]: {str(v)[:200]}")
    except Exception:
        pass

    return "\n".join(parts)
