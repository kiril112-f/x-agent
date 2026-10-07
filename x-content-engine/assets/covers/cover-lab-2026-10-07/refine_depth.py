"""Compose real app artwork into generated glass housings; no generated logo lettering."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
from build_lab import HERE, text, picture, rebuild


def app_tile(name, angle):
    casing = Image.open(HERE / "assets/glass-casing.png").convert("RGBA")
    # Measured front face in the inspected 1280 px generated casing.
    icon = Image.open(HERE / f"assets/{name}-app-store.jpg").convert("RGBA").resize((698,698), Image.Resampling.LANCZOS)
    mask = Image.new("L", icon.size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,697,697), radius=116, fill=255)
    icon.putalpha(mask)
    casing.alpha_composite(icon, (268,272))
    # Generated cutouts include alpha 1–8 noise far outside the visible silhouette.
    # Bounding on alpha>0 left invisible margins and made our ground shadows float.
    bounds = casing.getchannel("A").point(lambda p:255 if p>8 else 0).getbbox()
    casing = casing.crop((max(0,bounds[0]-5),max(0,bounds[1]-5),min(casing.width,bounds[2]+5),min(casing.height,bounds[3]+5)))
    casing = casing.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    casing.save(HERE / f"assets/{name}-glass.png")


def revise():
    app_tile("tiktok", 3)
    app_tile("instagram", -2)
    # Surface illumination plus two shared-baseline contact shadows.
    import numpy as np
    yy,xx=np.mgrid[0:800,0:2000]
    t=yy/799
    a=np.array([27,64,200]); b=np.array([8,24,95])
    rgb=a[None,None,:]*(1-t[:,:,None])+b[None,None,:]*t[:,:,None]
    glow=np.exp(-(((xx-850)/650)**2+((yy-650)/230)**2))
    rgb+=glow[:,:,None]*np.array([8,22,55])
    Image.fromarray(np.clip(rgb,0,255).astype('uint8')).save(HERE/'assets/blue-stage.png')
    ground=Image.new('RGBA',(2000,800))
    for box,opacity,blur in [((585,710,1200,758),85,20),((639,723,916,741),155,6),((892,723,1168,741),155,6)]:
        layer=Image.new('RGBA',ground.size)
        ImageDraw.Draw(layer).ellipse(box,fill=(0,3,22,opacity))
        ground.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))
    ground.save(HERE/'assets/contact-shadows.png')
    layers = [picture("blue-stage", fit="cover"),
        text("the", [165,100,300,105], 132, weight=750, fill="#ffffff", tracking=-3),
        text("organic", [145,130,1710,455], 485, min_size=440, weight=850, fill="#ffffff", tracking=-14),
        text("playbook", [1160,500,740,185], 182, min_size=165, weight=750, fill="#ffffff", tracking=-5),
        picture("contact-shadows", fit="cover"),
        picture("tiktok-glass", [620,435,300,300]),
        picture("instagram-glass", [870,435,300,300])]
    spec = dict(size=[2000,800], layers=layers, practice_only=True,
        status="agent revision after explicit rejection of v1; awaiting user review",
        reference_ids=[6,11,31], concept="Two real distribution platforms in front of oversized lettering",
        logo_source="Original App Store artwork; logos composited as source pixels into generated housings")
    (HERE / "final/05-glass.json").write_text(json.dumps(spec,indent=2),encoding="utf-8")
    rebuild()


if __name__ == "__main__":
    revise()
