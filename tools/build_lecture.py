# -*- coding: utf-8 -*-
import sys; sys.path.insert(0, '/home/user/dq/tools')
from common import *
import qdb

def card(cid, title, cids, defn, tx, figs='', kp='', manual_stars=None, long=False, wide=False, no_exam=None, anchor=None):
    if cids:
        n = sum(qdb.count(c) for c in cids); st = max(qdb.stars(c) for c in cids)
        meta = f'<span class="meta">출제 {n}회 · 중요도 <span class="stars">{qdb.star_str(st)}</span></span>'
        ex = exam_line(cids)
    else:
        meta = f'<span class="meta">출제 0회 · 중요도 <span class="stars">{qdb.star_str(manual_stars or 1)}</span></span>'
        ex = no_exam_line(no_exam or '이번 족보에서 강의자료만으로 풀 수 있는 출제 문항 없음')
    kpp = f'<p class="kp">{kp}</p>' if kp else ''
    fg = f'<div class="figs">{figs}</div>' if figs else ''
    long = cid in ('c-uv', 'c-psoriasis')
    cls = 'fwe wide' if (wide or not figs) else 'fwe'
    return (f'<section class="concept{" long" if long else ""}" id="{cid}"><h4>{title} {meta}</h4>'
            f'<p class="def"><b>한 줄 정의</b> {defn}</p><div class="{cls}"><div class="tx">{tx}{kpp}</div>{fg}</div>{ex}</section>')

H = hl
B = []
B.append('<h1>두경부 및 피부 — 피부과 강의록 (시험 대비)</h1>')
B.append('<p class="sub">강의자료: ① 표피 및 부속기의 모반과 종양(25p) · ② 색소 이상증 &amp; 피부노화(34p) · ③ 구진비늘질환(42p) / 족보: 17-21학번 족보(84p) · 2025 시험지(10p) · 16학번본 족보(5p)</p>')
B.append('''<nav class="toc"><b>목차</b> <a href="#s1">1. 전체 요약</a><a href="#s2">2. 강의별 상세</a><a href="#s2a">2-1 모반·종양</a><a href="#s2b">2-2 색소·노화</a><a href="#s2c">2-3 구진비늘</a><a href="#s3">3. 개념 비교</a><a href="#s4">4. 개념 간 관계</a><a href="#s5">5. 족보 연결 핵심</a><a href="#s6">6. 시험 직전 정리</a></nav>''')
B.append('''<div class="legend"><span><span class="exam-highlight">초록 하이라이트</span><sup class="qr">①</sup> = 실제 족보 출제 + 강의자료에 존재 + 해당 문제 풀이에 필요한 내용 (번호 = §5 족보 연결 개념)</span>
<span><span class="badge">📌</span> 족보에 출제된 강의 사진</span><span>★ = 학습 우선순위(출제 확률 아님)</span>
<span>[추론] [확인 필요] [판독 불가] [자료 근거 없음] = 근거 표기</span></div>''')

# ---------------- 1. 전체 요약 ----------------
B.append('<h2 id="s1">1. 시험 대비 전체 요약</h2>')
anchor = {1:'c-psoriasis',2:'c-psoriasis',3:'c-psoriasis',4:'c-uv',5:'c-uv',6:'c-ak',7:'c-nevus',8:'c-vitiligo',9:'c-scc',10:'c-lp',11:'c-psoriasis',12:'c-uv',13:'c-pr',14:'c-bcc'}
rows = ''
for c in sorted(qdb.CONCEPTS, key=lambda c: (-qdb.stars(c), -qdb.count(c), c)):
    nm, one, loc = qdb.CONCEPTS[c]
    rows += f'<tr><td>{circ(c)}</td><td><a href="#{anchor[c]}"><b>{nm}</b></a></td><td>{one}</td><td>{qdb.count(c)}</td><td>{qdb.recent(c)}</td><td class="stars">{qdb.star_str(qdb.stars(c))}</td><td>{loc}</td></tr>'
B.append('<h3>★ 족보 연계 핵심 개념 (강의자료만으로 풀 수 있는 족보 40문항 기준)</h3>'
         '<table><tr><th>#</th><th>개념</th><th>핵심 한 줄</th><th>출제</th><th>최근</th><th>중요도</th><th>강의 위치</th></tr>' + rows + '</table>')
B.append('<p class="note">별점 산정: 출제 횟수(1회→★★, 2회→★★★, 3회→★★★★, 4회 이상→★★★★★) + 2025 시험 출제 시 1단계 가산(2회 이상). 실제 출제 확률을 의미하지 않습니다. 출제 횟수는 “강의자료만으로 풀 수 있는 문항”만 집계했고, 21개 문항(Mohs 적응증·흑색종 위험인자 등)은 제외/판단 보류했습니다(→ 족보정리 §7).</p>')
B.append('<h3>반복 출제 핵심 (3회 이상)</h3><ul>'
         '<li>건선: 역학·악화요인 ①, 건선성 관절염 ②, 치료(NBUVB) ③ — <b>2021·2022·2023·2025 매년 출제</b></li>'
         '<li>UV: UVA/UVB 특성 ④, 급성·만성 반응 ⑤ — 매년 출제(선지 순서까지 동일한 경우 있음)</li>'
         '<li>암전구증 ⑥ (정답은 늘 IP), 진피 melanocytic lesion = Mongolian spot ⑦, 백반증 ⑧, SCC 고위험 ⑨, 편평태선 Wickham striae ⑩</li></ul>')
