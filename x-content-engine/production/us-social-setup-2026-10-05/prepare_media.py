"""Preserve supplied media; compose the specifically requested four-screen layout."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import pillow_heif

ROOT = Path(__file__).resolve().parent
MEDIA = ROOT / 'media'
pillow_heif.register_heif_opener()
with Image.open(MEDIA / 'IMG_4666.heic') as photo:
    ImageOps.exif_transpose(photo).convert('RGB').save(MEDIA / 'IMG_4666.jpg', quality=96)

# These are the user's exact UI screenshots, resized without retouching or redrawing.
W, H = 2400, 1550
canvas = Image.new('RGB', (W, H), '#F4F2ED')
draw = ImageDraw.Draw(canvas)
def font(size, bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/' + ('arialbd.ttf' if bold else 'arial.ttf'), size)
ink = '#181918'
muted = '#6D6E68'
orange = '#F57C2A'
draw.text((82, 56), 'Build a feed worth studying', font=font(70, True), fill=ink)
draw.text((85, 148), 'Search the niche. Save useful examples. Keep the right creators close.', font=font(31), fill=muted)

columns = [(82, 595, '1', 'Search the niche'), (662, 1085, '2', 'Study + save a video'), (1810, 508, '3', 'Follow the creator')]
for x,w,n,title in columns:
    draw.rounded_rectangle((x,220,x+58,278), radius=29, fill=orange)
    box = draw.textbbox((0,0), n, font=font(31,True))
    draw.text((x+29-(box[2]-box[0])/2,230),n,font=font(31,True),fill='white')
    draw.text((x+77,227), title, font=font(34,True),fill=ink)

source_names=['IMG_8675.png','IMG_8671.png','IMG_8672.png','IMG_8674.png']
positions=[(82, 336), (662, 336), (1236,336), (1810,336)]
max_size=(508,1100)
for name,(x,y) in zip(source_names,positions):
    source=Image.open(MEDIA/name).convert('RGB')
    source.thumbnail(max_size,Image.Resampling.LANCZOS)
    draw.rounded_rectangle((x-2,y-2,x+source.width+2,y+source.height+2),radius=6,fill='#D8D7D2')
    canvas.paste(source,(x,y))

draw.text((82,1470),'Original screenshots • Example niche: fitness',font=font(27),fill=muted)
draw.text((1900,1470),'@KirillMorozovop',font=font(27),fill=muted)
canvas.save(MEDIA/'niche-research-workflow.png',optimize=True)

# Keep references as supplied. These are reference-only assets, not publication assets.
REF=ROOT.parents[1]/'assets'/'cover-references'/'2026-10-05'
REF.mkdir(parents=True,exist_ok=True)
refs={
 '01-cinematic-proof.png':'ed35b415-a13c-4132-b851-2c7b5ff79515',
 '02-minimal-metric.png':'9d0c4c31-c663-47bf-baa0-4f9a061a83b4',
 '03-neon-app.png':'1e4f51fe-99dc-44b2-b8f8-9fd9b96cd6a1',
 '04-luminous-engraving.png':'236cba09-8bda-46f0-accc-28505c44784b',
 '05-editorial-banknote.png':'f2fe4a27-46d9-4949-aaf1-b0b60a44cd28',
 '06-dan-koe-boat.png':'9ce98f2f-e656-4a51-9705-ebd8f6cdf8cd',
 '07-dan-koe-astronaut.png':'9d39d9bd-ba84-4937-a145-a0fb488de4c2',
 '08-dan-koe-fall.png':'3599de17-2214-4295-a953-206b185febe1',
}
import shutil
for name, ident in refs.items():
    shutil.copyfile(Path('C:/Users/User/AppData/Local/Temp')/('codex-clipboard-'+ident+'.png'), REF/name)
print('Created collage:',MEDIA/'niche-research-workflow.png')
print('Converted HEIC:',MEDIA/'IMG_4666.jpg')
print('Preserved references:',REF)
