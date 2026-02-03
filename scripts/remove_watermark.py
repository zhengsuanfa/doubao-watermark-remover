#!/usr/bin/env python3
"""
Doubao Watermark Remover

Removes the "豆包AI生成" watermark from Doubao-generated images.
The watermark appears in the BOTTOM-RIGHT corner.
"""
import os
import sys
from typing import List, Tuple

from PIL import Image

ALPHA_THRESHOLD = 0.002
MAX_ALPHA = 0.99
LOGO_VALUE = 255  # Doubao uses white text


def detect_watermark_config(width: int, height: int) -> Tuple[int, int, int]:
    """
    Detect watermark configuration based on image size.
    Returns: (logo_width, logo_height, margin_right)
    """
    # Doubao watermark "豆包AI生成" appears in bottom-right corner
    # Scale watermark based on image size
    if width > 1024 or height > 1024:
        # Large image - scale up watermark proportionally
        scale = min(width, height) / 288  # Base on alpha image size
        logo_width = int(120 * scale * 1.2)  # Add 20% buffer
        logo_height = int(20 * scale * 1.5)
        margin_right = int(10 * scale)
        return logo_width, logo_height, margin_right
    # Small image
    return 90, 18, 8


def calculate_position(width: int, height: int, logo_width: int, logo_height: int, margin_right: int, margin_bottom: int) -> Tuple[int, int]:
    """
    Calculate watermark position.
    Doubao watermark "豆包AI生成" is in the BOTTOM-RIGHT corner.
    """
    return width - margin_right - logo_width, height - margin_bottom - logo_height


def load_alpha_map(logo_width: int, logo_height: int) -> List[float]:
    """
    Load pre-captured alpha map for the watermark.
    If not found, create a default one (less accurate but functional).
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    asset_path = os.path.abspath(os.path.join(script_dir, "..", "assets", "doubao_alpha.png"))

    if not os.path.exists(asset_path):
        # Return a default flat alpha if no map exists
        # Increased alpha for better removal without proper alpha map
        return [0.25] * (logo_width * logo_height)

    with Image.open(asset_path) as img:
        img = img.convert("RGB")
        if img.width != logo_width or img.height != logo_height:
            # Resize if needed
            img = img.resize((logo_width, logo_height))
        pixels = list(img.getdata())

    alpha_map: List[float] = [0.0] * (logo_width * logo_height)
    for i, (r, g, b) in enumerate(pixels):
        max_channel = r if r >= g and r >= b else (g if g >= b else b)
        alpha_map[i] = max_channel / 255.0

    return alpha_map


def remove_watermark(input_path: str, output_path: str) -> None:
    """
    Remove Doubao watermark by completely replacing watermark region.
    Uses 100% background replacement for detected watermark pixels.
    """
    with Image.open(input_path) as img:
        img = img.convert("RGB")
        width, height = img.size

        logo_width, logo_height, margin_right = detect_watermark_config(width, height)
        margin_bottom = 5  # Based on captured image

        start_x, start_y = calculate_position(width, height, logo_width, logo_height, margin_right, margin_bottom)
        alpha_map = load_alpha_map(logo_width, logo_height)

        pixels = img.load()

        # Build per-column background color map from area above watermark
        bg_color_map = {}
        for x_offset in range(logo_width):
            column_samples = []
            # Sample from a wider area above
            for sy in range(max(0, start_y - 60), start_y):
                sx = start_x + x_offset
                if 0 <= sx < width:
                    column_samples.append(pixels[sx, sy])
            if column_samples:
                column_samples.sort(key=lambda p: p[0] + p[1] + p[2])
                median_idx = len(column_samples) // 2
                bg_color_map[x_offset] = column_samples[median_idx]
            else:
                bg_color_map[x_offset] = (100, 100, 100)

        # Also sample from left of watermark for better background match
        left_bg_colors = []
        for sx in range(max(0, start_x - 30), start_x):
            for sy in range(start_y, min(height, start_y + logo_height)):
                left_bg_colors.append(pixels[sx, sy])
        if left_bg_colors:
            left_bg_colors.sort(key=lambda p: p[0] + p[1] + p[2])
            left_bg = left_bg_colors[len(left_bg_colors) // 2]
        else:
            left_bg = (100, 100, 100)

        # Process watermark region - COMPLETE replacement for detected watermark pixels
        for row in range(logo_height):
            y = start_y + row
            if y < 0 or y >= height:
                continue
            alpha_row_offset = row * logo_width
            for col in range(logo_width):
                x = start_x + col
                if x < 0 or x >= width:
                    continue

                alpha = alpha_map[alpha_row_offset + col]

                # For any pixel with alpha > threshold, COMPLETELY replace with background
                if alpha > 0.15:
                    # Use column-specific background color
                    bg_r, bg_g, bg_b = bg_color_map.get(col, left_bg)

                    # Add slight noise for natural look
                    import random
                    noise = random.randint(-3, 3)
                    r_out = max(0, min(255, bg_r + noise))
                    g_out = max(0, min(255, bg_g + noise))
                    b_out = max(0, min(255, bg_b + noise))

                    pixels[x, y] = (r_out, g_out, b_out)

        img.save(output_path)


def usage() -> str:
    script_name = os.path.basename(sys.argv[0])
    return f"Usage: python {script_name} <input-image> <output-image>"


def main() -> int:
    if len(sys.argv) != 3:
        print(usage(), file=sys.stderr)
        return 1

    input_path, output_path = sys.argv[1], sys.argv[2]
    try:
        remove_watermark(input_path, output_path)
    except Exception as exc:
        print(f"Failed: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

    print(f"Removed Doubao watermark -> {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
