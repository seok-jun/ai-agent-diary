# 인간과 AI의 판단 글 게시 명세

## AS-IS

- 원문 `human-ai-judgment.md`는 저장소 밖 다운로드 폴더에 있다.
- `Standalone`에는 개발 및 AI 활용 관련 단독 글 3편이 등록되어 있다.
- 홈과 단독 글 목록의 글 수 및 링크는 수동으로 관리한다.

## TO-BE

- 원문을 2026-07-21자 `Standalone` 게시글로 추가한다.
- 인간의 승인과 불투명한 AI 판단을 표현한 전용 썸네일을 추가한다.
- 홈과 단독 글 목록에 새 글을 노출하고 전체 글 수를 갱신한다.

## 영향 파일

- `docs/standalone/2026-07-21-human-ai-judgment.md`
- `docs/assets/images/standalone/2026-07-21-human-ai-judgment/thumbnail.png`
- `docs/standalone/README.md`
- `docs/index.md`

## 제약 조건

- 한국어 원문과 참고문헌을 보존한다.
- 게시글 front matter, 날짜 표기, 이미지 경로, permalink 관례를 따른다.
- 썸네일에는 생성형 이미지의 오탈자 위험을 피하기 위해 문자를 넣지 않는다.

## 검증 기준

- front matter의 `title`과 본문의 H1이 일치한다.
- 홈과 `Standalone` 목록에서 새 permalink로 이동할 수 있다.
- 썸네일 경로가 실제 파일과 일치한다.
- Jekyll 빌드와 `git diff --check`가 성공한다.
