---
title: "AI 코딩 에이전트를 제대로 통제하는 방법"
parent: Standalone
nav_order: 2
permalink: /standalone/2026-05-07-controlling-ai-coding-agents/
date: 2026-05-07
description: "AI 코딩 에이전트를 신뢰하되 통제하는 실무 원칙 — 에이전트를 안전하게 다루기 위한 지침 정리."
image: /assets/images/standalone/2026-05-07-controlling-ai-coding-agents/thumbnail.png
---

# AI 코딩 에이전트를 제대로 통제하는 방법

_2026.05.07 게시_

![AI 코딩 에이전트를 제대로 통제하는 방법]({{ '/assets/images/standalone/2026-05-07-controlling-ai-coding-agents/thumbnail.png' | relative_url }})

AI 코딩 도구를 쓰다 보면 묘한 순간을 자주 만난다.

간단한 수정만 요청했는데 갑자기 구조를 바꾸고,
요청하지 않은 리팩토링을 하고,
도메인 규칙을 모르는 상태에서 그럴듯한 코드를 만들어낸다.

Claude Code, Codex, Cursor 같은 AI 코딩 에이전트가 강력해진 것은 맞다. 하지만 실무에서 중요한 것은 단순히 "코드를 잘 짜는가"가 아니다. 더 중요한 질문은 이것이다.

> AI가 건드리면 안 되는 코드를 건드리지 않게 만들 수 있는가?

이 문제의식에서 나온 대표적인 방식이 `CLAUDE.md`이고, Codex에서는 같은 역할을 `AGENTS.md`가 담당한다.

---

## 1. CLAUDE.md란 무엇인가?

`CLAUDE.md`는 Claude Code가 프로젝트를 작업할 때 참고하는 프로젝트 지침 파일이다. Anthropic의 Context Engineering 글에 따르면 Claude Code는 `CLAUDE.md`를 초기 컨텍스트에 넣고, 이후 `glob`, `grep` 같은 도구로 필요한 파일을 탐색하는 하이브리드 방식을 사용한다. 즉, `CLAUDE.md`는 단순한 메모 파일이 아니라 AI 에이전트가 프로젝트를 이해하고 행동하는 기준점이다.

Claude Code 공식 문서에 따르면 `CLAUDE.md` 파일은 세션 시작 시 전체가 로드되며, **파일이 200줄을 넘으면 컨텍스트 소모가 커지고 지침 준수율이 떨어질 수 있다**고 명시되어 있다. 또한 `/memory` 명령을 통해 현재 세션에 로드된 메모리 파일을 직접 확인하고 편집할 수 있다.

핵심은 이렇다.

> **CLAUDE.md = Claude Code에게 주는 프로젝트 작업 규칙**

예를 들면 다음과 같은 내용을 넣을 수 있다.

```markdown
# CLAUDE.md

## 기본 원칙

- 요청받은 범위만 수정한다.
- 관련 없는 리팩토링, 포맷팅, 파일 이동은 하지 않는다.
- 기존 코드 스타일과 네이밍을 우선한다.
- 요구사항이 애매하면 구현 전에 가정을 명시한다.
- 변경 후에는 수정 파일, 수정 이유, 검증 방법을 요약한다.
```

---

## 2. 카파시 스타일 CLAUDE.md의 핵심

