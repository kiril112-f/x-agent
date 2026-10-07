"""Six distinct cover studies; editable specs and same-size reference comparisons."""
import importlib.util
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'x-content-engine/INDEX.md').exists())
sp=importlib.util.spec_from_file_location('cover',ROOT/'.agents/skills/x-cover-compose/scripts/render_cover.py')
renderer=importlib.util.module_from_spec(sp);sp.loader.exec_module(renderer)
FONTS=Path('C:/Windows/Fonts')
LIB=ROOT/'x-content-engine/assets/cover-references/2026-10-07'
refs={i['input_number']:i for i in json.loads((LIB/'manifest.json').read_text(encoding='utf-8-sig'))['items'] if i['status']=='downloaded'}
STUDIES=[
 ('01-glass',6,'Transparent 3D glass','Real platform identity rendered as translucent material, not an opaque app tile.'),
 ('02-monochrome',15,'Philosophical engraving','Visibility is a deliberate act: a person pulls back a curtain to reveal a horizon.'),
 ('03-editorial',17,'Warm editorial engraving','One repeatable mechanism converts an operator\'s input into repeated output.'),
 ('04-cinematic',19,'Cinematic object','A paper plane makes the idea of work reaching its audience tangible.'),
 ('05-collage',12,'Tactile monochrome collage','Attention comes from a human gaze; torn paper makes the visual editorial rather than technological.'),
 ('06-blueprint',20,'System / blueprint','Distribution is a designed route linking an idea, its form and an audience.')]

def txt(text,box,size,**kw):return dict(type='text',text=text,box=box,size=size,**kw)
def pic(name,box=(0,0,2000,800),**kw):return dict(type='image',path='../assets/'+name+'.png',box=box,**kw)
def stage(name,top,bottom,glowcolor=(0,0,0),center=(1000,600)):
    y,x=np.mgrid[0:800,0:2000];t=y/799
    rgb=np.array(top)[None,None,:]*(1-t[:,:,None])+np.array(bottom)[None,None,:]*t[:,:,None]
    g=np.exp(-(((x-center[0])/750)**2+((y-center[1])/300)**2))
    rgb+=g[:,:,None]*np.array(glowcolor)
    Image.fromarray(np.clip(rgb,0,255).astype('uint8')).save(HERE/'assets'/f'{name}.png')

def initial_specs():
    stage('blue-stage',(17,63,180),(5,26,92),(0,20,30),(850,650))
    stage('dark-stage',(12,14,16),(5,6,8),(35,19,7),(1450,650))
    s={}
    s['01-glass']=dict(layers=[pic('blue-stage',fit='cover'),
        txt('the',[165,100,300,105],132,weight=750,fill='white',tracking=-3),
        txt('organic',[145,130,1710,455],485,min_size=440,weight=850,fill='white',tracking=-14),
        txt('playbook',[1155,500,745,185],182,min_size=165,weight=750,fill='white',tracking=-5),
        pic('01-glass-v1',[525,367,715,420])])
    s['02-monochrome']=dict(layers=[pic('02-monochrome-v1',fit='cover')])
    s['03-editorial']=dict(background='#f4ead5',layers=[
        txt('build',[95,145,920,245],300,min_size=250,font='serif',fill='#321d14',tracking=-9),
        txt('once.',[95,445,925,260],300,min_size=250,font='serif-italic',fill='#8d391e',tracking=-8),
        pic('03-editorial-v1',[710,115,1220,650])])
    s['04-cinematic']=dict(layers=[pic('dark-stage',fit='cover'),
        txt('MAKE IT',[90,110,1040,220],260,min_size=225,font='condensed',fill='#f7f0df',tracking=-5),
        txt('TRAVEL.',[90,365,1040,265],290,min_size=245,font='condensed',fill='#f7f0df',tracking=-5),
        dict(type='rect',box=[95,690,270,16],fill='#ff641c'),
        pic('04-cinematic-v1',[810,45,1150,740])])
    s['05-collage']=dict(background='#101011',layers=[
        txt('attention',[95,75,1810,330],350,min_size=300,font='serif',fill='#f4f0e5',tracking=-11),
        txt('is earned.',[95,535,920,185],180,min_size=150,font='serif-italic',fill='#f4f0e5',tracking=-5),
        pic('05-collage-v1',[820,250,1120,510])])
    s['06-blueprint']=dict(background='#102638',layers=[])
    ls=s['06-blueprint']['layers']
    for x in range(0,2000,80):ls.append(dict(type='line',points=[x,0,x,800],fill='#163346',stroke=1))
    for y in range(0,800,80):ls.append(dict(type='line',points=[0,y,2000,y],fill='#163346',stroke=1))
    ls.extend([txt('design',[90,105,1030,280],310,min_size=275,weight=850,fill='#f5f4e9',tracking=-10),
        txt('the route',[90,440,1030,210],215,min_size=185,weight=700,fill='#f5f4e9',tracking=-7),
        dict(type='line',points=[1190,190,1670,190,1780,300,1780,410,1460,410,1300,570,1300,655,1820,655],fill='#f26c3c',stroke=13)])
    for x,y,label in [(1240,190,'IDEA'),(1680,410,'FORMAT'),(1390,655,'AUDIENCE')]:
        ls.extend([dict(type='ellipse',box=[x-22,y-22,44,44],fill='#102638',outline='#f26c3c',stroke=10),
           txt(label,[x-95,y-105,420,65],58,font='mono',fill='#f5f4e9')])
    for slug,ref,title,concept in STUDIES:
        s[slug].update(size=[2000,800],practice_only=True,style=title,reference_id=ref,concept=concept,approval='unreviewed by user')
        (HERE/'final'/f'{slug}.json').write_text(json.dumps(s[slug],indent=2),encoding='utf-8')

