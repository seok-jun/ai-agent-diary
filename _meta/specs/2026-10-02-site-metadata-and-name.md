# 사이트 메타데이터와 이름 통일 명세

> 리뷰 대상: `_config.yml`, 공유 메타데이터(head include), 사이드바 내비게이션을 바꾸는 변경이다.

## AS-IS

- 사이트 이름이 세 가지로 섞여 있다. `_config.yml` 제목과 저장소 README는 "seok jun.log archive", 홈 H1·사이드바 로고는 "SJ archive"(SJ 배지 + "archive"), 홈 상단 문구는 "AI Agent Diary".
- `_includes/head_custom.html`이 `{% seo title=false %}`를 한 번 더 호출해, 테마가 이미 출력한 og:·twitter: 태그가 모든 페이지에 두 번씩 나온다.
- `twitter:` 블록에 계정이 없어 `twitter:site`가 "@"로, `twitter:creator`가 "@seok jun"으로 출력된다.
- `<html lang="en-US">`, `og:locale`은 `en_US`다.
- 홈의 og:title·twitter:title이 "Home"이고, 섬네일이 없는 페이지의 공유 이미지는 파비콘(512×512)이다.
- 사이드바 단독 글 섹션 이름이 영어 "Standalone"이다.

## TO-BE

- 이름을 "AI Agent Diary"로 통일한다: 사이트 제목, 홈 H1(워드마크), 사이드바 로고, 저장소 README 제목.
- 중복 `{% seo %}` 호출을 지워 태그가 한 번씩만 나오게 한다.
- `twitter:` 블록을 지운다. 이미지가 있으면 `twitter:card=summary_large_image`는 jekyll-seo-tag 기본값으로 계속 나온다.
- `lang: ko`, `locale: ko_KR`을 추가한다.
- 홈 `title`을 "AI Agent Diary"로 바꾸고, 기본 공유 이미지를 1200×630 `assets/images/brand/og-default.png`로 바꾼다. 글별 `image:`는 그대로 우선한다.
- 단독 글 섹션 제목을 "단독 글"로 바꾸고, 하위 글 9편의 `parent`를 맞춘다. URL(permalink)은 바꾸지 않는다.

## 영향 파일

- `docs/_config.yml`, `docs/_includes/head_custom.html`
- `docs/index.md`, `docs/standalone/README.md`, 단독 글 9편 front matter `parent`
- `docs/assets/images/brand/wordmark.svg`, `wordmark-sidebar.svg`, `og-default.png`(신규), `docs/_sass/custom/custom.scss`(홈 워드마크 최대 너비)
- `README.md`

## 제약 조건

- 글 URL, 본문, 검색 설정, Pages 워크플로는 바꾸지 않는다.
- Just the Docs에는 사이드바 전용 제목 옵션이 없어, 홈의 사이드바 항목 이름도 "Home"에서 "AI Agent Diary"로 바뀐다.

## 검증 기준

- Jekyll 빌드가 성공한다.
- 홈: og:title "AI Agent Diary", og:image `og-default.png`. 평가 글·SDLC 글: og:image가 각 글 섬네일.
- og:·twitter: 태그가 페이지마다 한 번씩만 나오고, "@"로 시작하는 twitter 태그가 없다. `<html lang="ko">`.
- 사이드바에 "단독 글"이 보이고 하위 글 9편이 모두 그 아래에 있다.
- 데스크톱(1280px)·모바일(390px) 홈 화면을 확인한다.
