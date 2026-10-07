"""Make a reference-only feed-size inspection sheet; never modifies originals."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'x-content-engine' / 'INDEX.md').exists())
LIBRARY = ROOT / 'x-content-engine/assets/cover-references/2026-10-07/originals'
entries = [('Current baseline', HERE.parent / 'experiments-2026-10-07/01-photo.png')]
for number in (6, 11, 25, 17, 15, 12, 19, 16):
    entries.append((f'Reference {number:02}', next(LIBRARY.glob(f'{number:02}-*'))))
canvas = Image.new('RGB', (1120, 570), '#e8e5df')
draw = ImageDraw.Draw(canvas)
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 18)
for i, (label, path) in enumerate(entries):
    x, y = 20 + (i % 3) * 370, 10 + (i // 3) * 190
    draw.text((x, y), label, font=font, fill='#242424')
    im = ImageOps.contain(Image.open(path).convert('RGB'), (340, 136), Image.Resampling.LANCZOS)
    canvas.paste(im, (x, y + 32))
canvas.save(HERE / 'references-340.jpg', quality=96)
print(HERE / 'references-340.jpg')
