# AI 개발 활동 대시보드: 구현 및 보안 경계

## 목적

사용자의 Codex 프로필 누적·일별 토큰과 GitHub 개발 활동을 `/activity/`에 표시한다. 독자는 인증 없이 통계만 조회한다. 블로그는 Jekyll/Just the Docs, GitHub Pages를 그대로 사용한다.

## 수집·게시 경로

- Windows 원클릭 `update-activity.cmd` → `_meta/activity/one-click.ps1`.
- Codex 통계는 로그인된 로컬 Codex CLI와 버전 고정된 비공식 `codex-usage-analyzer@0.4.1`에서 읽는다. 승인한 날짜·숫자만 새 JSON으로 구성한다.
- GitHub는 읽기 PAT의 `GET /user`로 사용자 ID를 확인하고, 블로그 소유자 ID와 다르면 즉시 중단한다.
- `GET /user/repos`의 모든 페이지에서 **토큰으로 읽을 수 있는** 개인·협업·조직 Public/Private 저장소를 자동 발견한다. 저장소를 수동 입력받지 않는다. 집계 기간은 Codex 가장 오래된 일별 기록일부터 전날(KST)까지이다.
- 기본 브랜치 본인 작성 커밋, 본인 작성 병합 PR, 본인 작성 완료 이슈를 일별 합산한다. 통계 게시용 자동 커밋은 제외한다. 코드 추가·삭제량은 API 비용 때문에 원클릭 기본값에서 집계하지 않는다.
- 수집이 전부 성공하고 `validate`를 통과해야, **블로그 저장소만 쓰기 가능한 별도 PAT**로 `docs/assets/activity/data.json` 한 파일을 `main`에 갱신한다. API 리다이렉트는 금지하며, 변경이 없으면 커밋하지 않는다. 기존 Pages 워크플로가 변경을 배포한다.

## 보안 정책

- Fine-grained PAT 두 개: 집계 대상 읽기 전용, 블로그 단일 저장소의 Contents 쓰기 전용. 값은 Windows 로그인 사용자별 DPAPI로 암호화하여 체크아웃 **외부** `%LOCALAPPDATA%AIActivityDashboard`에 보관한다. 사용자/저장소 목록을 공개 파일, GitHub 이슈, Actions 로그에 기록하지 않는다.
- 수집기는 원본 API 응답·stderr·인증 헤더를 출력하지 않는다. GitHub API는 고정 `https://api.github.com` 호스트에만 접근하고 리다이렉트를 따르지 않는다.
- 정적 공개 JSON은 닫힌 스키마를 검증하여 숫자와 날짜 외의 자유 텍스트, 저장소 식별자, 메시지, SHA, 사용자 정보를 거부한다. UI는 가변 데이터를 `textContent`로 표시한다.
- 예약 작업과 수동 실행은 해당 PowerShell 프로세스에서만 `RemoteSigned` 정책을 적용한다. 시스템 정책이나 GPO 우회 목적이 아니다.
- 누락·오류·권한 부재 시 수집을 중단하고 **불완전한 집계를 공개하지 않는다**. 최대 API 1,000 요청 예산을 초과해도 실패한다.

## 남는 위험과 검증 상태

- **게시 권한이 탈취되면** 블로그의 파일 수정이 가능하다. 짧은 PAT 만료기간, 게시 토큰의 저장소 단일 범위, 로컬 PC 보안 관리가 필요하다.
- **비공개 저장소라도 날짜별 활동량과 숫자 자체는 공개**되므로 업무 패턴이 추론될 수 있다.
- **외부 npm 패키지**는 버전을 고정했지만, 패키지 공급망과 로컬 사용자 계정 침해 가능성을 없애지 못한다.
- GitHub Fine-grained PAT의 'All repositories'는 선택한 Resource owner 범위에 한정된다. 다른 소유자·조직의 Private 저장소는 해당 권한이 없으면 자동으로 수집되지 않는다.
- 회귀 테스트는 날짜·정수 스키마, 개인 정보 canary, 원자적 파일 갱신, 페이지네이션, 자동 발견, 다른 계정 키 차단, 집계 실패 보존 등의 합성 입력을 포함한다.
- **Windows 실기기의 Codex 로그인·PAT·네트워크·실제 Pages 배포 통합 검증은 아직 미완료**. PR #27은 Draft 상태를 유지하고 프로덕션 병합은 사용자 판단에 따른다.
