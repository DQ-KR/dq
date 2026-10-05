import re, base64, io, sys
from PIL import Image, ImageChops
from crops import CROPS
S='/tmp/claude-0/-home-user-dq/11c67a3c-075f-5213-9dc2-1b7a08590888/scratchpad/w/img/'
def img_b64(k):
    l,t,r,b=CROPS[k]; im=Image.open(S+k+'.jpg').convert('RGB'); W,H=im.size
    im=im.crop((int(l*W),int(t*H),int(r*W),int(b*H)))
    bb=ImageChops.difference(im,Image.new('RGB',im.size,'white')).point(lambda p:255 if p>18 else 0).getbbox()
    if bb: im=im.crop(bb)
    if im.width>520: im=im.resize((520,int(im.height*520/im.width)))
    buf=io.BytesIO(); im.save(buf,'JPEG',quality=78); return base64.b64encode(buf.getvalue()).decode()
src=open('content.html',encoding='utf8').read()
def fig(m):
    a=dict(re.findall(r'(\w+)="([^"]*)"',m.group(0)))
    star=f'<span class="star">📌 {a["star"]}</span>' if 'star' in a else ''
    cls=' hl' if star else ''
    return f'<figure class="{cls}"><img src="data:image/jpeg;base64,{img_b64(a["id"])}">{star}<figcaption>{a.get("cap","")}</figcaption></figure>'
src=re.sub(r'<fig [^>]*/>',fig,src)
src=re.sub(r'\[\[([\d\* ]+)\]\]',lambda m:''.join(f'<span class="y">’{y}</span>' for y in m.group(1).split()),src)
src=re.sub(r'==(.+?)==',r'<mark>\1</mark>',src)
css='''
@page{size:A4;margin:9mm}
*{box-sizing:border-box}
body{font-family:'NanumGothic','Nanum Gothic',sans-serif;font-size:9.2pt;line-height:1.42;color:#1a1a1a;margin:0 auto;max-width:900px;padding:8px}
h1{font-size:16pt;margin:0 0 2px;color:#14365d}h2{font-size:12.5pt;margin:14px 0 6px;padding:3px 8px;background:#14365d;color:#fff;border-radius:3px;break-after:avoid}
h3{font-size:10.5pt;margin:0 0 3px;color:#14365d;border-bottom:1.5px solid #14365d}
.sub,.note{font-size:8.3pt;color:#555;margin:2px 0 6px}
mark{background:#7CFC00;background:rgba(124,252,0,.62);padding:0 1px;border-radius:2px;color:inherit}
.legend{border:1px solid #bbb;padding:5px 8px;font-size:8.3pt;display:flex;flex-wrap:wrap;gap:4px 14px;margin:6px 0;border-radius:4px;background:#fafafa}
.y{display:inline-block;font-size:7pt;background:#e8eef7;color:#14365d;border-radius:8px;padding:0 4px;margin:0 1px;font-weight:bold}
.chipk .y{}
.card{display:grid;grid-template-columns:1fr 205px;gap:8px;margin:0 0 8px;padding-bottom:6px;border-bottom:1px dashed #ccc;break-inside:avoid-page}
.card:not(:has(.figs)){grid-template-columns:1fr}
ul{margin:2px 0;padding-left:15px}li{margin:1px 0}
.figs{display:flex;flex-wrap:wrap;gap:4px;align-content:flex-start}
figure{margin:0;width:calc(50% - 2px);position:relative}figure img{width:100%;display:block;border:1px solid #ccc}
figure:only-child,figure.hl{width:100%}
figcaption{font-size:7pt;color:#555;text-align:center}
.star{position:absolute;top:2px;left:2px;background:#ff6a00;color:#fff;font-size:6.8pt;font-weight:bold;padding:0 4px;border-radius:3px}
figure.hl img{border:2px solid #ff6a00}
.q{border:1px solid #6aa84f;background:#f4fbef;border-radius:4px;padding:3px 7px;margin:4px 0;font-size:8.4pt}
.q ul{list-style:none;padding-left:4px;margin:1px 0 3px}
.q li.o::before{content:"○ ";color:#1b8a2f;font-weight:bold}.q li.x::before{content:"✕ ";color:#c0392b;font-weight:bold}
.q li.o{color:#14532d;font-weight:bold}
.o2{color:#14532d;font-weight:bold}.x2{color:#444}
.add{border:1.5px dashed #8e44ad;background:#f8f0fc;border-radius:4px;padding:3px 7px;margin:4px 0;font-size:8.4pt}
.addtag{background:#8e44ad;color:#fff;font-size:7pt;font-weight:bold;border-radius:3px;padding:0 4px}
.starx{color:#ff6a00;font-weight:bold}.chipx{font-style:normal;background:#e3f4d8;border:1px solid #6aa84f;padding:0 4px;border-radius:3px}
table{border-collapse:collapse;width:100%;margin:4px 0;font-size:8.4pt}th,td{border:1px solid #bbb;padding:2px 5px;vertical-align:top}th{background:#e8eef7}
table.sum td:first-child{font-weight:bold;white-space:nowrap}
@media print{body{max-width:none;padding:0}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
@media(max-width:640px){.card{grid-template-columns:1fr}}
'''
html=f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>피부과 강의록 정리 + 족보</title><style>{css}</style></head><body>{src}</body></html>'
open('derm_notes.html','w',encoding='utf8').write(html)
print(len(html)/1e6,'MB')
