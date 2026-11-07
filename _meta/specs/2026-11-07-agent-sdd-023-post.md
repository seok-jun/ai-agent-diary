# Agent SDD 연재 23편 게시 명세

상태: 2026-11-07 게시(작성자 결정). 22편과 같은 PR로 올린다.

## AS-IS

- 연재는 22편(preview.7, 11월 1일 작성, 이번에 함께 게시)까지다. 공개 저장소는 2026-11-06 `v1.0.0`, 2026-11-07 `v1.0.1`을 냈고, 같은 날 README 첫 화면 개편(PR #11)과 1분 체험 스크립트·데모(PR #12)를 `main`에 병합했다.
- 저장소 방문은 최근 2주 4명, 스타 0개였다(작성자가 GitHub traffic에서 확인).

## TO-BE

- 연재 23편 `023-try-it-in-a-minute.md`.
- 중심 이야기: 1.0·1.0.1에서 바뀐 것(10편 구조로 방법론을 프로젝트 밖에, 일상 작업 간결 경로, 임시 파일 범위)을 짧게 적고, 아무도 써 보지 않은 이유를 첫 화면과 설치 품에서 찾아 1분 체험을 만든 일, 그 체험 환경에서 두 Agent에게 실제로 시킨 결과.
- 22편 끝의 "써 볼 사람이 있다면 이슈로"에서 이어 받는다.
- 내부 용어(W/P/M, resolver, claim, SUMMARY, PRODUCT COMPLETE, merge-tree 등)는 쓰지 않거나 풀어 쓴다. 다른 SDD 도구를 이름으로 비교하지 않는다(실행에 쓴 도구 이름만 적는다).

## 영향 파일

- `docs/series/agent-sdd/023-try-it-in-a-minute.md` (신규)
- `docs/series/agent-sdd/022-first-task-from-the-readme.md`: 23편 링크
- `docs/series/agent-sdd/README.md`: 용어 표의 adaptive-agentic-sdd 설명, `last_modified_at`
- `README.md`(저장소 루트): 연재 편수 22 → 23

## 제약

- 숫자는 공개 저장소 `main`(`da6f1cc` 이후)과 `v1.0.0`·`v1.0.1` 태그의 `CHANGELOG.md`, `docs/releases/`, `docs/eval-results/`에 있는 것만 쓴다. 저장소 밖 사실은 작성자가 확인한 방문 통계뿐이다.
- 효과(결과·재작업·비용)를 재지 않았다는 점, Large 멈춤이 예제 프로젝트 규칙을 따른 결과라는 점, Claude Code 실행이 그 Agent의 자체 보고라는 점을 흐리지 않는다.
- 비공개 제품·저장소 이름, 회사 일, 로컬 경로를 쓰지 않는다.
- 썸네일(`thumbnail.png`, 2400×1260)은 기존 연재 썸네일 구성(큰 제목·파란 강조·편수·오른쪽 일러스트)을 따라 새로 만들었다. 본문 그림은 구조도 `outside-the-project.svg`와, 공개 저장소 `docs/assets/demo.svg`(실제 Codex 실행 두 건을 줄인 애니메이션)의 사본 `demo.svg`.
- 작성자 피드백(글이 많고 썸네일이 없음)에 따라 본문을 약 30% 줄이고 텍스트 트리를 그림으로 바꿨다.

## 본문 숫자와 근거

| 본문 | 근거 |
| --- | --- |
| 1.0 11/6, 1.0.1 다음 날 아침 | 태그 `v1.0.0` 2026-11-06 19:49 KST, `v1.0.1` 2026-11-07 08:48 KST |
| 방문 4명, 스타 0개 | 작성자 확인(GitHub traffic, 2026-11-07) |
| preview.8은 태그 없이 1.0 | `docs/releases/preview.8.md` |
| 간결 경로, 임시 파일 범위, 이전 시험의 OS 임시 폴더 | `docs/releases/1.0.1.md`, `docs/eval-results/2026-11-06-small-route/README.md` |
| 다섯 언어, 첫 시도 3/5, 환경 문제 두 건, 4.5~5.7분, SUMMARY 한 번 | `docs/eval-results/2026-11-06-small-route/README.md` |
| 체험 스크립트 약 5초, 오프라인, 폴더 밖 쓰기 없음, READY 확인 | `try/setup.py`, README 빠른 시작 |
| Codex `--add-dir` 수정, Large 문구, Claude Code 원본 폴더 | PR #12 설명과 커밋 |
| Codex Small: 회귀 테스트 5개 실패 먼저, 8개 통과, 병합·종료, 두 파일 | `docs/eval-results/2026-11-07-try-sandbox/README.md` |
| Codex Large: 여섯 가지 결정, 코드 무변경, 권한 문서 근거 | 같은 기록 Results·Limits |
| Claude Code macOS: Git 2.37 대체 절차, 병합 명령 재시도, 자체 보고 | 같은 기록 Claude Code run on macOS |
| Codex 첫 시도 거부(루트가 Git 저장소 아님) | 같은 기록 Setup |
| Windows·macOS 123개, 두 판 READY, 거부 시 해시 동일, Linux 미실행 | 같은 기록 macOS check, PR #12 |

## 검증 기준

- `bundle exec jekyll build --baseurl "/ai-agent-diary"` 성공, `git diff --check` 통과.
- front matter와 H1 일치, 내부 링크는 permalink와 후행 슬래시.
- 연재 목차에 22·23편이 순서대로 나타나는지 확인.
- 본문에서 내부 용어, 비공개 이름, 로컬 경로 검색 결과 0건.
- Codex 편집 검토(어투·흐름·사실) 반영.
