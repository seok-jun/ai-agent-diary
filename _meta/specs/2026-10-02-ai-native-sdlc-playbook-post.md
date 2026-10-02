# AI-Native SDLC 플레이북 단독 글 게시 명세

## AS-IS

- Anthropic의 [The AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook)(2026.08.21)을 다룬 글이 사이트에 없다.
- 단독 글은 7편이며, 저장소 소개(`README.md`)의 단독 글 편수는 3편으로 남아 있다.

## TO-BE

- 처음 접하는 독자도 이해할 수 있도록 플레이북을 한국어로 재구성한 단독 글을 2026-10-02자로 게시한다.
- 용어 표, 단계별 비교표, 산출물·게이트 표, 역할 변화 표, 측정 지표 표와 SVG 도식 4개(병목 이동, 여섯 단계 고리, control band 대응, 도입 순서)를 포함한다.
- 단독 글 목록, 홈, 저장소 소개에 새 글과 편수(8편)를 반영하고, 기존 단독 글의 `nav_order`를 하나씩 뒤로 민다.

## 영향 파일

- `docs/standalone/2026-10-02-ai-native-sdlc-playbook.md`
- `docs/assets/images/standalone/2026-10-02-ai-native-sdlc-playbook/*.svg`
- `docs/standalone/README.md`, `docs/index.md`, `README.md`
- 기존 단독 글 7편의 front matter `nav_order`

## 제약 조건

- 원문에서 확인한 내용과 이 글의 해석을 구분해 표시하고, 출처와 확인 기준일을 남긴다.
- 도식은 기존 단독 글 SVG와 같은 밝은 배경 팔레트와 글꼴 스택을 쓴다.
- 테마, 검색 설정, Pages 워크플로는 변경하지 않는다.

## 검증 기준

- Jekyll 빌드와 `git diff --check`가 성공한다.
- 홈·단독 글 목록·사이드바에서 새 글이 맨 위에 보이고 열린다.
- 표와 코드 블록, SVG 도식이 렌더링되고 내부 링크가 연결된다.

## 백로그

- 현재 보류된 결정이나 후속 작업 없음.

## 후속 변경: 섬네일 추가

- AS-IS: 새 글에 전용 섬네일이 없고 공유 이미지도 사이트 기본값을 사용한다.
- TO-BE: 제목과 여섯 단계 고리를 담은 1600×900 섬네일을 글 상단과 front matter `image`에 연결한다.
- 영향 파일: 게시글, `docs/assets/images/standalone/2026-10-02-ai-native-sdlc-playbook/thumbnail.png`, `_meta/image-prompts/2026-10-02-ai-native-sdlc-playbook.md`.
- 검증 기준: 문자와 구성을 검토하고, 이미지 경로·공유 메타데이터가 빌드 결과에 반영됐는지 확인한다.