def render_all():
    for slug,ref,title,concept in STUDIES:
        p=HERE/'final'/f'{slug}.json'
        renderer.render(p,p.with_suffix('.png'),FONTS)
        print('Rendered',slug)

def comparisons():
    font=ImageFont.truetype(str(FONTS/'arial.ttf'),22)
    thumbs=Image.new('RGB',(740,600),'#e8e5dc');td=ImageDraw.Draw(thumbs)
    overview=Image.new('RGB',(1600,1200),'#e8e5dc');od=ImageDraw.Draw(overview)
    for i,(slug,ref,title,concept) in enumerate(STUDIES):
        a=Image.open(LIB/refs[ref]['path']).convert('RGB');b=Image.open(HERE/'final'/f'{slug}.png').convert('RGB')
        out=Image.new('RGB',(1000,1100),'#e8e5dc');d=ImageDraw.Draw(out)
        for y,im,label in [(40,a,f'Reference {ref:02d}'),(490,b,title)]:
            out.paste(im.resize((1000,400),Image.Resampling.LANCZOS),(0,y));d.text((12,y-30),label,font=font,fill='#111111')
        out.paste(a.resize((340,136),Image.Resampling.LANCZOS),(75,940));out.paste(b.resize((340,136),Image.Resampling.LANCZOS),(585,940))
        out.save(HERE/'comparisons'/f'{slug}.jpg',quality=94)
        x,y=(i%2)*800+20,(i//2)*400+20
        overview.paste(b.resize((760,304),Image.Resampling.LANCZOS),(x,y));od.text((x,y+318),f'{i+1:02d} / {title}',font=font,fill='#111111')
        x,y=(i%2)*370+15,(i//2)*200+15
        thumbs.paste(b.resize((340,136),Image.Resampling.LANCZOS),(x,y));td.text((x,y+143),f'{i+1:02d} / {title}',font=font,fill='#111111')
    overview.save(HERE/'six-styles.jpg',quality=95);thumbs.save(HERE/'thumbnails.png')

def gallery():
    import html
    ru=[('Прозрачное 3D-стекло','Стекло передаёт фон через тело. Знаки сгенерированы вместе с материалом по референсу.'),
        ('Философская ч/б гравюра','Человек открывает занавес: видимость начинается с действия. Метафора, а не случайный фантастический пейзаж.'),
        ('Тёплая журнальная гравюра','Один оператор и повторяемый механизм. Бумага, рустовая краска и отдельно набранный serif.'),
        ('Кинематографический объект','Работа должна добраться до людей: бумажный самолёт как физическая метафора распространения.'),
        ('Монохромный коллаж','В центре внимания — человек. Рваная бумага, один взгляд и собранная типографика.'),
        ('Техническая схема','Идея → формат → аудитория. Настоящая логика маршрута вместо декоративных сетей.')]
    cards=[]
    for i,(slug,ref,title,concept) in enumerate(STUDIES):
        src='../../../cover-references/2026-10-07/'+refs[ref]['path']
        cards.append(f'''<article><a href="final/{slug}.png"><img src="final/{slug}.png" alt="{ru[i][0]}"></a><h2>{i+1:02d} / {ru[i][0]}</h2><p>{ru[i][1]}</p><div class="links"><a href="final/{slug}.json">Редактируемая версия</a><a href="comparisons/{slug}.jpg">Сравнение + 340 px</a><a href="{html.escape(refs[ref]['source_url'])}">Источник ↗</a></div><details><summary>Оригинал и результат рядом</summary><div class="compare"><img src="{src}" alt="Оригинал {ref}"><img src="final/{slug}.png" alt="Наш вариант"></div></details></article>''')
    doc='''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Шесть направлений обложек</title><style>*{box-sizing:border-box}body{margin:0;background:#e9e6de;color:#20201d;font:16px/1.5 system-ui,sans-serif}main{max-width:1600px;margin:auto;padding:45px 30px 70px}.eyebrow{letter-spacing:.14em;text-transform:uppercase;font-size:12px}h1{font-size:clamp(40px,5vw,76px);line-height:1.03;letter-spacing:-.055em;max-width:1000px;margin:20px 0}header p{max-width:850px;color:#60605a}.grid{display:grid;grid-template-columns:1fr 1fr;gap:44px 26px;margin-top:45px}article{min-width:0}img{width:100%;display:block;aspect-ratio:2.5;object-fit:contain;background:#191919}h2{font-size:22px;letter-spacing:-.03em;margin:16px 0 5px}article p{font-size:14px;color:#55554e;margin:0 0 14px}.links{display:flex;gap:16px;flex-wrap:wrap;font-size:13px}a{color:inherit;text-underline-offset:3px}details{margin-top:15px;padding-top:13px;border-top:1px solid #c5c1b6}summary{cursor:pointer;font-size:13px}.compare{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:14px}.note{border-top:1px solid #c5c1b6;padding:25px 0;margin-top:55px;max-width:950px}.note p{color:#55554e}nav{display:flex;gap:20px;font-size:14px;flex-wrap:wrap;margin-top:25px}@media(max-width:750px){main{padding:25px 15px}.grid,.compare{grid-template-columns:1fr}}</style><main><header><div class="eyebrow">Round 2 · 07.10.2026</div><h1>Шесть направлений.<br>Не шесть перекрасок.</h1><p>Каждое начинается с мысли и сравнивается с отдельным оригиналом. Это учебные кандидаты, а не обещание охватов или одобренный единый стиль. Выбор для реальной статьи зависит от её тезиса.</p><nav><a href="six-styles.jpg">Все шесть одним изображением</a><a href="thumbnails.png">Проверка в ленте</a><a href="HANDOFF.txt">Текст для агента статьи</a><a href="review.md">Журнал решений</a><a href="../index.html#library">28 оригиналов</a></nav></header><div class="grid">CARDS</div><section class="note"><h2>Что теперь должен делать агент</h2><p>Понять статью → придумать связную концепцию → показать стили с картинками → собрать текст и изображение → сравнить с оригиналом и при 340 px → исправлять конкретные дефекты до результата. Количество попыток не заменяет качество.</p><p>Для стекла проверять прозрачность тела, а не только края PNG. Для философской иллюстрации — объяснимую связь с мыслью и связность действия. Текст, числа и схема остаются точно редактируемыми.</p></section></main></html>'''
    (HERE/'index.html').write_text(doc.replace('CARDS',''.join(cards)),encoding='utf-8')

if __name__=='__main__':
    import sys
    if '--init' in sys.argv:initial_specs()
    render_all();comparisons();gallery()
