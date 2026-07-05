# 다음 글 아이디어

## Agent SDD 실무 개발 시리즈

- **PR 완료 후 business 문서 자동 동기화 (project-rules.md 기반 운영 규칙)**
  - 배경: [004-sdd-artifacts-keep-or-delete](../docs/series/agent-sdd/004-sdd-artifacts-keep-or-delete.md) 작성 중 codex 리뷰에서 나온 제안. AGENT.md/CLAUDE.md(프로젝트 기조) → project-rules.md(SDD 산출물 운영 규칙) → business 문서(현행 도메인 지식) 구조로 역할을 나누고, PR 완료 시점에 Agent가 diff·코드를 기준으로 business 문서를 자동 승격/갱신하게 만드는 아이디어(`/business-doc-sync` 같은 커맨드 포함).
  - 보류 이유: 아직 실제로 시도해본 적 없는 설계라, 지금 쓰면 이 시리즈의 "직접 겪은 것만 쓴다"는 톤과 어긋남.
  - 조건: 실제 프로젝트에 project-rules.md를 만들어 Agent에게 몇 번 시켜본 뒤, "해보니 이랬다" 식으로 쓸 것.
