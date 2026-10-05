# -*- coding: utf-8 -*-
import sys, html, collections; sys.path.insert(0, '/home/user/dq/tools')
from common import *
import qdb
E = html.escape
anchor = {1:'c-psoriasis',2:'c-psoriasis',3:'c-photo',4:'c-uv',5:'c-uv',6:'c-ak',7:'c-nevus',8:'c-vitiligo',9:'c-scc',10:'c-lp',11:'c-psoriasis',12:'c-uv',13:'c-pr',14:'c-bcc'}
LV = {'직접': ('t-ok', '직접'), '종합': ('t-ok', '종합'), '추론': ('t-inf', '추론')}
INC = qdb.INC
B = []
B.append('<h1>족보정리 — 두경부 및 피부(피부과) · 강의자료만으로 풀 수 있는 족보 문제</h1>')
B.append('<p class="sub">분석 족보: 17-21학번 족보(84p, 2019·2021·2022·2023·2025 복원) · 2025 시험지(10p) · 16학번본 족보(5p, 연도 미상) / 대조 강의자료: 강의① 모반·종양(25p) · 강의② 색소이상증·피부노화(34p) · 강의③ 구진비늘질환(42p). 외부 자료·인터넷은 사용하지 않았습니다.</p>')
B.append('<nav class="toc"><b>목차</b> <a href="#t1">1. 출제 경향</a><a href="#t2">2. 출제 빈도 TOP</a><a href="#t3">3. 풀 수 있는 족보 문제</a><a href="#t4">4. 반복 출제 문제</a><a href="#t5">5. 문제 유형별</a><a href="#t6">6. 자주 틀리는 포인트</a><a href="#t7">7. 제외된 문제</a></nav>')
B.append('<div class="legend"><span><span class="tag t-ok">직접/종합</span> 강의자료에 정답 근거가 존재 / 여러 슬라이드 결합</span><span><span class="tag t-inf">추론</span> 강의 근거로 소거·추론</span><span><span class="tag t-no">NO</span> 강의자료만으로 풀 수 없음</span><span><span class="tag t-hold">판단 보류</span></span><span>🟢 강의자료만으로 풀이 가능 = O</span></div>')

# ---------- 1. 경향 ----------
nlec = collections.Counter();
for q in INC:
    nlec['강의①' if q['c'] in (6,7,9,14) else '강의②' if q['c'] in (4,5,8,12) else '강의③'] += 1
byyear = collections.Counter()
for q in INC:
    p = q['id'].split('-')[0]; byyear[qdb.SRC[p]] += 1
typ = collections.Counter()
for q in INC:
    for t in q['typ'].split('·'): typ[t] += 1
lv = collections.Counter(q['level'] for q in INC)
B.append('<h2 id="t1">1. 전체 출제 경향</h2>')
B.append(f'<div class="exam-line"><b>분석 결과 요약</b><br>강의 범위 내 족보 문항 {len(INC)+len(qdb.EXC)}개 중 <b>강의자료만으로 풀이 가능 {len(INC)}개 (🟢 O)</b>, 제외·판단 보류 {len(qdb.EXC)}개. '
         f'근거 수준: 직접 {lv["직접"]} · 종합 {lv["종합"]} · 추론 {lv["추론"]}. (2025 족보 복원본의 5문항은 2025 시험지와 동일 문항이라 중복 집계하지 않았고 시험지 기준으로 집계)</div>')
