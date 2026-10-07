from pathlib import Path
from markdown_it import MarkdownIt
import json, re

ROOT=Path(__file__).resolve().parent
md=(ROOT/'article.md').read_text(encoding='utf-8')
title,body=md.split('\n\n',1)
render=MarkdownIt('commonmark',{'html':True}).render

# Native X media is inserted with its own upload controls. Keep text as rich HTML.
text_only=re.sub(r'^!\[[^\]]*\]\([^)]+\)\s*$', '', body, flags=re.M)
text_only=re.sub(r'\n{3,}', '\n\n', text_only).strip()
(ROOT/'x-body.html').write_text(render(text_only),encoding='utf-8')
(ROOT/'x-title.txt').write_text(title.removeprefix('# '),encoding='utf-8')

segments=[]
cursor=0
for match in re.finditer(r'^!\[([^\]]*)\]\(([^)]+)\)',body,re.M):
    segments.append({'html':render(body[cursor:match.start()].strip()),'image':str(ROOT/match[2]),'alt':match[1]})
    cursor=match.end()
segments.append({'html':render(body[cursor:].strip()),'image':None})
(ROOT/'x-segments.json').write_text(json.dumps(segments,ensure_ascii=False,indent=2),encoding='utf-8')

full=render(md)
cover='../../assets/covers/us-social-setup/experiments-2026-10-07/01-photo.png'
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>US Audience Setup — Kirill Morozov</title><style>body{margin:0;background:#faf9f6;color:#20211e;font:19px/1.6 system-ui,sans-serif}main{max-width:780px;margin:64px auto;padding:0 28px 80px}h1{font-size:48px;line-height:1.06;letter-spacing:-1.9px;margin:36px 0}h2{font-size:29px;line-height:1.18;letter-spacing:-.6px;margin:54px 0 22px}h3{font-size:24px;line-height:1.22;margin:36px 0 18px}p{margin:0 0 24px}img{display:block;max-width:100%;max-height:760px;object-fit:contain;margin:30px auto}pre{font:15px/1.65 ui-monospace,monospace;background:#eeeae3;border-radius:12px;padding:28px;white-space:pre-wrap}a{color:#126fc4}.cover{width:100%;max-height:none}.author{font-size:14px;color:#72766e;letter-spacing:.08em}</style><main><p class="author">KIRILL MOROZOV · X ARTICLE DRAFT</p><img class="cover" src="'''+cover+'">'+full+'</main></html>'
(ROOT/'article-preview.html').write_text(html,encoding='utf-8')
words=len(re.findall(r"\b[\w’'-]+\b",text_only))
ratio=len(text_only[:text_only.index('US AUDIENCE SETUP')].split())/len(text_only.split())
print(json.dumps({'words':words,'object_start':round(ratio*100,1),'images':len(segments)-1,'save_phrase_count':body.count('make sure you save this article so you can read it later or prompt it with your agent')}))
