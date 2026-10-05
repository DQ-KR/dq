# -*- coding: utf-8 -*-
import os, re, html
from PIL import Image
import qdb

OUT = '/home/user/dq/output/'
CIRC = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭'
def circ(n): return CIRC[n-1]

CSS = r'''
:root{--navy:#14365d;--line:#cfd6e0;--bg:#fff;--soft:#f5f7fb;--ink:#1a1a1a}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'NanumGothic','Nanum Gothic','Malgun Gothic','Apple SD Gothic Neo',sans-serif;font-size:10.5pt;line-height:1.55;color:var(--ink);margin:0 auto;max-width:1000px;padding:14px 16px;background:var(--bg)}
h1{font-size:19pt;margin:6px 0 2px;color:var(--navy)}
h2{font-size:14pt;margin:22px 0 8px;padding:5px 10px;background:var(--navy);color:#fff;border-radius:4px;break-after:avoid;page-break-after:avoid}
h3.pb{break-before:page;page-break-before:always}
h3{font-size:12pt;margin:16px 0 6px;color:var(--navy);border-bottom:2px solid var(--navy);padding-bottom:2px;break-after:avoid;page-break-after:avoid}
h4{font-size:11pt;margin:0 0 4px;color:var(--navy);break-after:avoid;page-break-after:avoid}
.sub,.note{font-size:9pt;color:#555;margin:2px 0 8px}
nav.toc{border:1px solid var(--line);background:var(--soft);padding:8px 14px;border-radius:6px;margin:10px 0;font-size:9.5pt}
nav.toc a{color:var(--navy);text-decoration:none;margin-right:12px;white-space:nowrap}
nav.toc a:hover{text-decoration:underline}
.exam-highlight{background:linear-gradient(transparent 35%,#b7f7c1 35%,#b7f7c1 90%,transparent 90%);padding:0 2px;border-radius:2px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
sup.qr{font-size:7pt;color:#1b7a34;font-weight:bold;margin-left:1px}
.legend{border:1px solid var(--line);padding:6px 10px;font-size:9pt;border-radius:6px;background:var(--soft);display:flex;flex-wrap:wrap;gap:4px 16px}
.concept{margin:0 0 14px;padding:8px 10px 8px;border:1px solid var(--line);border-radius:6px;break-inside:avoid;page-break-inside:avoid}
.concept.long{break-inside:auto;page-break-inside:auto}
.concept.long .fwe{display:block;break-inside:auto;page-break-inside:auto}
.concept.long .figs{flex-direction:row;flex-wrap:wrap;margin-top:6px}
.concept.long .figs>figure,.concept.long .figs>.figrow{flex:1 1 30%;min-width:30%}
.concept.long .figs>.figrow{flex:1 1 60%}
.concept h4 .meta{font-weight:normal;font-size:8.5pt;color:#444;margin-left:8px}
.stars{color:#d4891a;letter-spacing:1px;font-size:10pt}
.def{margin:2px 0 4px;padding:3px 8px;background:#eef3fb;border-left:4px solid var(--navy);border-radius:3px}
.fwe{display:grid;grid-template-columns:minmax(0,58%) minmax(0,40%);gap:2%;align-items:start;break-inside:avoid;page-break-inside:avoid}
.fwe.wide{grid-template-columns:1fr}
.fwe .tx ul{margin:2px 0;padding-left:17px}.fwe .tx li{margin:1px 0}
.figs{display:flex;flex-direction:column;gap:6px;margin-bottom:8px}
figure{margin:0;break-inside:avoid;page-break-inside:avoid}
figure img{display:block;width:100%;height:auto;border:1px solid var(--line)}
figcaption{font-size:8pt;color:#444;line-height:1.3;margin-top:2px}
figcaption b{color:#14365d}
.badge{display:inline-block;background:#ff6a00;color:#fff;font-size:7.5pt;font-weight:bold;padding:0 5px;border-radius:3px;margin-right:3px}
figure.hl img{border:2px solid #ff6a00}
.fwe.wide .figs,.concept.long .figs{flex-direction:row;flex-wrap:wrap;margin-top:6px}
.figrow{display:flex;gap:8px;flex-wrap:wrap}
.figrow figure{flex:1 1 40%}
.exam-line{margin-top:6px;padding:4px 8px;background:#f1fbf3;border:1px solid #8fd19e;border-radius:4px;font-size:9pt}
.exam-line b{color:#1b7a34}
.kp{margin:3px 0;font-size:9.5pt}
.kp::before{content:"핵심 포인트 ";font-weight:bold;color:#b25a00}
table{border-collapse:collapse;width:100%;margin:6px 0;font-size:9.3pt}
th,td{border:1px solid #bbb;padding:3px 6px;vertical-align:top}
th{background:#e8eef7}
tr{break-inside:avoid;page-break-inside:avoid}
.flow{display:flex;flex-wrap:wrap;align-items:center;gap:4px;margin:4px 0}
.flow span{border:1px solid var(--navy);border-radius:4px;padding:2px 8px;background:#fff}
.flow i{font-style:normal;color:var(--navy);font-weight:bold}
.tag{display:inline-block;font-size:7.5pt;font-weight:bold;border-radius:3px;padding:0 5px;color:#fff}
.t-ok{background:#1b7a34}.t-inf{background:#c77700}.t-no{background:#b0382d}.t-hold{background:#6b6f76}
.q{border:1px solid var(--line);border-radius:6px;margin:8px 0;padding:6px 10px;break-inside:avoid;page-break-inside:avoid}
.q .qh{display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-weight:bold;color:var(--navy)}
.q ol{margin:4px 0 4px 0;padding-left:0;list-style:none}
.q ol li{margin:1px 0}
.q ol li.ans{font-weight:bold;color:#14532d}
.q ol li.ans::after{content:' ✔ 정답';font-size:8pt;color:#1b7a34}
.q .row{font-size:9.3pt;margin:2px 0}
.q .row b{color:#14365d}
.q img{max-width:100%;height:auto;border:1px solid var(--line);display:block}
.mini{font-size:8.5pt;color:#555}
footer.page-note{margin-top:20px;font-size:8.5pt;color:#555;border-top:1px solid var(--line);padding-top:6px}
@page{size:A4;margin:12mm 11mm 14mm 11mm}
@media print{body{max-width:none;padding:0;font-size:9.6pt}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}nav.toc a{color:#000}.noprint{display:none}}
@media(max-width:700px){.fwe{grid-template-columns:1fr}body{padding:10px}}
'''

