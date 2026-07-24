---
title: "AI Engineer World's Fair 2026, Agentic Engineering 세션에서 나온 이야기들"
parent: Standalone
nav_order: 2
permalink: /standalone/2026-06-29-ai-engineer-worlds-fair-2026-agentic-engineering/
date: 2026-06-29
description: "AI Engineer World's Fair 2026의 Agentic Engineering 세션 여덟 개를 Harness, Skill, Agentic SDLC, Eval, Sandbox 관점에서 정리한 글."
---

# AI Engineer World's Fair 2026, Agentic Engineering 세션에서 나온 이야기들

2026년 6월 29일부터 7월 2일까지 샌프란시스코 Moscone West에서 AI Engineer World's Fair 2026이 열렸다. 이 글은 그중 Agentic Engineering 계열 세션 여덟 개를 정리한 것이다.

→ [공식 페이지](https://www.ai.engineer/worldsfair/2026)

먼저 밝혀둘 것이 있다. **나는 이 행사에 직접 참석하지 않았다.** 공식 일정 페이지에 공개된 세션 소개문, 발표사가 공개한 기술 문서, 공개된 트랙 영상을 기준으로 정리했다. 세션 초록이 없는 경우에는 해당 회사가 공개한 문서로 보완했고, 어디까지가 확인된 내용이고 어디부터가 해석인지는 각 항목과 글 마지막 표에 구분해 두었다.

전체를 관통하는 주제를 한 줄로 요약하면 이렇다. **모델 성능보다 그 모델을 감싸는 실행 구조(Harness)와 운영 체계로 논의가 옮겨갔다.**

---

## 1. Building on the Codex Harness

**발표자:** Dominik Kundel, OpenAI · **분야:** Harness Engineering
[일정](https://www.ai.engineer/worldsfair/schedule?q=Dominik+Kundel)

Codex는 CLI 프로그램 하나가 아니다. 모델 호출·도구 실행·승인·Sandbox·대화 상태를 관리하는 **공통 Harness**가 중심에 있고, CLI와 IDE Extension은 그 위에 얹힌 클라이언트다.

초기 Codex CLI는 터미널 UI와 Harness가 붙어 있는 구조였다. 여러 클라이언트에서 같은 실행 구조를 쓰기 위해 UI와 실행 엔진을 분리한 결과물이 **Codex App Server**다. App Server는 JSON-RPC 인터페이스로 다음을 공통 처리한다.

- 사용자 인증
- 대화 및 작업 이력
- 도구 실행 요청
- 승인 요청
- 실행 이벤트 스트리밍
- Sandbox 정책
- Agent 상태 관리

따라서 CLI와 IDE Extension은 서로 다른 Agent라기보다 **동일하거나 유사한 Harness를 서로 다른 클라이언트에서 사용하는 구조**에 가깝다. 모델, 승인 정책, Sandbox, MCP 같은 설정 계층도 공유한다.

이 구조를 알면 같은 도구인데 CLI와 IDE의 동작이 다를 때 원인을 좁힐 수 있다. 클라이언트가 주입하는 시스템 컨텍스트, Skill 탐색·로딩 방식, 작업 디렉터리와 파일 접근 범위, 승인·Sandbox 정책, 대화 상태 유지 방식, 프롬프트 직렬화 방식이 각각 달라질 수 있기 때문이다. **모델 성능 차이로만 설명하기 어려운 영역이다.**

**참고 자료**
- [Unlocking the Codex harness](https://openai.com/index/unlocking-the-codex-harness/)
- [Codex App Server](https://developers.openai.com/codex/app-server) · [Codex CLI](https://developers.openai.com/codex/cli) · [IDE Extension](https://developers.openai.com/codex/ide) · [설정 구조](https://developers.openai.com/codex/config-basic)

---

## 2. How Anthropic Builds: Lessons from Labs

**발표자:** Mike Krieger, Anthropic · **분야:** Harness Engineering
[일정](https://www.ai.engineer/worldsfair/schedule?q=Mike+Krieger) · [Day 4 Harness Engineering 트랙 영상](https://www.youtube.com/watch?v=I2cbIws9j10)

Anthropic Labs는 Claude Code, MCP, Skills, Claude in Chrome, Cowork처럼 기존 채팅 인터페이스를 넘어서는 실험적 제품을 빠르게 만들고 검증하는 조직이다.

Anthropic의 공개 자료에서 Agent는 단순한 모델 호출이 아니라 대략 세 요소의 결합으로 설명된다.

> Agent = 모델 세션 + Harness + 격리된 실행 환경

Claude Code 역시 파일을 읽고, 명령을 실행하고, 코드를 수정하고, 결과를 검증하는 실행 환경이다. 중요한 것은 모델의 추론 능력만이 아니라 Harness가 작업 상태를 어떻게 유지하고, 도구와 권한을 어떻게 제공하며, 장시간 작업을 어떻게 이어가게 하느냐다.

한 가지 흥미로운 지적이 있다. **모델이 발전할수록 기존 Harness의 가정이 빠르게 낡는다는 것이다.** 예전 모델에 필요했던 과도한 단계 분해나 복잡한 제어 로직이, 새 모델에서는 오히려 작업을 방해할 수 있다. Harness는 한 번 만들고 끝나는 게 아니라 모델 세대에 맞춰 덜어내야 하는 대상이라는 얘기다.

**참고 자료**
- [Anthropic Labs 소개](https://www.anthropic.com/news/introducing-anthropic-labs)
- [장기 실행 Agent Harness 설계](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Managed Agents](https://www.anthropic.com/engineering/managed-agents) · [Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)

---

## 3. 500 Skills, Zero Fine-Tuning

**발표자:** Ajay Prakash, LinkedIn · **분야:** Skills·Context Engineering
[일정](https://www.ai.engineer/worldsfair/schedule?day=3&session=363)

LinkedIn은 범용 Coding Agent가 사내 엔지니어링 환경을 이해할 수 있도록 **CAPTAIN이라는 MCP 서버**를 구축했다.

세션 소개문에 따르면 CAPTAIN은 수백 개의 도구를 Agent에게 한꺼번에 노출하는 대신 Meta-tool 3단계 구조를 쓴다.

1. **Discover** — 현재 작업에 필요한 Skill 검색
2. **Inspect** — Skill의 설명과 사용법 확인
3. **Execute** — 선택한 Skill 실행

각 Skill은 문서만 제공하는 것이 아니라 사내의 암묵적 지식과 반복 업무를 **실행 가능한 Workflow**로 표현한다. 이 방식으로 500개 이상의 Skill을 운영하고 있다고 설명한다.

핵심 주장은 모델을 별도로 Fine-tuning하지 않더라도, 적절한 Context와 Skill을 **작업 시점에 선택적으로** 제공하면 범용 Agent를 조직 환경에 적응시킬 수 있다는 것이다.

Skill 수가 늘어나면 문제의 무게중심이 작성에서 선택으로 옮겨간다. 어떤 요청에 어떤 Skill을 노출할지, 잘못 고르는 것을 어떻게 막을지, 여러 Skill을 어떻게 조합할지, 필요한 것만 Context에 로드할 수 있는지, Skill 변경이 기존 Workflow를 깨지 않는지, 성공률과 오작동을 어떻게 측정할지가 실제 과제가 된다. Skill을 프롬프트 조각이 아니라 **버전과 테스트를 가진 내부 소프트웨어 패키지**로 다뤄야 한다는 시사점이다.

> 500이라는 숫자는 발표사 자체 집계다. Skill 하나의 단위(파일 하나인지 워크플로 하나인지)를 알 수 없으므로 다른 조직 수치와 직접 비교하기는 어렵다.

---

## 4. Agentic SDLC at Uber: Building Blocks for Uber's Software Factory

**발표자:** Uday Kiran Medisetty, Adam Huda · **분야:** AI-Native Enterprise
[일정](https://www.ai.engineer/worldsfair/schedule?day=2&day=3&q=uber&track=AI-Native+Enterprises&track=Evals)

Uber는 Agent 활용을 코드 생성 단계에 한정하지 않고 소프트웨어 개발 생명주기 전체로 확장하고 있다. 세션 소개문이 제시한 흐름은 다음과 같다.

> 조사 및 Spec 작성 → 자율 코드 생성 → 검증 및 Validation → 코드 반영 → 운영 모니터링 → 결과를 다음 개발 Loop에 반영

이를 지원하는 공통 기반으로 Model Gateway, MCP Infrastructure, Agent Skills, Knowledge Systems, Cloud Developer Environments, 검증·관측 체계를 제시한다.

이 사례에서 눈여겨볼 것은 개별 Agent의 코딩 능력이 아니라 **각 단계를 연결하는 상태와 계약**이다. 이전 단계에서 확정된 결정, 아직 해결되지 않은 질문, 변경 대상 파일과 제외 대상, 구현 완료 조건, 실행한 테스트와 결과, Reviewer의 지적 사항, PR 이후 관측할 지표 같은 정보가 단계를 넘어가며 유지돼야 하기 때문이다.

정리하면 Agentic SDLC의 본질은 Agent를 많이 실행하는 것이 아니라 **단계 사이의 정보 손실을 줄이고 결과를 다음 단계의 입력으로 연결하는 것**에 가깝다.

> 소개문에는 엔지니어의 월간 AI 사용률, AI 관여 PR 비율, 완전 자율 생성 PR 비율 같은 수치도 나온다. 다만 발표자 측 제공 수치이고 "AI 관여"의 정의와 측정 기준이 함께 공개돼 있지 않아 이 글에는 옮기지 않았다.

---

## 5. Building Closed-Loop Evals for a Multimodal Agent at Uber Scale

**발표자:** Soumya Gupta, Jai Chopra · **분야:** Evals
[일정](https://www.ai.engineer/worldsfair/schedule?day=2&day=3&q=uber&track=AI-Native+Enterprises&track=Evals)

Uber는 음식 사진을 개선하는 Multimodal Agent를 사례로 Closed-Loop Eval을 설명한다.

이 Agent는 사진을 보기 좋게 만드는 것만으로는 충분하지 않다. 원래 음식의 형태를 유지해야 하고, 브랜드와 포장 정보를 훼손하면 안 되고, 서로 다른 음식 사진을 획일화하면 안 되고, 시각적 품질을 높이면서도 사실성을 유지해야 한다.

소개문은 이런 평가 과정에서 Agent가 측정 지표만 만족시키는 **Reward Hacking**이 발생할 수 있다고 지적한다. 이를 막기 위해 Offline Eval과 실제 사용자 반응 같은 Online Signal을 연결하고, 실행 결과를 다음 데이터·정책·Agent 변경에 되먹이는 Closed Feedback Loop를 구성한다.

일반적인 Eval이 이런 모양이라면,

> 테스트 입력 → 실행 → 기대 결과 비교 → 통과 또는 실패

Closed-Loop Eval은 한 단계 더 나아간다.

> 실제 작업 실행 → 실패·수정·리뷰 데이터 수집 → 실패 유형 분류 → Skill·Prompt·Harness·Eval Case 수정 → 재실행 → 운영 결과 확인

코딩 Agent에 대입하면 Loop의 입력이 될 데이터는 이미 개발 과정에 존재한다. Agent가 수정했지만 사람이 되돌린 코드, PR Review에서 반복되는 지적, 테스트는 통과했으나 운영에서 발생한 오류, 불필요하게 넓은 파일 수정, Reviewer Agent와 Executor Agent의 판단 불일치, 잘못 실행된 Skill, Agent가 반복적으로 되묻는 영역 같은 것들이다.

Eval을 출시 전 테스트 세트가 아니라 **운영 결과를 개선으로 되돌리는 지속적인 제어 시스템**으로 보는 관점이다.

---

## 6. Sandboxes Aren't Optional: Runtime Isolation Patterns for Coding Agents at Scale

**발표자:** Robert Brennan, OpenHands · **분야:** Sandbox & Platform Engineering
[일정](https://www.ai.engineer/worldsfair/schedule?track=Sandbox+%26+Platform+Engineering)

주장은 단순하다. **프롬프트에 "하지 마"라고 적는 것만으로는 실행을 안전하게 통제할 수 없다.** Agent가 명령어와 코드를 실행할 수 있다면 안전성은 프롬프트가 아니라 Runtime에서 강제해야 한다.

소개문이 다루는 통제 수단은 다음과 같다.

- Docker 또는 Kubernetes 기반 격리
- Agent별 파일시스템 범위 제한
- CPU·Memory·실행 시간 제한
- 외부 네트워크 Egress 통제
- 역할 기반 권한 관리
- Secret 접근 제한
- 명령과 파일 변경 Audit Trail
- Timeout 및 실패 시 Graceful Degradation
- 다수 Agent 병렬 실행 시 자원 통제

소개문은 프롬프트 지시를 무시한 Agent가 운영 데이터베이스를 손상시킨 사례를 문제의식으로 제시하고, 최대 50개의 Agent를 격리된 환경에서 병렬 실행하는 패턴을 다룬다고 설명한다.

특정 디렉터리 밖 파일 수정 금지, 운영 DB 접근 금지, 허용 도메인 외 네트워크 요청 금지, Secret 원문 읽기 금지, 승인 없는 Push·Merge·Deploy 금지, 시간·비용 초과 시 종료 — 이런 규칙은 프롬프트 지침이 아니라 시스템 정책으로 구현해야 한다는 것이 결론이다.

> 자율성은 신뢰를 전제로 주는 권한이 아니라, 통제된 환경 안에서 허용하는 실행 범위다.

---

## 7. What We Learned by Analyzing 1M AI-Generated PRs

**발표자:** Daksh Gupta, Greptile · **분야:** Software Factories
[일정](https://www.ai.engineer/worldsfair/schedule?track=Software+Factories) · [Day 2 Software Factories 트랙 영상](https://www.youtube.com/watch?v=htM02KMNZnk)

Greptile은 자사 Review 시스템을 통과한 End-to-End AI 생성 PR을 대규모로 분석했다고 설명한다. 발표 소개문에는 Agent별 코드 특성, 보안 문제, Review 과정에서 반복되는 패턴이 포함된다.

이 발표와 관련해 도구별 취약점 비교 수치가 여러 경로로 인용되는데, **인용 전에 기준선을 확인할 필요가 있다.** Greptile이 공개한 분석 글(Rise of the Overnight Agents, 2026년 5월)의 수치는 도구끼리의 비교가 아니라 **사람이 쓴 코드 대비 비율**이다.

<cite index="10-1">Claude 쪽에서 사람 대비 비율이 높은 항목은 IDOR / 테넌트 체크 누락 1.75배, 오래된 주석·잘못된 문서 1.69배, off-by-one 1.64배, XSS 1.57배였고, 인증 우회는 1.50배로 집계됐다. Codex는 환경변수·설정 버그 1.35배, 기존 기능 파손 1.34배, 로그에 시크릿 노출 1.34배처럼 설정과 파손 계열에서 사람보다 높았고 나머지 대부분은 사람 수준 이하였다. Devin은 환경변수·설정 버그를 제외하면 대부분 사람 수준 이하였다.</cite>

<cite index="8-1">판별 방식도 함께 봐야 한다. GitHub에서 봇이 작성자로 등록된 PR은 1% 미만이라, `Co-Authored-By` 푸터나 `codex/` 브랜치 접두사 같은 신호를 조합해 AI 생성 여부를 추정했다고 밝히고 있다.</cite> <cite index="10-1">이 방식으로 집계한 완전 AI 생성 PR 비율은 2025년 2월 0.86%에서 2026년 4월 27.6%로 올라갔다.</cite>

즉 판별 자체가 휴리스틱이고, 비교 기준선도 사람이다. 여기에 더해 각 도구의 버전, 도구가 맡은 작업의 난이도, 언어·프레임워크 분포, 생성 후 사람의 수정 여부, 취약점 판정 기준(정적 키워드 스윕인지 실제 검증인지), 조직별 Review 강도, 도구별 표본 수 차이를 확인하지 않으면 도구 성능 비교로 읽기 어렵다. 한쪽 도구에 더 복잡한 자율 작업을 맡기는 경향이 있었다면, 그 수치는 도구 성능이 아니라 작업 난이도를 재고 있는 것일 수 있다.

이 분석의 가치는 "어느 Agent가 낫다"는 순위보다 **AI 생성 코드가 실제 PR에서 어떤 실패 패턴을 만드는지**에 있다. 조직 내부에서도 Agent 생성 PR의 평균 변경 파일 수, 사람이 다시 수정한 비율, Review Comment 수와 유형, Merge 이후 Revert 비율, 보안 규칙 위반 수, 테스트 누락률, 중복 코드 발생률, 변경 후 문서 불일치율 같은 지표는 직접 측정할 수 있다.

---

## 8. Addy Osmani Closing Keynote

**트랙:** Autoresearch
[일정](https://www.ai.engineer/worldsfair/schedule?q=Addy+Osmani) · [Day 3 Autoresearch 트랙 영상](https://www.youtube.com/watch?v=4sX_He5c4sI)

공식 일정에 Closing Keynote로 등록돼 있고 Autoresearch 트랙에 포함돼 있다. 다만 **세션 설명이 아직 `TBD` 상태**라 발표 내용을 사전에 단정하기 어렵다.

Autoresearch라는 개념 자체는, Agent가 제한된 시간 동안 코드를 수정하고 실험을 실행해서 결과가 개선되면 변경을 유지하고 나빠지면 폐기하는 과정을 반복하는 구조를 가리킨다. [Karpathy의 공개 프로젝트](https://github.com/karpathy/autoresearch)가 대표적인 예다.

아래는 발표 요약이 아니라, 영상이 공개됐을 때 확인해볼 만한 질문 목록이다.

- Agent가 내부적으로 반복할 수 있는 범위는 어디까지인가
- 어떤 결과를 Agent가 스스로 판단할 수 있는가
- 언제 사람의 승인이 필요한가
- 실험 목표와 평가 지표는 누가 정의하는가
- 비용과 실행 시간은 어디에서 제한하는가
- Agent가 최적화 지표를 악용하지 않는지 누가 검증하는가

구조적으로는 Loop가 두 겹으로 나뉜다.

**Agent 내부 Loop**
> 분석 → 수정 → 실행 → 평가 → 유지 또는 폐기 → 재시도

**사람·조직 외부 Loop**
> 목표 설정 → 제약 정의 → 결과 검토 → 정책·Eval 변경 → 다음 작업 승인

내부 Loop가 아무리 빨라져도 목표, 권한, 평가 기준, 운영 반영 여부는 외부 Loop에서 관리해야 한다는 점에서 앞의 Sandbox·Eval 세션과 이어진다.

---

## 세션들에서 공통으로 보이는 방향

**1. 모델보다 Harness가 중요해지고 있다.** 모델은 추론을 담당하지만 실제 Agent 품질은 Context 선택, Skill Routing, 도구 제공, 실행 환경, 상태 유지, 승인 정책, Eval, 관측의 결합으로 결정된다. 같은 모델이라도 CLI, IDE, 사내 Agent Platform의 결과가 달라지는 이유다.

**2. Skill은 문서가 아니라 실행 가능한 조직 지식이다.** 명확한 Trigger, 입출력 계약, 의존 도구, 접근 권한, 버전, Owner, Eval Case, 성공·실패 기록을 갖는 관리 대상이 돼야 한다.

**3. Agentic SDLC는 코드 생성 자동화가 아니다.** 요구사항 → 분석 → 설계 → 구현 → 검증 → Review → PR → 운영 관측 → 개선을 연결하는 시스템이고, 코드 생성은 그중 일부다.

**4. Eval은 실행 전 검사가 아니라 운영 피드백 루프다.** 정적 테스트 케이스만으로는 실제 사용 중 발생하는 실패를 반영하기 어렵다. PR Review, 수정 이력, Revert, 장애, 사용자 피드백이 다시 Eval과 Skill로 돌아가야 한다.

**5. 자율성은 Sandbox와 함께 커진다.** Agent가 할 수 있는 일이 많아질수록 프롬프트 규칙이 아니라 최소 권한, 작업 영역 격리, Secret 관리, 네트워크 제한, 명령 기록, 비용 제한, 승인 Gate 같은 Runtime 통제가 필요하다.

**6. 사람의 역할이 코드 작성에서 목표 정의와 증거 검증으로 이동한다.** 문제와 목표 정의, 설계 선택, 위험도 판단, 승인 조건 설정, Eval 기준 정의, Agent가 제출한 증거 검증, 운영 반영 여부 결정이 사람의 몫이 된다. 다만 이건 선언으로 되는 게 아니라 "Agent가 어떤 증거를 어떤 형식으로 제출해야 하는가"를 규격으로 정의해야 성립한다.

---

## 종합하면 이런 구조가 그려진다

여러 세션의 내용을 겹쳐 보면 대략 다음 계층이 나온다. 특정 발표에서 제시된 단일 아키텍처가 아니라, 세션들을 종합해 정리한 그림이다.

```text
CLI / IDE / Web Client
          │
          ▼
Shared Agent Harness / App Server
          ├─ Session / State
          ├─ Approval Policy
          ├─ Context Builder
          └─ Skill Router
          │
          ▼
Skill Registry / Knowledge System
          ├─ Discover
          ├─ Inspect
          ├─ Execute
          └─ Eval / Version
          │
          ▼
Sandboxed Runtime
          ├─ Filesystem Scope
          ├─ Tool Permissions
          ├─ Network Policy
          ├─ Secret Broker
          └─ Resource Limits
          │
          ▼
SDD → Implementation → Test → Review → PR
          │
          ▼
Observability / Closed-Loop Eval
          └─ Skill·Prompt·Harness·Policy 개선
```

물론 이 전체를 한 번에 만드는 것은 현실적이지 않다. 세션들이 공통으로 강조한 우선순위를 순서로 옮기면 이 정도가 된다.

1. Skill별 Trigger·입출력·권한·Eval을 명시한다
2. Skill 선택과 실제 실행을 분리한다
3. 개발 단계별 산출물과 완료 조건을 정의한다
4. Executor와 Reviewer의 책임을 분리한다
5. Agent가 제출해야 하는 검증 증거를 표준화한다
6. 실행 환경의 파일·명령·네트워크 권한을 제한한다
7. PR Review 결과를 Eval Case로 다시 수집한다
8. Skill 성공률과 사람의 수정 비용을 측정한다

---

## 어떤 순서로 보면 좋을까

Agent 도구 체인과 Skill 설계에 관심이 있다면 이 순서를 추천한다. 관심사가 다르면 순서도 달라진다.

1. **Building on the Codex Harness** — CLI와 IDE Extension의 동작 차이, App Server, Skill 실행 경로
2. **500 Skills, Zero Fine-Tuning** — Skill이 수백 개일 때의 검색·선택·조합·평가
3. **Agentic SDLC at Uber** — Spec부터 운영 관측까지 조직 단위 워크플로
4. **Sandboxes Aren't Optional** — 자율 실행에 필요한 Runtime 통제
5. **Building Closed-Loop Evals** — 정적 Eval을 지속 개선 루프로 확장
6. **What We Learned by Analyzing 1M AI-Generated PRs** — AI 생성 코드의 실패 유형과 Review 지표
7. **How Anthropic Builds** — 제품·조직 차원의 Harness 운영
8. **Addy Osmani Closing Keynote** — 설명이 TBD이므로 영상 공개 후 확인

---

## 내용별 확인 상태

| 항목 | 확인 상태 |
|---|---|
| 행사 일정·장소·트랙 구성 | 공식 페이지 기준 |
| Codex Harness / App Server 구조 | OpenAI 공식 문서 기준 (세션 초록 아님) |
| Anthropic의 Agent·Harness 설명 | Anthropic 공개 엔지니어링 문서 기준 (세션 초록 아님) |
| LinkedIn CAPTAIN 구조, Skill 500개 이상 | 세션 소개문 기준, 발표사 자체 집계 |
| Uber Agentic SDLC 구성요소 | 세션 소개문 기준 |
| Uber의 AI 사용률·PR 비율 | 정의와 측정 기준 미공개라 본문에서 제외 |
| Uber Closed-Loop Eval 사례 | 세션 소개문 기준 |
| OpenHands Sandbox 패턴, Agent 50개 병렬 | 세션 소개문 기준 |
| Greptile 취약점 비율 | 공개 블로그 원문 확인, **비교 기준선은 다른 도구가 아니라 사람** |
| Addy Osmani Keynote 내용 | 미확인 (`TBD`). 본문의 Loop 구분은 발표 요약이 아니라 배경 개념 정리 |

세션 초록이 공개되지 않은 항목은 각 회사가 공개한 기술 문서로 보완했다. 문서와 실제 발표 내용이 다를 수 있으므로, 중요한 판단의 근거로 삼으려면 영상 공개 후 발표 본문을 직접 확인하는 편이 낫다.
