"""Targeted layout revision after reading the v1 comparison boards."""
import json,shutil
from pathlib import Path
from build import HERE,render_all,comparisons

def snapshot(slug):
    for ext in ['.json','.png','-thumb.png','.qa.json']:
        src=HERE/'final'/(slug+ext); dst=HERE/'iterations'/(slug+'-v1'+ext)
        if not dst.exists():shutil.copy2(src,dst)
    dst=HERE/'iterations'/(slug+'-comparison-v1.jpg')
    if not dst.exists():shutil.copy2(HERE/'comparisons'/(slug+'.jpg'),dst)

for slug in ['04-cinematic','05-collage','06-blueprint']:
    snapshot(slug)
    p=HERE/'final'/(slug+'.json');spec=json.loads(p.read_text(encoding='utf-8'))
    ls=spec['layers']
    if slug=='04-cinematic':
        ls[-1]['box']=[700,15,1020,680]
        ls[2].update(size=260,min_size=250,box=[90,365,1000,240])
    elif slug=='05-collage':
        ls[0].update(size=380,min_size=340,box=[95,75,1810,350],tracking=0)
        ls[1].update(size=160,min_size=150,box=[95,430,860,175])
        ls[2]['box']=[930,310,990,450]
    else:
        for layer in ls:
            if layer.get('text')=='FORMAT':layer.update(box=[1470,300,390,65],size=64)
            if layer.get('text')=='AUDIENCE':layer.update(box=[1400,550,480,65],size=64)
    spec['revision']='documented final corrections after reference comparisons; see review.md'
    p.write_text(json.dumps(spec,indent=2),encoding='utf-8')
render_all();comparisons()