B.append('<h3>핵심 숫자 (공식 대신)</h3><table><tr><th>항목</th><th>값</th><th>출처</th></tr>'
         f'<tr><td>건선 유병률 / 가족력</td><td>{H("미국 2% · 한국 약 1%",1)} / {H("백인 1/3 · 한국 약 25%",1)}</td><td>강의③ p.6</td></tr>'
         f'<tr><td>건선 초발 연령</td><td>{H("20대 &gt; 10대 &gt; 30대",1)}</td><td>강의③ p.6</td></tr>'
         f'<tr><td>건선성 관절염</td><td>건선의 {H("6–42%",2)} · 일반인구 0.05–1% · {H("peak 35–40세",2)} · {H("성별차 없음",2)}</td><td>강의③ p.18</td></tr>'
         '<tr><td>건선 손발톱 pitting / 건선(Pso) 유병률</td><td>30–50% / 0.5–3%</td><td>강의③ p.19, p.18</td></tr>'
         '<tr><td>UVA / UVB / UVC</td><td>320–400 / 290–320 / 200–290 nm</td><td>강의② p.4, 5, 7</td></tr>'
         '<tr><td>MED (동양인)</td><td>UVA 50–70 J/cm² · UVB 50–70 mJ/cm² (UVB가 1/1000 양)</td><td>강의② p.6</td></tr>'
         f'<tr><td>SCC 고위험</td><td>{H("≥2cm · 침윤 ≥4mm",9)} · 전이: 일광손상 5% / 아랫입술 13% / 흉터 40%</td><td>강의① p.14–15</td></tr>'
         '<tr><td>BCC 전이율 / Bowen 악성화 / Queyrat 악성화</td><td>0.0028–0.55% / ≈5% (장기 42%에서 전암·암) / 10–33%</td><td>강의① p.13, p.6</td></tr>'
         '<tr><td>거대 선천성 색소성 모반</td><td>&gt;20cm · 흑색종 6–12% · 소아 흑색종의 ≈40%</td><td>강의① p.24</td></tr>'
         '<tr><td>백반증 유병률 / 일등친 가족력</td><td>0.1–2% / 약 20%</td><td>강의② p.22</td></tr>'
         '<tr><td>Kligman formula</td><td>hydroquinone 5% + tretinoin 0.1% + dexamethasone 0.1%</td><td>강의② p.34</td></tr>'
         '<tr><td>NBUVB / 엑시머</td><td>311 nm / 308 nm</td><td>강의② p.17</td></tr></table>')
B.append('<h3>핵심 비교 (→ §3 참조)</h3><p>BCC·SCC·Bowen · 유방 Paget vs 유방외 Paget · Epidermal vs Dermal melanocytic lesion · UVA vs UVB vs UVC · Segmental vs Non-segmental 백반증 · 건선/장미색잔비늘증/PRP/편평태선 · Small vs Large plaque parapsoriasis</p>')

# ---------------- 2. 상세 ----------------
B.append('<h2 id="s2">2. 강의별 상세 정리</h2>')
B.append('<h3 id="s2a">2-1. 강의① 표피 및 부속기의 모반과 종양</h3>')

B.append(card('c-class', '피부 종양의 분류 (기원별)', [], '피부 종양은 기원 세포에 따라 keratinocytic / melanocytic / adnexal / lympho-hematologic / neural·soft tissue / uncertain / inherited syndromes로 분류한다.',
 '<ul><li>Keratinocytic(non-melanoma): <b>BCC, SCC, Bowen병(SCC in situ), Merkel cell carcinoma</b></li><li>Melanocytic: 악성흑색종 · Adnexal: eccrine·apocrine·follicular·sebaceous 분화 종양</li><li>Lympho-hematologic: mycosis fungoides 등 · Inherited: Gorlin, Muir-Torre, XP에서의 피부암 등</li></ul>',
 f'{fig("tumor_classification","피부 종양 분류표",w=75)}', manual_stars=1, wide=True))

B.append(card('c-ak', '1. 광선각화증(AK)과 암전구증', [6],
 f'만성 일광노출 부위의 각화성 종양으로 편평세포암으로 이행할 수 있는 <b>암전구증</b>이며, 가장 흔한 암전구증이다.',
 '<ul><li><b>원인</b> 과다 일광노출 · 하얀 피부 → p53 유전자 돌연변이</li>'
 '<li><b>증상</b> 홍색~회색 1–10mm 각화성 구진, 표면에 단단히 부착된 인설 · <b>DDx</b> DLE, 지루각화증, Bowen병, 편평세포암</li>'
 '<li><b>치료</b> 전기소작, 냉동요법, 소파술, CO₂ 레이저, 5-fluorouracil 국소도포 · <b>예후</b> 다발성인 경우 약 10%가 10년 내 편평세포암으로 이행</li>'
 f'<li><b>전구암증(precancerous conditions)</b>: {H("광선각화증, 비소각화증, 백판증(leukoplakia), 피각, 선천성 거대 색소성모반, 만성방사선피부염, 색소성 건피증, Bowen병, Queyrat 홍색비후증",6)} <span class="mini">(강의① p.4)</span></li></ul>',
 f'{fig("ak_to_scc_uv","UV에 의한 subclinical AK → AK → SCC 진행")}{fig("ak_histology","광선각화증의 조직병리학 소견")}',
 kp=f'암전구증 목록을 외워 두면 “전구암증이 아닌 것”은 목록에 없는 질환(족보: 매년 IP)이다. <span class="mini">[IP는 강의자료에 없음 → 목록에 없다는 사실로 판단]</span>', long=True))

B.append(card('c-bowen', '2. Bowen병과 Queyrat 홍색비후증', [],
 '표피 내에 국한된 편평세포암(squamous cell carcinoma in situ)이다.',
 '<ul><li><b>원인</b> 노출부위=만성 일광노출 / 비노출부위=비소중독·방사선치료·바이러스(HPV16 33–64%)</li>'
 '<li><b>증상</b> 직경 수 mm~수 cm, 경계가 뚜렷한 홍반성 원형·부정형 판. 구진상·사마귀 모양, 인설·가피 동반</li>'
 '<li><b>DDx</b> Paget병, 악성흑색종, 기저세포암, 건선, 화폐상습진, 체부백선, 원판상 홍반성루푸스</li>'
 '<li><b>치료</b> 단순절제, 모즈미세도식수술, 전기소작, 냉동, CO₂ 레이저, 방사선, 광역동치료 · <b>예후</b> 약 5%가 편평세포암으로 이행, 장기적으로 약 42%에서 피부·점막의 전암 또는 암 발생</li>'
 '<li><b>Queyrat 홍색비후증</b>: 음경 귀두·포피에 발생한 Bowen병. 악성화 빈도 높고(10–33%) 더 침습적이며 전이가 잘 됨(점막하층 침범 시 약 20%에서 국소 림프절 전이)</li></ul>',
 '', manual_stars=2, no_exam='Bowen병·Queyrat는 암전구증 목록(§ AK)의 구성원으로만 출제됨(보기 선지)'))

