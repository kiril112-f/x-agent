from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
import json

root=Path(__file__).resolve().parents[2]/'assets'/'covers'/'us-social-setup'
media=Path(__file__).resolve().parent/'media'
W,H=2500,1000
bg=ImageOps.fit(Image.open(media/'730895729222269935f59393f520f736.jpg').convert('RGB'),(W,H),centering=(.5,.41))
bg=bg.filter(ImageFilter.GaussianBlur(16))
bg=ImageEnhance.Brightness(bg).enhance(.36).convert('RGBA')

def face(size):
    f=ImageFont.truetype('C:/Windows/Fonts/Inter-VariableFont_opszwght.ttf',size)
    f.set_variation_by_axes([32,900])
    return f

def text_layer(text,size,tracking):
    font=face(size)
    lengths=[font.getlength(c) for c in text]
    width=round(sum(lengths)+tracking*(len(text)-1))
    lay=Image.new('RGBA',(width+30,size*2))
    d=ImageDraw.Draw(lay)
    x=10
    for c,length in zip(text,lengths):
        d.text((x,0),c,font=font,fill='white',stroke_width=0)
        x+=length+tracking
    return lay.crop(lay.getbbox())

# Two scales, one real black weight; centered by actual glyph bounds.
hero=text_layer('US traffic',455,-20)
sub=text_layer('from abroad',158,-6)
bg.alpha_composite(hero,((W-hero.width)//2,360))
bg.alpha_composite(sub,((W-sub.width)//2,745))

# A single compact cluster of original app icons, analogous to reference 01.
icons=['tiktok-app-store.jpg','instagram-app-store.jpg','youtube-app-store.jpg']
for i,(name,angle) in enumerate(zip(icons,[-12,0,12])):
    ic=Image.open(root/'icons'/name).convert('RGBA').resize((165,165),Image.Resampling.LANCZOS)
    mask=Image.new('L',ic.size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,164,164),radius=39,fill=255)
    ic.putalpha(mask)
    ic=ic.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
    x=1010+i*164-ic.width//2+82
    bg.alpha_composite(ic,(x,230-ic.height//2))

out=root/'cover-5x2-v3.png'
bg.convert('RGB').save(out,optimize=True)
bg.convert('RGB').resize((500,200),Image.Resampling.LANCZOS).save(root/'cover-5x2-v3-mobile.png')
print(json.dumps({'size':[W,H],'hero_width':hero.width,'hero_width_fraction':round(hero.width/W,3),'hero_height':hero.height,'center_x':W/2,'weight':900,'file':str(out)}))
