# AI 개발 활동 수집 운영

이 문서와 수집기는 사이트에 배포되지 않는다. 공개 파일은 `docs/assets/activity/data.json` 하나다. 방문자는 인증 없이 이 파일만 읽는다. 초기 Codex 기록은 사용자가 제공한 2026-10-16 contractVersion 1 출력의 안전한 숫자와 날짜 125개를 재구성했다. GitHub는 아직 미수집이다.

## 1. 수집 전 확인

- Python 3.10 이상. 추가 Python 패키지는 필요 없다.
- Windows 로그인 세션에서 사용 중인 `codex-usage-analyzer`의 설치 출처와 버전을 사용자가 확인한다. 이 저장소는 비공식 도구를 설치하거나 `npx`로 최신 버전을 자동 실행하지 않는다. 실제 설치된 실행 파일 절대 경로를 사용한다. `.cmd` 실행 파일도 지원한다.
- analyzer의 `--json` 출력은 `contractVersion: 1`, `capturedAt`, `summary`, `dailyUsageBuckets`를 가져야 한다. 도구가 바뀌면 공개 스키마를 느슨하게 풀지 말고 비공개 환경에서 호환성을 확인한다. 로그인 정보·세션 원문을 Actions로 옮기지 않는다.
- 원본 JSON·설정·토큰 파일은 반드시 **공개 저장소 외부**의 개인 폴더에 둔다. `docs/`, `_meta/`, GitHub issue/PR/로그에 원본을 붙이지 않는다. 민감한 내용을 포함한 전체 명령/응답 출력이나 PowerShell 디버그 trace를 공유하지 않는다.

## 2. Codex 로컬 수집

저장소 루트에서 실제 절대 경로로 바꿔 실행한다.

```powershell
python _meta/activity/collect.py codex --analyzer 'C:\path\to\codex-usage-analyzer.cmd'
python _meta/activity/collect.py validate
```

기존 원본 파일을 입력하려면 저장소 밖의 파일을 지정한다.

```powershell
python _meta/activity/collect.py codex --input 'C:\private-activity\usage.json'
```

수집기는 stdout을 메모리에서 읽고 허용한 필드만 새 객체로 만든다. analyzer stderr·원본 파일은 복사하지 않는다. 알 수 없는 입력 필드는 버리며, 날짜/정수/중복/합계/일 최고치 검증을 통과해야 공개 파일을 원자적으로 교체한다. 스냅샷을 다시 가져와도 중복 합산하지 않는다. 연속 활동과 최장 작업은 도구의 summary 값이며, 현재 날짜로 추정하거나 재계산하지 않는다. 첫 bucket 전의 날짜와 마지막 수집일 뒤는 미수집으로 표시한다.

## 3. GitHub 최소 권한 인증과 대상

**이번 PR은 실제 비공개 저장소를 조회하지 않았다.** 사용자가 집계 대상 저장소를 선택한 뒤 설정한다. 공개·비공개별 구분 수치나 저장소별 수치는 저장하지 않는다.