B.append(card('c-paget', '3. Paget병 (유방 / 유방외)', [],
 '표피 내에 비정상 세포(Paget 세포)가 나타나는 병변으로, 유방에 생기면 유방 Paget병, 그 외 부위는 유방외 Paget병이다.',
 '<ul><li><b>유방 Paget</b>: 유두·유륜 주위 습진성 병변, <b>유방암 동반</b>. 유방 유선관 선암(adenocarcinoma)이 표피로 전이되어 발생. 편측 유두·유륜의 경계명확·진물 나는 인설성 홍반, 미란, 가피, 얕은 궤양. DDx 신경피부염·아토피피부염·화폐상습진·유두상선종·유두유륜각화증. 치료 유방절제술</li>'
 '<li><b>유방외 Paget(EMPD)</b>: 일차 = 아포크린샘으로 분화가 예정된 다기능 줄기세포의 악성화 / 이차 = 기저암(내부 장기암)에 의해 발생. <b>항문주위</b> 발생이 외음부 발생보다 내부 장기암 동반 확률이 높음. 호발: 항문·성기·서혜부·액와. 치료 외과적 절제(특히 모즈미세도식수술)</li></ul>',
 f'{fig("mammary_paget","유방 Paget병")}<div class="figrow">{fig("empd_vulva","외음부 유방외 Paget병(EMPD)")}{fig("empd_histology","EMPD 조직 소견")}</div>', manual_stars=1))

B.append(card('c-bcc', '4. 기저세포암 (Basal cell carcinoma)', [14],
 f'{H("인간에서 발생하는 가장 흔한 악성종양",14)}으로, 자외선에 오래 노출된 부위에 생기며 천천히 커지고 전이율이 극히 낮다.',
 '<ul><li><b>분류</b> '+H("Keratinocytic(epidermal) 종양에 속함",14)+' <span class="mini">(p.2 분류표)</span></li>'
 '<li><b>원인</b> 자외선(직업적 장기노출보다 간헐적으로 짧게 노출되는 것이 위험), 표피 DNA 손상, 외상·반흔, 방사선. 손바닥·발바닥·입술 홍순에는 발생 없음 → 털피지단위(모낭)에서 유래?'
 ' · '+H("PTCH 조절 유전자의 변이",14)+'</li>'
 '<li><b>DDx</b> 편평세포암, 각화극세포종, 광선각화증, 피지선 과형성</li>'
 '<li><b>치료</b> 외과적 절제 <b>특히 모즈미세도식수술</b>, 냉동치료, 방사선치료, CO₂ 레이저 · <b>예후</b> '+H("낮은 전이율(0.0028–0.55%)",14)+', 높은 완치율</li></ul>',
 '', kp='p53 돌연변이는 BCC가 아니라 광선각화증의 원인(강의① p.4)이고, BCC는 PTCH 변이.'))

B.append(card('c-scc', '5. 편평세포암 (Squamous cell carcinoma)', [9],
 '표피의 각질형성세포에서 유래하는 악성종양으로 주변 림프절 전이가 잘 된다.',
 '<ul><li><b>원인</b> 자외선B, 열상, 화학물질(그을음·광유·타르·비소 등), 방사선, HPV(5, 16), 면역억제, 유전 피부질환(눈피부백색증, 색소건피증)</li>'
 '<li><b>증상</b> 결절판상·우췌상·궤양 등 다양. 촉진 시 경결병소의 범위를 초과하여 암세포가 침범</li><li><b>DDx</b> 광선각화증, 각화극세포종, 가성암종성 과형성</li>'
 '<li><b>전이</b> 약 6–8%: 일광손상 피부 약 5% · 아랫입술 약 13% · 흉터 약 40% / 전이된 SCC의 5년 생존율 34.4%</li><li><b>치료</b> 외과적 절제(특히 모즈), 전기소작, 소파술, 방사선, 냉동</li>'
 f'<li><b>재발·전이 고위험 환자</b> ({"강의①"} p.15, 붉은 글씨): ① 부위 {H("입술, 귀",9)} ② 크기 {H("2cm 이상",9)} ③ 침윤 깊이 {H("4mm 이상",9)} / 뼈·근육·신경침범 ④ 조직 소견 {H("불완전 분화",9)}, 방추세포형 아형, 종양주위 림프구 소실 ⑤ 발생요인 흉터·만성궤양·만성골수염·자외선조사 ⑥ {H("재발 병변",9)} ⑦ 면역 억제된 환자</li></ul>', '',
 kp='고위험 수치는 “2cm 이상 / 4mm 이상 / 입술·귀 / 재발”. 다리·1cm·2mm·몸통·well-differentiated는 오답으로 반복 출제.'))

B.append(card('c-melanoma', '6. 악성흑색종 (Malignant melanoma)', [],
 '멜라닌세포에서 유래하는 악성종양으로, 강의에서는 WHO 아형 분류와 임상 사진을 제시한다.',
 '<ul><li><b>WHO 분류 major subtypes</b>: Superficial spreading melanoma · Nodular melanoma · Lentigo maligna melanoma · Acral lentiginous melanoma</li>'
 '<li><b>Other</b>: desmoplastic, blue nevus에서 발생, giant congenital nevus에서 발생, 소아 흑색종, naevoid, NOS</li><li>거대 선천성 색소성 모반에서 흑색종 발생(→ 모반 카드 참조)</li></ul>',
 f'{fig("melanoma_subtypes","SSM · Nodular · Acral lentiginous · Lentigo maligna melanoma",w=58)}{fig("melanoma_who_table","WHO 악성흑색종 아형 표",w=40)}', manual_stars=2, wide=True,
 no_exam='관련 족보 문항(위험인자: 백인·점 개수·BRAF 등)은 있으나 강의자료에 해당 내용이 없어 제외 → 족보정리 §7', long=True))

