# seok jun.log archive

AI Agent 개발, SDD, 개발 방법론, 그리고 AI 시대에 대한 이야기를 다루는 개인 기술 블로그입니다. GitHub과 GitHub Pages에서 위키처럼 탐색할 수 있도록 정리했습니다.

## 사이트

- **GitHub Pages (빌드 후)**: https://seok-jun.github.io/ai-agent-diary/
  - 저장소 Settings → Pages → Source를 "GitHub Actions"로 설정하고 `main`에 push하면 `.github/workflows/pages.yml`이 자동으로 빌드/배포합니다.

## 문서 구성

- [전체 글 목록](./docs/index.md)
- [Agent SDD 실무 개발](./docs/series/agent-sdd/README.md) — AI Agent 실무 적용을 다룬 7편의 연재
- [AI에게 물어본 인간의 미래](./docs/series/ai-future-dialogue/README.md) — 프롤로그와 본편 7편으로 구성된 연재
- [단독 글](./docs/standalone/README.md) — 개발 및 AI 활용에 관한 독립 문서 3편

## 파일명 규칙

- 연재 문서는 `3자리 순번-주제-slug.md` 형식을 사용합니다.
- 단독 문서는 `YYYY-MM-DD-주제-slug.md` 형식을 사용합니다.
- README의 문서 제목과 링크는 실제 파일명 및 본문 제목을 기준으로 관리합니다.

## 기술 스택

- [Jekyll](https://jekyllrb.com/) + [Just the Docs](https://just-the-docs.com/) 테마
- 소스는 `docs/` 폴더, 배포는 GitHub Actions (`.github/workflows/pages.yml`)

## 원본

- Velog: https://velog.io/@hiha12ha/posts
- RSS: https://v2.velog.io/rss/@hiha12ha
