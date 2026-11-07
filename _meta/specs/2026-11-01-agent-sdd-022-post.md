# Agent SDD 연재 22편 게시 명세

상태: 2026-11-07 게시(작성자 결정, 23편과 함께). 11월 1일 초안에서 시점 표현(게시일, "지금 판", 확인 범위 제목)만 고치고 23편 링크를 더했다.

## AS-IS

- 연재는 21편(preview.1~2 공개)까지다. 공개 저장소는 2026-10-31에 `v1.0.0-preview.7`을 냈고, 같은 날 `main` 첫 화면을 v1 소개로 바꿨다(v0.2는 아래로).
- 다른 세션에서 쓴 초안(저장소 밖)은 사실관계는 맞지만 릴리스 노트처럼 무겁고 내부 용어가 많았다.

## TO-BE

- 연재 22편 `022-first-task-from-the-readme.md`. 위치는 작성자가 연재 22편으로 골랐다(2026-11-01).
- 중심 이야기: README를 처음 온 사람 기준으로 다시 쓰고, 새 Agent에게 README만 주고 첫 작업까지 시켜 본 일. 규칙을 지킨 실행이 멈춘 자리에서 모델 규칙을 바꾼 것, macOS 확인, 답안지가 보였던 행동 평가.
- 21편 끝의 예고(기록 이야기)는 언급하지 않는다(작성자 결정).
- "확인된 것"은 네 줄로 줄이고 세부는 공개 기록 링크로 넘긴다. 설치 방법은 빠른 시작 링크로 보낸다.
- 내부 용어(c′, runner v2, must_not, INVALID, fixture, Review A/B, REQUIRED, condensed)는 쓰지 않거나 풀어 쓴다.

## 영향 파일

- `docs/series/agent-sdd/022-first-task-from-the-readme.md` (신규)
- `docs/series/agent-sdd/README.md`: 용어 표의 adaptive-agentic-sdd 설명("21·22편"), `last_modified_at`
- `README.md`(저장소 루트): 연재 편수 21 → 22
- 홈·연재 목차·편수는 front matter에서 자동 생성된다.

## 제약

- 숫자는 공개 저장소 `v1.0.0-preview.7` 태그의 `README.md`, `ko/README.md`, `CHANGELOG.md`, `docs/eval-results/`에 있는 것만 쓴다.
- 효과(결과·재작업·비용)를 재지 않았다는 점, 행동 평가가 약한 근거라는 점을 흐리지 않는다.
- 비공개 제품·저장소 이름, 회사 일, 사람과 나눈 대화 내용은 쓰지 않는다. 다른 도구를 이름으로 비교하지 않는다(실행에 쓴 도구 이름만 적는다).
- 썸네일은 이번에 만들지 않았다. 필요하면 글 내용에 맞게 새로 구상한다.

## 본문 숫자와 근거

| 본문 | 근거(태그 기준) |
| --- | --- |
| 10/30~31 이틀에 preview.3~7, 10/31 밤 preview.7 | 태그 날짜(preview.3 10/30 11:42 KST ~ preview.7 10/31 23:45 KST) |
| `main` 첫 화면 v1, v0.2는 아래로, 함께 관리하지 않음 | 공개 `main` README, CHANGELOG Unreleased |
| 등급 네 개와 각 등급의 절차, 자동 격상을 낮추지 못함 | `ko/README.md` 깊이가 어떻게 달라지나 |
| preview.3 등급 넷·Epic 묶음, preview.5 영어판 채움, preview.6 README 재작성 | CHANGELOG preview.3·5·6 |
| 첫 사용 실행 네 번과 결과, Windows 한 대, 사람 답 미리 제공, 로컬 bare remote | `docs/eval-results/2026-10-31-first-use/README.md`, CHANGELOG preview.7 Limits |
| 모델 규칙 완화의 범위, 의미를 바꾼 변경 | `ko/README.md` 모델 routing, CHANGELOG preview.7 Policy |
| macOS 88개 중 하위 테스트 2개 실패, 별칭으로 88개 통과, 수정 뒤 89개 통과, 보조 진행 | `docs/eval-results/2026-10-31-macos-first-use/README.md`, CHANGELOG preview.7 Portability |
| 행동 평가 기준선 21/14/1, 22/14/0, 낡은 사례로 실패 6번 | `docs/eval-results/2026-10-30/README.md` |
| 정답 파일 노출, preview.6 확인 4/6 | CHANGELOG preview.7 Evaluation records, preview.6 Bounded behavior check |
| 새 실행기에서 Codex 파일 읽기 실패, Claude 부분 근거, 실행기 미수정 | `docs/eval-results/2026-10-31-routing-cprime/README.md` |
| Windows 89개, 두 판 × 두 작업 관리 방식 설치·검사 | `ko/README.md` 이번 릴리스, CHANGELOG preview.7 Validation |

## 검증 기준

- `bundle exec jekyll build --baseurl "/ai-agent-diary"` 성공, `git diff --check` 통과.
- front matter와 H1 일치, 내부 링크는 permalink와 후행 슬래시.
- 연재 목차에 22편이 나타나고 범위가 "9~22편"으로 바뀌는지 확인.
- 본문에서 내부 용어, 비공개 이름, 로컬 경로 검색 결과 0건.