B.append(card('c-nevus', '7. 모반(Nevus)과 melanocytic lesion', [7],
 '모반은 melanocyte에서 유래한 모반세포(nevus cell)로 이루어진 종양이며 hamartoma로서 보통 출생 시 존재하고 성숙 또는 거의 성숙한 구조를 보인다.',
 '<ul><li><b>Epidermal melanocytic lesion</b>: '+H("Freckle, Lentigo, Nevus spilus, Becker’s nevus, Café-au-lait macule",7)+'</li>'
 '<li><b>Dermal melanocytic lesion</b>: '+H("Ota nevus, Mongolian spot, Ito nevus, 후천성 양측성 Ota-like macules, dermal melanocytic hamartoma",7)+'</li>'
 '<li><b>Halo nevus</b>: 탈색소 띠(depigmented zone)로 둘러싸인 색소모반</li>'
 '<li><b>선천성 모반</b> (1) Giant pigmented nevus: 털이 많은 큰 암색 반 + 작고 더 어두운 위성병변, 체간 dermatome 분포, 직경 &gt;20cm, 흑색종 발생 6–12%, 소아 흑색종의 약 40%, 치료 전절제 (2) Small(&lt;1.5cm)·Medium(1.5–20cm)</li></ul>',
 f'<div class="figrow">{fig("ectopic_mongolian_spot","이소성 몽고반(ectopic Mongolian spots)")}{fig("halo_nevus","Halo nevus")}</div>{fig("giant_congenital_nevus","거대 선천성 색소성 모반")}',
 kp='족보 단골: 진피형 = Mongolian spot (표기: “진피 악성 흑색종”, “epidermis 유래 아닌 것”, “악성 흑색종의 유래가 다른 것” 등으로 변형).', long=True))

B.append('<h3 id="s2b" class="pb">2-2. 강의② 색소 이상증 &amp; 피부노화</h3>')
B.append(card('c-uv', '1. 자외선·적외선과 피부 반응', [4, 5, 12],
 f'UV는 파장에 따라 UVA(320–400nm)·UVB(290–320nm)·UVC(200–290nm)로 나뉘며, 피부에 급성(홍반·tanning)·만성(비후·광노화·암) 반응과 유익/해로운 효과를 일으킨다.',
 '<table><tr><th></th><th>파장</th><th>특징 (강의② p.4–7)</th></tr>'
 f'<tr><td><b>UVA</b></td><td>320–400 nm (UVAII 320–340 / UVAI 340–400)</td><td>{H("Melanogenic action",4)} · 홍반 유발은 매우 약함(UVB의 1/1000) · {H("광노화(photoaging)에 더 큰 역할",4)} (지표 햇빛에 약 10배 많음, 연중·종일(흐린 날도), 진피 깊이 침투) · 독성은 {H("간접기전(ROS)",5)} — porphyrin·riboflavin·quinone 같은 내인성 광감작제</td></tr>'
 f'<tr><td><b>UVB</b></td><td>290–320 nm</td><td>{H("유리창에 차단됨",4)} · sunburn·suntanning·광발암의 주원인 · {H("직접 DNA 손상",4)}(CPD: C-C·T-C dimer, 가장 mutagenic / 6-4PP: CPD보다 복구 효율 좋음) · 염증·면역억제, PGE₂ 방출, polyamine 합성↑, 혈관신생</td></tr>'
 '<tr><td><b>UVC</b></td><td>200–290 nm</td><td>정상 피부에 홍반을 매우 효율적으로 유발, 살균(germicidal), 오존층에 막혀 지표면 도달 못함</td></tr>'
 '<tr><td><b>IR</b></td><td>760nm–1mm (IRA 760–1400 / IRB 1400–3000 / IRC 3000nm–1mm)</td><td>피부 온도 상승. 최근 IRA는 표피·진피·지방층까지 침투해 손상 가능, IRB·C는 불명</td></tr></table>'
 '<ul><li><b>MED</b>(Minimal Erythema Dose): 24시간 후 겨우 인지되는 홍반(sunburn)을 일으키는 최소량. '+H("UVB 광자가 UVA 광자보다 평균 약 1000배 더 energetic",4)+'. 동양인 MED: UVA 50–70 J/cm², UVB 50–70 mJ/cm²</li>'
 '<li><b>유익 효과</b>: 기분 상승 — 각질세포의 UV 노출 → POMC promoter 자극 → β-endorphin 분비 → 기분 개선·이완</li>'
 f'<li><b>해로운 효과</b>({"p.10"}): {H("UVB = 직접 DNA 손상, UVA = 발색단을 통한 간접 DNA 손상",5)} → melanoma, non-melanoma skin cancer, {H("immunosuppression",5)}, photoaging, burns, cataracts, ocular melanoma, {H("photodermatoses",12)}</li>'
 f'<li><b>피부 반응</b>(p.11): {H("급성 = Erythema(sunburn), Pigmentation(Tanning)",5)} / {H("만성 = Thickening, Photoaging, Mutation·skin cancer",5)} / Immune regulation</li></ul>',
 f'{fig("em_spectrum_table","전자기파 분류표",w=48)}{fig("uv_detrimental_effects","UV의 해로운 작용 도식 (UVB: 직접 DNA 손상 / UVA: 발색단 통한 간접 손상)",w=50)}{fig("infrared_spectrum","적외선(IRA·IRB·IRC) 파장",w=55)}',
 kp=f'혼동 주의 — “UVB는 유리창 통과 ✕(차단됨)”, “UVA가 UVB의 1/1000 ✕(UVB 필요량이 1/1000, 광자 에너지는 UVB가 1000배)”, “sunburn·두께 증가 = 만성 ✕/급성”.', long=True))

B.append(card('c-aging', '2. 피부노화 (Aging)', [5],
 '노화는 시간에 따른 내인성 노화와 UV·바람·열·흡연에 의한 외인성 노화로 나뉘며, 광노화는 외인성 노화에 속한다.',
 '<ul><li><b>Intrinsic aging(내인노화·climacteric)</b>: 시간 경과에 따른 불가피한 생리적 감퇴 — 건조(거칠음), 주름, 이완, 신생물, 탄력 소실, 상처 회복 지연</li>'
 f'<li><b>Extrinsic aging(외인노화)</b>: UV(가장 중요), 바람, 열, 흡연. {H("Photoaging = 만성 일광노출에 의한 변화가 내인성 노화에 중첩된 것",5)}</li>'
 '<li><b>광노화 기전</b>: UVR → 성장인자 수용체 군집화 + ROS 생성 → NF-κB↑, AP-1↑, TGF-β↓ → 염증성 cytokine↑·MMP↑·procollagen 합성↓·elastin 발현↑ → collagen 생성↓·분해↑, elastin 축적 → solar elastosis, 깊은 주름, 거친 결, 모세혈관확장, 색소침착</li>'
 '<li>활성산소(ROS)가 내인·외인 노화 모두에서 큰 역할 → <b>항산화물질</b> 사용이 노화 예방에 중요</li></ul>',
 f'{fig("wrinkle","주름(wrinkle)",w=36)}{fig("photoaging_mechanism","UVR에 의한 광노화 기전",w=62)}', wide=True))

