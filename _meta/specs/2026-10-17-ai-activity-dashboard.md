# AI 개발 활동 대시보드 명세

## 분류와 합의

- 공통 분류 절만 적용: P3(기존 블로그 이용 장애 없음), Epic(수집 모듈 신설; 개인정보·스케줄 경계 포함).
- 저장소: 공개 `seok-jun/ai-agent-diary`, 기본 브랜치 `main`. 작업 브랜치에서 PR까지 진행하며 직접 병합하지 않는다.
- 사용자 확인: 공개·비공개를 합산한 일별 숫자만 공개한다. 실제 수집 대상은 사용자가 비공개 설정에서 명시한다. 비공개 실데이터 수집은 이번 작업에서 실행하지 않는다.

## AS-IS

- `docs/`의 Jekyll 4.3 + Just the Docs. `Asia/Seoul`, 프로젝트 baseurl `/ai-agent-diary`.
- Pages 워크플로 하나가 모든 main push를 빌드한다. 별도 CI·테스트 프레임워크·수집기는 없다.
- 참조 대화에 사용자가 제공한 2026-10-16 Codex summary와 125개 일별 bucket이 있으며, bucket 합계는 lifetimeTokens와 일치한다.
- 현재 환경에는 Ruby가 없어 격리된 로컬 도구로 빌드 검증을 준비한다.

## TO-BE

- `/activity/`에 날짜·월 선택, 누적/일별/월별 토큰, 연속 활동/최장 작업, GitHub 커밋·병합 PR·완료 이슈·가능한 변경 줄 수를 표시한다. 최초 GitHub 상태는 미수집으로 표시한다.
- Codex: 비공식 analyzer의 JSON stdout을 메모리에서 수신하거나 비공개 로컬 파일을 입력받는다. contractVersion 1의 승인된 날짜·정수 필드만 새 객체로 재구성한다. 원본·stderr·예외 내용은 출력/저장하지 않는다. 중복 날짜·잘못된 날짜/수치·불일치는 실패시키며 기존 공개 파일을 유지한다.
- GitHub: 명시한 저장소 목록만 REST로 조회한다. 모든 페이지를 처리하고 로그인 기준 작성 커밋(기본 브랜치, committer date), 본인 작성 병합 PR(merged_at), 본인 작성 completed 이슈(closed_at)를 KST 일별로 합산한다. 변경량은 해당 커밋의 additions/deletions이며 병합 커밋은 중복을 막기 위해 제외한다. 합산 수치는 AI 기여의 인과 증거가 아니다.
- 수집은 날짜 구간을 통째로 교체해 재실행 중복을 방지한다. 실패/권한 거부는 부분 집계나 0으로 덮지 않는다. GitHub 누적은 수집 구간의 누적임을 명시한다.
- 공개 JSON은 닫힌 스키마로 검증한다. 저장소 이름·경로·제목·메시지·SHA·계정·인증값·자유 텍스트·원본 응답은 넣지 않는다. 민감 설정은 repo 외부 또는 Secret에만 둔다. API 응답과 오류는 메모리에서만 처리한다.
- 기본 운영은 로그인한 Windows 사용자 세션에서 하루 한 번 수집, 변경된 안전 JSON만 전용 브랜치로 커밋 후 PR을 수동 생성/검토한다. 수집기가 git push/병합을 수행하지 않는다.
- 기존 Pages 워크플로 하나를 유지하고 docs 경로 변경으로 트리거를 제한한다. 선택적 하루 1회 Actions 수집 예시는 `_meta/` 문서에만 제공하며 기본 활성화하지 않는다. 읽기 전용 Fine-grained PAT 또는 App 설치 토큰을 사용한다.

## 영향 파일과 제약

- 허용: `docs/activity.md`, `docs/assets/activity/*`, `docs/index.md`(링크), `docs/_sass/custom/custom.scss`(대시보드 범위 스타일), `.github/workflows/pages.yml`(경로 필터), `.gitignore`, `_meta/activity/*`, 이 명세, README 링크.
- 기존 글, 검색 구현, 테마/의존성, `_config.yml`, 다른 워크플로는 수정하지 않는다. 새 배포 서비스나 전체 CI는 추가하지 않는다.
- 초기 Codex 수치는 사용자 제공 자료를 검증 후 재구성한다. GitHub 실데이터·비공개 설정은 PR에 포함하지 않는다.

## 검증 기준

- 개인정보 canary를 입력 원본/오류에 섞어도 공개 출력·로그에 등장하지 않는다. 허용 목록/strict validation, 원자적 쓰기, 실패 시 기존 파일 보존을 테스트한다.
- API pagination, 사용자 필터, KST 경계, completed/not_planned 구분, 병합·중복 SHA, 날짜 구간 재실행, 미수집/0 구분을 합성 응답으로 검증한다.
- Jekyll production build, 새 내부 URL/검색, JS 문법·동작, 데스크톱·모바일 화면/키보드 사용을 확인한다.
- 구현과 별도의 리뷰를 실시하고, PR에 검증 결과와 남은 인증/스케줄 설정을 기록한다.

## 백로그

- 사용자 승인된 실제 저장소 목록·읽기 전용 인증 설정 후 GitHub 최초 수집.
- 사용자 PC에서 analyzer 설치 경로/버전 확인 후 Task Scheduler 등록. 자동 등록·활성화하지 않는다.
- 필요 시 사용자 선택으로 하루 한 번 Actions 수집을 활성화한다. Codex는 로그인 세션이 있는 로컬에서만 수집한다.

## 구현·검증 결과

- Python 16개, JavaScript 4개 테스트 통과. 허용 목록·민감 canary·원자적 쓰기·실패 보존·동시 실행 잠금·페이지네이션·KST 경계·작성자·완료 사유·SHA 중복·미수집 구간을 검증했다.
- 독립 설계/구현 리뷰 실시. 저장소 이름의 대소문자 차이로 PR/이슈가 이중 집계되는 문제를 수정하고 회귀 테스트를 추가했다. 실제 비공개 저장소/API는 조회하지 않았다.
- 격리된 로컬 Ruby 3.2.11에서 기존 Gemfile로 `JEKYLL_ENV=production bundle exec jekyll build --baseurl '/ai-agent-diary'` 성공. 소스 Gemfile과 `_config.yml`은 변경하지 않았다.
- 홈/활동 페이지의 로컬 링크 109개 대상 모두 존재하고 `_meta/`는 빌드 결과에 없다. 한국어 `AI 개발 활동` 및 영문 `Codex` 검색 결과 확인. 브라우저 오류 로그 없음.
- 390×844, 1280×900에서 페이지 가로 넘침 없음. 일별 2026-10-16은 17,877,204, 10월은 2,489,502,945, 누적은 6,221,527,557토큰으로 표시된다. 월 내역은 마지막 관측일까지 먼저 보인다. 스크린샷은 `_meta/activity/screenshots/`에 있다.
- 추가 CI/예약 실행/실제 인증/프로덕션 병합은 활성화하지 않았다. 기본 운영은 로그인 세션에서 수집 후 안전 JSON만 PR로 검토하는 방식이다.
