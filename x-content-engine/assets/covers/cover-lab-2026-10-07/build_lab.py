"""Rebuild the practice gallery from immutable image assets and editable JSON specs."""
import importlib.util
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
loader = importlib.util.spec_from_file_location("compositor", ROOT / ".agents/skills/x-cover-compose/scripts/render_cover.py")
module = importlib.util.module_from_spec(loader)
loader.loader.exec_module(module)
FONT_DIR = Path("C:/Windows/Fonts")


def text(value, box, size, **kw):
    return dict(type="text", text=value, box=box, size=size, **kw)


def picture(name, box=(0, 0, 2000, 800), **kw):
    return dict(type="image", path=f"../assets/{name}.png", box=box, **kw)


def create_specs():
    examples = {}
    examples["01-monochrome"] = dict(background="#101010", layers=[picture("engraving-v2", fit="cover")])
    examples["02-editorial"] = dict(layers=[picture("editorial", fit="cover"),
        text("Build once.", [85, 130, 1050, 170], 156, font="serif", fill="#381c10"),
        text("Publish often.", [85, 315, 1040, 155], 143, font="serif-italic", fill="#923a20")])
    examples["03-cinematic"] = dict(layers=[picture("cinematic", fit="cover"),
        text("Make content", [110, 210, 1780, 195], 218, min_size=195, weight=900, fill="#ffffff", align="center", tracking=-5),
        text("worth watching.", [110, 425, 1780, 180], 200, min_size=175, weight=900, fill="#ffffff", align="center", tracking=-5)])
    examples["04-type"] = dict(background="#f4f0e7", layers=[
        text("Less noise.", [90, 110, 1820, 265], 325, min_size=290, weight=900, tracking=-9),
        text("More signal.", [90, 425, 1820, 295], 320, min_size=260, weight=900, fill="#d94320", tracking=-9)])
    examples["05-glass"] = dict(layers=[dict(type="gradient", start="#203bbe", end="#081765"),
        text("organic", [95, 55, 1800, 360], 380, min_size=340, weight=900, fill="#ffffff", tracking=-12),
        text("installs", [95, 435, 1580, 295], 380, min_size=340, weight=900, fill="#ffffff", tracking=-12),
        picture("glass", [1450, 255, 470, 470], trim_alpha=True)])
    examples["06-system"] = dict(background="#f9f8f4", layers=[
        text("Give every slide a job.", [100, 95, 1800, 185], 171, min_size=135, weight=800, tracking=-4)])
    ls = examples["06-system"]["layers"]
    for x, label in [(100, "Hook"), (780, "Value"), (1460, "Action")]:
        ls.extend([dict(type="rect", box=[x, 370, 440, 265], outline="#222222", stroke=5, radius=16),
            text(label, [x + 20, 442, 400, 120], 105, min_size=90, weight=700, align="center", valign="center")])
    for x in (592, 1272):
        ls.extend([dict(type="line", points=[x, 502, x+135, 502], stroke=8, fill="#d94320"),
            dict(type="polygon", points=[[x+135, 502], [x+100, 479], [x+100, 525]], fill="#d94320")])
    for name, spec in examples.items():
        spec.update(size=[2000, 800], practice_only=True,
                    note="Fictional cover brief. No measured results or endorsement claimed.")
        p = HERE / "final" / f"{name}.json"
        p.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    # Actual first-pass alternatives, retained for observable comparison.
    initial = json.loads(json.dumps(examples["02-editorial"]))
    initial["layers"][1] = text("Build once.", [85, 140, 950, 160], 145, weight=850, fill="#381c10")
    initial["layers"][2] = text("Publish often.", [85, 320, 1040, 150], 140, weight=850, fill="#381c10")
    (HERE / "iterations/02-editorial-v1.json").write_text(json.dumps(initial, indent=2), encoding="utf-8")
    initial = dict(size=[2000, 800], layers=[picture("engraving", fit="cover")])
    (HERE / "iterations/01-monochrome-v1.json").write_text(json.dumps(initial, indent=2), encoding="utf-8")


def rebuild():
    for folder in ("iterations", "final"):
        for p in sorted((HERE / folder).glob("*.json")):
            if p.name.endswith(".qa.json"):
                continue
            if folder == "iterations" and p.with_suffix(".png").exists():
                continue  # Preserve observed historical renders even if shared assets later change.
            module.render(p, p.with_suffix(".png"), FONT_DIR)
            print(p.name)
    names = [p for p in sorted((HERE / "final").glob("*.png")) if not p.stem.endswith("-thumb")]
    sheet = Image.new("RGB", (1600, 1200), "#e7e6e3")
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(str(FONT_DIR / "arial.ttf"), 24)
    for i, p in enumerate(names):
        x, y = (i % 2)*800+20, (i//2)*400+20
        im = Image.open(p).convert("RGB").resize((760, 304), Image.Resampling.LANCZOS)
        sheet.paste(im, (x, y))
        d.text((x, y+320), p.stem, fill="#111111", font=font)
    sheet.save(HERE / "practice-board.jpg", quality=94)
    thumbs = Image.new("RGB", (720, 510), "#e7e6e3")
    td = ImageDraw.Draw(thumbs)
    for i, p in enumerate(names):
        x, y = (i % 2)*360+10, (i//2)*170+10
        thumbs.paste(Image.open(p.with_name(p.stem+'-thumb.png')), (x,y))
        td.text((x,y+140),p.stem[:2],font=font,fill='#111111')
    thumbs.save(HERE / 'thumbnail-board.png')


if __name__ == "__main__":
    import sys
    if "--init-specs" in sys.argv:
        create_specs()
    rebuild()
