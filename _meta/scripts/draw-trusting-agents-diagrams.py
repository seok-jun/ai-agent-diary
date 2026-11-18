"""Rebuild the SVG diagrams for the 2026-11-18 standalone post (standard library only).

Usage: python draw-trusting-agents-diagrams.py
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/assets/images/standalone/2026-11-18-trusting-ai-coding-agents'
OUT.mkdir(parents=True, exist_ok=True)

INK, MUTED, LINE = '#182D3C', '#657681', '#D5DFE4'
TEAL, TEAL_BG = '#328399', '#E7F3F7'
AMBER, AMBER_BG = '#BC8936', '#FBE8BE'
PURPLE, PURPLE_BG = '#9B83BA', '#F0EBF8'
RED, RED_BG = '#C2554D', '#FBE9E7'
FONT = 'Malgun Gothic, Apple SD Gothic Neo, Noto Sans KR, sans-serif'


def text(x, y, s, size=22, color=INK, anchor='middle', weight=400):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}">{escape(s)}</text>')


def box(x, y, w, h, fill, stroke, lines, size=22):
    """Rounded box with centred lines. Each line is (text, weight)."""
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    gap = size + 10
    top = y + h / 2 - gap * (len(lines) - 1) / 2 + size * 0.36
    for i, (s, weight) in enumerate(lines):
        out += text(x + w / 2, round(top + i * gap, 1), s, size, INK, 'middle', weight)
    return out


def arrow(points, color=MUTED, dash=False):
    """Polyline with an arrow head on the last segment."""
    (x1, y1), (x2, y2) = points[-2], points[-1]
    dx, dy = x2 - x1, y2 - y1
    n = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / n, dy / n
    bx, by = x2 - ux * 10, y2 - uy * 10
    head = f'{x2},{y2} {bx - uy * 5:.1f},{by + ux * 5:.1f} {bx + uy * 5:.1f},{by - ux * 5:.1f}'
    pts = ' '.join(f'{x},{y}' for x, y in points)
    return (f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round"'
            + (' stroke-dasharray="7 6"' if dash else '') + f'/><polygon points="{head}" fill="{color}"/>')


def save(name, title, desc, heading, sub, body, height, width=960):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
           f'role="img" aria-labelledby="title desc">\n<title id="title">{escape(title)}</title>'
           f'<desc id="desc">{escape(desc)}</desc>\n<rect width="{width}" height="{height}" fill="#FFFFFF"/>\n'
           f'<g font-family="{FONT}">\n'
           + text(40, 56, heading, 30, INK, 'start', 700) + '\n'
           + text(40, 95, sub, 20, MUTED, 'start') + '\n'
           + body + '\n</g>\n</svg>\n')
    (OUT / name).write_text(svg, encoding='utf-8', newline='\n')


# 1. how a justified workaround spreads
b = box(40, 140, 250, 100, PURPLE_BG, PURPLE, [('아키텍처 충돌', 700), ('근본 원인은 그대로', 400)])
b += arrow([(290, 190), (353, 190)])
b += box(355, 140, 250, 100, RED_BG, RED, [('타이머로 임시 우회', 700), ('+ 정당화하는 주석', 400)])
b += arrow([(605, 190), (668, 190)])
b += box(670, 140, 250, 100, AMBER_BG, AMBER, [('코드베이스에 남는다', 700), ('다음 작업의 입력', 400)])
b += arrow([(795, 240), (795, 300), (480, 300), (480, 243)], RED)
b += text(637, 334, '다음 에이전트가 같은 방식을 따라 쓴다', 20, RED)
b += box(40, 390, 880, 110, TEAL_BG, TEAL, [
    ('순환을 끊으려면', 700),
    ('주석 대신 린트 규칙으로 막고, 오류 메시지로 근본 원인을 고치게 안내한다', 400)])
save('workaround-spread.svg', '우회 코드가 퍼지는 순환',
     '아키텍처 충돌을 타이머로 우회하고 주석으로 정당화하면, 그 코드가 다음 작업의 입력이 되어 같은 우회가 반복된다.',
     '우회 코드가 퍼지는 순환', '주석이 임시 우회를 설계 근거처럼 보이게 만든다', b, 540)


# 2. cost of one verified task (conceptual, no measured values)
def bar(y, label, parts):
    out = text(40, y - 14, label, 22, INK, 'start', 700)
    x = 40
    for w, fill, stroke, s in parts:
        out += f'<rect x="{x}" y="{y}" width="{w}" height="64" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        if s:
            out += text(x + w / 2, y + 40, s, 20, INK, 'middle', 700)
        x += w + 6
    return out


b = bar(170, '검증을 아낀 경우', [
    (190, TEAL_BG, TEAL, '구현'), (70, AMBER_BG, AMBER, '검증'), (430, RED_BG, RED, '재작업 · 뒤늦은 결함 수정')])
b += bar(310, '위험도에 맞춰 검증한 경우', [
    (190, TEAL_BG, TEAL, '구현'), (230, AMBER_BG, AMBER, '검증'), (110, RED_BG, RED, '재작업')])
b += bar(450, '검증을 무조건 늘린 경우', [
    (190, TEAL_BG, TEAL, '구현'), (420, AMBER_BG, AMBER, '검증 · 실행 시간 · 오탐 대응'), (110, RED_BG, RED, '재작업')])
b += f'<line x1="40" y1="552" x2="920" y2="552" stroke="{LINE}" stroke-width="2"/>'
b += text(40, 590, '봐야 할 것은 검증의 비율이 아니라 막대 전체의 길이다', 21, MUTED, 'start')
save('verified-task-cost.svg', '검증된 작업 하나에 드는 전체 비용',
     '검증을 아끼면 재작업이 늘고, 무조건 늘리면 검증 비용이 커진다. 위험도에 맞춘 검증이 전체 비용을 줄일 수 있다는 개념도.',
     '검증된 작업 하나에 드는 전체 비용', '개념을 보여 주는 그림이다. 실제 측정값이 아니다', b, 620)


# 3. from a failure to a constraint
b = box(290, 130, 380, 62, RED_BG, RED, [('에이전트의 실패', 700)])
b += arrow([(480, 192), (480, 226)])
b += box(290, 228, 380, 62, AMBER_BG, AMBER, [('근거와 함께 기록한다', 700)])
b += arrow([(480, 290), (480, 324)])
b += box(250, 326, 460, 100, '#FFFFFF', LINE, [('고칠 가치가 있는가?', 700), ('반복 · 위험도 · 기대 효과 · 적용 비용', 400)], 21)
b += arrow([(710, 376), (758, 376)], AMBER)
b += text(734, 362, '아직', 18, AMBER)
b += box(760, 340, 160, 72, AMBER_BG, AMBER, [('기록만 유지', 700)], 21)
b += arrow([(480, 426), (480, 488)], TEAL)
b += text(498, 464, '고친다', 19, TEAL, 'start')
b += text(480, 520, '어떤 수단으로 막을지 왼쪽부터 따져 본다', 20, MUTED)
b += box(40, 540, 270, 100, TEAL_BG, TEAL, [('① 설계로 없앤다', 700), ('API · 구조 · 리팩터링', 400)], 21)
b += arrow([(310, 590), (343, 590)])
b += box(345, 540, 270, 100, TEAL_BG, TEAL, [('② 검사로 막는다', 700), ('린트 · 테스트 · CI', 400)], 21)
b += arrow([(615, 590), (648, 590)])
b += box(650, 540, 270, 100, PURPLE_BG, PURPLE, [('③ 산문으로 남긴다', 700), ('지침 · 사람의 리뷰', 400)], 21)
b += arrow([(480, 640), (480, 688)], TEAL)
b += box(290, 690, 380, 62, TEAL_BG, TEAL, [('효과를 다시 확인한다', 700)])
b += arrow([(290, 721), (22, 721), (22, 259), (288, 259)], TEAL, dash=True)
b += text(36, 488, "다음 기록으로", 18, TEAL, "start")
save('failure-to-constraint.svg', '실패가 제약이 되기까지',
     '실패를 기록하고 고칠 가치를 판단한 뒤, 설계, 검사, 산문 순서로 수단을 고르고 효과를 다시 확인하는 흐름.',
     '실패가 제약이 되기까지', '실패를 곧바로 규칙으로 만들지 않고, 판단을 한 번 거친다', b, 790)
