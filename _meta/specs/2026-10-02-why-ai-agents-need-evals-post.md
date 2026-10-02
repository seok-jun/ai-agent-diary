# AI 에이전트 Eval 필요성 단독 글 게시 명세

## AS-IS

- 단독 글 중에 Eval을 주제로 한 글이 없다. Eval은 AI-Native SDLC 플레이북 글의 용어 표와 테스트 단계, World's Fair 정리 글의 Uber 세션, Agent SDD 연재 8편(Skill Eval 실행 기록)에서 부분적으로만 다룬다.
- "왜 Eval이 필요한가"를 처음 접하는 독자 기준으로 설명한 글이 없다.
- 단독 글은 8편이다.

## TO-BE

- Anthropic의 [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)(2026.01.09)를 중심 출처로, Eval이 왜 필요한지를 비유 위주로 풀어 쓴 단독 글을 2026-10-02자로 게시한다.
- 용어 표(시험 비유 열 포함), 일반 프로그램과 에이전트 비교표, Eval이 필요한 이유 표, 고객 사례 표, 채점자 비교표, 실력·회귀 시험 표, 평가 방법 비교표, 시험지 함정 표, 시작 로드맵 표와 SVG 도식 4개(두더지 잡기 대 Eval 고리, 시험지 구조, pass@k·pass^k 그래프, 스위스 치즈 모델)를 포함한다.
- 1600×900 섬네일을 글 상단과 front matter `image`(공유 이미지)에 연결한다.
- 단독 글 목록, 홈, 저장소 소개에 새 글과 편수(9편)를 반영하고, 기존 단독 글의 `nav_order`를 하나씩 뒤로 민다.

## 영향 파일

- `docs/standalone/2026-10-02-why-ai-agents-need-evals.md`
- `docs/assets/images/standalone/2026-10-02-why-ai-agents-need-evals/*.svg`, `thumbnail.png`
- `docs/standalone/README.md`, `docs/index.md`, `README.md`
- 기존 단독 글 8편의 front matter `nav_order`
- `_meta/image-prompts/2026-10-02-why-ai-agents-need-evals.md`

## 제약 조건

- 원문에서 확인한 내용과 이 글의 비유·해석을 구분해 표시하고, 출처와 확인 기준일을 남긴다.
- 도식은 기존 단독 글 SVG와 같은 밝은 배경 팔레트와 글꼴 스택을 쓴다.
- 테마, 검색 설정, Pages 워크플로는 변경하지 않는다.

## 검증 기준

- Jekyll 빌드와 `git diff --check`가 성공한다.
- 홈·단독 글 목록·사이드바에서 새 글이 맨 위에 보이고 열린다.
- 표와 SVG 도식, 섬네일이 렌더링되고 내부 링크가 연결된다.
- 빌드 결과의 `og:image`·`twitter:image`가 새 섬네일을 가리킨다.

## 백로그

- 현재 보류된 결정이나 후속 작업 없음.