B.append('<table><tr><th>구분</th><th>내용</th></tr>'
 f'<tr><td>가장 많이 출제된 단원</td><td>강의③ 구진비늘질환 {nlec["강의③"]}문항 (건선 중심) &gt; 강의① {nlec["강의①"]}문항 = 강의② {nlec["강의②"]}문항</td></tr>'
 '<tr><td>가장 많이 출제된 개념</td><td>건선(역학·악화요인 / 관절염 / 치료) · UVA·UVB 특성 · 암전구증 · 진피 melanocytic lesion — 각 4회</td></tr>'
 '<tr><td>반복 출제 문제</td><td>2021→2022→2023→2025 동일 선지 구성이 거의 그대로 반복된 문항군 9개(§4). 족보 해설에도 “왕족/족보 그대로”로 표시</td></tr>'
 '<tr><td>문제 유형</td><td>전부 객관식(5지선다 위주). 설명 선지형 다수, 사진 제시형(건선·백반증·편평태선·장미색잔비늘증), 정의형 단답 1문항. 계산·서술형 출제 없음</td></tr>'
 '<tr><td>최근 출제 경향(2025 시험지)</td><td>건선 3문항(73–75: 역학·관절염·치료) · UV 2문항(76–77) · 진피 melanocytosis 1(78) · 백반증 1(79, 사진) · 암전구증 1(80) · SCC 고위험 1(81) = 한형진 파트 9문항</td></tr>'
 '<tr><td>2025 새로 등장</td><td>UV 해로운 작용(77)·SCC 고위험 인자의 “일광각화증 유래/3cm” 선지 — 이전 연도에는 없던 선지 구성(강의자료로 도출)</td></tr></table>')
B.append('<h3>출처별 풀이 가능 문항 수</h3><table><tr><th>출처</th>' + ''.join(f'<th>{k}</th>' for k in byyear) + '</tr><tr><td>문항 수</td>' + ''.join(f'<td>{v}</td>' for v in byyear.values()) + '</tr></table>')

# ---------- 2. TOP ----------
B.append('<h2 id="t2">2. 출제 빈도 TOP (개념별)</h2>')
rows = ''
order = sorted(qdb.CONCEPTS, key=lambda c: (-qdb.count(c), -qdb.stars(c), c))
for i, c in enumerate(order, 1):
    rows += f'<tr><td>{i}</td><td>{circ(c)} {qdb.CONCEPTS[c][0]}</td><td>{qdb.count(c)}</td><td>{qdb.recent(c)}</td><td class="stars">{qdb.star_str(qdb.stars(c))}</td></tr>'
B.append('<table><tr><th>순위</th><th>개념</th><th>출제 횟수</th><th>최근 출제</th><th>중요도</th></tr>' + rows + '</table>')
B.append('<p class="note">※ 풀 수 있는 문항에서 추출된 개념이 14개뿐이어서 TOP 30을 채울 수 없습니다(억지로 늘리지 않음). 같은 개념을 다른 방식으로 물은 문제는 별개 출제 사례로 집계. 별점은 학습 우선순위이며 실제 출제 확률이 아닙니다.</p>')

# ---------- 3. 문제 카드 ----------
B.append('<h2 id="t3">3. 강의자료만으로 풀 수 있는 족보 문제 (🟢 O)</h2>')
IMGQ = {'E25-73': '2025_exam_q73_question.png', 'E25-79': '2025_exam_q79_question.png'}
for c in sorted(qdb.CONCEPTS):
    qs = [q for q in INC if q['c'] == c]
    B.append(f'<h3>{circ(c)} {qdb.CONCEPTS[c][0]} <span class="meta mini">출제 {len(qs)}회 · <span class="stars">{qdb.star_str(qdb.stars(c))}</span> · 강의록 <a href="강의록.html#{anchor[c]}">연결</a></span></h3>')
    for q in qs:
        cls, lab = LV[q['level']]
        opts = ''
        if q['id'] in IMGQ:
            opts = f'<img src="assets/족보/{IMGQ[q["id"]]}" alt="{q["id"]} 문제 이미지" style="max-width:560px">'
            ans_txt = q['ans']
        else:
            li = ''
            for i, o in enumerate(q['opts']):
                mark = qdb.CIRC if hasattr(qdb, 'CIRC') else '①②③④⑤'
                m = '①②③④⑤'[i]
                a = ' class="ans"' if m == q['ans'] else ''
                li += f'<li{a}>{m} {E(o)}</li>'
            stem_html = ''
            opts = f'<div class="row"><b>문제 원문</b> {E(q["stem"])}</div><ol>{li}</ol>'
        if q['id'] in IMGQ:
            opts = f'<div class="row"><b>문제 이미지</b></div>{opts}'
        refs = ' · '.join(q['refs'])
        note = f'<div class="row"><b>비고</b> {E(q["note"])}</div>' if q['note'] else ''
        B.append(f'<div class="q"><div class="qh"><span>{qdb.qlabel(q["id"])}</span><span class="tag {cls}">{lab}</span><span class="mini">{q["typ"]}</span></div>'
                 f'{opts}'
                 f'<div class="row">🟢 <b>강의자료만으로 풀이 가능 = O</b> · 근거 수준: <b>{q["level"]}</b> · 관련 강의: {refs}</div>'
                 f'<div class="row"><b>정답</b> {E(q["ans"])}</div>'
                 f'<div class="row"><b>해설(강의자료 근거)</b> {E(q["why"])}</div>'
                 f'<div class="row"><b>핵심 개념</b> {circ(c)} {qdb.CONCEPTS[c][0]} → <a href="강의록.html#{anchor[c]}">강의록 연결</a></div>{note}</div>')

