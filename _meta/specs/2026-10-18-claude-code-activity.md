# Claude Code 토큰 사용량 추가

## 분류

- Priority: P2. Codex 토큰만 표시돼 Claude Code로 한 작업량이 대시보드에서 빠진다.
- SDD grade: Medium. 공개 JSON 스키마에 출처 하나를 추가하고 수집기·원클릭·화면·테스트를 함께 바꾼다.

## AS-IS

- 공개 JSON은 `codex`, `github` 두 출처만 허용하는 닫힌 스키마다.
- Claude Code에는 `codex-usage-analyzer`에 해당하는 고정 분석 도구가 없다.
- Claude Code는 로컬 대화 기록(`<설정 폴더>/projects/**/*.jsonl`)을 기본 30일 뒤 삭제한다.

## TO-BE

- 수집기 `claude` 명령이 로컬 Claude Code 설정 폴더의 대화 기록에서 `assistant` 응답의 `usage` 정수 네 개(input, output, cache creation, cache read)와 시각만 읽는다. 외부 패키지를 쓰지 않는다.
- 같은 응답이 여러 줄·여러 파일(재개·포크)에 반복되므로 `message.id`+`requestId`로 중복을 제거하고 필드별 최댓값을 쓴다. `<synthetic>` 모델 응답은 제외한다.
- 시각을 한국 시간 날짜로 묶어 `{date, tokens}`만 공개한다. 프로젝트 경로·세션 ID·모델명·메시지는 공개하지 않는다.
- 기록 삭제로 과거 날짜가 줄어들지 않도록, 기존 공개 값과 새로 계산한 값 중 날짜별 최댓값을 유지한다. 요약(`totalTokens`, `peakDailyTokens`, `activeDays`)은 일별 값에서 다시 계산하고 검증한다.
- 기존 공개 JSON에 `claude` 키가 없으면 `null`로 읽는다. `schemaVersion`은 1을 유지한다.
- 원클릭은 Claude Code 설정 폴더(`CLAUDE_CONFIG_DIR`, `%USERPROFILE%\.claude`)가 있으면 집계하고, 없으면 건너뛴다.
- 대시보드는 Claude 누적·기간별 토큰을 Codex와 나란히 표시하고, 추이·비율의 토큰 기준을 Codex / Claude Code / 합계 중에서 고르게 한다. 기본값은 기존과 같은 Codex다. 합계는 두 출처와 GitHub가 모두 수집된 날짜만 쓴다.

## 영향 파일

- `_meta/activity/collect.py`, `_meta/activity/test_collect.py`, `_meta/activity/one-click.ps1`, `_meta/activity/README.md`
- `docs/assets/activity/dashboard.js`, `docs/activity.md`, `docs/_sass/custom/custom.scss`, `_meta/activity/dashboard.test.cjs`
- `docs/assets/activity/data.json`(로컬 수집 결과)

## 제약

- PAT·게시 경로·예약 작업·Pages 워크플로·내비게이션·검색·`_config.yml`은 변경하지 않는다.
- 사용자 Claude Code 설정(`cleanupPeriodDays` 등)은 바꾸지 않는다. 외부 차트·분석 의존성을 추가하지 않는다.

## 검증 기준

- 중복 제거, KST 경계, 날짜별 최댓값 병합, 개인 정보 canary, 체크아웃 내부 폴더 거부, 구버전 JSON 읽기에 대한 Python 테스트를 통과한다.
- Claude 선택·합계 기준의 공통 기간·비율 계산에 대한 JavaScript 테스트를 통과한다.
- 데스크톱·모바일에서 Claude 표시와 토큰 기준 전환을 확인한다. Jekyll 빌드와 `git diff --check`를 확인하고 실행 불가 항목은 구분해 기록한다.

## 검증 결과

- Python 테스트 29개 통과(Claude 6개 추가): 중복 제거·KST 경계·`<synthetic>` 제외·부분 줄 무시, 날짜별 최댓값 병합, 비정상 usage·빈 폴더·체크아웃 내부 폴더 거부, 닫힌 스키마, 구버전 JSON 읽기, CLI 출력에 경로 미노출.
- JavaScript 테스트 10개 통과(Claude 2개 추가): Claude 별도 커버리지, Claude·합계 기준 공통 기간과 비율.
- 원클릭 스크립트 PowerShell 구문 분석 오류 0, 설정 폴더 탐색 함수 단독 실행 확인.
- 이 PC의 실제 기록으로 `claude` 수집 후 `validate` 통과: 2026-09-04 ~ 2026-10-18, 활동일 30일. 기존 `codex`·`github` 블록은 그대로다.
- 배포 테마에 로컬 Markdown·JavaScript·CSS·JSON을 적용한 임시 브라우저 미리보기에서 데스크톱 1280px·모바일 390px의 히어로 2개, 기록 카드 6개, 지표 카드 5개, 표 6열, 비교 토큰 3종 전환, 미수집 안내, 가로 넘침 없음, 브라우저 예외 없음을 확인했다. 스크린샷: `_meta/activity/screenshots/claude-*.png`.
- `git diff --check` 통과. 전체 Jekyll 빌드는 로컬 Ruby/Bundler가 없어 미실행이다.

## 남는 위험

- 수집 전에 삭제된 대화 기록은 복구할 수 없다. 30일보다 긴 간격으로 수집하면 그 사이 기록이 0처럼 보일 수 있다. 매일 자동 실행이나 `cleanupPeriodDays` 상향은 사용자가 결정한다.
- 이 PC에서 사용한 Claude Code만 집계한다. claude.ai 채팅, 다른 PC, 클라우드 세션은 포함하지 않는다.
- 대화 기록 형식은 공개 계약이 아니므로 Claude Code 업데이트로 바뀔 수 있다. 형식이 맞지 않으면 수집을 중단하고 기존 데이터를 유지한다.
