# Agent SDD 연재 12~14편 (차세대 전환) 게시 명세

## AS-IS

- Agent SDD 연재는 11편까지 게시되어 있고, 홈·연재 목록·저장소 소개의 편수도 11편이다.
- 차세대 전환(모델 발전에 따른 가드레일 재평가, 방법론과 프로젝트 분리)을 다룬 글은 없다. 분리 구상만 10편에 있다.
- 글의 근거가 되는 실험 기록은 비공개 개발 저장소에 있어 독자가 볼 수 없다.

## TO-BE

- 2026-10-02자로 연재 12~14편을 게시한다.
  - 12편: 가드레일이 걸림돌이 된 건 아닌지 의심하게 된 과정과, 걷어내기 전에 먼저 재보기로 한 이유.
  - 13편: 보조 절차 하나만 넣고 빼는 첫 비교 실험과 판정 보류.
  - 14편: 두 번의 실험을 멈춘 격리 문제와 멈춘 뒤에 지킨 것.
- 편마다 섬네일 1장과 본문 SVG 도식(12편 4장, 13편 3장, 14편 3장)을 넣고, front matter `image`에 섬네일을 연결한다.
- 연재 목록, 홈의 시리즈 카드, 저장소 소개에 세 편과 편수(14편)를 반영한다.

## 영향 파일

- `docs/series/agent-sdd/012-outgrown-guardrails.md`
- `docs/series/agent-sdd/013-removing-one-guardrail.md`
- `docs/series/agent-sdd/014-isolation-stopped-the-experiment.md`
- `docs/assets/images/agent-sdd/012-outgrown-guardrails/`, `013-removing-one-guardrail/`, `014-isolation-stopped-the-experiment/`의 `thumbnail.png`와 `*.svg`
- `docs/series/agent-sdd/README.md`, `docs/index.md`, `README.md`
- `_meta/image-prompts/012-014-agent-sdd-next-gen.md`

## 제약 조건

- 공개 글이 비공개 저장소 링크에 의존하지 않도록 과제 설명, 판정표, 결과 수치를 본문에 직접 싣는다.
- 수치는 개발 저장소의 기록 그대로 쓰고, 체감과 측정값을 구분해 적는다. 실험이 보류·중단된 사실을 성공처럼 쓰지 않는다.
- 비유(보조바퀴와 헬멧, 교실 시험, 평지 자전거)는 설명을 위해 이 글에서 붙인 것이다.
- 도식은 기존 단독 글 SVG와 같은 밝은 배경 팔레트와 글꼴 스택을 쓰고, 섬네일은 10편 섬네일의 구성을 따른다.
- 테마, 검색 설정, Pages 워크플로는 변경하지 않는다.

## 검증 기준

- Jekyll 빌드와 `git diff --check`가 성공한다.
- 홈·연재 목록·사이드바에서 세 편이 열리고, 글 사이의 이전·다음 링크가 연결된다.
- 표와 SVG 도식, 섬네일이 렌더링된다.
- 빌드 결과의 `og:image`·`twitter:image`가 각 섬네일을 가리킨다.

## 검증 결과 (작성 시점)

- `git diff --check` 통과, 본문이 참조하는 이미지 13개의 파일 존재 확인.
- SVG와 섬네일은 헤드리스 Chrome으로 렌더링해 글자 겹침과 잘림을 확인했다.
- 작성 환경의 Ruby가 2.6이라 Jekyll 빌드는 실행하지 못했다. 병합 후 Pages 빌드와 공개 URL에서 확인이 필요하다.

## 백로그

- 같은 날짜(2026-10-02) 글이 다섯 편이라 홈 "최근 글"의 정렬과 NEW 배지 위치가 의도와 다를 수 있다. 필요하면 게시일을 나누거나 `date`에 시각을 넣는다.
- 15편 이후(외부 연결 구현과 OS 독립성, 적응 규칙의 효과, 공개 버전업)는 해당 검증이 끝난 뒤 쓴다.