# ---------- 4. 반복 ----------
B.append('<h2 id="t4">4. 반복 출제 문제</h2><table><tr><th>개념</th><th>출제 사례</th><th>반복 패턴</th></tr>')
pat = {1:'사진(판상 건선) + 5지선다: 50대/75%/외상 악화/스트레스 無/유병률 10% — 선지 5개가 4번 모두 동일',2:'30–40대 / 성별차 / 70% / 5% / 손톱건선 — 정답 선지만 ①↔② 위치 이동',
 3:'retinoid 1차 외용 / vit D3 2차 외용 / NBUVB / 면역조절제 안전 / 순환치료 불필요 — 3회 동일, 정답 항상 NBUVB',4:'UVA melanogenic / UVA 광노화 無 / UVB 유리창 / UVB DNA 無 / 1000배 뒤바뀜 — 4회 동일(선지 순서까지)',
 5:'급성(홍반·tanning) vs 만성(두께 증가·광노화) 구분을 매번 다른 선지로 변형',6:'광선각화증·백판증·홍색비후증·XP·(Bowen) 중 IP가 정답 — 4회 모두 정답은 IP',
 7:'Mongolian spot을 표피 목록과 대비 — 발문만 4가지로 변형',8:'임상형 3종(segmental/non-segmental/focal) 정답, 여자>남자·멘델·자가면역 무관·cellular만 오답',9:'재발 병변 / ≥2cm가 정답, 다리·1cm·2mm 오답',
 10:'Wickham striae 3회(다른 sign 오답으로 구성)',11:'정의형 단답',12:'Photosensitivity 정답 — Tanning·Vit D·NO·Pain relief 오답',13:'Herald patch',14:'BCC 한국인 포함 가장 흔한 암'}
for c in order:
    qs = [q for q in INC if q['c'] == c]
    B.append(f'<tr><td>{circ(c)} {qdb.CONCEPTS[c][0]}</td><td>{" · ".join(qdb.qlabel(q["id"]) for q in qs)}</td><td>{pat[c]}</td></tr>')
B.append('</table>')

# ---------- 5. 유형 ----------
B.append('<h2 id="t5">5. 문제 유형별 분석</h2><table><tr><th>유형</th><th>문항 수</th><th>특징·대응</th></tr>'
 f'<tr><td>객관식 (5지/4지)</td><td>{len(INC)}</td><td>전 문항 객관식. 보기 1개만 강의 문장과 일치하도록 구성</td></tr>'
 f'<tr><td>설명 선지형(옳은/옳지 않은 것)</td><td>{typ["설명 선지형"]}</td><td>수치(%, cm, mm, 나이)와 부정 표현(~하지 않는다)을 정확히 확인</td></tr>'
 f'<tr><td>사진 제시형</td><td>{typ["사진 제시형"]}</td><td>건선(강의③ p.11), 백반증(강의② p.24), 장미색잔비늘증(강의③ p.25), 구강 편평태선 — 강의 사진 그대로 출제</td></tr>'
 f'<tr><td>정의형(단답)</td><td>{typ["정의형(단답)"]}</td><td>Koebner 현상</td></tr>'
 '<tr><td>비교형 / 서술형 / 계산형 / 응용형</td><td>0</td><td>족보에 해당 유형 없음(응용: 구강 LP 사진 문제 1문항은 사진 제시형으로 집계)</td></tr></table>')

