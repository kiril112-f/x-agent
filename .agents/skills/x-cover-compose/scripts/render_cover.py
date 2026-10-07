"""Deterministic layered cover compositor. Python 3.10+, Pillow; no network.

Coordinates describe visible ink, not font ascenders. JSON is the editable source.
Run: python render_cover.py spec.json --out cover.png
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

FONT_FILES = {
    "sans": "Inter-VariableFont_opszwght.ttf",
    "serif": "georgia.ttf", "serif-italic": "georgiai.ttf",
    "condensed": "impact.ttf", "mono": "consola.ttf",
}


def font_for(layer, size, spec_dir, font_dir):
    name = layer.get("font", "sans")
    path = font_dir / FONT_FILES[name] if name in FONT_FILES else spec_dir / name
    if not path.is_file():
        raise ValueError(f"Missing font {path}. Supply --font-dir or an explicit font path; no silent fallback.")
    font = ImageFont.truetype(str(path), size)
    if name == "sans":
        axes = font.get_variation_axes()
        values = [a["default"] for a in axes]
        for i, a in enumerate(axes):
            axis_name = a["name"].decode() if isinstance(a["name"], bytes) else a["name"]
            if "weight" in axis_name.lower():
                values[i] = layer.get("weight", 850)
            elif "optical" in axis_name.lower():
                values[i] = min(a["maximum"], size)
        font.set_variation_by_axes(values)
    return font, path


def text_geometry(text, font, tracking):
    # Whole-line shaping preserves kerning when tracking is zero.
    if tracking == 0:
        return font.getbbox(text), None
    cursor, placements, boxes = 0.0, [], []
    for char in text:
        b = font.getbbox(char)
        placements.append((cursor, char))
        if b[2] > b[0] and b[3] > b[1]:
            boxes.append((cursor + b[0], b[1], cursor + b[2], b[3]))
        cursor += font.getlength(char) + tracking
    if not boxes:
        raise ValueError("Text has no visible glyphs")
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes)), placements


def render(spec_path, out_path, font_dir):
    spec_path, out_path = Path(spec_path).resolve(), Path(out_path).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8-sig"))
    width, height = spec.get("size", [2000, 800])
    if not (320 <= width <= 8000 and 100 <= height <= 8000):
        raise ValueError("Invalid canvas size")
    canvas = Image.new("RGBA", (width, height), spec.get("background", "#ffffff"))
    report = {"spec": str(spec_path), "size": [width, height], "layers": [],
              "automated_geometry_pass": False, "visual_review": "required"}
    for index, layer in enumerate(spec.get("layers", [])):
        kind = layer["type"]
        record = {"index": index, "type": kind}
        draw = ImageDraw.Draw(canvas)
        if kind == "image":
            if layer.get("fit", "contain") not in {"contain", "cover"}:
                raise ValueError("image fit must be contain or cover")
            opacity = layer.get("opacity", 1)
            if not isinstance(opacity, (int, float)) or not math.isfinite(opacity) or not 0 <= opacity <= 1:
                raise ValueError("image opacity must be finite and between 0 and 1")
            centering = layer.get("centering", [.5, .5])
            if not isinstance(centering, (list, tuple)) or len(centering) != 2 or any(not isinstance(v, (int, float)) or not math.isfinite(v) or not 0 <= v <= 1 for v in centering):
                raise ValueError("image centering requires two values between 0 and 1")
            path = (spec_path.parent / layer["path"]).resolve()
            with Image.open(path) as source:
                asset = source.convert("RGBA")
            if layer.get("trim_alpha"):
                box = asset.getchannel("A").getbbox()
                if box is None:
                    raise ValueError("Entirely transparent image")
                asset = asset.crop(box)
            x, y, w, h = layer["box"]
            if layer.get("fit", "contain") == "cover":
                asset = ImageOps.fit(asset, (w, h), Image.Resampling.LANCZOS,
                                     centering=tuple(layer.get("centering", [.5, .5])))
            else:
                asset.thumbnail((w, h), Image.Resampling.LANCZOS)
                x += (w - asset.width) // 2
                y += (h - asset.height) // 2
            if layer.get("opacity", 1) != 1:
                asset.putalpha(asset.getchannel("A").point(lambda p: round(p * layer["opacity"])))
            canvas.alpha_composite(asset, (x, y))
            record.update(path=str(path), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                          bbox=[x, y, x + asset.width, y + asset.height])
        elif kind == "gradient":
            # Directional two-color gradient. No random noise or platform artifacts.
            from PIL import ImageColor
            a, b = [ImageColor.getrgb(layer[k]) for k in ("start", "end")]
            rows = Image.new("RGB", (1, height))
            rows.putdata([tuple(round(a[c] + (b[c] - a[c]) * y / max(1, height - 1)) for c in range(3)) for y in range(height)])
            canvas.alpha_composite(rows.resize((width, height)).convert("RGBA"))
        elif kind == "text":
            text = layer["text"]
            if not text.strip() or "\n" in text:
                raise ValueError("Each text layer must be one nonempty line; explicit lines preserve composition")
            x, y, w, h = layer["box"]
            size = layer["size"]
            minimum = layer.get("min_size", size)
            while True:
                font, path = font_for(layer, size, spec_path.parent, font_dir)
                bounds, placements = text_geometry(text, font, layer.get("tracking", 0))
                ink_w, ink_h = bounds[2] - bounds[0], bounds[3] - bounds[1]
                if ink_w <= w and ink_h <= h:
                    break
                size -= 1
                if size < minimum:
                    raise ValueError(f"Text overflow in layer {index}: {text!r}; revise line breaks or box, do not silently shrink")
            align = layer.get("align", "left")
            x += {"left": 0, "center": (w - ink_w) / 2, "right": w - ink_w}[align]
            y += {"top": 0, "center": (h - ink_h) / 2, "bottom": h - ink_h}[layer.get("valign", "top")]
            origin = (x - bounds[0], y - bounds[1])
            color = layer.get("fill", "#111111")
            if placements is None:
                draw.text(origin, text, font=font, fill=color)
            else:
                for dx, char in placements:
                    draw.text((origin[0] + dx, origin[1]), char, font=font, fill=color)
            if not layer.get("allow_bleed", False) and (x < 0 or y < 0 or x + ink_w > width or y + ink_h > height):
                raise ValueError(f"Text outside canvas in layer {index}")
            record.update(text=text, font=str(path), font_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                          weight=layer.get("weight"), size=size,
                          bbox=[round(x, 2), round(y, 2), round(x + ink_w, 2), round(y + ink_h, 2)],
                          thumbnail_ink_height=round(ink_h * 340 / width, 2))
        elif kind in ("rect", "ellipse"):
            x, y, w, h = layer["box"]
            bbox = (x, y, x + w, y + h)
            options = dict(fill=layer.get("fill"), outline=layer.get("outline"), width=layer.get("stroke", 1))
            if kind == "ellipse":
                draw.ellipse(bbox, **options)
            else:
                draw.rounded_rectangle(bbox, radius=layer.get("radius", 0), **options)
        elif kind == "line":
            draw.line(layer["points"], fill=layer.get("fill", "black"), width=layer.get("stroke", 3), joint="curve")
        elif kind == "polygon":
            draw.polygon([tuple(p) for p in layer["points"]], fill=layer["fill"])
        else:
            raise ValueError(f"Unsupported layer type: {kind}")
        report["layers"].append(record)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(out_path)
    thumb = canvas.convert("RGB")
    thumb.thumbnail((340, 340), Image.Resampling.LANCZOS)
    thumb.save(out_path.with_name(out_path.stem + "-thumb.png"))
    report["automated_geometry_pass"] = True
    report["output_sha256"] = hashlib.sha256(out_path.read_bytes()).hexdigest()
    out_path.with_suffix(".qa.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--font-dir", type=Path, default=Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts")
    args = parser.parse_args()
    result = render(args.spec, args.out, args.font_dir)
    print(json.dumps({"output": str(args.out), "geometry": "pass", "visual_review": "required"}))
