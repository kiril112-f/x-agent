"""Compare the actual exported candidate with reference 06 at identical sizes."""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
p=argparse.ArgumentParser()
p.add_argument('--label',default='Current candidate')
p.add_argument('--out',default='reference-comparison.jpg')
args=p.parse_args()
ref=ROOT/'x-content-engine/assets/cover-references/2026-10-07/originals/06-aleksascales-2088259816296726744.jpg'
output=Image.new('RGB',(1000,1100),'#e8e7e3')
d=ImageDraw.Draw(output)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
for y,path,label in [(40,ref,'Reference 06'),(490,HERE/'final/05-glass.png',args.label)]:
    im=Image.open(path).convert('RGB')
    output.paste(im.resize((1000,400),Image.Resampling.LANCZOS),(0,y))
    d.text((12,y-33),label,font=font,fill='black')
for x,path in [(80,ref),(580,HERE/'final/05-glass.png')]:
    output.paste(Image.open(path).convert('RGB').resize((340,136),Image.Resampling.LANCZOS),(x,940))
output.save(HERE/args.out,quality=95)
