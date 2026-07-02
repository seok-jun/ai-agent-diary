# hiha12ha.log archive

Velog에 작성한 글을 GitHub에서 위키처럼 탐색할 수 있도록, 그리고 GitHub Pages로도 볼 수 있도록 정리한 문서 저장소입니다.

## 사이트

- **GitHub Pages (빌드 후)**: https://seok-jun.github.io/ai-agent-diary/
  - 저장소 Settings → Pages → Source를 "GitHub Actions"로 설정하고 `main`에 push하면 `.github/workflows/pages.yml`이 자동으로 빌드/배포합니다.

## 바로가기 (GitHub에서 바로 보기)

- [전체 글 목록](./docs/index.md)
- [Agent SDD 실무 개발](./docs/series/agent-sdd/README.md)
- [AI에게 물어본 인간의 미래](./docs/series/ai-future-dialogue/README.md)
- [단독 글](./docs/standalone/README.md)

## 정리 기준

- 원문 출처는 각 Markdown 파일의 front matter와 본문 상단에 보존했습니다.
- Velog RSS에 시리즈 메타데이터가 포함되어 있지 않아, 제목 패턴과 본문 연결 관계를 기준으로 분류했습니다.
- 연재 번호가 명확한 글은 시리즈 폴더에 묶고, 애매한 글은 `standalone`으로 분리했습니다.

## 기술 스택

- [Jekyll](https://jekyllrb.com/) + [Just the Docs](https://just-the-docs.com/) 테마
- 소스는 `docs/` 폴더, 배포는 GitHub Actions (`.github/workflows/pages.yml`)

## 원본

- Velog: https://velog.io/@hiha12ha/posts
- RSS: https://v2.velog.io/rss/@hiha12ha