최근 많이 언급되는 "카파시 CLAUDE.md"는 한 가지 오해가 있다. **Andrej Karpathy 본인이 직접 만든 파일이 아니다.** Karpathy가 2026년 1월 26일 X에 올린 LLM 코딩 에이전트의 실패 패턴 관찰 글을 바탕으로, 개발자 Forrest Chang이 정리한 [`forrestchang/andrej-karpathy-skills`](https://github.com/forrestchang/andrej-karpathy-skills) 저장소의 `CLAUDE.md`다. Karpathy는 이 저장소를 직접 만들지도, 공식적으로 보증하지도 않았다는 점을 알아두는 것이 좋다.

해당 저장소는 네 가지 원칙을 중심으로 LLM 코딩 실수를 줄이려는 목적을 가진다.

1. Think Before Coding
2. Simplicity First
3. Surgical Changes
4. Goal-Driven Execution

### 2.1 Think Before Coding

구현 전에 먼저 생각하라는 원칙이다.

AI 코딩 에이전트는 요구사항이 애매해도 조용히 하나의 해석을 선택하고 그대로 구현하는 경우가 많다. 그래서 구현 전에 가정을 명시하고, 해석이 여러 개라면 대안을 제시하고, 더 단순한 방법이 있다면 사용자에게 말해야 한다.

**나쁜 요청 예시:**

> 할인 로직 추가해줘.

**좋은 요청 예시:**

> 할인 로직을 추가해줘. 구현 전에 아래 항목을 먼저 확인해줘.
>
> 1. 현재 할인 로직이 어디에서 계산되는지 설명
> 2. 즉시 할인과 예약 할인이 분리되어 있는지 확인
> 3. 외부몰 할인값과 내부 DB 할인값 중 어느 쪽이 우선인지 가정 명시
> 4. 변경 대상 파일 후보와 변경하지 말아야 할 파일 명시
> 5. 구현 전에 간단한 수정 계획 제시

이렇게 요청하면 AI가 바로 코드를 고치기보다 먼저 구조를 파악하고, 위험한 가정을 드러내게 된다.

### 2.2 Simplicity First

필요한 최소 코드만 작성하라는 원칙이다.

AI는 작은 요구사항에도 추상화 계층을 새로 만들거나, 설정 파일을 추가하거나, 재사용 가능성을 과하게 고려하는 경향이 있다. 하지만 운영 중인 레거시 프로젝트에서는 "좋아 보이는 구조 변경"이 오히려 장애 리스크가 될 수 있다.

**나쁜 결과 예시 — 요청: 특정 API 응답 필드 하나 추가**

- 공통 `ResponseWrapper` 신규 생성
- 기존 Controller 응답 구조 변경
- DTO 계층 재설계
- 기존 테스트 대량 수정

**좋은 결과 예시 — 요청: 특정 API 응답 필드 하나 추가**

- 기존 DTO에 필요한 필드만 추가
- 해당 필드를 채우는 Service 로직만 최소 수정
- 기존 응답 구조는 유지
- 변경된 필드 검증 테스트만 추가

실무에서는 "확장 가능성"보다 "이번 변경의 정확성"이 더 중요할 때가 많다.

### 2.3 Surgical Changes

필요한 부분만 외과수술처럼 고치라는 원칙이다.

이 원칙은 레거시 SI 프로젝트에서 특히 중요하다. 기존 코드가 마음에 들지 않아도, 요청받지 않은 부분은 건드리지 않아야 한다. `andrej-karpathy-skills`의 원칙도 인접 코드, 주석, 포맷팅을 임의로 개선하지 말고, 기존 스타일을 따르며, 무관한 dead code는 삭제하지 말고 언급만 하라고 정리한다.

**나쁜 예시:**

```diff
- if (StringUtils.isNotEmpty(prodCd)) {
-     result = productService.getProduct(prodCd);
- }
+ Optional.ofNullable(prodCd)
+     .filter(StringUtils::isNotEmpty)
+     .map(productService::getProduct)
+     .ifPresent(value -> result = value);
```

요구사항이 "상품 조회 조건 하나 추가"였는데 기존 스타일을 함수형으로 바꾸면, 의도하지 않은 영향이 생길 수 있다.

**좋은 예시:**

```diff
  if (StringUtils.isNotEmpty(prodCd)) {
+     if ("Y".equals(useYn)) {
          result = productService.getProduct(prodCd);
+     }
  }
```

기존 코드 스타일을 유지하면서 요구사항과 직접 연결된 부분만 고치는 방식이다.

### 2.4 Goal-Driven Execution

명령이 아니라 성공 기준을 주라는 원칙이다.

"버그 고쳐줘"라고 하면 AI는 구현부터 하려 한다. 반면 "실패 테스트를 먼저 만들고, 그 테스트가 통과하도록 수정해줘"라고 하면 훨씬 검증 가능한 방식으로 움직인다.

**나쁜 요청:**

> 버그 고쳐줘.

**좋은 요청:**

> 아래 버그를 수정해줘.
>
> **성공 기준:**
>
> 1. 현재 버그를 재현하는 테스트를 먼저 작성한다.
> 2. 테스트가 실패하는 것을 확인한다.
> 3. 최소 수정으로 테스트를 통과시킨다.
> 4. 기존 테스트가 깨지지 않는지 확인한다.
> 5. 수정 파일, 수정 이유, 검증 결과를 요약한다.

이 방식은 AI에게 "무엇을 할지"보다 "언제 성공으로 볼지"를 알려준다.

---

## 3. Codex에서는 CLAUDE.md가 아니라 AGENTS.md

Codex에도 같은 개념이 있다. 다만 파일명이 다르다.

- **Claude Code** = `CLAUDE.md`
- **Codex** = `AGENTS.md`

OpenAI 공식 문서에 따르면 Codex는 작업을 시작하기 전에 `AGENTS.md` 파일을 읽는다. 전역 지침과 프로젝트별 지침을 계층적으로 합쳐서 매 작업마다 일관된 기대치를 제공하는 구조다.

Codex의 탐색 순서는 대략 다음과 같다.

**1. 전역 범위**

```text
~/.codex/AGENTS.override.md
또는
~/.codex/AGENTS.md
```

**2. 프로젝트 범위**

Git 루트부터 현재 작업 디렉토리까지 내려오며 다음 순서로 탐색한다.

```text
AGENTS.override.md
AGENTS.md
project_doc_fallback_filenames에 정의된 fallback 파일명
```

**3. 병합 순서**

루트에서 현재 디렉토리 방향으로 합쳐지며, 더 가까운 디렉토리의 지침이 나중에 붙으므로 우선 적용된다.

OpenAI 문서에서는 Codex가 빈 파일은 건너뛰고, 기본적으로 `project_doc_max_bytes` 값인 32 KiB 한도까지 지침을 합친다고 설명한다. 지침이 잘리면 한도를 늘리거나, 하위 디렉토리별로 파일을 나누는 방식을 사용할 수 있다.

---

## 4. AGENTS.md는 AI용 README다

AGENTS.md 공식 사이트([agents.md](https://agents.md/))는 이 파일을 **"coding agents를 위한 README"**라고 설명한다. 사람을 위한 `README.md`와 달리, `AGENTS.md`에는 빌드 단계, 테스트 명령, 코드 컨벤션, 작업 시 주의사항처럼 AI 에이전트가 작업할 때 필요한 정보를 담는다.

즉 이렇게 나눠 생각하면 좋다.

**README.md**

- 사람을 위한 프로젝트 설명
- 실행 방법
- 기여 방법
- 주요 기능 소개

**AGENTS.md**

- AI 에이전트를 위한 작업 규칙
- 수정 가능 범위
- 수정 금지 영역
- 빌드, 테스트, 린트 명령
- 도메인 규칙
- 검증 기준

---

## 5. Codex용 AGENTS.md 예시

아래는 Java, Spring, MyBatis, Oracle, React 프로젝트에서 사용할 수 있는 예시다.

```markdown
# AGENTS.md

## 역할

이 프로젝트에서 Codex는 기존 운영 코드를 안전하게 수정하는 보조 개발자 역할을 한다.
빠른 구현보다 정확성, 최소 변경, 검증 가능성을 우선한다.

## 기본 원칙

- 요청받은 범위만 수정한다.
- 관련 없는 리팩토링, 포맷팅, 파일 이동은 하지 않는다.
- 기존 코드 스타일과 네이밍을 우선한다.
- 요구사항이 애매하면 구현 전에 가정을 명시한다.
- 여러 해석이 가능하면 조용히 하나를 선택하지 말고 대안을 제시한다.
- 변경 후에는 수정 파일, 수정 이유, 검증 방법, 남은 리스크를 요약한다.
- 실행하지 못한 검증은 반드시 "실행하지 못함"으로 표시한다.

## Java / Spring 규칙

- 기존 Service, Mapper, DTO 구조를 임의로 재설계하지 않는다.
- 동일 클래스 멤버 접근 시 기존 스타일에 맞춰 this. 사용을 유지한다.
- 새 의존성 추가는 사용자 확인 없이 하지 않는다.
- 운영 로직은 최소 변경 원칙을 따른다.
- 예외 처리는 기존 프로젝트 스타일을 따른다.

## MyBatis / Oracle SQL 규칙

- MyBatis XML의 기존 SQL 스타일을 유지한다.
- Oracle SQL에서 인덱스 사용성을 해칠 수 있는 불필요한 함수 적용을 피한다.
- WHERE 조건의 컬럼에 불필요하게 TRUNC, TO_CHAR 등을 적용하지 않는다.
- 기존 쿼리를 전체 재작성하지 말고, 요구사항에 필요한 조건만 최소 수정한다.
- 성능 영향이 예상되면 수정 전에 설명한다.

## React / TypeScript 규칙

- 기존 컴포넌트 구조와 hook 사용 방식을 유지한다.
- 타입 오류를 우회하기 위해 any를 남발하지 않는다.
- LCP, CLS, lazy loading, Suspense, Swiper 관련 코드는 임의로 구조 변경하지 않는다.
- React Query 옵션을 변경할 때는 refetch, cache, staleTime 영향 범위를 설명한다.

## 수정 금지 영역

- 사용자 요청과 직접 관련 없는 공통 유틸
- 전역 설정 파일
- 빌드 설정
- 배포 스크립트
- 외부몰 연동 공통 모듈
- 정산, 가격, 재고, 할인 핵심 로직

단, 요청받은 작업에 반드시 필요하다면 수정 전에 이유를 설명한다.

## 검증 규칙

가능한 경우 아래 검증을 수행한다.

- Java 변경: 관련 테스트 또는 최소한 컴파일 영향 확인
- TypeScript 변경: typecheck 실행
- React 변경: lint 또는 build 확인
- SQL 변경: 실행 계획 또는 예상 인덱스 영향 설명

## 완료 보고 형식

1. 변경 파일
2. 변경 요약
3. 검증 결과
4. 실행하지 못한 검증
5. 남은 리스크
```

---

## 6. 폴더별 AGENTS.md 구조 예시

큰 프로젝트에서는 루트 `AGENTS.md` 하나에 모든 내용을 넣는 것보다, 영역별로 나누는 것이 좋다.

```text
project-root/
├── AGENTS.md
├── backend/
│   └── AGENTS.md
├── frontend/
│   └── AGENTS.md
├── batch/
│   └── AGENTS.md
└── docs/
    ├── domain-rules.md
    ├── build-and-test.md
    └── external-marketplace.md
```

루트에는 공통 원칙을 둔다.

```markdown
# AGENTS.md

## 공통 원칙

- 최소 변경을 우선한다.
- 기존 스타일을 유지한다.
- 요청하지 않은 리팩토링은 하지 않는다.
- 변경 후 검증 결과를 요약한다.

## 참고 문서

- docs/domain-rules.md
- docs/build-and-test.md
- docs/external-marketplace.md
```

백엔드 폴더에는 Java와 SQL 규칙을 둔다.

```markdown
# backend/AGENTS.md

## Backend 규칙

- Spring Service 구조를 임의로 재설계하지 않는다.
- MyBatis Mapper XML은 기존 스타일을 유지한다.
- Oracle SQL 수정 시 인덱스 영향 가능성을 설명한다.
- 외부몰 연동 로직은 최소 변경 원칙을 따른다.
```

프론트엔드 폴더에는 React 규칙을 둔다.

```markdown
# frontend/AGENTS.md

## Frontend 규칙

- 기존 컴포넌트 구조를 유지한다.
- LCP, CLS 관련 코드는 임의로 변경하지 않는다.
- React Query 옵션 변경 시 refetch 조건을 설명한다.
- Swiper 설정 변경 시 초기 렌더링과 lazy loading 영향을 설명한다.
```

이렇게 나누면 Codex가 현재 작업 디렉토리에 가까운 지침을 더 강하게 참고할 수 있다. OpenAI 문서에서도 하위 디렉토리에 `AGENTS.override.md` 또는 `AGENTS.md`를 두어 세부 규칙을 적용하는 방식을 설명한다.

---

## 7. 좋은 지시문 예시

`AGENTS.md`를 만들어도 사용자의 요청이 너무 추상적이면 AI가 흔들릴 수 있다. 아래처럼 성공 기준을 함께 주는 것이 좋다.

### 예시 1: 버그 수정

**나쁜 요청:**

> 이 버그 고쳐줘.

**좋은 요청:**

> 상품 상세에서 특정 옵션 선택 시 가격이 잘못 표시되는 버그를 수정해줘.
>
> **작업 순서:**
>
> 1. 현재 가격 계산 흐름을 먼저 설명
> 2. 버그가 발생할 수 있는 지점 후보를 나열
> 3. 가장 작은 수정 범위를 제안
> 4. 수정 후 영향 범위 설명
> 5. 가능하면 테스트 또는 검증 방법 제시
>
> **주의:**
>
> - 공통 가격 계산 유틸은 임의로 리팩토링하지 말 것
> - 요청과 무관한 포맷팅 변경 금지

### 예시 2: SQL 수정

**나쁜 요청:**

> 이 쿼리 성능 개선해줘.

**좋은 요청:**

> 아래 Oracle SQL의 성능 개선 가능성을 검토해줘.
>
> **요구사항:**
>
> 1. 먼저 현재 쿼리의 병목 가능성을 설명
> 2. 인덱스 사용을 방해하는 조건이 있는지 확인
> 3. 쿼리 전체 재작성보다 최소 변경안을 우선 제안
> 4. 변경 전후 차이를 diff 형태로 보여줘
> 5. 실행 계획을 확인하지 못하면 그 한계를 명시해줘
>
> **주의:**
>
> - 비즈니스 결과가 바뀌면 안 됨
> - WHERE 조건 의미를 임의로 변경하지 말 것

### 예시 3: React 성능 개선

**나쁜 요청:**

> LCP 개선해줘.

**좋은 요청:**

> 메인 hero 영역의 LCP 개선안을 검토하고 최소 수정으로 적용해줘.
>
> **작업 순서:**
>
> 1. 현재 hero 컴포넌트 렌더링 구조 설명
> 2. LCP에 영향을 줄 수 있는 요소 확인
> 3. 이미지 loading, fetchpriority, width, height, aspect-ratio 적용 가능성 검토
> 4. 첫 번째 hero만 eager 처리하고 나머지는 기존 lazy 전략 유지
> 5. CLS 영향이 생기지 않는지 설명
>
> **주의:**
>
> - Swiper 구조를 전체 재작성하지 말 것
> - 기존 lazy rendering 전략을 임의로 제거하지 말 것
> - 관련 없는 카드 컴포넌트 수정 금지

---

## 8. CLAUDE.md와 AGENTS.md의 차이 정리

| 구분           | Claude Code                                  | Codex                                      |
| -------------- | -------------------------------------------- | ------------------------------------------ |
| 대표 지침 파일 | `CLAUDE.md`                                  | `AGENTS.md`                                |
| 목적           | Claude Code의 프로젝트 기억과 작업 규칙 제공 | Codex의 프로젝트별 작업 규칙 제공          |
| 적용 범위      | Claude Code 세션                             | Codex CLI, IDE extension, Codex app        |
| 핵심 내용      | 프로젝트 규칙, 도메인 규칙, 행동 원칙        | 빌드, 테스트, 수정 범위, 컨벤션, 검증 기준 |
| 주의점         | 200줄 초과 시 지침 준수율 저하 가능          | 기본 32 KiB 한도 내에서 지침 병합          |

Codex CLI는 로컬 터미널에서 실행되며 선택한 디렉토리의 코드를 읽고, 수정하고, 명령을 실행할 수 있다. 따라서 `AGENTS.md`에는 "어떤 명령을 실행해도 되는지", "어떤 파일은 건드리면 안 되는지", "어떤 검증을 해야 하는지"를 명확히 적는 것이 중요하다.

> **두 도구를 모두 쓴다면?**
> AGENTS.md는 이미 Cursor, Codex, Factory, Amp, Jules 등 다수 도구가 표준으로 채택한 포맷이다. 하나의 `AGENTS.md`를 두고, Claude Code의 `CLAUDE.md`에서 `AGENTS.md` 형태로 import 하거나 동일 내용을 심볼릭 링크로 공유하는 방식도 고려할 수 있다.

---

## 9. AGENTS.md와 Skills의 차이

Codex에는 `AGENTS.md` 외에도 Skills라는 개념이 있다. OpenAI 문서에 따르면 Skill은 `SKILL.md`와 선택적 스크립트, 참고 자료를 포함하는 디렉토리이며, Codex가 특정 작업에 필요한 워크플로우를 안정적으로 따르도록 돕는다. 또한 Codex는 처음부터 모든 Skill 본문을 읽는 것이 아니라, 이름, 설명, 파일 경로를 먼저 보고 필요할 때 전체 `SKILL.md`를 로드하는 progressive disclosure 방식을 사용한다.

차이는 이렇게 보면 된다.

**AGENTS.md**

- 프로젝트 전체의 기본 작업 규칙
- 항상 참고해야 하는 개발 컨벤션
- 수정 범위, 검증 기준, 금지 행동

**Skill**

- 특정 작업을 위한 재사용 가능한 절차
- 예: SQL 튜닝 절차
- 예: LCP 개선 절차
- 예: 외부몰 상품 등록 검증 절차

실무에서는 둘을 같이 쓰는 것이 좋다.

- **AGENTS.md** = 기본 헌법
- **Skill** = 반복 작업용 플레이북
- **테스트, 빌드, 린트** = 실제 게이트
- **PR 리뷰** = 최종 안전장치

---

## 10. 실무 적용 순서

처음부터 거창하게 만들 필요는 없다. 아래 순서로 시작하는 것이 좋다.

### 1단계: 루트 AGENTS.md 생성

```text
project-root/
└── AGENTS.md
```

처음에는 네 가지만 넣어도 충분하다.

```markdown
# AGENTS.md

## 기본 원칙

- 요청받은 범위만 수정한다.
- 관련 없는 리팩토링은 하지 않는다.
- 기존 코드 스타일을 유지한다.
- 변경 후 검증 방법을 명시한다.
```

### 2단계: 빌드와 테스트 명령 추가

```markdown
## 검증 명령

- Backend build: `./gradlew build`
- Backend test: `./gradlew test`
- Frontend install: `pnpm install`
- Frontend typecheck: `pnpm typecheck`
- Frontend lint: `pnpm lint`
```

실제 프로젝트 명령에 맞게 수정해야 한다.

### 3단계: 수정 금지 영역 추가

```markdown
## 수정 금지 영역

- 배포 스크립트
- 운영 환경 설정
- 정산 로직
- 가격 계산 공통 모듈
- 외부몰 연동 공통 유틸

필요한 경우 수정 전에 이유를 설명한다.
```

### 4단계: 도메인 문서 연결

```markdown
## 참고 문서

작업 전 필요한 경우 아래 문서를 먼저 읽는다.

- docs/domain-rules.md
- docs/external-marketplace.md
- docs/build-and-test.md
```

### 5단계: 하위 폴더별 규칙 분리

```text
backend/AGENTS.md
frontend/AGENTS.md
batch/AGENTS.md
```

프로젝트가 커질수록 루트 파일 하나에 모든 규칙을 넣는 것보다, 하위 영역별로 나누는 방식이 유지보수에 유리하다.

---

## 결론

`CLAUDE.md`와 `AGENTS.md`의 핵심은 프롬프트 기술이 아니다. 본질은 AI 코딩 에이전트에게 **"작업 규율"**을 부여하는 것이다.

AI는 코드를 빠르게 만들 수 있다. 하지만 실무에서는 빠른 코드보다 안전한 변경이 더 중요하다. 특히 레거시 시스템, 외부몰 연동, 가격, 재고, 정산, 배치, 운영 SQL 같은 영역에서는 AI가 임의로 코드를 개선하는 순간 리스크가 커진다.

그래서 AI 코딩 에이전트를 실무에 붙일 때는 다음 구조가 필요하다.

- **AGENTS.md 또는 CLAUDE.md** → AI의 기본 행동 규칙
- **도메인 문서** → 업무 규칙과 예외 조건
- **테스트, 빌드, 린트** → 기계적 검증 장치
- **PR 리뷰** → 최종 판단

결국 중요한 것은 이것이다.

> AI에게 "코드를 짜라"고만 지시하지 말고,
> **"어디까지 생각하고, 어디까지 고치고, 어떻게 검증해야 하는지"**를 알려줘야 한다.

이것이 `CLAUDE.md`와 `AGENTS.md`가 중요한 이유다.

---

## 참고 자료

- [AGENTS.md 공식 사이트](https://agents.md/) — coding agent를 위한 README 성격의 공개 포맷.
- [OpenAI Codex 공식 문서: Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md) — Codex는 작업 전 AGENTS.md를 읽고, 전역 지침과 프로젝트별 지침을 계층적으로 병합한다.
- [Anthropic Claude Code Memory 문서](https://code.claude.com/docs/en/memory) — CLAUDE.md는 세션 시작 시 전체 로드되며, 200줄 초과 시 컨텍스트 소모와 지침 준수율 저하 가능.
- [Anthropic Context Engineering 글](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Claude Code는 CLAUDE.md를 초기 컨텍스트에 넣고, 이후 파일 탐색 도구로 필요한 정보를 찾는 하이브리드 방식을 사용한다.
- [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) — Karpathy의 LLM 코딩 실패 패턴 관찰을 바탕으로 Forrest Chang이 정리한 네 가지 원칙 CLAUDE.md 저장소. (Karpathy 본인의 저장소가 아님)
