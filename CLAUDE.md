# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 이 저장소의 정체

이 저장소는 **애플리케이션이 아니라** Velog 블로그 글을 위키처럼 탐색하도록 재정리한 Jekyll 문서 사이트다. 모든 Jekyll 소스는 `docs/`에 있고, 나머지(`README.md`, `_meta/`, `AGENTS.md`)는 GitHub 탐색용일 뿐 빌드되는 사이트에 포함되지 않는다. 본문은 한국어이며, 별도 요청이 없으면 한국어 문장과 출처 표기를 그대로 보존한다.

`AGENTS.md`(한국어)가 규칙을 더 자세히 다루는 권위 있는 기여 가이드다. 이 파일에 없는 내용은 `AGENTS.md`를 참고한다.

## 명령어

모든 명령은 Ruby 3.2 환경에서 `docs/` 안으로 이동해 실행한다.

```bash
cd docs
bundle install                                       # Jekyll + Just the Docs 설치
bundle exec jekyll serve --livereload                # 로컬 미리보기
bundle exec jekyll build --baseurl "/ai-agent-diary" # 프로덕션과 동일한 방식으로 docs/_site 생성
```

테스트 프레임워크는 없다. "검증"은 다음을 뜻한다: Jekyll 빌드 성공, 내부 링크 연결, 표·코드 블록 렌더링, 한글·영문 검색 동작 확인. SCSS·레이아웃 변경은 데스크톱과 모바일 너비 모두에서 검토한다. `docs/_site/`는 절대 커밋하지 않는다.

## 아키텍처

- **테마:** [Just the Docs](https://just-the-docs.com/), `docs/_config.yml`에서 설정한다. `baseurl`은 `/ai-agent-diary`(GitHub Pages 프로젝트 사이트)이며, 이 값과 저장소 이름이 어긋나면 링크가 깨진다.
- **내비게이션은 front matter로 구동된다.** 모든 게시 글은 YAML front matter에 `title`, `parent`, `nav_order`, `permalink`를 정의하고, 바로 아래에 `title`과 동일한 H1을 둔다. 사이드바 트리는 파일 위치가 아니라 `parent`/`nav_order`로 구성된다. `series/*/README.md`가 섹션의 부모이며, 하위 글들이 `parent`로 이를 가리킨다.
- **콘텐츠 구성:** `docs/index.md`(홈, 직접 구성한 카드 아카이브), `docs/series/<series-name>/`(순번 글 + 부모 README), `docs/standalone/`(단독 글).
- **검색:** `docs/_includes/lunr/custom-index.js`의 커스텀 Lunr 인덱싱(한글·영문에 맞춤). 테마 스타일 오버라이드는 `docs/_sass/custom/custom.scss`.
- **배포:** `main`에 push하면 `.github/workflows/pages.yml`이 `JEKYLL_ENV=production`으로 `docs/`를 빌드해 GitHub Pages에 배포한다. 워크플로는 이 하나만 유지한다.

## 어기면 문제가 생기는 규칙

- **파일명:** 연재 글은 3자리 순번(`001-ai-task-grading.md`), 단독 글은 `YYYY-MM-DD-topic-slug.md` 형식.
- **내부 링크는 후행 슬래시가 붙은 permalink**(`./series/agent-sdd/001-ai-task-grading/`)를 쓰고, `.md` 주소로는 링크하지 않는다.
- YAML과 SCSS는 공백 두 칸으로 들여쓰고, 파일은 UTF-8을 사용한다.
- 하나의 커밋에는 일관된 문서·사이트 변경 하나만 담고, 제목은 명령형으로 쓴다(예: `Fix documentation navigation and search`).

## 작업 절차 (AGENTS.md 기준)

Medium 이상 변경은 구현 전에 짧은 명세(AS-IS, TO-BE, 영향 파일, 제약 조건, 검증 기준)를 작성한다. 오타 같은 Trivial 작업은 직접 수정할 수 있다. Pages 워크플로, 내비게이션, `_config.yml`, 검색, 데이터 구조처럼 영향이 큰 변경은 리뷰 대상으로 명확히 표시한다.
