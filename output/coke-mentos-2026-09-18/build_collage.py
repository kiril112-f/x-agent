from pathlib import Path
from PIL import Image, ImageChops

root = Path(__file__).resolve().parent
temp = Path('C:/Users/User/AppData/Local/Temp')
names = [
    'codex-clipboard-fab2303a-7c61-437a-b7a3-2b3a9d4f5df0.png',
    'codex-clipboard-20938cba-0997-457d-9a33-7fb8759fa2e5.png',
    'codex-clipboard-e2ee56d8-e0a4-4ddb-ab73-9c8cd7c859f4.png',
    'codex-clipboard-59804184-63cf-4297-bb18-7694bdabecfa.png',
]
images = [Image.open(temp / name).convert('RGB') for name in names]
width, height = max(i.width for i in images), max(i.height for i in images)
gap = 12
canvas = Image.new('RGB', (width * 2 + gap, height * 2 + gap), 'white')
for index, source in enumerate(images):
    panel_x = (index % 2) * (width + gap)
    panel_y = (index // 2) * (height + gap)
    canvas.paste((10, 10, 10), (panel_x, panel_y, panel_x + width, panel_y + height))
    x = panel_x + (width - source.width) // 2
    y = panel_y + (height - source.height) // 2
    canvas.paste(source, (x, y))
    assert ImageChops.difference(source, canvas.crop((x, y, x + source.width, y + source.height))).getbbox() is None
destination = root / 'app-revenue-collage.png'
canvas.save(destination)
print(f'Saved {destination} ({canvas.width}x{canvas.height}); all four source pixel regions verified unchanged.')
