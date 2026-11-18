# AI 코딩 에이전트를 믿는 방법이 바뀌고 있다 — 게시 기록

- 요청: 작성자가 넘긴 완성 초안(2026-11-18)을 단독 글 형식에 맞춰 올린다. 발표 이미지를 넣을 수 있으면 넣고, 어색하거나 번역투인 표현을 다듬는다.
- 상태: 초안 반영. 커밋·게시 전. 작성자 검토 필요.
- 분류: P3 / Trivial. 게시 콘텐츠와 비동작 메타데이터만 다룬다.
- AS-IS: 단독 글 13편. 이 발표를 다룬 글 없음.
- TO-BE: `docs/standalone/2026-11-18-trusting-ai-coding-agents.md` 추가, nav_order 1 부여, 기존 단독 글 순번 +1, README의 단독 글 편수 14편으로 갱신.
- 근거와 공개 범위: 공개 발표(AI Engineer CODE 2026, Lauren Tan)의 공식 요약 페이지와 자동 생성 자막, 공개 저장소(`seok-jun/adaptive-agentic-sdd`)만 다룬다. 회사 실무 내용 없음.
- 초안에서 바꾼 것:
  - 부제를 도입 한 줄로 옮기고, 절 제목을 `## 1.` 형식으로 맞췄다.
  - 역피라미드 목록, 코드·주석·검증 장치의 역할, 기계적 판단 세 단계를 표로 바꿨다.
  - 코드 블록에 `js` 언어 표시를 붙였다.
  - "그녀", "~라는 점이다", "개인적으로" 같은 번역투·반복 표현을 줄였다. 주장과 근거의 내용은 바꾸지 않았다.
  - Anthropic 글 두 개의 링크를 사이트의 다른 글이 쓰는 `/engineering/` 주소로 맞췄다.
  - Agent SDD 연재 목차와 Eval 단독 글로 가는 내부 링크를 하나씩 추가했다.
- 발표 사실 대조(공식 페이지 자막 기준): 본인 PR 약 3,000개/월, Cursor의 타이머·주석 사례, 주석 99% 금지, Cindy의 검증 토큰 70% 언급은 자막과 일치한다.
- 작성자 확인이 필요한 곳:
  1. 제품 이름 "Grok Bot". 자동 자막은 Grabbot·Grockbot·graphbot으로 흔들려서 표기를 확인하지 못했다. 공식 페이지의 소속 표기는 SpaceXSI다.
  2. 발표 이미지. 공식 요약 페이지의 발표 화면 캡처(`trust-pyramid.jpg`, 854×480, 약 29KB)를 블로그 자산으로 받아 2절 본문에 썼다.
  4. 섬네일(`thumbnail.png`, 1672×941). 이미지 생성 모델을 쓰지 않고 `_meta/scripts/thumbnail-2026-11-18-trusting-ai-coding-agents.html`의 SVG를 헤드리스 Chrome으로 캡처했다. 앞 글들의 따뜻한 크림색·굵은 제목 분위기를 따랐지만 수채화풍 일러스트는 아니다. 문구 "같은 실수를 또 한다면, 규칙보다 환경을"은 초안에 없던 것이다.
  5. 본문 그림 3장(`workaround-spread.svg`, `verified-task-cost.svg`, `failure-to-constraint.svg`). `_meta/scripts/draw-trusting-agents-diagrams.py`로 만든다. 비용 그림의 막대 길이는 개념을 보여 주는 값이고 측정값이 아니다.
- 함께 바꾼 것(2026-11-18): 목차가 없던 단독 글 10편(이 글 포함)에 기존 4편과 같은 목차 블록(`{: .no_toc }`, `<details>` + `{:toc}`)을 넣어 단독 글 14편을 통일했다.
  3. 참고 자료의 Formal verification, Codex as a platform은 본문에서 직접 인용하지 않는다. 초안대로 남겼다.
- 검증: front matter·H1 일치, 내부 링크 permalink 존재, 이미지 경로, 코드 블록 짝, 공백 검사를 했다. 이 PC에 Ruby가 없어 Jekyll 빌드와 화면 확인은 하지 못했다.
