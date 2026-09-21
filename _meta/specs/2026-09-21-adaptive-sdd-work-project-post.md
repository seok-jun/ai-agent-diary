# Adaptive SDD 실무 재적용 글 게시 명세

## AS-IS

- 게시할 원문은 첨부된 `pasted-text.txt`에 있으며 사이트에는 등록되지 않았다.
- 원격 최신 변경을 반영한 Agent SDD 연재와 홈의 시리즈 편수는 10편이다.
- 원문의 문자 도식 두 곳은 한글·영문 폭과 화면 너비에 따라 정렬이 어긋날 수 있다.

## TO-BE

- 원문을 2026-09-21자 Agent SDD 연재 11편으로 게시한다.
- 요청·반환 도식은 Markdown 표로 바꾸고, 시점별 도식은 바로 아래 표에 통합한다.
- 기존 표의 열 구조를 확인하고 한국어 본문, 수치, 출처를 보존한다.
- 홈과 연재 목록, 저장소 소개에 11편을 반영하고 기존 Pages 워크플로로 배포한다.

## 영향 파일

- `docs/series/agent-sdd/011-adaptive-sdd-work-project.md`
- `docs/series/agent-sdd/README.md`
- `docs/index.md`
- `README.md`

## 제약 조건

- front matter의 제목과 H1을 일치시키고 기존 날짜 및 permalink 관례를 따른다.
- 내부 링크는 후행 슬래시가 있는 permalink와 `relative_url`을 사용한다.
- 테마, 검색 설정, Pages 워크플로는 변경할 필요가 없다.
- 구현 후 별도 검토 단계에서 원문 보존, 목록과 URL, 표 렌더링을 확인한다.

## 검증 기준

- Jekyll 빌드와 `git diff --check`가 성공한다.
- 홈·연재 목록·사이드바에서 새 글을 열 수 있다.
- 표와 코드 블록이 정상 렌더링되며 데스크톱과 모바일에서 내용을 읽을 수 있다.
- 새 글의 내부 링크가 연결되고 한글·영문 검색에서 새 글을 찾을 수 있다.
- GitHub Pages 배포 완료 후 공개 URL에서 글을 확인한다.

## 백로그

- 현재 보류된 결정이나 후속 작업 없음.

## 후속 변경: 섬네일 추가

- AS-IS: 11편에는 전용 섬네일이 없고 공유 이미지도 사이트 기본값을 사용한다.
- TO-BE: 기존 연재의 밝은 배경·남색·초록색과 어울리는 가로형 섬네일을 생성해 글 상단과 공유 메타데이터에 연결한다.
- 영향 파일: 게시글, `docs/assets/images/agent-sdd/011-adaptive-sdd-work-project/thumbnail.png`, `_meta/image-prompts/011-adaptive-sdd-work-project.md`.
- 제약 조건: 원문과 표를 유지하고, 과밀한 도식 대신 Agent와 사람 사이의 요청·결과 전달을 표현한다.
- 검증 기준: 생성 이미지의 문자와 구성을 검토하고, 이미지 경로·공유 메타데이터·Pages 배포를 확인한다.
