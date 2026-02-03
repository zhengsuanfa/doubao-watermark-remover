#!/usr/bin/env python3
"""
Capture Alpha Map Tool

Extracts the alpha channel from a Doubao watermarked black image.
This creates the reference alpha map used for watermark removal.

Usage:
    python capture_alpha_map.py <black-with-watermark.png> <width> <height>
"""
import os
import sys

from PIL import Image


def capture_alpha_map(input_path: str, watermark_width: int, watermark_height: int) -> None:
    """
    Extract alpha map from a black image with Doubao watermark.
    Watermark "豆包AI生成" is in the BOTTOM-RIGHT corner.
    """
    with Image.open(input_path) as img:
        img = img.convert("RGB")
        width, height = img.size

        # Calculate position (bottom-right for Doubao)
        margin_right = 20 if watermark_width > 150 else 15
        margin_bottom = 15

        start_x = width - margin_right - watermark_width
        start_y = height - margin_bottom - watermark_height

        # Extract the watermark region
        watermark_box = (start_x, start_y, start_x + watermark_width, start_y + watermark_height)
        watermark_region = img.crop(watermark_box)

        # Save as alpha map
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.abspath(os.path.join(script_dir, "..", "assets", "doubao_alpha.png"))

        watermark_region.save(output_path)
        print(f"Alpha map saved to: {output_path}")
        print(f"Size: {watermark_width}x{watermark_height}")


def usage() -> str:
    script_name = os.path.basename(sys.argv[0])
    return f"Usage: python {script_name} <black-with-watermark.png> <width> <height>\n\n" \
           f"Example: python {script_name} black_doubao.png 200 40"


def main() -> int:
    if len(sys.argv) != 4:
        print(usage(), file=sys.stderr)
        return 1

    input_path = sys.argv[1]
    try:
        watermark_width = int(sys.argv[2])
        watermark_height = int(sys.argv[3])
    except ValueError:
        print("Error: width and height must be integers", file=sys.stderr)
        print(usage(), file=sys.stderr)
        return 1

    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        capture_alpha_map(input_path, watermark_width, watermark_height)
    except Exception as exc:
        print(f"Failed: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