# ---------- 6. 함정 ----------
B.append('<h2 id="t6">6. 자주 틀리는 포인트</h2><ul>'
 '<li><b>UVA ↔ UVB 뒤바뀜</b>: “UVA가 UVB의 1/1000이고 광자 에너지 1000배” ✕ — UVB가 광자 에너지 1000배, 같은 홍반에 필요한 양은 UVB가 1/1000. UVB는 유리창 <u>차단</u>(✕ 통과).</li>'
 '<li><b>급성 vs 만성</b>: 홍반·tanning = 급성 / 피부 두께 증가·광노화·암 = 만성 / 광노화 = 외인성(내인성 ✕)</li>'
 '<li><b>건선 치료 순서</b>: retinoid는 외용 1차 ✕(전신), vit D3는 2차 ✕(1차). 약제(MTX 등)가 “부작용 적어 편하게” ✕.</li>'
 '<li><b>건선 수치</b>: 초발 10~30대(50대 ✕), 가족력 25%(75% ✕), 유병률 1~2%(10% ✕), PsA 6–42%(70% ✕)·35–40세(20대 ✕)·성별차 없음.</li>'
 '<li><b>백반증</b>: 성별차 없음, 유전질환 아님, 자가면역 관여(세포성+체액성), oxidative stress 관여, 임상형 3종.</li>'
 '<li><b>암전구증</b>: 목록 외 정답 IP(색소실조증). 기저세포암의 원인은 p53이 아니라 PTCH.</li>'
 '<li><b>SCC 고위험</b>: 다리·1cm·2mm·몸통·high differentiation ✕ / 입술·귀·≥2cm·≥4mm·재발·면역억제 ○.</li>'
 '<li><b>sign 구별</b>: Wickham(LP) / Auspitz(건선) / Herald patch(장미색잔비늘증) / Koebner(공통) / Pterygium(LP 손톱) / sandal(PRP).</li>'
 '<li><b>진피 vs 표피</b>: Mongolian spot만 진피 — 발문이 “악성 흑색종”으로 잘못 표기돼도 개념은 melanocytic lesion.</li></ul>')

# ---------- 7. 제외 ----------
B.append('<h2 id="t7">7. 제외된 족보 문제</h2>')
B.append('<table><tr><th>문제</th><th>출처</th><th>판정</th><th>제외 이유</th></tr>')
for qid, what, jud, why in qdb.EXC:
    tag = 't-no' if jud == 'NO' else 't-hold'
    B.append(f'<tr><td>{E(what)}</td><td>{qdb.qlabel(qid)}</td><td><span class="tag {tag}">{jud}</span></td><td>{E(why)}</td></tr>')
B.append('</table>')
B.append('<p class="note"><b>강의자료 자체가 제공되지 않은 피부 강의 문항</b>(알레르기·감염성 피부질환, 피부 구조·전신질환 피부양상 등)은 “강의자료만으로 풀이 가능 = NO”로 일괄 제외했습니다 — '
         + ' / '.join(f'{k}: {v}번' for k, v in qdb.OUT_OF_SCOPE_DERM.items()) +
         ' (확인된 22문항). 17-21학번 족보의 이비인후과·안과·치과·청각 등 다른 과목 문항은 해당 강의자료가 없으므로 개별 집계하지 않고 전체 제외했습니다.</p>')
B.append('<p class="note">[확인 필요] 16학번본 족보는 연도가 표기되어 있지 않아 “16학번본-A/B/C”로 구분했습니다(A: 37–45번 세트, B: 객17–24 세트, C: p.3의 3번). 2025 시험지 77·79·81번은 족보에 정답이 없어 강의자료 기반으로 도출한 값입니다.</p>')
open(OUT + '족보정리.html', 'w', encoding='utf8').write(page('족보정리 — 두경부 및 피부(피부과)', '\n'.join(B)))
print('ok', len(INC))
