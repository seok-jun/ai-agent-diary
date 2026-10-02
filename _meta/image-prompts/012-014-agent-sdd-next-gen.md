# 12~14편 섬네일·도식 제작 기록

- 제작 방식: SVG로 직접 구성한 뒤 헤드리스 Chrome으로 PNG 캡처(1200×630을 2배율로 렌더링해 2400×1260). 이미지 생성 모델은 쓰지 않았다.
- 글꼴: Pretendard 우선, 없으면 Apple SD Gothic Neo 등 시스템 한글 글꼴
- 용도: 글 상단 및 Open Graph / Twitter 공유 이미지

## 섬네일 공통 구성

10편 섬네일의 틀을 따랐다. 옅은 청회색 배경에 모서리 원 두 개, 상단 알약 태그, 두 줄 제목(남색 `#2b3856`, 강조 초록 `#3d9a62`), 흰 카드 두 장과 가운데 남색 원, 하단 알약 한 줄.

| 편 | 게시 자산 | 태그 | 왼쪽 카드 | 오른쪽 카드 | 가운데 | 하단 |
| --- | --- | --- | --- | --- | --- | --- |
| 12 | `docs/assets/images/agent-sdd/012-outgrown-guardrails/thumbnail.png` | 차세대 · 왜 시작했나 | 4월의 모델 — 가드레일이 약점을 메웠다 | 10월의 모델 — 가드레일은 그때 그대로 | 6개월 | 고치기 전에 먼저 재본다 |
| 13 | `docs/assets/images/agent-sdd/013-removing-one-guardrail/thumbnail.png` | 차세대 · 첫 실험 | 조건 A — 편집 전에 변경 목록 쓰기, 17/17 통과 | 조건 B — 아무 요구 없음, 17/17 통과 | VS | 빼도 된다? → 아직 모른다 |
| 14 | `docs/assets/images/agent-sdd/014-isolation-stopped-the-experiment/thumbnail.png` | 차세대 · 실험이 멈춘 이유 | 첫 번째 실험 — 52초 · 편집 0건 | 두 번째 실험 — 앞 후보의 파일이 읽혔다 | 격리 | 사전 검사 통과 ≠ 실제로 써본 뒤 |

13편 카드의 "17/17 통과"와 14편 카드의 "52초 · 편집 0건"은 본문에 실린 실제 실험 기록이다.

## 본문 도식

기존 단독 글 SVG와 같은 팔레트(파랑 `#ddf4ff`, 노랑 `#fff8c5`, 초록 `#dafbe1`, 빨강 `#ffebe9`, 회색 `#f6f8fa`)와 글꼴 스택을 쓴 820px 폭 SVG다.

- 12편: `guardrail-gap.svg`(예전 모델과 지금 모델의 가드레일, 체감을 그린 것이며 측정값 아님), `helmet-vs-training-wheels.svg`(통제와 보조 절차), `six-months.svg`(4월~10월 타임라인), `inside-vs-outside.svg`(방법론이 프로젝트 안에 있을 때와 밖에 둘 때)
- 13편: `one-sentence-diff.svg`(두 조건의 차이), `four-runs.svg`(네 번의 실행 결과), `easy-task.svg`(쉬운 과제에서 차이가 안 보이는 이유)
- 14편: `precheck-vs-real.svg`(사전 검사와 실제 실행의 차이), `allow-beats-deny.svg`(폴더 차단과 파일에 남은 허용), `budget-kept.svg`(호출 한도 사용 내역)