Fine-grained PAT를 [발급](https://github.com/settings/personal-access-tokens/new)할 때:

- Resource owner와 **Only select repositories**에서 실제 집계할 저장소만 선택한다. 조직 저장소는 조직 승인·SSO 및 정책을 확인한다. 여러 owner는 각각의 토큰/설정을 별도 운영해야 한다. 이 최소 구현은 실행당 토큰 하나와 그 토큰이 접근 가능한 대상 목록만 지원한다.
- Repository permissions: **Contents: Read-only**, **Pull requests: Read-only**, **Issues: Read-only**. Metadata 읽기는 기본 부여된다. Administration/Actions/Workflows 쓰기는 수집에 필요 없다.
- 짧은 만료일을 설정하고 만료 전에 교체한다. 기본 `GITHUB_TOKEN`은 다른 비공개 저장소를 읽는 인증으로 사용하지 않는다.
- 대안: 같은 읽기 권한의 GitHub App을 선택한 저장소에 설치하고, 짧은 수명의 installation token을 `ACTIVITY_READ_TOKEN`으로 주입한다. App private key를 공개 checkout에 저장하지 않는다.

저장소 밖 `C:\private-activity\github.json`에 다음 형태를 저장한다. 아래 저장소는 공개 예시이며, 실제 비공개 이름은 로컬 파일 또는 Actions Secret에만 입력한다.

```json
{
  "login": "seok-jun",
  "repositories": ["seok-jun/ai-agent-diary"],
  "since": "2026-10-01",
  "withLines": true
}
```

`since`부터 어제(KST)까지 **전체 구간을 재집계하여 교체**한다. 페이지 제한까지 모두 읽으며, 요청 예산 1,000회를 초과하거나 403/404/429 등 하나라도 실패하면 GitHub 기존 기록을 유지한다. 부분 성공을 0으로 게시하지 않는다. 빈 저장소(409)도 실패하므로 대상에서 빼거나 초기 커밋 후 수집한다. 최근 한 달부터 시작하면 호출량을 줄일 수 있다. `since`를 뒤로 옮기면 과거 공개 GitHub 집계는 제거된다. 대상 변경 시에도 전체 구간을 재집계하므로 서로 다른 대상의 증분을 섞지 않는다. 저장소가 많거나 이력이 길면 범위를 줄이고 `withLines: false`로 호출량을 줄인다. 변경량은 커밋당 추가 요청이 필요하다. 자동 재시도는 하지 않는다.

GitHub 집계의 한계:

- 커밋은 author가 해당 GitHub login에 연결된 기본 브랜치의 커밋이며 committer date로 묶는다. 연결되지 않은 이메일·다른 브랜치·삭제/force-push된 커밋은 제외될 수 있다. merge commit은 커밋 수에 포함하지만 줄 수에서는 제외한다. 동일 SHA는 지정한 저장소 전체에서 한 번만 센다.
- PR/이슈는 본인 **작성** 기준이다. 다른 사람 PR을 병합하거나 다른 사람 이슈를 닫은 행위는 별도 집계하지 않는다. 이슈는 현재 `closed`이면서 `state_reason: completed`인 항목만 센다. 다시 열린 이슈/PR의 이전 상태 이력을 복원하는 이벤트 장부가 아니다.
- 줄 수는 커밋 stats의 합계이며 최종 코드베이스 크기·순수 작업량·AI 생성 비율을 뜻하지 않는다. squash/rebase에 따라 커밋 수가 달라질 수 있다.

토큰을 명령 인자에 쓰지 않는다. 로컬 예약 실행에는 같은 Windows 사용자만 복호화하는 DPAPI 파일을 사용할 수 있다. 저장소 밖 개인 폴더에서 한 번 실행한다(조직 장치 정책과 폴더 접근 권한도 확인).

```powershell
$activitySecret = Read-Host 'Read-only fine-grained PAT' -AsSecureString
$activitySecret | ConvertFrom-SecureString | Set-Content -LiteralPath 'C:\private-activity\read-token.dpapi'
Remove-Variable activitySecret
```

수집 실행 예시:

```powershell
& .\_meta\activity\run-local.ps1 `
  -Python 'C:\path\to\python.exe' `
  -Analyzer 'C:\path\to\codex-usage-analyzer.cmd' `
  -GitHubConfig 'C:\private-activity\github.json' `
  -EncryptedToken 'C:\private-activity\read-token.dpapi'
```

Codex와 GitHub는 독립 갱신이다. 한 수집이 실패하면 해당 원본의 기존 값은 유지되고 전체 실행은 실패 코드로 끝난다. 두 실행이 동시에 공개 파일을 갱신하지 않도록 `.collect.lock`을 사용한다. 프로세스 강제 종료로 lock이 남았다면 실행 중인 수집기가 없는지 확인한 후 lock 파일 하나만 제거한다.

## 4. 하루 한 번 Windows 예약 실행 (기본 권장)

먼저 수동 수집·검증에 성공한 뒤 **작업 스케줄러 → 작업 만들기**에서 등록한다. 이 PR은 작업을 자동 등록하지 않는다.

1. 일반: 현재 사용자, **사용자가 로그온할 때만 실행**. 관리자 권한은 필요 없다.
2. 트리거: 매일 23:30 등 하루 한 번. PC가 꺼져 있으면 건너뛰거나, 설정에서 가능한 다음 시점에 실행하도록 선택한다. GitHub는 어제까지, Codex는 수집 순간까지 반영한다.
3. 동작: Windows PowerShell 실행 파일을 지정한다. 인수는 아래의 경로를 실제 값으로 바꾼다. 실행 정책은 PC의 기존 승인된 정책을 따른다. `Bypass`로 전역 정책을 바꾸지 않는다.

```text
-NoProfile -NonInteractive -WindowStyle Hidden -File "C:\checkout\ai-agent-diary\_meta\activity\run-local.ps1" -Python "C:\path\to\python.exe" -Analyzer "C:\path\to\codex-usage-analyzer.cmd" -GitHubConfig "C:\private-activity\github.json" -EncryptedToken "C:\private-activity\read-token.dpapi"
```

4. 설정: 중복 실행 시 **새 인스턴스를 시작하지 않음**, 실행 제한 30분. 실패는 Task Scheduler 종료 코드로 확인하고 원본/민감 디버그 로그를 공개하지 않는다. DPAPI 복호화는 암호화한 동일 사용자/PC에서만 가능하다.
5. 정기 갱신 전용 checkout/브랜치를 사용한다. 수집기는 커밋·push·PR 생성·병합을 수행하지 않는다. 변경된 공개 JSON만 검토 후 PR로 반영한다.

```powershell
python _meta/activity/collect.py validate
git diff --check
git diff --stat
git add -- docs/assets/activity/data.json
git diff --cached --name-only
git commit -m 'Update safe activity aggregates'
git push
```

변경이 없으면 커밋하지 않는다. PR 본문에는 집계 구간과 검증 결과만 적는다. 원본/설정/저장소 목록은 첨부하지 않는다. `main`으로 직접 push하거나 자동 병합하지 않는다. `[skip ci]`는 Pages 배포까지 막으므로 데이터 배포 커밋에는 붙이지 않는다.

## 5. Actions 대안 — 기본 비활성, Codex 수집 금지

현재 `.github/workflows/pages.yml` 하나만 유지한다. 추가 전체 CI·예약 실행은 활성화하지 않았다. 기본 Pages push 트리거는 `docs/**`와 해당 워크플로 변경으로 제한되어 `_meta/`·README만 바뀐 main 커밋은 빌드하지 않는다. 데이터가 PR로 병합될 때만 기존 Pages 배포가 한 번 실행된다.

로컬 예약 대신 Actions가 꼭 필요하면, 사용자가 기존 단일 워크플로에 아래 설정을 적용한다.

1. Settings → Secrets and variables → Actions → Repository secrets에 `ACTIVITY_READ_TOKEN`(위 읽기 전용 PAT 또는 App 설치 토큰), `ACTIVITY_CONFIG_JSON`(로컬 설정과 같은 JSON)을 추가한다. App 설치 토큰은 짧은 수명이므로 예약 실행마다 발급하는 App 방식으로 바꾸거나 PAT를 사용한다. 토큰·설정값을 코드/로그/PR 본문에 넣지 않는다. Repo Actions의 debug logging도 끈다.
2. `on`에 `schedule: [{cron: '43 15 * * *'}]`(KST 매일 00:43)를 추가한다. 기존 `build` job에는 `if: github.event_name != 'schedule'`을 추가해 예약 수집이 Jekyll을 빌드하지 않게 한다. `deploy`는 build를 needs로 의존하므로 함께 건너뛴다.
3. 아래 job을 **기존 워크플로에만** 추가한다. 수집은 1회, 최대 15분, 결과물은 검증된 JSON 하나만 1일 보존한다. 외부 repo 토큰은 Python 단계에만 전달하며 checkout은 기본 `GITHUB_TOKEN`으로 한다. 원본 API 응답을 artifact/cache에 넣지 않는다.

```yaml
  collect-activity:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    timeout-minutes: 15
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - name: Collect numeric GitHub aggregates
        env:
          ACTIVITY_READ_TOKEN: ${{ secrets.ACTIVITY_READ_TOKEN }}
          ACTIVITY_CONFIG_JSON: ${{ secrets.ACTIVITY_CONFIG_JSON }}
        run: python3 _meta/activity/collect.py github
      - name: Validate public fields
        run: python3 _meta/activity/collect.py validate
      - uses: actions/upload-artifact@v4
        with:
          name: safe-activity
          path: docs/assets/activity/data.json
          retention-days: 1
          if-no-files-found: error
```

4. 성공한 artifact의 안전 JSON을 내려받아 검증한 뒤 전용 브랜치 PR로 반영한다. 최신 Codex 기록이 있다면 JSON 전체를 오래된 artifact로 덮지 않고 `github` 섹션만 반영하여 전체를 재검증한다. 자동 쓰기 권한·프로덕션 직접 반영·무인 PR 자동화는 이번 최소 기능 범위에 포함하지 않는다.

## 검증

```powershell
python -m unittest discover -s _meta/activity -p 'test_*.py'
node --test _meta/activity/dashboard.test.cjs
python _meta/activity/collect.py validate
cd docs
bundle exec jekyll build --baseurl '/ai-agent-diary'
```

공개 스키마는 `collect.py`의 `validate()`가 권위 있는 허용 목록이다. 새 필드는 UI·개인정보 검토·검증을 함께 변경해야 한다. GitHub 인증/원본 오류는 의도적으로 고정된 일반 오류만 출력한다. 문제를 조사할 때 비공개 환경에서 권한과 기간을 확인하며 API 응답을 공개 로그에 추가하지 않는다.

공식 근거: [커밋 API](https://docs.github.com/en/rest/commits/commits), [PR API](https://docs.github.com/en/rest/pulls/pulls), [이슈 API](https://docs.github.com/en/rest/issues/issues), [Fine-grained PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens), [Actions 경로 필터](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).
