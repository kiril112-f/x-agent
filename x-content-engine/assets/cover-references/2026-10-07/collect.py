"""Download exact X Article covers from saved projected Xquik metadata.

No X APIs, cookies, article bodies, avatar substitution, or generative editing.
Pillow is used only for image validation and an unedited contact sheet.
"""
import json, hashlib, textwrap, urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
ORDER = '''adamtwtz/2038595868778233949
adamtwtz/2047050264193179804
adamtwtz/2053172056896737759
aleksascales/2100966961345655200
adamtwtz/2097073557868056925
aleksascales/2088259816296726744
PaulSolt/2042716870512353294
aureliuscajigas/2088304647014641893
PerezHatesAI/2098064168058241089
sleepclip/2095544458679026094
jasonzhou1993/2099837130927427989
jammer3k/2100632361759305949
chddaniel/2100925069765534024
PaulSolt/2045580498232373433
thedankoe/2010751592346030461
thedankoe/2101361833940791607
Zephyr_hg/2070171729373118742
jonnyscales/2102879882153730442
meetshukla_/2103014988956799196
EXM7777/2088992368695628159
NicholasDulait/2106387243803824504
devoncnp/2105345806870126935
fuckgrowth/2041580077826371733
jesseabed_
eglitisX/2103067359938527253
linoleighton/2089068010107539613
andrewyng/2088302050706686198
ErnestoSOFTWARE/2014110519913857122
aureliuscajigas/2088304647014641893
aleksascales/2088259816296726744
wickedguro/2086788813301661865'''.splitlines()
metadata = json.loads((ROOT / 'metadata.json').read_text(encoding='utf-8'))
byid = {i['sourceTweetId']: i for i in metadata['items']}

def fetch(entry):
    n, original = entry
    if '/' not in original:
        return dict(input_number=n, source_url='https://x.com/' + original, status='profile_not_specific_article', reason='Profile URL identifies no particular article cover; avatar/banner are not substituted.')
    handle, sid = original.split('/')
    item = byid[sid]
    dest = ROOT / 'originals' / f'{n:02d}-{handle}-{sid}.jpg'
    dest.parent.mkdir(exist_ok=True)
    original_url = item['article.coverMedia.mediaInfo.originalImgUrl']
    # pbs original size preserves the metadata dimensions instead of default large.
    download_url = original_url.rsplit('.', 1)[0] + '?format=jpg&name=orig'
    result = dict(input_number=n, source_url=f'https://x.com/{handle}/status/{sid}', source_tweet_id=sid, author=item['author.username'], title=item['article.title'], article_id=item['article.articleId'], cover_url=original_url, download_url=download_url, retrieval_method='Apify xquik/x-tweet-scraper article mode, projected cover metadata; HTTPS pbs.twimg.com original image', run_id='omOYKfddoXf0thSwk', dataset_id='4LyuRSFBzgm6URkUa', expected_width=item['article.coverMedia.mediaInfo.originalImgWidth'], expected_height=item['article.coverMedia.mediaInfo.originalImgHeight'])
    try:
        if not dest.exists():
            req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=45) as response:
                data = response.read()
            dest.write_bytes(data)
        with Image.open(dest) as img:
            img.load()
            result.update(width=img.width, height=img.height, format=img.format)
        result.update(status='downloaded', path=dest.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(dest.read_bytes()).hexdigest(), bytes=dest.stat().st_size)
    except Exception as exc:
        result.update(status='failed', error=str(exc))
    return result

unique, seen, duplicates = [], {}, {}
for n, original in enumerate(ORDER, 1):
    if original in seen:
        duplicates[n] = seen[original]
    else:
        seen[original] = n
        unique.append((n, original))
with ThreadPoolExecutor(max_workers=6) as executor:
    rows = list(executor.map(fetch, unique))
by_number = {r['input_number']:r for r in rows}
for n, first in duplicates.items():
    copy = dict(by_number[first])
    copy.update(input_number=n, duplicate_of_input=first, status='duplicate_reused' if copy['status']=='downloaded' else copy['status'])
    rows.append(copy)
rows.sort(key=lambda r:r['input_number'])
manifest = dict(retrieved_date='2026-10-07', source_count=31, unique_article_count=28, duplicate_count=2, profile_count=1, delivered_rows=28, article_bodies_saved=False, items=rows)
(ROOT/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')

font_path='C:/Windows/Fonts/arial.ttf'
font=ImageFont.truetype(font_path, 20)
small=ImageFont.truetype(font_path, 17)
covers=[r for r in rows if r['status']=='downloaded']
for page, start in enumerate(range(0,len(covers),8),1):
    batch=covers[start:start+8]
    cw,ch,margin=700,375,24
    row_count=(len(batch)+1)//2
    sheet=Image.new('RGB',(cw*2+margin*3,ch*row_count+margin*(row_count+1)),'#e7e7e7')
    draw=ImageDraw.Draw(sheet)
    for pos,row in enumerate(batch):
        x=margin+(pos%2)*(cw+margin); y=margin+(pos//2)*(ch+margin)
        im=Image.open(ROOT/row['path']).convert('RGB')
        thumb=ImageOps.contain(im,(cw,280))
        sheet.paste(thumb,(x+(cw-thumb.width)//2,y+(280-thumb.height)//2))
        draw.text((x,y+289),f"{row['input_number']:02d} · @{row['author']} · {row['width']}×{row['height']}",fill='#111111',font=font)
        label_title=''.join(c for c in row['title'] if ord(c)<65536).strip()
        for line_number,line in enumerate(textwrap.wrap(label_title,width=74)[:2]):
            draw.text((x,y+317+line_number*22),line,fill='#333333',font=small)
    sheet.save(ROOT/f'contact-sheet-{page:02d}.jpg',quality=94)

md=['# Original X Article cover library — 2026-10-07','', '28 unique article covers; 31 supplied links, including two duplicates and one profile. Cover metadata only was retrieved locally; article bodies were not saved.','', 'Source: Apify `xquik/x-tweet-scraper`, run `omOYKfddoXf0thSwk`, dataset `4LyuRSFBzgm6URkUa`. Covers downloaded from the `article.coverMedia.mediaInfo.originalImgUrl` field using original-size CDN URLs.','', 'The Jesse Abed URL is a profile, not a specific article. No avatar/banner was substituted.','', '| # | Author / title | Local cover | Status |','|---|---|---|---|']
for r in rows:
    title=r.get('title',r['source_url']).replace('|',' / ')
    source=f"[{r.get('author','Jesse Abed')} — {title}]({r['source_url']})"
    cover=f"[image]({r['path']})" if 'path' in r else '—'
    md.append(f"| {r['input_number']} | {source} | {cover} | {r['status']} |")
md += ['', 'Contact sheets: ' + ' · '.join(f'[sheet {i}](contact-sheet-{i:02d}.jpg)' for i in range(1,5)), '', 'Manifest includes source URLs, cover URLs, dimensions, checksums, retrieval route and duplicate linkage. Existing 2026-10-05 images were retained independently; this library has exact article provenance.']
(ROOT/'README.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps({'downloaded':len(covers),'failed':[r['input_number'] for r in rows if r['status']=='failed'],'manifest':str(ROOT/'manifest.json')}))
