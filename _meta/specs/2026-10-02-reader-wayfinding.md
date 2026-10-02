# 처음 온 독자 길 찾기 명세

> 리뷰 대상: `_config.yml`(front matter defaults, Sass 설정), 새 레이아웃 `_layouts/agent-sdd-post.html`을 추가하는 변경이다.

## AS-IS

- Agent SDD 14편의 "작성 시점의 기록" 안내가 글 본문마다 `{% include agent-sdd-notice.html %}`로 들어가 있다. 문구나 위치를 바꾸려면 14편을 다시 고쳐야 한다. 안내 링크는 영문 저장소(adaptive-agentic-sdd)를 가리킨다.
- 홈의 연재 카드는 1~4편, 5~8편, 9~14편 세 묶음으로 나뉘어 있지만, 연재 목록 페이지(`series/agent-sdd/README.md`)는 14편을 한 목록으로만 보여준다.
- 로컬 빌드마다 Just the Docs 테마 Sass에서 Dart Sass 경고(@import, 전역 내장 함수, darken·lighten)가 수십 줄 나온다.

## TO-BE

- `_config.yml` defaults가 `series/agent-sdd` 아래 글에 `layout: agent-sdd-post`와 `series_notice: true`를 준다. 레이아웃이 글의 날짜 줄(`_YYYY.MM.DD 게시_`) 바로 뒤에 공용 include를 넣는다. 연재 목록 페이지는 defaults로 제외한다.
- 14편 본문은 안내를 넣기 전 상태로 되돌린다.
- 안내 문구는 사이트 말투(~다체)로 쓰고, 한국어 저장소(adaptive-agentic-sdd-ko)로 연결한다.
- 연재 목록 페이지를 홈과 같은 세 묶음으로 나누고, 묶음마다 제목·범위·한 줄 설명을 둔다.
- `_config.yml`의 `sass` 설정으로 테마 쪽 deprecation 경고를 끈다.

## 영향 파일

- `docs/_config.yml`, `docs/_layouts/agent-sdd-post.html`, `docs/_includes/agent-sdd-notice.html`
- `docs/series/agent-sdd/001~014`(include 줄 삭제만), `docs/series/agent-sdd/README.md`
- `docs/_sass/custom/custom.scss`

## 제약 조건

- 기존 글 본문은 고치지 않는다. 14편은 include 줄을 지워 안내 추가 전 상태로 돌아가는 것만 허용한다.
- 단독 글과 "AI에게 물어본 인간의 미래" 시리즈에는 안내를 넣지 않는다.
- 홈에는 "AI에게 물어본 인간의 미래" 시리즈를 계속 노출하지 않는다.
- 14편의 `last_modified_at`은 바꾸지 않는다. 독자에게 보이는 내용이 바뀐 연재 목록 페이지만 갱신한다.

## 검증 기준

- `bundle exec jekyll build --baseurl "/ai-agent-diary"`가 경고 없이 끝난다.
- 생성된 HTML에서 안내가 Agent SDD 14편에만 한 번씩, 날짜 줄 바로 뒤에 나온다.
- 새로 만들거나 바꾼 내부 링크가 모두 실제 permalink로 연결된다.
- 연재 목록 페이지가 데스크톱과 모바일 너비에서 가로 넘침 없이 보인다.

## 백로그

- 소개 페이지 문안은 글쓴이 답을 기다린다.
- 1편 상단 등급표 안내 문구는 제안만 하고 글쓴이 결정을 기다린다.
- 9~14편 묶음을 9~11편과 12~14편으로 나눌지 글쓴이 결정을 기다린다.
