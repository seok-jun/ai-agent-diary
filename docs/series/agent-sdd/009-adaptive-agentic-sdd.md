---
title: "멀티 Agent 개발을 실제로 운영해보고 정리한 것들"
parent: Agent SDD 실무 개발
nav_order: 9
permalink: /series/agent-sdd/009-adaptive-agentic-sdd/
date: 2026-09-01
description: "기존 SDD 방식에 멀티 Agent 병렬 개발, 작업 격리, 검증 Gate를 실제로 적용해보면서 바뀐 운영 방식을 정리한 기록."
image: /assets/images/agent-sdd/009-adaptive-agentic-sdd/thumbnail.png
---

# 멀티 Agent 개발을 실제로 운영해보고 정리한 것들

_2026.09.01 게시_

![Adaptive Agentic SDD]({{ '/assets/images/agent-sdd/009-adaptive-agentic-sdd/thumbnail.png' | relative_url }})

예전 글에서 멀티 Agent 병렬 개발을 다음 단계로 적어둔 적이 있다.

그때는 executor / reviewer를 나누는 데까지 해봤고,<br>
`git worktree`를 이용해서 여러 작업을 동시에 돌리는 건 아직 운영 전이었다.

[Agent에게 바로 개발시키지 않기 — 실무에서 AI 개발을 안정화한 방식]({{ '/series/agent-sdd/002-agent-sdd-stabilizing-ai-development/' | relative_url }})

이번에는 실제 프로젝트에서 여러 이슈를 나누고,<br>
작업 공간도 따로 격리하고, 여러 Agent를 동시에 돌리고, 리뷰 Agent까지 분리해서 계속 써봤다.

해보고 나니까 생각보다 중요한 건 **몇 개를 동시에 돌릴 수 있느냐**가 아니었다.

**서로 따로 움직이는 Agent들이 같은 기준으로 판단하고, 마지막에는 한 방향으로 결과를 모을 수 있느냐가 더 중요했다.**

---

## 병렬로 돌리는 것 자체는 어렵지 않았다

처음에는 대충 이런 그림을 생각했다.

```text
Issue A -> Agent A ─┐
Issue B -> Agent B ─┼-> Merge
Issue C -> Agent C ─┘
```

실제로 `git worktree`를 쓰면 작업 디렉터리도 분리할 수 있다.

```text
Issue A -> Worktree A -> Agent A ─┐
Issue B -> Worktree B -> Agent B ─┼-> Merge
Issue C -> Worktree C -> Agent C ─┘
```

파일을 서로 밟는 문제는 확실히 줄었다.

그런데 worktree는 어디까지나 **작업 공간을 격리하는 도구**였다.

실제로 운영하려면 그 위에 다른 규칙이 더 필요했다.

| 필요했던 것 | 이유 |
| --- | --- |
| **Claim** | 같은 작업을 여러 Agent가 동시에 잡지 않게 |
| **변경 경계** | 다른 worktree라도 같은 모듈이나 계약을 건드릴 수 있음 |
| **판단 기준** | Issue, 코드, 과거 문서가 서로 다를 수 있음 |
| **검증 Gate** | Agent의 `완료했습니다`만으로는 부족함 |
| **Cleanup** | Merge 뒤 임시 문서와 작업 상태까지 정리해야 끝남 |

실제로 구현 Agent가 작업을 끝냈다고 판단했는데,<br>
별도 리뷰에서 인수 조건이 빠져 있거나 실제 동작이 기대와 다른 경우가 있었다.

코드가 작성됐고 테스트 일부가 통과했다는 것과<br>
**작업이 끝났다는 건 같은 의미가 아니었다.**

그래서 지금은 Agent의 완료 선언보다<br>
**인수 조건을 어떤 증거로 확인했는지**를 완료 기준으로 본다.

결국 병렬 Agent 개발은<br>
**Agent를 여러 개 띄우는 문제보다 작업의 경계와 완료 기준을 정하는 문제에 가까웠다.**

---

## 예전에 만든 등급 분류도 조금 다르게 보이기 시작했다

작업을 등급으로 나누는 건 예전부터 쓰고 있었다.

[AI한테 일을 시킬 때, 다 똑같이 다루면 안 되더라]({{ '/series/agent-sdd/001-ai-task-grading/' | relative_url }})

