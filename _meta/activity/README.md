# AI 개발 활동 — Windows 원클릭 업데이트

**평소에는 저장소 루트의 `update-activity.cmd`를 더블클릭하면 끝납니다.**

실제 Codex 토큰 통계와 GitHub 개발 활동을 새로 조회한 후, 검증한 숫자만 공개 블로그의 `docs/assets/activity/data.json`으로 자동 게시합니다. 매번 JSON 복사·git 명령·수동 PR 작업을 할 필요가 없습니다.

> 현재 코드는 **PR #27의 Draft 브랜치**에 있습니다. 검토 후 `main`에 병합해야 실제 블로그 게시가 가능합니다. 최초 병합만 수동으로 하고, 이후 데이터 갱신은 실행기가 담당합니다.

## 최초 1회: 키 두 개만 준비하세요

Windows PC에 **Python 3.10+, Node.js 20+, 로그인된 Codex CLI**가 필요합니다. 프로그램은 기본 설치 경로에서 실제 `codex.exe`를 탐색하고, 고정 버전인 `codex-usage-analyzer@0.4.1`로 사용량을 가져옵니다. 해당 도구는 [외부 오픈소스](https://github.com/postmelee/codex-usage-analyzer)이며, 처음 실행 시 npm에서 다운로드될 수 있습니다.

[GitHub Fine-grained PAT](https://github.com/settings/personal-access-tokens/new) **두 개**를 발급하고, 저장소 루트의 **`update-activity.cmd`**를 더블클릭하세요.

- **집계용 키:** Contents / Pull requests / Issues 읽기 권한. 공개·비공개를 **모두** 집계하려면 PAT의 Repository access가 **All repositories**여야 합니다. 이 설정도 **해당 Resource owner 범위**에만 적용됩니다.
- **게시용 키:** **`seok-jun/ai-agent-diary` 한 저장소에만** Contents 읽기·쓰기 권한. Private 프로젝트에 쓰기 권한을 부여하지 마세요.

실행기에서 물어보는 내용은 **집계용 키, 게시용 키, 통계 공개 동의, 매일 23:30 자동 갱신 여부**입니다. **GitHub ID, 저장소 목록, 시작일은 묻지 않습니다.** 키를 채팅이나 GitHub 이슈에 붙여 넣지 마세요.

키는 Windows 사용자별 DPAPI를 통해 암호화되며 저장소 바깥의 `%LOCALAPPDATA%\AIActivityDashboard`에 저장합니다. 키나 자동 실행 옵션을 변경하려면 `configure-activity.cmd`를 더블클릭하세요.

## 매번 실행하면?

1. Codex 통계를 실제 로그인된 CLI에서 다시 읽고, 누적·일별 숫자 정합성을 검증합니다.
2. **집계용 PAT로 `GET /user`를 호출해 GitHub 로그인 ID를 자동 판별**합니다.
3. **`GET /user/repos`를 끝 페이지까지 조회**하여 토큰이 접근할 수 있는 개인/협업/조직 저장소를 자동 발견합니다. Private 저장소도 토큰 권한이 있으면 포함됩니다.
4. 발견한 전체 저장소에서 **본인 작성 기본 브랜치 커밋, 본인 작성 병합 PR, 본인 작성 완료 이슈**를 수집합니다. GitHub 집계 기간은 Codex의 가장 오래된 일별 사용 기록부터 **어제(한국 시간)까지**로 자동 설정합니다. 최초 입력, 수집 설정 파일이나 수동 목록 관리가 필요 없습니다.
5. 데이터 검증에 성공한 경우에만 **검증된 공개용 숫자 JSON 한 파일**을 GitHub API로 `main`에 게시합니다. 변경이 없으면 커밋하지 않고, 게시가 되면 기존 Pages 워크플로가 한 번 실행됩니다.

실행 창에는 **발견한 저장소 개수와 Private 개수만** 표시합니다. 이름, 저장소 경로, 커밋 메시지, PR/이슈 제목, API 원문, 인증 키는 공개 파일에 저장하지 않습니다. 자동 갱신 때문에 생성된 'Update safe AI development activity aggregates' 커밋은 개발 활동 수에서 제외합니다.

## '전체 저장소'의 정확한 의미

**자동으로 찾아주는 범위는 '집계용 PAT에 접근 권한이 부여된 저장소 전체'입니다.** 키가 Only select repositories이면 그 목록만 보입니다. 다른 소유자·조직의 비공개 저장소는 별도 리소스 소유자 권한과 승인이 필요할 수 있으며, 인증으로 발견되지 않은 저장소를 임의로 세지 않습니다.

현재 구현은 **토큰 하나**로 접근 가능한 저장소를 조회합니다. 서로 다른 소유자별 PAT를 합치는 기능은 아직 없습니다. 접근 가능한 저장소가 0개이거나 API 예산(최대 1,000 요청)·권한 문제가 발생하면 **불완전한 숫자를 게시하지 않고 중단**합니다. 저장소 수가 많으면 초기 집계에 시간이 걸릴 수 있습니다. 이력 전체를 반복 조회하므로 추후 증분 최적화가 필요할 수 있습니다. 코드 변경 줄 수는 비용 절약을 위해 기본 수집 대상에서 제외하지만 커밋/PR/이슈는 집계합니다.

GitHub 수치는 Codex와 기간을 비교하기 위한 **관측 구간 누적**이지 GitHub 계정 생성일부터의 전체 커밋 개수가 아닙니다. Codex는 실행 시점까지, GitHub는 한국 시간 어제까지 집계합니다. PC가 꺼져 있거나 로그아웃 상태이면 예약 실행이 지연될 수 있습니다.

## 오류와 안전

- **인증 실패:** 집계용 PAT가 All repositories인지, Contents/PR/Issues 읽기 권한이 있는지, 조직 승인·SSO가 필요한지 확인하세요.
- **게시 실패:** PR #27이 `main`에 병합되었는지, 게시용 키가 해당 저장소의 Contents 쓰기 권한이 있는지 확인하세요.
- **Codex 실패:** 로그인된 CLI와 Node.js/Python 설치, [사용량 분석 도구](https://github.com/postmelee/codex-usage-analyzer)의 고정 버전 동작을 확인하세요.
- **설정 재입력:** `configure-activity.cmd` 더블클릭.

Windows PowerShell 실행 정책은 시스템 전체에서 변경하지 않습니다. `.cmd`는 개인 Windows PC에서 해당 PowerShell 프로세스에 한해 `-ExecutionPolicy Bypass`로 실행하므로, 회사 보안 정책이 있는 기기에서는 회사 정책을 따르세요.

수집 실패 시 공개 데이터를 부분 덮어쓰지 않습니다. 다만 수집기 내부의 로컬 JSON은 먼저 변경될 수 있으니, 게시 전 전체 검증을 재실행합니다. 토큰은 영구 환경변수로 저장하지 않습니다.

## 개발자용 점검 (일반 사용자는 불필요)

```powershell
python -m unittest discover -s _meta/activity -p 'test_*.py'
node --test _meta/activity/dashboard.test.cjs
python _meta/activity/collect.py validate
```

수집 구현: `_meta/activity/collect.py` · Windows 실행기: `_meta/activity/one-click.ps1` · 공개 JSON: `docs/assets/activity/data.json`.

**Windows 실기기에서 키 인증부터 Pages 배포까지 실제 통합 검증은 아직 진행하지 못했습니다.** PR은 Draft로 유지합니다.
