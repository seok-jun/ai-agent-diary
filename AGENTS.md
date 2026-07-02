# 저장소 가이드라인

## 프로젝트 구조 및 모듈 구성

이 저장소는 애플리케이션이 아니라 Jekyll 기반 문서 사이트다. 사이트 소스는 `docs/`에 둔다. 홈페이지는 `docs/index.md`, 연재 글은 `docs/series/<series-name>/`, 단독 글은 `docs/standalone/`에서 관리한다. 테마 스타일 수정은 `docs/_sass/custom/`, 검색 확장은 `docs/_includes/`에 둔다. 사이트에 배포하지 않을 가져오기 기록과 메타데이터는 `_meta/`에 보관한다. GitHub Pages 배포 워크플로는 `.github/workflows/pages.yml` 하나만 유지한다.

## 빌드, 테스트 및 개발 명령

Ruby 3.2 환경에서 `docs/`로 이동한 뒤 실행한다.

```bash
bundle install
bundle exec jekyll serve --livereload
bundle exec jekyll build --baseurl "/ai-agent-diary"
```

`bundle install`은 Jekyll과 Just the Docs 의존성을 설치한다. `jekyll serve`는 로컬 미리보기를 실행하고, `jekyll build`는 GitHub Pages와 같은 방식으로 `docs/_site/`을 생성한다. `_site/`은 커밋하지 않는다. 커밋 전에는 `git diff --check`로 불필요한 공백 오류를 확인한다.

## Markdown 스타일 및 이름 규칙

파일은 UTF-8을 사용하고 YAML과 SCSS는 공백 두 칸으로 들여쓴다. 모든 게시 글은 front matter에 `title`, `parent`, `nav_order`, `permalink`를 정의하고, 바로 아래에 `title`과 동일한 H1 제목을 둔다. 연재 글은 `001-ai-task-grading.md`처럼 3자리 순번을 사용한다. 단독 글은 `YYYY-MM-DD-topic-slug.md` 형식을 따른다.

배포 페이지 링크는 `./001-ai-task-grading/`처럼 permalink와 후행 슬래시를 사용한다. `.md` 주소로 링크하지 않는다. 별도 요청이 없다면 한국어 본문과 출처 표기를 보존한다.

## 에이전트용 SDD 작업 절차

Medium 이상 변경은 구현 전에 AS-IS, TO-BE, 영향 파일, 제약 조건, 검증 기준을 짧은 명세로 작성한다. 단순 오타 같은 Trivial 작업은 직접 수정할 수 있다. 보류된 결정과 후속 작업은 백로그에 남긴다. 워크플로, 내비게이션, 데이터 구조처럼 영향이 큰 변경은 구현과 리뷰를 분리한다.

## 테스트 지침

별도 테스트 프레임워크나 커버리지 기준은 없다. Jekyll 빌드 성공, 내부 링크 연결, 표와 코드 블록 렌더링, 한글·영문 검색 동작을 확인한다. SCSS나 레이아웃 변경은 데스크톱과 모바일 너비에서 모두 검토한다.

## 커밋 및 Pull Request 지침

최근 커밋처럼 `Fix documentation navigation and search` 형태의 짧고 명령형인 제목을 사용한다. 하나의 커밋에는 하나의 일관된 문서 또는 사이트 변경만 담는다.

PR에는 변경 내용, 변경 이유, 검증 방법을 적는다. 레이아웃 변경에는 스크린샷을, 내비게이션 수정에는 영향받는 URL을 포함한다. `_config.yml`, 검색 기능, Pages 워크플로 변경은 명확히 표시한다. 인증 정보, 개인키, 로컬 환경 파일, 분석 서비스 비밀값은 절대 커밋하지 않는다.