그때는 주로 **작업마다 프로세스를 얼마나 무겁게 가져갈지**에 초점이 있었다.

멀티 Agent로 실제 운영해보니 이 등급이<br>
Agent의 **분석·리뷰·검증 비용을 어디에 더 쓸지 정하는 기준**으로 좀 더 구체화됐다.

| Grade | 지금 적용하는 방식 |
| --- | --- |
| **Small** | 짧게 확인하고 바로 구현 + 대상 검증 |
| **Medium** | AS-IS / TO-BE + 검증 전략 |
| **Large** | 설계 검토 + 독립 코드 리뷰 |
| **Epic** | 먼저 작업 분할 |

핵심은 등급 이름이 아니다.

> **실패 비용이 큰 작업에는 더 많은 분석과 검증 비용을 쓰고, 작은 작업에는 그 비용을 강제하지 않는다.**

지금 내가 `Adaptive`라고 부르는 부분도 사실 이쪽에 더 가깝다.

---

## Source of Truth도 하나로 잡기 애매했다

Agent가 하나일 때보다 여러 개일 때 이 문제가 더 잘 보인다.

어떤 Agent는 Issue를 보고,<br>
어떤 Agent는 예전 SDD 문서를 보고,<br>
어떤 Agent는 현재 코드를 보고 판단한다.

셋이 서로 다른 내용을 말하면 뭘 믿어야 할까?

지금은 하나의 문서를 무조건 SSOT로 잡기보다<br>
**정보 종류마다 기준 출처가 다르다**고 보고 있다.

| 알고 싶은 것 | 먼저 볼 곳 |
| --- | --- |
| 이번 작업에서 뭘 바꿔야 하나? | 현재 Issue |
| 지금 실제로 어떻게 동작하나? | 현재 main 코드 |
| 어디까지 건드려도 되나? | Architecture / Agent Policy |
| UI가 어떻게 보여야 하나? | Visual Spec |
| 왜 예전에 이렇게 결정했나? | ADR / 결정 기록 |
| 구현 중 임시 계획은? | SDD 작업 문서 |

특히 현재 동작은 명확하게 잡았다.

> **AS-IS는 과거 문서가 아니라 현재 코드에서 다시 확인한다.**

문서는 오래될 수 있지만,<br>
현재 동작을 확인하는 질문에 대해서는 현재 코드가 가장 직접적인 증거이기 때문이다.

---

## Agent가 많이 읽는다고 항상 더 잘하는 것도 아니었다

이 부분은 예전에 따로 한번 측정해본 적이 있다.

[문서는 토큰 청구서를 크게 줄이지 않는다 — 대신 Agent가 헤매는 시간을 줄인다]({{ '/series/agent-sdd/005-docs-cut-agent-wandering-not-tokens/' | relative_url }})

이번에는 여기서 한 단계 더 나가서<br>
**탐색 범위를 운영 규칙으로 제한**하는 쪽으로 정리했다.

```text
Issue
  ↓
직접 관련 경로
  ↓
직접 Symbol
  ↓
공개 Contract
  ↓
Caller / Callee
  ↓
더 봐야 할 근거가 있을 때만 범위 확장
```

저장소 전체를 먼저 읽는 게 기본값은 아니다.

**필요한 곳에서 시작하고, 더 봐야 할 이유가 생겼을 때 넓힌다.**

Agent 하나일 때도 효과가 있었지만,<br>
여러 개를 동시에 돌릴 때는 이 차이가 훨씬 크게 느껴졌다.

여러 Agent가 각자 저장소 전체를 처음부터 탐색하기 시작하면<br>
생각보다 컨텍스트와 토큰 비용이 금방 커진다.

### 대안을 찾기 위해 일부러 탐색하지 않는다

이 흐름과 같이 정리된 게 `Trade-off Capture`다.

설계 문서를 채우기 위해 일부러 대안을 여러 개 만들어내지는 않는다.

분석 과정에서 **실제로 경쟁하는 선택지가 나타났을 때만**<br>
선택지와 비용, 최종 결정을 기록한다.

```text
Trade-off Discovery X
Trade-off Capture   O
```

대안 탐색 자체도 Agent의 컨텍스트와 추론 비용을 쓰기 때문이다.

---

## 지금은 이런 흐름으로 보고 있다