B.append(card('c-photo', '3. 광치료 (Phototherapy)', [3],
 '질환 치료에 도움이 되는 파장의 자외선을 선택적으로 피부에 조사하는 치료이다.',
 '<ul><li><b>적응증</b>: 건선, 백반증, 아토피피부염, 피부 T세포 림프종(mycosis fungoides), 광과민성 피부염, 색소성 두드러기 등</li>'
 f'<li><b>종류</b>: 광대역 UVB(290–320nm) · PUVA(photochemotherapy) · {H("단일파장 UVB(311nm): Narrowband UVB",3)} · UVA1(고/중용량) · 엑시머 레이저(308nm; 표적 광치료)</li>'
 f'<li><b>NBUVB 장점 (vs PUVA)</b>: 호전이 빠름, 관해가 김, 과도한 홍반 적음, 저렴, 광감작제 불필요, 임신·소아에 사용, 치료 후 눈 보호 불필요, 발암성 낮음, 피부침윤 T세포 제거 효과는 비슷</li>'
 '<li><b>vs 광대역 UVB</b>: 피부 침투가 더 깊음, 진피 T세포 apoptosis 유도 효율↑, 과도한 홍반 적음</li></ul>',
 f'{fig("phototherapy_spectrum","UVB·UVA 파장과 광치료 스펙트럼 (Narrowband UVB 311nm)",w=62)}', wide=True,
 kp='족보에서는 건선 치료 문항의 정답 선지로 “광선치료는 주로 NBUVB”가 반복 출제([추론]으로 포함 — 족보정리 참조).'))

B.append(card('c-vitiligo', '4. 백반증 (Vitiligo)', [8],
 f'{H("표피 melanocyte의 소실",8)}이 병리학적 hallmark인 탈색소 질환이다.',
 '<ul><li><b>역학</b> 인구의 0.1–2%, 소아 또는 젊은 성인(주로 10–30세) · '+H("성별 차이 없음",8)+' · '+H("유전질환은 아니나 유전소인이 있음",8)+' (약 20%에서 일등친 백반증)</li>'
 f'<li><b>임상형</b> {H("Segmental · Non-segmental · Focal",8)}<br>· Segmental: 조기 발병(주로 소아), 빠른 진행 후 안정, dermatomal 분포, 모발 조기 침범(leukotrichia)<br>· Non-segmental: 평생 지속, 예측 불가한 확산, <b>Koebner phenomenon</b>, 모발은 후기 침범 (acrofacial 형 사진)</li>'
 f'<li><b>병인</b> 유전요인 + {H("oxidative stress",8)} → 자가면역. {H("세포성·체액성 자가면역(cellular and humoral)",8)}, 이웃 환경 변화(keratinocyte apoptosis↑), melanocytorrhagy, 산화스트레스(세포막 변화), autocytotoxicity</li>'
 '<li><b>동반 자가면역질환</b> 갑상선질환, DM, 부신기능부전, 경피증, SLE, 원형탈모, 중증근무력증, 악성빈혈 · 재색소 치료(스테로이드·calcineurin inhibitor·UV)의 면역억제 효과가 자가면역 가설을 간접 지지</li>'
 '<li><b>광치료 기전</b> 면역: photoimmunosuppression / 멜라닌세포: 모낭 outer root sheath의 비활성 melanocyte가 활성화·증식·이동, keratinocyte의 mitogen 방출 자극, 이동 증진</li></ul>',
 f'{fig("vitiligo_nonsegmental_acrofacial","Non-segmental (acrofacial) 백반증","2025 · 2022 · 2021 족보 사진")}<div class="figrow">{fig("vitiligo_segmental","Segmental type")}{fig("vitiligo_lesions","백반증 병변")}</div>{fig("vitiligo_repigmentation","광치료 시 모낭을 통한 재색소 도식")}',
 kp='“여자>남자 ✕ / 멘델 유전 ✕ / 자가면역 무관 ✕ / cellular만 ✕(둘 다) / oxidative stress 무관 ✕” 선지가 반복 출제.', long=True))

B.append(card('c-hyper', '5. 멜라닌세포·과다색소침착(기미)', [],
 '기미(melasma)는 햇빛 노출 부위에 생기는 불규칙한 연갈색~회갈색 반이다.',
 '<ul><li><b>Melanocyte</b> neural crest 기원, dendrite, 표피 기저층에 위치, MC : KC = 1 : 10, epidermal melanin unit</li>'
 '<li><b>과다색소침착 목록</b> Melasma(기미), Peutz-Jeghers syndrome, PUVA lentigines(흑색점), Riehl’s melanosis(흑색증), Dyschromatosis universalis hereditaria(유전전신색소이상증), Dohi acromelanosis(말단흑색증), Reticulate acropigmentation of Kitamura</li>'
 '<li><b>Melasma(Chloasma faciei)</b> 그리스어 khloasma = greenness. 깊이별 epidermal / dermal·mixed(melanophage 존재), 임상형 centrofacial · malar · mandibular</li>'
 '<li><b>치료</b> 국소 미백제 — <b>Kligman formula</b>(hydroquinone 5% + tretinoin 0.1% + dexamethasone 0.1%), kojic acid, glycolic acid, arbutin, α-bisabolol, tretinoin / 경구 tranexamic acid / chemical peel(TCA, glycolic acid, oxygen peel) / 광치료(low-fluence 1,064-nm QSNY laser, dye laser, 830·850nm LED, IPL)</li></ul>',
 f'{fig("melanocyte_structure","표피 기저층의 melanocyte와 epidermal melanin unit")}', manual_stars=1))