def img_tag(fn, folder='강의록', alt='', maxnat=True):
    p = OUT + f'assets/{folder}/{fn}'
    with Image.open(p) as im: w, h = im.size
    st = f' style="max-width:{w}px"' if maxnat else ''
    return f'<img src="assets/{folder}/{fn}" alt="{html.escape(alt)}" width="{w}" height="{h}"{st}>'

def find_img(stem):
    for f in os.listdir(OUT + 'assets/강의록'):
        if f.startswith(stem + '_'): return f
    raise FileNotFoundError(stem)

LECT = {'L1': '강의① 표피 및 부속기의 모반과 종양', 'L2': '강의② 색소 이상증 & 피부노화', 'L3': '강의③ 구진비늘질환'}
def fig(stem, cap, badge='', w=None):
    sty = f' style="flex:0 0 {w}%;max-width:{w}%"' if w else ''
    f = find_img(stem); m = re.search(r'_(l\d)p(\d+)\.', f)
    src = f'{LECT[m.group(1).upper()]} p.{int(m.group(2))}'
    hl = ' class="hl"' if badge else ''
    b = f'<span class="badge">📌 {badge}</span>' if badge else ''
    return f'<figure{hl}{sty}>{img_tag(f, alt=cap)}<figcaption>{b}<b>{cap}</b><br>그림 출처: {src}</figcaption></figure>'

def hl(text, n): return f'<span class="exam-highlight">{text}</span><sup class="qr">{circ(n)}</sup>'

def exam_line(cids):
    rows = []
    for c in cids:
        qs = [q for q in qdb.INC if q['c'] == c]
        labs = ' · '.join(qdb.qlabel(q['id']) for q in qs)
        rows.append(f'<div><b>{circ(c)} {qdb.CONCEPTS[c][0]}</b> — 출제 {len(qs)}회 · 최근 {qdb.recent(c)} · <span class="stars">{qdb.star_str(qdb.stars(c))}</span><br><span class="mini">[족보: {labs}]</span></div>')
    return '<div class="exam-line">📗 <b>족보 연계</b>' + ''.join(rows) + '</div>'

def no_exam_line(txt='이번 족보에서 강의자료만으로 풀 수 있는 출제 문항 없음'):
    return f'<div class="exam-line" style="background:#f6f6f6;border-color:#ccc">📗 <b>족보 연계</b> {txt}</div>'

def page(title, body, js=''):
    return f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{CSS}</style></head><body>{body}{js}</body></html>'
