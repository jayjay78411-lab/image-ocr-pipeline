"""Command-line entry point for the image_ocr package."""
from __future__ import annotations

import argparse
import json
import os
import sys

# Allow running directly from scripts/ without installing the package.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from image_ocr import extract, ocr_text, metadata_text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Extract text and metadata from an image without a vision model."
    )
    parser.add_argument("image", help="Path to the image file")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    parser.add_argument(
        "--no-metadata", action="store_true", help="Skip the metadata section"
    )
    args = parser.parse_args(argv)

    with_metadata = not args.no_metadata

    if args.json:
        text, engine = ocr_text(args.image)
        payload: dict = {"text": text, "engine": engine}
        if with_metadata:
            payload["metadata"] = metadata_text(args.image)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(extract(args.image, with_metadata=with_metadata))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