B.append('<h3 id="s2c">2-3. 강의③ 구진비늘(구진인설성) 질환</h3>')
B.append('<p class="note">강의 목록: 건선 · 장미색잔비늘증 · 모공성홍색잔비늘증 · 박탈피부염 · 유건선 · 흰색잔비늘증 · 편평태선 · 광택태선 · 선상태선 (제공된 슬라이드는 건선~편평태선, 박탈피부염·흰색잔비늘증·광택태선·선상태선 슬라이드 없음 → [자료 근거 없음])</p>')
B.append(card('c-psoriasis', '1. 건선 (Psoriasis)', [1, 2, 3, 11],
 '은백색의 인설을 동반한 구진과 판을 나타내는 흔한 만성·재발성 염증성 피부질환이다.',
 '<ul><li><b>정의</b> 둥글고 경계가 뚜렷한 홍반성 건조 판 + 회백~은백색의 겹겹이(imbricated, lamella) 인설. <b>호발</b> scalp, elbows, knees, 사지 신측, 천골부, 손발톱, 배꼽</li>'
 f'<li><b>역학</b> {H("미국 2% · 한국 약 1%",1)} / 초발 {H("20대, 10대, 30대",1)} (조기초발·만기초발 건선) / 가족력 {H("백인 1/3, 한국 약 25%",1)}</li>'
 f'<li><b>악화요인</b> {H("피부외상",1)}, 감염(β-streptococcal infection → 물방울양 건선), 기후(겨울에 악화·위도 높은 지역), 건조한 피부, {H("스트레스",1)}, 약물(lithium, β-blocker, chloroquine, NSAID[indomethacin 포함])</li>'
 '<li><b>병인</b> 유전요인 + 면역병인(initiation → amplification[급성] → maintenance[만성]); plasmacytoid DC·myeloid DC·T cell·keratinocyte·neutrophil, cytokine·chemokine</li>'
 '<li><b>임상형</b> Psoriasis vulgaris(=plaque) · Guttate(=eruptive) · Inverse(=flexural) · Pustular(generalized vs localized) · Psoriatic erythroderma</li>'
 f'<li><b>임상 특징</b> {H("Koebner’s phenomenon",11)} = isomorphic response, 사소한 외상 부위에도 전형적 병변 출현(편평태선·lichen nitidus·PRP에서도 관찰) / '
 'Auspitz sign: 인설을 강제로 제거할 때 점상출혈(진피유두 끝 위 표피가 얇아져서) / 지도설 / 손발톱 pitting(건선 환자의 30–50%)</li>'
 f'<li><b>건선성 관절염(PsA)</b> 건선(0.5–3%)의 {H("6–42%",2)}에서 발생, 일반인구 {H("0.05–1%",2)}(seropositive RA 수준) / {H("발병 peak 35–40세",2)} / {H("성별 차이 없음",2)}</li>'
 f'<li><b>치료</b> ① 외용: <b>1st line</b> {H("Emollients, Glucocorticoids, Vitamin D3 analogs",3)} / <b>2nd line</b> {H("Dithranol, Tazarotene, Tar",3)} ② 광치료·광화학요법: PUVA, {H("NBUVB",3)} (UVB: broadband vs narrowband) ③ 전신치료: {H("Methotrexate, Cyclosporine, Retinoids, Biologics",3)}</li></ul>',
 f'{fig("psoriasis_clinical","건선 임상 사진 (체간 판상 건선 / 유방하 건선)","2025 · 2023 · 2022 · 2021 족보 사진",w=64)}'
 f'{fig("psoriasis_types","건선 유형: plaque · guttate · pustular · inverse · erythrodermic",w=100)}'
 f'<div class="figrow">{fig("psoriasis_plaque_a","Plaque type")}{fig("psoriasis_plaque_b","Plaque type")}</div>'
 f'<div class="figrow">{fig("psoriasis_plaque_c","Plaque type")}{fig("psoriasis_koebner","Koebner 현상")}</div>'
 f'<div class="figrow">{fig("psoriasis_nail","손발톱 건선")}{fig("psoriasis_histology","건선의 조직병리학 소견")}</div>',
 kp='1차 외용제 = emollient·glucocorticoid·<b>vit D3 analog</b>(retinoid는 전신), 광치료는 <b>NBUVB</b>가 중심, “치료제는 모두 부작용이 적어 편하게 사용 ✕”.', long=True))

B.append(card('c-pr', '2. 장미색잔비늘증 (Pityriasis rosea)', [13],
 '원인 불명의 가벼운 염증성 발진(exanthem)으로 연어색 구진·반을 보인다.',
 '<ul><li>연어색(salmon-colored) 구진과 반, 병변 가장자리에 collarette 모양 인설(처음엔 분리되나 융합 가능)</li>'
 f'<li>대개 {H("단일 herald patch(mother patch)",13)}로 시작 → 1–2주 후 새 병변이 빠르게 퍼짐 → 3–8주에 자연 소실</li>'
 '<li>병변의 장축이 피부 할선(lines of cleavage)과 평행하게 배열</li></ul>',
 f'{fig("pityriasis_rosea","장미색잔비늘증","2019 족보 해설: 시험에 강의록과 동일한 사진")}', kp='진단에 유용한 sign = Herald patch (Koebner·Auspitz·Wickham·Pterygium은 오답 선지).'))

B.append(card('c-prp', '3. 모공성홍색잔비늘증 (Pityriasis rubra pilaris, PRP)', [],
 '작은 모공성 구진, 노르스름한 분홍색 인설반, 융합된 손발바닥 각화증을 특징으로 하는 만성 피부질환이다.',
 '<ul><li>모공성 구진: 뾰족한 갈색 핀머리 크기, 중심에 각질 마개(horny plug)</li><li>두피의 인설·홍반으로 시작 · 병변 내 <b>정상 피부 섬(small islands of normal skin)</b></li>'
 '<li>손발바닥 각화증 + 균열 경향, 발 측면까지 퍼져 “sandal” 모양 · 손발톱은 둔하고 거칠고 두꺼우며 부서지기 쉬움(pit 거의 없음)</li></ul>',
 f'<div class="figrow">{fig("prp_a","PRP")}{fig("prp_palmoplantar","손발바닥 각화증")}</div>{fig("prp_normal_islands","정상 피부 섬(islands of normal skin)")}', manual_stars=1, long=True))

B.append(card('c-para', '4. 유건선(Parapsoriasis)과 태선모양잔비늘증(Pityriasis lichenoides)', [],
 '유건선은 만성·치료저항성이며 자각증상이 없는 반구진 인설성 발진군이다.',
 '<ul><li><b>Small plaque</b>(소판상, 1–5cm): 림프종으로 진행하지 않음 · <b>Large plaque</b>(대판상, 5–15cm): 10–30%에서 T-cell lymphoma로 진행(특히 심한 소양증 동반)</li>'
 '<li><b>Pityriasis lichenoides</b>: PLEVA(=Mucha-Haberman병; self-limiting, 반·구진·수포의 다형성 발진) / PLC(chronica; 홍반·황색 인설성 반과 태선양 구진이 서서히 발생, 수개월~수년 후 자연 소실)</li></ul>',
 f'<div class="figrow">{fig("parapsoriasis_small_plaque","Small plaque parapsoriasis")}{fig("parapsoriasis_large_plaque","Large plaque parapsoriasis")}</div>{fig("pityriasis_lichenoides_chronica","Pityriasis lichenoides chronica")}', manual_stars=1))

