# AI 에이전트 Eval 필요성 글 섬네일 제작 기록

- 제작 방식: HTML·CSS로 직접 구성한 뒤 Chromium(Playwright)으로 1600×900 PNG 캡처. 이미지 생성 모델은 쓰지 않았다.
- 글꼴: Pretendard (npm `pretendard` 패키지의 OTF)
- 게시 자산: `docs/assets/images/standalone/2026-10-02-why-ai-agents-need-evals/thumbnail.png`
- 용도: 글 상단 및 Open Graph / Twitter 공유 이미지

## 구성

- 배경: 아주 옅은 청회색(`#f4f7fb`), 모서리에 옅은 원 두 개 (AI-Native SDLC 글 섬네일과 같은 틀)
- 왼쪽: 상단 문구 "ANTHROPIC ENGINEERING · AI AGENT EVALS", 제목 "감으로는 / 고칠 수 없다"("감"만 파란색 `#2f6fde`), 부제 "AI 에이전트에 Eval이 필요한 이유", 칩 "실패 → 시험 문제 → 회귀 방지 → 숫자"
- 오른쪽: "EVAL SUITE · 에이전트 시험지" 카드. 다섯 문항(환불 요청 처리, 항공권 예약 확인, 검색이 필요 없는 질문, 파일 수정 후 테스트, 지난달 사고 재현)에 통과·실패 표시, 오른쪽 위에 빨간 채점 도장 "통과 46/50 · 지난번 42"
- 문항과 점수는 본문의 비유를 보여주기 위한 예시이며 실제 측정값이 아니다.
- 통과·실패 색은 본문 도식과 같은 팔레트(초록 `#4ac26b`, 빨강 `#ff8182`)를 쓴다.