![멀티 Agent 실전 운영 흐름]({{ '/assets/images/agent-sdd/009-adaptive-agentic-sdd/workflow.png' | relative_url }})

예전에는 SDD를 하나의 긴 절차처럼 보는 느낌이 강했다.

지금은 **필요한 Gate를 작업 위험도에 따라 선택해서 타는 구조**에 더 가깝다.

```text
Issue
  ↓
Grade
  ↓
Claim
  ↓
Isolation
(worktree 등)
  ↓
Parallel Agents
  ↓
Review / QA
  ↓
Merge
  ↓
Cleanup
```

여기서 worktree는 전체 Workflow가 아니다.

**병렬 작업을 안전하게 하기 위한 Isolation 수단 중 하나**다.

그리고 실제 작업을 돌릴 때 계속 보는 기준은 대략 이 정도다.

| 원칙 | 한 줄로 |
| --- | --- |
| **Issue-first** | 현재 작업의 목표와 범위는 Issue에서 시작 |
| **Observed AS-IS** | 현재 동작은 현재 코드에서 확인 |
| **Risk-Adaptive** | 위험도에 따라 분석·검증 깊이를 다르게 |
| **Bounded Exploration** | 필요한 곳부터 보고 근거가 있을 때 확장 |
| **Evidence-Based Completion** | `완료했습니다`가 아니라 검증 결과로 판단 |
| **Lifecycle Completion** | Merge 이후 정리와 작업 해제까지 포함 |

안드로이드 앱을 실제로 개발하면서 쓰는 워크플로라<br>
실기기 QA도 Gate 중 하나로 두고 있다.

다만 모든 PR에 강제하지는 않는다.

실제 UI, 권한, 알림, 백그라운드 동작처럼<br>
테스트나 에뮬레이터만으로 확인하기 어려운 경우에만 Merge Gate로 둔다.

독립 리뷰도 마찬가지다.

Small 수정까지 매번 별도 Agent를 붙이면 오히려 비용만 늘어난다.

반대로 비용, 쿼터, 재시도 정책처럼<br>
잘못 구현했을 때 손해가 큰 작업은 독립 리뷰 비용을 쓰는 게 훨씬 싸다.

---

## Adaptive Agentic SDD

이렇게 실제로 쓰면서 바뀐 규칙들을 한 번 정리해둔 게<br>
`Adaptive Agentic SDD`다.

새로운 방법론을 만들겠다고 시작한 건 아니다.

기존에 쓰던 SDD에

```text
멀티 Agent
+ 작업 Claim
+ Isolation
+ 위험도별 Gate
+ 제한된 탐색
+ 완료 증거
+ Cleanup
```

이런 것들이 실제 운영 과정에서 하나씩 붙었고,<br>
겹치는 규칙은 다시 걷어내면서 지금 형태가 됐다.

전체 흐름과 템플릿은 아래 저장소에 정리해뒀다.

- [Adaptive Agentic SDD — 한국어](https://github.com/seok-jun/adaptive-agentic-sdd-ko)
- [Adaptive Agentic SDD — English](https://github.com/seok-jun/adaptive-agentic-sdd)

---

## 해보고 나서 바뀐 생각

예전에는 멀티 Agent 개발이라고 하면<br>
일단 **Agent를 많이 병렬로 돌리는 그림**부터 생각했다.

실제로 해보니 병렬성 자체는 생각보다 핵심이 아니었다.

> **각 Agent가 독립적으로 움직여도, 같은 기준으로 판단해서 결과를 하나로 합칠 수 있느냐가 더 중요했다.**

worktree도 그걸 위한 도구 중 하나였고,<br>
SDD도 그 기준을 잡는 방법 중 하나였다.

결국 중요한 건 도구를 많이 붙이는 게 아니라<br>
Agent가 어디까지 판단하고, 어디까지 탐색하고, 무엇을 증거로 작업을 끝낼지 정하는 쪽이었다.

그리고 이 규칙들도 계속 늘릴 생각은 없다.

실제로 사고를 막지 못하는 규칙이면 바꾸고,<br>
비용만 늘리는 절차라면 빼는 게 맞다고 본다.

**좋은 Agent Workflow는 규칙이 계속 늘어나는 게 아니라, 써볼수록 더 작고 정교해져야 하지 않을까 싶다.**
