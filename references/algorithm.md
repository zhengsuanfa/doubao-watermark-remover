# Doubao Watermark Removal Algorithm

## Reverse Alpha Blending

Doubao visible watermark uses alpha compositing with white text:

```
watermarked = α × logo + (1 - α) × original
```

Solve for original:

```
original = (watermarked - α × logo) / (1 - α)
```

Where:
- `logo` is white (255, 255, 255)
- `α` (alpha) varies per pixel (captured from reference image)

## Watermark Location

Like Gemini, **Doubao watermark is in the BOTTOM-RIGHT corner**.

Text: "豆包AI生成"

## Detection Rules

| Image Size | Watermark Size | Right Margin | Bottom Margin |
|------------|----------------|--------------|---------------|
| > 1024px   | ~180×40        | 20px         | 15px          |
| ≤ 1024px   | ~140×35        | 15px         | 15px          |

## Capturing Alpha Map

To create an accurate alpha map:

1. Create a pure black image (RGB: 0,0,0)
2. Upload to Doubao and let it add watermark
3. The resulting image will have the watermark in white with varying alpha
4. Use `capture_alpha_map.py` to extract the alpha values

```bash
python capture_alpha_map.py black_with_watermark.png 180 40
```

This saves `assets/doubao_alpha.png` for use in removal.

## Limitations

- Only removes the visible Doubao text watermark
- Does not remove invisible/steganographic watermarks
- Works best with captured alpha map from same image size
- Watermark position/font may change over time
