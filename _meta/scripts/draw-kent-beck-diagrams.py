"""Rebuild the article's editable SVG diagrams (Python standard library only)."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/assets/images/standalone/2026-10-08-kent-beck-features-futures'
OUT.mkdir(parents=True, exist_ok=True)
INK, MUTED, BLUE, GREEN, RED = '#1f2937', '#576574', '#2563a6', '#18785d', '#c84b4b'


def text(x, y, s, size=22, color=INK, anchor='start', weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{escape(s)}</text>'


def line(x1, y1, x2, y2, color=MUTED, arrow=False, dash=False):
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="2.5"' + (' marker-end="url(#arrow)"' if arrow else '') + (' stroke-dasharray="6 5"' if dash else '') + '/>'


def rect(x, y, w, h, fill='#f6f8fa', stroke='#d7dfe5'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}"/>'


def dot(x, y, color, r=6):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'


def save(name, title, desc, body, height, width=640):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L8,4 L0,8" fill="none" stroke="{MUTED}" stroke-width="2"/></marker></defs>
<rect width="{width}" height="{height}" rx="16" fill="#fff"/>
<g font-family="Malgun Gothic, Apple SD Gothic Neo, Noto Sans KR, sans-serif">{body}</g></svg>'''
    (OUT / name).write_text(svg + '\n', encoding='utf-8')


b = text(28, 40, '완료를 확인하는 세 가지 질문', 25, weight=700)
for y, n, title, sub, color, fill in [
    (65, '01', '코드가 만들어졌나?', '함수와 파일이 생겼다', BLUE, '#eef6ff'),
    (181, '02', '요구한 대로 동작하나?', '실패·중복 요청도 실제로 확인한다', GREEN, '#edf8f2'),
    (297, '03', '다음에도 바꿀 수 있나?', '변경 범위와 얽힌 의존성을 살펴본다', '#8b5b24', '#fff8ed'),
]:
    b += rect(28, y, 584, 96, fill) + text(48, y+38, n, 24, color, weight=700)
    b += text(104, y+36, title, 24, weight=700) + text(104, y+70, sub, 21, MUTED)
save('three-questions.svg', '코드 생성과 완료 사이의 세 질문', '코드 생성, 현재 동작 검증, 미래 변경 검토는 서로 다른 확인이다.', b, 415)


def axes():
    return (text(28, 39, 'Futures · 변경할 수 있는 선택지', 23, weight=700)
            + line(90, 350, 90, 68, arrow=True) + line(90, 350, 588, 350, arrow=True)
            + text(586, 388, 'Features · 현재 기능', 22, anchor='end', weight=700)
            + text(45, 91, '많음', 18, MUTED) + text(45, 348, '적음', 18, MUTED)
            + text(90, 383, '적음', 18, MUTED) + text(583, 336, '많음', 18, MUTED))


b = axes()
b += '<path d="M90,115 C145,115 191,120 244,136 S332,166 366,194 S416,245 431,265 S476,318 490,346" fill="none" stroke="#c84b4b" stroke-width="5"/>'
for x, y in [(90,115), (244,136), (366,194), (431,265), (490,346)]:
    b += dot(x,y,RED)
b += text(112, 93, '시작', 20, MUTED)
b += rect(282, 70, 308, 68, '#fff0ee', '#edc4bf') + text(436, 98, '기능을 계속 추가한다', 24, RED, 'middle', 700) + text(436, 125, '유지해야 할 제약도 쌓인다', 18, RED, 'middle')
b += text(122, 280, '기능은 있지만', 22, RED) + text(122, 310, '바꾸기 어려운 상태', 22, RED)
b += text(28, 430, '개념도 · 시간축과 실측 수치가 없는 그림', 18, MUTED)
save('features-drain.svg', '기능만 추가하는 빨간 궤적', '가로축 Features, 세로축 Futures. 기능을 추가하며 선택지를 소진하는 개념도이며 실측 곡선이 아니다.', b, 455)

b = axes()
b += '<path d="M90,225 C260,226 414,260 490,346" fill="none" stroke="#c84b4b" stroke-width="3" stroke-dasharray="7 6" opacity=".6"/>'
b += '<path d="M90,218 L188,244 L188,183 L286,209 L286,147 L384,173 L384,110 L482,136 L482,76 L552,98" fill="none" stroke="#18785d" stroke-width="5" stroke-linejoin="round"/>'
for x,y in [(90,218),(188,244),(188,183),(286,209),(286,147),(384,173),(384,110),(482,136),(482,76),(552,98)]:
    b += dot(x,y,GREEN,4.5)
b += text(103, 277, '① 기능 추가 ↘', 20, BLUE, weight=700)
b += text(307, 92, '② 구조 정리 ↑', 20, GREEN, weight=700)
b += text(267, 320, '정리 없이 기능만 추가하면', 18, RED)
b += text(28, 430, '두 활동을 번갈아 한다 · 회복의 크기는 예시', 18, MUTED)
save('features-recovery.svg', '기능과 변경 가능성을 번갈아 늘리는 초록 궤적', '기능 추가는 오른쪽 아래로, 현재 동작을 유지하는 구조 정리는 위로 이동한다. 회복량을 보장하는 정량 모델이 아니다.', b, 455)

b = text(28, 40, '예시 · 문자 업체를 바꿔야 한다면', 25, weight=700)
b += rect(20, 62, 600, 169, '#fff4f2') + text(38, 95, '정리 전: 업무 코드마다 업체를 직접 호출', 21, RED, weight=700)
for y, label in [(116, '주문'),(153,'배송'),(190,'취소')]:
    b += rect(43,y,115,31,'#fff') + text(100,y+23,label,20,anchor='middle')
    b += line(166,y+16,391,y+16,arrow=True) + text(490,y+23,'문자 업체 API',20,anchor='middle')
b += text(320, 270, '동작은 유지하고, 업체 의존성을 모은다', 21, MUTED, 'middle')
b += rect(20, 292, 600, 207, '#eff8f2') + text(38, 326, '정리 후: 공통 경로 뒤에서 업체를 연결', 21, GREEN, weight=700)
for y,label in [(349,'주문'),(390,'배송'),(431,'취소')]:
    b += rect(43,y,101,33,'#fff') + text(93,y+24,label,20,anchor='middle')
    b += line(150,y+16,208,407,arrow=True)
b += rect(218,373,177,67,'#fff','#86bca3') + text(306,415,'알림 경로',23,GREEN,'middle',700)
b += line(401,407,442,407,arrow=True) + rect(451,373,150,67,'#fff') + text(526,402,'문자 업체',21,anchor='middle') + text(526,427,'API',20,MUTED,'middle')
b += text(28,535,'중복 발송·재시도 규칙은 별도 검증이 필요하다',20,MUTED)
save('notification-boundary.svg', '알림 업체 의존성을 모으는 가상 사례', '정리 전에는 주문 배송 취소가 각각 업체를 호출한다. 정리 후에는 공통 알림 경로가 업체를 연결한다. 중복과 재시도의 정확성은 별도 검증한다.', b, 560)

b = text(28,40,'명세로 돌아오는 길이 있는가',25,weight=700)
b += rect(20,65,600,138,'#fff4f2') + text(40,99,'처음 쓴 명세로 끝내려는 흐름',22,RED,weight=700)
for x,label in [(43,'명세'),(242,'구현'),(441,'완성 기대')]:
    b += rect(x,122,156,53,'#fff') + text(x+78,155,label,22,anchor='middle')
for x in (204,403): b+=line(x,149,x+31,149,arrow=True)
b += rect(20,227,600,243,'#eff8f2') + text(40,264,'발견에 맞춰 다시 결정하는 흐름',22,GREEN,weight=700)
for x,label in [(43,'작은 명세'),(242,'구현'),(441,'검증·사용')]:
    b+=rect(x,295,156,57,'#fff')+text(x+78,331,label,22,anchor='middle')
for x in (204,403): b+=line(x,324,x+31,324,arrow=True)
b+='<path d="M519,357 V406 H121 V357" fill="none" stroke="#18785d" stroke-width="3" marker-end="url(#arrow)"/>'
b+=text(320,443,'새 사실 → 기대 동작·계획·검증 기준 수정',20,GREEN,'middle')
save('spec-feedback.svg','명세와 반복 개발','명세 구현 완성의 일방향 흐름과, 검증 및 사용자 발견이 다시 명세로 돌아오는 반복 흐름의 비교.',b,493)

b=text(28,40,'만든 것과 달라진 것을 구분한다',25,weight=700)
items=[('Effort · 투입','개발 시간과 모델 호출 비용',BLUE,'#edf5ff'),('Output · 산출물','주문 상태 알림을 만들었다',BLUE,'#edf5ff'),('Outcome · 사용자 변화','상태를 묻는 전화가 줄었다',GREEN,'#eff8f2'),('Mission · 함께 추구할 목적','고객이 안심하고 주문을 맡긴다','#7653a4','#f5f0fc')]
for i,(title,sub,color,fill) in enumerate(items):
    y=66+i*117
    b+=rect(70,y,500,91,fill)+text(95,y+35,title,24,color,weight=700)+text(95,y+68,sub,22)
    if i<3:b+=line(320,y+96,320,y+112,arrow=True)
b+=text(28,554,'화살표마다 확인이 필요하다 · 알림 사례는 가상',20,MUTED)
save('effort-to-mission.svg','노력에서 공동의 목적으로','개발 시간과 비용, 알림 기능, 고객 행동 변화, 안심하고 주문한다는 목적의 흐름. 앞 단계를 달성해도 다음 단계는 자동으로 달성되지 않는다.',b,580)

b=text(28,40,'정리를 실행하는 절차와 선택하는 판단',25,weight=700)
b+=text(28,73,'정리의 필요를 발견한 뒤, 할 일로 선택하는 과정',20,MUTED)
b+=rect(28,102,278,150,'#edf5ff')+text(48,137,'새 기능 요청',22,BLUE,weight=700)
b+=text(48,183,'기존 코드 분석',21)+text(48,218,'필요한 정리 발견',21)
b+=rect(334,102,278,150,'#fff8ed')+text(354,137,'기능 요청이 없는 영역',22,'#8b5b24',weight=700)
b+=text(354,183,'반복 수정·검증 부담',21)+text(354,218,'정리할 근거가 있는가',21)
b+=line(167,257,167,288,arrow=True)
b+=line(473,257,473,288,arrow=True,dash=True)
b+=rect(28,296,278,68,'#edf5ff')+text(167,337,'선행 정리 작업으로 분리',21,BLUE,'middle',700)
b+='<rect x="334" y="296" width="278" height="68" rx="12" fill="#fff8ed" stroke="#8b5b24" stroke-width="2" stroke-dasharray="6 5"/>'
b+=text(473,337,'누가, 언제 선택할까?',21,'#8b5b24','middle',700)
b+='<path d="M167,369 V394 H305 V417" fill="none" stroke="#576574" stroke-width="2.5" marker-end="url(#arrow)"/>'
b+='<path d="M473,369 V394 H335 V417" fill="none" stroke="#576574" stroke-width="2.5" stroke-dasharray="6 5" marker-end="url(#arrow)"/>'
b+=rect(60,425,520,92,'#eff8f2')+text(320,461,'선택된 구조 정리 작업',23,GREEN,'middle',700)
b+=text(320,494,'목표·범위·유지할 동작·검증 조건',21,anchor='middle')
b+=line(320,522,320,549,arrow=True)
b+=rect(60,557,520,92,'#eff8f2')+text(320,593,'기존 SDD 절차로 수행',23,GREEN,'middle',700)
b+=text(320,626,'분석 → 검토 → 구현 → 검증',21,anchor='middle')
b+=text(28,688,'실선: PR #54의 흐름  ·  점선: 더 살펴볼 작업 선택',20,MUTED)
save('adaptive-loop.svg','구조 정리 작업의 선택과 실행','왼쪽 실선은 새 기능을 위한 기존 코드 분석에서 정리를 발견하고 선행 작업으로 분리한 PR 54의 흐름이다. 오른쪽 점선은 기능 요청이 없어도 반복 수정과 검증 부담을 근거로 정리를 선택하는 경로이며, 누가 언제 우선할지 판단이 필요하다. 선택된 정리 작업은 목표와 범위, 유지할 동작과 검증 조건을 정해 기존 SDD 절차로 수행할 수 있다.',b,715)

b=rect(0,0,1200,630,'#eef3ec','#eef3ec')
b+=text(72,82,'AI AGENT DIARY  /  STANDALONE',22,GREEN,weight=700)
b+=text(72,177,'기능은 늘었는데,',54,weight=700)+text(72,250,'왜 고치기는 어려워졌을까',54,weight=700)
b+=text(75,310,'켄트 백의 Features와 Futures',28,MUTED)
b+=line(80,555,80,376)+line(80,555,1119,555)
b+='<path d="M81,416 C452,418 606,458 736,550" stroke="#c84b4b" fill="none" stroke-width="6" stroke-dasharray="12 10"/>'
b+='<path d="M81,418 L270,447 L270,397 L472,427 L472,374 L675,404 L675,351 L877,381 L877,327 L1088,357" fill="none" stroke="#18785d" stroke-width="7" stroke-linejoin="round"/>'
b+=text(920,485,'기능만 계속 추가',26,RED)+text(880,280,'다음 변경의 여지',26,GREEN)
b+=text(80,602,'그래프로 풀어 읽고, Adaptive Agentic SDD와 비교하다',25,MUTED)
save('thumbnail.svg','기능은 늘었는데 왜 고치기는 어려워졌을까','기능만 늘리는 빨간 궤적과 변경 여지를 회복하는 초록 궤적을 대비한 글 표지.',b,630,1200)

print(f'Wrote 8 SVGs to {OUT}')
