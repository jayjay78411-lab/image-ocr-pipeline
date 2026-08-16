"""OCR extraction using rapidocr-onnxruntime, with an auto-install fallback."""
from __future__ import annotations

import os
import subprocess
import sys

_ENGINE = "rapidocr-onnxruntime"


def _ensure_engine() -> None:
    """Import the OCR engine, installing it on first use if missing."""
    try:
        import rapidocr_onnxruntime  # noqa: F401
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q", _ENGINE]
        )


def ocr_text(image_path: str) -> tuple[str, str]:
    """Run OCR on an image.

    Returns a tuple of (joined_text, engine_name). On OCR failure or an image
    with no detectable text, the text portion is an empty string.
    """
    _ensure_engine()
    # Keep the engine's noisy startup output out of stdout.
    os.environ.setdefault("RAPIDOCR_LOG_LEVEL", "ERROR")
    import logging

    logging.disable(logging.CRITICAL)
    from rapidocr_onnxruntime import RapidOCR

    engine = RapidOCR()
    result, _ = engine(image_path)
    if not result:
        return "", _ENGINE
    lines = [text for (_box, text, _score) in result]
    return "\n".join(lines), _ENGINE