B.append(card('c-lp', '5. 편평태선 (Lichen planus)', [10],
 '피부·모낭·점막을 침범하는 흔한 소양성 염증성 질환으로 작고 보랏빛의 편평한 다각형 구진이 특징이다.',
 '<ul><li><b>Pathognomonic</b> 작고 violaceous한 편평 다각형 구진(원발진) · '+H("Wickham’s striae: 병변을 가로지르는 회백색 점(puncta) 또는 줄(streaks)",10)+'</li>'
 '<li><b>호발</b> 굴측 손목, 체간, 내측 대퇴, 정강이, 손등, 귀두 · Koebner phenomenon(+)</li>'
 '<li><b>손발톱</b> pterygium formation이 특징적, 종주 홈(longitudinal grooving), 근위·원위 조갑박리, ridging, splitting, midline fissure</li>'
 f'<li><b>구강</b> Reticular(볼 안쪽) · Atrophic · {H("Ulcerative(erosive): premalignant condition(전암 상태)",10)}</li>'
 '<li><b>생식기</b> 귀두: 편평 다각형 구진 또는 고리 모양 배열 / 음순·항문: 침연(maceration)으로 희게 보임</li></ul>',
 f'<div class="figrow">{fig("lichen_planus_skin","피부 병변(발목·손등)")}{fig("lichen_planus_oral","구강 편평태선")}</div>{fig("lichen_planus_nail","손톱 편평태선(pterygium)")}',
 kp='회백색 띠 = Wickham’s striae. Auspitz sign(건선), Herald patch(장미색잔비늘증), Pterygium(LP 손톱)과 구분.', long=True))

# ---------------- 3. 비교 ----------------
B.append('<h2 id="s3">3. 개념 비교</h2>')
B.append('<h3>피부암·상피내암 비교</h3><table><tr><th>구분</th><th>BCC</th><th>SCC</th><th>Bowen병</th></tr>'
 f'<tr><td>정의</td><td>{H("인간에서 가장 흔한 악성종양",14)}</td><td>표피 각질형성세포 유래 악성종양</td><td>표피내 국한된 SCC (in situ)</td></tr>'
 '<tr><td>전이</td><td>극히 낮음(0.0028–0.55%)</td><td>림프절 전이 잘 됨(6–8%)</td><td>약 5%가 SCC로 이행</td></tr>'
 '<tr><td>원인</td><td>UV(간헐적 노출), PTCH 변이</td><td>UVB, 화학물질, 방사선, HPV 5·16, 면역억제</td><td>일광(노출부), 비소·방사선·HPV16(비노출부)</td></tr>'
 '<tr><td>치료</td><td colspan="3">외과적 절제(특히 모즈), 냉동, 방사선, CO₂ 레이저(Bowen은 전기소작·광역동도)</td></tr></table>')
B.append('<h3>Paget병 비교</h3><table><tr><th></th><th>유방 Paget</th><th>유방외 Paget</th></tr><tr><td>부위</td><td>유두·유륜</td><td>항문·성기·서혜부·액와</td></tr><tr><td>기전</td><td>유방 유선관 선암이 표피로 전이</td><td>일차: 아포크린샘 분화 예정 줄기세포 악성화 / 이차: 기저 내부 장기암</td></tr><tr><td>치료</td><td>유방절제술</td><td>외과적 절제(특히 Mohs)</td></tr></table>')
B.append('<h3>Epidermal vs Dermal melanocytic lesion</h3><table><tr><th>Epidermal</th><th>Dermal</th></tr><tr><td>'+H("Freckle, Lentigo, Nevus spilus, Becker’s nevus, Café-au-lait macule",7)+'</td><td>'+H("Ota nevus, <b>Mongolian spot</b>, Ito nevus, 후천성 양측성 Ota-like macules, dermal melanocytic hamartoma",7)+'</td></tr></table>')
B.append('<h3>UVA · UVB · UVC</h3><table><tr><th>구분</th><th>UVA</th><th>UVB</th><th>UVC</th></tr>'
 f'<tr><td>파장</td><td>320–400nm</td><td>290–320nm</td><td>200–290nm</td></tr>'
 f'<tr><td>유리창</td><td>(강의록 언급 없음)</td><td>{H("차단",4)}</td><td>지표 도달 X(오존층)</td></tr>'
 f'<tr><td>주요 작용</td><td>{H("melanogenic, 광노화",4)}, 진피 침투</td><td>sunburn·tanning·광발암, {H("직접 DNA 손상",4)}</td><td>살균, 홍반 매우 효율적</td></tr>'
 '<tr><td>홍반 필요량(MED)</td><td>50–70 J/cm²</td><td>50–70 mJ/cm² (1/1000)</td><td>—</td></tr>'
 '<tr><td>광자 에너지</td><td>낮음</td><td>UVA의 약 1000배</td><td>—</td></tr></table>')
B.append('<h3>Segmental vs Non-segmental 백반증</h3><table><tr><th></th><th>Segmental</th><th>Non-segmental</th></tr>'
 '<tr><td>발병</td><td>조기(주로 소아)</td><td>평생 지속</td></tr><tr><td>경과</td><td>빠른 진행 후 안정</td><td>예측 불가한 확산</td></tr>'
 '<tr><td>분포</td><td>Dermatomal</td><td>(acrofacial 등) · Koebner phenomenon</td></tr><tr><td>모발</td><td>조기 침범(leukotrichia)</td><td>후기 침범</td></tr></table>')
