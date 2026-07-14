# PR business 문서 갱신 글 추가 명세

## AS-IS

- `Agent SDD 실무 개발` 연재는 6편까지 게시되어 있다.
- 신규 원문에는 Jekyll front matter가 없고, 이전 글 링크와 이미지 경로가 게시용으로 정리되지 않았다.

## TO-BE

- 원문을 연재 7편으로 게시한다.
- 이전 실험은 연재 5편으로 연결하고, 제공된 SVG 두 개를 사이트 자산으로 포함한다.
- 연재 인덱스의 편수, 소개, 목록, 읽기 순서를 7편 기준으로 갱신한다.

## 영향 파일

- `docs/series/agent-sdd/007-pr-business-docs-skill.md`
- `docs/series/agent-sdd/README.md`
- `docs/assets/images/agent-sdd/007-pr-business-docs-skill/*`

## 제약 조건

- 한국어 원문과 수치, 출처 맥락을 보존한다.
- 게시 링크는 permalink와 후행 슬래시를 사용한다.
- 생성된 `_site/`은 커밋 대상에 포함하지 않는다.

## 검증 기준

- front matter의 `title`과 본문의 H1이 일치한다.
- 이전 글 링크와 SVG 경로가 실제 파일 및 permalink와 연결된다.
- Jekyll 프로덕션 빌드와 `git diff --check`가 성공한다.