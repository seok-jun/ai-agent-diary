# AI 개발 활동 수집

Windows에서 Codex 토큰과 GitHub 개발 활동을 갱신하는 원클릭 도구입니다.

## 실행

1. [PR #27](https://github.com/seok-jun/ai-agent-diary/pull/27)을 검토하고 `main`에 병합한 뒤, 블로그 저장소를 PC에 받아둡니다.
2. Python 3.10 이상, Node.js 20 이상, **로그인된 Codex CLI**를 준비합니다.
3. GitHub Fine-grained PAT 두 개를 준비합니다.
   - **집계용:** 대상 저장소의 Contents·Pull requests·Issues 읽기 권한
   - **게시용:** `seok-jun/ai-agent-diary`만 Contents 읽기·쓰기 권한
4. **`update-activity.cmd` 더블클릭.** 첫 실행에만 두 키와 공개 동의를 입력합니다. 매일 자동 실행 등록도 선택할 수 있습니다.

이후에는 같은 파일을 더블클릭하면 됩니다. 키 변경은 `configure-activity.cmd`를 실행하세요.

## 알아둘 점

- GitHub ID·저장소 목록은 **집계용 키로 자동 조회**합니다. '전체'는 **그 키가 접근 가능한 저장소 전체**이며, 다른 소유자·조직의 비공개 저장소는 별도 권한이 필요할 수 있습니다.
- 키는 PC 사용자 계정에 암호화해 저장하고, **숫자·날짜 통계만** 블로그에 공개합니다. Private 저장소 이름·제목·메시지는 게시하지 않습니다. 다만 활동량과 날짜 자체는 공개됩니다.
- 외부 분석 도구 [codex-usage-analyzer 0.4.1](https://github.com/postmelee/codex-usage-analyzer)을 사용합니다. 인증 정보는 공유하지 마세요.
- 작업은 기존 GitHub Pages 배포를 사용합니다. PC가 꺼져 있으면 갱신이 지연됩니다.

**상태:** Windows 실기기에서 인증·게시까지 통합 검증은 아직 완료하지 않았습니다. PR 병합 전에는 실제 블로그에 게시하지 마세요.