B.append('<h3>구진비늘질환 구분</h3><table><tr><th>질환</th><th>핵심 단서</th></tr>'
 f'<tr><td>건선</td><td>은백색 층상 인설, {H("Koebner",11)}, Auspitz sign, 손발톱 pitting, 관절염</td></tr>'
 f'<tr><td>장미색잔비늘증</td><td>{H("Herald patch",13)}, collarette 인설, 할선과 평행, 3–8주 자연 소실</td></tr>'
 '<tr><td>모공성홍색잔비늘증</td><td>모공성 구진+horny plug, 정상 피부 섬, 손발바닥 각화증(sandal)</td></tr>'
 f'<tr><td>편평태선</td><td>violaceous 편평 다각형 구진, {H("Wickham’s striae",10)}, pterygium, 구강 erosive형 전암</td></tr>'
 '<tr><td>유건선</td><td>small(1–5cm, 림프종 X) vs large(5–15cm, T-cell lymphoma 10–30%)</td></tr>'
 '<tr><td>태선모양잔비늘증</td><td>PLEVA(급성·다형성 발진) vs PLC(만성·태선양 구진)</td></tr></table>')

# ---------------- 4. 관계 ----------------
B.append('<h2 id="s4">4. 개념 간 관계</h2>')
B.append('<div class="flow"><span>과다 일광노출 + 하얀 피부</span><i>→</i><span>p53 변이</span><i>→</i><span>subclinical AK</span><i>→</i><span>광선각화증</span><i>→</i><span>편평세포암</span><i>→</i><span>림프절 전이</span></div>')
B.append('<div class="flow"><span>UVR</span><i>→</i><span>ROS·성장인자 수용체 군집화</span><i>→</i><span>NF-κB↑ AP-1↑ TGF-β↓</span><i>→</i><span>MMP↑ procollagen↓ elastin↑</span><i>→</i><span>solar elastosis·주름 (광노화)</span></div>')
B.append('<div class="flow"><span>유전요인 + oxidative stress</span><i>→</i><span>세포성·체액성 자가면역</span><i>→</i><span>melanocyte 소실</span><i>→</i><span>백반증(Segmental / Non-segmental / Focal)</span></div>')
B.append('<div class="flow"><span>피부외상·감염·약물·스트레스</span><i>→</i><span>건선 악화 / Koebner 현상</span><i>→</i><span>plaque·guttate·pustular·inverse·erythroderma</span><i>→</i><span>PsA(6–42%)</span></div>')
B.append('<div class="flow"><span>건선 치료</span><i>→</i><span>1차 외용(emollient·steroid·vit D3)</span><i>→</i><span>2차 외용(dithranol·tazarotene·tar)</span><i>→</i><span>광치료(NBUVB·PUVA)</span><i>→</i><span>전신(MTX·cyclosporine·retinoid·biologics)</span></div>')

# ---------------- 5. 족보 연결 ----------------
B.append('<h2 id="s5">5. 족보와 연결된 핵심 개념 (출제 빈도 순)</h2>')
for c in sorted(qdb.CONCEPTS, key=lambda c: (-qdb.count(c), -qdb.stars(c), c)):
    qs = [q for q in qdb.INC if q['c'] == c]
    B.append(f'<div class="exam-line"><b>{circ(c)} {qdb.CONCEPTS[c][0]}</b> — 출제 {len(qs)}회 · 최근 {qdb.recent(c)} · <span class="stars">{qdb.star_str(qdb.stars(c))}</span> · 강의 위치 {qdb.CONCEPTS[c][2]}<br>'
             f'<span class="mini">[족보: {" · ".join(qdb.qlabel(q["id"]) for q in qs)}] → 정답: {" / ".join(q["ans"] for q in qs)}</span></div>')

# ---------------- 6. 직전 정리 ----------------
B.append('<h2 id="s6">6. 시험 직전 핵심 정리</h2><ul>'
 f'<li><b>정의</b> 광선각화증 = 편평세포암으로 이행 가능한 암전구증 / Bowen = SCC in situ / BCC = {H("인간에서 가장 흔한 악성종양",14)}, {H("PTCH 변이",14)} / 백반증 = {H("표피 melanocyte 소실",8)}</li>'
 f'<li><b>숫자</b> 건선 {H("미국 2%·한국 1%, 가족력 한국 25%, 초발 10~30대",1)} / PsA {H("6–42%, peak 35–40세, 성별차 없음",2)} / SCC 고위험 {H("2cm·4mm",9)} / UVA 320–400, UVB 290–320, UVC 200–290</li>'
 f'<li><b>순서·분류</b> 암전구증 목록 {H("AK·비소각화증·백판증·피각·거대모반·만성방사선피부염·XP·Bowen·Queyrat",6)} (IP ✕) / 진피형 {H("Ota·Mongolian·Ito",7)} / 백반증 임상형 {H("Segmental·Non-segmental·Focal",8)}</li>'
 f'<li><b>비교·함정</b> UVA = {H("melanogenic·광노화",4)}, UVB = {H("유리창 차단·직접 DNA 손상",4)} / UV 급성 = {H("홍반·tanning",5)}, 만성 = 비후·광노화·암 / 광노화 = 외인성</li>'
 f'<li><b>치료</b> 건선 {H("1차 외용 = emollient·steroid·vit D3 analog",3)}, {H("광치료는 NBUVB",3)}, retinoid·MTX·cyclosporine = 전신</li>'
 f'<li><b>예외·단서</b> {H("Wickham’s striae",10)}(편평태선) · {H("Herald patch",13)}(장미색잔비늘증) · {H("Koebner",11)}(건선·LP·백반증 non-segmental) · UV 해로운 영향 {H("photodermatoses",12)}</li>'
 '<li><b>실제 족보 출제 사진</b> 📌 건선 임상 사진(강의③ p.11), 📌 non-segmental 백반증 사진(강의② p.24), 장미색잔비늘증 사진(강의③ p.25)</li></ul>')
B.append('<footer class="page-note">근거 표기: [추론] = 강의자료 근거로 소거·추론한 판단 / [확인 필요] = 자료 불충분 / [판독 불가] = 원문 소실 / [자료 근거 없음] = 강의자료에 없음. 이미지는 제공된 강의 PDF의 원본 이미지 객체에서 필요한 영역만 무손실로 추출했으며 원본 해상도를 유지했습니다(강의 PDF 자체가 저해상도 슬라이드 이미지 — 업스케일하지 않음). 이 문서에는 외부 자료를 사용하지 않았습니다.</footer>')

open(OUT + '강의록.html', 'w', encoding='utf8').write(page('강의록 — 두경부 및 피부(피부과)', '\n'.join(B)))
print('ok', len('\n'.join(B)))
