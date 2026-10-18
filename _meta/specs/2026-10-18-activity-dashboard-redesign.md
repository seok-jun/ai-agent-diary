# AI 개발 활동 대시보드 화면 개편

## 분류

- Priority: P2. Codex와 Claude Code 수치가 한 카드 묶음·한 표에 섞여 출처를 구분하기 어렵다.
- SDD grade: Medium. 공개 페이지의 구조·스타일·렌더링을 함께 바꾸지만 집계 계산과 공개 JSON은 그대로다.

## AS-IS

- Codex·Claude 기록 카드가 한 격자에 섞여 있고, 기간별 지표 5개가 같은 줄에 놓인다.
- 차트는 '비교 토큰' 선택에 따라 한 출처만 보여 Codex와 Claude를 함께 볼 수 없다.
- 비율 카드는 선택한 기준 하나만 보여 출처 간 비교가 어렵다.

## TO-BE

- **누적 사용량:** 도구별 카드 두 개(Codex 파랑, Claude Code 주황). 각 카드에 축약 총량과 그 도구의 기록만 둔다.
- **기간 선택:** 일별·월별·전체 세그먼트와 날짜 입력을 하나의 고정 도구 막대에 두고, 아래 모든 영역에 적용한다.
- **AI 토큰:** Codex·Claude Code·합계 지표와 두 도구를 쌓은 막대그래프(범례·툴팁).
- **GitHub 개발 활동:** 커밋·병합 PR·완료 이슈 지표와 병합 PR·완료 이슈를 나란히 둔 막대그래프. 단위가 같은 두 지표만 한 축을 공유한다.
- **토큰 100만 개당 병합·완료:** Codex·Claude Code·합계 세 줄을 한 표로 보여 주어 선택 메뉴를 없앤다. 각 줄에 비교한 기간을 함께 쓴다.
- **활동 내역:** 'AI 토큰'·'GitHub' 묶음 머리글로 출처를 구분한다. 일별 보기에서는 고른 날을 그 달 안에서 강조한다.
- 차트 색상은 dataviz 검증기로 색각 이상 구분·대비를 확인한다. 청록(병합 PR)은 대비가 3:1 미만이므로 범례·표로 보완한다.

## 영향 파일

- `docs/activity.md`, `docs/assets/activity/dashboard.js`, `docs/_sass/custom/custom.scss`, `_meta/activity/dashboard.test.cjs`

## 제약

- `select`·`history`·`comparison` 계산, 수집기, 공개 JSON 스키마, 워크플로, 내비게이션, 검색 설정은 바꾸지 않는다. 외부 차트 의존성을 추가하지 않는다.

## 검증 결과

- JavaScript 테스트 12개 통과(축 최댓값·토큰 합계 보조 함수 2개 추가). Sass 컴파일 통과.
- 배포 테마에 로컬 Markdown·JavaScript·CSS·JSON을 적용한 임시 미리보기에서 데스크톱 1280px·모바일 390px의 도구별 카드 2개, 지표 6개, 두 차트, 툴팁 색상 표시, 비율 표 3줄, 일별·월별·전체 전환, 일별 강조, 미수집 안내, 비율 표 가로 넘침 없음, 페이지 가로 넘침 없음, 브라우저 예외 없음을 확인했다. 스크린샷: `_meta/activity/screenshots/redesign-*.png`.
- 전체 Jekyll 빌드는 로컬 Ruby가 없어 Pages 워크플로에서 확인한다.
