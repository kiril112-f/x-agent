"""Exact user-requested screenshot crops; no generation or analytics redrawing."""
from pathlib import Path
import hashlib
import json
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'x-content-engine' / 'INDEX.md').exists())
ASSETS = HERE / 'assets'
ASSETS.mkdir(exist_ok=True)

attachment = Path('C:/Users/User/Downloads/videos-no-longer-getting-pushed-to-those-in-the-united-v0-plmwzdhn5yhg1.webp')
preserved = ASSETS / 'locations-66-original.webp'
if not preserved.exists():
    shutil.copyfile(attachment, preserved)

SPECS = [
    dict(id='locations-66', source=preserved, box=[26, 61, 850, 557], radius=30,
         origin='User attachment, 2026-10-07. Ownership and original web URL not supplied.',
         keep='Locations; United States 66.4%; Other 14.6%; United Kingdom 5.8%',
         remove='Saudi Arabia and all subsequent rows', label='01 / Supplied screenshot'),
    dict(id='viewer-insights-97', source=ROOT / 'x-content-engine/production/us-social-setup-2026-10-05/media/camphoto_1144747756-2.jpg',
         box=[430, 1490, 2535, 2672], radius=78,
         origin='Original photograph supplied in the article Notion draft; closing body image.',
         keep='Viewer insights and tabs; United States 97.5%; Other 0.6%',
         remove='Chart above; Guyana and all subsequent rows', label='02 / Article photo'),
]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def font(size, bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/' + ('arialbd.ttf' if bold else 'arial.ttf'), size)

manifest = []
for spec in SPECS:
    original = ImageOps.exif_transpose(Image.open(spec['source'])).convert('RGB')
    crop = original.crop(spec['box']).convert('RGBA')
    scale = 4
    mask = Image.new('L', (crop.width * scale, crop.height * scale), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, mask.width - 1, mask.height - 1), radius=spec['radius'] * scale, fill=255)
    crop.putalpha(mask.resize(crop.size, Image.Resampling.LANCZOS))
    output = ASSETS / (spec['id'] + '-rounded.png')
    crop.save(output, optimize=True)
    # Exact source RGB is retained. Only the alpha channel around corners changes.
    assert crop.convert('RGB').tobytes() == original.crop(spec['box']).tobytes()
    manifest.append({
        **{k: v for k, v in spec.items() if k != 'source'},
        'source': str(spec['source'].relative_to(ROOT)).replace('\\', '/'),
        'source_size': original.size, 'source_sha256': digest(spec['source']),
        'output': str(output.relative_to(HERE)).replace('\\', '/'),
        'output_size': crop.size, 'output_sha256': digest(output),
        'pixel_check': 'RGB matches exact source crop; only corner alpha edited',
    })

board = Image.new('RGB', (1480, 570), '#e8e5df')
d = ImageDraw.Draw(board)
for i, spec in enumerate(SPECS):
    x = 40 + i * 740
    d.text((x, 30), spec['label'], font=font(25, True), fill='#242424')
    asset = Image.open(ASSETS / (spec['id'] + '-rounded.png'))
    asset = ImageOps.contain(asset, (660, 440), Image.Resampling.LANCZOS)
    board.paste(asset, (x, 90), asset)
board.save(HERE / 'proof-crops.jpg', quality=95)

(HERE / 'proof-manifest.json').write_text(json.dumps({
    'purpose': 'Two independent real analytics cards for cover concepts; not a before/after series.',
    'transforms': 'Rectangular crop and antialiased rounded alpha corners only. No reshoot, regeneration, perspective correction, number editing, or color correction.',
    'assets': manifest,
}, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps([{'file': item['output'], 'size': item['output_size'], 'check': item['pixel_check']} for item in manifest]))
