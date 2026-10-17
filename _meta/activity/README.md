# AI 개발 활동 — Windows 원클릭 업데이트

**평소에는 저장소 루트의 `update-activity.cmd`를 더블클릭하면 끝납니다.**
Codex 통계와 지정한 GitHub 공개·비공개 저장소의 활동을 새로 조회하고, 숫자만 검증하여 블로그의 `docs/assets/activity/data.json` 한 파일을 자동 갱신합니다. 변경이 있으면 GitHub Pages가 배포됩니다. JSON 복사, git commit/push, PR 작성은 매번 필요하지 않습니다.

> **배포 전 확인:** 이 실행기는 현재 작업 PR(#27)의 일부입니다. 최초 1회 PR을 검토하고 `main`에 병합한 뒤 로컬에서 사용하세요. PR이 병합되기 전에는 게시 단계가 실패합니다. 병합 자체를 자동화하지는 않습니다.

## 딱 한 번만 준비

1. Windows PC에 **Python 3.10 이상, Node.js 20 이상, 로그인된 Codex CLI**가 있어야 합니다. 사용하던 `npx`가 동작하는 PC에서 실행하세요. Codex CLI는 `codex.cmd --version`으로 확인할 수 있지만, 원클릭 실행기가 실제 `codex.exe`를 자동 탐색하므로 평소에 명령어를 입력할 필요는 없습니다.
2. 집계 대상 GitHub 저장소를 정합니다. Private 저장소도 가능하며, 첫 실행 시 `owner/name`을 쉼표로 구분해 입력합니다. 공개 저장소에 이 목록이 기록되지 않습니다.
3. [GitHub Fine-grained PAT 발급 화면](https://github.com/settings/personal-access-tokens/new)에서 **용도가 다른 토큰 두 개**를 준비합니다.
   - **집계용 PAT:** 선택한 대상 저장소만 접근하도록 하고 **Contents / Pull requests / Issues = Read-only**. Private 저장소는 이 토큰으로 읽습니다.
   - **게시용 PAT:** 오직 `seok-jun/ai-agent-diary` 한 저장소에 **Contents = Read and write**. 다른 Private 저장소에 접근하게 하지 마세요. 토큰 만료 전 갱신해야 합니다.
4. 이 저장소를 PC에 내려받은 상태에서 **`update-activity.cmd`를 더블클릭**합니다. 첫 실행에만 사용자 ID, 집계 저장소, 시작일, 두 토큰, 공개 게시 동의를 입력합니다. 등록을 원한다면 **매일 23:30 Windows 작업 스케줄러** 설정도 선택할 수 있습니다.

설정은 저장소 바깥의 **`%LOCALAPPDATA%\AIActivityDashboard`**에 저장됩니다. 토큰은 로그인한 Windows 사용자의 DPAPI로 암호화됩니다. 작업 스케줄러도 **로그인한 사용자 세션에서만** 실행합니다. 개인 PC가 꺼져 있거나 로그아웃 중에는 즉시 실행되지 않으며, 지원되는 경우 다음 로그인 때 실행될 수 있습니다.

토큰 교체, 저장소 변경, 집계 시작일 변경은 **`configure-activity.cmd`**를 더블클릭하세요. 원클릭 실행기가 다시 초기 설정을 받습니다.

## 더블클릭하면 일어나는 일

1. 설치된 Codex CLI의 Windows native `codex.exe`를 찾아 비공식 `codex-usage-analyzer@0.4.1`을 **고정 버전**으로 실행합니다. 최초 사용 시 해당 npm 패키지를 다운로드할 수 있습니다. 이 외부 패키지를 신뢰하는지 [소스](https://github.com/postmelee/codex-usage-analyzer)를 확인하세요. `latest`를 임의로 실행하지 않습니다.
2. 기존 Python 수집기(`collect.py`)가 총 토큰·날짜별 버킷을 검증하고, **숫자·날짜 외의 원본 정보는 버립니다.** 원본 출력과 인증 응답은 공개 JSON/로그로 저장하지 않습니다.
3. GitHub REST API로 선택한 저장소의 **기본 브랜치 본인 작성 커밋, 병합된 본인 PR, 완료된 본인 이슈**를 지정된 집계 시작일부터 **어제(한국 시간)**까지 다시 계산합니다. 계산 중 하나라도 실패하면 게시를 중단합니다. 코드 추가/삭제 줄 수는 별도 선택 사항이며 API 요청량이 늘어납니다.
4. **기존 공개 JSON 전체를 재검증**한 뒤, GitHub Contents API로 `main`의 오직 `docs/assets/activity/data.json` 한 파일만 갱신합니다. 변경이 없으면 커밋하지 않습니다. main 업데이트가 성공하면 기존 Pages 워크플로가 사이트를 배포합니다.

**중요:** 이 프로그램을 실행하면 공개용 통계가 곧바로 `main`에 게시됩니다. 첫 설정에서 이에 동의해야 하며, 게시용 PAT는 블로그 단일 저장소로 제한해야 합니다. 브랜치 보호 규칙이 업데이트를 막는 경우에는 실패를 알려주고, 규칙을 우회하지 않습니다. GitHub Actions 사용량을 늘리는 별도 일별 수집 워크플로는 만들지 않습니다. 게시 시 기존 Pages 배포는 1회 실행됩니다.

## 표시와 집계 한계

- 현재 PR에 들어 있는 `2026-10-16`의 **62억 토큰은 사용자가 제공한 초기 스냅샷**입니다. 첫 원클릭 수집 성공 후 새 계정 집계로 교체됩니다. 성공하지 못하면 실시간 통계라고 표시하면 안 됩니다.
- GitHub 숫자는 **설정한 저장소·시작일부터의 활동만** 집계합니다. Codex 전체 토큰과 GitHub 생산성의 1:1 인과관계를 의미하지 않습니다.
- GitHub의 오늘 활동은 그날 도중 집계하면 흔들리므로 **어제까지** 집계합니다. Codex는 실행 시점까지 집계합니다.
- 토큰 합산 및 GitHub 수집이 실패하면 블로그 게시는 중지됩니다. Private 저장소명, URL, 이슈·커밋 본문, 작성자 목록, 인증 토큰, 원본 API 응답은 공개 파일에 기록하지 않습니다.
- PC가 꺼져 있거나 Codex 계정 로그인/비공식 프로필 API가 만료되면 갱신이 실패할 수 있습니다. 그런 날은 기존 공개 값이 유지되며 **새 값처럼 꾸미지 않습니다**.

## 문제 발생 시

- `Python` 또는 `npx.cmd`를 못 찾음: Windows에서 Python 3.10+ / Node.js 20+를 설치하고 새로운 터미널 환경에서 다시 실행합니다.
- `codex.exe`를 못 찾음: Codex CLI가 설치·로그인되었는지 확인합니다. 현재 구현은 기본 npm 설치 경로와 PATH에서 자동 탐색합니다.
- GitHub 집계 실패: 두 토큰의 만료/저장소별 권한, 조직 SSO 승인, 첫 설정에서 지정한 저장소·시작일을 확인하세요. 읽기용 토큰은 게시에 사용하지 않습니다.
- 게시 실패: **PR #27을 main에 병합했는지**, 게시용 PAT에 블로그 저장소 Contents 쓰기 권한이 있는지 확인합니다.
- Settings 변경: **`configure-activity.cmd` 더블클릭**. 민감한 토큰·전체 API 오류를 GitHub 이슈나 채팅에 붙이지 마세요.

Windows PowerShell의 로컬 `.ps1` 실행을 위해 `.cmd`가 PowerShell을 **해당 프로세스에서만** `-ExecutionPolicy Bypass`로 시작합니다. PC의 영구 실행 정책을 변경하지 않습니다. 회사 PC/GPO가 이를 금지한다면 해당 정책을 우회하지 말고 개인 PC에서만 사용하세요.

## 개발자 참고

기존 수집 엔진과 검증 테스트는 유지했습니다. 수동 진단이 필요하면 아래를 실행할 수 있지만, **평소 사용자는 실행할 필요가 없습니다.**

```powershell
python -m unittest discover -s _meta/activity -p 'test_*.py'
node --test _meta/activity/dashboard.test.cjs
python _meta/activity/collect.py validate
```

수집·변환은 `_meta/activity/collect.py`, Windows 원클릭과 DPAPI 인증·자동 게시는 `_meta/activity/one-click.ps1`, 게시 데이터 스키마는 `docs/assets/activity/data.json`을 참고하세요. Windows 원클릭 실행은 실제 사용자 PC에서의 인증/네트워크 통합 확인이 별도로 필요합니다.
